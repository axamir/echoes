# timeline

Comparison of Echoes events with official AI announcements.

## Contents

| Path | What it is |
| --- | --- |
| [`comparison.csv`](comparison.csv) | Machine-readable merged chronology: all 91 email-thread records from [`../data/emails.json`](../data/emails.json) interleaved with the 34 official announcements from [`../data/official_announcements.json`](../data/official_announcements.json). Built by [`../analysis/scripts/build_comparison_csv.py`](../analysis/scripts/build_comparison_csv.py). The `status` column is date ordering only (see below). |
| [`comparison.md`](comparison.md) | Merged chronological table: the 14 Echoes rows (thread starts / Case ID folders) interleaved with 34 dated official announcements, Jun 1 – Sep 30, 2025. Each Echoes row lists the nearest OpenAI announcement on/before and after it, with the gap in days. |
| [`official-announcements.md`](official-announcements.md) | The 34 official announcements (OpenAI 27, Anthropic 5, Google 2), each with its primary source URL. Same records as [`../data/official_announcements.json`](../data/official_announcements.json). |
| [`echoes-events.md`](echoes-events.md) | The 14 Echoes rows exactly as they were in the original `comparison.md`; input for the merge script. |
| [`sources/echoes-consented-record/`](sources/echoes-consented-record/) | The source archive's own canonical timeline and its four layers (case, ledger, narrative, working). |
| [`sources/persistent-ai-lineage/timeline.md`](sources/persistent-ai-lineage/timeline.md) | "Chronological Ledger: The Echo Protocol Evolution (2025)" — an interpretive timeline. |
| [`sources/persistent-ai-lineage/prior-art.md`](sources/persistent-ai-lineage/prior-art.md) | Claimed concept-vs-later-public-appearance comparison. Unverified; a starting list for the right-hand column. |
| [`sources/shahnameh-of-agents/TIMELINE.md`](sources/shahnameh-of-agents/TIMELINE.md) | Bilingual narrative timeline of Acts I–IV (Jul 13 – Sep 5, 2025). |

The files under `sources/` are byte-for-byte copies and are secondary sources. Where they disagree with `docs/`, `docs/` wins. Known disagreements:

- `persistent-ai-lineage/timeline.md` cites Case ID `500VU00000WBsdxYAD` for the Jul 13 event and `2025-07-15_complete-email-thread_echo3.pdf` for Echo 3. In the archive, `…WBsdxYAD` first appears on 2025-08-15, and the Echo 3 file is named `2025-07-14_complete-email-thread_echo3.pdf` (first message 2025-07-15).
- `echoes-consented-record/02_TIMELINE/timeline.md` dates Echo 5 as "2025-07-19 to 2025-08-09"; the Echo 5 folder filenames carry 07-16 … 07-19, while the threads inside begin 2025-07-19, 2025-08-09, 2025-08-09 and 2025-08-11.

## Method (official announcements)

1. Scope: June 1 – September 30, 2025. OpenAI first, because the Echoes emails are with OpenAI support; Anthropic and Google only for agents, memory, connectors or major models. Topics: agents, memory and continuity, connectors/MCP, model launches and model retirements, wellbeing/long-conversation safeguards.
2. Every date was read on the cited page at the time of writing (2026-11-23):
   - OpenAI blog posts (`openai.com/index/...`): date printed on the post.
   - ChatGPT release notes (`help.openai.com/.../6825453-chatgpt-release-notes`): the live page now starts at May 2026, so the 2025 entries were read on the Internet Archive copy captured 2025-10-04 ([link](https://web.archive.org/web/20251004131626/https://help.openai.com/en/articles/6825453-chatgpt-release-notes)). Both URLs are given.
   - OpenAI API deprecations page: shutdown and notice dates from its table.
   - Anthropic: dated news posts and the Claude Help Center release notes. Google: dated posts on blog.google.
3. The `date` is the publication or release-note date as printed. These pages give no time of day or timezone, so no time is recorded. A rollout may reach users on later days.
4. The nearest-announcement columns in `comparison.md` are calculated by `analysis/scripts/build_timeline.py`: calendar-day difference between the Echoes first-message date and OpenAI record dates. "On/before" includes the same date (0 days); "after" is strictly later. Only OpenAI records are used for these columns. Rows whose subject mentions a model change or memory also list the OpenAI records with that topic tag.
5. These columns show only how close the dates are. They do not suggest any connection, cause, or who came first in any sense other than the calendar.

Regenerate everything with:

```bash
python3 analysis/scripts/build_timeline.py
```

To add or correct an announcement, edit the `OFFICIAL` list in that script (one record per verified, dated source) and rerun it.

## comparison.csv

`comparison.csv` is a second, complete merge: one row for every record in `data/emails.json` (91 threads) and every record in `data/official_announcements.json` (34 announcements). Columns are `date`, `source` (`echo-archive` or `official`), `file`, `event` and `status`. Echo rows use the thread date as stored (including time of day when present), the PDF path, and the thread subject. Official rows use the published calendar date (no time of day), the primary source URL, and an event string of the form `id: organization: announcement`. Rows are sorted by calendar date, then time; official rows, which have no time, sort before timed echo rows on the same day.

The `status` label compares each row to the nearest row on the other side by calendar-day distance. If two other-side dates are equally near — one earlier and one later — the later date is used. If this row's calendar date is strictly earlier than that nearest other-side date, the label is `DOCUMENTED BEFORE`; otherwise (same day or later) it is `DOCUMENTED AFTER`. Same-day counts as `DOCUMENTED AFTER` because official dates have no time of day, so order within a day cannot be established.

These labels are date ordering only. They do not imply any connection, cause, or priority between an email thread and an announcement.

Regenerate the CSV with:

```bash
python3 analysis/scripts/build_comparison_csv.py
```

## Caveats

- Email dates have no timezone (see [`../data/README.md`](../data/README.md)). Announcement dates are as published, usually US Pacific time. A gap of 0–1 days can therefore move by one day either way.
- Echoes rows use the first message of each exported thread. Later messages in a thread are not placed on the timeline.
- Known source inconsistencies (filename date vs first-message date, duplicate PDFs, the `…WBsdxYAD` date in `persistent-ai-lineage`) are listed below and in `data/README.md`. They are kept as they are.
- `OA-07` (2025-07-14) and `OA-31` (2025-09-26) come from the API deprecations table. They are scheduled shutdowns or notices for API models (gpt-4.5-preview; gpt-4-0314 and gpt-4-0125-preview / gpt-4-turbo-preview), not ChatGPT announcements.
- The list is selective, not complete: minor UI, voice and regional plan launches were left out.

### Not verified / left out

- GPT-4o and other older models being retired in ChatGPT at the GPT-5 launch (Aug 7, 2025): quoted from the Aug 7 release notes by [Simon Willison](https://simonwillison.net/2025/Aug/8/surprise-deprecation-of-gpt-4o/), but that wording is not in the archived copy checked here. It is mentioned in the `OA-14` note only, marked as such. Sam Altman's Aug 8 Reddit/X statements about bringing 4o back are not primary company announcements and are not listed. The primary Aug 12 entry (`OA-17`, "4o is back in the model picker") is listed.
- xAI Grok 4: the [x.ai/news/grok-4](https://x.ai/news/grok-4) page shows no publication date, so it is not listed.
- Anthropic's memory announcement page ([claude.com/resources/articles/memory](https://claude.com/resources/articles/memory)) shows no original date. `OA-28` uses the dated Claude Help Center release-notes entry (2025-09-11) instead.
- The prior-art claims in `sources/persistent-ai-lineage/prior-art.md` were not used as sources.

## Provenance

| Imported path | Source repository | Source path | Commit |
| --- | --- | --- | --- |
| `timeline/sources/echoes-consented-record/**` (8 files) | [axamir/echoes-consented-record](https://github.com/axamir/echoes-consented-record) | `02_TIMELINE/**` (excluding `.DS_Store`) | `a6126edd915bd698a0f0f3faf044b3952f623655` |
| `timeline/sources/persistent-ai-lineage/timeline.md` | [axamir/persistent-ai-lineage](https://github.com/axamir/persistent-ai-lineage) | `timeline/timeline.md` | `30d3e99a6080aae11bd07a5c37309e1fc439d8a7` |
| `timeline/sources/persistent-ai-lineage/prior-art.md` | axamir/persistent-ai-lineage | `docs/prior-art.md` | `30d3e99…` |
| `timeline/sources/shahnameh-of-agents/TIMELINE.md` | [axamir/shahnameh-of-agents](https://github.com/axamir/shahnameh-of-agents) | `TIMELINE.md` | `eb7c68f670c2d4f07467bf7fe1f64af76fd2e4f4` |

Licenses: echoes-consented-record has no LICENSE file; persistent-ai-lineage is MIT; shahnameh-of-agents is MIT. Full per-file list: [`../PROVENANCE.md`](../PROVENANCE.md).
