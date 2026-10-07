"""Tests for the command-line interface."""

import sys

import pytest

from mdr import cli


def run_main(monkeypatch, *argv):
    calls = {}

    def fake_serve(path, mode, port=0, open_browser=True, lifetime=5.0):
        calls.update(path=path, mode=mode, port=port, open_browser=open_browser,
                     lifetime=lifetime)

    monkeypatch.setattr(cli, "serve", fake_serve)
    monkeypatch.setattr(sys, "argv", ["mdr", *argv])
    cli.main()
    return calls


def test_cli_file_mode(tmp_path, monkeypatch):
    md = tmp_path / "note.md"
    md.write_text("# x")

    calls = run_main(monkeypatch, str(md), "--no-open")

    assert calls["mode"] == "file"
    assert calls["path"] == md.resolve()
    assert calls["open_browser"] is False


def test_cli_directory_opens_browser_by_default(tmp_path, monkeypatch):
    calls = run_main(monkeypatch, str(tmp_path))
    assert calls["mode"] == "directory"
    assert calls["open_browser"] is True


def test_cli_defaults_to_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    calls = run_main(monkeypatch, "--no-open")

    assert calls["path"] == tmp_path.resolve()
    assert calls["mode"] == "directory"


def test_cli_port_passthrough(tmp_path, monkeypatch):
    md = tmp_path / "n.md"
    md.write_text("# x")

    calls = run_main(monkeypatch, str(md), "-p", "8000", "--no-open")

    assert calls["port"] == 8000


def test_cli_lifetime_default_and_flag(tmp_path, monkeypatch):
    md = tmp_path / "n.md"
    md.write_text("# x")

    calls = run_main(monkeypatch, str(md), "--no-open")
    assert calls["lifetime"] == 5.0

    calls = run_main(monkeypatch, str(md), "-t", "2.5", "--no-open")
    assert calls["lifetime"] == 2.5


def test_cli_missing_path_exits(tmp_path, capsys, monkeypatch):
    missing = tmp_path / "nope"
    monkeypatch.setattr(sys, "argv", ["mdr", str(missing)])

    with pytest.raises(SystemExit) as exc:
        cli.main()

    assert exc.value.code == 1
    assert "does not exist" in capsys.readouterr().err


def test_cli_non_md_file_exits(tmp_path, capsys, monkeypatch):
    f = tmp_path / "x.txt"
    f.write_text("x")
    monkeypatch.setattr(sys, "argv", ["mdr", str(f)])

    with pytest.raises(SystemExit) as exc:
        cli.main()

    assert exc.value.code == 1
    assert "not a markdown" in capsys.readouterr().err
