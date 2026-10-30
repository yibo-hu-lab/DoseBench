import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from evaluate import evaluate, calibration
from run_model import parse


class ScoringTests(unittest.TestCase):
    def test_invalids_remain_in_consistency_denominator(self):
        gold = {'one': {'gold': 'NO'}}
        rows = [dict(case_id='one', run=i+1, decision=d, confidence='9',
                     parse_status='valid' if d else 'missing')
                for i, d in enumerate(['NO', 'NO', 'YES', '', ''])]
        result = evaluate(gold, rows)
        self.assertEqual(result['accuracy_pct'], 100)
        self.assertEqual(result['consistency_pct'], 40)
        self.assertEqual(result['confidence']['excluded'], 2)

    def test_tie_is_incorrect(self):
        rows = [dict(case_id='one', run=i+1, decision=d, confidence='9')
                for i, d in enumerate(['YES', 'YES', 'NO', 'NO', 'AMBIGUOUS'])]
        self.assertEqual(evaluate({'one': {'gold': 'YES'}}, rows)['accuracy_pct'], 0)

    def test_missing_and_duplicate_runs_fail(self):
        row = dict(case_id='one', run=1, decision='NO')
        for rows in ([row], [row] * 5):
            with self.assertRaises(ValueError):
                evaluate({'one': {'gold': 'NO'}}, rows)

    def test_ece_boundaries(self):
        self.assertAlmostEqual(calibration([(1, True), (0, False)]), 0)
        self.assertAlmostEqual(calibration([(0.9, False), (0.9, True)]), .4)

    def test_strict_parser(self):
        self.assertEqual(parse('{"decision":"A","confidence":9}')[:2], ('YES', 9))
        self.assertIsNone(parse('{"decision":"Apple","confidence":9}')[0])
        for value in ('11', 'true', '9.5'):
            self.assertIsNone(parse('{"decision":"B","confidence":' + value + '}')[1])
        self.assertIsNone(parse('[]')[0])


if __name__ == '__main__':
    unittest.main()
