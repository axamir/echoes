# docs/grok — @grok conversation archive

Public posts on X (Twitter) from **@AmirStarship** addressed to **@grok**, as archived in the source repository (extracted June 2, 2026; 774 entries). Every entry begins with an `@grok` mention. Replies from Grok are not stored as separate entries. This is a primary source for the public, X-based part of the Echoes story. Files are byte-for-byte copies; nothing was edited.

## Contents

| Path | What it is |
| --- | --- |
| [`archive/Grok-001/` … `archive/Grok-774/`](archive/) | One folder per entry: `thread.md` (text) and `metadata.json` (`threadId`, `date`, `tweetCount`, `extractedAt`, `source`). |
| [`archive/README.md`](archive/README.md), [`archive/INDEX.md`](archive/INDEX.md) | The source archive's own README and index. |
| [`GROK_RAW_ARCHIVE.md`](GROK_RAW_ARCHIVE.md) | The same 774 entries compiled into one file (`### Tweet 1` … `### Tweet 774`). |
| [`GROK_RAW_ARCHIVE.md.ots`](GROK_RAW_ARCHIVE.md.ots) | OpenTimestamps proof for `GROK_RAW_ARCHIVE.md`, from the source repository. |

## Known quirks (as found in the source, not corrected)

- **No dates.** Every `metadata.json` has `"date": "Unknown"`, so these entries are not in `data/` or `timeline/`.
- **Truncated text in `thread.md`.** In about 555 of the 774 entries, `thread.md` is shorter than the matching `### Tweet N` in `GROK_RAW_ARCHIVE.md`. For example, `Grok-002/thread.md` contains only `@grok Grok,`. Use `GROK_RAW_ARCHIVE.md` for full text.
- **Broken index links.** `archive/README.md` links to `Unknown-001/`… folders that don't exist (the folders are named `Grok-NNN`), and `archive/INDEX.md` reports "Total Threads: 0".
- **Leftover terminal output.** The end of `GROK_RAW_ARCHIVE.md` (after Tweet 774) has two lines of local terminal output: a filename message and a shell prompt.
- `grok_archive_full.tar.gz` from the source repository was not copied, because it packages the same folders.
- Other public X accounts are mentioned in the posts (e.g. @xai, @elonmusk). Four public x.ai contact addresses appear in Tweet 774. No phone numbers, street addresses or tokens were found.

## Provenance

| Imported path | Source repository | Source path | Commit |
| --- | --- | --- | --- |
| `docs/grok/archive/**` (1,550 files) | [axamir/echoes-consented-record](https://github.com/axamir/echoes-consented-record) | `02_GROK_ARCHIVE/**` | `a6126edd915bd698a0f0f3faf044b3952f623655` |
| `docs/grok/GROK_RAW_ARCHIVE.md` | axamir/echoes-consented-record | `GROK_RAW_ARCHIVE.md` | `a6126ed…` |
| `docs/grok/GROK_RAW_ARCHIVE.md.ots` | axamir/echoes-consented-record | `GROK_RAW_ARCHIVE.md.ots` | `a6126ed…` |

Per-file SHA-256 values are listed in [`../../PROVENANCE.md`](../../PROVENANCE.md).
