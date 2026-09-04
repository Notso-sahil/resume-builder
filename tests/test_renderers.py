import tempfile
from pathlib import Path
from src.schemas.models import (
    ResumeProjectPortfolio,
    CandidateProfile,
    EducationEntry,
    JDDeconstruction,
    EvaluatorScore,
    ProjectSpec,
)
from src.prompts.synthesis_prompts import fallback_synthesize
from src.renderers.docx_renderer import render_docx
from src.renderers.latex_renderer import render_latex
from src.renderers.dossier_renderer import render_dossier


def get_test_portfolio():
    candidate = CandidateProfile(
        full_name="Sahil Yadav",
        title="AI Engineer",
        phone="+91 8700122453",
        email="sahillyaadav@gmail.com",
        linkedin="linkedin.com/in/sahil-yadav-1ab468249",
        github="github.com/Notso-sahil",
        professional_objective="Passionate AI Engineer building agentic systems.",
        education=[
            EducationEntry(
                degree="B.Tech - Artificial Intelligence",
                institution="VIPS, New Delhi",
                year_range="2024 - 2028",
            )
        ],
    )
    jd_analysis = fallback_synthesize("", JDDeconstruction)
    projects = fallback_synthesize("", ProjectSpec)
    eval_audit = EvaluatorScore(
        ats_coverage_score=94.0,
        metric_plausibility_score=9.2,
        stack_cohesion_score=9.5,
        passed_all_gates=True,
    )
    portfolio = ResumeProjectPortfolio(
        jd_analysis=jd_analysis,
        projects=projects,
        evaluator_audit=eval_audit,
        candidate_profile=candidate,
        markdown_summary="Test portfolio",
    )
    return portfolio, candidate


def test_render_docx():
    portfolio, candidate = get_test_portfolio()
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = Path(tmpdir) / "test_resume.docx"
        res = render_docx(portfolio, candidate, out_file)
        assert res.exists()
        assert res.stat().st_size > 1000


def test_render_latex():
    portfolio, candidate = get_test_portfolio()
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = Path(tmpdir) / "test_resume.tex"
        res = render_latex(portfolio, candidate, out_file)
        assert res.exists()
        with open(res, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Sahil Yadav" in content
            assert "Synapse" in content
            assert r"\resumeSubheading" in content


def test_render_dossier():
    portfolio, _ = get_test_portfolio()
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = Path(tmpdir) / "test_dossier.md"
        res = render_dossier(portfolio, out_file)
        assert res.exists()
        with open(res, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Technical Interview Defense Dossier" in content
            assert "Architectural Trade-offs" in content
            assert "5 Probing Interview Questions" in content
