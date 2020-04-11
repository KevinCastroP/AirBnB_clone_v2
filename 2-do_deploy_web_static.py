#!/usr/bin/python3
"""
Fabric script to generate a .tgz file
from the contents of the web_static folder
"""


from datetime import datetime
from fabric.api import local, settings, env
from fabric.operations import put, run
import os.path


env.hosts = ['35.185.100.242', '54.90.130.112']


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
    if not archive_path:
        return False
    Path = archive_path.split("/")[-1]
    Name = Path.split(".")[0]

    put(archive_path, "/tmp/", use_sudo=True)
    try:
        run("rm -rf /data/web_static/releases/{}/".format(Name))
        run("mkdir -p /data/web_static/releases/{}/".format(Name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(Path, Name))
        run("rm /tmp/{}".format(Path))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(Name, Name))
        run("rm -rf /data/web_static/releases/{}/web_static".
            format(Name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(Name))
    except SystemExit:
        return False
    finally:
        return True
