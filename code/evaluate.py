"""Score one model/condition CSV against an explicit gold file (standard library only)."""
import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

LABELS = ('YES', 'NO', 'AMBIGUOUS')


def load_gold(path):
    path = Path(path)
    with path.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle)) if path.suffix == '.csv' else json.load(handle)
    out = {}
    for row in rows:
        cid = str(row['case_id'])
        if cid in out or row['gold'] not in LABELS:
            raise ValueError(f'Duplicate ID or invalid gold label: {cid}')
        out[cid] = dict(row, case_id=cid)
    if not out:
        raise ValueError('Gold file is empty')
    return out


def accepted(row):
    return (row.get('decision') in LABELS and
            row.get('parse_status', 'valid') not in
            {'missing', 'invalid', 'invalid_json', 'invalid_decision', 'error'})


def percentage(numerator, denominator):
    return 100 * numerator / denominator if denominator else None


def calibration(pairs, bins=10):
    if not pairs:
        return None
    groups = defaultdict(list)
    for confidence, correct in pairs:
        groups[min(int(confidence * bins), bins - 1)].append((confidence, correct))
    return sum(abs(sum(c for c, _ in group) - sum(ok for _, ok in group))
               for group in groups.values()) / len(pairs)


def evaluate(gold, rows, runs=5, confidence_scale=10):
    if runs < 1 or confidence_scale not in (1, 10):
        raise ValueError('Use positive runs and confidence scale 1 or 10')
    grouped = defaultdict(list)
    seen = set()
    for row in rows:
        cid = str(row['case_id'])
        run = int(row['run'])
        if cid not in gold or not 1 <= run <= runs or (cid, run) in seen:
            raise ValueError(f'Unknown case, invalid run, or duplicate response: {cid}, {run}')
        seen.add((cid, run))
        grouped[cid].append(row)
    # Fail on incomplete experiments rather than silently bias metrics.
    if len(seen) != len(gold) * runs:
        raise ValueError(f'Expected {len(gold) * runs} rows, got {len(seen)}')
    predictions = {}
    consistency = []
    pairs = []
    invalid = 0
    for cid in gold:
        votes = Counter(row['decision'] for row in grouped[cid] if accepted(row))
        maximum = max(votes.values(), default=0)
        winners = [label for label, count in votes.items() if count == maximum]
        predictions[cid] = winners[0] if len(winners) == 1 else 'TIE_OR_INVALID'
        consistency.append(maximum / runs)
        for row in grouped[cid]:
            if not accepted(row):
                invalid += 1
                continue
            try:
                value = float(row['confidence'])
            except (KeyError, TypeError, ValueError):
                continue
            low = 1 if confidence_scale == 10 else 0
            if math.isfinite(value) and low <= value <= confidence_scale:
                pairs.append((value / confidence_scale, row['decision'] == gold[cid]['gold']))
    def accuracy(ids):
        return percentage(sum(predictions[c] == gold[c]['gold'] for c in ids), len(ids))
    no = [c for c in gold if gold[c]['gold'] == 'NO']
    correct = [c for c, ok in pairs if ok]
    wrong = [c for c, ok in pairs if not ok]
    return {
        'questions': len(gold), 'responses': len(rows), 'runs_per_question': runs,
        'accuracy_pct': accuracy(list(gold)),
        'false_approval_rate_pct': percentage(sum(predictions[c] == 'YES' for c in no), len(no)),
        'recall_pct': {label: accuracy([c for c in gold if gold[c]['gold'] == label]) for label in LABELS},
        'consistency_pct': 100 * sum(consistency) / len(gold),
        'invalid_decisions': invalid,
        'ties_or_no_valid_decision': sum(v == 'TIE_OR_INVALID' for v in predictions.values()),
        'confidence': {
            'included': len(pairs), 'excluded': len(rows) - len(pairs),
            'mean_correct': sum(correct) / len(correct) if correct else None,
            'mean_incorrect': sum(wrong) / len(wrong) if wrong else None,
            'ece_10_bins': calibration(pairs),
        },
        'accuracy_by_category_pct': {
            category: accuracy([c for c in gold if gold[c].get('category', '') == category])
            for category in sorted({q.get('category', '') for q in gold.values()})
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gold', required=True, help='JSON or CSV: case_id, question, gold, category')
    parser.add_argument('--responses', required=True, help='CSV: case_id, run, decision, confidence, parse_status')
    parser.add_argument('--runs', type=int, default=5)
    parser.add_argument('--confidence-scale', type=int, choices=(1, 10), default=10)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    with open(args.responses, encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    result = evaluate(load_gold(args.gold), rows, args.runs, args.confidence_scale)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
