"""Tests for markdown rendering and directory listing."""

from mdr.renderer import _task_list_preprocessor, render_directory, render_markdown


def test_render_markdown_basic():
    html = render_markdown("# Hello\n\nSome **bold** text.", "test")
    assert ">Hello</h1>" in html
    assert "<strong>bold</strong>" in html
    assert "<title>test - mdr</title>" in html


def test_render_markdown_fenced_code():
    html = render_markdown("```python\nprint('hi')\n```", "t")
    assert "codehilite" in html


def test_render_markdown_tables():
    html = render_markdown("| a | b |\n|---|---|\n| 1 | 2 |", "t")
    assert "<table>" in html
    assert "<td>1</td>" in html


def test_render_markdown_raw_html_passthrough():
    html = render_markdown("<b>raw</b> html", "t")
    assert "<b>raw</b>" in html


def test_task_list_unchecked():
    out = _task_list_preprocessor("- [ ] todo")
    assert '<input type="checkbox" disabled>' in out


def test_task_list_checked():
    out = _task_list_preprocessor("- [x] done")
    assert "checked disabled" in out


def test_task_list_rendered():
    html = render_markdown("- [x] done\n- [ ] todo", "t")
    assert 'class="task-list-item"' in html
    assert "checked" in html


def test_render_directory_lists_md_files(tmp_path):
    (tmp_path / "b.md").write_text("# B")
    (tmp_path / "a.md").write_text("# A")
    (tmp_path / "notes.txt").write_text("not md")
    (tmp_path / "subdir").mkdir()

    html = render_directory(tmp_path)

    assert html.index("a.md") < html.index("b.md")
    assert "subdir/" in html
    assert "notes.txt" not in html


def test_render_directory_hides_hidden_dirs(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "x.md").write_text("# x")

    html = render_directory(tmp_path)
    assert ".git" not in html


def test_render_directory_empty(tmp_path):
    html = render_directory(tmp_path)
    assert "No markdown files found" in html


def test_render_directory_escapes_names(tmp_path):
    (tmp_path / "<b>.md").write_text("# x")

    html = render_directory(tmp_path)
    assert "&lt;b&gt;.md" in html
    assert "<b>.md" not in html
