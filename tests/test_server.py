"""Tests for the HTTP server."""

import json
import threading
import urllib.error
import urllib.request

import pytest

from mdr.server import MdrHandler, MdrServer, _is_safe_path


@pytest.fixture
def run_server(tmp_path):
    servers = []

    def _start(path, mode):
        srv = MdrServer(("127.0.0.1", 0), MdrHandler, path=path, mode=mode)
        thread = threading.Thread(target=srv.serve_forever, daemon=True)
        thread.start()
        servers.append(srv)
        return f"http://127.0.0.1:{srv.server_address[1]}"

    yield _start

    for srv in servers:
        srv.shutdown()
        srv.server_close()


def _get(url):
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def test_binds_to_localhost(run_server, tmp_path):
    base = run_server(tmp_path, "directory")
    assert base.startswith("http://127.0.0.1:")


def test_file_mode_serves_rendered_md(tmp_path, run_server):
    md = tmp_path / "readme.md"
    md.write_text("# Title\n\nbody")

    base = run_server(md, "file")
    status, body = _get(base + "/")

    assert status == 200
    assert ">Title</h1>" in body


def test_directory_mode_root_listing(tmp_path, run_server):
    (tmp_path / "note.md").write_text("# N")

    base = run_server(tmp_path, "directory")
    status, body = _get(base + "/")

    assert status == 200
    assert "note.md" in body
    assert "dir-listing" in body


def test_directory_mode_serves_md_file(tmp_path, run_server):
    (tmp_path / "note.md").write_text("# Hello")

    base = run_server(tmp_path, "directory")
    status, body = _get(base + "/note.md")

    assert status == 200
    assert ">Hello</h1>" in body


def test_directory_mode_subdirectory(tmp_path, run_server):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "s.md").write_text("# S")

    base = run_server(tmp_path, "directory")
    status, body = _get(base + "/sub/")

    assert status == 200
    assert "s.md" in body


def test_directory_mode_missing_file(tmp_path, run_server):
    base = run_server(tmp_path, "directory")
    status, _ = _get(base + "/missing.md")
    assert status == 404


def test_directory_mode_non_md_forbidden(tmp_path, run_server):
    (tmp_path / "secret.txt").write_text("x")

    base = run_server(tmp_path, "directory")
    status, _ = _get(base + "/secret.txt")

    assert status == 403


def test_directory_mode_blocks_traversal(tmp_path, run_server):
    secret = tmp_path.parent / "outside.md"
    secret.write_text("# secret")

    base = run_server(tmp_path, "directory")
    try:
        status, _ = _get(base + "/../outside.md")
        assert status == 403
    finally:
        secret.unlink()


def test_url_encoded_paths(tmp_path, run_server):
    md = tmp_path / "my note.md"
    md.write_text("# Spaced")

    base = run_server(tmp_path, "directory")
    status, body = _get(base + "/my%20note.md")

    assert status == 200
    assert ">Spaced</h1>" in body


def test_api_mtime_file_mode(tmp_path, run_server):
    md = tmp_path / "note.md"
    md.write_text("# N")

    base = run_server(md, "file")
    status, body = _get(base + "/api/mtime")

    assert status == 200
    assert json.loads(body)["mtime"] == pytest.approx(md.stat().st_mtime)


def test_api_mtime_directory_mode_returns_dir_mtime(tmp_path, run_server):
    (tmp_path / "note.md").write_text("# N")

    base = run_server(tmp_path, "directory")
    status, body = _get(base + "/api/mtime")

    assert status == 200
    assert json.loads(body)["mtime"] == pytest.approx(tmp_path.stat().st_mtime)


def test_is_safe_path(tmp_path):
    inside = tmp_path / "a.md"
    outside = tmp_path.parent / "b.md"
    assert _is_safe_path(tmp_path, inside)
    assert not _is_safe_path(tmp_path, outside)


def test_serve_shuts_down_after_lifetime(tmp_path):
    from mdr.server import serve

    thread = threading.Thread(
        target=serve,
        args=(tmp_path, "directory"),
        kwargs={"lifetime": 0.3, "open_browser": False},
        daemon=True,
    )
    thread.start()
    thread.join(timeout=5)
    assert not thread.is_alive()
