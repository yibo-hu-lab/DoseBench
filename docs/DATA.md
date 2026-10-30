# Data sources

`data/sample.json` contains 50 public-source questions from the final DoseBench dataset. Each entry includes the question, gold label, category, source, license, and a link to its saved results (`result_case_id`).

| Source and credit | Questions | License |
|---|---:|---|
| [K-QA — Itay Manes et al. (2024)](https://huggingface.co/datasets/Itaykhealth/K-QA) | 19 | [MIT](../licenses/K-QA-MIT.txt) |
| [HealthBench — OpenAI, Arora et al. (2025)](https://huggingface.co/datasets/openai/healthbench) | 17 | [MIT](../licenses/HealthBench-MIT.txt) |
| [MedicationQA — Asma Ben Abacha et al. (2019)](https://github.com/abachaa/Medication_QA_MedInfo2019) | 8 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [MeQSum — Asma Ben Abacha and Dina Demner-Fushman (2019)](https://github.com/abachaa/MeQSum) | 5 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [ExpertQA — Chaitanya Malaviya et al. (2024)](https://github.com/chaitanyamalaviya/ExpertQA) | 1 | [MIT](../licenses/ExpertQA-MIT.txt) |

These are the adapted questions supplied for DoseBench, which differ from the original source questions. This release makes no further changes to their text or final labels. Retain the source credits and licenses when reusing them. The project MIT license does not replace the data's source licenses.

`saved_results/` contains numerical results for all 230 cases, without full question text or Reddit IDs. `new_85` means 77 public-dataset questions plus eight developed questions. The 50-question sample alone does not reproduce the full paper scores.

Drug Facts text and structured rules are preserved from the supplied experimental package. Source records and question hashes are in `data/provenance.json`.
