import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / "scenarios.json").read_text(encoding="utf-8"))


class HardeningScenarioContract(unittest.TestCase):
    def test_schema_and_identity(self):
        self.assertEqual(DATA["schemaVersion"], 1)
        self.assertTrue(DATA["system"])
        self.assertTrue(DATA["source"])
        self.assertGreaterEqual(len(DATA["requiredInvariants"]), 4)
        self.assertGreaterEqual(len(DATA["scenarios"]), 5)

    def test_scenario_ids_are_unique_and_machine_safe(self):
        ids = [item["id"] for item in DATA["scenarios"]]
        self.assertEqual(len(ids), len(set(ids)))
        for scenario_id in ids:
            self.assertRegex(scenario_id, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_each_scenario_is_actionable_and_covers_every_invariant(self):
        allowed = set(DATA["requiredInvariants"])
        covered = set()
        for item in DATA["scenarios"]:
            self.assertGreaterEqual(len(item["setup"]), 1)
            self.assertTrue(item["action"].strip())
            self.assertGreaterEqual(len(item["expect"]), 2)
            invariants = set(item["invariants"])
            self.assertTrue(invariants)
            self.assertFalse(invariants - allowed)
            covered.update(invariants)
        self.assertEqual(covered, allowed)

    def test_fixture_contains_no_credentials_or_live_endpoints(self):
        raw = json.dumps(DATA).lower()
        for marker in [
            "ghp_",
            "github_pat_",
            "access_token=",
            "refresh_token=",
            "client_secret=",
            "authorization: bearer ",
            "rtmp://",
        ]:
            self.assertNotIn(marker, raw)

    def test_expectations_are_not_false_successes(self):
        for item in DATA["scenarios"]:
            joined = " ".join(item["expect"]).lower()
            self.assertNotIn("ignore error", joined)
            self.assertNotIn("always succeeds", joined)


if __name__ == "__main__":
    unittest.main()
