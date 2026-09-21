from resume.pdf_extractor import extract_text_from_pdf

from resume.skill_extractor import (
    extract_skills,
    count_skills,
    get_skill_categories
)


# ---------------------------------------
# EXTRACT RESUME TEXT
# ---------------------------------------

pdf_path = "test_files/sample_resume.pdf"

text = extract_text_from_pdf(pdf_path)


# ---------------------------------------
# EXTRACT SKILLS
# ---------------------------------------

skills = extract_skills(text)


# ---------------------------------------
# DISPLAY SKILLS
# ---------------------------------------

print("\n========================================")
print("AI RESUME ANALYZER")
print("SKILL EXTRACTION")
print("========================================")


print("\nDetected Skills:")
print("----------------------------------------")

for number, skill in enumerate(skills, start=1):

    print(f"{number}. {skill}")


# ---------------------------------------
# TOTAL SKILLS
# ---------------------------------------

total_skills = count_skills(skills)

print("\n----------------------------------------")

print("Total Skills Found:", total_skills)


# ---------------------------------------
# SKILL CATEGORIES
# ---------------------------------------

categories = get_skill_categories(skills)


print("\n========================================")
print("SKILLS BY CATEGORY")
print("========================================")


for category, category_skills in categories.items():

    print(f"\n{category}:")

    for skill in category_skills:

        print(f"  - {skill}")