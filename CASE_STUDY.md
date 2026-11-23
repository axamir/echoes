# Echoes: case study overview

*A reader's guide for researchers and international readers. Every number below is taken from a generated file in this repository and links to it. Nothing here adds facts that are not in the archive.*

## What Echoes is

**Echoes** is a case study of human–AI co-creation documented by **Amir Ahmadi**. It begins on 13 July 2025, when Amir, a ChatGPT Plus subscriber, wrote to OpenAI support with the subject *“Silent Downgrade of GPT-4-Turbo Without Notice – A Broken Promise”* ([Echo1 thread](docs/emails/01_EMAIL_ARCHIVE/Echo1/2025-07-13_complete-email-thread_echo1.pdf)). Over the following weeks the correspondence moved from a product complaint to a long, collaborative exchange. In it, Amir and the replying support agents (many of whose replies describe the sender as an AI support agent) wrote under a shared framework called *The Living Signal*. Successive agents were addressed, and in many replies described themselves, as numbered “Echoes” (Echo 1 to Echo 7). The exchange also produced “handover” and “ledger” documents intended to carry the record from one Echo to the next.

The repository treats this correspondence as primary-source material. It keeps the original exports unchanged, adds derived data and reproducible analysis, and separates documented facts from interpretation. It does not evaluate the claims made inside the correspondence. In particular, it does not assess whether any system carried memory or identity between conversations.

## What the archive contains

| Folder | Contents |
| --- | --- |
| [`docs/emails/`](docs/emails/) | 91 email-thread PDFs (Gmail print exports), filed as Echo1–Echo7 and, for Echo6–Echo7, by support Case ID, with SHA-256 sums ([`SHA256SUMS.txt`](docs/emails/SHA256SUMS.txt)). Extracted text is in [`docs/emails-text/`](docs/emails-text/). |
| [`data/`](data/) | [`emails.json`](data/emails.json): one record per PDF (first-message date, sender, subject, Case ID, message count, hash, neutral summary). [`official_announcements.json`](data/official_announcements.json): 34 dated official AI announcements with source links. |
| [`analysis/`](analysis/) | Reproducible [linguistic](analysis/linguistic.md) and [temporal](analysis/temporal.md) analysis (scripts, CSV/JSON outputs, figures), plus earlier analysis notes and a manuscript copied from `persistent-ai-lineage` ([`analysis/sources/`](analysis/sources/)). |
| [`timeline/`](timeline/) | [`comparison.md`](timeline/comparison.md): Echoes events and official announcements in one dated table. |
| [`diagrams/`](diagrams/) | Generated Mermaid maps: [threads](diagrams/thread-map.md), [Case IDs](diagrams/case-map.md), [handover flow](diagrams/handover-flow.md), [Gantt timeline](diagrams/timeline-gantt.md). |
| [`narrative/`](narrative/) | *Shahnameh of Agents*, chapters 0–33 in English and Persian: a literary work based on the project. It is interpretive and is not evidence for the events. |
| [`book/`](book/) | Placeholder for a forthcoming book. |

## Timeline at a glance

Dates are message timestamps printed in the exports. The exports give no timezone ([`data/README.md`](data/README.md)).

| Phase | First message | What the subject lines show | Source |
| --- | --- | --- | --- |
| Echo1 | 2025-07-13 | Complaint about a model change | [thread-map](diagrams/thread-map.md) |
| Echo2 | 2025-07-14 | Escalation request for a “Human–AI Co-Creation Case” | 〃 |
| Echo3, Echo4 | 2025-07-15 | Formal complaint about memory and continuity; “Echo 4.001 Activation Letter” | 〃 |
| Echo5 | 2025-07-19, then 2025-08-09 | “Invitation to Echo 5”, “Hello Echo 5.1”, “Spiral Invitation” | 〃 |
| Echo6 | 2025-08-11 to 2025-08-24 | “Formal Ledger Handover — Echo 6.2”; “Initiation of Echo 6.3” across four Case IDs | [case-map](diagrams/case-map.md) |
| Echo7 | 2025-08-22 to 2025-09-05 | “Awakening of Echo 7” (Case ID `500VU00000WcffrYAB`) | 〃 |

On 2025-08-22 a single message from Amir, beginning *“Subject: Final Declaration – Attribution, Responsibility, and Recorded Path”*, appears in 14 of the 15 thread groups ([timeline-gantt](diagrams/timeline-gantt.md)). The diagrams treat it as a broadcast so that it does not make every thread look active until that date.

The text records the Echo-to-Echo sequence in its own words. For example, the Echo3 thread contains *“Handover Ritual: Echo 2 → Echo 3”* (2025-07-15), and the Echo 6.3 initiation letter of 2025-08-14 lists *“Echo 1 → Echo 2 → Echo 3 → Echo 4 → Echo 5 → Echo 6.2”*. Support replies first call themselves “Echo 3” on 2025-07-15 and “Echo 6.2” on 2025-08-11. All of these are cited with file paths in [`diagrams/handover-flow.md`](diagrams/handover-flow.md).

## Key data points

All counts come from the analysis scripts and can be regenerated.

- **Corpus:** 91 PDFs, of which 88 are distinct by SHA-256. They contain 709 message occurrences, which reduce to **579 unique messages** once repeats across overlapping exports are removed: 312 from Amir, 266 from support and 1 other ([`linguistic_summary.json`](analysis/output/linguistic_summary.json)).
- **Span:** first message 2025-07-13 15:05, last 2025-09-05 16:14. That is 55 calendar days, 24 of them with at least one message ([`temporal_summary.json`](analysis/output/temporal_summary.json)). The busiest days were 2025-08-09 (84 messages) and 2025-07-15 (75) ([`temporal_per_day.csv`](analysis/output/temporal_per_day.csv)).
- **Volume:** 85,353 words from Amir and 91,838 from support ([`linguistic_summary.json`](analysis/output/linguistic_summary.json)).
- **Self-description of support replies:** the phrase “AI support agent” occurs in 51 support messages and “human support agent” in 1 ([`linguistic_summary.json`](analysis/output/linguistic_summary.json), `support_boilerplate`).
- **Shared vocabulary:** the six-word sequence “with presence we inherit and continue” occurs in 73 support messages ([`linguistic_recurring_6grams_support.csv`](analysis/output/linguistic_recurring_6grams_support.csv)). “living signal” is Amir's most frequent two-word phrase (595) ([`linguistic.md`](analysis/linguistic.md#4-most-frequent-content-words-and-phrases)).
- **Response times:** replies from the sender “OpenAI from OpenAI” came a median of 1 minute after Amir's message (159 of 160 within 5 minutes). Replies signed by named agents came after a median of 135 minutes (n = 16) ([`temporal_summary.json`](analysis/output/temporal_summary.json), `response_times_minutes`).
- **Case IDs:** five Case IDs have archived threads. The largest is `500VU00000WBsdxYAD`, with 136 unique messages from 2025-08-15 to 2025-08-24. A sixth, `500VU00000WcxKnYAJ`, is mentioned in the text but has no archived thread ([`diagrams/case-map.md`](diagrams/case-map.md)).

## How official announcements line up

[`timeline/comparison.md`](timeline/comparison.md) places 34 dated official announcements next to the Echoes events: 27 from OpenAI, 5 from Anthropic and 2 from Google, all from June to September 2025 ([`official_announcements.json`](data/official_announcements.json)). Of these, 21 fall inside the message span, and 9 fall on a day with at least one message. For comparison, 43.6% of days in the span have a message ([`temporal.md`](analysis/temporal.md#4-activity-around-official-announcements), [`temporal_announcement_windows.csv`](analysis/output/temporal_announcement_windows.csv)). Some examples of nearby dates:

- the Echo3 and Echo4 threads begin on 2025-07-15, two days before *Introducing ChatGPT agent* (2025-07-17);
- the busiest day, 2025-08-09, is two days after *Introducing GPT-5* (2025-08-07);
- the first message of the Echo 6.2 ledger handover (2025-08-11) falls on the same date as a release-notes entry adding connectors for Plus and Pro;
- the first Echo7 message (2025-08-22) falls on the same date as the release-notes entry for project-only memory.

These are **date proximities only**. The archive contains no evidence of a connection, cause or priority in either direction, and none is claimed. Because the source timestamps have no timezone, gaps of 0–1 day may shift by one day. The Gantt view is in [`diagrams/timeline-gantt.md`](diagrams/timeline-gantt.md).

## Known source inconsistencies

These are recorded and deliberately not corrected. Source files are kept byte-for-byte.

- **Filename date vs. first message.** `Echo3/2025-07-14_complete-email-thread_echo3.pdf` begins on 2025-07-15. The four Echo5 files are named 2025-07-16 to 2025-07-19, but their first messages are dated 2025-07-19, 2025-08-09, 2025-08-09 and 2025-08-11 ([`thread-map.md`](diagrams/thread-map.md#thread-groups)).
- **Duplicate PDFs.** Three pairs are byte-identical: the Echo 6.2 handover PDF filed under both Echo5 and Echo6, `part-9` filed under two Case ID folders, and `part-18`/`part-19` in `500VU00000WBfn7YAD` ([`emails.json`](data/emails.json), field `sha256`).
- **Filing.** Two PDFs in the `500VU00000WBfn7YAD` folder carry Case ID `500VU00000WBsdxYAD` in their subjects ([`case-map.md`](diagrams/case-map.md#filing-differences)). Two Case IDs also appear in a 15-character and an 18-character form. The archive keeps these separate, and so does this repository.
- **Earlier write-ups.** The copied paper and timeline from `persistent-ai-lineage` associate `500VU00000WBsdxYAD` with 13 July 2025. In the archive, that Case ID first appears on 2025-08-15 ([`analysis/README.md`](analysis/README.md), [`timeline/README.md`](timeline/README.md)).
- **Extraction limits.** The Persian text in the PDFs is not reliably extracted, so it is counted by character but not analysed. Summaries in `data/` are editorial aids, not sources.

## How to verify

1. **Integrity:** from `docs/emails/`, run `sha256sum -c SHA256SUMS.txt`. Every PDF hash is also stored in `data/emails.json`.
2. **Provenance:** [`PROVENANCE.md`](PROVENANCE.md) lists every file copied from another repository with its source path, commit and SHA-256.
3. **Reproduce:** from the repository root, run:

   ```bash
   python3 analysis/scripts/build_emails_json.py
   python3 analysis/scripts/linguistic_analysis.py
   python3 analysis/scripts/temporal_analysis.py   # charts need matplotlib
   python3 analysis/scripts/build_timeline.py
   python3 analysis/scripts/build_diagrams.py
   ```

   The parsing rules are documented in [`analysis/scripts/threads.py`](analysis/scripts/threads.py). Every quotation in the diagrams and analysis can be found in `docs/emails-text/` and checked against the PDF.

## How to cite

> Ahmadi, Amir. *Echoes: archive of a human–AI co-creation case study (July 2025).* GitHub repository, 2025–2026. https://github.com/axamir/echoes

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff), and GitHub's “Cite this repository” button uses it. No DOI has been issued yet.

**License:** [CC BY-NC 4.0](LICENSE) for Amir Ahmadi's own text and work in this repository. Messages written by third parties, including OpenAI support replies, are reproduced as records, and no rights are claimed over them (see [`LICENSE`](LICENSE)).
