"""Automatic scoring against the locked A5 ground truth. No hand ranking.
- node/chunk is relevant if its text contains any one required fact (regex below)
- answer is correct if it contains every required fact group; Q9/Q10 are correct if it declines."""
import re
FACT = {  # any one match makes a retrieved passage relevant
 "Q1": r"88 percent|95 percent",
 "Q2": r"Success criteria",
 "Q3": r"83\.8|0\.239",
 "Q4": r"\b138\b|\b865\b",
 "Q5": r"25,300|\$105|89 ?%|89 percent",
 "Q6": r"deterministic engine|intelligent operator",
 "Q7": r"own what is durable|partner to learn",
 "Q8": r"measured win|Level 1",
}
ANS = {  # every group must match (case-insensitive)
 "Q1": [r"88", r"95"],
 "Q2": [r"persona", r"task", r"context", r"example", r"rules", r"success criteria", r"steps"],
 "Q3": [r"83\.8", r"0\.239"],
 "Q4": [r"138", r"865"],
 "Q5": [r"\$?105\b", r"25,300", r"89"],
 "Q6": [r"deterministic", r"operator|instructions"],
 "Q7": [r"partner", r"own what is durable|rent what is common|durable and specific"],
 "Q8": [r"measured win|before-and-after|before and after", r"level 1|proven"],
}
DECLINE = r"do not have enough information|does not (?:specify|state|provide|name|list|give|recommend)|do not (?:specify|state)|not (?:specified|stated|named|listed)|no (?:specific )?(?:size|recommendation)|does not mention"
def relevant(qid, text):
    return qid in FACT and re.search(FACT[qid], text, re.I) is not None
def correct(qid, answer):
    if qid in ("Q9", "Q10"):
        return re.search(DECLINE, answer, re.I) is not None
    return all(re.search(g, answer, re.I) for g in ANS[qid])
def retrieval(qid, texts):
    """texts in rank order -> dict(recall, precision, first, rr)"""
    marks = [relevant(qid, t) for t in texts]
    first = next((i + 1 for i, m in enumerate(marks) if m), None)
    return dict(marks="".join("Y" if m else "N" for m in marks), recall=any(marks),
                precision=sum(marks) / len(marks) if marks else 0.0, first=first, rr=1 / first if first else 0.0)
