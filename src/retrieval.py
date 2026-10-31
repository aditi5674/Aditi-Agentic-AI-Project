import math
import re
from pathlib import Path
from . import config

TOKEN_RE = re.compile(r"[a-z0-9]+", re.I)


def _tokens(text):
    return TOKEN_RE.findall(text.lower())


def _chunks():
    path = Path(config.DATA_DIR) / "student_handbook.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    sections, heading, body = [], "General", []
    for line in text.splitlines():
        if line.startswith("## "):
            if body:
                sections.append((heading, "\n".join(body).strip()))
            heading, body = line[3:].strip(), []
        elif line.strip() and not line.startswith("# "):
            body.append(line.strip())
    if body:
        sections.append((heading, "\n".join(body).strip()))
    return sections


def retrieve(query: str, limit: int = 3):
    docs = _chunks()
    if not docs:
        return []
    q = _tokens(query)
    tokenized = [_tokens(h + " " + body) for h, body in docs]
    avgdl = sum(map(len, tokenized)) / max(len(tokenized), 1)
    scores = []
    for idx, ((heading, body), terms) in enumerate(zip(docs, tokenized)):
        score = 0.0
        for term in set(q):
            tf = terms.count(term)
            if not tf:
                continue
            df = sum(1 for doc in tokenized if term in doc)
            idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
            k1, b = 1.5, 0.75
            denom = tf + k1 * (1 - b + b * len(terms) / max(avgdl, 1))
            score += idf * tf * (k1 + 1) / denom
        if score > 0:
            scores.append((score, heading, body))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [{"heading": h, "text": body, "score": round(s, 3)} for s, h, body in scores[:limit]]
