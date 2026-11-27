# Build and unit-test review

This internal engineering revision covers CMake, the Python binding loader, prefix selection, and isolated Python unit tests on Linux with procfs. The candidate working tree also contains research changes under separate review. Results for that working tree and historical EXP-011 results apply to their respective source versions.

From the repository root on a host with GNU Radio 3.10 development files, its matching Python interpreter, NumPy, Pillow, PyQt5, VOLK, pybind11, a C++17 compiler, CMake and Ninja:

```sh
cmake -S . -B build/native -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/local" -DPython3_EXECUTABLE="$(command -v python3)"
cmake --build build/native --parallel 2
ctest --test-dir build/native -R '^qa_(module_provenance|tempest_msgbtn|message_to_var|image_source)$' --output-on-failure
cmake --install build/native
python3 scripts/tempest_env.py --prefix "$PWD/local" -- python3 -c 'from gnuradio import tempest; print(tempest.__file__)'
```

The provenance test checks the selected Python package and mapped C++ library. A conflicting native library must cause a startup error. Use a fresh build directory when changing interpreters. Retain the test output and Git revision in bug reports.

Qualification of this revision excludes other operating systems, RF hardware, and end-to-end reconstruction. The original research programs remain in the base history. This review does not qualify their use.
