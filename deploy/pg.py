from __future__ import absolute_import

import os
import tempfile

from fabric.api import (
    abort, env, execute, get, hide, put, settings, sudo, task
)
from fabric.contrib import django as _django

from .lib.tasks import DefaultTargetTask
from .lib.utils import local, pgrun, run, set_db_envs, set_remote_tempfile
from .lib.notify import created, notify_ok


@task()
@task(task_class=DefaultTargetTask)
def setup():
    "Install psycopg supporting pacakges and create the cache database"
    with hide('stdout'):
        sudo('aptitude -y install python-dev libpq-dev')
    notify_ok('Installed python-dev and libpq-dev packages.')
    execute(create_cache_db)


@task(task_class=DefaultTargetTask)
def create_db():
    "Create the database"
    with hide('everything'):
        set_db_envs()
    pg_cmd = (
        'if ! psql -l | grep -w -q {db_name}; then '
        'createdb -O {db_user} {db_name}; fi'
    ).format(**env)
    if env.is_remote:
        sudo(pg_cmd, user='postgres')
    else:
        local(pg_cmd)
    created(env.db_name)


@task(task_class=DefaultTargetTask)
def create_cache_db():
    "Create the cache database"
    pg_cmd = (
        'if ! psql -l | grep -w -q {cache_db}; then '
        'createdb -O etsidata {cache_db}; fi'
    ).format(**env)
    sudo(pg_cmd, user='postgres')
    created(env.cache_db)


@task()
def local_drop():
    """
    Drop the local database
    """
    with hide('everything'):
        set_db_envs()
    local('dropdb {db_name}'.format(**env))
    notify_ok('Database "{db_name}" dropped!'.format(**env))


@task(task_class=DefaultTargetTask)
def drop_db():
    "Drop the database"
    with hide('everything'):
        set_db_envs()
    pg_cmd = (
        'if psql -l | grep -w -q {db_name}; then dropdb {db_name}; fi'
    ).format(**env)
    sudo(pg_cmd, user='postgres')
    notify_ok('Database "{db_name}" dropped!'.format(**env))


def _pg_dump(dumpfile, *tables):
    with hide('everything'):
        set_db_envs()
    pg_cmd = "pg_dump -Fc -Z9 -O -x -h {db_host} -U {db_user} -f {dumpfile} ".\
        format(dumpfile=dumpfile, **env)
    if tables:
        pg_cmd += '-t {} '.format(' -t '.join(tables))
    pg_cmd += '{db_name}'.format(**env)

    pgrun(pg_cmd)


@task(task_class=DefaultTargetTask)
def dump(dumpfile, *tables):
    """
    pg_dump the target DB to the specified remote file, optionally specifying
    db tables:
    `pg.dump:<remote_file_path>,[table1,table2,...]`
    """
    path, file = os.path.split(dumpfile)
    with hide('everything'):
        run('mkdir -p {}'.format(path))
    _pg_dump(dumpfile, *tables)
    notify_ok('Database exported to {}'.format(dumpfile))


@task(task_class=DefaultTargetTask)
def archive(dumpfile):
    """
    pg_dump the target DB to the specified remote file, excluding tables
    related to reporting
    `pg.dump:<remote_file_path>`
    """
    path, file = os.path.split(dumpfile)
    with hide('everything'):
        run('mkdir -p {}'.format(path))
        set_db_envs()
    pg_cmd = ("pg_dump -Fc -Z9 -O -x -T '*reports*' -T report_export_jobs -h "
              "{db_host} -U {db_user} -f {dumpfile} {db_name}").format(
                  dumpfile=dumpfile, **env)
    pgrun(pg_cmd)
    notify_ok('Database archived to {}'.format(dumpfile))


@task(task_class=DefaultTargetTask)
def pull_remote_dump(dumpfile, *tables):
    """
    pg_dump the target DB to the specified local file, optionally specifying
    db tables:
    `pg.pull_remote_dump:<local_file_path>,[table1,table2,...]`
    """
    with hide('everything'):
        set_remote_tempfile()
    _pg_dump(env.tempfile, *tables)
    get(env.tempfile, dumpfile)
    notify_ok('Database exported to {}'.format(dumpfile))
    run('rm -f {tempfile}'.format(**env))


def _pg_dump_for_apps(func, dumpfile, *apps):
    if not apps:
        abort('Must specify at least one Django app.')
    _django.project('etsidata')
    tables = []
    from django.db.models import get_app, get_models
    for app in [get_app(a) for a in apps]:
        tables.extend([m._meta.db_table for m in get_models(
            app, include_auto_created=True)])
    execute(func, dumpfile, *tables)


@task(task_class=DefaultTargetTask)
def dump_for_apps(dumpfile, *apps):
    """
    pg_dump only tables for specied Django apps to the specified remote file:
    `pg.dump_for_apps:<remote_file_path>,app1[,app2,...]`
    """
    _pg_dump_for_apps(dump, dumpfile, *apps)


@task(task_class=DefaultTargetTask)
def pull_remote_dump_for_apps(dumpfile, *apps):
    """
    pg_dump only tables for specied Django apps to the specified local file:
    `pg.pull_remote_dump_for_apps:<local_file_path>,app1[,app2,...]`
    """
    _pg_dump_for_apps(pull_remote_dump, dumpfile, *apps)


@task()
def local_restore(dumpfile):
    """
    Restores the local database using the supplied export file. This assumes
    that the database exists. The restore will drop database objects and
    recreate them.
    `pg.local_restore:<path_to_export_file>`
    """
    env.dumpfile = dumpfile
    with hide('everything'):
        set_db_envs()

    with settings(warn_only=True), hide('warnings'):
        local('pg_restore -O -c -d {db_name} {dumpfile}'.format(**env))
    notify_ok('Database "{db_name}" restored.'.format(**env))


@task(task_class=DefaultTargetTask)
def refresh_from_remote():
    """
    Restores local database based on remote database. This will:
    1. Export the remote database and download the export file locally
    2. Restore the local database using the export file
    """
    of = tempfile.mkstemp()[1]
    os.remove(of)
    execute(pull_remote_dump, of)
    execute(local_restore, of)
    os.remove(of)


@task(task_class=DefaultTargetTask)
def restore(dumpfile):
    """
    Restores the remote database using the supplied remote export file. This
    assumes that the database exists. The restore will drop database objects
    and recreate them.
    `pg.restore:<path_to_remote_export_file>`
    """
    with hide('everything'):
        set_db_envs()

    pgrun(('pg_restore -O -c -n public -h {db_host} -U {db_user} '
           '-d {db_name} {dumpfile}').format(dumpfile=dumpfile, **env))
    notify_ok('Database "{db_name}" restored.'.format(**env))


@task(task_class=DefaultTargetTask)
def restore_to_remote(dumpfile):
    """
    Restores the remote database using the supplied local export file. This
    assumes that the database exists. The restore will drop database objects
    and recreate them.
    `pg.restore_to_remote:<path_to_local_export_file>`
    """
    with hide('everything'):
        set_remote_tempfile()
    put(dumpfile, env.tempfile)
    execute(restore, env.tempfile)
    run('rm -f {tempfile}'.format(**env))
