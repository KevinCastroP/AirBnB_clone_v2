#!/usr/bin/python3
"""
Fabric script to generate a .tgz file
from the contents of the web_static folder
"""


from fabric.api import *
from datetime import datetime
import os.path


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
