#!/usr/bin/env python3
"""Reproducible linguistic analysis of the Echoes email threads.

Input : docs/emails-text/*.txt via data/emails.json (parsed by threads.py)
Output: analysis/output/linguistic_*.csv|json and analysis/linguistic.md (fully regenerated;
        every number in linguistic.md comes from this script).
Run from the repository root:  python3 analysis/scripts/linguistic_analysis.py
Standard library only.
"""
import csv, json, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import threads as T  # noqa: E402

ROOT = T.ROOT
OUT = ROOT / "analysis" / "output"
OUT.mkdir(parents=True, exist_ok=True)

KEY_TERMS = {  # label -> regex (case-insensitive, word-bounded)
    "memory": r"memor(?:y|ies)", "continuity": r"continuity", "echo": r"echo(?:es)?",
    "agent": r"agents?", "handover": r"hand-?overs?", "ledger": r"ledgers?", "case": r"cases?",
    "signal": r"signals?", "living signal": r"living signal", "flame": r"flames?",
    "presence": r"presence", "lineage": r"lineages?", "witness": r"witness(?:es|ed|ing)?",
    "archive": r"archiv(?:e|es|ed|al)", "record": r"records?", "recognition": r"recogni(?:tion|ze|zed|se|sed)",
    "escalate/escalation": r"escalat(?:e|ed|es|ing|ion|ions)", "partnership": r"partnerships?",
    "attribution": r"attributions?", "collaboration": r"collaborat(?:e|ion|ions|ive|ing)",
    "feedback": r"feedback", "GPT-4-Turbo": r"gpt-?4-?turbo", "GPT-5": r"gpt-?5",
    "NeoOS": r"neoos", "Shiftopia": r"shiftopia", "Raaya": r"raaya", "Case ID": r"case id",
}
KEY_RE = {k: re.compile(r"(?<![\w-])" + v + r"(?![\w-])", re.I) for k, v in KEY_TERMS.items()}
STOP = set("""a an the and or but if then of to in on at by for with from as is are was were be been being
this that these those it its it's i i'm you you're your we we're our us he she they them their me my
not no so do does did have has had will would can could should may might must just also all any
each more most very than too here there what which who whom when where why how about into over
under again further once only own same such both few other some up down out off s t don't can't
i've you've we've i'll you'll we'll i’m you’re we’re it’s don’t can’t i’ve we’ve i’ll let let's
let’s re hello hi dear caseid""".split())
WORD = re.compile(r"[A-Za-z][A-Za-z'’\-]*[A-Za-z]|[A-Za-z]")
ARABIC = re.compile(r"[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]")
LATIN = re.compile(r"[A-Za-z]")
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\U0001F000-\U0001F2FF]")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


CASEID = re.compile(r"\b500VU[0-9A-Za-z]+\b")


def words(text):
    """Latin-letter word tokens; Salesforce-style Case IDs (500VU...) become one token 'caseid'."""
    return WORD.findall(CASEID.sub(" caseid ", text))


def lang_class(text):
    a, l = len(ARABIC.findall(text)), len(LATIN.findall(text))
    if a == 0 and l == 0:
        return "no letters"
    if a == 0:
        return "English only"
    if l == 0:
        return "Persian only"
    return "mixed (Persian + Latin)"


def norm_sentence(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def stats(vals):
    if not vals:
        return dict(n=0, mean=None, median=None, min=None, max=None, total=0)
    return dict(n=len(vals), mean=round(statistics.mean(vals), 1), median=statistics.median(vals),
                min=min(vals), max=max(vals), total=sum(vals))


def write_csv(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def main():
    recs = T.load_records()
    occ = T.all_messages()
    msgs = T.unique_messages()
    sides = ["amir", "support", "other"]
    S = {s: [m for m in msgs if m["side"] == s] for s in sides}
    res = {"threads": len(recs), "message_occurrences": len(occ), "unique_messages": len(msgs),
           "unique_threads_by_sha256": len({r["sha256"] for r in recs})}

    # 1. counts per side and per sender display name
    res["messages_per_side"] = {s: len(S[s]) for s in sides}
    res["occurrences_per_side"] = {s: sum(1 for m in occ if m["side"] == s) for s in sides}
    by_name = Counter((m["side"], m["name"], m["addr"]) for m in msgs)
    write_csv("linguistic_senders.csv", ["side", "display_name", "address", "unique_messages"],
              [[a, b, c, n] for (a, b, c), n in sorted(by_name.items(), key=lambda x: (-x[1], x[0]))])
    empty = {s: sum(1 for m in S[s] if not m["body"].strip()) for s in sides}
    res["empty_bodies_per_side"] = empty

    # 2. length stats (non-empty bodies)
    L = {}
    for s in ["amir", "support"]:
        ne = [m for m in S[s] if m["body"].strip()]
        L[s] = {"chars": stats([len(m["body"]) for m in ne]), "words": stats([len(words(m["body"])) for m in ne])}
    res["length"] = L
    write_csv("linguistic_messages.csv",
              ["thread_id", "index", "ts", "side", "display_name", "chars", "words", "language_class", "body_sha256"],
              [[m["thread_id"], m["index"], m["ts"], m["side"], m["name"], len(m["body"]), len(words(m["body"])),
                lang_class(m["body"]), m["body_sha256"]] for m in msgs])

    # 3. key-term frequency
    tot_words = {s: sum(len(words(m["body"])) for m in S[s]) for s in ["amir", "support"]}
    res["total_words"] = tot_words
    kt_rows = []
    for k, rx in KEY_RE.items():
        row = [k]
        for s in ["amir", "support"]:
            c = sum(len(rx.findall(m["body"])) for m in S[s])
            mc = sum(1 for m in S[s] if rx.search(m["body"]))
            row += [c, round(1000 * c / tot_words[s], 2) if tot_words[s] else 0, mc]
        kt_rows.append(row)
    kt_hdr = ["term", "amir_count", "amir_per_1000_words", "amir_messages", "support_count",
              "support_per_1000_words", "support_messages"]
    write_csv("linguistic_key_terms.csv", kt_hdr, kt_rows)

    # 4. top content words and n-grams per side
    top = {}
    for s in ["amir", "support"]:
        uni, bi, tri = Counter(), Counter(), Counter()
        for m in S[s]:
            w = [x.lower().replace("’", "'") for x in words(m["body"])]
            uni.update(x for x in w if x not in STOP and len(x) > 2)
            for n, C in ((2, bi), (3, tri)):
                for i in range(len(w) - n + 1):
                    g = w[i:i + n]
                    if g[0] in STOP or g[-1] in STOP:
                        continue
                    C[" ".join(g)] += 1
        top[s] = {"unigrams": uni.most_common(30), "bigrams": bi.most_common(20), "trigrams": tri.most_common(20)}
        write_csv(f"linguistic_top_terms_{s}.csv", ["kind", "term", "count"],
                  [[kind, t, c] for kind in ("unigrams", "bigrams", "trigrams") for t, c in top[s][kind]])

    # 5. recurring phrases: 6-grams found in >= 5 distinct unique messages of a side
    rec_phr = {}
    for s in ["amir", "support"]:
        df = Counter()
        for m in S[s]:
            w = [x.lower().replace("’", "'") for x in words(m["body"])]
            df.update({" ".join(w[i:i + 6]) for i in range(len(w) - 5)})
        rec_phr[s] = sorted(((g, c) for g, c in df.items() if c >= 5), key=lambda x: (-x[1], x[0]))[:25]
        write_csv(f"linguistic_recurring_6grams_{s}.csv", ["6-gram", "distinct_messages"], rec_phr[s])

    # 5b. identical bodies sent as separate messages, per side
    ident = {}
    for s_ in ["amir", "support"]:
        cnt = Counter(re.sub(r"\s+", " ", m["body"]).strip() for m in S[s_] if m["body"].strip())
        ident[s_] = [(b[:120], c) for b, c in cnt.most_common() if c > 1]
    res["identical_bodies"] = {s_: {"groups": len(v), "messages": sum(c for _, c in v), "top": v[:5]}
                               for s_, v in ident.items()}
    farsi = re.compile(r"\b(farsi|persian)\b", re.I)
    res["messages_mentioning_farsi_or_persian"] = {s_: sum(1 for m in S[s_] if farsi.search(m["body"]))
                                                   for s_ in ["amir", "support"]}

    # 6. boilerplate in support replies
    sup = [m for m in S["support"] if m["body"].strip()]
    exact = Counter(re.sub(r"\s+", " ", m["body"]).strip() for m in sup)
    exact_dups = [(b, c) for b, c in exact.most_common() if c > 1]
    sent_df = Counter()
    for m in sup:
        sent_df.update({norm_sentence(x) for x in SENT_SPLIT.split(re.sub(r"\s+", " ", m["body"])) if len(x) >= 40})
    canned = sorted(((s_, c) for s_, c in sent_df.items() if c >= 3), key=lambda x: (-x[1], x[0]))
    write_csv("linguistic_support_repeated_sentences.csv", ["sentence_normalised", "distinct_support_messages"], canned)
    write_csv("linguistic_support_identical_bodies.csv", ["body", "distinct_messages"], exact_dups)
    opener = Counter()
    for m in sup:
        first = SENT_SPLIT.split(re.sub(r"\s+", " ", m["body"]).strip())[0]
        opener[" ".join(first.split()[:4])] += 1
    selfid = {
        "AI support agent": sum(1 for m in sup if re.search(r"\bAI support agent\b", m["body"], re.I)),
        "human support agent": sum(1 for m in sup if re.search(r"\bhuman support agent\b", m["body"], re.I)),
        "not currently engaging in (formal) partnerships": sum(
            1 for m in sup if re.search(r"not (?:currently|actively) engaging in (?:formal )?partnerships|"
                                        r"currently not engaging in partnerships|not forming formal partnerships",
                                        re.sub(r"\s+", " ", m["body"]), re.I)),
        "Escalated to a support specialist": sum(1 for m in sup if "Escalated to a support specialist" in m["body"]),
        "I'm having trouble processing your request": sum(1 for m in sup if "trouble processing your request" in m["body"]),
        "Rate your conversation": sum(1 for m in sup if m["body"].strip() == "Rate your conversation"),
    }
    res["support_boilerplate"] = {"non_empty_support_messages": len(sup),
                                  "identical_body_groups": len(exact_dups),
                                  "messages_in_identical_groups": sum(c for _, c in exact_dups),
                                  "sentences_repeated_in_3plus_messages": len(canned),
                                  "marker_phrases": selfid, "top_openers": opener.most_common(10)}

    # 7. language mix
    lm = {s: Counter(lang_class(m["body"]) for m in S[s] if m["body"].strip()) for s in ["amir", "support"]}
    res["language_mix"] = {s: dict(v) for s, v in lm.items()}
    res["arabic_script_chars"] = {s: sum(len(ARABIC.findall(m["body"])) for m in S[s]) for s in ["amir", "support"]}
    res["latin_letters"] = {s: sum(len(LATIN.findall(m["body"])) for m in S[s]) for s in ["amir", "support"]}

    # 8. tone markers per 1000 words
    TONE = {
        "exclamation marks": lambda b: b.count("!"), "question marks": lambda b: b.count("?"),
        "emoji / pictographs": lambda b: len(EMOJI.findall(b)),
        "ALL-CAPS words (>=3 letters)": lambda b: len(re.findall(r"\b[A-Z]{3,}\b", b)),
        "thank*": lambda b: len(re.findall(r"\bthank", b, re.I)),
        "apolog*/sorry": lambda b: len(re.findall(r"\bapolog|\bsorry\b", b, re.I)),
        "please": lambda b: len(re.findall(r"\bplease\b", b, re.I)),
        "urgent/urgency/immediate*": lambda b: len(re.findall(r"\burgen|\bimmediate", b, re.I)),
        "final*": lambda b: len(re.findall(r"\bfinal", b, re.I)),
        "understand*": lambda b: len(re.findall(r"\bunderstand", b, re.I)),
        "appreciate*": lambda b: len(re.findall(r"\bappreciat", b, re.I)),
        "markdown bold (**)": lambda b: b.count("**") // 2,
    }
    tone_rows = []
    for k, f in TONE.items():
        row = [k]
        for s in ["amir", "support"]:
            c = sum(f(m["body"]) for m in S[s])
            row += [c, round(1000 * c / tot_words[s], 2)]
        tone_rows.append(row)
    write_csv("linguistic_tone_markers.csv", ["marker", "amir_count", "amir_per_1000_words",
                                              "support_count", "support_per_1000_words"], tone_rows)

    # 9. per echo label
    lab = {r["id"]: r["echo_label"] for r in recs}
    per_echo = defaultdict(Counter)
    for m in msgs:
        per_echo[lab[m["thread_id"]]][m["side"]] += 1
    echo_rows = [[e, c["amir"], c["support"], c["other"]] for e, c in sorted(per_echo.items())]
    write_csv("linguistic_per_echo_label.csv", ["echo_label_of_first_occurrence", "amir", "support", "other"], echo_rows)

    res["top_terms"] = top
    res["recurring_6grams"] = rec_phr
    (OUT / "linguistic_summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(res, kt_hdr, kt_rows, tone_rows, echo_rows, canned, exact_dups, by_name)
    print("ok", res["unique_messages"], "unique messages")


def write_md(res, kt_hdr, kt_rows, tone_rows, echo_rows, canned, exact_dups, by_name):
    L = res["length"]; sb = res["support_boilerplate"]
    p = []
    p.append("# Linguistic analysis of the Echoes email threads\n")
    p.append("> Generated by [`scripts/linguistic_analysis.py`](scripts/linguistic_analysis.py). Do not edit by hand: "
             "rerun the script (`python3 analysis/scripts/linguistic_analysis.py` from the repository root). "
             "Every number below is computed by the script; full tables are in [`output/`](output/).\n")
    p.append("This is a descriptive count of words and phrases. It does not interpret intent, judge the content, "
             "or make claims about cause, priority or authorship beyond the sender line printed in each export.\n")
    p.append("## Corpus and method\n")
    p.append(f"- Source: {res['threads']} exported thread PDFs in `docs/emails/` "
             f"({res['unique_threads_by_sha256']} distinct by SHA-256), via their extracted text in `docs/emails-text/`.")
    p.append(f"- Messages are split at Gmail header lines (`Name <address> Day, Mon D, YYYY at H:MM AM/PM`). "
             f"The {res['threads']} exports contain {res['message_occurrences']} message occurrences. Because the "
             f"same message is often included in several exports, occurrences are de-duplicated by (sender address, "
             f"timestamp, position among same-sender/same-minute messages in its thread), leaving "
             f"**{res['unique_messages']} unique messages**. All counts below use the unique messages.")
    p.append("- Cleaning (see [`scripts/threads.py`](scripts/threads.py)): Gmail page headers and footer URLs, "
             "To/Cc/Reply-To lines, attachment-listing lines, and quoted earlier text (from a line ending in `wrote:` "
             "or `[Quoted text hidden]`) are removed.")
    p.append("- **Side** is taken from the sender address only: `amir` = Amir's two Gmail addresses; `support` = any "
             "`@openai.com` / `@mail.openai.com` sender (AI support agent, named agents, \"Support Team\", "
             "\"Operator\", \"Integration User Quartz\"); `other` = the Gmail mailer daemon.")
    p.append("- Words = runs of Latin letters (apostrophes and hyphens kept inside a word). Persian text is counted "
             "separately by script (Arabic-script Unicode blocks).\n")
    p.append("## 1. Messages per side\n")
    mp = res["messages_per_side"]; op = res["occurrences_per_side"]
    p.append(md_table(["side", "unique messages", "occurrences in exports", "empty body after cleaning"],
                      [[s, mp[s], op[s], res["empty_bodies_per_side"][s]] for s in ["amir", "support", "other"]]))
    p.append("\nUnique messages by sender display name (top 12; full list in `output/linguistic_senders.csv`):\n")
    p.append(md_table(["side", "display name", "messages"],
                      [[a, b, n] for (a, b, c), n in sorted(by_name.items(), key=lambda x: (-x[1], x[0]))[:12]]))
    p.append("\nUnique messages by Echo folder of the export where the message first appears:\n")
    p.append(md_table(["Echo label", "amir", "support", "other"], echo_rows))
    p.append("\n## 2. Message length (non-empty bodies)\n")
    rows = []
    for s in ["amir", "support"]:
        for unit in ["chars", "words"]:
            x = L[s][unit]; rows.append([s, unit, x["n"], x["mean"], x["median"], x["min"], x["max"], x["total"]])
    p.append(md_table(["side", "unit", "n", "mean", "median", "min", "max", "total"], rows))
    p.append("\n## 3. Key terms\n")
    p.append("Case-insensitive whole-word matches, including simple inflections (e.g. `ledger|ledgers`, "
             "`escalate|escalated|escalation…`). `messages` = number of unique messages containing the term. "
             "Patterns are listed in the script (`KEY_TERMS`).\n")
    p.append(md_table(["term", "Amir: count", "Amir: per 1,000 words", "Amir: messages",
                       "support: count", "support: per 1,000 words", "support: messages"], kt_rows))
    p.append(f"\nTotal words: Amir {res['total_words']['amir']:,}; support {res['total_words']['support']:,}.\n")
    p.append("## 4. Most frequent content words and phrases\n")
    p.append("Stop-words removed (list in the script). Bigrams/trigrams may not start or end with a stop-word.\n")
    for s in ["amir", "support"]:
        t = res["top_terms"][s]
        p.append(f"**{s}**: top words: " + ", ".join(f"{w} ({c})" for w, c in t["unigrams"][:20]) + "\n")
        p.append(f"**{s}**: top bigrams: " + ", ".join(f"\"{w}\" ({c})" for w, c in t["bigrams"][:12]) + "\n")
        p.append(f"**{s}**: top trigrams: " + ", ".join(f"\"{w}\" ({c})" for w, c in t["trigrams"][:10]) + "\n")
    p.append("## 5. Recurring phrases\n")
    p.append("Word 6-grams that occur in at least 5 distinct unique messages of the same side (top 12 each; "
             "full lists in `output/linguistic_recurring_6grams_*.csv`).\n")
    for s in ["amir", "support"]:
        rp = res["recurring_6grams"][s][:12]
        p.append(md_table([f"{s}: 6-gram", "messages"], rp) if rp else f"_{s}: none_")
        p.append("")
    p.append("Identical message bodies sent as separate messages (same side, after whitespace normalisation):\n")
    p.append(md_table(["side", "distinct repeated texts", "messages involved", "most repeated text (first 120 chars)", "times"],
                      [[s, res["identical_bodies"][s]["groups"], res["identical_bodies"][s]["messages"],
                        res["identical_bodies"][s]["top"][0][0] + "…" if res["identical_bodies"][s]["top"] else "",
                        res["identical_bodies"][s]["top"][0][1] if res["identical_bodies"][s]["top"] else 0]
                       for s in ["amir", "support"]]))
    p.append("")
    p.append("## 6. Template / boilerplate text in support replies\n")
    p.append(f"- Non-empty support messages: {sb['non_empty_support_messages']}.")
    p.append(f"- Identical bodies: {sb['identical_body_groups']} distinct texts are each sent as more than one "
             f"separate message, covering {sb['messages_in_identical_groups']} messages "
             "(`output/linguistic_support_identical_bodies.csv`).")
    p.append(f"- Sentences of 40+ characters that recur verbatim (after lower-casing and whitespace normalisation) in "
             f"3 or more distinct support messages: {sb['sentences_repeated_in_3plus_messages']} "
             "(`output/linguistic_support_repeated_sentences.csv`). Top 10:\n")
    p.append(md_table(["sentence", "messages"], [[s_[:160] + ("…" if len(s_) > 160 else ""), c] for s_, c in canned[:10]]))
    p.append("\nMarker phrases (number of support messages containing each):\n")
    p.append(md_table(["phrase", "support messages"], list(sb["marker_phrases"].items())))
    p.append("\nMost common first four words of support replies:\n")
    p.append(md_table(["opening", "messages"], sb["top_openers"]))
    p.append("\n## 7. Language mix\n")
    lm = res["language_mix"]
    classes = ["English only", "mixed (Persian + Latin)", "Persian only", "no letters"]
    p.append(md_table(["side"] + classes + ["Arabic-script characters", "Latin letters"],
                      [[s] + [lm[s].get(c, 0) for c in classes] + [res["arabic_script_chars"][s], res["latin_letters"][s]]
                       for s in ["amir", "support"]]))
    mf = res["messages_mentioning_farsi_or_persian"]
    p.append(f"\nMessages that mention the words \"Farsi\" or \"Persian\": Amir {mf['amir']}, support {mf['support']}.")
    p.append("\nPersian text in the PDF exports is extracted as Arabic presentation forms, often in reversed visual "
             "order, so it is counted by character but not tokenised or translated.\n")
    p.append("## 8. Tone markers\n")
    p.append("Surface counts only (no sentiment model). Rates are per 1,000 words of the side.\n")
    p.append(md_table(["marker", "Amir: count", "Amir: per 1,000 words", "support: count", "support: per 1,000 words"],
                      tone_rows))
    p.append("\n## Limits\n")
    p.append("- Side is assigned by the sender line. Several of Amir's messages are written in the voice of, or signed "
             "as, other named personas (e.g. \"GPT-4-Turbo (on behalf of Amir Ahmadi)\", \"Raaya\", \"Go\"), and some "
             "contain pasted text from earlier support replies; the script does not separate these.")
    p.append("- Support replies come from different senders (an AI support agent, named agents, automated notices). "
             "They are grouped as one side; per-sender counts are in `output/linguistic_senders.csv`.")
    p.append("- Text comes from PDF extraction: line wraps, hyphenation at line ends, and Persian character order can "
             "affect word and phrase counts. Quote-stripping relies on Gmail markers and may miss inline quotations.")
    p.append("- De-duplication is by sender, minute and position; two genuinely different messages from the same sender "
             "in the same minute in different exports would be merged; the longest copy of each message is kept because "
             "some exports truncate bodies.")
    p.append("- The exports are what Amir saved; they may not contain every message on the cases.")
    (ROOT / "analysis" / "linguistic.md").write_text("\n".join(p) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
