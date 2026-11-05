"""Validate environment configuration without printing secret values."""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
TYPES = {"str", "int", "float", "bool", "url"}

def parse_example(path: Path) -> dict[str, str]:
    """Read KEY=value declarations; values are only documentation defaults."""
    result = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            raise ValueError(f"{path}:{number}: expected KEY=value")
        key, value = line.split("=", 1)
        key = key.strip()
        if not KEY.fullmatch(key):
            raise ValueError(f"{path}:{number}: invalid variable name")
        if key in result:
            raise ValueError(f"{path}:{number}: duplicate variable {key}")
        result[key] = value.strip()
    return result

def parse_dotenv(path: Path) -> dict[str, str]:
    """Parse simple .env files; does not evaluate shell expressions."""
    values = parse_example(path)
    for key, value in values.items():
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            values[key] = value[1:-1]
    return values

def validate(value: str, kind: str) -> bool:
    if kind == "str":
        return bool(value.strip())
    if kind == "int":
        try:
            int(value)
            return True
        except ValueError:
            return False
    if kind == "float":
        try:
            number = float(value)
            return number == number and abs(number) != float("inf")
        except ValueError:
            return False
    if kind == "bool":
        return value.lower() in {"true", "false", "1", "0", "yes", "no", "on", "off"}
    if kind == "url":
        from urllib.parse import urlparse
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    return False

def audit(required: dict[str, str], actual: dict[str, str], types: dict[str, str] | None = None) -> dict:
    types = types or {}
    checks = []
    for name in sorted(required):
        value = actual.get(name)
        if value is None or not value.strip():
            status = "missing"
        elif not validate(value, types.get(name, "str")):
            status = "invalid"
        else:
            status = "ok"
        checks.append({"name": name, "status": status, "type": types.get(name, "str")})
    return {"ok": all(c["status"] == "ok" for c in checks), "checks": checks,
            "summary": {status: sum(c["status"] == status for c in checks) for status in ("ok", "missing", "invalid")}}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit required environment variables without revealing values")
    parser.add_argument("--example", default=".env.example", help="File listing required KEY=value entries")
    parser.add_argument("--env-file", help="Optional .env file (otherwise uses process environment)")
    parser.add_argument("--types", help="Optional JSON object mapping variable names to str/int/float/bool/url")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        required = parse_example(Path(args.example))
        actual = dict(os.environ) if not args.env_file else parse_dotenv(Path(args.env_file))
        types = {}
        if args.types:
            types = json.loads(Path(args.types).read_text(encoding="utf-8"))
            if not isinstance(types, dict) or any(not isinstance(k, str) or v not in TYPES for k, v in types.items()):
                raise ValueError("types must be a JSON object with supported type names")
            unknown = set(types) - set(required)
            if unknown:
                raise ValueError("types contain unknown variables: " + ", ".join(sorted(unknown)))
        result = audit(required, actual, types)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"env-doctor: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for check in result["checks"]:
            print(f"{check['status'].upper():7} {check['name']} ({check['type']})")
        print("PASS" if result["ok"] else "FAIL")
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
