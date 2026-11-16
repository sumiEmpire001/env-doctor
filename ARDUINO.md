# Arduino configuration format demo

Open `examples/arduino-config/arduino-config.ino` with repository layout intact. Supports Uno/Mega and ESP32 with `LED_BUILTIN` defined by the board core. Demonstrates format-only checks on static example strings and defaults the diagnostic LED off. This does not verify URL reachability, TLS certificates, credential correctness, or actual runtime safety. Do not store real API secrets in firmware source or logs; never enable a motor, relay, heater, or network operation merely because syntax validation passes.

Host regression: `cmake -S . -B build && cmake --build build && ctest --test-dir build --output-on-failure`. The Python CLI remains authoritative for full dotenv and JSON processing. Embedded C++ intentionally supports only a bounded subset. Arduino and ESP32 hardware compilation and physical tests remain unverified; relative includes may need adaptation when copying sketches outside this checkout.
