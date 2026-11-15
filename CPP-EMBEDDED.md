# Embedded configuration validation companion
C++11 allocation-free checks for integer, boolean, nonempty and basic HTTP(S) strings. Values are never logged or returned. Unlike Python Env Doctor, this does not read .env files, implement a CLI or fully validate URL grammar. For firmware configuration validation only, not secret storage.

## Host validation
```sh
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```
Run existing Python regression tests where present: `python -m unittest discover -s tests -v`.
Hardware safety: no GPIO actuation, no motor/pump/relay switching. Host tests do not establish Arduino Uno or ESP32 binary compatibility or device reliability. Use dedicated hardware watchdogs and physical interlocks for actuators.
