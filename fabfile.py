from fabric.api import cd, env, lcd, put, sudo, run
from fabric.contrib.files import exists
from config import *


local_app_dir = './flask_cbr'
local_config_dir = './config'

remote_app_dir = '/home/flask_cbr'
remote_flask_dir = remote_app_dir + '/flask_cbr'
remote_nginx_dir = '/etc/nginx/sites-enabled'
remote_supervisor_dir = '/etc/supervisor/conf.d'

env.hosts = [server_ip]
env.user = server_user
env.password = server_password


def install_requirements():
    """ Install required packages. """
    sudo('apt-get update')
    sudo('apt-get install -y python')
    sudo('apt-get install -y python-pip')
    sudo('apt-get install -y python-virtualenv')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y gunicorn')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y git')


def install_flask():
    """
    1. Create project directories
    2. Create and activate a virtualenv
    3. Copy Flask files to remote host
    """
    if exists(remote_app_dir) is False:
        sudo('mkdir ' + remote_app_dir)
    if exists(remote_flask_dir) is False:
        sudo('mkdir ' + remote_flask_dir)
    with lcd(local_app_dir):
        with cd(remote_flask_dir):
            put('*', './', use_sudo=True)
            if exists(remote_flask_dir+'/cbr-db') is False:
                run('git clone https://github.com/epogrebnyak/cbr-db.git')
                run('mkdir cbr-db/output')
        with cd(remote_flask_dir):
            sudo('pip install -r requirements.txt')


def configure_nginx():
    """
    1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    sudo('/etc/init.d/nginx start')
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    if exists('/etc/nginx/sites-enabled/flask_cbr') is False:
        sudo('touch /etc/nginx/sites-available/flask_cbr')
        sudo('ln -s /etc/nginx/sites-available/flask_cbr' +
             ' /etc/nginx/sites-enabled/flask_cbr')
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put('./flask_cbr', './', use_sudo=True)
    sudo('/etc/init.d/nginx restart')


def configure_supervisor():
    """
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """
    with lcd(local_config_dir):
        with cd(remote_supervisor_dir):
            put('./flask_cbr.conf', './', use_sudo=True)
            sudo('supervisorctl reread')
            sudo('supervisorctl update')


def run_app():
    """ Run the app! """
    with cd(remote_flask_dir):
        sudo('supervisorctl stop flask_cbr')
        sudo('supervisorctl start flask_cbr')


def status():
    """ Is our app live? """
    sudo('supervisorctl status')


def create():
    install_requirements()
    install_flask()
    configure_nginx()
    configure_supervisor()
