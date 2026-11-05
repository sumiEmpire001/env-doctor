# Env Doctor 🩺

A lightweight Python CLI that checks whether your project's required environment variables are present and correctly formatted **without printing their values**.

## Features

- Read required keys from `.env.example`
- Check the process environment or an explicit local `.env` file
- Validate optional `str`, `int`, `float`, `bool`, and HTTP(S) `url` types
- Human-readable or JSON output for CI integrations
- Exit codes: **0** pass, **1** failed checks, **2** invalid input
- No runtime dependencies, Python 3.9+

## Install locally

```bash
python -m pip install .
```

Or run directly: `python env_doctor.py --help`.

## Usage

Create a `.env.example` file listing required keys (values are ignored):

```dotenv
API_TOKEN=
PORT=
SERVICE_URL=
```

Check actual process environment:

```bash
env-doctor --example .env.example
```

Check a local file and validate types:

```bash
env-doctor --example .env.example --env-file .env --types types.example.json --json
```

`types.example.json`:

```json
{"PORT": "int", "SERVICE_URL": "url"}
```

## Security limitations

The tool **does not print variable values**, but variable names and statuses are visible. It does not execute shell commands or expand shell variables. The `.env` parser intentionally supports only simple `KEY=value` lines, optional `export`, and surrounding quotes; it is **not** a complete dotenv/shell parser. Do not commit real `.env` files or credentials. The CLI does not automatically read `.env`; pass `--env-file` explicitly.

## Development

```bash
python -m unittest discover -s tests -v
python -m pip install build
python -m build
```

GitHub Actions tests Python 3.9, 3.11, and 3.13 on Linux and Windows.

## License

MIT — see [LICENSE](LICENSE).
