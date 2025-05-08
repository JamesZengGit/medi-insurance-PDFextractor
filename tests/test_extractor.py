import pytest
from src.extractor import extract_title, extract_rules, extract_codes

@pytest.fixture
def simple_lines():
    return [
        "Title of Document",
        "Subtitle",
        "MEDICAL POLICY CRITERIA",
        "I. First rule detail",
        "Consider"
        "A. Subrule detial"
        "B. Subrule detail"
        "II. Second rule",
        "detail"
        "NOTE: A summary of the supporting rationale for the policy criteria is at the end of the policy.",
        "Codes Number Description",
        "CPT 12345 Some code description",
        "67890 Another code",
        "Date of Origin",
    ]

def test_extract_title_present(simple_lines):
    assert extract_title(simple_lines) == "Subtitle"

def test_extract_title_missing():
    assert extract_title([]) == ""

def test_extract_rules_happy_path(simple_lines):
    rules = extract_rules(
        simple_lines,
        "MEDICAL POLICY CRITERIA",
        "NOTE: A summary of the supporting rationale for the policy criteria is at the end of the policy."
    )
    assert rules["rule_id"] == "1"
    ids = [r["rule_id"] for r in rules["rules"]]
    assert ids == ["1.1"]
    assert rules["rules"][0]["rule_text"] == "First rule detail Consider"
    assert rules["rules"][1]["rule_text"] == "Second rule detail"

def test_extract_rules_no_markers():
    # If start or end not present, should return {}
    lines = ["No markers here"]
    assert extract_rules(lines, "START", "END") == {}

def test_extract_codes_happy_path(simple_lines):
    codes = extract_codes(
        simple_lines,
        "Codes Number Description",
        "Date of Origin"
    )
    assert isinstance(codes, list)
    assert codes["cpt"] == "12345"
    assert codes['icd10'] is None

def test_extract_codes_empty():
    # Missing code section yields empty list
    assert extract_codes(["No codes here"], "START", "END") == []
