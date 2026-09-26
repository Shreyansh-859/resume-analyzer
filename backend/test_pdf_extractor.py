import os
from resume.pdf_extractor import extract_text_from_pdf

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "test_files", "sample_resume.pdf")

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