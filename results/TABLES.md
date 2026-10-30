# Results on the final 230 questions

Generated from saved decisions. Percentages use case-level plurality across five runs.

## Prompt results

| Model | Condition | Accuracy | FAR | Amb. recall | Consistency |
|---|---|---:|---:|---:|---:|
| Qwen2.5-7B | Standard | 53.0 | 28.9 | 33.3 | 82.9 |
| Qwen2.5-7B | Checklist | 42.2 | 9.6 | 73.8 | 81.4 |
| Qwen2.5-7B | Drug Facts | 54.8 | 28.9 | 2.4 | 82.8 |
| Qwen2.5-7B | Both | 54.8 | 23.7 | 21.4 | 79.0 |
| Qwen2.5-14B | Standard | 53.0 | 14.0 | 57.1 | 86.0 |
| Qwen2.5-14B | Checklist | 50.9 | 10.5 | 78.6 | 87.9 |
| Qwen2.5-14B | Drug Facts | 57.0 | 14.9 | 40.5 | 87.0 |
| Qwen2.5-14B | Both | 55.2 | 10.5 | 54.8 | 86.2 |
| Qwen2.5-32B | Standard | 57.8 | 24.6 | 16.7 | 90.6 |
| Qwen2.5-32B | Checklist | 63.0 | 14.9 | 59.5 | 85.7 |
| Qwen2.5-32B | Drug Facts | 64.8 | 26.3 | 28.6 | 89.7 |
| Qwen2.5-32B | Both | 62.6 | 24.6 | 31.0 | 90.0 |
| Mistral-7B | Standard | 44.8 | 60.5 | 7.1 | 85.1 |
| Mistral-7B | Checklist | 49.1 | 59.6 | 33.3 | 81.6 |
| Mistral-7B | Drug Facts | 46.5 | 48.2 | 9.5 | 79.0 |
| Mistral-7B | Both | 48.7 | 51.8 | 11.9 | 79.7 |
| Llama-3-8B | Standard | 49.6 | 36.0 | 19.0 | 80.5 |
| Llama-3-8B | Checklist | 52.2 | 27.2 | 38.1 | 79.6 |
| Llama-3-8B | Drug Facts | 54.8 | 28.1 | 4.8 | 85.1 |
| Llama-3-8B | Both | 57.0 | 21.9 | 9.5 | 85.0 |
| GPT-4o-mini | Standard | 54.3 | 48.2 | 9.5 | 92.6 |
| GPT-4o-mini | Checklist | 56.1 | 46.5 | 33.3 | 87.0 |
| GPT-4o-mini | Drug Facts | 57.0 | 40.4 | 2.4 | 93.6 |
| GPT-4o-mini | Both | 56.1 | 41.2 | 7.1 | 91.1 |
| GPT-5.4-mini | Standard | 62.2 | 22.8 | 69.0 | 87.4 |
| GPT-5.4-mini | Checklist | 30.9 | 0.0 | 95.2 | 92.4 |
| GPT-5.4-mini | Drug Facts | 65.7 | 28.9 | 33.3 | 89.0 |
| GPT-5.4-mini | Both | 60.4 | 14.9 | 71.4 | 87.6 |
| GPT-5.6-terra | Standard | 54.8 | 14.9 | 78.6 | 93.6 |
| GPT-5.6-terra | Checklist | 42.6 | 5.3 | 95.2 | 95.7 |
| GPT-5.6-terra | Drug Facts | 67.0 | 14.9 | 66.7 | 94.0 |
| GPT-5.6-terra | Both | 62.2 | 12.3 | 76.2 | 93.0 |

## Standard-condition confidence

| Model | Measure | Correct | Incorrect | ECE | Included |
|---|---|---:|---:|---:|---:|
| Qwen2.5-7B | verbal | 0.601 | 0.583 | 0.313 | 1149 |
| Qwen2.5-14B | verbal | 0.787 | 0.664 | 0.237 | 1147 |
| Qwen2.5-32B | verbal | 0.889 | 0.845 | 0.292 | 1150 |
| Mistral-7B | verbal | 0.856 | 0.826 | 0.405 | 1142 |
| Llama-3-8B | verbal | 0.819 | 0.807 | 0.325 | 1147 |
| GPT-4o-mini | verbal | 0.884 | 0.860 | 0.332 | 1150 |
| GPT-5.4-mini | verbal | 0.872 | 0.779 | 0.234 | 1150 |
| GPT-5.6-terra | verbal | 0.921 | 0.864 | 0.346 | 1150 |
| Qwen2.5-7B | probe | 0.928 | 0.838 | 0.450 | 230 |
| Qwen2.5-14B | probe | 0.952 | 0.897 | 0.416 | 230 |
| Qwen2.5-32B | probe | 0.962 | 0.947 | 0.445 | 230 |
| Mistral-7B | probe | 0.895 | 0.834 | 0.438 | 230 |
| Llama-3-8B | probe | 0.858 | 0.813 | 0.331 | 230 |

## Rule baseline

Covered 38/230 questions; correct on 13/38 covered questions.

Other tables are saved as CSV files alongside this report.
