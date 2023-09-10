#!/usr/bin/python3
"""creates a .tgz archive from
contents in the web_static folder
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Creates a .tgz archive from the contents of
    folder.
    Returns:
        str: Path to the created archive otherwise
        None
    """
    local("mkdir -p versions")
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    arch_path = "versions/web_static_{}.tgz".format(time)
    archive = local("tar -czvf {} web_static".format(arch_path))
    arch_size = os.stat(arch_path).st_size
    if archive.succeeded:
        print("web_static packed: {} -> {}Bytes".format(arch_path, arch_size))
        return archive
    return None
