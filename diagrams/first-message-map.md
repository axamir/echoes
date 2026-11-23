# Interaction map — who opens each archived thread

Generated from [`data/emails.json`](../data/emails.json): an arrow means the **first message** of an archived thread (PDF) was sent by that sender, grouped by Echo folder or Case ID folder. Edge labels are PDF counts (duplicate PDFs in the source are counted). Only the first message of each thread is used; replies inside threads are not counted.

```mermaid
flowchart LR
  N0["Integration User Quartz (support-team@mail.openai.com)"] -->|1| N1["500VU00000WBfn7"]
  N2["Support Team (support-team@mail.openai.com)"] -->|25| N3["500VU00000WBfn7YAD"]
  N0["Integration User Quartz (support-team@mail.openai.com)"] -->|1| N4["500VU00000WBsdx"]
  N2["Support Team (support-team@mail.openai.com)"] -->|48| N5["500VU00000WBsdxYAD"]
  N2["Support Team (support-team@mail.openai.com)"] -->|6| N6["500VU00000WcffrYAB"]
  N7["Amir Ahmadi (starship.amir@gmail.com)"] -->|1| N8["Echo1"]
  N7["Amir Ahmadi (starship.amir@gmail.com)"] -->|1| N9["Echo2"]
  N7["Amir Ahmadi (starship.amir@gmail.com)"] -->|1| N10["Echo3"]
  N11["Amir Ahmadi (starship.meta@gmail.com)"] -->|1| N12["Echo4"]
  N7["Amir Ahmadi (starship.amir@gmail.com)"] -->|4| N13["Echo5"]
  N7["Amir Ahmadi (starship.amir@gmail.com)"] -->|2| N14["Echo6"]
```
