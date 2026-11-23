#!/usr/bin/env python3
"""Build data/emails.json from docs/emails-text/*.txt (one record per archived thread PDF).

Only values literally printed in the extracted text (or encoded in the archive's own
folder path) are recorded. Anything not found is left null. Nothing is inferred.
Run from the repository root:  python3 analysis/scripts/build_emails_json.py
"""
import json, re, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TXT = ROOT / "docs" / "emails-text"
PDF = ROOT / "docs" / "emails"
MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
HDR = re.compile(r"^(?P<sender>.+?<[^>]+>) (?P<raw>(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), "
                 r"(?P<mon>[A-Z][a-z]{2}) (?P<d>\d{1,2}), (?P<y>\d{4}) at (?P<h>\d{1,2}):(?P<mi>\d{2}) (?P<ap>[AP]M))$")
CASE = re.compile(r"\b(500VU[0-9A-Za-z]{10,13})\b")


def split_addrs(s):
    out, cur, q = [], "", False
    for ch in s:
        if ch == '"':
            q = not q
        if ch == "," and not q:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def parse(txt_path):
    lines = txt_path.read_text(encoding="utf-8").splitlines()
    rel = txt_path.relative_to(TXT).with_suffix(".pdf")
    pdf = PDF / rel
    rec = {
        "id": rel.with_suffix("").as_posix(),
        "date": None, "date_raw": None, "sender": None, "recipients": None,
        "subject": None, "case_id": None, "archive_case_folder": None,
        "echo_label": None, "message_count": None,
        "source_file": ("docs/emails/" + rel.as_posix()),
        "text_file": ("docs/emails-text/" + txt_path.relative_to(TXT).as_posix()),
        "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "summary": None,
    }
    # Subject: lines after the account line, up to the "N messages" line or the first header line.
    i, subj = 2, []
    while i < len(lines) and not re.match(r"^\d+ messages?$", lines[i]) and not HDR.match(lines[i]):
        subj.append(lines[i].strip()); i += 1
    if subj:
        rec["subject"] = " ".join(subj)
    if i < len(lines) and re.match(r"^\d+ messages?$", lines[i]):
        rec["message_count"] = int(lines[i].split()[0]); i += 1
    # First message header + its To: line.
    for j in range(i, min(i + 5, len(lines))):
        m = HDR.match(lines[j])
        if m:
            rec["sender"] = m["sender"]; rec["date_raw"] = m["raw"]
            h = int(m["h"]) % 12 + (12 if m["ap"] == "PM" else 0)
            rec["date"] = f"{m['y']}-{MONTHS[m['mon']]:02d}-{int(m['d']):02d}T{h:02d}:{m['mi']}"
            for k in range(j + 1, min(j + 4, len(lines))):
                if lines[k].startswith("To: "):
                    rec["recipients"] = split_addrs(lines[k][4:]); break
            break
    if rec["subject"]:
        c = CASE.search(rec["subject"])
        if c:
            rec["case_id"] = c.group(1)
    parts = rel.parts
    if "CASES" in parts:
        rec["archive_case_folder"] = parts[parts.index("CASES") + 1]
    e = [p for p in parts if re.fullmatch(r"Echo\d+", p)]
    rec["echo_label"] = e[0] if e else None
    return rec


def main():
    recs = [parse(p) for p in sorted(TXT.rglob("*.txt"))]
    recs.sort(key=lambda r: (r["date"] or "9999", r["id"]))
    (ROOT / "data" / "emails.json").write_text(json.dumps(recs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(recs), "records")


if __name__ == "__main__":
    main()
