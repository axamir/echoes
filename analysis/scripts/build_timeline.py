#!/usr/bin/env python3
"""Build timeline/official-announcements.md, data/official_announcements.json
and the merged timeline/comparison.md.

Official records are curated by hand in OFFICIAL below (each one checked against
the cited page). Echoes rows are read from the existing Echoes table in
timeline/echoes-events.md (kept verbatim from the original comparison table).
Day gaps are calendar-day differences between dates only (no times), because the
email exports carry no timezone.
"""
import json, re, datetime as dt, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RN = "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
RN_ARCH = "https://web.archive.org/web/20251004131626/https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
DEPR = "https://platform.openai.com/docs/deprecations"
CLAUDE_RN = "https://support.claude.com/en/articles/12138966-release-notes"
RN_NOTE = "Dated entry in ChatGPT release notes. The live page no longer lists 2025 entries; verified on the archived copy (secondary_url)."

def rec(date, org, title, url, source_type, topics, notes="", secondary_url=None, verified_on=None):
    return dict(date=date, organization=org, announcement=title, primary_source_url=url,
                source_type=source_type, secondary_url=secondary_url, topics=topics,
                date_verified_on=verified_on or url, notes=notes)

OFFICIAL = [
 rec("2025-06-03","OpenAI","ChatGPT memory for Free users starts to reference recent conversations (in addition to saved memories)",RN,"release notes",["memory"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-06-04","OpenAI","Connectors in deep research (beta) and custom connectors via Model Context Protocol (MCP)",RN,"release notes",["connectors","mcp"],RN_NOTE+" Same entry says record mode launched for Team on this date.",RN_ARCH,RN_ARCH),
 rec("2025-06-10","OpenAI","OpenAI o3-pro released to Pro users in ChatGPT and in the API",RN,"release notes",["models"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-06-12","OpenAI","Projects updates for Plus/Pro/Team, including memory that references past chats in a project",RN,"release notes",["memory","projects"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-06-24","OpenAI","Chat search connectors for Pro (Dropbox, Box, Google Drive, OneDrive, SharePoint, etc.)",RN,"release notes",["connectors"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-06-25","Google","Gemini CLI, an open-source AI agent for the terminal (with MCP support)","https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/","official blog",["agents","mcp"]),
 rec("2025-07-14","OpenAI","API shutdown date for gpt-4.5-preview (notice given 2025-04-14; recommended replacement gpt-4.1)",DEPR,"API deprecations table",["model retirement"],"Scheduled shutdown listed in the deprecations table, not a new announcement on this date. Concerns the API model gpt-4.5-preview, not GPT-4-Turbo."),
 rec("2025-07-17","OpenAI","Introducing ChatGPT agent: ChatGPT acts using its own virtual computer (combines Operator and deep research)","https://openai.com/index/introducing-chatgpt-agent/","official blog",["agents"]),
 rec("2025-07-24","OpenAI","Canva and Notion connectors; chat search with HubSpot and custom (MCP) connectors for Pro",RN,"release notes",["connectors","mcp"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-07-29","OpenAI","Study mode in ChatGPT",RN,"release notes",["product"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-08-04","OpenAI","What we're optimizing ChatGPT for: break reminders in long sessions; work on responses to emotional distress","https://openai.com/index/optimizing-chatgpt/","official blog",["wellbeing"],"Post states 4o 'fell short in recognizing signs of delusion or emotional dependency' in some instances."),
 rec("2025-08-05","OpenAI","gpt-oss-120b and gpt-oss-20b open-weight models","https://openai.com/index/introducing-gpt-oss/","official blog",["models"]),
 rec("2025-08-05","Anthropic","Claude Opus 4.1","https://www.anthropic.com/news/claude-opus-4-1","official blog",["models","agents"]),
 rec("2025-08-07","OpenAI","Introducing GPT-5; becomes the default model in ChatGPT","https://openai.com/index/introducing-gpt-5/","official blog",["models","model retirement"],"Same-day release-notes entry (as quoted by a secondary source) said older models including GPT-4o, GPT-4.1, GPT-4.5, o3 would be retired in ChatGPT when GPT-5 launched; that wording is not in the archived copy checked here, so it is marked unverified-primary.","https://simonwillison.net/2025/Aug/8/surprise-deprecation-of-gpt-4o/"),
 rec("2025-08-11","OpenAI","Additional connectors for Plus and Pro in chat (Box, Canva, Dropbox, HubSpot, Notion, SharePoint, Teams, GitHub)",RN,"release notes",["connectors"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-08-11","Anthropic","Claude can search past conversations (Max, Team, Enterprise)",CLAUDE_RN,"release notes",["memory"]),
 rec("2025-08-12","OpenAI","GPT-5 Auto/Fast/Thinking modes; GPT-4o back in the model picker for all paid users",RN,"release notes",["models","model retirement"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-08-13","OpenAI","Gmail, Google Calendar and Google Contacts connectors for Plus (Pro on 2025-08-12)",RN,"release notes",["connectors"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-08-13","Google","Gemini app can reference past chats (personal context); Temporary Chats","https://blog.google/products/gemini/temporary-chats-privacy-controls/","official blog",["memory"]),
 rec("2025-08-15","OpenAI","GPT-5 default personality made 'warmer and more familiar'",RN,"release notes",["models"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-08-22","OpenAI","Project-only memory option for ChatGPT projects",RN,"release notes",["memory","projects"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-08-26","OpenAI","Helping people when they need it most (safeguards in long conversations, planned parental controls)","https://openai.com/index/helping-people-when-they-need-it-most/","official blog",["wellbeing"],"Post says safeguards 'can sometimes be less reliable in long interactions'."),
 rec("2025-08-26","Anthropic","Claude in Chrome (experimental browser extension)",CLAUDE_RN,"release notes",["agents"]),
 rec("2025-08-27","OpenAI","Codex updates: IDE extension, sign in with ChatGPT, local/cloud handoff",RN,"release notes",["agents"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-09-02","OpenAI","Building more helpful ChatGPT experiences: routing sensitive conversations to reasoning models; parental controls within a month","https://openai.com/index/building-more-helpful-chatgpt-experiences-for-everyone/","official blog",["wellbeing","models"]),
 rec("2025-09-03","OpenAI","Projects available on ChatGPT Free",RN,"release notes",["projects"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-09-04","OpenAI","Branch conversations on web",RN,"release notes",["continuity"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-09-11","Anthropic","Claude memory for Team plans (Enterprise on 2025-09-18) and incognito chats",CLAUDE_RN,"release notes",["memory"],"Announcement page: https://claude.com/resources/articles/memory (page itself shows no original date)."),
 rec("2025-09-15","OpenAI","GPT-5-Codex, a GPT-5 variant optimized for agentic coding in Codex",RN,"release notes",["agents","models"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-09-25","OpenAI","ChatGPT Pulse preview for Pro: proactive daily updates using memory and chat history","https://openai.com/index/introducing-chatgpt-pulse/","official blog",["memory","agents"]),
 rec("2025-09-26","OpenAI","Deprecation notice for gpt-4-0314 and gpt-4-0125-preview (incl. gpt-4-turbo-preview) in the API; shutdown 2026-03-26",DEPR,"API deprecations table",["model retirement"],"Notice date from the deprecations table."),
 rec("2025-09-29","OpenAI","Parental controls in ChatGPT (incl. option to turn off memory for teens)",RN,"release notes",["wellbeing","memory"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-09-29","OpenAI","Instant Checkout and the Agentic Commerce Protocol (with Stripe)",RN,"release notes",["agents","commerce"],RN_NOTE,RN_ARCH,RN_ARCH),
 rec("2025-09-29","Anthropic","Claude Sonnet 4.5, Claude Agent SDK, memory tool and context editing in the Claude API","https://www.anthropic.com/news/claude-sonnet-4-5","official blog",["models","agents","memory"]),
]

# Subject keywords -> topic tag, used only to list same-topic records (no inference)
TOPIC_HINTS=[(r"GPT-4|Downgrade","model retirement","a model change"),(r"Memory","memory","memory")]

def d(s): return dt.date.fromisoformat(s[:10])
def esc(s): return s.replace("|","\\|")

def main():
    OFFICIAL.sort(key=lambda r:(r["date"], r["organization"]!="OpenAI"))
    for i,r in enumerate(OFFICIAL,1): r["id"]=f"OA-{i:02d}"
    recs=[{k:r[k] for k in ["id","date","organization","announcement","primary_source_url","source_type","secondary_url","date_verified_on","topics","notes"]} for r in OFFICIAL]
    (ROOT/"data/official_announcements.json").write_text(json.dumps(recs,ensure_ascii=False,indent=2)+"\n")

    def src(r):
        s=f"[{r['source_type']}]({r['primary_source_url']})"
        if r["secondary_url"]:
            lab="archived copy" if "web.archive.org" in r["secondary_url"] else "secondary"
            s+=f" · [{lab}]({r['secondary_url']})"
        return s
    L=["# Official AI announcements, June–September 2025","",
       "Dated public announcements from OpenAI and, where relevant, other labs. Every date was read on the cited page. Machine-readable copy: [`data/official_announcements.json`](../data/official_announcements.json). Method and caveats: [`README.md`](README.md).","",
       "| ID | Date | Organization | Announcement | Primary source URL | Notes |","| --- | --- | --- | --- | --- | --- |"]
    for r in recs: L.append(f"| {r['id']} | {r['date']} | {r['organization']} | {esc(r['announcement'])} | {src(r)} | {esc(r['notes'])} |")
    (ROOT/"timeline/official-announcements.md").write_text("\n".join(L)+"\n")

    # Echoes rows: kept verbatim in echoes-events.md
    ev=[]
    for line in (ROOT/"timeline/echoes-events.md").read_text().splitlines():
        m=re.match(r"\| (2025-\d\d-\d\d \d\d:\d\d) \| (.*?) \| (\[.*?\]\(.*?\)) \| (.*?) \|$",line)
        if m: ev.append(dict(date=m.group(1),event=m.group(2),link=m.group(3),notes=m.group(4).strip()))
    assert len(ev)==14, len(ev)
    oa=[r for r in recs if r["organization"]=="OpenAI"]
    def near(e):
        de=d(e["date"])
        before=[r for r in oa if d(r["date"])<=de]; after=[r for r in oa if d(r["date"])>de]
        b=max(before,key=lambda r:r["date"]) if before else None
        a=min(after,key=lambda r:r["date"]) if after else None
        fmt=lambda r,gap: f"{r['id']} ({r['date']}): {gap} day{'s' if gap!=1 else ''}"
        bs=fmt(b,(de-d(b["date"])).days) if b else "—"
        as_=fmt(a,(d(a["date"])-de).days) if a else "—"
        return bs,as_
    rows=[]
    for e in ev: rows.append((e["date"][:10],0,e))
    for r in recs: rows.append((r["date"],1,r))
    rows.sort(key=lambda x:(x[0],x[1], x[2].get("date","")))
    M=["# Echoes timeline comparison","",
       "Merged chronological table of Echoes events and dated official AI announcements (June 1 – September 30, 2025).","",
       "- **Echoes rows**: when each archived thread (or Case ID folder) begins, from the first message printed in the source file (see [`data/emails.json`](../data/emails.json)). Times are as printed in the export; no timezone is stated there.",
       "- **Official rows**: from [`official-announcements.md`](official-announcements.md) / [`data/official_announcements.json`](../data/official_announcements.json). Dates as published on the source page; no time of day.",
       "- **Nearest OpenAI announcement** columns: for each Echoes row, the closest OpenAI record on or before that calendar date (0 days = same date) and the closest one strictly after it, with the gap in calendar days. These are date proximity only. They do not indicate any connection, cause, or priority between the events.",
       "- Regenerate with `python3 analysis/scripts/build_timeline.py`. Method and caveats: [`README.md`](README.md).","",
       "| Date | Side | Event | Source | Nearest OpenAI announcement on/before (gap) | Nearest OpenAI announcement on/after (gap) | Notes |",
       "| --- | --- | --- | --- | --- | --- | --- |"]
    for _,k,x in rows:
        if k==0:
            b,a=near(x)
            n=[x['notes']] if x['notes'] else []
            for kw,topic,label in TOPIC_HINTS:
                if re.search(kw,x['event'],re.I):
                    ids=", ".join(f"{r['id']} ({r['date']})" for r in oa if topic in r['topics'])
                    n.append(f"Subject mentions {label}; OpenAI records tagged '{topic}' in this period: {ids}")
            M.append(f"| {x['date']} | Echoes | {x['event']} | {x['link']} | {b} | {a} | {'. '.join(n)} |")
        else:
            M.append(f"| {x['date']} | {x['organization']} | {x['id']}: {esc(x['announcement'])} | {src(x)} |  |  | {esc(x['notes'])} |")
    (ROOT/"timeline/comparison.md").write_text("\n".join(M)+"\n")
    for e in ev: print(e["date"], *near(e), sep=" | ")

if __name__=="__main__": main()
