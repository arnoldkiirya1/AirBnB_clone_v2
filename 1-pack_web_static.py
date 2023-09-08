#!/usr/bin/python3
from fabric.api import local
from datetime import date
from time import strftime


def do_pack():
    """ Script that archives contents of web_static folder """

    time_stamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czf versions/web_static_{}.tgz web_static/"
              .format(time_stamp))

        return "versions/web_static_{}.tgz".format(time_stamp)

    except Exception as e:
        return None
