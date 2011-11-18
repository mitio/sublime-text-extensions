#!/usr/bin/env python

import os
import sys


def contains(search, target):
    for line in file(target):
        if search in line:
            return True
    return False


def contains_with_first_line(search, target):
    for pos, line in enumerate(file(target)):
        if search in line:
            return [pos]
    return False


def contains_with_lines(search, target):
    lines = []
    for pos, line in enumerate(file(target)):
        if search in line:
            lines.append(pos)
    return lines if lines else False


def grep(search, paths, recursive=False,
         contains_func=contains, filter_func=None):
    results = []
    results_append = results.append
    sub_paths = []
    sub_paths_append = sub_paths.append
    listdir = os.listdir
    isdir = os.path.isdir
    join = os.path.join
    for path in paths:
        # print 'path =', path
        for result in listdir(path):
            target = join(path, result)
            if filter_func and filter_func(target) is False:
                continue
            if isdir(target):
                if recursive:
                    sub_paths_append(target)
            else:
                lines = contains_func(search, target)
                if lines is True:
                    results_append(target)
                elif lines is not False:
                    [results_append('%s:%d' % (target, line)) for line in lines]
    if sub_paths:
        results.extend(grep(search, sub_paths, recursive=recursive,
                            contains_func=contains_func,
                            filter_func=filter_func))
    return results


if __name__ == '__main__':
    args = sys.argv[1:]

    RECURSIVE = False
    CONTAINS_FUNC = contains

    if '-r' in args:
        del args[args.index('-r')]
        RECURSIVE = True

    if '-n' in args:
        del args[args.index('-n')]
        CONTAINS_FUNC = contains_with_lines

    if '-f' in args:
        del args[args.index('-f')]
        CONTAINS_FUNC = contains_with_first_line

    search = args[0]
    paths = args[1:]

    for result in grep(search, paths, recursive=RECURSIVE,
                       contains_func=CONTAINS_FUNC):
        print result
