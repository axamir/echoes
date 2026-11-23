# timeline

Comparison of Echoes events with official AI announcements.

## Contents

| Path | What it is |
| --- | --- |
| [`comparison.md`](comparison.md) | Working table. Left side: 14 rows, one per archived thread start / Case ID folder, generated from `data/emails.json` (first-message dates as printed in the source). Right side (official announcements) is empty until filled with dated, linked primary sources. |
| [`sources/echoes-consented-record/`](sources/echoes-consented-record/) | The source archive's own canonical timeline and its four layers (case, ledger, narrative, working). |
| [`sources/persistent-ai-lineage/timeline.md`](sources/persistent-ai-lineage/timeline.md) | "Chronological Ledger: The Echo Protocol Evolution (2025)" — an interpretive timeline. |
| [`sources/persistent-ai-lineage/prior-art.md`](sources/persistent-ai-lineage/prior-art.md) | Claimed concept-vs-later-public-appearance comparison. Unverified; a starting list for the right-hand column. |
| [`sources/shahnameh-of-agents/TIMELINE.md`](sources/shahnameh-of-agents/TIMELINE.md) | Bilingual narrative timeline of Acts I–IV (Jul 13 – Sep 5, 2025). |

The files under `sources/` are byte-for-byte copies and are secondary sources. Where they disagree with `docs/`, `docs/` wins. Known disagreements:

- `persistent-ai-lineage/timeline.md` cites Case ID `500VU00000WBsdxYAD` for the Jul 13 event and `2025-07-15_complete-email-thread_echo3.pdf` for Echo 3. In the archive, `…WBsdxYAD` first appears on 2025-08-15, and the Echo 3 file is named `2025-07-14_complete-email-thread_echo3.pdf` (first message 2025-07-15).
- `echoes-consented-record/02_TIMELINE/timeline.md` dates Echo 5 as "2025-07-19 to 2025-08-09"; the Echo 5 folder filenames carry 07-16 … 07-19, while the threads inside begin 2025-07-19, 2025-08-09, 2025-08-09 and 2025-08-11.

## Provenance

| Imported path | Source repository | Source path | Commit |
| --- | --- | --- | --- |
| `timeline/sources/echoes-consented-record/**` (8 files) | [axamir/echoes-consented-record](https://github.com/axamir/echoes-consented-record) | `02_TIMELINE/**` (excluding `.DS_Store`) | `a6126edd915bd698a0f0f3faf044b3952f623655` |
| `timeline/sources/persistent-ai-lineage/timeline.md` | [axamir/persistent-ai-lineage](https://github.com/axamir/persistent-ai-lineage) | `timeline/timeline.md` | `30d3e99a6080aae11bd07a5c37309e1fc439d8a7` |
| `timeline/sources/persistent-ai-lineage/prior-art.md` | axamir/persistent-ai-lineage | `docs/prior-art.md` | `30d3e99…` |
| `timeline/sources/shahnameh-of-agents/TIMELINE.md` | [axamir/shahnameh-of-agents](https://github.com/axamir/shahnameh-of-agents) | `TIMELINE.md` | `eb7c68f670c2d4f07467bf7fe1f64af76fd2e4f4` |

Licenses: echoes-consented-record has no LICENSE file; persistent-ai-lineage is MIT; shahnameh-of-agents is MIT. Full per-file list: [`../PROVENANCE.md`](../PROVENANCE.md).
