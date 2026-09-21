import re


# Common technical skills
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "React.js",
    "Node.js",
    "Express",
    "Flask",
    "Django",
    "FastAPI",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Natural Language Processing",
    "Data Science",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "REST API",
    "REST APIs",
    "Tailwind",
    "Bootstrap",
    "Linux",
    "Figma",
]


def normalize_text(text):
    """
    Convert text to lowercase and remove
    unnecessary special characters.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\s-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def detect_skills(text):
    """
    Detect technical skills from text.
    """

    normalized_text = normalize_text(text)

    detected = []

    for skill in SKILLS:

        skill_normalized = normalize_text(skill)

        pattern = r"\b" + re.escape(
            skill_normalized
        ) + r"\b"

        if re.search(
            pattern,
            normalized_text
        ):

            if skill not in detected:
                detected.append(skill)

    return detected


def calculate_match_percentage(
    resume_skills,
    job_skills
):
    """
    Calculate percentage of job skills
    found in the resume.
    """

    if not job_skills:
        return 0

    resume_set = {
        normalize_text(skill)
        for skill in resume_skills
    }

    job_set = {
        normalize_text(skill)
        for skill in job_skills
    }

    matched = resume_set.intersection(
        job_set
    )

    percentage = (
        len(matched) /
        len(job_set)
    ) * 100

    return round(
        percentage,
        2
    )


def analyze_job_match(
    resume_text,
    job_description
):
    """
    Compare resume with a job description.

    Returns:
    - Resume skills
    - Job skills
    - Matching skills
    - Missing skills
    - Match percentage
    """

    resume_skills = detect_skills(
        resume_text
    )

    job_skills = detect_skills(
        job_description
    )

    resume_normalized = {
        normalize_text(skill): skill
        for skill in resume_skills
    }

    job_normalized = {
        normalize_text(skill): skill
        for skill in job_skills
    }

    matched_skills = []

    missing_skills = []

    for normalized, original in job_normalized.items():

        if normalized in resume_normalized:

            matched_skills.append(
                original
            )

        else:

            missing_skills.append(
                original
            )

    match_percentage = calculate_match_percentage(
        resume_skills,
        job_skills
    )

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }