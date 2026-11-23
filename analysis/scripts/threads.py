#!/usr/bin/env python3
"""Shared parser: split docs/emails-text/*.txt (Gmail print exports) into messages.

Used by linguistic_analysis.py, temporal_analysis.py and make_digests.py.
Rules (all mechanical, no inference):
- A message starts at a header line "Name <addr> Day, Mon D, YYYY at H:MM AM|PM".
- Gmail print furniture is removed: page header lines ("DD/MM/YYYY, HH:MM Gmail - ...")
  and page-footer URL lines ("https://mail.google.com/...").
- Header lines directly after the message header (To:, Cc:, Reply-To:, Bcc:) are removed.
- Gmail attachment listings are removed: "<file>.pdf 203K" lines, and a "<file>.pdf" line followed
  by a size line ("4K").
- Quoted earlier text is cut: everything from a line ending in "wrote:" (e.g.
  "On Tue, Jul 15, 2025 at 5:26 AM ... wrote:" / "You wrote:") or a "[Quoted text hidden]"
  marker to the end of the message. Lines starting with ">" are kept: in these exports they are
  Markdown block quotes inside the message itself, not Gmail quoting.
- side = "amir" if the sender address is one of Amir's addresses, "support" if the address
  is an @openai.com / @mail.openai.com address, otherwise "other".
- Duplicates: the same message can appear in several exported threads (overlapping case
  exports, copies of the same PDF). Within one thread every header is a separate message.
  Across threads, a message's key is (sender address, timestamp, n), where n counts earlier
  messages in the same thread with the same sender and timestamp. unique_messages() keeps one
  occurrence per key: the one with the longest cleaned body (some exports truncate bodies).
Timestamps carry no timezone in the source (Gmail print view prints local time without zone).
"""
import json, re, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
HDR = re.compile(r"^(?P<name>.+?) <(?P<addr>[^>]+)> (?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), "
                 r"(?P<mon>[A-Z][a-z]{2}) (?P<d>\d{1,2}), (?P<y>\d{4}) at (?P<h>\d{1,2}):(?P<mi>\d{2}) (?P<ap>[AP]M)$")
PAGE_HDR = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2} Gmail - ")
PAGE_URL = re.compile(r"^https://mail\.google\.com/")
META = re.compile(r"^(To|Cc|Bcc|Reply-To): ")
QUOTE_START = re.compile(r"wrote:\s*$")
SIZE = re.compile(r"^\d+(?:\.\d+)?\s?[KM]B?$")
EXT_END = re.compile(r"\.(pdf|png|jpe?g|docx?|txt|md|zip|mp4|mov|csv|json)\s*$", re.I)
ATTACH = re.compile(r"^\S.*\.(pdf|png|jpe?g|docx?|txt|md|zip|mp4|mov)\s+\d+K$", re.I)
AMIR = {"starship.amir@gmail.com", "starship.meta@gmail.com"}


def side_of(addr):
    a = addr.lower()
    if a in AMIR:
        return "amir"
    if a.endswith("@openai.com") or a.endswith(".openai.com"):
        return "support"
    return "other"


def load_records():
    return json.loads((ROOT / "data" / "emails.json").read_text(encoding="utf-8"))


def parse_thread(text_file):
    lines = (ROOT / text_file).read_text(encoding="utf-8").splitlines()
    msgs, cur = [], None
    for ln in lines:
        m = HDR.match(ln)
        if m:
            if cur:
                msgs.append(cur)
            h = int(m["h"]) % 12 + (12 if m["ap"] == "PM" else 0)
            cur = {"name": m["name"], "addr": m["addr"], "side": side_of(m["addr"]),
                   "ts": f"{m['y']}-{MONTHS[m['mon']]:02d}-{int(m['d']):02d}T{h:02d}:{m['mi']}",
                   "raw": [], "in_meta": True, "quoted": False}
            continue
        if cur is None or PAGE_HDR.match(ln) or PAGE_URL.match(ln):
            continue
        if cur["in_meta"] and META.match(ln):
            continue
        cur["in_meta"] = False
        if cur["quoted"]:
            continue
        if QUOTE_START.search(ln) or ln.strip() == "[Quoted text hidden]":
            cur["quoted"] = True
            continue
        if ATTACH.match(ln.strip()):
            continue
        cur["raw"].append(ln)
    if cur:
        msgs.append(cur)
    for c in msgs:  # attachment listings printed as "<file>.pdf" followed by a size line ("4K")
        raw, keep = c["raw"], []
        for j, ln in enumerate(raw):
            if SIZE.match(ln.strip()) and keep and EXT_END.search(keep[-1]):
                keep.pop(); continue
            keep.append(ln)
        c["raw"] = keep
    out, seen = [], {}
    for i, c in enumerate(msgs):
        kk = (c["addr"].lower(), c["ts"]); n = seen.get(kk, 0); seen[kk] = n + 1
        body = "\n".join(c["raw"]).strip()
        norm = re.sub(r"\s+", " ", body).strip()
        out.append({"thread_id": None, "index": i, "name": c["name"], "addr": c["addr"],
                    "side": c["side"], "ts": c["ts"], "body": body,
                    "body_sha256": hashlib.sha256(norm.encode()).hexdigest(),
                    "key": (c["addr"].lower(), c["ts"], n)})
    return out


def all_messages():
    """Every message occurrence, in emails.json order (duplicates included)."""
    res = []
    for r in load_records():
        for m in parse_thread(r["text_file"]):
            m["thread_id"] = r["id"]
            res.append(m)
    return res


def unique_messages():
    best, order = {}, []
    for m in all_messages():
        k = m["key"]
        if k not in best:
            order.append(k); best[k] = m
        elif len(m["body"]) > len(best[k]["body"]):
            best[k] = m
    res = [best[k] for k in order]
    res.sort(key=lambda m: (m["ts"], m["key"]))
    return res
