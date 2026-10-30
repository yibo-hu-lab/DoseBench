# Data scope and attribution

## Shareable question sample

`data/sample.json` contains six HealthBench-derived entries from the final 230-question DoseBench dataset: N-Q003, N-Q051, N-Q054, N-Q056, N-Q088, and N-Q089. Their question text and gold labels are unchanged from the final gold file. There are two YES, two NO, and two AMBIGUOUS examples.

Fields:

- `case_id`: DoseBench sample identifier; not a Reddit ID.
- `question`: the question evaluated in DoseBench.
- `gold`: final DoseBench label.
- `category`: category as stored in the final gold file.
- `source`, `source_item_id`, `license`: upstream attribution.
- `result_case_id`: link to the numerical rows in `saved_results/`.

The benchmark question text differs from the upstream HealthBench conversation text. We preserve the supplied DoseBench version and identify the upstream source, without attributing undocumented adaptation steps to a particular person. The source conversations' rubric labels are not DoseBench's gold labels.

Upstream: OpenAI, **HealthBench: Evaluating Large Language Models Towards Improved Human Health** (2025), [paper](https://arxiv.org/abs/2505.08775), [official dataset](https://huggingface.co/datasets/openai/healthbench), [license declaration](https://github.com/openai/simple-evals#benchmarks), [MIT license](../licenses/HealthBench-MIT.txt).

All six source IDs were checked in the official `2025-05-07-06-14-12_oss_eval.jsonl` release. `data/provenance.json` records its SHA-256 digest and hashes of each source prompt and benchmark question. The MIT notice is retained. DoseBench-specific labels and metadata fall under the project license.

## Saved numerical results

The saved results cover all 230 questions but do not contain their full text. They retain the original decisions and confidence values; incorrect and invalid decisions have not been repaired. Result IDs are new arbitrary identifiers. The private mapping to original records is not distributed.

| File | Rows | Fields |
|---|---:|---|
| `case_metadata.csv` | 230 | Result ID, final gold label, normalized category, source group |
| `model_decisions.csv` | 36,800 | Result ID, model, condition, run (1–5), decision, verbal confidence |
| `probe_decisions.csv` | 1,150 | Result ID, open-weight model, run (1), decision, probe confidence |
| `baseline_decisions.csv` | 230 | Result ID and deterministic baseline outcome |

The final labels are YES (74), NO (114), and AMBIGUOUS (42). Category spelling variants are consolidated into the paper's six categories: interval (31), rolling 24-hour total (13), multiple medications (50), repeated dosing (32), missing information (36), and dose safety (68).

## Experimental inputs

`data/drug_facts.txt` and `data/drug_rules.json` are preserved byte-for-byte from the supplied code package. The former is the benchmark's Drug Facts sheet, not a live copy of a current product label. The latter supports the baseline and is not a complete executable implementation of every human annotation rule. The preserved prompt strings are in `code/prompts.py`.
