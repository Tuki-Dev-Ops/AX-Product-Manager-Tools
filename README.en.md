# Planning Document Workspace

[한국어](README.md) · **English** · [中文](README.zh.md) · [日本語](README.ja.md)

A working structure for writing IT service planning documents and keeping the links between them under control.
Writing standards are defined in [CLAUDE.md](CLAUDE.md).

---

## Background

Planning work is split across documents: project overview, planning review, service structure, flow, IA, wireframes, and functional specifications.
Splitting them makes each document readable, but editing one does not update the others.

* A requirement is added in 01 but never reaches the function list in 03.
* A screen is removed in 05 while the functional specification in 07 still refers to it.
* A screen appears in the flow in 04 but is missing from the screen list in 05.

As the document set grows, these gaps stop being visible to the naked eye.
Anything missed at review time turns into rework during design and development.

This repository keeps the links between documents as separate data rather than inside the prose,
and reports broken links every time the documents are built.

## Purpose

| Purpose | Approach |
| --- | --- |
| Traceability | Connect requirement → function → flow → screen → specification by identifier |
| Consistency checking | Detect broken links automatically when the dashboard is generated |
| Work visibility | Show status, progress, and change history for every document on one screen |
| Consistent writing | Keep sentence, terminology, status-name, and notation rules in a single `CLAUDE.md` |

The goal is not to generate documents automatically.
It is to keep documents written by people from drifting apart.

## How to run

### Prerequisites

Python 3.9 or later, plus PyYAML.

```bash
pip install pyyaml
```

### Build the dashboard

```bash
python tools/build_dashboard.py
```

This writes `dashboard/index.html`. Open it directly in a browser.
Document bodies are embedded in the HTML, so no server is required.

| Tab | Contents |
| --- | --- |
| Status | Overall progress, per-document progress and target time, counts by state |
| Change history | Every change entry, filterable by keyword, status, source, and document |

Selecting a document shows its full text inside the dashboard.
Flows, IA, architecture, and wireframes are drawn as diagrams within the text.

Consistency results are not shown on screen. They are printed to the console at build time.

```text
Built: dashboard/index.html (639KB, document text included)
Overall progress 100% · in progress 0 · pending 0 · done 8
Check: 0 open items, 0 unlinked items
```

### Screen code viewer

`dashboard/wireframe.html` inspects wireframes one screen at a time.
Pick a screen on the left and the rendered screen and its HTML appear on the right.
"Copy code" hands over the HTML and CSS for that screen as-is.

### Working sequence

1. Edit the document.
2. Add a change entry to `_data/changes.yaml`. List affected downstream documents under `affects`.
3. Reflect new or changed identifiers in `_data/trace.yaml`.
4. Record open questions, assumptions, and pending decisions in `_data/issues.yaml`.
5. Update status, progress, target time, version, and date in `_data/documents.yaml`.
6. Rebuild the dashboard and read the console check results.

When an upstream document changes, every document that inherits from it returns to the "In review" state.

## Structure

### Folders

```text
.
├── CLAUDE.md                  Writing standards + operating rules
├── README.md                  This document
├── docs/                      Client-facing planning documents (final deliverables)
│   ├── 01_프로젝트개요.md        Project overview
│   ├── 02_기획검토.md            Planning review
│   ├── 03_서비스구조.md          Service structure
│   ├── 04_Flow.md               Flow chart
│   ├── 05_IA.md                 Information architecture
│   ├── 06_Wireframe.md          Wireframes
│   ├── 07_기능명세.md            Functional specification
│   └── 08_검토결과.md            Review results
├── research/                  Raw research. Planning decisions belong in docs/02
├── _data/                     Cross-document link data
│   ├── documents.yaml         Status, progress, target time, inheritance per document
│   ├── trace.yaml             Requirement → function → flow → screen → spec entries
│   ├── changes.yaml           Change history
│   └── issues.yaml            Open questions, assumptions, pending decisions, conflicts
├── tools/
│   ├── build_dashboard.py     YAML + documents → dashboard, consistency check
│   └── dashboard_template.html
├── dashboard/
│   ├── index.html             Dashboard (generated)
│   └── wireframe.html         Screen code viewer (generated)
└── agent-system/              Role-based instructions used to extend the documents
```

Files under `dashboard/` are generated. Do not edit them directly.
To change the display, edit `tools/dashboard_template.html` and rebuild.

### Document inheritance

A downstream document takes the items defined upstream and makes them concrete. It never defines new items of its own.

```text
01 Project overview ──── defines: requirements (REQ)
 ├─→ 02 Planning review ─ defines: decisions (DC), proposals
 │      └─→ 03
 └─→ 03 Service structure defines: user types (UT), functions (FN)
        ├─→ 04 Flow chart ── defines: flows (FL)        refs: FN, UT
        ├─→ 05 IA ────────── defines: screens (SC)      refs: FN, FL
        │      └─→ 06 Wireframe defines: screen detail  refs: SC, FL
        └─→ 07 Functional spec defines: specs (FS)      refs: FN, SC, DC
08 Review results ─────── defines: issues (IS)          refs: consistency of 04–07
```

| Document | Upstream | Defines here | Inherited items |
| --- | --- | --- | --- |
| 01 Project overview | none | Requirements (REQ), scope, target users | none |
| 02 Planning review | 01 | Decisions (DC), proposals | REQ, scope |
| 03 Service structure | 01, 02 | User types (UT), functions (FN) | REQ, DC |
| 04 Flow chart | 03 | Flows (FL) | FN, UT |
| 05 IA | 03, 04 | Screens (SC), menu structure | FN, FL |
| 06 Wireframe | 05, 04 | Screen layout, behavior, exceptions | SC, FL |
| 07 Functional spec | 03, 05, 06, 02 | Specifications (FS) | FN, SC, DC |
| 08 Review results | 04, 05, 06, 07 | Issues (IS), corrections | FL, SC, FS |

### Identifiers

Identifiers are defined once in `_data/trace.yaml` and only referenced in the documents.
An assigned identifier is never changed, and is never reused after the item is deleted.

| Prefix | Item | Defined in |
| --- | --- | --- |
| REQ | Requirement | 01 |
| DC | Decision | 02 |
| UT | User type | 03 |
| FN | Function | 03 |
| FL | User flow | 04 |
| SC | Screen | 05 |
| FS | Functional specification | 07 |
| IS | Review issue | 08 |
| CH | Change entry | `_data/changes.yaml` |

Screen IDs follow `{channel}-{domain}-{type}`, for example `ADM-EVNT-LIST`.

### Consistency checks

The following conditions are checked at build time. Violations are printed with the document that owns the fix.

| Check | Owner |
| --- | --- |
| A requirement (REQ) is not linked to any function (FN) | 03 |
| A function (FN) does not appear in any flow (FL) | 04 |
| A function (FN) has no screen (SC) | 05 |
| A screen (SC) does not appear in any flow (FL) | 04 |
| A screen (SC) has no wireframe yet | 06 |
| A screen (SC) has no functional specification (FS) | 07 |
| A reference points to an identifier that does not exist | Definition conflict |

### Document status and progress

Each document entry in `_data/documents.yaml` carries the following values.

| Field | Values | Meaning |
| --- | --- | --- |
| status | Not started / Drafting / In review / Confirmed | Working state |
| category | Planning / Design / Specification / Review | Shown as a tag on the dashboard |
| progress | 0–100 | Progress. A confirmed document counts as 100 |
| eta | 2026-09-05 18:00 | Target completion time. Empty means undecided |

```text
Not started   Writing has not begun
Drafting      Draft in progress
In review     Draft complete; under review or affected by an upstream change
Confirmed     Reviewed; usable as the basis for downstream documents
```

Overall progress is the average across the eight documents.
The remaining time shown is the countdown to the latest target time among unfinished documents.

### Research material

Research results are kept verbatim under `research/`.
They are not copied into the documents. They are converted into decisions for this service and recorded in `docs/02_기획검토.md`.
Source URLs stay with the original research file.
