# Arduino configuration format demo

Open `examples/arduino-config/arduino-config.ino` with repository layout intact. Supports Uno/Mega and ESP32 with `LED_BUILTIN` defined by the board core. Demonstrates format-only checks on static example strings and defaults the diagnostic LED off. This does not verify URL reachability, TLS certificates, credential correctness, or actual runtime safety. Do not store real API secrets in firmware source or logs; never enable a motor, relay, heater, or network operation merely because syntax validation passes.

Host regression: `cmake -S . -B build && cmake --build build && ctest --test-dir build --output-on-failure`. The Python CLI remains authoritative for full dotenv and JSON processing. Embedded C++ intentionally supports only a bounded subset. Arduino and ESP32 hardware compilation and physical tests remain unverified; relative includes may need adaptation when copying sketches outside this checkout.

## Board-build CI (added 2026-11-17)
The `.github/workflows/arduino-board-compile.yml` workflow invokes `arduino-cli compile` for **Arduino Uno (AVR)** and **ESP32 generic dev module**. This checks board-toolchain compatibility in GitHub Actions; host CMake/g++ and Python CI remain separate. A green compile does not establish actual sensor readings, wiring, pin compatibility on every variant, watchdog behavior, or electrical safety. Test on the actual board before connecting actuators.

URL validation rejects whitespace, user-info (@) and backslash; this is syntax screening only, not DNS/TLS or endpoint trust validation.
