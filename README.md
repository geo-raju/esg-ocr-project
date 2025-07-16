# ESG OCR Extraction MVP

This project is an MVP (Minimum Viable Product) for extracting **Environmental, Social, and Governance (ESG) metrics** from company sustainability reports using:

- OCR for scanned PDFs
- Regex-based metric extraction
- spaCy-based NER for contextual enhancement
- Structured CSV export with tags

The pipeline extracts values like **carbon emissions**, **energy usage**, and **water consumption**, then labels them with relevant **ESG categories**.

---

## How to Run
### 1. Clone the repository

```bash
git clone -b mvp https://github.com/geo-raju/esg-ocr-project.git
cd esg-ocr-project
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Run pipeline on a pdf file

```bash
python main.py --input data/esg_report.pdf
```

#### Run Demo with Sample PDF

A demo PDF is provided in the `data/` directory. To extract ESG metrics directly from it:

```bash
python main.py
```

---

## ⚙️ Requirements

- Python 3.8+
- [spaCy](https://spacy.io/)
- [pandas](https://pandas.pydata.org/)
- Hugging Face Transformers (optional)

See `requirements.txt` for all dependencies.

## Maintainer

Built by Geo during an internship project for **Carbon Happy World** 🌍
