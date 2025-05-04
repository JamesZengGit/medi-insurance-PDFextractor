from src.extractor import extract_title, extract_rules, extract_codes

def test_extract_title():
    lines = ["This is a Sample Title", "", "MEDICAL POLICY CRITERIA"]
    title = extract_title(lines)
    assert "Sample Title" in title

def test_extract_rules():
    lines = [
        "Ignore this",
        "MEDICAL POLICY CRITERIA",
        "Rule A applies to patients with X.",
        "NOTE: A summary of the supporting rationale for the policy criteria is at the end of the policy."
    ]
    rules = extract_rules(lines, "MEDICAL POLICY CRITERIA", "NOTE: A summary of the supporting rationale for the policy criteria is at the end of the policy.")
    assert "Rule A" in rules

def test_extract_codes():
    lines = [
        "Codes Number Description",
        "CPT 12345 Test Code Alpha",
        "67890 Test Code Beta",
        "Date of Origin"
    ]
    codes = extract_codes(lines, "Codes Number Description", "Date of Origin")
    assert len(codes) == 1
    assert "12345" in codes[0]
