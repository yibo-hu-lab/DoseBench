import csv
import hashlib
import json
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'code'))
from evaluate import evaluate, load_gold


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gold = load_gold(ROOT / 'saved_results/case_metadata.csv')
        cls.groups = defaultdict(list)
        with (ROOT / 'saved_results/model_decisions.csv').open() as handle:
            for row in csv.DictReader(handle):
                cls.groups[row['model'],row['condition']].append(row)

    def test_counts_and_all_conditions(self):
        self.assertEqual(Counter(q['gold'] for q in self.gold.values()),
                         {'YES':74,'NO':114,'AMBIGUOUS':42})
        self.assertEqual(len(self.groups), 32)
        for key, rows in self.groups.items():
            self.assertEqual(len(rows),1150)
            evaluate(self.gold, rows)

    def test_standard_paper_values(self):
        expected = {'Qwen2.5-7B':(53.0,28.9,33.3,82.9),
                    'Qwen2.5-14B':(53.0,14.0,57.1,86.0),
                    'Qwen2.5-32B':(57.8,24.6,16.7,90.6),
                    'Mistral-7B':(44.8,60.5,7.1,85.1),
                    'Llama-3-8B':(49.6,36.0,19.0,80.5),
                    'GPT-4o-mini':(54.3,48.2,9.5,92.6),
                    'GPT-5.4-mini':(62.2,22.8,69.0,87.4),
                    'GPT-5.6-terra':(54.8,14.9,78.6,93.6)}
        included=0
        for model, values in expected.items():
            r=evaluate(self.gold,self.groups[model,'Standard'])
            actual=(r['accuracy_pct'],r['false_approval_rate_pct'],r['recall_pct']['AMBIGUOUS'],r['consistency_pct'])
            self.assertEqual(tuple(round(v,1) for v in actual),values)
            included+=r['confidence']['included']
        self.assertEqual(included,9185)

    def test_sample_integrity(self):
        rows=json.loads((ROOT/'data/sample.json').read_text())
        provenance=json.loads((ROOT/'data/provenance.json').read_text())
        hashes={r['case_id']:r['benchmark_question_sha256'] for r in provenance['records']}
        self.assertEqual(len(rows),50)
        self.assertEqual(Counter(r['source'] for r in rows),
                         {'K-QA':19,'HealthBench':17,'MedicationQA':8,'MeQSum':5,'ExpertQA':1})
        for row in rows:
            self.assertEqual(hashlib.sha256(row['question'].encode()).hexdigest(),hashes[row['case_id']])
            self.assertEqual(self.gold[row['result_case_id']]['gold'],row['gold'])
            self.assertIn(row['license'], ('MIT', 'CC-BY-4.0'))

    def test_result_schema_has_no_text_or_original_ids(self):
        expected={'case_metadata.csv':{'case_id','gold','category','source_group'},
                  'model_decisions.csv':{'case_id','model','condition','run','decision','confidence'},
                  'probe_decisions.csv':{'case_id','model','run','decision','confidence'},
                  'baseline_decisions.csv':{'case_id','decision'}}
        for name,fields in expected.items():
            with (ROOT/'saved_results'/name).open() as handle:
                reader=csv.DictReader(handle)
                self.assertEqual(set(reader.fieldnames),fields)
                for row in reader:
                    self.assertRegex(row['case_id'],r'^case_\d{3}$')


if __name__=='__main__':
    unittest.main()
