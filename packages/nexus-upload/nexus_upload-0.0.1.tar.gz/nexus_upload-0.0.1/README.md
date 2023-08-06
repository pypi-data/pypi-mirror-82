nexus_upload
============================================================

Table of Contents
=================

- [About](#About)
- [Installing](#installing)
- [Usage](#Usage)

About
=====

nexus_upload is a command line tool to batch upload packages to Nexus server.

Installing
==========

- **Windows**

1. Install [Python 2.7 or 3.4+](https://www.python.org/):

    When installing, option **`Add python.exe to Path`** must be selected and enabled. Or after installation, manually add the Python installation directory and its Scripts subdirectory to your PATH. Depending on your Python version, the defaults would be C:\Python27 and C:\Python27\Scripts respectively.

1. Install `nexus_upload` via pip

    ```
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ nexus_upload
    ```

1. Reboot the system

- **Linux**

1. Install [Python 2.7 or 3.4+](https://www.python.org/)

1. Install `nexus_upload` via pip

    ```
    pip install -i https://mirrors.aliyun.com/pypi/simple/ nexus_upload
    ```

- **MacOSX**

1. Install [Python 2.7 or 3.4+](https://www.python.org/)

1. Install `nexus_upload` via pip

    ```
    pip install -i https://pypi.douban.com/simple/ nexus_upload
    ```

Usage
=====

- **General command help**

    ```
    nexus_upload --help
    usage: nexus_upload [-h] -s <url> -r <repo> -u <user> -p <pass> -j <jar> [<jar> ...] -f <path> [--ssh-server <host:port>]
                          [--ssh-login <user:pass>]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s <url>, --server <url>
                            The Nexus server url
      -r <repo>, --repository <repo>
                            The Nexus repository name, eg. maven-releases
      -u <user>, --username <user>
                            The Nexus login username
      -p <pass>, --password <pass>
                            The Nexus login password
      -j <jar> [<jar> ...], --jar <jar> [<jar> ...]
                            Upload specific package jar(s), eg: com.alibaba:fastjson:jar:1.2.62
      -f <path>, --folder <path>
                            Upload package jars from local or remote path
      --ssh-server <host:port>
                            Remote ssh's host and port, eg: ssh.server.com:22
      --ssh-login <user:pass>
                            Remote ssh's username and password, eg: root:pass
    ```
