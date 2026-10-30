# Reproduction details

## Saved-result analysis

`python reproduce.py` joins the numerical results to final gold labels, scores each model and condition, and creates:

- `prompt_results.csv`: accuracy, false approval rate (FAR), AMBIGUOUS recall, and consistency for eight models × four conditions.
- `prompt_changes.csv`: median percentage-point changes from Standard and counts of models increasing, decreasing, or unchanged.
- `label_recall.csv`, `category_accuracy.csv`, `source_accuracy.csv`: Standard-condition breakdowns.
- `bootstrap_intervals.csv`: 2,000 question-level bootstrap resamples, seed 42, percentile endpoints.
- `confidence.csv`: verbal confidence for eight models and probe confidence for five open-weight models.
- `baseline_summary.csv`: coverage and accuracy on covered cases from saved baseline decisions.
- `TABLES.md`: readable prompt and confidence tables.
- Three figures in PDF and PNG: `decision_behavior`, `category_accuracy`, and `verbal_confidence`.

This reproduces the main numerical findings from saved results. It does not rerun model inference, reconstruct the unreleased question texts, regenerate manual annotation agreement, or reproduce the paper's typesetting.

### Scoring

A case's prediction is its unique most frequent valid YES, NO, or AMBIGUOUS decision across five runs. A tie or no valid decision is incorrect. Invalid decisions cast no vote, but remain in the five-run consistency denominator. FAR is the fraction of gold-NO cases predicted YES. Recall uses the cases with the corresponding gold label. Consistency is the maximum valid vote count divided by five, averaged over cases.

All expected runs must be present exactly once. The evaluator stops on missing, duplicate, or unknown case/run pairs. A missing result file is not treated as an invalid generated answer.

Verbal confidence uses each individual generated answer, scaled from 1–10 to 0–1. Answers with invalid decisions or missing/out-of-range confidence are excluded from confidence analysis only. Standard includes 9,185 of 9,200 responses. Probe confidence uses the separate decision-only prompt's answer, with one result per case and open-weight model. ECE uses ten equal-width bins; confidence 1.0 belongs to the final bin. Empty groups are written as null, not zero.

Bootstrap sampling preserves the order of rows in `case_metadata.csv`. IDs have been replaced, but row order is retained to preserve seeded resampling. Sample-level confidence and case-level plurality accuracy have different denominators and should not be substituted for one another.

### Validation against supplied results

The 36,800 decisions were cross-checked against the separate supplied response files after restricting to the final 230 cases. All matched. The saved baseline was rerun on the private final question file: 38 covered cases and 13 correct decisions. Tests protect the main Standard-condition values, dataset counts, the confidence denominator, and important scoring edge cases.

## Optional new generations

The open-weight runner uses prompt strings and the Drug Facts sheet from the supplied code package. It records the generated text along with parsed decisions and confidence. These new response files are local outputs and are excluded from version control.

The first public runner deliberately fixes these issues in the supplied runner:

1. Accept only an exact A/B/C decision in a JSON object; do not infer A from a word beginning with A.
2. Accept only integer confidence values from 1 to 10; reject booleans and fractional values.
3. Set `top_k=0` explicitly, with temperature 0.7, top-p 1.0, and 512 maximum new tokens.
4. Derive a repeatable seed as `base_seed + question_index * runs + run_number` (zero-based question index, one-based run number).
5. Accept an explicit input file and refuse to overwrite an existing response CSV.

These changes do not alter the released historical numerical results. The new seed formula and parser are documented release choices, not a claim about the exact historical implementation. Model/library versions, hardware, and stricter parsing can change fresh results. Generation was not tested with full model weights during release preparation; CPU scoring and saved-result plotting were tested. The supplied baseline was also checked privately before exporting its numerical outcomes.

API-model runners and token-probe generation are outside this first release. The public saved outputs are enough to reproduce their reported numerical results without API access.

## Environment

The analysis was checked with Python 3.12.14, NumPy 2.3.5, and Matplotlib 3.10.8. `requirements.txt` pins the plotting libraries. The evaluator uses the Python standard library only. Install a suitable PyTorch build, Transformers, and Accelerate separately only if running new model generations.

## Deferred baseline implementation

The supplied extractor comments describe some elements as adopted as-is from medExtractR. Its [upstream package description](https://github.com/cran/medExtractR/blob/master/DESCRIPTION) specifies GPL (>= 2). The supplied notes do not establish which code, if any, was copied. To avoid presenting this implementation under the repository's MIT license without resolving that provenance, the first release includes only its numerical decisions, summary, and structured rules. The original implementation remains in the private preparation files.
