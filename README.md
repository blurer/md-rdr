# mdr

Lightweight markdown reader that renders files in the browser.

## Why?

Working with markdown files is great, but reading them legibly is a pain sometimes. Your options are:

- Push to Git and read it on the web
- Open VSCode and use a markdown preview (heavy)
- Open in Obsidian (don't always want to load into the vault)

`mdr` skips all of that. It spins up a tiny localhost server and opens the rendered page in your browser. That's it.

## Install

```bash
uv sync
```

## Usage

```bash
mdr file.md          # render a file
mdr ./docs/          # browse a directory of .md files
mdr                  # browse current directory
mdr -p 8080 file.md  # custom port
mdr --no-open file.md # don't auto-open browser
```

### Desktop integration (Linux)

To open `.md` files with `mdr` on double-click:

```bash
# Create a .desktop entry (adjust the Exec path to your install)
cat > ~/.local/share/applications/mdr.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=mdr
Comment=Lightweight Markdown Reader
Exec=/home/YOU/.local/bin/mdr %f
MimeType=text/markdown;text/x-markdown;
Terminal=false
NoDisplay=true
EOF

# Set as default
xdg-mime default mdr.desktop text/markdown
xdg-mime default mdr.desktop text/x-markdown
```

## Features

- **GitHub-dark theme** — easy on the eyes, matches terminal aesthetics
- **Syntax highlighting** — fenced code blocks with Pygments
- **Live reload** — edit a file, browser updates automatically (1s polling)
- **Task lists** — `- [x]` and `- [ ]` render as checkboxes
- **Tables, TOC, smart quotes** — all the standard markdown extensions
- **Directory browsing** — navigate folders of markdown files
- **Zero config** — picks a random free port, opens the browser, done

## Dependencies

- Python 3.10+
- `markdown` — parsing
- `pygments` — syntax highlighting
- Everything else is stdlib
