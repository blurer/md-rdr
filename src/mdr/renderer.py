"""Markdown to HTML conversion and directory listing."""

import re
from html import escape
from pathlib import Path

import markdown

from mdr.templates import render_page, render_directory_page

# Regex to convert task list items before markdown processing
_TASK_RE = re.compile(r"^(\s*[-*])\s+\[([ xX])\]\s+", re.MULTILINE)


def _task_list_preprocessor(text: str) -> str:
    """Convert `- [ ] item` / `- [x] item` to HTML checkboxes."""
    def _replace(m: re.Match) -> str:
        indent = m.group(1)
        checked = ' checked disabled' if m.group(2).lower() == 'x' else ' disabled'
        return f'{indent} <input type="checkbox"{checked}> '
    return _TASK_RE.sub(_replace, text)


# Shared markdown instance
_MD_EXTENSIONS = [
    "fenced_code",
    "codehilite",
    "tables",
    "toc",
    "sane_lists",
    "smarty",
]

_MD_EXTENSION_CONFIGS = {
    "codehilite": {
        "css_class": "codehilite",
        "guess_lang": False,
    },
}


def render_markdown(text: str, title: str = "") -> str:
    """Convert markdown text to a full HTML page."""
    text = _task_list_preprocessor(text)
    md = markdown.Markdown(
        extensions=_MD_EXTENSIONS,
        extension_configs=_MD_EXTENSION_CONFIGS,
    )
    body = md.convert(text)

    # Add task-list-item class to <li> elements containing our checkboxes
    body = body.replace(
        '<li><input type="checkbox"',
        '<li class="task-list-item"><input type="checkbox"',
    )

    return render_page(title, body)


def render_directory(dir_path: Path) -> str:
    """Generate an HTML directory listing of markdown files."""
    items = []

    # Collect subdirectories and .md files, sorted
    entries = sorted(dir_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))

    for entry in entries:
        if entry.is_dir() and not entry.name.startswith('.'):
            name = escape(entry.name)
            items.append(
                f'<li><a href="/{name}/"><span class="dir-icon">📁</span>{name}/</a></li>'
            )
        elif entry.suffix.lower() == '.md':
            name = escape(entry.name)
            items.append(
                f'<li><a href="/{name}"><span class="dir-icon">📄</span>{name}</a></li>'
            )

    if not items:
        body = "<p>No markdown files found in this directory.</p>"
    else:
        body = f'<h1>{escape(dir_path.name) or "/"}</h1>\n<ul class="dir-listing">{"".join(items)}</ul>'

    return render_directory_page(escape(str(dir_path)), body)
