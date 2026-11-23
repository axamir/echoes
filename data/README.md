# data

Derived structured data for the Echoes project.

- `emails.schema.json` — JSON Schema for one email record
- `emails.json` — array of email records (currently an empty array: `[]`)

Each record in `emails.json` must validate against the schema and must point to an existing file in `docs/` via `source_file`. Populate this file only from actual source documents. Do not invent `id`, `date`, `sender`, `recipients`, `subject`, `case_id`, or `summary` values.

**Status:** `emails.json` is an empty placeholder dataset. No email records have been added yet.
