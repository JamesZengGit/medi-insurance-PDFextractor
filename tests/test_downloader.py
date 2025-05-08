import requests
from unittest import mock
from src.downloader import download_web_pdf

class DummyResponse:
    def __init__(self, status_code=200, content=b"PDFDATA"):
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.exceptions.HTTPError(f"Status {self.status_code}")

def test_download_success(tmp_path, monkeypatch):
    url = "https://example.com/file.pdf"
    target = tmp_path / "out.pdf"
    dummy = DummyResponse(status_code=200, content=b"%PDF-1.4")
    monkeypatch.setattr(requests, "get", lambda u, headers=None: dummy)

    result = download_web_pdf(url, "KEY", str(target))

    assert result == str(target)
    assert target.exists()
    assert target.read_bytes().startswith(b"%PDF-1.4")

def test_download_http_error(tmp_path, monkeypatch, caplog):
    url = "https://example.com/missing.pdf"
    target = tmp_path / "out.pdf"
    mock_response = mock.Mock()
    mock_response.status_code = 404
    mock_response.content = b""
    dummy = DummyResponse(status_code=404)
    monkeypatch.setattr(requests, "get", lambda u, headers=None: dummy)

    result = download_web_pdf(url, "KEY", str(target))

    assert result is None
    assert "HTTP error" in caplog.text

def test_download_unexpected_exception(tmp_path, monkeypatch, caplog):
    def bad_get(u, headers=None):
        raise requests.exceptions.ConnectionError("No network")
    monkeypatch.setattr(requests, "get", bad_get)

    result = download_web_pdf("https://bad.url", "KEY", str(tmp_path / "x.pdf"))

    assert result is None
    assert "Request failed" in caplog.text
    assert "No network" in caplog.text

