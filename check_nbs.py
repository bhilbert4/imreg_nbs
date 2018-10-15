#!/usr/bin/env python3

import os
import sys
import nbformat
import logging

log = logging.getLogger('check_nbs')

def visit_nbs(nbpath, visitfunc):
    success = True
    for root, dirs, files in os.walk(nbpath):
        for name in files:
            _, ext = os.path.splitext(name)
            full_path = os.path.join(root, name)
            if ext != '.ipynb':
                continue

            if name.startswith('exec_'): #skip the executed ones
                continue

            if 'ipynb_checkpoints' in full_path:  # skip checkpoint saves
                continue

            success = success and visitfunc(name, full_path)
    return success


def do_checks(name, full_path):
    log.info('Checking notebook {}'.format(name))
    success = True
    if is_executed(name, full_path):
        log.error('Notebook {} has executed cells!'.format(name))

    return success


def is_executed(name, full_path):
    nb = nbformat.read(full_path, nbformat.NO_CONVERT)
    for cell in nb.cells:
        if cell.cell_type == 'code':
            if cell.outputs:
                return True
    return False

if __name__ == '__main__':
    logging.basicConfig()
    log.setLevel(logging.INFO)
    success = visit_nbs('.', do_checks)
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)
