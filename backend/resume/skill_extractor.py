import re


# ============================================================
# TECHNICAL SKILLS
# ============================================================

TECHNICAL_SKILLS = [
    "Python",
    "Java",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "Kotlin",
    "Swift",
    "Go",
    "Rust",
    "PHP",
    "Ruby",
    "Dart",
    "MATLAB",

    "HTML",
    "CSS",
    "Bootstrap",
    "Tailwind",
    "Tailwind CSS",
    "React",
    "React.js",
    "Next.js",
    "Vue",
    "Vue.js",
    "Angular",
    "Node.js",
    "Express",
    "Express.js",

    "FastAPI",
    "Flask",
    "Django",
    "Spring",
    "Spring Boot",
    "Laravel",
    ".NET",
    "ASP.NET",

    "SQL",
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "MongoDB",
    "Redis",
    "Firebase",
    "Supabase",
    "Oracle",

    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "Data Science",
    "Data Analytics",
    "Generative AI",

    "Pandas",
    "NumPy",
    "SciPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "OpenCV",

    "Linear Regression",
    "Logistic Regression",
    "Decision Tree",
    "Random Forest",
    "Naive Bayes",
    "K-Means",
    "KMeans",
    "SVM",
    "Support Vector Machine",
    "PCA",
    "Principal Component Analysis",

    "REST API",
    "REST APIs",
    "REST",
    "GraphQL",
    "WebSocket",
    "WebSockets",
    "JWT",

    "AWS",
    "Amazon Web Services",
    "Azure",
    "Microsoft Azure",
    "Google Cloud",
    "GCP",

    "Docker",
    "Kubernetes",
    "Jenkins",

    "Git",
    "GitHub",
    "GitLab",
    "Postman",
    "VS Code",
    "Visual Studio",
    "Figma",
    "Jupyter",
    "Jupyter Notebook",

    "Linux",
    "Unix",
    "Windows",
    "macOS",

    "Vercel",
    "IBM Watson",
    "SQLAlchemy",
    "Alembic",
    "Vite",
]


# ============================================================
# SOFT SKILLS
# ============================================================

SOFT_SKILLS = [
    "Communication",
    "Communication Skills",
    "Written Communication",
    "Verbal Communication",

    "Leadership",
    "Leadership Skills",
    "Team Leadership",

    "Teamwork",
    "Team Work",
    "Collaboration",
    "Team Collaboration",

    "Problem Solving",
    "Problem-Solving",

    "Critical Thinking",
    "Analytical Skills",
    "Analytical Thinking",

    "Decision Making",
    "Decision-Making",

    "Time Management",
    "Project Management",

    "Adaptability",
    "Flexibility",

    "Creativity",
    "Innovation",

    "Presentation",
    "Presentation Skills",

    "Public Speaking",

    "Negotiation",
    "Conflict Resolution",

    "Organization",
    "Organizational Skills",

    "Attention to Detail",

    "Work Ethic",

    "Interpersonal Skills",

    "Multitasking",

    "Mentoring",

    "Research",

    "Planning",

    "Coordination",
    "Coordinated",
    "Coordinating",

    "Event Management",

    "Team Building",

    "Quick Learner",
    "Fast Learner",

    "Self Motivation",
    "Self-Motivated",

    "Responsibility",
    "Accountability",
]


# ============================================================
# NORMALIZE
# ============================================================

def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SAFE REGEX
# ============================================================

def make_skill_pattern(skill):

    skill = normalize_text(skill)

    escaped = re.escape(skill)

    # Very short skills need special handling.
    #
    # This prevents:
    #
    # C
    #
    # from matching:
    #
    # CGPA
    # CSS
    # C++
    #

    if skill in ["c", "r", "go"]:

        return (
            rf"(?<![a-z0-9+#])"
            rf"{escaped}"
            rf"(?![a-z0-9+#])"
        )

    return (
        rf"(?<![a-z0-9+#])"
        rf"{escaped}"
        rf"(?![a-z0-9+#])"
    )


# ============================================================
# FIND SKILLS
# ============================================================

def find_skills(text, skill_list):

    if not text:
        return []

    normalized = normalize_text(text)

    found = []

    # Longest first
    sorted_skills = sorted(
        skill_list,
        key=len,
        reverse=True
    )

    for skill in sorted_skills:

        pattern = make_skill_pattern(skill)

        if re.search(
            pattern,
            normalized,
            re.IGNORECASE
        ):

            if skill not in found:
                found.append(skill)

    # Return in original list order
    ordered = []

    for skill in skill_list:

        if skill in found:
            ordered.append(skill)

    return ordered


# ============================================================
# TECHNICAL SKILLS
# ============================================================

def extract_skills(text):

    """
    Extract technical skills from the COMPLETE resume.

    We intentionally search the whole resume instead of only
    resume_data['skills'].

    This makes the analyzer work even when PDF layout
    extraction does not correctly isolate the Skills section.
    """

    return find_skills(
        text,
        TECHNICAL_SKILLS
    )


# ============================================================
# SOFT SKILLS
# ============================================================

def extract_soft_skills(text):

    """
    Extract soft skills from the complete resume.

    This also works when the resume has no dedicated
    Soft Skills section.
    """

    return find_skills(
        text,
        SOFT_SKILLS
    )


# ============================================================
# ALL SKILLS
# ============================================================

def extract_all_skills(text):

    return {
        "technical_skills":
            extract_skills(text),

        "soft_skills":
            extract_soft_skills(text)
    }


# ============================================================
# BACKWARD COMPATIBILITY & HELPERS
# ============================================================

SKILLS = TECHNICAL_SKILLS


def count_skills(skills):
    return len(skills)


SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript",
        "Kotlin", "Swift", "Go", "Rust", "PHP", "Ruby", "Dart", "MATLAB"
    ],
    "Web & Frameworks": [
        "HTML", "CSS", "Bootstrap", "Tailwind", "Tailwind CSS",
        "React", "React.js", "Next.js", "Vue", "Vue.js", "Angular",
        "Node.js", "Express", "Express.js", "FastAPI", "Flask",
        "Django", "Spring", "Spring Boot", "Laravel", ".NET", "ASP.NET"
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "SQLite", "MongoDB",
        "Redis", "Firebase", "Supabase", "Oracle"
    ],
    "AI & Data Science": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence",
        "NLP", "Natural Language Processing", "Computer Vision",
        "Data Science", "Data Analytics", "Generative AI",
        "Pandas", "NumPy", "SciPy", "Scikit-learn",
        "TensorFlow", "PyTorch", "Keras", "OpenCV",
        "Linear Regression", "Logistic Regression", "Decision Tree",
        "Random Forest", "Naive Bayes", "K-Means", "KMeans",
        "SVM", "Support Vector Machine", "PCA", "Principal Component Analysis"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Azure", "Microsoft Azure",
        "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins",
        "Git", "GitHub", "GitLab"
    ],
    "Tools & Others": [
        "REST API", "REST APIs", "REST", "GraphQL", "WebSocket",
        "WebSockets", "JWT", "Postman", "VS Code", "Visual Studio",
        "Figma", "Jupyter", "Jupyter Notebook", "Linux", "Unix",
        "Windows", "macOS", "Vercel", "IBM Watson", "Vite"
    ]
}


def get_skill_categories(skills):
    categories = {}
    normalized_skills = {str(s).lower(): s for s in skills}
    for cat_name, cat_skills in SKILL_CATEGORIES.items():
        found = [s for s in cat_skills if s.lower() in normalized_skills]
        if found:
            categories[cat_name] = found
    return categories