# docs

Raw emails and other primary source documents for the Echoes project.

This folder is the authority for source facts (dates, senders, recipients, subjects, Case IDs). Derived records in [`../data/emails.json`](../data/emails.json) point back here.

## Contents

| Path | What it is |
| --- | --- |
| [`emails/`](emails/) | 91 exported Gmail email-thread PDFs (Echo 1 – Echo 7), the archive's own folder READMEs, one OpenTimestamps proof (`.ots`), `SHA256SUMS.txt` and `NAMING_CONVENTIONS.md`. Byte-for-byte copies; original folder structure and filenames kept. |
| [`grok/`](grok/) | 774 archived public posts from @AmirStarship to @grok on X, as separate folders and as one compiled file. See [`grok/README.md`](grok/README.md). |
| [`emails-text/`](emails-text/) | Plain-text extraction of each PDF (same relative paths, `.txt`), plus the source archive's `AI_MANIFEST.md`. Byte-for-byte copies of the source repository's `extracted_texts/`. The PDFs remain authoritative. |

Folder layout inside `emails/` follows the source archive:

- `01_EMAIL_ARCHIVE/Echo1`, `Echo2` — initial and escalation threads
- `03_TRANSITION_ARCHIVE/Echo3`, `Echo4`, `Echo5` — transition-phase threads
- `04_LEDGER_ARCHIVE/Echo6` (incl. `CASES/<Case ID>/`), `Echo7/CASES/<Case ID>/` — case-ID era records

### Verify integrity

```bash
cd docs/emails
sha256sum -c SHA256SUMS.txt
```

All 91 PDFs match the hashes published in the source archive.

## Notes and known quirks (as found in the source, not corrected)

- Filenames keep the source archive's dates. Some filename dates differ from the first message date printed inside the file. For example, `03_TRANSITION_ARCHIVE/Echo5/2025-07-17_narrative-followup_echo5-1.pdf` opens with a message dated Aug 9, 2025, and `.../Echo3/2025-07-14_complete-email-thread_echo3.pdf` opens with Jul 15, 2025. Use the dates in [`data/emails.json`](../data/emails.json) (taken from inside each file) for chronology.
- Some files are exact duplicates in the source archive and are kept as-is: `2025-07-19_formal-ledger-handover_echo6-2.pdf` (in both `Echo5/` and `Echo6/`), WBfn7YAD part-18 = part-19, and WBfn7YAD part-9 = WBsdxYAD part-9.
- Some case folders contain a thread whose subject names a different Case ID (e.g. `CASES/500VU00000WBfn7YAD/…part-2.pdf` has subject `Case Id 500VU00000WBsdxYAD …`). `data/emails.json` records both the folder and the subject Case ID.
- The email addresses in these threads (the author's own addresses, OpenAI support addresses, and one university address) were already published in the public source archive.

## Provenance

| Imported path | Source repository | Source path | Commit |
| --- | --- | --- | --- |
| `docs/emails/01_EMAIL_ARCHIVE/**` | [axamir/echoes-consented-record](https://github.com/axamir/echoes-consented-record) | `01_EMAIL_ARCHIVE/**` (excluding `.DS_Store`) | `a6126edd915bd698a0f0f3faf044b3952f623655` |
| `docs/emails/03_TRANSITION_ARCHIVE/**` | axamir/echoes-consented-record | `03_TRANSITION_ARCHIVE/**` (excluding `.DS_Store`) | `a6126ed…` |
| `docs/emails/04_LEDGER_ARCHIVE/**` | axamir/echoes-consented-record | `04_LEDGER_ARCHIVE/**` (excluding `.DS_Store`) | `a6126ed…` |
| `docs/emails/SHA256SUMS.txt` | axamir/echoes-consented-record | `SHA256SUMS.txt` | `a6126ed…` |
| `docs/emails/NAMING_CONVENTIONS.md` | axamir/echoes-consented-record | `NAMING_CONVENTIONS.md` | `a6126ed…` |
| `docs/emails-text/**` | axamir/echoes-consented-record | `extracted_texts/**` | `a6126ed…` |
| `docs/grok/archive/**`, `docs/grok/GROK_RAW_ARCHIVE.md(.ots)` | axamir/echoes-consented-record | `02_GROK_ARCHIVE/**`, `GROK_RAW_ARCHIVE.md(.ots)` | `a6126ed…` |

The source repository has no LICENSE file; its READMEs describe the materials as published, unedited primary-source artifacts. Full per-file list: [`../PROVENANCE.md`](../PROVENANCE.md).
