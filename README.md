# AntiGravity Autonomous Resume Engine

An intelligent, multi-stage agentic engine that deconstructs technical Job Descriptions (JDs), synthesizes architecturally sound engineering projects across 3 complementary archetypes, rigorously optimizes ATS-targeted resume bullets using the Google XYZ formula, self-audits metric plausibility, and produces an **Interview Defense Dossier** with ready-to-export resumes in `.pdf`, `.docx`, or **LaTeX** (`.tex`) format.

---

## Features

- **Smart Candidate Profile**: Automatically extracts and caches candidate contact details, objective, education, and experience from your resume PDF. Subsequent runs load instantly from cache.
- **External Job Configs (`jobs/`)**: Define company targets in clean JSON configs without modifying engine source code.
- **JD Deconstruction**: Extracts core technical stack, domain, implicit scale, and targeted ATS keywords.
- **3-Archetype Project Synthesis**:
  1. *Core Domain Engine* (business domain match)
  2. *Distributed Systems / Scale Engine* (concurrency, queuing, caching, p99 latency)
  3. *Developer Tooling / Infra / MCP* (internal leverage, developer productivity)
- **Evaluator-Optimizer Critique Loop**: Strict mathematical and hardware sanity checks, plus algorithmic ATS keyword coverage (>= 85% required).
- **Single-Format Clean Generation**: Defaults to PDF silently or generates Word (`.docx`) / Jake's Resume LaTeX (`.tex`) on request.
- **Non-Destructive Archival**: Automatically archives past generations to `output/old/` without overwriting or deleting historical files.
- **Interview Defense Dossier**: Generates "Why Not X" architectural trade-offs, failure mode analyses, and 5 probing interview questions with model answers.

---

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Add Your Resume

Place your resume PDF in the project root. On first run, it will extract and cache your profile to `output/candidate_profile.json`.

### 3. Run the Pipeline

```bash
# Default interactive mode (prompts for job selection, defaults to PDF)
python main.py

# Non-interactive generation for a pre-configured company
python main.py --job naive

# Specify a custom format
python main.py --job naive --format docx
python main.py --job pindrop --format latex

# Custom JD text file
python main.py --jd path/to/jd.txt
```

### 4. Generated Artifacts

Outputs are saved in the `output/` directory:
- `output/<company>_resume.pdf` — Tailored resume (PDF default)
- `output/<company>_ques.md` — Interview Defense Dossier (trade-offs, failure modes, Q&A)
- `output/candidate_profile.json` — Cached candidate profile
- `output/portfolio_data.json` — Full structured JSON payload
- `output/old/` — Historical resumes and dossiers from previous runs

---

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```
