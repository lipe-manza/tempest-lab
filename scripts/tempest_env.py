#!/usr/bin/env python3
"""Run one command with an explicit isolated gr-tempest installation prefix."""
import argparse
import json
import os
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefix', required=True, type=Path)
    p.add_argument('--hier', type=Path, help='Generated GRC hierarchy directory')
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    prefix = a.prefix.resolve()
    command = a.command[1:] if a.command[:1] == ['--'] else a.command
    if not command:
        p.error('Supply a command, e.g. python3 scripts/doctor.py')
    info = json.loads((prefix/'share/gr-tempest/build-info.json').read_text())
    env = os.environ.copy()
    env.pop('TEMPEST_TEST_BUILD', None)
    env['TEMPEST_PREFIX'] = str(prefix)
    def prepend(key, value):
        env[key] = str(value)+(os.pathsep+env[key] if env.get(key) else '')
    prepend('PYTHONPATH', prefix/'share/gr-tempest/pythonpath_control')
    prepend('LD_LIBRARY_PATH', prefix/info['library_relative_dir'])
    prepend('GRC_BLOCKS_PATH', prefix/'share/gnuradio/grc/blocks')
    if a.hier:
        hierarchy = a.hier.resolve()
        if not hierarchy.is_dir():
            p.error('Hierarchy directory does not exist')
        env['GRC_HIER_PATH'] = str(hierarchy)
        prepend('GRC_BLOCKS_PATH', hierarchy)
        prepend('PYTHONPATH', hierarchy)
    os.execvpe(command[0], command, env)


if __name__ == '__main__':
    main()
