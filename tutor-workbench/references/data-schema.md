# 本地数据约定

所有 JSON 使用 UTF-8、数组为主、稳定 `id` 不复用。日期用 `YYYY-MM-DD`；难度只用 `基础`、`巩固`、`提升`。

## 知识库

`knowledge-points.json`

```json
{
  "schema_version": "1.0",
  "items": [{
    "id": "hsm-c1-set-kp-001",
    "name": "集合的确定性",
    "definition_or_core_conclusion": "…",
    "formulas_properties_methods": ["…"],
    "confusions_and_errors": ["…"],
    "difficulty": "基础",
    "suitable_for": ["初升高衔接", "高一基础巩固"],
    "verification_status": "verified"
  }]
}
```

`question-types.json`

```json
{
  "schema_version": "1.0",
  "items": [{
    "id": "hsm-c1-set-qt-001",
    "name": "判断对象是否构成集合",
    "knowledge_point_ids": ["hsm-c1-set-kp-001"],
    "recognition_features": ["题目给出一个对象总体，要求判断能否构成集合"],
    "basic_approach": ["检查对象范围是否明确", "检查同一标准下归属是否唯一"],
    "common_errors": ["把‘很高’‘好看’等主观描述当作确定条件"],
    "difficulty": "基础",
    "suitable_for": ["初升高衔接"],
    "example_ids": ["…"]
  }]
}
```

`examples.json`

```json
{
  "schema_version": "1.0",
  "items": [{
    "id": "hsm-c1-set-ex-001",
    "question_type_id": "hsm-c1-set-qt-001",
    "stem": "…",
    "answer": "…",
    "concise_solution": ["…"],
    "difficulty": "基础",
    "suitable_for": ["初升高衔接"],
    "verification_status": "verified"
  }]
}
```

`source-material.json` only records local provenance for maintenance, not for learner output: `material_id`, `local_path`, `subject`, `grade`, `textbook_version`, `chapter`, `ingested_on`, `coverage_note`.

## 学生与经验

`students/student-profiles.json`: one item per `student_id`; fields: `grade`, `region`, `textbook_version`, `subject`, `current_score`, `foundation`, `weak_chapters`, `learning_state`, `parent_goal`, `lesson_frequency`, `lesson_duration_minutes`, `updated_on`. Keep `observations` as dated facts and `working_hypotheses` separate.

`experience-base/lesson-retrospectives.json`: `lesson_id`, `student_id`, `date`, `subject`, `topic`, `planned_goal`, `actual_progress`, `observations`, `inferences`, `stuck_points`, `effective_moves`, `ineffective_moves`, `emotion_and_engagement`, `parent_focus`, `next_adjustments`, `linked_example_ids`.

`experience-base/teaching-rules.json`: only promoted patterns. Each rule has `id`, `rule`, `scope`, `supporting_lesson_ids` (at least two unless tutor-promoted), `counter_signal`, `status` (`trial`/`stable`), `last_updated`.
