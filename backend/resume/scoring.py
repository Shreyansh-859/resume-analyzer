import re


# ============================================================
# PROJECT DETECTION
# ============================================================

def extract_project_titles(projects):
    """
    Extract actual project names from the PROJECTS section.

    GitHub links, URLs, dates, bullet descriptions and
    section headings are NOT counted as projects.
    """

    if not projects:
        return []

    lines = [
        line.strip()
        for line in projects.split("\n")
        if line.strip()
    ]

    project_titles = []

    for line in lines:

        # ----------------------------------------------------
        # Ignore URLs / GitHub links
        # ----------------------------------------------------

        if re.search(
            r"(https?://|www\.|github\.com|linkedin\.com)",
            line,
            re.IGNORECASE
        ):
            continue

        # ----------------------------------------------------
        # Ignore section headings
        # ----------------------------------------------------

        normalized = line.lower().strip()

        ignored_headings = {
            "projects",
            "project",
            "project experience",
            "project experiences",
            "academic projects",
            "academic project",
            "personal projects",
            "personal project",
            "technical projects",
            "software projects",
        }

        if normalized in ignored_headings:
            continue

        # ----------------------------------------------------
        # Ignore education accidentally captured
        # ----------------------------------------------------

        education_words = [
            "education",
            "bachelor",
            "b.tech",
            "b.e.",
            "b.e",
            "degree",
            "university",
            "college",
            "school",
            "higher secondary",
            "hsc",
            "ssc",
            "cgpa",
            "semester",
            "percentage",
            "board",
        ]

        if any(
            word in normalized
            for word in education_words
        ):
            continue

        # ----------------------------------------------------
        # Ignore obvious dates
        # ----------------------------------------------------

        if re.fullmatch(
            r"[\d\s\-–—/|.]+",
            line
        ):
            continue

        # ----------------------------------------------------
        # Ignore lines that are clearly descriptions
        # ----------------------------------------------------

        description_starts = (
            "developed ",
            "built ",
            "created ",
            "designed ",
            "implemented ",
            "engineered ",
            "worked ",
            "used ",
            "using ",
            "integrated ",
            "leveraged ",
            "added ",
            "tested ",
            "implemented ",
            "participated ",
            "responsible ",
        )

        if normalized.startswith(
            description_starts
        ):
            continue

        # ----------------------------------------------------
        # Ignore bullet points
        # ----------------------------------------------------

        if line.startswith(
            ("•", "-", "–", "*")
        ):
            continue

        # ----------------------------------------------------
        # Ignore long sentences
        # ----------------------------------------------------

        if len(line.split()) > 10:
            continue

        # ----------------------------------------------------
        # Ignore description continuations / full sentences
        # ----------------------------------------------------

        if re.match(r"^[a-z]", line) or line.endswith("."):
            continue

        # ----------------------------------------------------
        # Ignore contact information
        # ----------------------------------------------------

        if "@" in line:
            continue

        if re.search(
            r"\+?\d[\d\s().-]{8,}",
            line
        ):
            continue

        # ----------------------------------------------------
        # Ignore location lines
        # ----------------------------------------------------

        locations = [
            "mumbai",
            "maharashtra",
            "india",
            "thane",
            "pune",
            "delhi",
            "bengaluru",
            "bangalore",
            "navi-mumbai",
        ]

        if any(
            location == normalized
            for location in locations
        ):
            continue

        # ----------------------------------------------------
        # Ignore generic information lines
        # ----------------------------------------------------

        if normalized.startswith(
            (
                "github link",
                "linkedin",
                "portfolio",
                "languages:",
                "interests:",
                "leadership",
                "soft skills:",
                "technical skills:",
            )
        ):
            continue

        # ----------------------------------------------------
        # Clean project title
        # ----------------------------------------------------

        title = re.sub(
            r"\s*\|\s*.*$",
            "",
            line
        ).strip()

        title = re.sub(
            r"\s+(live|github|demo)$",
            "",
            title,
            flags=re.IGNORECASE
        ).strip()

        if not title:
            continue

        # ----------------------------------------------------
        # Avoid duplicate projects
        # ----------------------------------------------------

        title_key = title.lower()

        if title_key not in {
            item.lower()
            for item in project_titles
        }:

            project_titles.append(title)

    return project_titles


# ============================================================
# SKILL SCORE
# ============================================================

def calculate_skill_score(skills):
    """
    Calculate the skill component of the resume score.

    Maximum = 30 points.
    """

    if not isinstance(skills, list):
        skills = []

    number_of_skills = len(skills)

    # 10 or more skills receive the full score.
    score = min(
        number_of_skills / 10,
        1
    ) * 30

    return round(score, 2)


# ============================================================
# EDUCATION SCORE
# ============================================================

def calculate_education_score(education):
    """
    Calculate education component.

    Maximum = 15 points.
    """

    if not education:
        return 0

    return 15


# ============================================================
# EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(experience):
    """
    Calculate experience component.

    Maximum = 20 points.
    """

    if not experience:
        return 0

    return 20


# ============================================================
# PROJECT SCORE
# ============================================================

def calculate_project_score(projects):
    """
    Calculate project component.

    Maximum = 15 points.

    Actual project titles are counted instead of simply
    counting every line in the PROJECTS section.
    """

    project_titles = extract_project_titles(
        projects
    )

    number_of_projects = len(
        project_titles
    )

    if number_of_projects == 0:
        return 0

    # --------------------------------------------------------
    # Project scoring
    # --------------------------------------------------------

    if number_of_projects >= 3:
        return 15

    return 10


# ============================================================
# CERTIFICATION SCORE
# ============================================================

def calculate_certification_score(certifications):
    """
    Calculate certification component.

    Maximum = 10 points.
    """

    if not certifications:
        return 0

    return 10


# ============================================================
# COMPLETENESS SCORE
# ============================================================

def calculate_completeness_score(
    resume_data
):
    """
    Calculate resume completeness.

    Maximum = 10 points.
    """

    important_fields = [
        "name",
        "email",
        "phone",
        "education",
        "skills",
        "projects",
        "experience",
        "certifications"
    ]

    completed = 0

    for field in important_fields:

        value = resume_data.get(
            field
        )

        if value:
            completed += 1

    score = (
        completed
        / len(important_fields)
    ) * 10

    return round(
        score,
        2
    )


# ============================================================
# COMPLETE RESUME SCORE
# ============================================================

def calculate_resume_score(
    resume_data,
    skills
):
    """
    Calculate the complete resume score.

    Maximum = 100 points.
    """

    # --------------------------------------------------------
    # Individual scores
    # --------------------------------------------------------

    skill_score = calculate_skill_score(
        skills
    )

    education_score = calculate_education_score(
        resume_data.get(
            "education",
            ""
        )
    )

    experience_score = calculate_experience_score(
        resume_data.get(
            "experience",
            ""
        )
    )

    project_text = resume_data.get(
        "projects",
        ""
    )

    project_titles = extract_project_titles(
        project_text
    )

    project_count = len(
        project_titles
    )

    project_score = calculate_project_score(
        project_text
    )

    certification_score = calculate_certification_score(
        resume_data.get(
            "certifications",
            ""
        )
    )

    completeness_score = calculate_completeness_score(
        resume_data
    )

    # --------------------------------------------------------
    # Total score
    # --------------------------------------------------------

    total_score = (
        skill_score
        + education_score
        + experience_score
        + project_score
        + certification_score
        + completeness_score
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "skills": skill_score,
        "education": education_score,
        "experience": experience_score,
        "projects": project_score,
        "project_count": project_count,
        "project_titles": project_titles,
        "certifications": certification_score,
        "completeness": completeness_score,
        "total": round(
            total_score,
            2
        )
    }