#!/usr/bin/python3
"""deploy archive on web server"""
from fabric.api import *
from os import path


env.user = 'ubuntu'
env.hosts = ['100.25.34.61', '100.25.180.211']
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """ script that distributes an archive to your web servers """
    try:
        if not (path.exists(archive_path)):
            return False

        put(archive_path, '/tmp/')
        time_stamp = archive_path[-18:-4]
        
        # create folder to uncompress into
        run('sudo mkdir -p /data/web_static/releases/web_static_{}'.format(time_stamp))
        
        # uncompress archive
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}'.format(time_stamp, time_stamp))

        #remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(time_stamp))

        # organize file structure
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(time_stamp, time_stamp))
        
        # remove current symbolic link
        run('sudo rm -rf /data/web_static/current')

        # cleaning up
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static/'.format(time_stamp))

        # build new symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(time_stamp))
    except:
        return False

    return True
