#!/usr/bin/python3
"""Distributes an archive to web servers"""
from fabric.api import env, put, run
import os

env.hosts = ['54.209.192.89', '52.23.178.163']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    to_acrchive = os.path.basename(archive_path)
    folder_name = to_archive.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}".format(folder_name)
    success = False

    try:
        # Upload archive to /tmp/ directory on web server
        put(archive_path, '/tmp/{}'.format(to_archive))

        # Create the folder that receives archived files
        run('mkdir -p {}'.format(folder_path))

        # decompress the archive into the folder
        run('tar -xzf /tmp/{} -C {}'.format(to_archive, folder_path))

        # Delete the uploaded archive
        run('rm -rf /tmp/{}'.format(to_archive))

        # Move contents from archive folder to current folder
        run('mv {}/web_static/* {}'.format(folder_path, folder_path))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(folder_path))

        # Delete the old current link
        run('rm -rf /data/web_static/current')

        # Create a new symlink
        run('ln -s {} /data/web_static/current'.format(folder_path))
        print('New version deployed!')
        success = True
        return True
    except Exception:
        success = False
    return success
