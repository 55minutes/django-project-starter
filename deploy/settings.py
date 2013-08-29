from fabric.api import env

# Project configuration
env.name = '{{ project_name }}'
env.repository = 'git@bitbucket.org:55minutes/{name}.git'.format(**env)

# SSH configuration
env.forward_agent = True
env.use_ssh_config = True

# Set the default target
env.default_target = 'local'

# Set the upstart configuration location
env.upstart_conf = '/etc/init/uwsgi_{name}.conf'.format(**env)

# What secrets do we want to ask for?
env.secrets = {
    'db_password': 'PostgreSQL password: ',
    'postmark_api_key': 'Postmark API Key: ',
    'secret_key': 'Project-wide SECRET_KEY: ',
}
