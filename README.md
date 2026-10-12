# reen_skills

个人 Agent Skills 集合，兼容支持 `SKILL.md` 的 Agent 平台（例如 Codex、Claude Code 等）。

## 包含的 Skills

| Skill | 用途 |
| --- | --- |
| `advisor-wechat-english` | 与外籍学术导师沟通的自然英文微信表达 |
| `cs2-skin-quant` | CS2 饰品市场分析与交易实验评估 |
| `github-profile-banner-studio` | GitHub 个人主页横幅制作与优化 |
| `hatch-pet` | 动画宠物素材生成与验证 |
| `human-writing` | 自然中文创作、长文写作与改稿 |
| `product-design` | 从产品访谈、设计到实现与发布的完整工作流 |
| `aihot` | 查询当前中文 AI 热点与日报 |
| `frontend-design` | 设计有辨识度的网页与 App 界面 |
| `grilling` | 逐个问题澄清想法和决策 |
| `hv-analysis` | 用横纵分析法完成深度研究并生成 PDF |
| `khazix-writer` | 公众号长文写作工作流 |
| `leader` | 将目标拆成可执行的 Agent 任务书 |
| `neat-freak` | 同步项目代码、文档、规则和记忆 |
| `prototype` | 快速验证 UI 或逻辑原型 |
| `reenai-writer` | 个人中文写作和风格校准 |
| `tutor-workbench` | 本地优先的家教备课与教学资料工作流 |
| `writing-fragments` | 从原始素材中挖掘写作片段 |
| `writing-shape` | 将素材逐段组织成文章 |

## 安装

安装单个 Skill：

```bash
npx skills add Reen-Ai-H/reen_skills --skill grilling --agent codex
```

安装全部 Skill：

```bash
npx skills add Reen-Ai-H/reen_skills --skill '*' --agent codex
```

## 来源与公开使用说明

本仓库是个人整理与分发集合。每个 Skill 目录保留原始文件、作者信息和许可证文件（如原目录包含）。使用或再分发前，请阅读对应目录中的 `SKILL.md`、`LICENSE` 或 `LICENSE.txt`，并遵守原作者许可。

特别注意：

- `khazix-writer` 包含特定作者风格工作流，不应冒充原作者或用于未经授权的商业模仿。
- `tutor-workbench` 是本地优先的教学工作流，使用前应替换为自己的资料路径和知识库。
- `aihot` 依赖其文档中说明的匿名只读 API 约定。
- `frontend-design` 的许可条款以其目录中的 `LICENSE.txt` 为准。

本仓库不包含 Codex 系统自带的 `imagegen`、`openai-docs`、`skill-creator`、`skill-installer` 等系统 Skill，也不包含由插件安装和管理的 Skill。

同步日期：2026-10-12。当前包含 18 个本地个人 Skill，保留配套 references、scripts、assets、agents 和测试资料；不包含运行缓存和本地凭据。
