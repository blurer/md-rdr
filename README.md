# mdr

Lightweight markdown reader that renders files in the browser, then gets out of the way.

## Why?

I live in markdown all day — homelab notes, docs, runbooks — across Obsidian on mobile
and a mix of Mac and Linux machines. Reading them legibly is still a pain:

- Push to Git and read it on the web
- Open VSCode and use a markdown preview (heavy)
- Open in Obsidian (don't always want to load into the vault)
- Editor previews and print-to-PDF output are jank, especially from mobile

`mdr` skips all of that. It spins up a tiny localhost server, opens the rendered page
in your browser, and **shuts itself down a few seconds later**. No preview panes, no
vault, no service left running in the background. Want to read again? Run it again
(double-click the file).

Bonus: the styled page prints cleanly from the browser's own Print → Save as PDF,
which beats most editor print options.

## Install

```bash
uv sync
```

## Usage

```bash
mdr file.md            # render a file, server self-destructs after 5s
mdr ./docs/            # browse a directory of .md files
mdr                    # browse current directory
mdr -t 30 file.md      # keep the server alive for 30 seconds
mdr -p 8080 file.md    # custom port
mdr --no-open file.md  # don't auto-open browser
```

The tab can stay open after the server exits — you'll see the last rendered page.
Reload just fails; run `mdr` again for a fresh one.

## Security & scope

`mdr` is **not intended for external hosting**. It's a localhost convenience tool:

- Binds to `127.0.0.1` only — never listens on the network
- Random port per run, gone within seconds
- Path traversal protection; directory mode serves only `.md` files
- No auth, no TLS, and markdown-embedded HTML renders as-is — fine for your own
  files on localhost, not something you'd ever want to expose

The short lifetime is the point: nothing lingers to attack or to forget about.

## Features

- **Ephemeral by design** — server self-destructs after a few seconds (`--lifetime` to tune)
- **GitHub-dark theme** — easy on the eyes, matches terminal aesthetics
- **Print/PDF-friendly** — clean output from the browser's Print dialog
- **Syntax highlighting** — fenced code blocks with Pygments
- **Live reload** — edit a file and the browser updates automatically (while the server is alive)
- **Task lists** — `- [x]` and `- [ ]` render as checkboxes
- **Tables, TOC, smart quotes** — all the standard markdown extensions
- **Directory browsing** — navigate folders of markdown files
- **Zero config** — picks a random free port, opens the browser, done

## Dependencies

- Python 3.10+
- `markdown` — parsing
- `pygments` — syntax highlighting
- Everything else is stdlib

## Desktop integration (Linux)

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

### Desktop integration (macOS)

Double-click `.md` files in Finder to open them in `mdr`:

```bash
# 1. Create a launcher app (AppleScript applet) in ~/Applications
cat > /tmp/mdr.applescript << 'EOF'
on open theFiles
	repeat with f in theFiles
		set p to POSIX path of f
		do shell script "/Users/YOU/.local/bin/mdr " & quoted form of p & " >/dev/null 2>&1 &"
	end repeat
end open
EOF
osacompile -o ~/Applications/mdr.app /tmp/mdr.applescript

# 2. Give it a bundle id, then re-sign (editing the plist invalidates osacompile's
#    signature, and Launch Services silently kills the applet on launch otherwise)
/usr/libexec/PlistBuddy -c "Add :CFBundleIdentifier string com.mdr.app" \
  ~/Applications/mdr.app/Contents/Info.plist
codesign --force --deep -s - ~/Applications/mdr.app

# 3. Register with Launch Services
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f ~/Applications/mdr.app

# 4. Make mdr the default handler for .md files
defaults write com.apple.LaunchServices/com.apple.launchservices.secure LSHandlers -array-add \
  '{ LSHandlerContentTag = md; LSHandlerContentTagClass = "public.filename-extension"; LSHandlerRoleAll = "com.mdr.app"; }'
defaults write com.apple.LaunchServices/com.apple.launchservices.secure LSHandlers -array-add \
  '{ LSHandlerContentType = "net.daringfireball.markdown"; LSHandlerRoleAll = "com.mdr.app"; }'
killall lsd

# Verify (should print mdr / ~/Applications/mdr.app / com.mdr.app)
brew install duti
duti -x md
```

Notes:

- Finder resolves `.md` to the UTI `net.daringfireball.markdown` (claimed by whichever
  editor declared it first, e.g. Zed), so both the extension and the UTI handler are set.
- `duti -s` is unreliable on recent macOS — it exits 0 without persisting. Use the
  `defaults write` commands above; `duti -x` is still handy for verification.
- Each double-click starts a fresh `mdr` server on a random port, opens the browser,
  and the server shuts itself down shortly after.
- To revert: remove the two `com.mdr.app` entries from
  `defaults read com.apple.LaunchServices/com.apple.launchservices.secure LSHandlers`
  and re-assign the handler via Finder (Get Info → Open with → Change All).
