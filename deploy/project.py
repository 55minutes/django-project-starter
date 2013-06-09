from os.path import expanduser, join
from string import Template

from fabric.api import env, prompt, require, task
from fabric.colors import green
from fabric.utils import apply_lcwd


def render_template(filename, context=None):
    filename = apply_lcwd(filename, env)
    with open(expanduser(filename)) as inputfile:
        text = Template(inputfile.read())
    return text.substitute(context or {})


def render_settings():
    "Render Django settings file"
    require('target', 'static_root')

    secrets = {
        'db_password': 'PostgreSQL password: ',
        'postmark_api_key': 'Postmark API Key: ',
        'secret_key': 'Project-wide SECRET_KEY: ',
    }
    for k, msg in ((k, v) for k, v in secrets.items()
                   if not env.get(k, False)):
        prompt(msg, key=k)
    return render_template(join(env.template_dir, 'settings.py'), env)


def local_setup():
    "Generate {{ project_name }}/settings.py and $VIRTUAL_ENV/bin hooks"
    require(
        'gemset_fp', 'guard_fp', 'name', 'settings_fp', 'template_dir',
        'virtual_env'
    )

    with open(env.settings_fp, 'w+') as of:
        of.write(render_settings())
    print(green('{} generated'.format(env.settings_fp)))

    with open(env.gemset_fp, 'w+') as of:
        of.write(env.name)
    print(green('{} generated'.format(env.gemset_fp)))

    with open(env.guard_fp, 'w+') as of:
        of.write(render_template(join(env.template_dir, 'Guardfile'), env))
    print(green('{} generated'.format(env.guard_fp)))

    ve_bin = join(env.virtual_env, 'bin')
    for hook in ('postactivate', 'postdeactivate'):
        hook_file = join(ve_bin, hook)
        with open(hook_file, 'w+') as of:
            of.write(render_template(join(env.template_dir, hook), env))
        print(green('{} generated'.format(hook_file)))


@task()
def setup():
    if env.is_remote:
        pass
    else:
        local_setup()
