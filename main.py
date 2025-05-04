import os
import json
import argparse
from src.downloader import download_web_pdf
from src.parser import extract_pdf_lines
from src.extractor import extract_title, extract_rules, extract_codes
from src.utils import load_api_key

def parse_args():
    parser = argparse.ArgumentParser(description="Extract medical PDF info.")
    parser.add_argument("--url", required=True, help="PDF URL")
    parser.add_argument("--api_key", help="API key for auth (or use .env)")
    parser.add_argument("--output-pdf", default="data/sample.pdf", help="Output PDF file path")
    parser.add_argument("--output-json", help="Optional path to save extracted data as JSON")
    parser.add_argument("--insurance", default="Unknown", help="Insurance company name")
    return parser.parse_args()

def extract_mi(url: str, key: str, insurance: str, pdf_loc="data/sample.pdf"):
    rulesstart_sign = "MEDICAL POLICY CRITERIA"
    rulesend_sign = "NOTE: A summary of the supporting rationale for the policy criteria is at the end of the policy."
    codesstart_sign = "Codes Number Description"
    codesend_sign = "Date of Origin"

    download_web_pdf(url, key, pdf_loc)
    print(f"{url} PDF Extraction Initiating^-^")

    lines = extract_pdf_lines(pdf_loc)

    output = {
        "title": extract_title(lines),
        "insurance_name": insurance,
        "rules": extract_rules(lines, rulesstart_sign, rulesend_sign),
        "codes": extract_codes(lines, codesstart_sign, codesend_sign)
    }
    print("PDF Extraction Complete")

    return output

def main():
    args = parse_args()
    key = load_api_key(args.api_key)
    txt = extract_mi(args.url, key, args.insurance, args.output_pdf)
    with open(args.output_json, 'w') as f:
        json.dump(txt, f, indent=4) # Write the output to a file
    print("Please check your $currentFolder/output.json"); f.close()

if __name__ == "__main__":
    main()
