# Running a model (optional)

To generate new answers, install PyTorch for your hardware, `transformers`, and `accelerate`. You need access to the model weights and suitable hardware.

```bash
python code/run_model.py --model Qwen/Qwen2.5-7B-Instruct --condition standard --input data/sample.json --out runs/sample.csv
python code/evaluate.py --gold data/sample.json --responses runs/sample.csv --out runs/sample_metrics.json
```

Conditions: `standard`, `checklist`, `drug_facts`, or `both`. Each uses five runs. Use a new output filename for each experiment.

The runner requires JSON with an exact A/B/C decision and integer confidence from 1 to 10. It uses temperature 0.7, top-p 1.0, top-k 0, and at most 512 new tokens. Seeds are `42 + question_index * runs + run_number`. This parser and seed formula differ from the supplied older runner; fresh results may differ. Full model generation has not been tested in this release.

## Scoring

The most common valid answer is the case prediction; ties count as incorrect. Consistency uses all five runs. FAR measures YES predictions on gold-NO cases. Verbal confidence excludes invalid decisions or missing scores: 9,185 Standard responses remain. Probe confidence uses separate answers. ECE uses ten bins; bootstrap intervals use 2,000 resamples with seed 42.

API and probe generation code is not included. Baseline results are included; its extractor code is deferred pending license clarification.

To run the checks:

```bash
python -m unittest discover -s tests -v
```
