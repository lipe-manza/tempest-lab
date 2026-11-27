#!/usr/bin/env python3
"""Reject false-positive QA against a system OOT module or a missing build."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class Provenance(unittest.TestCase):
    def test_selected_binding_and_library(self):
        from gnuradio import tempest
        root = Path(os.environ['TEMPEST_TEST_BUILD']).resolve()
        self.assertEqual(Path(tempest.__file__).resolve().parent,
                         root/'test_modules/gnuradio/tempest')
        libraries = {Path(line.split(None, 5)[5]).resolve()
                     for line in Path('/proc/self/maps').read_text().splitlines()
                     if 'libgnuradio-tempest' in line}
        self.assertTrue(libraries)
        self.assertTrue(all(path.parent == root/'lib' for path in libraries))
        print(json.dumps({'module':tempest.__file__,'libraries':list(map(str,libraries))}))

    def test_missing_build_is_fatal(self):
        with tempfile.TemporaryDirectory(prefix='tempest-missing-binding-') as folder:
            env = dict(os.environ, TEMPEST_TEST_BUILD=folder)
            result = subprocess.run([sys.executable,'-c','print("MUST_NOT_RUN")'],
                                    env=env,capture_output=True,text=True,timeout=15)
            self.assertEqual(result.returncode,91)
            self.assertIn('TEMPEST_PROVENANCE_ERROR',result.stderr)
            self.assertNotIn('MUST_NOT_RUN',result.stdout)


if __name__ == '__main__':
    unittest.main()
