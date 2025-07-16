import argparse
import os

from ocr.extract_text import extract_text_from_file
from extractors.extract_metrics import extract_esg_metrics, enrich_metrics_with_context
# from nlp.ner_transformers import run_transformer_ner
from nlp.ner_spacy import run_spacy_ner

def main(input_file):
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return
    
    output_txt = "output/report.txt"
    # Ensure output directory exists
    output_dir = os.path.dirname(output_txt)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extract_text_from_file(input_file, output_txt)
    print(f"OCR complete. Text saved to {output_txt}")

    # Load OCR text
    with open("output/report.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Extract ESG metrics
    df = extract_esg_metrics(text)

    # Run NER extraction
    # ner_results = run_transformer_ner(text)
    ner_results = run_spacy_ner(text)

    df = enrich_metrics_with_context(df, ner_results)
    df = df[df["value"].astype(str).str.strip() != ""]
    df = df[df["unit"].astype(str).str.strip()  != ""]

    df.to_csv("output/extracted_metrics.csv", index=False)
    print(df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ESG metrics from OCR text file")
    parser.add_argument("--input", type=str, default="data/MacBook_Pro_16-inch_PER_Oct2024.pdf", help="Path to input file")

    args = parser.parse_args()
    main(args.input)










