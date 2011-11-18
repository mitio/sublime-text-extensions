#!/bin/bash -l

# Small wrapper to run vrun.py within a login shell. Necessary under OSX e.g.
# when running within Sublime Text 2 to have a full shell environment.
# 
# @author: Oktay Acikalin <ok@ryotic.de>
# 
# @license: MIT (http://www.opensource.org/licenses/mit-license.php)
# 
# @since: 2011-02-20

path=$(dirname $0)

${path}/vrun.py "$@"
