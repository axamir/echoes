# Echoes

## خلاصه فارسی

این مخزن، خانهٔ پروژهٔ **Echoes** است: یک مطالعهٔ موردی هم‌آفرینی انسان و هوش مصنوعی (ژوئیه ۲۰۲۵، امیر احمدی). اینجا هم آرشیو منابع و داده‌ها نگهداری می‌شود و هم، در آینده، کتاب پروژه. فایل‌های منبع (ایمیل‌ها و جلدهای داستان) هنوز اضافه نشده‌اند. وقتی آن‌ها در پوشهٔ `docs` و `narrative` قرار گرفتند، داده‌های مشتق‌شده در `data`، جدول زمانی در `timeline`، و تحلیل‌ها در `analysis` از روی همان منابع ساخته می‌شوند.

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

Until source files are added, `data/emails.json` is an empty array and the timeline table has headers only.

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

**Source files are still to be added.** This repository currently contains only the folder scaffold, README files, an empty emails dataset, a JSON Schema, and an empty timeline table. No emails, Case IDs, narrative volumes, analysis results, timeline events, or book chapters have been added yet.
