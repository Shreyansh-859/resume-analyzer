from resume.pdf_extractor import extract_text_from_pdf


pdf_path = "test_files/sample_resume.pdf"


text = extract_text_from_pdf(pdf_path)


print("\n========================================")
print("AI RESUME ANALYZER")
print("PDF TEXT EXTRACTION")
print("========================================")

print("\nExtracted Resume Text:")
print("----------------------------------------")

print(text)

print("----------------------------------------")

print("\nTotal Characters:", len(text))
print("Total Words:", len(text.split()))