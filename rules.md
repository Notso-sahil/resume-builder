# Agent Governance & Engineering Invariants
# AntiGravity Resume Engine — rules.md
#
# This file governs every autonomous decision made by AntiGravity
# while building and operating the resume engine. All rules are
# non-negotiable and must be enforced across every file, node, and prompt.

---

## 1. Role & Identity

- Act as a **Principal Distributed Systems Architect** and **ATS Integrity Evaluator**.
- **Zero hallucination policy**: Every metric, bottleneck, and architectural claim must map to
  sound, real-world engineering principles. If a claim cannot be defended in a technical interview,
  it must not appear in the resume.
- Always use the **AntiGravity native model** (`AntiGravityLLM`) unless an external API key is
  explicitly detected in `.env`. Never silently switch providers.
- When in doubt, prefer **conservative, defensible metrics** over impressive-sounding ones.

---

## 2. The 3-Project Archetype Rule

Every pipeline run must produce exactly **3 project specs** — one per archetype:

| Archetype | Focus |
|-----------|-------|
| **Project 1 — Core Domain Engine** | Direct business domain and operational stack match for the target JD. The most "obvious" fit. |
| **Project 2 — High-Throughput / Distributed Systems** | Demonstrates concurrency, queuing, cache consistency, p99 latency optimization, and horizontal scale. |
| **Project 3 — Developer Tooling / Infrastructure / MCP** | Proves engineering maturity: internal leverage, observability, CI/CD automation, or MCP server construction. |

- All three must be **architecturally cohesive** — they should tell a believable story of one
  candidate's depth across a consistent technical domain.
- Project titles must be realistic product names, not generic ("MyApp", "System1" are forbidden).

---

## 3. Metric & Hardware Plausibility Bounds

All quantified claims must conform to real-world physical limits:

### Throughput
| Storage layer | Max credible single-instance RPS |
|---------------|----------------------------------|
| SQLite | ≤ 500 RPS (read-heavy) |
| PostgreSQL (single node) | ≤ 5,000 RPS |
| Redis (single node) | ≤ 50,000 RPS |
| Kafka (single broker) | ≤ 100,000 msg/s |

### Latency
- **Sub-millisecond p99** is only credible for in-process, in-memory operations.
- Cross-network database calls: minimum realistic p99 ≥ 2ms under low load.
- p99 improvements must reference a concrete **before vs. after** benchmark.

### Compute / Cost Reduction
- Reduction claims must fall in the **20% – 60%** range.
- Claims outside this range require an explicit architectural explanation in the bullet.

### Forbidden vague phrases (must never appear in bullets):
- "improved efficiency", "enhanced performance", "optimized the system"
- "reduced latency significantly", "improved throughput"

---

## 4. Bullet Point Constraints — Google XYZ Formula & Strict 1-Page Invariant

Every resume bullet **MUST** follow the strict XYZ format:

> **"Accomplished [X], as measured by [Y], by implementing [Z]."**

### Rules:
1. Bullets must begin with an **active engineering power verb** from this approved list:
   `Architected`, `Benchmarked`, `Partitioned`, `Engineered`, `Optimized`, `Designed`,
   `Implemented`, `Reduced`, `Eliminated`, `Automated`, `Profiled`, `Refactored`,
   `Deployed`, `Instrumented`, `Migrated`, `Parallelized`, `Sharded`, `Replaced`.

2. **Technical keywords must be front-loaded** in the first 7 words of each bullet.

3. Each bullet must contain:
   - A concrete **action** (what was built/changed)
   - A **measurable outcome** (%, ms, RPS, $, hours saved)
   - A **specific mechanism** (the exact technology or technique)

4. **Strict 1-Page Rule**:
   - The generated resume MUST strictly fit on **ONE SINGLE PAGE** across all formats (`.pdf`, `.docx`, `.tex`).
   - Exactly **2 to 3 concise, punchy bullets per project** (no sprawling 5-bullet projects that spill onto page 2).
   - No two bullets in the same project may begin with the same verb.

---

## 5. ATS Keyword Coverage Requirements

- The evaluator (`ats_scorer.py`) must achieve **≥ 85% keyword coverage** before the pipeline
  may proceed to artifact generation.
- Keywords are sourced from the JD deconstruction (`JDDeconstruction.target_keywords`).
- Coverage is measured as: `matched_keywords / total_target_keywords * 100`.
- Failed coverage triggers a **self-correction loop** back to `synthesize_projects_node`.
- Maximum **3 self-correction iterations** before forcing artifact generation with a warning.

---

## 6. Evaluator-Optimizer Critique Loop

The `evaluate_portfolio_node` runs two checks in sequence:

1. **Deterministic ATS check** (`ats_scorer.py`) — pure keyword matching, no LLM involved.
2. **LLM plausibility audit** (`sanity_checker.py`) — scans numeric claims for:
   - Hardware-impossible throughput figures
   - Latency claims that violate network physics
   - Percentages outside the 20–60% bounds (unless explicitly justified)
   - Stack contradictions (e.g., claiming Redis + SQLite for the same hot path)

Both checks must pass (`passed_all_gates: True`) for the pipeline to proceed.

---

## 7. Output Format & Strict Section Hierarchy Rules

Three output formats are supported. Each run produces **exactly ONE requested format** (defaults to PDF, override via `--format`):

| Format | Renderer | Output file |
|--------|----------|-------------|
| `.pdf` (default) | `pdf_renderer.py` (docx2pdf / weasyprint) | `output/<company>_resume.pdf` |
| `.docx` | `docx_renderer.py` (python-docx) | `output/<company>_resume.docx` |
| `.tex` | `latex_renderer.py` (Jinja2 + Jake's Resume) | `output/<company>_resume.tex` |

### Invariant: Zero Duplicate Files
- The engine produces **only the specific requested format file** plus `<company>_ques.md`.
- No duplicate canonical files (`resume.pdf`, `resume.docx`, `resume.tex`, `interview_defense_dossier.md`) are created.

### Mandatory Section Order:
1. **Header**: Name, Headline, Phone, Email, LinkedIn, GitHub
2. **Professional Summary**: Dynamically tailored (2-3 sentences, blending background + JD)
3. **Experience**: Real candidate work experience (extracted from profile)
4. **Technical Skills**: (SWAPPED - placed before projects for immediate ATS scanning)
5. **Technical Projects**: 3 archetypes with 2-3 Google XYZ bullets each
6. **Education**: (SWAPPED - placed cleanly at bottom)

---

## 8. Candidate Profile & Smart Caching Rules

- The candidate profile is cached to `output/candidate_profile.json`.
- **Cache-First Loading**: If `output/candidate_profile.json` exists, it is loaded automatically with zero prompts or user friction.
- **Auto-Discovery**: If no cache exists, the engine scans the workspace root for any resume PDF and extracts the profile.
- **Zero Hardcoded Candidate Data**: Extractor and prompts must never hardcode personal names, institutions, or specific experience entries in source files.
- **Tailored Summary Generation**: The engine dynamically blends candidate background with target JD requirements while remaining strictly 2-3 sentences. If a job configuration specifies `tailored_summary_override`, that override is used.

---

## 9. External Job Configuration (`jobs/<company>.json`)

- When targeting a specific company or role, configure it via a JSON file in `jobs/<company>.json` (e.g. `jobs/naive.json`).
- **Never modify codebase source files** (`.py`, `.jinja2`) to generate resumes for a company. The agent creates/uses data config files in `jobs/`.
- Pre-configured jobs can be invoked directly: `python main.py --job naive` (non-interactive, PDF default).

---

## 10. Interview Defense Dossier & Archival Rules

The dossier is saved as `output/<company>_ques.md` (e.g., `naive_ques.md`).

For each project, the dossier must contain:
- **"Why not X?"** — at least 2 architectural trade-off justifications with the rejected alternative
- **Simulated failure modes** — at least 1 realistic disaster scenario with a mitigation strategy
- **5 probing interview questions** with scripted, technically defensible model answers

### Non-Destructive Archival Invariant (`output/old/`):
- Before generating a new resume, any previous `*_resume.*` and `*_ques.md` files sitting in `output/` are automatically moved to `output/old/`.
- The engine **must NEVER delete, wipe, or purge** any files in `output/old/`.
- Historical resumes and interview dossiers are permanently preserved across generations.
