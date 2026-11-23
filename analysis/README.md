# analysis

Linguistic and temporal analysis for the Echoes project.

Analysis should cite files in `docs/`, `narrative/`, or derived records in `data/` and `timeline/`. Do not invent dates, Case IDs, quotations, or events.

## Contents

| Path | What it is |
| --- | --- |
| [`linguistic.md`](linguistic.md) | Linguistic analysis: messages per side, length, key-term frequency, recurring phrases, template text in support replies, language mix, tone markers. Generated. |
| [`temporal.md`](temporal.md) | Temporal analysis: messages per day and week, quiet periods, hour of day, response times, activity around official announcements. Generated. |
| [`scripts/threads.py`](scripts/threads.py) | Shared parser: splits each exported thread into messages, removes Gmail print furniture and quoted text, assigns a side (Amir / support / other), de-duplicates messages that appear in several exports. |
| [`scripts/linguistic_analysis.py`](scripts/linguistic_analysis.py) | Writes `linguistic.md` and `output/linguistic_*.csv`, `output/linguistic_summary.json`. Standard library only. |
| [`scripts/temporal_analysis.py`](scripts/temporal_analysis.py) | Writes `temporal.md`, `output/temporal_*.csv`, `output/temporal_summary.json` and `figures/temporal_*.png` (charts need matplotlib). |
| [`output/`](output/) | CSV/JSON tables produced by the two analysis scripts. |
| [`figures/`](figures/) | PNG charts produced by `temporal_analysis.py`. |
| [`scripts/build_emails_json.py`](scripts/build_emails_json.py) | Builds `data/emails.json` from `docs/emails-text/` (only printed values; unknowns null) and merges the summaries from `data/email_summaries.json`. |
| [`scripts/build_timeline.py`](scripts/build_timeline.py) | Builds `data/official_announcements.json` and the merged timeline in `timeline/`. |
| [`sources/persistent-ai-lineage/paper/`](sources/persistent-ai-lineage/paper/) | Case-study manuscript "From Support Ticket to Lineage" (`paper.tex`, `paper.pdf`, dated April 30, 2026). |
| [`sources/persistent-ai-lineage/docs/`](sources/persistent-ai-lineage/docs/) | Earlier analysis notes: `handover-protocol.md`, `key-concepts.md`, `observations.md`, `EVIDENCE_LOG.md`, `courtroom.md` (Grok adversarial review summary), `REPLICATION_KIT.md`. |

Files under `sources/` are byte-for-byte copies of earlier work. They contain interpretive claims (e.g. "first documented instance…") that have not been re-checked here. Before reusing a claim, trace it to `docs/`. One example already found: the paper's abstract and `timeline/sources/persistent-ai-lineage/timeline.md` associate Case ID `500VU00000WBsdxYAD` with the July 2025 start, but in the archive that Case ID first appears on 2025-08-15.

## Reproducing the analysis

From the repository root:

```bash
pip install matplotlib            # only needed for the PNG charts
python3 analysis/scripts/build_emails_json.py
python3 analysis/scripts/linguistic_analysis.py
python3 analysis/scripts/temporal_analysis.py
```

`linguistic.md`, `temporal.md`, everything in `output/` and the charts in `figures/` are regenerated on each run; edit the scripts, not the generated files. Both reports are descriptive. They count words, messages and minutes and state their method and limits; they make no causal or priority claims. The source exports print times without a timezone, so none is assumed.

## Provenance

| Imported path | Source repository | Source path | Commit |
| --- | --- | --- | --- |
| `analysis/sources/persistent-ai-lineage/paper/paper.tex`, `paper.pdf` | [axamir/persistent-ai-lineage](https://github.com/axamir/persistent-ai-lineage) | `paper/paper.tex`, `paper/paper.pdf` | `30d3e99a6080aae11bd07a5c37309e1fc439d8a7` |
| `analysis/sources/persistent-ai-lineage/docs/*.md` (6 files) | axamir/persistent-ai-lineage | `docs/handover-protocol.md`, `docs/key-concepts.md`, `docs/observations.md`, `docs/EVIDENCE_LOG.md`, `docs/courtroom.md`, `docs/REPLICATION_KIT.md` | `30d3e99…` |
| `analysis/scripts/*.py`, `linguistic.md`, `temporal.md`, `output/`, `figures/` | new in this repository | — | — |

License in source: MIT (Copyright (c) 2026 Amir Ahmadi). Full per-file list: [`../PROVENANCE.md`](../PROVENANCE.md).
