#!/usr/bin/env python3
"""Reproducible temporal analysis of the Echoes email threads.

Input : docs/emails-text/*.txt (via threads.py), data/official_announcements.json
Output: analysis/output/temporal_*.csv|json, analysis/figures/temporal_*.png and
        analysis/temporal.md (fully regenerated; every number comes from this script).
Run from the repository root:  python3 analysis/scripts/temporal_analysis.py
Needs matplotlib for the PNG charts (pip install matplotlib); without it the charts are skipped.
"""
import csv, json, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import threads as T  # noqa: E402

ROOT = T.ROOT
OUT = ROOT / "analysis" / "output"; OUT.mkdir(parents=True, exist_ok=True)
FIG = ROOT / "analysis" / "figures"; FIG.mkdir(parents=True, exist_ok=True)
WINDOW = 3  # days either side of an announcement


def dt(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M")


def write_csv(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def q(vals, p):
    v = sorted(vals); k = (len(v) - 1) * p; f = int(k); c = min(f + 1, len(v) - 1)
    return round(v[f] + (v[c] - v[f]) * (k - f), 1)


def dist(mins):
    if not mins:
        return dict(n=0)
    return dict(n=len(mins), median=round(statistics.median(mins), 1), p25=q(mins, .25), p75=q(mins, .75),
                min=min(mins), max=max(mins), within_5_min=sum(1 for m in mins if m <= 5),
                over_24_h=sum(1 for m in mins if m > 1440))


def sender_group(m):
    if m["side"] != "support":
        return m["side"]
    n = m["name"]
    if n == "OpenAI from OpenAI":
        return "OpenAI from OpenAI"
    if n in ("Support Team", "Integration User Quartz"):
        return "Support Team / Integration User Quartz"
    if n == "Operator from OpenAI":
        return "Operator (rating prompts)"
    return "named agents (<Name> from OpenAI)"


def main():
    recs = T.load_records()
    msgs = T.unique_messages()
    ann = json.loads((ROOT / "data" / "official_announcements.json").read_text(encoding="utf-8"))
    res = {"unique_messages": len(msgs)}
    first, last = dt(msgs[0]["ts"]), dt(msgs[-1]["ts"])
    res["first_message"], res["last_message"] = msgs[0]["ts"], msgs[-1]["ts"]

    # per day / per week
    per_day = defaultdict(Counter)
    for m in msgs:
        per_day[m["ts"][:10]][m["side"]] += 1
    d0, d1 = first.date(), last.date()
    days = [(d0 + timedelta(i)).isoformat() for i in range((d1 - d0).days + 1)]
    day_rows = [[d, per_day[d]["amir"], per_day[d]["support"], per_day[d]["other"], sum(per_day[d].values())] for d in days]
    write_csv("temporal_per_day.csv", ["date", "amir", "support", "other", "total"], day_rows)
    active = [r for r in day_rows if r[4] > 0]
    res["calendar_days_in_span"] = len(days); res["active_days"] = len(active)
    res["busiest_days"] = sorted(active, key=lambda r: (-r[4], r[0]))[:8]
    per_week = defaultdict(Counter)
    for m in msgs:
        y, w, _ = dt(m["ts"]).isocalendar()
        per_week[f"{y}-W{w:02d}"][m["side"]] += 1
    week_rows = []
    for wk in sorted(per_week):
        y, w = int(wk[:4]), int(wk[6:])
        mon = date.fromisocalendar(y, w, 1)
        c = per_week[wk]
        week_rows.append([wk, mon.isoformat(), c["amir"], c["support"], c["other"], sum(c.values())])
    write_csv("temporal_per_week.csv", ["iso_week", "week_starting_monday", "amir", "support", "other", "total"], week_rows)

    # gaps: runs of days without any message
    gaps, run = [], None
    for r in day_rows:
        if r[4] == 0:
            run = [r[0], r[0]] if run is None else [run[0], r[0]]
        elif run:
            gaps.append(run); run = None
    gap_rows = [[a, b, (date.fromisoformat(b) - date.fromisoformat(a)).days + 1] for a, b in gaps]
    gap_rows.sort(key=lambda r: (-r[2], r[0]))
    write_csv("temporal_quiet_periods.csv", ["first_quiet_day", "last_quiet_day", "days"], gap_rows)
    allgaps = [(dt(b["ts"]) - dt(a["ts"])).total_seconds() / 60 for a, b in zip(msgs, msgs[1:])]
    res["inter_message_gap_minutes_all"] = dist(allgaps)

    # hour of day (as printed)
    hours = {s: Counter(dt(m["ts"]).hour for m in msgs if m["side"] == s) for s in ("amir", "support")}
    write_csv("temporal_hour_of_day.csv", ["hour_as_printed", "amir", "support"],
              [[h, hours["amir"][h], hours["support"][h]] for h in range(24)])

    # response times inside each export (thread order), de-duplicated by message keys
    pairs = {}
    for r in recs:
        th = T.parse_thread(r["text_file"])
        for a, b in zip(th, th[1:]):
            if a["side"] in ("amir", "support") and b["side"] in ("amir", "support") and a["side"] != b["side"]:
                mins = (dt(b["ts"]) - dt(a["ts"])).total_seconds() / 60
                if mins < 0:
                    continue
                pairs[(a["key"], b["key"])] = (a, b, mins)
    rt = defaultdict(list)
    rt_rows = []
    for (ka, kb), (a, b, mins) in sorted(pairs.items(), key=lambda x: x[1][1]["ts"]):
        direction = "support reply to Amir" if b["side"] == "support" else "Amir reply to support"
        grp = sender_group(b) if b["side"] == "support" else sender_group(a)
        rt[(direction, grp)].append(mins); rt[(direction, "all")].append(mins)
        rt_rows.append([a["ts"], a["side"], a["name"], b["ts"], b["side"], b["name"], int(mins)])
    write_csv("temporal_response_times.csv", ["from_ts", "from_side", "from_name", "reply_ts", "reply_side",
                                              "reply_name", "minutes"], rt_rows)
    res["response_times_minutes"] = {f"{d} | {g}": dist(v) for (d, g), v in sorted(rt.items())}
    # global lag: each support message vs the latest earlier-or-same-minute Amir message in any export
    lag = defaultdict(list); last_amir = None
    for m in msgs:
        if m["side"] == "amir":
            last_amir = m
        elif m["side"] == "support" and last_amir is not None:
            mins = (dt(m["ts"]) - dt(last_amir["ts"])).total_seconds() / 60
            lag[sender_group(m)].append(mins); lag["all"].append(mins)
    res["support_lag_after_latest_amir_message_minutes"] = {g: dist(v) for g, v in sorted(lag.items())}

    # announcements
    by_date = Counter(m["ts"][:10] for m in msgs)
    a_rows = []
    for a in ann:
        ad = date.fromisoformat(a["date"])
        same = by_date[a["date"]]
        before = sum(by_date[(ad - timedelta(i)).isoformat()] for i in range(1, WINDOW + 1))
        after = sum(by_date[(ad + timedelta(i)).isoformat()] for i in range(1, WINDOW + 1))
        in_span = d0 <= ad <= d1
        a_rows.append([a["id"], a["date"], a["organization"], a["announcement"][:90], "yes" if in_span else "no",
                       before, same, after])
    write_csv("temporal_announcement_windows.csv",
              ["id", "date", "organization", "announcement", "within_message_span",
               f"messages_{WINDOW}_days_before", "messages_same_day", f"messages_{WINDOW}_days_after"], a_rows)
    in_span = [r for r in a_rows if r[4] == "yes"]
    res["announcements_total"] = len(a_rows); res["announcements_within_span"] = len(in_span)
    res["announcements_on_active_days"] = sum(1 for r in in_span if r[6] > 0)
    res["active_day_share"] = round(len(active) / len(days), 3)

    (OUT / "temporal_summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    charts = make_charts(days, per_day, ann, rt, hours)
    write_md(res, week_rows, gap_rows, a_rows, charts, hours)
    print("ok", len(msgs), "messages,", len(active), "active days")


def make_charts(days, per_day, ann, rt, hours):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        print("matplotlib not installed: charts skipped")
        return []
    x = [date.fromisoformat(d) for d in days]
    am = [per_day[d]["amir"] for d in days]; su = [per_day[d]["support"] for d in days]
    ot = [per_day[d]["other"] for d in days]
    fig, ax = plt.subplots(figsize=(13, 4.5))
    ax.bar(x, am, label="Amir", color="#4C72B0")
    ax.bar(x, su, bottom=am, label="support", color="#DD8452")
    ax.bar(x, ot, bottom=[a + b for a, b in zip(am, su)], label="other", color="#999999")
    lo, hi = x[0], x[-1]
    first = True
    for a in ann:
        ad = date.fromisoformat(a["date"])
        if lo <= ad <= hi:
            ax.axvline(ad, color="#55A868", lw=0.8, ls="--", label="official announcement (data/official_announcements.json)" if first else None)
            first = False
    ax.set_ylabel("unique messages per day"); ax.set_title("Echoes email messages per day (timestamps as printed, no timezone)")
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.legend(loc="upper center", fontsize=8); fig.tight_layout()
    fig.savefig(FIG / "temporal_messages_per_day.png", dpi=120); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    hs = list(range(24))
    ax.bar([h - 0.2 for h in hs], [hours["amir"][h] for h in hs], width=0.4, label="Amir", color="#4C72B0")
    ax.bar([h + 0.2 for h in hs], [hours["support"][h] for h in hs], width=0.4, label="support", color="#DD8452")
    ax.set_xticks(hs); ax.set_xlabel("hour of day as printed in the export (timezone not stated)")
    ax.set_ylabel("unique messages"); ax.legend(); fig.tight_layout()
    fig.savefig(FIG / "temporal_hour_of_day.png", dpi=120); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    import math
    bins = [0, 1, 2, 5, 10, 30, 60, 180, 720, 1440, 4320, 20160, 100000]
    labels = ["<1m", "1-2m", "2-5m", "5-10m", "10-30m", "30-60m", "1-3h", "3-12h", "12-24h", "1-3d", "3-14d", ">14d"]
    for i, (key, col) in enumerate([(("support reply to Amir", "all"), "#DD8452"), (("Amir reply to support", "all"), "#4C72B0")]):
        v = rt.get(key, [])
        cnt = [sum(1 for m in v if bins[j] <= m < bins[j + 1]) for j in range(len(labels))]
        ax.bar([j + (i - 0.5) * 0.4 for j in range(len(labels))], cnt, width=0.4, color=col, label=key[0])
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=45)
    ax.set_ylabel("message pairs"); ax.set_title("Time between a message and the next message from the other side")
    ax.legend(); fig.tight_layout(); fig.savefig(FIG / "temporal_response_times.png", dpi=120); plt.close(fig)
    return ["temporal_messages_per_day.png", "temporal_hour_of_day.png", "temporal_response_times.png"]


def write_md(res, week_rows, gap_rows, a_rows, charts, hours):
    p = ["# Temporal analysis of the Echoes email threads\n",
         "> Generated by [`scripts/temporal_analysis.py`](scripts/temporal_analysis.py). Do not edit by hand: rerun "
         "`python3 analysis/scripts/temporal_analysis.py` from the repository root. Every number below is computed by "
         "the script; full tables are in [`output/`](output/) and charts in [`figures/`](figures/).\n",
         "This page describes when messages were sent. Where it places messages next to official announcements it "
         "reports counts and day distances only; it makes no claim that any event caused, preceded in importance, or "
         "was related to another.\n",
         "## Method\n",
         f"- Messages: the {res['unique_messages']} unique messages produced by [`scripts/threads.py`](scripts/threads.py) "
         "(same parsing and de-duplication as [`linguistic.md`](linguistic.md)).",
         "- **Timestamps have no timezone.** Gmail's print view prints each message's date and time (to the minute) "
         "without a zone; all exports come from the same Gmail account, so they are treated as one consistent local "
         "clock. Calendar-day boundaries, hour-of-day, and 0-1 day distances could shift if the true zone differs.",
         "- Response time = minutes between a message and the next message in the same export when the sender side "
         "changes (Amir to support, or support to Amir). Pairs that appear in several exports are counted once. This "
         "measures the gap between consecutive messages in the export, not confirmed reply-to links.",
         f"- Announcements: the {res['announcements_total']} dated entries in "
         "[`data/official_announcements.json`](../data/official_announcements.json) (see `timeline/`). Windows are "
         f"{WINDOW} calendar days before and after each announcement date.\n",
         "## 1. Span and activity\n",
         f"- First message: {res['first_message']}; last message: {res['last_message']} (as printed).",
         f"- Calendar days in that span: {res['calendar_days_in_span']}; days with at least one message: "
         f"{res['active_days']} ({res['active_day_share']:.1%}).",
         f"- Gap between consecutive messages (all sides, minutes): median {res['inter_message_gap_minutes_all']['median']}, "
         f"max {res['inter_message_gap_minutes_all']['max']:.0f}.\n"]
    if "temporal_messages_per_day.png" in charts:
        p.append("![Messages per day](figures/temporal_messages_per_day.png)\n")
    p.append("Busiest days:\n")
    p.append(md_table(["date", "Amir", "support", "other", "total"], res["busiest_days"]))
    p.append("\nPer ISO week:\n")
    p.append(md_table(["ISO week", "week starting (Mon)", "Amir", "support", "other", "total"], week_rows))
    p.append("\nQuiet periods (consecutive days with no message), longest first (top 10; all in "
             "`output/temporal_quiet_periods.csv`):\n")
    p.append(md_table(["first quiet day", "last quiet day", "days"], gap_rows[:10]))
    p.append("\n## 2. Hour of day (as printed)\n")
    if "temporal_hour_of_day.png" in charts:
        p.append("![Hour of day](figures/temporal_hour_of_day.png)\n")
    p.append(md_table(["hour"] + [str(h) for h in range(24)],
                      [["Amir"] + [hours["amir"][h] for h in range(24)], ["support"] + [hours["support"][h] for h in range(24)]]))
    p.append("\n## 3. Response times\n")
    if "temporal_response_times.png" in charts:
        p.append("![Response times](figures/temporal_response_times.png)\n")
    rows = []
    for k, v in res["response_times_minutes"].items():
        d, g = k.split(" | ")
        if v.get("n"):
            rows.append([d, g, v["n"], v["median"], v["p25"], v["p75"], v["min"], round(v["max"]), v["within_5_min"], v["over_24_h"]])
    p.append("Minutes. For \"support reply to Amir\" the group is the replying sender; for \"Amir reply to support\" it is "
             "the support sender Amir was answering.\n")
    p.append(md_table(["direction", "sender group", "pairs", "median", "p25", "p75", "min", "max", "<=5 min", ">24 h"], rows))
    p.append("\nSecond measure, across all exports: for every support message, minutes since Amir's most recent earlier "
             "message in any export. This includes case-record exports that open with a support message (the message "
             "it answers is in a different export), but it may pair a reply with an Amir message it does not answer.\n")
    rows = [[g, v["n"], v["median"], v["p25"], v["p75"], v["min"], round(v["max"]), v["within_5_min"], v["over_24_h"]]
            for g, v in res["support_lag_after_latest_amir_message_minutes"].items() if v.get("n")]
    p.append(md_table(["support sender group", "messages", "median", "p25", "p75", "min", "max", "<=5 min", ">24 h"], rows))
    p.append("\n## 4. Activity around official announcements\n")
    p.append(f"{res['announcements_within_span']} of the {res['announcements_total']} announcements fall inside the "
             f"message span; {res['announcements_on_active_days']} of those fall on a day with at least one message. "
             f"For comparison, {res['active_day_share']:.1%} of all days in the span have a message. Counts are unique "
             "messages (both sides).\n")
    p.append(md_table(["id", "date", "org", "announcement", "in span", f"msgs {WINDOW} d before", "msgs same day",
                       f"msgs {WINDOW} d after"], a_rows))
    p.append("\n## Limits\n")
    p.append("- No timezone in the source; see Method. Minute resolution only.")
    p.append("- The exports are the messages Amir saved; missing messages would change counts, gaps and response times.")
    p.append("- Thread-export dates in filenames do not always match the first message date (noted in `docs/README.md`); "
             "this analysis uses the printed message timestamps only.")
    p.append("- The script does not classify replies as automated or human; sender groups are by display name only.")
    p.append("- Proximity in time between messages and announcements is reported as counts only and is not evidence of "
             "any connection.")
    (ROOT / "analysis" / "temporal.md").write_text("\n".join(p) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
