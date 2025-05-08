## Project Purpose

This project provides a **robust, modular pipeline** for extracting structured knowledge from medical insurance PDFs --- a key preprocessing step for knowledge graph embedding in biomedical computing. Designed with scalability and open-source goals in mind, it *hopefully >_<* addresses the **urgent need** Bay Area medical AI and healthtech startups to turn unstructured policy text into machine-readable formats for downstream reasoning and analytics. Inspired by **insights gained through conversations** with innovative startup founders, I identified a recurring need for automated document understanding tools in early-stage healthcare ventures.

key words: end-to-end extraction, API configurations, clean architectures, comprehensive tests

---

## Overview

**Medical PDF Extractor** is a modular Python pipeline that downloads medical insurance policy PDFs, parses their contents, and extracts structured information (titles, policy criteria rules, and codes). The extracted data is intended for ingestion into a knowledge graph.

---

## Prerequisites

* **Python 3.8+**
* **Git** (for cloning the repo)
* **Virtual environment tool** (e.g., `venv`, `virtualenv`, or `conda`)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/medical-pdf-extractor.git
   cd medical-pdf-extractor
   ```

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate       # macOS/Linux
   .\venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

All sensitive or environment-specific values are stored in a `.env` file at the project root. The project uses `python-dotenv` to load these values into `os.environ`.

1. **Create a `.env`**

   ```bash
   touch .env
   ```
2. **Add the following variables**

   ```ini
   # .env
   API_KEY=your_api_key_here
   PDF_URL=https://example.com/sample-insurance-policy.pdf
   ```
3. **Verify**

   ```bash
   python -c "from src.utils import load_api_key; print(load_api_key())"
   # Should print your_api_key_here
   ```

---

## Usage

Once configured, run the extraction pipeline:

```bash
python main.py
```

This will:

1. Download the PDF from `PDF_URL` using `API_KEY` as a Bearer token.
2. Parse it with `pdfplumber`.
3. Extract:

   * **Title** (from line 2 of the PDF)
   * **Rules** (between `"MEDICAL POLICY CRITERIA"` and the summary marker)
   * **Codes** (between `"Codes Number Description"` and `"Date of Origin"`)
4. Print the resulting dictionary to stdout.

---

## Project Structure

```bash
medical-pdf-extractor/
│
├── main.py                 # Entry point: loads config and runs extract_mi()
├── .env                    # Local configuration (ignored by Git)
├── requirements.txt        # Pinned dependencies
├── README.md               # This file
├── .gitignore
│
├── src/                    # Main package
│   ├── __init__.py         # Exposes extract_pdf() API
│   ├── downloader.py       # download_web_pdf()
│   ├── parser.py           # extract_pdf_lines()
│   ├── extractor.py        # extract_title(), extract_rules(), extract_codes()
│   └── utils.py            # load_api_key()
│
└── tests/                  # Pytest suite
    ├── __init__.py
    ├── test_downloader.py
    ├── test_parser.py
    ├── test_extractor.py
    ├── test_resulting.py
    └── test_utils.py
```

---

## Running Tests

The project uses **pytest** for unit testing. To run all tests:

```bash
pytest --maxfail=1 --disable-warnings -q
```

* **`--maxfail=1`**: stops after first failure
* **`--disable-warnings`**: omits warning output
* **`-q`**: quiet mode, only shows summary

Ensure you have a sample PDF at `tests/sample.pdf` for parser tests.

---

## Contributing

1. **Fork** the repo
2. **Create** a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes:

   ```bash
   git commit -m "Add awesome feature"
   ```
4. **Push** to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open** a Pull Request against `main`.
