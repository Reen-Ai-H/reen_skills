---
name: tutor-workbench
description: Use the 家教工作台 for an individual tutor's real lesson preparation, teaching materials, parent feedback, student profiles, and teaching retrospectives. Trigger for authorised local teaching PPTX ingestion; high-school math or English tutoring preparation; junior-to-senior high math bridging; printable student handouts; concise teacher guides; parent feedback; and turning lesson observations into a reusable local experience base. Work only from the local knowledge and experience bases; do not use web research or external model APIs.
---

# 家教工作台

Use this skill as a local-first tutoring workflow. The project root is `C:\Users\maker\Desktop\就业\家教\家教工作台`.

## Non-negotiables

- Treat the knowledge base and experience base as the primary assets. Prefer their existing records; do not invent a source example, answer, or teaching conclusion.
- Ask for only the missing information required for the requested artifact. Preserve uncertainty as a note instead of guessing.
- Separate audiences: student materials contain only learning content; teacher guides contain teaching cues; parent feedback contains concrete observations, not diagnoses or generic praise.
- Keep student-facing output print-clean: no AI process, lesson workflow, parent communication, or lengthy motivational text.
- Keep personal data minimal. Use a stable `student_id` instead of full names in records.

## Choose the workflow

| Request | Do |
| --- | --- |
| Ingest an authorised PPTX | Run `scripts/inspect_pptx.py`, inspect the rendered slides, then create or update chapter JSON files using `references/data-schema.md`. Mark uncertain extraction for review. |
| Prepare a lesson | Read the student profile, matching knowledge records, question types, examples, and relevant experience records. Produce only the requested student handout, teacher guide, and/or parent-feedback draft. |
| Record a lesson | Add one retrospective record; update an experience rule only after the pattern appears in at least two lessons or the tutor explicitly promotes it. |
| Update a profile | Merge new observed facts into the student profile; distinguish observation from inference. |

## 1. Ingest a PPTX

1. Confirm that the material is authorised for the tutor's local use.
2. Run `scripts/inspect_pptx.py <pptx> --out <review-folder>`. It renders image-based PPTX slides locally and extracts native text when present.
3. Inspect every content-bearing slide. Ignore decorative pages, but retain all teachable definitions, methods, common errors, question families, and source examples.
4. Create or update the chapter's `knowledge-points.json`, `question-types.json`, `examples.json`, and `source-material.json` atomically in one patch.
5. Store examples only when their wording, answer, and explanation are readable. Set `verification_status` to `needs_review` otherwise.
6. Do not store slide numbers or citations in learner-facing output.

## 2. Prepare a lesson

Read `references/data-schema.md` first. Then:

1. Build a compact lesson brief from the student profile and the requested target.
2. Select the smallest coherent set of knowledge points and one representative example per question type. Match the difficulty to the student.
3. Generate the requested outputs under `outputs/<student_id>/<YYYY-MM-DD>-<topic>/`.
4. Name files `student-handout.md`, `teacher-guide.md`, and `parent-feedback-draft.md`. Create DOCX only when asked; use the document workflow and verify its rendering.

### Student handout rules

Use this order: `本节目标` → `知识点与提醒` → `典型题型` → `课堂练习（可选）` → `一页小结`.

- Include no more than 3–4 core knowledge points and 2–4 representative examples in one normal lesson.
- Write a recognisable signal and first action for every question type.
- Put solutions in a teacher-only companion unless the tutor asks for a student answer version.

### Teacher guide rules

Use: goal, suggested sequence, essential explanation, example entry point, answer/key steps, approximate timing, flexible adjustment, and after-class suggestion. Give options rather than a rigid script. Refer to `experience-base` when applicable.

### Parent feedback rules

Use observed evidence: what was learned, specific performance/state, demonstrated gains, remaining reinforcement, next topic, and one concise home suggestion. Avoid labels such as “基础薄弱” unless paired with a precise observable fact.

## 3. Record and promote experience

Use the retrospective format in `references/data-schema.md`.

- Write lesson facts first: obstacle, effective or ineffective explanation, emotional state, parent concern, and next adjustment.
- Do not treat a single lesson as a general rule.
- Promote a pattern to `experience-base/teaching-rules.json` only with two supporting lesson IDs or explicit tutor confirmation. State its scope and counter-signal.

## Required checks before delivery

- Every selected example exists in `examples.json` and is `verified`.
- The handout has no teacher/parent/internal content and its quantity fits the lesson duration.
- Every parent-feedback claim is supported by an observation from this lesson.
- The retrospective separates `observations` from `inferences`.

## Windows DOCX rendering

When a Word document must be visually verified on Windows, use
`scripts/render_docx_windows.py <docx> --output_dir <folder>` instead of calling
the generic renderer directly. This local wrapper supports Chinese paths,
creates a valid `file:///C:/...` LibreOffice profile URI, stages legacy-codepage
unsafe paths in an ASCII-only temporary directory, and falls back to installed
Microsoft Word if LibreOffice genuinely fails.
