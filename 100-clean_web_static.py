#!/usr/bin/python3
"""Fabric script to clean up outdated archives"""
from fabric.api import local, env, run
from datetime import datetime
import os

env.hosts = ['<54.237.67.184 web-01>', '<54.165.90.9 web-02>']
env.user = 'ubuntu' 
env.key_filename = '~/.ssh/id_rsa' 


def do_clean(number=0):
    """Deletes out-of-date archives."""
    try:
        number = int(number)
    except ValueError:
        return

    if number < 0:
        return

    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    # Delete outdated archives in the versions folder
    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -I {{}} rm -f {{}}".format(number))

    # Delete outdated archives in the web_static/releases folder
    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number))


def do_clean_remote(number=0):
    """Deletes out-of-date archives on remote servers."""
    try:
        number = int(number)
    except ValueError:
        return

    if number < 0:
        return

    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    # Delete outdated archives in the versions folder on remote servers
    run("cd ~/AirBnB_clone_v2/versions && ls -t | tail -n +{} | xargs -I {{}} rm -f {{}}".format(number))

    # Delete outdated archives in the web_static/releases folder on remote servers
    run("cd /data/web_static/releases && ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number))

