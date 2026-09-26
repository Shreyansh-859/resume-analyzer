from resume.job_matcher import analyze_job_match


if __name__ == "__main__":
    resume_text = """
    Computer Engineering student with experience in
    Python, SQL, HTML, CSS, Flask and Git.

    Projects include web applications using Python,
    Flask and MySQL.
    """


    job_description = """
    We are looking for a software developer with
    Python, SQL, React, JavaScript, HTML, CSS,
    Git and Docker experience.
    """


    result = analyze_job_match(
        resume_text,
        job_description
    )


    print("\n======================================")
    print("JOB MATCHING")
    print("======================================")


    print("\nResume Skills:")

    for skill in result["resume_skills"]:
        print("✓", skill)


    print("\nJob Required Skills:")

    for skill in result["job_skills"]:
        print("•", skill)


    print("\nMatching Skills:")

    for skill in result["matched_skills"]:
        print("✓", skill)


    print("\nMissing Skills:")

    for skill in result["missing_skills"]:
        print("✗", skill)


    print("\n======================================")
    print(
        "JOB MATCH:",
        result["match_percentage"],
        "%"
    )
    print("======================================")