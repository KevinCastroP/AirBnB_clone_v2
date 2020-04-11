#!/usr/bin/python3
"""
fabric file to compress all web_static folder
"""


from fabric.api import local, settings, env, hosts
from fabric.operations import put, run
from datetime import datetime as dt


def do_pack():
    """
    pack web_static files to tar
    """
    with settings(warn_only=True):
        res = local("mkdir -p versions")
        date = dt.now()
        pathname = "versions/web_static_"
        pathname += str(date.year)
        pathname += str(date.month)
        pathname += str(date.day)
        pathname += str(date.hour)
        pathname += str(date.minute)
        pathname += str(date.second)
        pathname += ".tgz"
        res2 = local("tar -cvzf " + pathname + " web_static")
        if res2.return_code == 0:
            return pathname

env.hosts = ['35.231.236.18', '3.95.205.51']


def do_deploy(archive_path):
    """
    Deploy function
    """
    if not archive_path:
        return False
    put(local_path=archive_path, remote_path='/tmp/', use_sudo=True)
    archive_name = archive_path.split('/')[1]
    data_path = '/data/web_static/releases/' + archive_name.split('.')[0] + '/'
    try:
        run('mkdir -p ' + data_path)
        run('tar -xzf /tmp/' +
            archive_name +
            ' -C ' + data_path)
        run('rm /tmp/' + archive_name)
        run('mv ' + data_path + 'web_static/* ' + data_path)
        run('rm -rf ' + data_path + 'web_static')
        run('rm -rf /data/web_static/current')
        run('ln -s ' + data_path + ' /data/web_static/current')
    except:
        return False
    finally:
        return True


def deploy():
    """
    Creates an distributes an archive to the web servers
    """
    return do_deploy(do_pack())


def do_clean(number=0):
    """
    clean unnecessary archives
    """
    number = int(number)
    if number == 0:
        number = 1
    archives = local('ls -tr -1 versions', capture=True)
    archives = archives.split('\n')[:-number]
    for arch in archives:
        local('rm -rf versions/' + arch)
    rem_archs = run("ls -tr -1 /data/web_static/releases/" +
                    " | grep -v test")
    rem_archs = rem_archs.split('\n')[:-number]
    rem_archs = [x.rstrip() for x in rem_archs]
    print(rem_archs)
    for arch in rem_archs:
        run('rm -rf /data/web_static/releases/' + arch)
