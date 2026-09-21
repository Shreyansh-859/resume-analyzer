from resume.pdf_extractor import extract_text_from_pdf

from resume.resume_analyzer import analyze_resume

from resume.skill_extractor import extract_skills

from resume.scoring import calculate_resume_score


# ---------------------------------------
# EXTRACT RESUME TEXT
# ---------------------------------------

pdf_path = "test_files/sample_resume.pdf"

text = extract_text_from_pdf(pdf_path)


# ---------------------------------------
# ANALYZE RESUME
# ---------------------------------------

resume_data = analyze_resume(text)


# ---------------------------------------
# EXTRACT SKILLS
# ---------------------------------------

skills = extract_skills(text)


# ---------------------------------------
# CALCULATE SCORE
# ---------------------------------------

scores = calculate_resume_score(
    resume_data,
    skills
)


# ---------------------------------------
# DISPLAY RESULTS
# ---------------------------------------

print("\n========================================")
print("AI RESUME ANALYZER")
print("RESUME SCORE")
print("========================================")


print("\nScore Breakdown:")
print("----------------------------------------")

print(
    f"Technical Skills     : "
    f"{scores['skills']}/30"
)

print(
    f"Education            : "
    f"{scores['education']}/15"
)

print(
    f"Experience           : "
    f"{scores['experience']}/20"
)

print(
    f"Projects             : "
    f"{scores['projects']}/15"
)

print(
    f"Certifications       : "
    f"{scores['certifications']}/10"
)

print(
    f"Completeness         : "
    f"{scores['completeness']}/10"
)

print("----------------------------------------")

print(
    f"TOTAL RESUME SCORE   : "
    f"{scores['total']}/100"
)


# ---------------------------------------
# INTERPRETATION
# ---------------------------------------

print("\n========================================")
print("SCORE INTERPRETATION")
print("========================================")

total = scores["total"]

if total >= 80:
    print("Strong resume based on this project's scoring criteria.")

elif total >= 60:
    print("Moderate resume based on this project's scoring criteria.")

else:
    print("Several areas of the resume can be improved.")