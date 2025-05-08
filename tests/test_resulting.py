import os
import tempfile
import json
from main import extract_mi
from src.utils import load_api_key

def test_full_extraction_pipeline():
    # Setup test variables
    url = "tests/sample.pdf"  # Public insurance PDF
    insurance = "Regene"
    api_key = load_api_key()
    
    assert api_key, "API key must be set in your .env file or passed for testing."

    # Use a temp file to avoid writing to real file system
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp_pdf:
        output = extract_mi(url=url, key=api_key, insurance=insurance, pdf_loc=tmp_pdf.name)

        # Validate output structure
        assert isinstance(output, dict), "Output should be a dictionary"
        assert "title" in output, "Missing 'title' in output"
        assert "rules" in output, "Missing 'rules' in output"
        assert "codes" in output, "Missing 'codes' in output"
        assert isinstance(output["rules"], list), "Rules should be a list"
        assert isinstance(output["codes"], list), "Codes should be a list or nested structure"
        assert len(output["title"]) > 0, "Title extraction failed"

        # Optionally log the output
        print(json.dumps(output, indent=2))
