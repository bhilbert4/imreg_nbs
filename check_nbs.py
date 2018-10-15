#!/usr/bin/env python3

import sys
import nbformat

def fail_message(msg):
    print('FAIL:', msg)


def visit_nbs(nbpath, visitfunc):
    success = True
    for root, dirs, files in walk(nbpath):
        for name in files:
            _, ext = path.splitext(name)
            full_path = path.join(root, name)

            if 'ipynb_checkpoints' in full_path:  # skip checkpoint saves
                continue

            success = success and visitfunc(name, full_path)
    return success

def do_checks(name, full_path):
    success = True
    if is_executed(name, full_path):
        fail_message('Notebook {} has executed cells!'.format(name))

    return success


def is_executed(name, full_path):
    nbformat.read(full_path, nbformat.NO_CONVERT)

if __name__ == '__main__':
    success = visit_nbs(do_checks)
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)
