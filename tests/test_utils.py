from src.utils import load_api_key

def test_load_api_key(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("API_KEY=TEST123\n")
    monkeypatch.chdir(tmp_path)
    key = load_api_key()
    assert key == "TEST123"

def test_load_api_key_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    key = load_api_key()
    assert key is None
