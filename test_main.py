"""Tests for main.py — Laugh Track: The Crypto Trading Joke Contest.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-200 characters,
not only whitespace. The entry is one line, a single joke about crypto and
trading life, with a clear setup and a turn, a recognisable trading detail,
tight phrasing and the punchline at the end.
"""

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main


class TestJokeContent(unittest.TestCase):
    def test_length_within_gate(self):
        self.assertGreaterEqual(len(main.JOKE), 1)
        self.assertLessEqual(len(main.JOKE), 200)

    def test_not_only_whitespace(self):
        self.assertTrue(main.JOKE.strip())

    def test_single_line(self):
        self.assertNotIn("\n", main.JOKE)
        self.assertNotIn("\r", main.JOKE)

    def test_valid_utf8(self):
        main.JOKE.encode("utf-8")

    def test_about_crypto_and_trading(self):
        lowered = main.JOKE.lower()
        self.assertIn("dip", lowered)
        self.assertIn("chart", lowered)

    def test_recognisable_trading_detail(self):
        lowered = main.JOKE.lower()
        self.assertTrue("chart" in lowered or "group chat" in lowered
                        or "bag" in lowered)

    def test_punchline_at_end(self):
        self.assertTrue(main.JOKE.rstrip().endswith("all along."))

    def test_has_setup_and_turn(self):
        # Setup: buying the dip. Turn: selling the panic (the wrong move),
        # then rationalising it as the plan.
        self.assertIn("bought the dip", main.JOKE)
        self.assertIn("sold the panic", main.JOKE)


class TestValidation(unittest.TestCase):
    def test_validate_accepts_joke(self):
        self.assertTrue(main.validate(main.JOKE))

    def test_validate_rejects_empty(self):
        self.assertFalse(main.validate(""))

    def test_validate_rejects_whitespace_only(self):
        self.assertFalse(main.validate("   \n\t"))

    def test_validate_rejects_too_long(self):
        self.assertFalse(main.validate("x" * 201))

    def test_validate_accepts_exactly_200(self):
        self.assertTrue(main.validate("x" * 200))

    def test_validate_rejects_multiline(self):
        self.assertFalse(main.validate("line one\nline two"))

    def test_validate_rejects_one_char_whitespace(self):
        self.assertFalse(main.validate(" "))


class TestRunIntegration(unittest.TestCase):
    def _run_main(self, out_path):
        env = dict(os.environ, ENTRY_OUTPUT=out_path)
        return subprocess.run(
            [sys.executable, "main.py"], cwd=os.path.dirname(
                os.path.abspath(__file__)), env=env,
            capture_output=True, text=True, timeout=30)

    def test_run_writes_entry_and_gate_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "nested", "entry.txt")
            result = self._run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, "rb") as f:
                raw = f.read()
            text = raw.decode("utf-8")
            self.assertEqual(text, main.JOKE)
            self.assertTrue(1 <= len(text) <= 200)
            self.assertTrue(text.strip())
            self.assertNotIn("\n", text)

    def test_run_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = os.path.join(tmp, "a", "entry.txt")
            out2 = os.path.join(tmp, "b", "entry.txt")
            self.assertEqual(self._run_main(out1).returncode, 0)
            self.assertEqual(self._run_main(out2).returncode, 0)
            with open(out1, "rb") as f:
                first = f.read()
            with open(out2, "rb") as f:
                second = f.read()
            self.assertEqual(first, second)

    def test_run_creates_missing_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "does", "not", "exist", "entry.txt")
            self.assertFalse(os.path.exists(os.path.dirname(out)))
            result = self._run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(os.path.exists(out))

    def test_run_writes_no_trailing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            self.assertEqual(self._run_main(out).returncode, 0)
            with open(out, "rb") as f:
                raw = f.read()
            self.assertFalse(raw.endswith(b"\n"))
            self.assertEqual(len(raw.decode("utf-8")), len(main.JOKE))


if __name__ == "__main__":
    unittest.main()
