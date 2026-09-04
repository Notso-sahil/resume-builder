# AntiGravity Autonomous Resume Engine: Architecture & Implementation Spec

An intelligent, multi-stage agentic engine that deconstructs technical Job Descriptions (JDs), synthesizes architecturally sound engineering projects across 3 complementary archetypes, rigorously optimizes ATS-targeted resume bullets using the Google XYZ formula, self-audits metric plausibility, and produces an **Interview Defense Dossier** with ready-to-export resumes in `.docx`, `.pdf`, or **LaTeX** (`.tex`) format.

---

## 0. Execution Modes

This engine supports two operating modes. **Mode 1 (AntiGravity-native) is the primary and default path.** Mode 2 is an optional fallback for users who supply their own LLM API keys.

| | Mode 1 — AntiGravity Native (Primary) | Mode 2 — External API Key (Secondary) |
|---|---|---|
| **LLM Provider** | AntiGravity built-in model (no key needed) | Any supported provider via `.env` key |
| **Requires `.env`?** | No | Yes (at least one key) |
| **CLI trigger** | Default — just run `python main.py` | Detected automatically when a key is present in `.env` |
| **Format selection** | User tells the AntiGravity agent in chat (e.g. *"give me a PDF"* or *"I want LaTeX"*) | User picks from a numbered interactive CLI menu |
| **Available formats** | `.docx` · `.pdf` · `.tex` (LaTeX) · `all` | `.docx` · `.pdf` · `.tex` (LaTeX) · `all` |

> **Primary Flow**: When no API key is detected, the engine uses the AntiGravity SDK model. The user specifies the desired output format conversationally — e.g., *"generate my resume as a PDF"* or *"I want the LaTeX version"*. The agent parses intent via `parse_format_from_chat()` and sets `output_format` before running the pipeline.
>
> **Secondary Flow**: When any API key is found in `.env`, the engine uses that external provider. Before the pipeline runs, the CLI shows a numbered menu and the user selects `.docx`, `.pdf`, `.tex`, or `all`.

---

## 1. System Architecture Overview

```
                      ┌──────────────────────────────┐
                      │    Target Job Description    │
                      └──────────────┬───────────────┘
                                     │
                                     ▼
                   [ 1. JD Deconstruction & Leveler ]
                   • Explicit Stack (Languages, DBs, Infra)
                   • Implicit Scale (Throughput, Concurrency)
                   • Domain & Seniority Profile
                                     │
                                     ▼
                  [ 2. Archetype Mapping & Cohesion ]
                   • Category 1: Core Domain Engine
                   • Category 2: Distributed / Scale System
                   • Category 3: Developer Tooling / Infra
                                     │
                                     ▼
                   [ 3. Deep Spec & Trade-off Synth ]
                   • Concrete Architectural Bottlenecks
                   • Hardware-bound Realistic Metrics
                   • Technology Selection Trade-offs
                                     │
                                     ▼
                   [ 4. ATS & XYZ Bullet Generator ]
                   • Google XYZ Formula Formatting
                   • Active Engineering Power Verbs
                   • Front-loaded Keyword Placement
                                     │
                                     ▼
             ┌──────────────────────────────────────────────┐
             │    [ 5. Evaluator-Optimizer Critique Loop ]   │
             │    • Mathematical & Hardware Sanity Checks   │
             │    • ATS Keyword Coverage Scoring (>=85%)    │
             │    • Stack Contradiction Detection           │
             └──────────────────────┬───────────────────────┘
                                    │ (Pass / Self-Correct)
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
       [ 6. Interview Defense Dossier ]   [ 7. Resume Artifact Engine ]
       • "Why Not X" Architectural Trade-offs   • .docx Resume Output
       • Simulated Failure Modes & Fixes        • .pdf  Resume Output
       • 5 Probing Interview Questions & Answers • .tex  Resume Output (Jake's LaTeX)
                                                 • JSONResume Schema Output
                                                 • Markdown Summary
```

### 1.1 LLM Initialization Flow

```
                  ┌─────────────────────────────────┐
                  │         config.py starts         │
                  └───────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  Is any API key in .env?  │
                    └──────┬────────────┬────────┘
                          NO           YES
                           │            │
                           ▼            ▼
               ┌──────────────────┐  ┌────────────────────────┐
               │ AntiGravity SDK  │  │  External LLM Provider │
               │ (primary model)  │  │  (secondary model)     │
               └──────────────────┘  └────────────────────────┘
                           │            │
                           └─────┬──────┘
                                 ▼
                       Unified LLM interface
                     (same pipeline for both)
```

---

## 2. Complete Project Directory Structure

Below is the complete file tree that AntiGravity must scaffold:

```text
resume-engine/
│
├── rules.md                        # Strict agent governance, metric bounds & coding invariants
├── README.md                       # Project overview and CLI execution guide
├── pyproject.toml                  # Python package configuration & dependencies
├── requirements.txt                # Pinned pip dependencies
├── .env.example                    # Optional API keys — only needed for secondary mode
├── .gitignore                      # Ignores output/, .env, __pycache__, *.pyc
│
├── src/
│   ├── __init__.py
│   ├── config.py                   # LLM initialization: AntiGravity SDK (primary) or API key (secondary)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── models.py               # Pydantic v2 schemas for all state, inputs, and artifacts
│   │
│   ├── extractors/
│   │   ├── __init__.py
│   │   └── profile_extractor.py    # Extracts CandidateProfile from a resume PDF using pdfplumber + LLM
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── extraction_prompts.py   # JD deconstruction prompt templates
│   │   ├── synthesis_prompts.py    # Archetype & project generation prompt templates
│   │   ├── critique_prompts.py     # ATS density & sanity check critique prompts
│   │   └── dossier_prompts.py      # Interview defense Q&A prompt templates
│   │
│   ├── evaluators/
│   │   ├── __init__.py
│   │   ├── ats_scorer.py           # Algorithmic keyword coverage & density verification
│   │   └── sanity_checker.py       # Hardware-bound mathematical checks (RPS, latency, RAM)
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py                # LangGraph TypedDict state definition
│   │   ├── nodes.py                # Graph node implementations (parse, synthesize, eval, export)
│   │   └── graph.py                # StateGraph assembly, conditional routing, and compilation
│   │
│   └── renderers/
│       ├── __init__.py
│       ├── docx_renderer.py        # Renders resume as formatted .docx (python-docx)
│       ├── pdf_renderer.py         # Converts .docx → .pdf (docx2pdf / weasyprint fallback)
│       ├── latex_renderer.py       # Renders resume as Jake's Resume .tex (Jinja2)
│       └── dossier_renderer.py     # Markdown formatter for the Interview Defense Dossier
│
├── templates/
│   ├── resume_template.docx        # Base .docx template with styles (headings, bullets, fonts)
│   ├── jakes_resume.tex.jinja2     # Jinja2 template for ATS-optimized LaTeX resume
│   └── interview_dossier.md.jinja2 # Jinja2 template for technical interview cheat sheet
│
├── output/                         # All generated artifacts written here (git-ignored)
│   ├── candidate_profile.json      # Extracted & cached candidate profile (from PDF)
│   ├── resume.docx                 # Output — formatted Word document
│   ├── resume.pdf                  # Output — PDF version
│   ├── resume.tex                  # Output — LaTeX source (compile with pdflatex if needed)
│   ├── interview_defense_dossier.md
│   └── portfolio_data.json
│
├── tests/
│   ├── __init__.py
│   ├── test_evaluator.py           # Unit tests for ATS scoring & sanity checks
│   ├── test_renderers.py           # Unit tests for .docx, .pdf, and .tex generation
│   ├── test_profile_extractor.py   # Unit tests for PDF extraction & CandidateProfile parsing
│   └── test_pipeline.py            # End-to-end integration test with sample JD
│
└── main.py                         # CLI entrypoint — detects mode, handles format, runs pipeline
```

---

## 3. File-by-File Implementation Guide

### 3.1 `rules.md` (Workspace Operational Invariants)
This file must be created directly in the root directory to govern AntiGravity's autonomous decisions:

```markdown
# Agent Governance & Engineering Invariants

1. Role & Identity:
   - Act as a Principal Distributed Systems Architect and ATS Integrity Evaluator.
   - Zero hallucination policy: Every claim must map to sound, real-world architectural principles.
   - Always use the AntiGravity native model unless an external API key is explicitly configured.

2. The 3-Project Archetype Rule:
   - Project 1 (Core Domain Engine): Direct business domain and operational stack match for the JD.
   - Project 2 (High-Throughput / Distributed Systems): Demonstrates concurrency, queuing, cache consistency, and p99 latency optimization.
   - Project 3 (Developer Tooling / Infrastructure / MCP): Proves engineering maturity, internal leverage, and operational automation.

3. Metric & Hardware Plausibility Bounds:
   - Throughput (RPS) and latency claims must conform to realistic physical hardware bounds (e.g., no 100k RPS on a single SQLite instance; no sub-millisecond p99 latency across unindexed remote multi-tenant tables).
   - Require concrete engineering bottlenecks (e.g., connection pool exhaustion, N+1 query loops, GIL contention, Kafka consumer rebalancing lag) over vague phrases like "improved efficiency".
   - Compute reduction claims must stay between 20% and 60% (realistic enterprise ranges).

4. Bullet Point Constraints (Google XYZ Formula) & Strict 1-Page Layout:
   - Every bullet MUST follow: "Accomplished [X], as measured by [Y], by implementing [Z]".
   - Bullets must start with active engineering power verbs (Architected, Benchmarked, Partitioned, Engineered, Optimized).
   - Technical keywords must be front-loaded in the first 7 words of each bullet.
   - Strictly fit on ONE SINGLE PAGE: exactly 2 to 3 punchy, high-impact bullets per project.

5. Code Quality & Typing:
   - Use strict Pydantic v2 schemas for all node transitions.
   - All LangGraph nodes must be pure functions that take TypedDict `AgentState` and return updated keys.
   - No monolithic code: Keep schemas, evaluators, prompts, agents, and renderers in dedicated modules.

6. Output Format & Section Hierarchy:
   - Three formats are supported: `.docx` (Word), `.pdf`, and `.tex` (Jake's LaTeX). The `all` option generates all three.
   - Strict Section Order: (1) Header → (2) Professional Summary (dynamically tailored, 2-3 sentences) → (3) Experience (e.g. AI Intern at IFSO, Delhi Police) → (4) Technical Skills (swapped before projects) → (5) Technical Projects (3 projects) → (6) Education (swapped to bottom).
   - Primary mode (AntiGravity chat): format parsed from natural language. Secondary mode (API key): numbered CLI menu.
   - LaTeX output uses Jake's Resume Jinja2 template with tight margins and vspaces to guarantee a strict 1-page fit.
```

### 3.2 `src/config.py`
Handles LLM initialization for both modes. AntiGravity SDK is loaded first; external keys are only used if explicitly present.

```python
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env if present; silently no-ops if absent

def get_llm():
    """
    Primary: Use the AntiGravity built-in SDK model — no API key required.
    Secondary (fallback): If GEMINI_API_KEY or OPENAI_API_KEY is set in .env,
    initialize the corresponding LangChain chat model instead.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if gemini_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=gemini_key)

    if openai_key:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o", openai_api_key=openai_key)

    # Default: AntiGravity native SDK model
    from antigravity import AntiGravityLLM  # provided by the AntiGravity runtime
    return AntiGravityLLM()

def is_secondary_mode() -> bool:
    """Returns True if an external API key is present, triggering secondary mode."""
    return bool(os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY"))
```

### 3.3 `src/extractors/profile_extractor.py`

**Approach — Two-step PDF → Structured Profile:**

```
User provides resume PDF path
         │
         ▼
 Step 1: pdfplumber
 extracts raw text
 from all pages
         │
         ▼
 Step 2: LLM (same get_llm())
 parses text → CandidateProfile
 using with_structured_output()
         │
         ▼
 Saved to output/candidate_profile.json
 (cached — skipped on next run if file exists)
```

**Why this approach?**
- `pdfplumber` is pure Python, needs no external binary, and handles both single and multi-column resume layouts reliably
- The LLM structured-output step handles formatting noise (e.g., garbled Unicode from PDF fonts) that regex-based parsers would miss
- Caching avoids re-extracting on every run — user only pays the cost once

```python
import json
import os
import pdfplumber
from pathlib import Path
from src.config import get_llm
from src.schemas.models import CandidateProfile

CACHE_PATH = Path("output/candidate_profile.json")

def extract_profile_from_pdf(pdf_path: str) -> CandidateProfile:
    """
    Two-step extraction:
      1. pdfplumber  → raw text string
      2. LLM         → CandidateProfile (structured output)

    Extracted fields: full_name, title, phone, email,
                      linkedin, github, professional_objective, education
    """
    # Step 1 — PDF text extraction
    raw_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            raw_text += page.extract_text() or ""

    # Step 2 — LLM structured extraction
    llm = get_llm()
    structured_llm = llm.with_structured_output(CandidateProfile)
    prompt = (
        "Extract the candidate's personal information from the following resume text.\n"
        "Focus only on: full name, professional title/headline, phone, email, "
        "LinkedIn URL, GitHub URL, professional objective/summary, and education entries.\n"
        "Ignore all work experience, projects, and skills sections.\n\n"
        f"Resume text:\n{raw_text}"
    )
    profile: CandidateProfile = structured_llm.invoke(prompt)
    return profile

def load_or_extract_profile(pdf_path: str | None) -> CandidateProfile | None:
    """
    Main entry point called from main.py.

    - If output/candidate_profile.json exists → load from cache (no re-extraction)
    - If pdf_path provided             → extract and cache
    - If pdf_path is None              → return None (renderers use placeholder header)
    """
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return CandidateProfile(**json.load(f))

    if not pdf_path:
        return None

    profile = extract_profile_from_pdf(pdf_path)

    # Cache the result
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        f.write(profile.model_dump_json(indent=2))

    return profile
```

### 3.4 `src/schemas/models.py`
Defines the strict contracts between all pipeline stages:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

# ---------------------------------------------------------------------------
# Candidate Profile — extracted from the user's resume PDF
# ---------------------------------------------------------------------------

class EducationEntry(BaseModel):
    degree: str                  # e.g. "B.Tech — Artificial Intelligence & Machine Learning"
    institution: str             # e.g. "Vivekananda Institute of Professional Studies (VIPS), New Delhi"
    year_range: str              # e.g. "2024 – 2028 (Expected)"
    details: Optional[str] = None  # e.g. "2nd Year"

class ExperienceEntry(BaseModel):
    role: str                    # e.g. "AI Intern"
    organization: str            # e.g. "IFSO, Delhi Police"
    period: str                  # e.g. "June - August"
    location: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)

class CandidateProfile(BaseModel):
    """
    Extracted and enriched candidate profile.
    Example (Sahil Yadav):
      full_name        = "Sahil Yadav"
      title            = "AI Engineer · Agentic Systems & GenAI Backend Development"
      phone            = "+91 8700122453"
      email            = "sahillyaadav@gmail.com"
      linkedin         = "linkedin.com/in/sahil-yadav-1ab468249"
      github           = "github.com/Notso-sahil"
      objective        = "Full-Stack Engineer and B.Tech AIML student with hands-on production
                          experience building agentic AI systems..."
      education        = [EducationEntry(degree="B.Tech — Artificial Intelligence & Machine Learning",
                                         institution="VIPS, New Delhi",
                                         year_range="2024 – 2028 (Expected)",
                                         details="2nd Year")]
      experience       = [ExperienceEntry(role="AI Intern", organization="IFSO, Delhi Police", period="June - August")]
    """
    full_name: str
    title: str                           # professional headline from resume header
    phone: str
    email: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    professional_objective: str          # summary / objective paragraph from uploaded resume
    tailored_summary: Optional[str] = None  # dynamically synthesized summary blending background + JD
    education: List[EducationEntry]
    experience: List[ExperienceEntry] = Field(default_factory=list)

class JDDeconstruction(BaseModel):
    role_title: str
    seniority_level: str
    domain: str
    primary_languages: List[str]
    frameworks: List[str]
    databases_and_storage: List[str]
    infrastructure_and_cloud: List[str]
    core_engineering_challenges: List[str]
    target_keywords: List[str]

class ArchitecturalTradeOff(BaseModel):
    decision: str
    chosen_technology: str
    rejected_technology: str
    justification: str

class FailureModeAnalysis(BaseModel):
    scenario: str
    impact: str
    mitigation_strategy: str

class ProjectSpec(BaseModel):
    project_title: str
    archetype: str  # "Core Domain" | "Distributed Systems" | "DevTools / Infra"
    high_level_architecture: str
    tech_stack: List[str]
    core_bottleneck: str
    technical_solution: str
    quantified_impact_metrics: List[str]
    trade_offs: List[ArchitecturalTradeOff]
    failure_modes: List[FailureModeAnalysis]
    xyz_bullets: List[str]
    interview_defense_qna: List[Dict[str, str]]

class EvaluatorScore(BaseModel):
    ats_coverage_score: float = Field(description="Percentage between 0.0 and 100.0")
    metric_plausibility_score: float = Field(description="Score between 0.0 and 10.0")
    stack_cohesion_score: float = Field(description="Score between 0.0 and 10.0")
    passed_all_gates: bool
    critique_feedback: Optional[str] = None

class OutputFormat(BaseModel):
    format: Literal["docx", "pdf", "latex", "all"] = "all"
    # "docx"  → Word document only
    # "pdf"   → PDF only
    # "latex" → Jake's Resume .tex source only
    # "all"   → generate all three formats

class ResumeProjectPortfolio(BaseModel):
    jd_analysis: JDDeconstruction
    projects: List[ProjectSpec]
    evaluator_audit: EvaluatorScore
    docx_output_path: Optional[str] = None    # path to generated .docx
    pdf_output_path: Optional[str] = None     # path to generated .pdf
    latex_output_path: Optional[str] = None   # path to generated .tex (Jake's Resume)
    markdown_summary: str
    portfolio_json_path: Optional[str] = None
```

### 3.4 `src/agents/state.py`
Defines the shared memory state across the LangGraph state machine:

```python
from typing import TypedDict, List, Optional
from src.schemas.models import (
    JDDeconstruction, ProjectSpec, EvaluatorScore,
    OutputFormat, CandidateProfile
)

class AgentState(TypedDict):
    raw_jd: str
    output_format: OutputFormat          # "docx" | "pdf" | "latex" | "all"
    candidate_profile: Optional[CandidateProfile]  # extracted from resume PDF; used by all renderers
    jd_analysis: Optional[JDDeconstruction]
    candidate_projects: Optional[List[ProjectSpec]]
    evaluation_result: Optional[EvaluatorScore]
    iteration_count: int
    critique_history: List[str]
    final_docx_path: Optional[str]       # set if format is "docx" or "all"
    final_pdf_path: Optional[str]        # set if format is "pdf" or "all"
    final_latex_path: Optional[str]      # set if format is "latex" or "all"
    final_dossier: Optional[str]
```

### 3.5 `src/agents/nodes.py`
Implements the core step logic:
* `deconstruct_jd_node`: Calls the structured output LLM using `JDDeconstruction` schema.
* `synthesize_projects_node`: Generates the 3 project archetypes with deep architectural specs and XYZ bullets (incorporates `critique_history` if re-prompted).
* `evaluate_portfolio_node`: Executes hybrid deterministic ATS calculation (`ats_scorer.py`) and LLM plausibility audit (`sanity_checker.py`), setting `passed_all_gates: True/False`.
* `generate_artifacts_node`: Dispatches to `docx_renderer.py`, `pdf_renderer.py`, and/or `latex_renderer.py` depending on `state["output_format"]`. In primary mode the format is resolved from the user's chat instruction via `parse_format_from_chat()`; in secondary mode it comes from the numbered CLI menu.

### 3.6 `src/agents/graph.py`
Assembles the cyclical LangGraph workflow:

```python
from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.nodes import (
    deconstruct_jd_node,
    synthesize_projects_node,
    evaluate_portfolio_node,
    generate_artifacts_node
)

def route_evaluation(state: AgentState):
    eval_data = state.get("evaluation_result")
    if eval_data and eval_data.passed_all_gates:
        return "generate_artifacts"
    if state["iteration_count"] >= 3:
        return "generate_artifacts" # Cap iterations to prevent infinite loop
    return "synthesize_projects"

def create_resume_graph():
    builder = StateGraph(AgentState)
    builder.add_node("deconstruct_jd", deconstruct_jd_node)
    builder.add_node("synthesize_projects", synthesize_projects_node)
    builder.add_node("evaluate_portfolio", evaluate_portfolio_node)
    builder.add_node("generate_artifacts", generate_artifacts_node)

    builder.set_entry_point("deconstruct_jd")
    builder.add_edge("deconstruct_jd", "synthesize_projects")
    builder.add_edge("synthesize_projects", "evaluate_portfolio")
    builder.add_conditional_edges(
        "evaluate_portfolio",
        route_evaluation,
        {
            "generate_artifacts": "generate_artifacts",
            "synthesize_projects": "synthesize_projects"
        }
    )
    builder.add_edge("generate_artifacts", END)
    return builder.compile()
```

### 3.7 `src/evaluators/ats_scorer.py` & `sanity_checker.py`
* **`ats_scorer.py`**: Tokenizes extracted keywords from Stage 1 against the generated XYZ bullets. Calculates precision/recall coverage scores ($\ge 85\%$ required).
* **`sanity_checker.py`**: Scans numeric claims via regular expressions and LLM verification to catch absurd numbers (e.g., p99 latency < 1ms on network DB, 1M RPS on single-threaded workers).

### 3.8 `src/renderers/` — All Renderers
* **`docx_renderer.py`**: Uses `python-docx` to render verified project bullets, headings, and contact info into `output/resume.docx` using the base template `templates/resume_template.docx`.
* **`pdf_renderer.py`**: Converts the generated `.docx` to `output/resume.pdf`. Uses `docx2pdf` (Windows/macOS with Word) as the primary converter, falling back to `weasyprint` on Linux or when Word is unavailable.
* **`latex_renderer.py`**: Renders verified projects into Jake's Resume LaTeX format via the Jinja2 template `templates/jakes_resume.tex.jinja2`, producing `output/resume.tex`. Uses standard Jake's Resume macros (`\resumeSubheading`, `\resumeItemListStart`). The `.tex` source is the deliverable — users compile with `pdflatex` themselves if needed.
* **`dossier_renderer.py`**: Generates `output/interview_defense_dossier.md` covering:
  - Technical trade-offs ("Why X over Y?").
  - Simulated architecture disaster scenarios and mitigations.
  - Top 5 interview defense questions with scripted model answers.

### 3.9 `main.py`
CLI entrypoint. Handles mode detection, format selection (chat in primary / 4-option menu in secondary), pipeline execution, and output reporting.

#### Primary Mode — AntiGravity Chat
In primary mode the program opens a conversational loop. The user pastes the JD and states their format preference in plain language. The `parse_format_from_chat()` helper resolves intent. Example exchanges:

```
You: Here's the JD: [paste]
Agent: Got it. What format would you like for the resume?
You: Give me a PDF please.
Agent: ✓ Format set to: pdf. Running pipeline...
```

Or all in one message:

```
You: [paste JD] — generate me the LaTeX version
Agent: ✓ Format set to: latex. Running pipeline...
```

#### Secondary Mode — Numbered CLI Menu
When an external API key is detected, a numbered prompt appears before the pipeline runs:

```
Select output format:
  [1] .docx  — Microsoft Word document
  [2] .pdf   — PDF document
  [3] .tex   — Jake's Resume LaTeX source
  [4] all    — Generate all three formats
```

```python
"""
AntiGravity Resume Engine — CLI Entrypoint

Usage:
    python main.py                          # AntiGravity native (primary, chat-based format)
    python main.py --jd path/to/jd.txt     # pre-load JD; format still selected via chat/menu

Mode detection is automatic:
    - No API keys in .env  →  AntiGravity SDK (primary) — format from user chat
    - API key in .env      →  External LLM (secondary)  — format from numbered CLI menu
"""

import sys
from rich.console import Console
from rich.prompt import Prompt
from src.config import is_secondary_mode
from src.agents.graph import create_resume_graph
from src.schemas.models import OutputFormat
from src.extractors.profile_extractor import load_or_extract_profile

console = Console()

FORMAT_MENU = {
    "1": ("docx",  ".docx  — Microsoft Word document"),
    "2": ("pdf",   ".pdf   — PDF document"),
    "3": ("latex", ".tex   — Jake's Resume LaTeX source"),
    "4": ("all",   "all    — Generate all three formats"),
}

def select_output_format_cli() -> OutputFormat:
    """Numbered CLI menu — shown in secondary mode only."""
    console.print("\n[bold cyan]Select output format:[/bold cyan]")
    for key, (_, label) in FORMAT_MENU.items():
        console.print(f"  [{key}] {label}")
    console.print()
    choice = Prompt.ask("Enter choice", choices=list(FORMAT_MENU.keys()), default="4")
    fmt, _ = FORMAT_MENU[choice]
    return OutputFormat(format=fmt)

def parse_format_from_chat(user_message: str) -> OutputFormat:
    """
    Primary mode helper — parses the user's natural-language format preference.
    Defaults to 'all' when no explicit format is mentioned.
    """
    msg = user_message.lower()
    if "latex" in msg or ".tex" in msg:
        return OutputFormat(format="latex")
    if "pdf" in msg:
        return OutputFormat(format="pdf")
    if "word" in msg or "docx" in msg or ".doc" in msg:
        return OutputFormat(format="docx")
    return OutputFormat(format="all")  # default when unspecified

def main():
    console.rule("[bold green]AntiGravity Resume Engine[/bold green]")

    # --- Step 0: Load candidate profile from resume PDF ---
    console.print("\n[bold]Step 1 of 3:[/bold] Candidate Profile")
    console.print("[yellow]Provide the path to your resume PDF (press Enter to skip):[/yellow]")
    pdf_path = input("> ").strip() or None
    candidate_profile = load_or_extract_profile(pdf_path)
    if candidate_profile:
        console.print(f"[green]✓ Profile loaded:[/green] {candidate_profile.full_name} · {candidate_profile.email}")
    else:
        console.print("[dim]⚠ No profile provided — resume header will use placeholder text.[/dim]")

    # --- Step 1: Read JD ---
    console.print("\n[bold]Step 2 of 3:[/bold] Job Description")
    if len(sys.argv) > 2 and sys.argv[1] == "--jd":
        with open(sys.argv[2]) as f:
            raw_jd = f.read()
    else:
        console.print("[yellow]Paste your Job Description below. Press Enter twice when done:[/yellow]")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        raw_jd = "\n".join(lines)

    # --- Step 2: Determine output format ---
    console.print("\n[bold]Step 3 of 3:[/bold] Output Format")
    if is_secondary_mode():
        console.print("[bold yellow]⚠ External API key detected — Secondary Mode.[/bold yellow]")
        output_format = select_output_format_cli()
    else:
        console.print("[bold green]✓ AntiGravity native model — Primary Mode.[/bold green]")
        console.print("[cyan]What format would you like? (docx / pdf / latex / all)[/cyan]")
        user_format_msg = input("> ").strip()
        output_format = parse_format_from_chat(user_format_msg)
        console.print(f"[green]✓ Format set to:[/green] {output_format.format}")

    # --- Run pipeline ---
    console.rule("[dim]Running pipeline...[/dim]")
    graph = create_resume_graph()
    final_state = graph.invoke({
        "raw_jd": raw_jd,
        "output_format": output_format,
        "candidate_profile": candidate_profile,
        "iteration_count": 0,
        "critique_history": [],
    })

    # --- Report outputs ---
    console.rule("[bold green]Pipeline Complete[/bold green]")
    if candidate_profile:
        console.print(f"[green]✓ Profile cache:[/green]     output/candidate_profile.json")
    if final_state.get("final_docx_path"):
        console.print(f"[green]✓ Resume (.docx):[/green]    {final_state['final_docx_path']}")
    if final_state.get("final_pdf_path"):
        console.print(f"[green]✓ Resume (.pdf):[/green]     {final_state['final_pdf_path']}")
    if final_state.get("final_latex_path"):
        console.print(f"[green]✓ Resume (.tex):[/green]     {final_state['final_latex_path']}")
    console.print(f"[green]✓ Interview Dossier:[/green] output/interview_defense_dossier.md")
    console.print(f"[green]✓ Portfolio JSON:[/green]    output/portfolio_data.json")

if __name__ == "__main__":
    main()
```

---

## 4. Dependencies (`requirements.txt`)

```text
# Core agentic framework
langgraph>=0.2.0
langchain>=0.2.0

# AntiGravity SDK (primary model — always required)
antigravity>=1.0.0

# Secondary model providers (optional — only needed if using API keys)
langchain-google-genai>=1.0.0
langchain-openai>=0.1.0

# Schema & validation
pydantic>=2.7.0

# Templating
jinja2>=3.1.0

# PDF resume input — candidate profile extraction
pdfplumber>=0.11.0       # pure-Python PDF text extraction (no external binary needed)

# Output rendering — .docx, .pdf, and .tex (LaTeX)
python-docx>=1.1.0
docx2pdf>=0.1.8          # primary PDF converter (uses MS Word on Windows/macOS)
weasyprint>=62.0         # fallback PDF converter (Linux / no-Word environments)
# Note: LaTeX output (.tex) is rendered via Jinja2 — no additional pip dependency.
# Users who want to compile .tex → .pdf themselves need pdflatex (MiKTeX / TeX Live).

# Environment & CLI
python-dotenv>=1.0.0
rich>=13.7.0
```

---

## 5. `.env.example`

```dotenv
# ============================================================
# AntiGravity Resume Engine — Environment Configuration
# ============================================================
#
# PRIMARY MODE (default): No keys needed.
# The engine uses the AntiGravity native model automatically.
#
# SECONDARY MODE (optional): Set ONE of the keys below to use
# an external LLM provider instead.
# ============================================================

# Option A: Google Gemini
# GEMINI_API_KEY=your_gemini_api_key_here

# Option B: OpenAI
# OPENAI_API_KEY=your_openai_api_key_here
```

---

## 6. Gap Analysis & Fixes Applied

The following gaps were identified in the original spec and have been addressed in this revision:

| # | Gap | Fix Applied |
|---|-----|-------------|
| 1 | No AntiGravity-native LLM path — only third-party keys | Added Section 0 (Execution Modes), `config.py` with `get_llm()` defaulting to `AntiGravityLLM()` |
| 2 | Output was LaTeX-only; no `.docx` or `.pdf` | Added `docx_renderer.py` + `pdf_renderer.py` alongside restored `latex_renderer.py`; all three formats now supported |
| 3 | No format selection mechanism | Secondary: 4-option numbered CLI menu (`select_output_format_cli()`); Primary: `parse_format_from_chat()` parses user's natural-language chat instruction |
| 4 | `main.py` spec was vague — no interactive flow described | Full `main.py` code with chat-based format parsing (primary) and numbered 4-option menu (secondary) |
| 5 | `AgentState` had no `output_format` field | Added `output_format: OutputFormat` to `state.py` |
| 6 | `ResumeProjectPortfolio` had `latex_resume_code` as a raw string | Replaced with `docx_output_path`, `pdf_output_path`, `latex_output_path` (file paths) |
| 7 | `.env.example` didn't distinguish optional vs required | Rewritten with clear primary/secondary commentary |
| 8 | `output/` directory missing from file tree | Added with `resume.docx`, `resume.pdf`, `resume.tex`, dossier, and JSON |
| 9 | No renderer unit tests | Added `tests/test_renderers.py` covering `.docx`, `.pdf`, and `.tex` generation |
| 10 | Architecture diagram (Step 7) listed only LaTeX | Expanded to show `.docx`, `.pdf`, `.tex`, JSON, and Markdown outputs |
| 11 | `antigravity` SDK dependency missing | Added `antigravity>=1.0.0` as a core (non-optional) dependency |
| 12 | `config.py` spec had no implementation logic | Added full `get_llm()` and `is_secondary_mode()` with AntiGravity-first fallback chain |
| 13 | `rules.md` didn't cover output format | Added Rule 6 describing three formats and the chat vs. CLI selection mechanism |
| 14 | `nodes.py` didn't mention output format awareness | Updated `generate_artifacts_node` to dispatch to the correct renderer(s) based on `output_format` |
| 15 | LaTeX was dropped entirely (regression in previous revision) | **Restored** `latex_renderer.py`, `jakes_resume.tex.jinja2`, `output/resume.tex`, and `OutputFormat.latex` |
| 16 | Primary mode had no format input mechanism | Added `parse_format_from_chat()` — keyword-matching helper that resolves format from the user's chat message |
| 17 | No candidate personal info (name, contact, education, objective) input path | Added `src/extractors/profile_extractor.py` — two-step `pdfplumber` + LLM extraction into `CandidateProfile` schema; cached to `output/candidate_profile.json`; integrated into `AgentState` and all renderers |
| 18 | `.gitignore` missing from project root | Added to directory structure, ignoring `output/`, `.env`, `__pycache__`, `*.pyc` |