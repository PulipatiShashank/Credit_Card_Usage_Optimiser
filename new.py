import sys
import os
import fitz  # PyMuPDF
import openai
from datetime import datetime
import tiktoken
import re

# ✅ Replace with your OpenAI API key
client = openai.OpenAI(api_key="")

PDF_DIR = "pdfs"

def extract_keywords(text):
    # Grab lowercase keywords excluding common stopwords
    stopwords = {"i", "have", "card", "credit", "the", "my", "a", "an"}
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return [word for word in words if word not in stopwords]

def extract_text_from_matching_pdfs(card_name, pdf_dir):
    content = ""
    keywords = extract_keywords(card_name)

    matched_files = [
        f for f in os.listdir(pdf_dir)
        if f.lower().endswith(".pdf") and any(k in f.lower() for k in keywords)
    ]

    if not matched_files:
        print(f"❌ No matching PDFs found for: {card_name} with keywords {keywords}")
        return ""

    print(f"📂 Matching PDFs: {matched_files}")
    
    for filename in matched_files:
        filepath = os.path.join(pdf_dir, filename)
        with fitz.open(filepath) as doc:
            for page in doc:
                content += page.get_text()
    
    return content.strip()

def extract_card_name(user_input):
    if "have" in user_input.lower():
        return user_input.lower().split("have", 1)[1].strip().title()
    return user_input.strip().title()

def truncate_to_max_tokens(text, max_tokens=12000):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return enc.decode(tokens)

def get_card_benefits(card_name, card_text):
    truncated_text = truncate_to_max_tokens(card_text)

    prompt = f"""
You are a financial expert.

Use only the official information below to determine the benefits of the credit card "{card_name}".

--- Official Source Start ---
{truncated_text}
--- Official Source End ---

Provide one clean, structured answer with:
1. Card Name
2. Best Store / Platform to use the card for payments
3. Typical Discount/Cashback Benefit and at what percentage
4. One-line Verdict

Format:
Card Name: <Card Name>
Best Platform: <Platform>
Benefit: <Cashback/Discount>
Verdict: <Verdict>
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()

def save_to_file(card_name, content):
    filename = f"{card_name.replace(' ', '_')}_benefits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Benefits of {card_name}:\n\n")
        file.write(content)
    print(f"\n✅ Benefits saved to: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python card.py 'I have XYZ Credit Card'")
        sys.exit(1)

    user_input = sys.argv[1]
    card_name = extract_card_name(user_input)

    print(f"\n🔍 Looking up benefits for: {card_name}\n")
    card_text = extract_text_from_matching_pdfs(card_name, PDF_DIR)

    if not card_text:
        print("❌ No relevant content found.")
        sys.exit(1)

    result = get_card_benefits(card_name, card_text)
    save_to_file(card_name, result)
