#!/usr/bin/env python

import subprocess
from six import string_types, binary_type
import sys
from os import path
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def changer_files(repo_path):
    cmd = ['git', '--git-dir=' + path.join(repo_path, '.git')] + ['show', '--name-only']
    try:
        res = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        res = None
    if isinstance(res, binary_type):
        res = res.decode()
    if isinstance(res, string_types):
        res = res.strip('\n')
    res = res.splitlines()
    res = res[6:-1]
    res = [path.dirname(i).split('/')[0] for i in res]
    res = list(set(res))
    return res

config_file = path.abspath(sys.argv[1])
repo_path = os.environ.get('TRAVIS_BUILD_DIR', False)
extra_args = ''
for change in changer_files(path.abspath(repo_path)):
    if not change:
        continue
    extra_args += "--path {0} ".format(path.abspath(path.join(repo_path, change)))

if extra_args:
    cmd = "run_pylint.py --extra-params --load-plugins=pylint_odoo --extra-params --enable=sql-injection -c {0} {1} ".format(config_file, extra_args)
    res = os.system(cmd)
    if res > 0:
        exit(1)
else:
    print(bcolors.OKGREEN+"There are no changes to review...good"+bcolors.ENDC)

