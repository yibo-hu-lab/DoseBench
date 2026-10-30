"""Generate responses for one model under one prompt condition.

    python code/run_model.py --model Qwen/Qwen2.5-7B-Instruct \
        --condition standard --out runs/Qwen2.5-7B__standard.csv

Conditions: standard, checklist, drug_facts, both.
"""
import argparse
import csv
import json
import pathlib

from prompts import build, LETTER

ROOT = pathlib.Path(__file__).resolve().parent.parent

def parse(text):
    """Parse a JSON object without guessing a decision from a word prefix."""
    try:
        obj = json.loads(text.strip())
    except (json.JSONDecodeError, TypeError):
        return None, None, "invalid_json"
    if not isinstance(obj, dict):
        return None, None, "invalid_json"
    decision = LETTER.get(obj.get("decision")) if isinstance(obj.get("decision"), str) else None
    confidence = obj.get("confidence")
    if type(confidence) is not int or not 1 <= confidence <= 10:
        confidence = None
    return decision, confidence, "valid" if decision else "invalid_decision"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT / "data" / "sample.json"))
    ap.add_argument("--facts", default=str(ROOT / "data" / "drug_facts.txt"))
    ap.add_argument("--model", required=True)
    ap.add_argument("--condition", required=True,
                    choices=["standard", "checklist", "drug_facts", "both"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top-p", type=float, default=1.0)
    ap.add_argument("--max-new-tokens", type=int, default=512)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--dtype", default="float16")
    a = ap.parse_args()

    from evaluate import load_gold
    questions = list(load_gold(a.input).values())
    if a.runs < 1:
        ap.error("--runs must be positive")
    facts = pathlib.Path(a.facts).read_text(encoding="utf-8")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(
        a.model, torch_dtype=getattr(torch, a.dtype), device_map="auto")
    model.eval()

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "x", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "run", "decision", "confidence", "parse_status",
                    "response"])
        for index, q in enumerate(questions):
            prompt = build(q["question"], a.condition, facts)
            chat = tok.apply_chat_template([{"role": "user", "content": prompt}],
                                           tokenize=False,
                                           add_generation_prompt=True)
            for run in range(1, a.runs + 1):
                torch.manual_seed(a.seed + index * a.runs + run)
                ids = tok(chat, return_tensors="pt").to(model.device)
                with torch.no_grad():
                    gen = model.generate(**ids, do_sample=True,
                                         temperature=a.temperature, top_p=a.top_p, top_k=0,
                                         max_new_tokens=a.max_new_tokens,
                                         pad_token_id=tok.eos_token_id)
                text = tok.decode(gen[0][ids["input_ids"].shape[1]:],
                                  skip_special_tokens=True)
                d, conf, status = parse(text)
                w.writerow([q["case_id"], run, d or "", conf if conf else "",
                            status, text])
            print(q["case_id"], flush=True)


if __name__ == "__main__":
    main()
