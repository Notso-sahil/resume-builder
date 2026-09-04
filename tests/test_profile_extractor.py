from pathlib import Path
from src.extractors.profile_extractor import (
    extract_profile_from_pdf,
    load_or_extract_profile,
    parse_profile_deterministic,
    find_candidate_resumes,
)
from src.schemas.models import CandidateProfile


def test_parse_profile_deterministic_no_hardcoded_leak():
    sample_text = (
        "ALEX RIVERA\n"
        "Lead Distributed Systems Architect\n"
        "+1 (555) 234-5678 | alex.rivera@example.com | linkedin.com/in/alex-rivera | github.com/arivera\n"
        "PROFESSIONAL OBJECTIVE\n"
        "Seasoned systems architect specializing in high-throughput event streaming and distributed consensus.\n"
        "EDUCATION\n"
        "M.S. in Computer Science  2018 – 2020\n"
        "Cornell University · Magna Cum Laude\n"
    )
    profile = parse_profile_deterministic(sample_text)
    assert profile.full_name == "ALEX RIVERA"
    assert profile.title == "Lead Distributed Systems Architect"
    assert "alex.rivera@example.com" in profile.email
    assert len(profile.education) > 0
    assert "Cornell" in profile.education[0].institution
    # Ensure no Sahil or IFSO leaks into generic profiles
    assert "sahil" not in profile.full_name.lower()
    for exp in profile.experience:
        assert "delhi police" not in exp.organization.lower()


def test_find_candidate_resumes(tmp_path):
    # Setup test PDFs in tmp_path
    (tmp_path / "my_resume.pdf").write_text("%PDF-1.4 dummy")
    (tmp_path / "other_doc.txt").write_text("dummy")

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "generated_resume.pdf").write_text("%PDF-1.4 dummy")

    found = find_candidate_resumes(tmp_path)
    assert len(found) == 1
    assert found[0].name == "my_resume.pdf"


def test_extract_profile_from_resume_pdf():
    # If a workspace resume PDF exists, verify extraction
    pdfs = find_candidate_resumes()
    if not pdfs:
        return

    profile = extract_profile_from_pdf(pdfs[0])
    assert isinstance(profile, CandidateProfile)
    assert len(profile.full_name) > 0
    assert "@" in profile.email
