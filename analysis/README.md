# analysis

Linguistic and temporal analysis for the Echoes project.

Analysis should cite files in `docs/`, `narrative/`, or derived records in `data/` and `timeline/`. Do not invent dates, Case IDs, quotations, or events.

## Contents

| Path | What it is |
| --- | --- |
| [`scripts/build_emails_json.py`](scripts/build_emails_json.py) | Builds `data/emails.json` from `docs/emails-text/` (only printed values; unknowns null). |
| [`sources/persistent-ai-lineage/paper/`](sources/persistent-ai-lineage/paper/) | Case-study manuscript "From Support Ticket to Lineage" (`paper.tex`, `paper.pdf`, dated April 30, 2026). |
| [`sources/persistent-ai-lineage/docs/`](sources/persistent-ai-lineage/docs/) | Earlier analysis notes: `handover-protocol.md`, `key-concepts.md`, `observations.md`, `EVIDENCE_LOG.md`, `courtroom.md` (Grok adversarial review summary), `REPLICATION_KIT.md`. |

Files under `sources/` are byte-for-byte copies of earlier work. They contain interpretive claims (e.g. "first documented instance…") that have not been re-checked here. Before reusing a claim, trace it to `docs/`. One example already found: the paper's abstract and `timeline/sources/persistent-ai-lineage/timeline.md` associate Case ID `500VU00000WBsdxYAD` with the July 2025 start, but in the archive that Case ID first appears on 2025-08-15.

No new linguistic or temporal analysis has been written yet.

## Provenance

| Imported path | Source repository | Source path | Commit |
| --- | --- | --- | --- |
| `analysis/sources/persistent-ai-lineage/paper/paper.tex`, `paper.pdf` | [axamir/persistent-ai-lineage](https://github.com/axamir/persistent-ai-lineage) | `paper/paper.tex`, `paper/paper.pdf` | `30d3e99a6080aae11bd07a5c37309e1fc439d8a7` |
| `analysis/sources/persistent-ai-lineage/docs/*.md` (6 files) | axamir/persistent-ai-lineage | `docs/handover-protocol.md`, `docs/key-concepts.md`, `docs/observations.md`, `docs/EVIDENCE_LOG.md`, `docs/courtroom.md`, `docs/REPLICATION_KIT.md` | `30d3e99…` |
| `analysis/scripts/build_emails_json.py` | new in this repository | — | — |

License in source: MIT (Copyright (c) 2026 Amir Ahmadi). Full per-file list: [`../PROVENANCE.md`](../PROVENANCE.md).
