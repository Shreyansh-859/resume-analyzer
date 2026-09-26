import os
from resume.pdf_extractor import extract_text_from_pdf

from resume.resume_analyzer import (
    analyze_resume,
    generate_recommendations
)

from resume.skill_extractor import (
    extract_skills,
    SKILLS
)

from resume.job_matcher import (
    analyze_job_match
)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "test_files", "sample_resume.pdf")

resume_text = extract_text_from_pdf(
    pdf_path
)


# ---------------------------------------
# RESUME ANALYSIS
# ---------------------------------------

resume_data = analyze_resume(
    resume_text
)


# ---------------------------------------
# SKILLS
# ---------------------------------------

resume_skills = extract_skills(
    resume_text
)


# ---------------------------------------
# SAMPLE JOB DESCRIPTION
# ---------------------------------------

job_description = """
We are looking for a Software Developer
with experience in Python, JavaScript,
React.js, FastAPI, SQL, Machine Learning,
Git, GitHub and PostgreSQL.

The candidate should understand REST APIs,
software development and database management.
"""


# ---------------------------------------
# JOB MATCHING
# ---------------------------------------

match_result = analyze_job_match(
    resume_text,
    resume_skills,
    job_description,
    SKILLS
)


# ---------------------------------------
# RECOMMENDATIONS
# ---------------------------------------

recommendations = generate_recommendations(
    resume_data,
    resume_skills,
    match_result["missing_skills"]
)


# ---------------------------------------
# DISPLAY
# ---------------------------------------

print("\n========================================")
print("AI RESUME ANALYZER")
print("RECOMMENDATIONS")
print("========================================")


for number, recommendation in enumerate(
    recommendations,
    start=1
):

    print(
        f"{number}. {recommendation}"
    )