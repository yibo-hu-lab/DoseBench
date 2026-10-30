# DoseBench

Code and results for [Can I Take Another Dose? DoseBench: Evaluating LLM Decision-Making in OTC Dosing QA](https://arxiv.org/abs/2606.04262).

DoseBench evaluates whether language models can answer adult acetaminophen and ibuprofen dosing questions with **YES**, **NO**, or **AMBIGUOUS**. The paper evaluates eight models on 230 questions, with five responses per question under four prompt conditions.

📄 Paper: https://arxiv.org/abs/2606.04262

## Reproduce the tables and figures

Use Python 3.11 or newer. Open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
python reproduce.py
```

After installing dependencies, the second command runs offline. It rebuilds the main numerical tables and three empirical figures from saved results. **No GPU, API key, or model download is needed.** Outputs are written to `results/` as CSV, Markdown, PDF, and PNG files.

The plots reproduce the numerical content of the paper's decision-behavior, question-category, and verbal-confidence figures. Their styling is simplified.

## What is included

| Path | Contents |
|---|---|
| `data/sample.json` | 50 public-source questions with gold labels |
| `data/provenance.json` | Source IDs and hashes for the sample |
| `data/drug_facts.txt` | Drug Facts text preserved from the supplied experimental code package |
| `data/drug_rules.json` | Structured rules used by the deterministic baseline |
| `saved_results/` | Numerical decisions and confidence scores for all eight models; no full question text or Reddit IDs |
| `code/` | Prompt construction, optional open-weight model runner, and scoring |
| `reproduce.py` | One-command analysis of the saved results |
| `tests/` | Checks for scoring and release consistency |
| `results/` | Rebuilt tables and figures |

The 50 questions are a subset of the final dataset. Their text and gold labels are unchanged. Reddit question text and original Reddit IDs are not included.

Code uses the [MIT license](LICENSE). Dataset licenses and credits are listed in [Data sources](docs/DATA.md). For new model runs, see [Running a model](docs/REPRODUCIBILITY.md).

## Citation

```bibtex
@article{kousar2026dosebench,
  title={Can I Take Another Dose? DoseBench: Evaluating LLM Decision-Making in OTC Dosing QA},
  author={Kousar, Maroof and Han, Jinsung and Chandra, Mohit and De Choudhury, Munmun and Hu, Yibo},
  journal={arXiv preprint arXiv:2606.04262},
  year={2026}
}
```

```
