import json
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from env_doctor import audit, main, parse_example, parse_dotenv, validate

class EnvDoctorTests(unittest.TestCase):
    def test_missing_and_invalid(self):
        result = audit({"TOKEN": "", "PORT": ""}, {"TOKEN": "secret", "PORT": "nope"}, {"PORT": "int"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["summary"], {"ok": 1, "missing": 0, "invalid": 1})
        self.assertNotIn("secret", json.dumps(result))

    def test_all_types(self):
        self.assertTrue(validate("https://example.com", "url"))
        self.assertFalse(validate("javascript:alert(1)", "url"))
        self.assertTrue(validate("yes", "bool"))
        self.assertFalse(validate("maybe", "bool"))
        self.assertTrue(validate("-12", "int"))
        self.assertFalse(validate("12.4", "int"))
        self.assertFalse(validate("nan", "float"))

    def test_example_errors(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ".env.example"
            p.write_text("A=1\nA=2\n")
            with self.assertRaises(ValueError):
                parse_example(p)

    def test_dotenv_quotes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ".env"
            p.write_text("export API_TOKEN='secret'\n")
            self.assertEqual(parse_dotenv(p)["API_TOKEN"], "secret")

    def test_cli_json_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            example = Path(d) / ".env.example"
            env = Path(d) / ".env"
            example.write_text("TOKEN=\nPORT=\n")
            env.write_text("TOKEN=secret\nPORT=8080\n")
            output = StringIO()
            with redirect_stdout(output):
                code = main(["--example", str(example), "--env-file", str(env), "--json"])
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(output.getvalue())["ok"])
            self.assertNotIn("secret", output.getvalue())
            env.write_text("PORT=bad\n")
            with redirect_stdout(StringIO()):
                self.assertEqual(main(["--example", str(example), "--env-file", str(env)]), 1)

if __name__ == "__main__":
    unittest.main()
