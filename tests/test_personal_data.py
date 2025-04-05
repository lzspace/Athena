import pytest
from assistant_core.interfaces import personal_data

def test_load_preferences_empty(tmp_path, monkeypatch):
    fake_dir = tmp_path / "PersonalD" / "Knowledge"
    fake_dir.mkdir(parents=True)
    prefs_file = fake_dir / "preferences.json"
    prefs_file.write_text('{"theme": "dark", "language": "de"}', encoding="utf-8")

    monkeypatch.setattr(personal_data, "PERSONALD_PATH", tmp_path / "PersonalD")
    prefs = personal_data.load_preferences()

    assert prefs.get("theme") == "dark"
    assert prefs.get("language") == "de"

def test_list_scripts_empty(tmp_path, monkeypatch):
    script_dir = tmp_path / "PersonalD" / "Scripts"
    script_dir.mkdir(parents=True)

    monkeypatch.setattr(personal_data, "PERSONALD_PATH", tmp_path / "PersonalD")
    assert personal_data.list_scripts() == []

def test_run_script_success(tmp_path, monkeypatch):
    scripts_dir = tmp_path / "PersonalD" / "Scripts"
    scripts_dir.mkdir(parents=True)
    script_file = scripts_dir / "hello.py"
    script_file.write_text('print("Hello, world!")', encoding="utf-8")

    monkeypatch.setattr(personal_data, "PERSONALD_PATH", tmp_path / "PersonalD")
    output = personal_data.run_script("hello.py")
    assert output == "Hello, world!"