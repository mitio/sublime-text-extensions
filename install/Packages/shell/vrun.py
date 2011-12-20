#!/usr/bin/env python -u

'''
Script to run a Python file thru a virual environment (virtualenv) if possible
otherwise directly.
Currently only supported within UNIX environments. Plz send me patches for
Windows environmnts and I will implement it properly.

Usage: vrun.py [--quiet] [--origin <filepath>] <python file>

Optional arguments:
--quiet             Don't print command to execute to stdout.
--origin <filepath> A filepath to extract a virtual environment folder from.

Optional env vars:
CODE_ENV            A folder where subfolders reside, each representing a
                    virtual environment root.

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-20
'''

import os
import sys
import shlex
import subprocess


QUIET = False  # Set to true for not printing any extra output.

ENV_DIR = os.getenv('CODE_ENV')
if ENV_DIR is None:
    raise Exception('Env var CODE_ENV not set!')

sys_argv = sys.argv[:]
# print sys_argv
# print os.system('env')

if '--quiet' in sys_argv:
    pos = sys_argv.index('--quiet')
    QUIET = True
    del sys_argv[pos]

if '--origin' in sys_argv:
    pos = sys_argv.index('--origin')
    filename = sys_argv[pos + 1]
    del sys_argv[pos:pos + 1]
else:
    parts = shlex.split(sys_argv[1])
    # print parts
    filename = parts[-1]
# print filename

if not os.path.exists(filename):
    msg = 'File not found: %s' % filename
    sys.stderr.write(msg)
    sys.exit(2)

# Ensure to have full filepath of filename for gathering the correct virtualenv.
filename = os.path.abspath(filename)

parts = os.path.dirname(filename).split(os.path.sep)

result = None
while len(parts) > 1:
    path = os.path.join(ENV_DIR, parts[-1])
    if os.path.exists(path):
        # print 'FOUND:', path
        result = path
        break
    del parts[-1]

if result is None:
    cmd = sys_argv[1]
else:
    script = os.path.join(result, 'bin/activate')
    cmd = 'source %s && %s' % (script, sys_argv[1])

if not QUIET:
    print '$ %s' % cmd
subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr,
                 shell=True).communicate()[0]
