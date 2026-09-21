import re
from difflib import SequenceMatcher


# ============================================================
# SECTION ALIASES
# ============================================================

SECTION_ALIASES = {
    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "profile summary",
        "professional profile",
        "career profile",
        "profile",
        "about me",
        "about",
        "personal summary",
        "executive summary",
        "overview",
        "professional overview",
        "career overview",
        "introduction",
    ],

    "objective": [
        "objective",
        "career objective",
        "professional objective",
        "career goal",
        "career goals",
        "professional goal",
        "professional goals",
        "objective statement",
        "career objective statement",
    ],

    "education": [
        "education",
        "educational qualification",
        "educational qualifications",
        "educational background",
        "educational details",
        "education details",
        "academic background",
        "academic qualification",
        "academic qualifications",
        "academic details",
        "academic history",
        "academic profile",
        "academic record",
        "educational history",
        "qualifications",
        "qualification",
        "degrees",
        "degree",
        "education and qualifications",
        "academic qualifications",
        "academic credentials",
    ],

    "skills": [
        "skills",
        "skill",
        "technical skills",
        "technical skill",
        "technical expertise",
        "technical competencies",
        "technical competency",
        "core competencies",
        "core competency",
        "key skills",
        "key technical skills",
        "technologies",
        "technology",
        "programming skills",
        "programming",
        "professional skills",
        "technical knowledge",
        "areas of expertise",
        "areas of expertize",
        "expertise",
        "competencies",
        "computer skills",
        "software skills",
        "it skills",
        "technical proficiencies",
        "technical proficiency",
        "skills and technologies",
        "technical skills and tools",
        "tools and technologies",
        "technologies and tools",
        "technical stack",
        "tech stack",
        "technology stack",
        "technology skills",
        "skills summary",
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "work history",
        "career history",
        "career experience",
        "professional history",
        "work profile",
        "work background",
        "employment experience",
        "industry experience",
        "relevant experience",
        "relevant work experience",
        "professional work experience",
        "work experience and internships",
        "experience and internships",
        "internship",
        "internships",
        "internship experience",
        "internship experiences",
        "internship history",
        "internship experience",
        "internships and experience",
        "internships and work experience",
        "internship and work experience",
        "industrial experience",
        "training and experience",
        "training experience",
    ],

    "projects": [
        "projects",
        "project",
        "project experience",
        "project experiences",
        "academic projects",
        "academic project",
        "personal projects",
        "personal project",
        "key projects",
        "selected projects",
        "major projects",
        "project work",
        "project portfolio",
        "projects and research",
        "projects and experience",
        "academic and personal projects",
        "technical projects",
        "software projects",
        "college projects",
        "university projects",
        "mini projects",
        "final year project",
        "final year projects",
        "capstone project",
        "capstone projects",
        "project highlights",
    ],

    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "professional certifications",
        "professional certification",
        "courses and certifications",
        "courses and certificates",
        "courses certifications",
        "certifications and courses",
        "certifications and training",
        "certificates and courses",
        "training and certifications",
        "courses and training",
        "licenses and certifications",
        "licenses certifications",
        "certifications and activities",
        "certification and activities",
        "certifications activities",
        "courses and certifications and activities",
        "certifications & activities",
        "certifications and activities",
    ],

    "achievements": [
        "achievements",
        "achievement",
        "awards",
        "award",
        "awards and achievements",
        "honors",
        "honours",
        "accomplishments",
        "accomplishment",
        "recognitions",
        "recognition",
        "academic achievements",
        "professional achievements",
        "key achievements",
        "notable achievements",
        "achievements and awards",
        "awards and honors",
        "awards and honours",
        "hackathons",
        "hackathon",
        "hackathons and competitions",
        "hackathon and competitions",
        "hackathons competitions",
        "competitions",
        "competition",
        "competitions and achievements",
        "competitions and awards",
        "hackathons and awards",
        "hackathons and achievements",
        "extracurricular achievements",
        "hackathons & certification",
        "hackathons and certification",
        "hackathon & certification",
        "hackathon and certification",
    ],

    "soft_skills": [
        "soft skills",
        "soft skill",
        "leadership",
        "leadership skills",
        "leadership and soft skills",
        "leadership soft skills",
        "interpersonal skills",
        "interpersonal",
        "personal skills",
        "people skills",
        "communication skills",
        "professional strengths",
        "strengths",
        "key strengths",
        "core strengths",
        "personal strengths",
        "management skills",
        "behavioral skills",
        "transferable skills",
    ],

    "additional": [
        "additional information",
        "additional info",
        "other information",
        "other details",
        "additional details",
        "additional",
        "miscellaneous",
        "miscellaneous information",
        "personal details",
        "personal information",
        "personal",
        "extra curricular",
        "extracurricular activities",
        "extra curricular activities",
        "co curricular activities",
        "co-curricular activities",
        "activities",
    ],

    "interests": [
        "interests",
        "interest",
        "hobbies",
        "hobby",
        "areas of interest",
        "professional interests",
        "personal interests",
        "interests and hobbies",
        "hobbies and interests",
    ],

    "languages": [
        "languages",
        "language",
        "language proficiency",
        "languages known",
        "known languages",
        "language skills",
        "linguistic skills",
    ],

    "references": [
        "references",
        "reference",
        "professional references",
        "references available upon request",
    ],

    "declaration": [
        "declaration",
        "declarations",
        "declaration statement",
    ],

    "cgpa": [
        "semester cgpa",
        "cgpa",
        "gpa",
        "academic performance",
        "academic results",
        "academic score",
        "grades",
        "marks",
        "percentage",
        "percentages",
    ],
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_heading(text):
    """
    Convert a heading into a standard comparable form.
    Example:

    'CERTIFICATIONS & ACTIVITIES'
    ->
    'CERTIFICATIONS AND ACTIVITIES'
    """

    if not text:
        return ""

    text = str(text).strip().upper()

    text = text.replace("&", " AND ")
    text = text.replace("/", " ")
    text = text.replace("\\", " ")
    text = text.replace("|", " ")
    text = text.replace("-", " ")
    text = text.replace("–", " ")
    text = text.replace("—", " ")

    text = re.sub(r"[^A-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# BUILD NORMALIZED ALIAS MAP
# ============================================================

NORMALIZED_ALIASES = {}

for section_type, aliases in SECTION_ALIASES.items():
    NORMALIZED_ALIASES[section_type] = {
        normalize_heading(alias)
        for alias in aliases
    }


# ============================================================
# BASIC CLEANING
# ============================================================

def clean_line(line):
    if not line:
        return ""

    line = str(line).strip()

    # Remove repeated whitespace
    line = re.sub(r"\s+", " ", line)

    return line


def get_clean_lines(text):
    if not text:
        return []

    lines = text.splitlines()

    result = []

    for line in lines:
        line = clean_line(line)

        if line:
            result.append(line)

    return result


# ============================================================
# HEADING DETECTION
# ============================================================

def exact_section_match(line):
    """
    Strongest heading detection method.
    """

    normalized = normalize_heading(line)

    if not normalized:
        return None

    for section_type, aliases in NORMALIZED_ALIASES.items():

        if normalized in aliases:
            return section_type

    return None


def looks_like_heading(line):
    """
    Determines whether a line visually looks like a heading.

    This is deliberately conservative because project titles
    and company names can also look like headings.
    """

    if not line:
        return False

    line = clean_line(line)

    words = line.split()

    # Headings are usually short.
    if len(words) > 8:
        return False

    # A sentence with lots of punctuation is probably content.
    if line.endswith("."):
        return False

    if "@" in line:
        return False

    if "http://" in line.lower() or "https://" in line.lower():
        return False

    # Date-heavy lines are probably content.
    if re.search(
        r"\b(19|20)\d{2}\b.*\b(19|20)\d{2}\b",
        line
    ):
        return False

    # Count alphabetic characters.
    letters = [char for char in line if char.isalpha()]

    if not letters:
        return False

    uppercase_count = sum(
        1 for char in letters if char.isupper()
    )

    uppercase_ratio = uppercase_count / len(letters)

    # ALL CAPS headings.
    if uppercase_ratio >= 0.75 and len(words) <= 7:
        return True

    # Title Case headings.
    title_words = 0

    for word in words:
        cleaned = re.sub(r"[^A-Za-z]", "", word)

        if cleaned and cleaned[0].isupper():
            title_words += 1

    if (
        len(words) <= 6
        and title_words >= max(2, len(words) - 1)
    ):
        return True

    return False


def fuzzy_section_match(line):
    """
    Conservative fuzzy matching.

    This helps with small spelling differences such as:

        CERTIFICATES & TRAINING
        PROFESSIONAL CERTIFICATE

    without treating arbitrary project names as headings.
    """

    if not looks_like_heading(line):
        return None

    normalized = normalize_heading(line)

    if not normalized:
        return None

    best_section = None
    best_ratio = 0

    for section_type, aliases in NORMALIZED_ALIASES.items():

        for alias in aliases:

            ratio = SequenceMatcher(
                None,
                normalized,
                alias
            ).ratio()

            if ratio > best_ratio:
                best_ratio = ratio
                best_section = section_type

    # Very conservative threshold.
    if best_ratio >= 0.92:
        return best_section

    return None


def get_section_type(line):
    """
    Detect the section represented by a line.

    Order:
        1. Exact heading
        2. Fuzzy heading
    """

    normalized = normalize_heading(line)

    if not normalized:
        return None

    exact = exact_section_match(line)

    if exact:
        return exact

    fuzzy = fuzzy_section_match(line)

    return fuzzy


# ============================================================
# INLINE HEADINGS
# ============================================================

def detect_inline_heading(line):
    """
    Handles:

        Education: B.Tech Computer Engineering

        Skills: Python, Java, SQL

        Objective: Looking for...

    """

    if not line:
        return None, ""

    if ":" not in line:
        return None, ""

    left, right = line.split(":", 1)

    left = clean_line(left)
    right = clean_line(right)

    section_type = exact_section_match(left)

    if section_type:

        return section_type, right

    # Do not use fuzzy matching for arbitrary inline text.
    return None, ""


def detect_heading_type(line):
    if not line:
        return None

    line = clean_line(line)

    if not line:
        return None

    inline_type, _ = detect_inline_heading(line)

    if inline_type:
        return inline_type

    return get_section_type(line)


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_sections(text):
    """
    Split complete resume text into logical sections.
    """

    lines = get_clean_lines(text)

    sections = {}

    current_section = None
    current_content = []

    def save_current_section():

        nonlocal current_section
        nonlocal current_content

        if current_section is None:
            current_content = []
            return

        content = "\n".join(current_content).strip()

        if content:

            if current_section in sections:
                sections[current_section] += "\n" + content

            else:
                sections[current_section] = content

        current_content = []

    for line in lines:

        inline_type, inline_content = detect_inline_heading(line)

        if inline_type:

            save_current_section()

            current_section = inline_type

            if inline_content:
                current_content.append(inline_content)

            continue

        heading_type = detect_heading_type(line)

        if heading_type:

            save_current_section()

            current_section = heading_type

            continue

        if current_section is not None:

            current_content.append(line)

    save_current_section()

    return sections


# ============================================================
# CONTACT INFORMATION
# ============================================================

def extract_email(text):

    if not text:
        return None

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text):

    if not text:
        return None

    patterns = [

        # Indian +91
        r"\+91[\s-]?[6-9]\d{9}",

        # Indian +91 with separated number
        r"\+91[\s-]?\d{5}[\s-]\d{5}",

        # Indian 10 digit
        r"\b[6-9]\d{9}\b",

        # International style
        r"\+\d{1,3}[\s-]?\d{7,12}",

        # General phone with spaces/dashes
        r"\b\d{3,5}[\s-]\d{3,5}[\s-]\d{3,5}\b",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(0).strip()

    return None


# ============================================================
# NAME EXTRACTION
# ============================================================

def is_probable_name(line):

    if not line:
        return False

    line = clean_line(line)

    if len(line) > 60:
        return False

    if "@" in line:
        return False

    if "http" in line.lower():
        return False

    # Phone-like
    if re.search(r"\+?\d[\d\s().-]{7,}", line):
        return False

    words = line.split()

    if not 2 <= len(words) <= 5:
        return False

    for word in words:

        cleaned = word.strip(".,:;|-()")

        if not re.fullmatch(
            r"[A-Za-z][A-Za-z.'-]*",
            cleaned
        ):
            return False

    normalized = normalize_heading(line)

    ignored = {
        "RESUME",
        "CV",
        "CURRICULUM VITAE",
        "PROFILE",
        "SUMMARY",
        "CAREER OBJECTIVE",
        "OBJECTIVE",
        "PROFESSIONAL SUMMARY",
        "MUMBAI",
        "MAHARASHTRA",
        "INDIA",
        "PUNE",
        "DELHI",
        "BENGALURU",
        "BANGALORE",
        "THANE",
        "STUDENT",
        "ENGINEER",
        "ENGINEERING",
        "COLLEGE",
        "UNIVERSITY",
        "COMPUTER ENGINEERING",
    }

    if normalized in ignored:
        return False

    # Location-like line
    location_words = {
        "MUMBAI",
        "MAHARASHTRA",
        "INDIA",
        "PUNE",
        "DELHI",
        "BENGALURU",
        "BANGALORE",
        "THANE",
        "HYDERABAD",
        "CHENNAI",
        "KOLKATA",
        "NAGPUR",
        "NASHIK",
        "SURAT",
        "GUJARAT",
        "KARNATAKA",
        "TAMIL NADU",
        "TELANGANA",
    }

    if any(
        word.upper() in location_words
        for word in words
    ):
        return False

    return True


def extract_name(text):

    lines = get_clean_lines(text)

    if not lines:
        return None

    # Most resumes put the name near the beginning.
    for line in lines[:20]:

        if is_probable_name(line):
            return line

    return None


# ============================================================
# SECTION CLEANING
# ============================================================

def clean_section_content(content):

    if not content:
        return ""

    lines = content.splitlines()

    result = []

    for line in lines:

        line = clean_line(line)

        if not line:
            continue

        result.append(line)

    return "\n".join(result).strip()


# ============================================================
# REMOVE DUPLICATE LINES
# ============================================================

def remove_duplicate_lines(text):

    if not text:
        return ""

    seen = set()
    result = []

    for line in text.splitlines():

        line = clean_line(line)

        if not line:
            continue

        key = line.lower()

        if key in seen:
            continue

        seen.add(key)
        result.append(line)

    return "\n".join(result)


# ============================================================
# COMBINE SECTIONS
# ============================================================

def combine_sections(sections, names):

    result = []

    for name in names:

        content = sections.get(name, "")

        if content:
            result.append(content)

    return remove_duplicate_lines(
        "\n".join(result)
    )


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_resume(text):

    if not text:

        return {
            "name": None,
            "email": None,
            "phone": None,

            "summary": "",
            "objective": "",

            "education": "",
            "skills": "",
            "projects": "",
            "experience": "",

            "certifications": "",
            "achievements": "",
            "soft_skills": "",

            "additional_information": "",
        }

    # --------------------------------------------------------
    # Extract sections
    # --------------------------------------------------------

    sections = extract_sections(text)

    # --------------------------------------------------------
    # Basic sections
    # --------------------------------------------------------

    summary = combine_sections(
        sections,
        ["summary"]
    )

    objective = combine_sections(
        sections,
        ["objective"]
    )

    education = combine_sections(
        sections,
        ["education", "cgpa"]
    )

    skills = combine_sections(
        sections,
        ["skills"]
    )

    projects = combine_sections(
        sections,
        ["projects"]
    )

    experience = combine_sections(
        sections,
        ["experience"]
    )

    certifications = combine_sections(
        sections,
        ["certifications"]
    )

    achievements = combine_sections(
        sections,
        ["achievements"]
    )

    soft_skills = combine_sections(
        sections,
        ["soft_skills"]
    )

    # --------------------------------------------------------
    # Additional information
    # --------------------------------------------------------

    additional_parts = []

    additional = sections.get(
        "additional",
        ""
    )

    interests = sections.get(
        "interests",
        ""
    )

    languages = sections.get(
        "languages",
        ""
    )

    references = sections.get(
        "references",
        ""
    )

    declaration = sections.get(
        "declaration",
        ""
    )

    if additional:
        additional_parts.append(
            additional
        )

    if interests:
        additional_parts.append(
            "Interests: " + interests
        )

    if languages:
        additional_parts.append(
            "Languages: " + languages
        )

    if references:
        additional_parts.append(
            "References: " + references
        )

    if declaration:
        additional_parts.append(
            "Declaration: " + declaration
        )

    additional_information = "\n".join(
        additional_parts
    )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "summary": summary,

        "objective": objective,

        "education": education,

        "skills": skills,

        "projects": projects,

        "experience": experience,

        "certifications": certifications,

        "achievements": achievements,

        "soft_skills": soft_skills,

        "additional_information":
            additional_information,
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    resume_data,
    skills,
    missing_skills
):

    recommendations = []

    if not isinstance(skills, list):
        skills = []

    if not isinstance(missing_skills, list):
        missing_skills = []

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    if len(skills) < 5:

        recommendations.append(
            "Add more relevant technical skills "
            "to your resume."
        )

    elif len(skills) < 10:

        recommendations.append(
            "Consider adding more technical skills "
            "relevant to your target job."
        )

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    for skill in missing_skills[:5]:

        recommendations.append(
            f"Consider learning or adding "
            f"relevant experience with {skill}."
        )

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    if not resume_data.get("experience"):

        recommendations.append(
            "Add internship, work experience, "
            "or relevant practical experience."
        )

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    if not resume_data.get("projects"):

        recommendations.append(
            "Add academic or personal projects "
            "that demonstrate your technical skills."
        )

    # --------------------------------------------------------
    # Certifications
    # --------------------------------------------------------

    if not resume_data.get("certifications"):

        recommendations.append(
            "Consider adding relevant certifications "
            "if you have completed any."
        )

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    if not resume_data.get("education"):

        recommendations.append(
            "Add your educational qualifications."
        )

    # --------------------------------------------------------
    # Summary / Objective
    # --------------------------------------------------------

    if (
        not resume_data.get("summary")
        and not resume_data.get("objective")
    ):

        recommendations.append(
            "Consider adding a concise professional "
            "summary or career objective."
        )

    # --------------------------------------------------------
    # General recommendations
    # --------------------------------------------------------

    recommendations.append(
        "Use clear section headings and "
        "consistent formatting."
    )

    recommendations.append(
        "Use specific, measurable achievements "
        "where possible instead of only listing duties."
    )

    return recommendations