#!/usr/bin/python3
"""
Fabric script to generate a .tgz file
from the contents of the web_static folder
"""


from fabric.api import *
from datetime import datetime
import os.path


env.host = ['35.185.100.242', '54.90.130.112']


def do_pack():
    """Creating a .tgz file to upload a folder to the servers"""
    DateTime = datetime.utcnow()
    upfile = "versions/web_static_{}{}{}{}{}{}.tgz".format(DateTime.year,
                                                           DateTime.month,
                                                           DateTime.day,
                                                           DateTime.hour,
                                                           DateTime.minute,
                                                           DateTime.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(upfile)).failed is True:
        return None
    return upfile

def do_deploy(archive_path):
    """Deploys static archive to web servers."""
    if os.path.isfile(archive_path) is False:
        return False
    Path = archive_path.split("/")[-1]
    Name = Path.split(".")[0]

    if put(archive_path, "/tmp/{}".format(Path)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(Name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(Name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(Path, Name)).failed is True:
        return False
    if run("rm /tmp/{}".format(Path)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(Name, Name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(Name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(Name)).failed is True:
        return False
    print("\nNew Version Successfuly Deployed!\n")
    return True
