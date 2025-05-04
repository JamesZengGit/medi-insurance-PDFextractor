import os
from src.parser import extract_pdf_lines

def test_extract_pdf_lines():
    sample_path = "tests/sample.pdf"
    assert os.path.exists(sample_path), "Sample PDF not found."
    
    lines = extract_pdf_lines(sample_path)
    assert isinstance(lines, list)
    assert all(isinstance(line, str) for line in lines)
    assert len(lines) > 0

import os
import pytest
from src.parser import extract_pdf_lines

def test_extract_pdf_lines_nonexistent(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_pdf_lines(str(tmp_path / "no.pdf"))

def test_extract_pdf_lines_empty_pdf(tmp_path, monkeypatch):
    empty = tmp_path / "empty.pdf"
    empty.write_bytes(b"")
    class DummyPDF:
        pages = []
        def __enter__(self): return self
        def __exit__(self, *args): pass
    monkeypatch.setattr("pdfplumber.open", lambda path: DummyPDF())

    lines = extract_pdf_lines(str(empty))
    assert isinstance(lines, list)
    assert lines == []

def test_extract_pdf_lines_real_pdf(tmp_path):
    # Requires tests/sample.pdf (contains at least one line of text)
    sample = "tests/sample.pdf"
    assert os.path.exists(sample)
    lines = extract_pdf_lines(sample)
    assert len(lines) > 0
    assert all(isinstance(l, str) for l in lines)
