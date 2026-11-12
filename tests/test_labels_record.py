"""Exercise the generic export against the deployed build-sync contract."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SYNC, PRODUCER, SOURCE, BUILD, COMMIT, VERSION, DOMAIN = sys.argv[1:]
sys.argv[1:] = []
SOURCE, BUILD = Path(SOURCE), Path(BUILD)


class LabelsRecord(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / "labels.toml"
        self.output.write_bytes((BUILD / "labels.toml").read_bytes())
        self.record = self.root / "labels.toml.build.json"
        self.ledger = self.root / "dependency-ledger.jsonl"
        self.rows = [json.loads(line) for line in
                     (BUILD / "dependency-ledger.jsonl").read_text().splitlines()]
        self.write_ledger()

    def write_ledger(self):
        self.ledger.write_text("".join(json.dumps(row) + "\n" for row in self.rows))

    def run_record(self):
        return subprocess.run(
            [SYNC, "--ledger", str(self.ledger), "--source-root", str(SOURCE),
             "--source-repository", "orchestration", "--source-commit", COMMIT,
             "--producer", PRODUCER, "--domain", DOMAIN,
             "--record", str(self.output)],
            capture_output=True, text=True, timeout=30, check=False)

    def assert_identity(self, record):
        expected = {
            "bin": "labels.toml", "installed_name": "labels.toml",
            "package": "orchestration", "release_group": "orchestration",
            "repository": "orchestration", "source_commit": COMMIT,
            "version": VERSION, "domain": DOMAIN, "profile": "generated",
            "sha256": hashlib.sha256(self.output.read_bytes()).hexdigest(),
        }
        for key, value in expected.items():
            self.assertEqual(record[key], value, key)
        self.assertIn("superloop-lint", record["cargo_version"])
        self.assertEqual(record["cargo_version"], record["rustc_version"])

    def test_built_export_has_source_identity(self):
        self.assert_identity(json.loads((BUILD / "labels.toml.build.json").read_text()))

    def test_repeated_record_preserves_output_and_record(self):
        output_before = (self.output.read_bytes(), self.output.stat().st_mtime_ns)
        first = self.run_record()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assert_identity(json.loads(self.record.read_text()))
        record_before = (self.record.read_bytes(), self.record.stat().st_mtime_ns)
        second = self.run_record()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(output_before, (self.output.read_bytes(), self.output.stat().st_mtime_ns))
        self.assertEqual(record_before, (self.record.read_bytes(), self.record.stat().st_mtime_ns))

    def assert_refusal(self, message):
        self.write_ledger()
        before = self.output.read_bytes()
        result = self.run_record()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertFalse(self.record.exists(), result.stderr)
        self.assertEqual(before, self.output.read_bytes())

    def test_absent_identity_names_the_output(self):
        self.rows = []
        self.assert_refusal("build output needs exactly one program identity: labels.toml")

    def test_duplicate_identity_names_the_output(self):
        self.rows += self.rows
        self.assert_refusal("build output needs exactly one program identity: labels.toml")

    def test_wrong_authority_names_the_identity(self):
        self.rows[0]["version_authority"] = "wrong-roster"
        self.assert_refusal("script version authority differs from roster: share/orchestration/labels.toml")

    def test_wrong_release_group_names_the_identity(self):
        self.rows[0]["release_group"] = "wrong-group"
        self.assert_refusal("script version authority differs from roster: share/orchestration/labels.toml")


if __name__ == "__main__":
    unittest.main()
