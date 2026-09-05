import unittest
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class OriginationLifecycleTests(unittest.TestCase):
    def test_degraded_line_can_pause_without_becoming_active(self):
        project = json.loads((ROOT / "alludium/project-types/vc_sourcing_line.json").read_text())
        self.assertIn({"from": "degraded", "to": "paused"}, project["initialVersion"]["lifecycleTransitions"])

if __name__ == "__main__":
    unittest.main()
