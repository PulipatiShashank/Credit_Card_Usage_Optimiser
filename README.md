# 💳 Credit Card Benefits CLI

This is a Python-based CLI tool that provides benefits and cashback details for credit cards by analyzing **official PDF documents** stored locally (like bank brochures or T&C PDFs).

---

## ✅ Features

- 🔍 Extracts accurate card benefits using **OpenAI GPT model**.
- 📄 Uses **your own PDFs** as the only source of truth (no external web search).
- 🔑 Matches keywords (like `cashback`, `sbi`, `axis`, etc.) in the filenames.
- 🧠 Automatically summarizes card benefits into structured format.
- 💾 Saves results to a neatly formatted `.txt` file.

---

## 📁 Folder Structure

project/
├── pdfs/ # Put all your credit card PDFs here
│ ├── sbi_cashback_2024.pdf
│ ├── axis_myzone.pdf
│ └── kotak_myntra.pdf
├── card.py # Main Python CLI script
├── README.md # This file


---

## ⚙️ Requirements

- Python 3.7+
- Install dependencies:

