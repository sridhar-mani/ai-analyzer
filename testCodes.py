import pdfplumber
import re

def read_pdf_content(file_path):
    try:
        pages_content = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                pages_content.append(lines)
        return pages_content
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None



def process_pdf_content(file_path):
    content = read_pdf_content(file_path)
    if not content:
        return None

    result = {}
    pending_headline = ""

    for page_num, page_lines in enumerate(content, 1):
        current_content = []
        headline_parts = []

        # First pass: collect potential headline parts
        for i, line in enumerate(page_lines):
            if is_headline(line):  # Only check first few lines
                headline_parts.append(line)
            else:
                current_content.append(line)

        # Construct headline
        if pending_headline:
            headline_parts.insert(0, pending_headline)
            pending_headline = ""

        headline = " ".join(headline_parts)

        # If headline seems incomplete, save it for next page
        if headline and len(headline.split()) <= 3:
            pending_headline = headline
            headline = ""

        result[page_num] = {
            'headline': headline,
            'content': current_content
        }

    return result

if __name__ == "__main__":
    file_path = "articles.pdf"
    processed_content = process_pdf_content(file_path)

    if processed_content:
        for page_num, data in processed_content.items():
            print(f"\nPage {page_num}:")
            if data['headline']:
                print(f"Headline: {data['headline']}")
            print("Content:")
            for line in data['content']:
                print(line)