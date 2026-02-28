"""Embedded CSS, JS, and HTML templates for mdr."""

CSS = """\
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #21262d;
    --border: #30363d;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --text-link: #58a6ff;
    --accent-green: #3fb950;
    --accent-red: #f85149;
    --code-bg: #161b22;
    --inline-code-bg: rgba(110,118,129,0.2);
    --table-border: #30363d;
    --table-row-alt: #161b22;
    --blockquote-border: #3fb950;
    --scrollbar-thumb: #30363d;
    --scrollbar-track: #0d1117;
}

*, *::before, *::after { box-sizing: border-box; }

html {
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

body {
    max-width: 860px;
    margin: 0 auto;
    padding: 32px 24px 64px;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
    line-height: 1.25;
    color: var(--text-primary);
}
h1 { font-size: 2em; padding-bottom: 0.3em; border-bottom: 1px solid var(--border); }
h2 { font-size: 1.5em; padding-bottom: 0.3em; border-bottom: 1px solid var(--border); }
h3 { font-size: 1.25em; }
h1:first-child, h2:first-child, h3:first-child { margin-top: 0; }

/* Links */
a { color: var(--text-link); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Paragraphs */
p { margin: 0 0 16px; }

/* Lists */
ul, ol { margin: 0 0 16px; padding-left: 2em; }
li { margin: 0.25em 0; }
li > p { margin-bottom: 0.5em; }

/* Task lists */
.task-list-item {
    list-style: none;
    margin-left: -1.5em;
}
.task-list-item input[type="checkbox"] {
    margin-right: 0.5em;
    vertical-align: middle;
    accent-color: var(--accent-green);
}

/* Code - inline */
code {
    background: var(--inline-code-bg);
    border-radius: 6px;
    padding: 0.2em 0.4em;
    font-size: 85%;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}

/* Code - blocks */
pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 0 0 16px;
    line-height: 1.45;
}
pre code {
    background: none;
    border-radius: 0;
    padding: 0;
    font-size: 85%;
}

/* Blockquotes */
blockquote {
    margin: 0 0 16px;
    padding: 0 1em;
    border-left: 4px solid var(--blockquote-border);
    color: var(--text-secondary);
}
blockquote > :last-child { margin-bottom: 0; }

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 0 0 16px;
    display: block;
    overflow-x: auto;
}
th, td {
    border: 1px solid var(--table-border);
    padding: 8px 16px;
    text-align: left;
}
th {
    background: var(--bg-tertiary);
    font-weight: 600;
}
tr:nth-child(even) { background: var(--table-row-alt); }

/* Horizontal rules */
hr {
    border: none;
    border-top: 2px solid var(--border);
    margin: 24px 0;
}

/* Images */
img { max-width: 100%; border-radius: 6px; }

/* Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--scrollbar-track); }
::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 4px; }

/* Directory listing */
.dir-listing { list-style: none; padding: 0; }
.dir-listing li {
    border-bottom: 1px solid var(--border);
}
.dir-listing li:last-child { border-bottom: none; }
.dir-listing a {
    display: block;
    padding: 10px 12px;
    border-radius: 6px;
    transition: background 0.15s;
}
.dir-listing a:hover {
    background: var(--bg-secondary);
    text-decoration: none;
}
.dir-icon { margin-right: 8px; }
"""

PYGMENTS_CSS = """\
/* Pygments - native-like dark theme */
.codehilite .hll { background-color: #21262d; }
.codehilite .c   { color: #8b949e; font-style: italic; }
.codehilite .k   { color: #ff7b72; }
.codehilite .o   { color: #e6edf3; }
.codehilite .cm  { color: #8b949e; font-style: italic; }
.codehilite .cp  { color: #8b949e; font-style: italic; }
.codehilite .c1  { color: #8b949e; font-style: italic; }
.codehilite .cs  { color: #8b949e; font-style: italic; }
.codehilite .gd  { color: #f85149; }
.codehilite .gi  { color: #3fb950; }
.codehilite .ge  { font-style: italic; }
.codehilite .gs  { font-weight: bold; }
.codehilite .gu  { color: #79c0ff; }
.codehilite .kc  { color: #ff7b72; }
.codehilite .kd  { color: #ff7b72; }
.codehilite .kn  { color: #ff7b72; }
.codehilite .kp  { color: #ff7b72; }
.codehilite .kr  { color: #ff7b72; }
.codehilite .kt  { color: #ffa657; }
.codehilite .m   { color: #79c0ff; }
.codehilite .s   { color: #a5d6ff; }
.codehilite .na  { color: #79c0ff; }
.codehilite .nb  { color: #ffa657; }
.codehilite .nc  { color: #ffa657; font-weight: bold; }
.codehilite .no  { color: #79c0ff; }
.codehilite .nd  { color: #d2a8ff; }
.codehilite .ni  { color: #e6edf3; }
.codehilite .ne  { color: #ffa657; }
.codehilite .nf  { color: #d2a8ff; }
.codehilite .nl  { color: #79c0ff; }
.codehilite .nn  { color: #ffa657; }
.codehilite .nt  { color: #7ee787; }
.codehilite .nv  { color: #79c0ff; }
.codehilite .ow  { color: #ff7b72; }
.codehilite .w   { color: #e6edf3; }
.codehilite .mb  { color: #79c0ff; }
.codehilite .mf  { color: #79c0ff; }
.codehilite .mh  { color: #79c0ff; }
.codehilite .mi  { color: #79c0ff; }
.codehilite .mo  { color: #79c0ff; }
.codehilite .sa  { color: #a5d6ff; }
.codehilite .sb  { color: #a5d6ff; }
.codehilite .sc  { color: #a5d6ff; }
.codehilite .dl  { color: #a5d6ff; }
.codehilite .sd  { color: #8b949e; }
.codehilite .s2  { color: #a5d6ff; }
.codehilite .se  { color: #79c0ff; }
.codehilite .sh  { color: #a5d6ff; }
.codehilite .si  { color: #a5d6ff; }
.codehilite .sx  { color: #a5d6ff; }
.codehilite .sr  { color: #a5d6ff; }
.codehilite .s1  { color: #a5d6ff; }
.codehilite .ss  { color: #79c0ff; }
.codehilite .bp  { color: #ffa657; }
.codehilite .fm  { color: #d2a8ff; }
.codehilite .vc  { color: #79c0ff; }
.codehilite .vg  { color: #79c0ff; }
.codehilite .vi  { color: #79c0ff; }
.codehilite .vm  { color: #79c0ff; }
.codehilite .il  { color: #79c0ff; }
"""

LIVE_RELOAD_JS = """\
(function() {
    var lastMtime = null;
    setInterval(function() {
        fetch('/api/mtime')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (lastMtime === null) {
                    lastMtime = data.mtime;
                } else if (data.mtime !== lastMtime) {
                    location.reload();
                }
            })
            .catch(function() {});
    }, 1000);
})();
"""


def render_page(title: str, body: str, live_reload: bool = True) -> str:
    """Wrap rendered markdown body in a full HTML page."""
    reload_script = f"<script>{LIVE_RELOAD_JS}</script>" if live_reload else ""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - mdr</title>
<style>{CSS}{PYGMENTS_CSS}</style>
</head>
<body>
{body}
{reload_script}
</body>
</html>"""


def render_directory_page(title: str, items_html: str) -> str:
    """Wrap a directory listing in a full HTML page (no live reload)."""
    return render_page(title, items_html, live_reload=False)
