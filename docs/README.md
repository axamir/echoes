# docs

Raw emails and other primary source documents for the Echoes project.

Each file should preserve the original date, sender, recipients, subject, and Case ID when those values are present in the source. Do not invent or infer identifiers. This folder is the authority for source facts; derived records in `data/` must point back here.

## Naming convention

Prefer:

- `YYYY-MM-DD_<sender>_<CaseID>.md`
- `YYYY-MM-DD_<sender>_<CaseID>.eml`

If a value is missing, omit it from the filename or mark it as unknown in the metadata table inside the file. Do not invent a date or Case ID to complete the name.

## Metadata template

Copy the table below to the top of each Markdown source file (or keep an equivalent header for `.eml` sidecars if needed). Replace every `TBD` with a value from the original message, or leave `TBD` / `unknown` if the source does not provide it.

| Field | Value |
| --- | --- |
| id | TBD *(placeholder)* |
| date | TBD *(ISO 8601, as stated in the source)* |
| sender | TBD |
| recipients | TBD |
| subject | TBD |
| case_id | TBD |
| source_file | `docs/YYYY-MM-DD_<sender>_<CaseID>.md` *(this file)* |
| summary | TBD *(short factual summary; do not invent events)* |

**Status:** No source emails have been added yet. The table above is a placeholder template only.
