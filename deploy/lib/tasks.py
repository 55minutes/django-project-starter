from fabric import state
from fabric.api import execute
from fabric.tasks import WrappedCallableTask


class DefaultTargetTask(WrappedCallableTask):
    def get_hosts(self, arg_hosts, arg_roles, arg_exclude_hosts, env=None):
        if not 'target' in state.env:
            execute('target.{}'.format(state.env.default_target))
        return super(DefaultTargetTask, self).get_hosts(
            arg_hosts, arg_roles, arg_exclude_hosts, env)
