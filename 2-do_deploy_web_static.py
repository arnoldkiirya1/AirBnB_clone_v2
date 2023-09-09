#!/usr/bin/python3
"""Fabric script to deploy archive to web servers"""
import os
from fabric.api import *
from datetime import datetime

# Set your server IP addresses here
env.hosts = ['<54.237.67.184 web-01>', '<54.165.90.9 web-02>']
env.user = 'ubuntu' 
env.key_filename = '~/.ssh/id_rsa' 

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers and deploys it
    Args:
        archive_path: The path to the archive on the local machine
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_filename)[0]

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p /data/web_static/releases/{}'.format(archive_no_ext))

        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(archive_filename, archive_no_ext))

        # Delete the uploaded archive
        run('rm /tmp/{}'.format(archive_filename))

        # Move files to proper location
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}'.format(
            archive_no_ext, archive_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_no_ext))

        # Remove old symlink and create a new one
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(archive_no_ext))

        return True
    except:
        return False

