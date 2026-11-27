"""Explicit per-process GNU Radio OOT selection; startup failures are fatal."""
import json
import os
from pathlib import Path
import sys
import sysconfig

build, prefix = os.environ.get('TEMPEST_TEST_BUILD'), os.environ.get('TEMPEST_PREFIX')
if build or prefix:
    try:
        if build and prefix:
            raise RuntimeError('Select either build or installed prefix, never both')
        if build:
            root = Path(build).resolve()
            namespace, libdir = root/'test_modules/gnuradio', root/'lib'
        else:
            root = Path(prefix).resolve()
            info = json.loads((root/'share/gr-tempest/build-info.json').read_text())
            namespace = root/info['python_relative_dir']/'gnuradio'
            libdir = root/info['library_relative_dir']
        expected = namespace/'tempest'
        if not (expected/('tempest_python'+sysconfig.get_config_var('EXT_SUFFIX'))).is_file():
            raise RuntimeError('Selected compiled binding missing: '+str(expected))
        import gnuradio
        gnuradio.__path__.insert(0, str(namespace))
        from gnuradio import tempest
        if Path(tempest.__file__).resolve().parent != expected:
            raise RuntimeError('Imported a different gnuradio.tempest: '+str(tempest.__file__))
        maps = Path('/proc/self/maps')
        if not maps.is_file():
            raise RuntimeError('Native provenance requires Linux procfs; other platforms unqualified')
        libraries = {Path(line.split(None, 5)[5]).resolve()
                     for line in maps.read_text().splitlines() if 'libgnuradio-tempest' in line}
        if not libraries or any(path.parent != libdir.resolve() for path in libraries):
            raise RuntimeError('Loaded a different native library: '+repr(libraries))
        # GRC documentation workers use stdout as a protocol. Never print here.
    except Exception as error:
        sys.stderr.write('TEMPEST_PROVENANCE_ERROR: '+str(error)+'\n')
        sys.stderr.flush()
        os._exit(91)
