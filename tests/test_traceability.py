"""Traceability integrity tests. python -m unittest discover -s tests -v"""

import unittest

from app.build import _load, validate


class TestTraceability(unittest.TestCase):
    def setUp(self):
        self.inv = _load("inventory.json")
        self.risks = _load("risk_register.json")
        self.controls = _load("control_mapping.json")
        self.evidence = _load("evidence.json")

    def test_no_broken_links(self):
        self.assertEqual(validate(self.inv, self.risks, self.controls, self.evidence), [])

    def test_every_risk_has_control_and_evidence(self):
        ctl = {c["id"]: c for c in self.controls}
        ev = {e["id"] for e in self.evidence}
        for r in self.risks:
            self.assertIn(r["control"], ctl, r["id"])
            self.assertIn(ctl[r["control"]]["evidence"], ev, r["id"])

    def test_detects_a_broken_link(self):
        bad = self.risks + [{"id": "x", "system": "nope", "title": "t", "owasp": "o",
                             "likelihood": "low", "impact": "low", "treatment": "mitigate",
                             "control": "ghost", "status": "open", "retest": "-"}]
        self.assertTrue(validate(self.inv, bad, self.controls, self.evidence))


if __name__ == "__main__":
    unittest.main()
