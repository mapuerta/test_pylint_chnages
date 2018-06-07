#!/usr/bin/env python

import subprocess
from six import string_types, binary_type
import sys
from os import path
import os

extra_params = [
    '--extra-params', '--load-plugins=pylint_odoo', '--extra-params',
    '--valid_odoo_versions=11.0', '--msgs-no-count', 'api-one-deprecated',
    '--extra-params', '--enable=api-one-deprecated', '--msgs-no-count',
    'api-one-multi-together', '--extra-params', '--enable=api-one-multi-together',
    '--msgs-no-count', 'attribute-deprecated', '--extra-params', '--enable=attribute-deprecated',
    '--msgs-no-count', 'class-camelcase', '--extra-params', '--enable=class-camelcase',
    '--msgs-no-count', 'create-user-wo-reset-password', '--extra-params',
    '--enable=create-user-wo-reset-password', '--msgs-no-count', 'consider-merging-classes-inherited',
    '--extra-params', '--enable=consider-merging-classes-inherited', '--msgs-no-count',
    'copy-wo-api-one', '--extra-params', '--enable=copy-wo-api-one', '--msgs-no-count',
    'dangerous-filter-wo-user', '--extra-params', '--enable=dangerous-filter-wo-user',
    '--msgs-no-count', 'dangerous-view-replace-wo-priority', '--extra-params',
    '--enable=dangerous-view-replace-wo-priority', '--msgs-no-count', 'deprecated-module',
    '--extra-params', '--enable=deprecated-module', '--msgs-no-count', 'duplicate-id-csv',
    '--extra-params', '--enable=duplicate-id-csv', '--msgs-no-count', 'duplicate-xml-fields',
    '--extra-params', '--enable=duplicate-xml-fields', '--msgs-no-count', 'duplicate-xml-record-id',
    '--extra-params', '--enable=duplicate-xml-record-id', '--msgs-no-count', 'file-not-used',
    '--extra-params', '--enable=file-not-used', '--msgs-no-count', 'incoherent-interpreter-exec-perm',
    '--extra-params', '--enable=incoherent-interpreter-exec-perm', '--msgs-no-count', 'invalid-commit',
    '--extra-params', '--enable=invalid-commit', '--msgs-no-count', 'javascript-lint', '--extra-params',
    '--enable=javascript-lint', '--msgs-no-count', 'manifest-deprecated-key', '--extra-params',
    '--enable=manifest-deprecated-key', '--msgs-no-count', 'method-compute', '--extra-params',
    '--enable=method-compute', '--msgs-no-count', 'method-inverse', '--extra-params', '--enable=method-inverse',
    '--msgs-no-count', 'method-required-super', '--extra-params', '--enable=method-required-super',
    '--msgs-no-count', 'method-search', '--extra-params', '--enable=method-search', '--msgs-no-count',
    'missing-newline-extrafiles', '--extra-params', '--enable=missing-newline-extrafiles', '--msgs-no-count',
    'missing-readme', '--extra-params', '--enable=missing-readme', '--msgs-no-count', 'no-utf8-coding-comment',
    '--extra-params', '--enable=no-utf8-coding-comment', '--msgs-no-count', 'unnecessary-utf8-coding-comment',
    '--extra-params', '--enable=unnecessary-utf8-coding-comment', '--msgs-no-count', 'odoo-addons-relative-import',
    '--extra-params', '--enable=odoo-addons-relative-import', '--msgs-no-count', 'old-api7-method-defined',
    '--extra-params', '--enable=old-api7-method-defined', '--msgs-no-count', 'openerp-exception-warning',
    '--extra-params', '--enable=openerp-exception-warning', '--msgs-no-count', 'redundant-modulename-xml',
    '--extra-params', '--enable=redundant-modulename-xml', '--msgs-no-count', 'sql-injection',
    '--extra-params', '--enable=sql-injection', '--msgs-no-count', 'too-complex',
    '--extra-params', '--enable=too-complex', '--msgs-no-count', 'translation-field',
    '--extra-params', '--enable=translation-field', '--msgs-no-count', 'translation-required',
    '--extra-params', '--enable=translation-required', '--msgs-no-count', 'use-vim-comment',
    '--extra-params', '--enable=use-vim-comment', '--msgs-no-count', 'wrong-tabs-instead-of-spaces',
    '--extra-params', '--enable=wrong-tabs-instead-of-spaces', '--msgs-no-count', 'xml-syntax-error',
    '--extra-params', '--enable=xml-syntax-error'] 


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

extra_params = " ".join(extra_params)
config_file = path.abspath(sys.argv[1])
repo_path = os.environ.get('TRAVIS_BUILD_DIR', False)
file_paths = ''
for change in changer_files(path.abspath(repo_path)):
    if not change:
        continue
    file_paths += "--path {0} ".format(path.abspath(path.join(repo_path, change)))

if file_paths:
    cmd = "run_pylint.py {0} -c {1} {2} ".format(extra_params, config_file, file_paths)
    res = os.system(cmd)
    if res > 0:
        print(bcolors.FAIL+"Multiple lines with lints...fail"+bcolors.ENDC)
        exit(1)
else:
    print(bcolors.OKGREEN+"There are no changes to review...good"+bcolors.ENDC)

