import os
from resume.pdf_extractor import extract_text_from_pdf
from resume.resume_analyzer import analyze_resume


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "test_files", "sample_resume.pdf")

    text = extract_text_from_pdf(pdf_path)


# ---------------------------------------
# ANALYZE RESUME
# ---------------------------------------

result = analyze_resume(text)


print("\n========================================")
print("AI RESUME ANALYZER")
print("RESUME INFORMATION EXTRACTION")
print("========================================")


print("\nName:")
print(result["name"])


print("\nEmail:")
print(result["email"])


print("\nPhone:")
print(result["phone"])


print("\n========================================")
print("EDUCATION")
print("========================================")

print(result["education"])


print("\n========================================")
print("TECHNICAL SKILLS")
print("========================================")

print(result["skills"])


print("\n========================================")
print("PROJECTS")
print("========================================")

print(result["projects"])


print("\n========================================")
print("EXPERIENCE")
print("========================================")

print(result["experience"])


print("\n========================================")
print("CERTIFICATIONS")
print("========================================")

print(result["certifications"])