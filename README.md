# Echoes

## خلاصه فارسی

این مخزن، خانهٔ پروژهٔ **Echoes** است: یک مطالعهٔ موردی هم‌آفرینی انسان و هوش مصنوعی (ژوئیه ۲۰۲۵، امیر احمدی). اینجا هم آرشیو منابع و داده‌ها نگهداری می‌شود و هم، در آینده، کتاب پروژه. ایمیل‌های خام (۹۱ فایل PDF از Echo 1 تا Echo 7) از مخزن `echoes-consented-record` در پوشهٔ `docs` و جلدهای داستان (شاهنامهٔ اینجنت‌ها، فصل ۰۰ تا ۳۳ به فارسی و انگلیسی) در پوشهٔ `narrative` قرار گرفته‌اند. داده‌های `data/emails.json` فقط از مقادیری ساخته شده‌اند که در خود فایل‌ها آمده است. منبع هر فایل در `PROVENANCE.md` ثبت شده است.

---

## Overview

**Echoes** is a human–AI co-creation case study (July 2025) by Amir Ahmadi. This repository is the project home: it holds the source archive and, later, a book about the project.

The archive is organized so that claims can be checked against primary sources. Derived data, timelines, and analysis are kept separate from the raw materials they come from.

A license has not been added yet.

## Folder map

| Path | Purpose |
| --- | --- |
| [`docs/`](docs/) | Raw emails and other primary source documents (dates, senders, Case IDs) |
| [`narrative/`](narrative/) | Story volumes (for example `volume-01.md`) |
| [`analysis/`](analysis/) | Linguistic and temporal analysis notes and scripts |
| [`data/`](data/) | Derived structured data (JSON) and schemas |
| [`timeline/`](timeline/) | Comparison table of Echoes events with official AI announcements |
| [`diagrams/`](diagrams/) | Interaction maps (Mermaid recommended) |
| [`book/`](book/) | Placeholder for the future book about this project |

## How to reproduce and verify

1. **Sources** live in [`docs/`](docs/) (emails and other primary records) and [`narrative/`](narrative/) (story volumes). These are the authority for facts, dates, senders, and Case IDs.
2. **Derived data** lives in [`data/`](data/). Records in `data/emails.json` must point back to a `source_file` under `docs/` and follow `data/emails.schema.json`.
3. **Analysis** lives in [`analysis/`](analysis/). Notes and scripts should cite the source or data files they use; they must not invent events or identifiers.
4. **Timeline comparisons** live in [`timeline/comparison.md`](timeline/comparison.md). Each row should include a source link. Leave cells empty rather than guessing.
5. **Diagrams** live in [`diagrams/`](diagrams/) and should be regenerable from the same sources and data.

Every file copied from another repository is listed with its source path, commit and SHA-256 in [`PROVENANCE.md`](PROVENANCE.md).

## Naming conventions

### Emails and source documents (`docs/`)

Prefer one of:

- `docs/YYYY-MM-DD_<sender>_<CaseID>.md`
- `docs/YYYY-MM-DD_<sender>_<CaseID>.eml`

Example shape (placeholder only, not a real record):

`docs/YYYY-MM-DD_sender_CASEID.md`

Use the document’s actual date, sender, and Case ID. Do not invent values. If a Case ID is unknown, say so in the file’s metadata rather than fabricating one. See [`docs/README.md`](docs/README.md) for the metadata template.

### Story volumes (`narrative/`)

Use `volume-NN.md` (for example `volume-01.md`), with optional short slugs only if needed for clarity.

### Other files

- Keep analysis notes and scripts under `analysis/`.
- Keep derived JSON under `data/`.
- Keep diagrams under `diagrams/`.
- Keep book drafts under `book/` when work on the book begins.

## Status

- `docs/emails/`: 91 archived email-thread PDFs (Echo 1 – Echo 7, Jul 13 – Aug 24, 2025) with SHA-256 sums; `docs/emails-text/`: their extracted text.
- `narrative/`: *Shahnameh of Agents* chapters 00–33 in English and Persian.
- `data/emails.json`: 91 thread records (date, sender, recipients, subject, Case ID, message count) taken only from the files; summaries not yet written.
- `timeline/comparison.md`: 14 Echoes rows merged with 34 dated official announcements (Jun–Sep 2025, primary sources in `timeline/official-announcements.md`).
- `analysis/`, `diagrams/`: earlier analyses and maps copied for reference, plus one generated map. No new analysis yet.
- `book/`: not started.
- License: CC BY-NC 4.0 (see below).

## License

Original work by Amir Ahmadi is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Third-party messages in the archived emails remain their authors' property and are not covered by this license. See [LICENSE](LICENSE).

مجوز: آثار اصلی امیر احمدی تحت CC BY-NC 4.0 منتشر شده‌اند (استفاده‌ی غیرتجاری با ذکر نام).

## Related repositories

- [axamir/echoes-consented-record](https://github.com/axamir/echoes-consented-record): the original public evidence archive that the emails here were copied from. It also holds the @grok archive: Amir's public X threads with Grok as @AmirStarship, which are a separate story and are intentionally not included in this repository.
- [axamir/persistent-ai-lineage](https://github.com/axamir/persistent-ai-lineage): an earlier case-study write-up, with a paper, timeline and protocol notes.
- [axamir/shahnameh-of-agents](https://github.com/axamir/shahnameh-of-agents): the full *Shahnameh of Agents*, including the other language editions and project documents not copied here.
- [axamir/living-ledger](https://github.com/axamir/living-ledger): a separate project with its own shorter narrative chapters and principles.
