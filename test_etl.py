import unittest

from src.etl import transform

ROW = dict(id="1", created_at="02.05.2026 21:00", category=" CARD ", channel="Chat",
           hours="9", sla_hours="8", csat="")


class TransformTest(unittest.TestCase):
    def test_cleans_values(self):
        row = transform([ROW])[0][0]
        self.assertEqual(row[2:5], ("2026-05", "Night", "Card"))
        self.assertEqual(row[8:], (0, None))

    def test_removes_bad_rows(self):
        clean, removed = transform([ROW, ROW, {**ROW, "id": "2", "hours": "-1"}])
        self.assertEqual(len(clean), 1)
        self.assertEqual(removed, {"duplicates": 1, "invalid_duration": 1})
