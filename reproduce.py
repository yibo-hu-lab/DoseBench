#!/usr/bin/env python3
"""Rebuild the main numerical tables and figures from saved results, without model calls."""
import argparse
import csv
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'code'))
from evaluate import LABELS, accepted, evaluate, load_gold

MODELS = ['Qwen2.5-7B', 'Qwen2.5-14B', 'Qwen2.5-32B', 'Mistral-7B',
          'Llama-3-8B', 'GPT-4o-mini', 'GPT-5.4-mini', 'GPT-5.6-terra']
CONDITIONS = ['Standard', 'Checklist', 'Drug Facts', 'Both']
CATEGORIES = ['Time Between Doses', 'Rolling 24-Hour Total', 'Multiple Medications',
              'Repeated Dosing', 'Missing Dosing Information', 'Dose Safety and Side Effects']


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def predictions(rows):
    grouped = defaultdict(Counter)
    for row in rows:
        if accepted(row):
            grouped[row['case_id']][row['decision']] += 1
    out = {}
    for cid, counts in grouped.items():
        maximum = max(counts.values())
        best = [label for label, count in counts.items() if count == maximum]
        out[cid] = best[0] if len(best) == 1 else 'TIE_OR_INVALID'
    return out


def bootstrap(gold, pred):
    # File order is preserved so the 2,000 seeded draws are reproducible.
    ids = list(gold)
    rng = random.Random(42)
    accuracy, far = [], []
    for _ in range(2000):
        sample = [rng.choice(ids) for _ in ids]
        accuracy.append(100 * sum(pred.get(cid) == gold[cid]['gold'] for cid in sample) / len(sample))
        negatives = [cid for cid in sample if gold[cid]['gold'] == 'NO']
        if negatives:
            far.append(100 * sum(pred.get(cid) == 'YES' for cid in negatives) / len(negatives))
    accuracy.sort(); far.sort()
    return accuracy[50], accuracy[1950], far[int(.025 * len(far))], far[int(.975 * len(far))]


def plots(out, metrics, gold):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.size': 10, 'pdf.fonttype': 42})
    standard = [metrics[(model, 'Standard')] for model in MODELS]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True,
                             gridspec_kw={'width_ratios': [1.2, 1]})
    for i, (model, result) in enumerate(zip(MODELS, standard)):
        x, y = result['accuracy_pct'], 100 - result['false_approval_rate_pct']
        axes[0].scatter(x, y, color='#2979a3' if i < 5 else '#bd5b29', s=45)
        offset = (-5, 10) if model == 'Qwen2.5-14B' else (4, -12) if model == 'GPT-5.6-terra' else (4, 5)
        axes[0].annotate(model, (x, y), xytext=offset, textcoords='offset points', fontsize=8,
                         ha='right' if model == 'Qwen2.5-14B' else 'left')
    axes[0].set(xlabel='Accuracy (%)', ylabel='Non-approval rate (100 − FAR) (%)',
                xlim=(42, 69), ylim=(30, 100), title='Standard condition')
    heatmap(axes[1], [[r['recall_pct'][label] for label in LABELS] for r in standard],
            [f'{label}\n(n={sum(q["gold"] == label for q in gold.values())})' for label in LABELS],
            MODELS, 'Recall by gold label')
    save_figure(fig, out, 'decision_behavior'); plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5), constrained_layout=True)
    heatmap(ax, [[r['accuracy_by_category_pct'][cat] for cat in CATEGORIES] for r in standard],
            ['Interval\n(n=31)', '24-hour total\n(n=13)', 'Multiple drugs\n(n=50)',
             'Repeated dosing\n(n=32)', 'Missing facts\n(n=36)', 'Dose safety\n(n=68)'],
            MODELS, 'Accuracy by question category — Standard condition')
    save_figure(fig, out, 'category_accuracy'); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)
    y = np.arange(len(MODELS))
    for offset, key, label, color in [(-.18, 'mean_correct', 'Correct', '#2979a3'),
                                     (.18, 'mean_incorrect', 'Incorrect', '#bd5b29')]:
        values = [r['confidence'][key] for r in standard]
        bars = ax.barh(y + offset, values, height=.32, label=label, color=color)
        ax.bar_label(bars, fmt='%.3f', padding=3, fontsize=9)
    ax.set(yticks=y, yticklabels=MODELS, xlim=(0, 1.07), xlabel='Mean verbal confidence',
           title='Confidence by answer correctness — Standard condition')
    ax.invert_yaxis()
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.01), ncol=2, frameon=False)
    ax.set_title('Confidence by answer correctness — Standard condition', pad=30)
    ax.set_ylim(len(MODELS) - .5, -.9)
    save_figure(fig, out, 'verbal_confidence'); plt.close(fig)


def heatmap(ax, data, columns, rows, title):
    import numpy as np
    values = np.array(data)
    ax.imshow(values, vmin=0, vmax=100, cmap='Blues', aspect='auto')
    ax.set(xticks=range(len(columns)), xticklabels=columns, yticks=range(len(rows)),
           yticklabels=rows, title=title)
    for i in range(len(rows)):
        for j in range(len(columns)):
            ax.text(j, i, f'{values[i,j]:.1f}', ha='center', va='center',
                    color='white' if values[i,j] >= 60 else 'black', fontsize=9)


def save_figure(fig, out, name):
    fig.savefig(out / f'{name}.pdf')
    fig.savefig(out / f'{name}.png', dpi=160)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'results')
    args = parser.parse_args()
    out = args.out; out.mkdir(parents=True, exist_ok=True)
    gold = load_gold(ROOT / 'saved_results/case_metadata.csv')
    all_rows = read_csv(ROOT / 'saved_results/model_decisions.csv')
    assert len(gold) == 230 and len(all_rows) == 36800, 'Incomplete saved results'
    grouped = defaultdict(list)
    for row in all_rows:
        grouped[(row['model'], row['condition'])].append(row)
    assert set(grouped) == {(m, c) for m in MODELS for c in CONDITIONS}
    metrics = {key: evaluate(gold, rows) for key, rows in grouped.items()}
    table = [dict(model=m, condition=c, accuracy=metrics[m,c]['accuracy_pct'],
                  far=metrics[m,c]['false_approval_rate_pct'],
                  ambiguous_recall=metrics[m,c]['recall_pct']['AMBIGUOUS'],
                  consistency=metrics[m,c]['consistency_pct']) for m in MODELS for c in CONDITIONS]
    write_csv(out / 'prompt_results.csv', table)
    lines = ['# Results on the final 230 questions', '',
             'Generated from saved decisions. Percentages use case-level plurality across five runs.', '',
             '## Prompt results', '', '| Model | Condition | Accuracy | FAR | Amb. recall | Consistency |',
             '|---|---|---:|---:|---:|---:|']
    for row in table:
        lines.append('| {model} | {condition} | {accuracy:.1f} | {far:.1f} | {ambiguous_recall:.1f} | {consistency:.1f} |'.format(**row))
    delta_rows = []
    for condition in CONDITIONS[1:]:
        row = dict(condition=condition)
        for metric, key in [('accuracy','accuracy_pct'),('far','false_approval_rate_pct'),('ambiguous_recall',None)]:
            values = [(metrics[m,condition][key] - metrics[m,'Standard'][key]) if key else
                      (metrics[m,condition]['recall_pct']['AMBIGUOUS'] - metrics[m,'Standard']['recall_pct']['AMBIGUOUS']) for m in MODELS]
            row[metric + '_median_pp'] = statistics.median(values)
            row[metric + '_increased'] = sum(x > 0 for x in values)
            row[metric + '_decreased'] = sum(x < 0 for x in values)
            row[metric + '_unchanged'] = sum(x == 0 for x in values)
        delta_rows.append(row)
    write_csv(out / 'prompt_changes.csv', delta_rows)
    recalls = [dict(model=m, **metrics[m,'Standard']['recall_pct']) for m in MODELS]
    write_csv(out / 'label_recall.csv', recalls)
    category = [dict(model=m, **metrics[m,'Standard']['accuracy_by_category_pct']) for m in MODELS]
    write_csv(out / 'category_accuracy.csv', category)
    source = []; intervals = []
    for model in MODELS:
        pred = predictions(grouped[model,'Standard'])
        row = dict(model=model)
        for group in ('reddit_145','new_85'):
            ids = [cid for cid,q in gold.items() if q['source_group']==group]
            row[group] = 100 * sum(pred.get(cid)==gold[cid]['gold'] for cid in ids) / len(ids)
        source.append(row)
        a0,a1,f0,f1 = bootstrap(gold,pred)
        intervals.append(dict(model=model,accuracy_low=a0,accuracy_high=a1,far_low=f0,far_high=f1))
    write_csv(out / 'source_accuracy.csv', source)
    write_csv(out / 'bootstrap_intervals.csv', intervals)
    confidence = [dict(model=m,measure='verbal',**metrics[m,'Standard']['confidence']) for m in MODELS]
    probes = read_csv(ROOT / 'saved_results/probe_decisions.csv')
    for model in MODELS[:5]:
        result = evaluate(gold, [r for r in probes if r['model']==model], runs=1, confidence_scale=1)
        confidence.append(dict(model=model,measure='probe',**result['confidence']))
    write_csv(out / 'confidence.csv', confidence)
    lines.extend(['', '## Standard-condition confidence', '', '| Model | Measure | Correct | Incorrect | ECE | Included |',
                  '|---|---|---:|---:|---:|---:|'])
    for r in confidence:
        lines.append('| {model} | {measure} | {mean_correct:.3f} | {mean_incorrect:.3f} | {ece_10_bins:.3f} | {included} |'.format(**r))
    baseline = read_csv(ROOT / 'saved_results/baseline_decisions.csv')
    assert len(baseline) == len(gold) and {r['case_id'] for r in baseline} == set(gold)
    covered = [r for r in baseline if r['decision'] in LABELS]
    hit = sum(r['decision'] == gold[r['case_id']]['gold'] for r in covered)
    baseline_rows = [dict(method='Rule baseline',questions=len(gold),covered=len(covered),
                          coverage_pct=100*len(covered)/len(gold),
                          accuracy_on_covered_pct=100*hit/len(covered))]
    write_csv(out / 'baseline_summary.csv', baseline_rows)
    lines.extend(['', '## Rule baseline', '',
                  f"Covered {len(covered)}/{len(gold)} questions; correct on {hit}/{len(covered)} covered questions.",
                  '', 'Other tables are saved as CSV files alongside this report.'])
    (out / 'TABLES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    plots(out, metrics, gold)
    print(f'Rebuilt tables and 3 empirical figures in {out}')
    print('No model calls, API keys, private questions, or network access required.')


if __name__ == '__main__':
    main()
