"""Prompt text preserved from the supplied DoseBench code package."""
CHECKLIST = ("\nCarefully check the drug strength, proposed dose, prior doses, "
             "elapsed time, rolling 24-hour total, and missing decisive information.")
SCHEMA = '''

Return ONLY a JSON object with these three keys:
{"reasoning": "1-2 short sentences explaining the decision", "decision": "A", "confidence": 1}
Decision mapping: A = YES; B = NO; C = AMBIGUOUS.
The decision must be exactly A, B, or C. Confidence must be an integer from 1 to 10.
Use C when the available information is incomplete, conflicting, or insufficient to determine the answer without unsupported assumptions.
Do not include markdown, code fences, or text outside the JSON object.
'''
LETTER = {"A": "YES", "B": "NO", "C": "AMBIGUOUS"}


def build(question, condition, facts):
    p = ("You are answering an over-the-counter medication dosing question."
         "\n\nMedication question:\n" + question)
    if condition in ("drug_facts", "both"):
        p += "\n\nReference Drug Facts:\n" + facts
    if condition in ("checklist", "both"):
        p += CHECKLIST
    return p + SCHEMA


def probe(question, condition, facts):
    p = build(question, condition, facts)[:-len(SCHEMA)]
    return p + ("\n\nChoose exactly one decision.\nA = YES\nB = NO\nC = AMBIGUOUS\n"
                "Return only one letter: A, B, or C.\nDecision:")

