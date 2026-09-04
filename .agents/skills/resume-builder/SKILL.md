---
name: resume-builder
description: Generates high-impact ATS-optimized resumes and interview defense dossiers for any target job description using the AntiGravity Resume Engine.
---

# Resume Builder Skill

Use this skill when the user provides a Job Description (JD) or asks to generate a tailored resume for a specific role or company.

## Token-Efficient Execution Instructions

**DO NOT read or explore files in `src/`, `templates/`, or `tests/`.**

Follow these 2 simple steps:

1. **Create Job Config**:
   Create a JSON file at `jobs/<company_slug>.json` containing:
   - `company_name`: string
   - `role_title`: string
   - `seniority_level`: string
   - `domain`: string
   - `primary_languages`: list of strings
   - `frameworks`: list of strings
   - `databases_and_storage`: list of strings
   - `infrastructure_and_cloud`: list of strings
   - `core_engineering_challenges`: list of strings
   - `target_keywords`: list of high-priority ATS keywords
   - `tailored_summary_override`: 2-3 sentence tailored summary (or null)
   - `fallback_projects`: null (engine synthesizes 3 archetypes automatically)

2. **Execute Engine**:
   Run the terminal command:
   ```bash
   python main.py --job <company_slug>
   ```
   (Outputs will be in `output/<company_slug>_resume.pdf` and `output/<company_slug>_ques.md`.)
