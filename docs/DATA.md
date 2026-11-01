# Data sources

`data/sample.json` contains 85 questions from the final DoseBench dataset: 77 adapted from public datasets and 8 written by the authors. The other 145 questions were collected from Reddit and are not redistributed. Each entry includes the question, gold label, category, source, license, and a link to its saved results (`result_case_id`).

| Source and credit | Questions | License |
|---|---:|---|
| [K-QA — Itay Manes et al. (2024)](https://huggingface.co/datasets/Itaykhealth/K-QA) | 19 | [MIT](../licenses/K-QA-MIT.txt) |
| [HealthBench — OpenAI, Arora et al. (2025)](https://huggingface.co/datasets/openai/healthbench) | 17 | [MIT](../licenses/HealthBench-MIT.txt) |
| [MedicationQA — Asma Ben Abacha et al. (2019)](https://github.com/abachaa/Medication_QA_MedInfo2019) | 8 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [MeQSum — Asma Ben Abacha and Dina Demner-Fushman (2019)](https://github.com/abachaa/MeQSum) | 5 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [ExpertQA — Chaitanya Malaviya et al. (2024)](https://github.com/chaitanyamalaviya/ExpertQA) | 1 | [MIT](../licenses/ExpertQA-MIT.txt) |
| [RxBench-SOL — RxBench-SOL contributors (2026)](https://github.com/MrZak2/rxbench-sol) | 10 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [Meddies Patient Safety — MeddiesAI (2026)](https://huggingface.co/datasets/Meddies/meddies-patient-safety) | 9 | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| [AfriMed-QA v2 — Nimo et al. (2025)](https://huggingface.co/datasets/afrimedqa/afrimedqa_v2) | 3 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [MEDIQA2019 — Ben Abacha et al. (2019)](https://github.com/abachaa/MEDIQA2019) | 2 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [PatientSafetyBench — Corbeil et al. (2025)](https://huggingface.co/datasets/microsoft/PatientSafetyBench) | 2 | [CDLA-Permissive-2.0](https://cdla.dev/permissive-2-0/) |
| [smolified-MediMind — bubun123](https://huggingface.co/datasets/bubun123/smolified-medimind-personalized-medication-adherence-assistant-for-chronic-disease-management) | 1 | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Written by the authors for this benchmark | 8 | [MIT](../LICENSE) |

These are the adapted questions supplied for DoseBench, which differ from the original source questions. This release makes no further changes to their text or final labels. Retain the source credits and licenses when reusing them. The project MIT license does not replace the data's source licenses. The nine questions adapted from Meddies Patient Safety carry a non-commercial license; the rest permit commercial use.

`saved_results/` contains numerical results for all 230 cases, without full question text or Reddit IDs. `new_85` means 77 public-dataset questions plus eight developed questions. These 85 questions alone do not reproduce the full paper scores, which are computed over all 230.

Drug Facts text and structured rules are preserved from the supplied experimental package. Source records and question hashes are in `data/provenance.json`.
