# AntiGravity Resume Engine — Agent Directives & Operational Guide

> [!IMPORTANT]
> **TOKEN-SAVER DIRECTIVE FOR AGENTS:**
> **DO NOT scan, grep, list, or view source files in `src/`, `templates/`, or `tests/`.**
> The engine is 100% complete, fully implemented, and automated. Reading the codebase wastes tokens.
> When a user asks you to generate a resume or target a job, follow the strict 2-step protocol below.

---

## The 2-Step Protocol for Generating a Resume

### Step 1: Create the Job Config File (`jobs/<company>.json`)
When the user provides a Job Description (JD) or company name:
1. Deconstruct the JD into: role title, company name, domain, stack keywords (languages, frameworks, DBs, cloud/tools).
2. Synthesize or identify 3 project archetypes targeting the role.
3. Write `jobs/<company_slug>.json` using this exact schema:

```json
{
  "company_name": "Target Company",
  "role_title": "AI Platform Engineer",
  "seniority_level": "Senior",
  "domain": "Autonomous AI Agents & Distributed Systems",
  "primary_languages": ["Python", "C++", "CUDA"],
  "frameworks": ["PyTorch", "vLLM", "LangGraph", "FastAPI"],
  "databases_and_storage": ["Redis", "PostgreSQL", "Kafka", "Qdrant"],
  "infrastructure_and_cloud": ["Docker", "Kubernetes", "AWS Cloud GPUs", "Triton"],
  "core_engineering_challenges": [
    "High-throughput vector indexing and sub-10ms similarity search under concurrent load",
    "Optimizing KV-cache footprint and speculative decoding for multi-agent loops"
  ],
  "target_keywords": [
    "Python", "PyTorch", "vLLM", "LangGraph", "CUDA", "FastAPI", "Docker", "RAG",
    "Speculative Decoding", "Continuous Batching", "KV-Cache", "Distributed Systems"
  ],
  "tailored_summary_override": "High-impact 2-3 sentence tailored summary blending candidate background with the target role.",
  "fallback_projects": null
}
```
*(Note: `fallback_projects` can be `null` — the engine automatically synthesizes the 3 archetypes and XYZ bullets using the keywords and domain).*

### Step 2: Execute the Pipeline via Terminal
Run the command directly using your shell/command execution tool:

```bash
# Default: generates high-quality PDF resume
python main.py --job <company_slug>

# Or if the user explicitly requested another format:
python main.py --job <company_slug> --format docx
python main.py --job <company_slug> --format latex
```

---

## Generated Outputs Location

The engine automatically writes clean outputs to the `output/` folder:
- Resume: `output/<company_slug>_resume.pdf` (or `.docx` / `.tex`)
- Interview Prep Dossier: `output/<company_slug>_ques.md`
- Cached Profile: `output/candidate_profile.json`
- Historical Generations: cleanly archived in `output/old/`

Report the generated file paths directly to the user when finished.

---

## Agent Invariants (Strict Rules)

1. **Zero Source Code Modifications**: NEVER edit or mutate files in `src/`, `templates/`, or root (`main.py`, `config.py`, etc.). Resumes are configured **exclusively via `jobs/<company>.json`**.
2. **Do Not Prompt for Format**: Always default to PDF silently unless the user explicitly requested docx or latex.
3. **Candidate Resume Missing**: If the user has not placed a resume PDF in the root directory and `output/candidate_profile.json` does not exist, instruct the user to copy their resume PDF into the root directory.
