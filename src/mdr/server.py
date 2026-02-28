"""HTTP server for rendering markdown files."""

import json
import sys
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import unquote

_IDLE_TIMEOUT = 10  # seconds with no requests before auto-shutdown

from mdr.renderer import render_markdown, render_directory


class MdrServer(ThreadingMixIn, HTTPServer):
    """Threaded HTTP server that holds mdr configuration."""
    daemon_threads = True

    def __init__(self, server_address, handler_class, *, path: Path, mode: str):
        self.target_path = path
        self.mode = mode  # "file" or "directory"
        self.last_request_time = time.monotonic()
        super().__init__(server_address, handler_class)


class MdrHandler(BaseHTTPRequestHandler):
    """Request handler for mdr routes."""

    server: MdrServer

    def log_message(self, format, *args):
        # Suppress default stderr logging for cleaner output
        pass

    def do_GET(self):
        self.server.last_request_time = time.monotonic()
        path = unquote(self.path)

        if path == "/api/mtime":
            self._handle_mtime()
        elif self.server.mode == "file":
            self._handle_file()
        else:
            self._handle_directory(path)

    def _handle_mtime(self):
        """Return JSON with file modification time for live reload."""
        if self.server.mode == "file":
            target = self.server.target_path
        else:
            # In directory mode, mtime isn't meaningful for a single file
            # Return directory mtime instead
            target = self.server.target_path

        try:
            mtime = target.stat().st_mtime
        except OSError:
            mtime = 0

        self._send_json({"mtime": mtime})

    def _handle_file(self):
        """Render the single target markdown file."""
        try:
            text = self.server.target_path.read_text(encoding="utf-8")
        except OSError as e:
            self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
            return

        html = render_markdown(text, self.server.target_path.name)
        self._send_html(html)

    def _handle_directory(self, url_path: str):
        """Serve directory listing or render a specific markdown file."""
        base = self.server.target_path

        if url_path == "/" or url_path == "":
            html = render_directory(base)
            self._send_html(html)
            return

        # Strip leading slash, resolve the requested file
        relative = url_path.lstrip("/")

        # Handle subdirectory requests
        if relative.endswith("/"):
            subdir = base / relative.rstrip("/")
            if subdir.is_dir() and _is_safe_path(base, subdir):
                html = render_directory(subdir)
                self._send_html(html)
                return
            self._send_error(HTTPStatus.NOT_FOUND, "Directory not found")
            return

        target = base / relative

        # Path traversal prevention
        if not _is_safe_path(base, target):
            self._send_error(HTTPStatus.FORBIDDEN, "Access denied")
            return

        if not target.exists() or not target.is_file():
            self._send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        if target.suffix.lower() != ".md":
            self._send_error(HTTPStatus.FORBIDDEN, "Only .md files are served")
            return

        text = target.read_text(encoding="utf-8")
        html = render_markdown(text, target.name)
        self._send_html(html)

    def _send_html(self, html: str):
        data = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, obj):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_error(self, status: HTTPStatus, message: str):
        data = message.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def _is_safe_path(base: Path, target: Path) -> bool:
    """Check that target is inside base (prevent path traversal)."""
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def serve(path: Path, mode: str, port: int = 0, open_browser: bool = True):
    """Start the mdr server and optionally open a browser."""
    server = MdrServer(("127.0.0.1", port), MdrHandler, path=path, mode=mode)
    host, actual_port = server.server_address

    url = f"http://127.0.0.1:{actual_port}"
    print(f"mdr serving {path} at {url}")
    print("Press Ctrl+C to stop")

    if open_browser:
        webbrowser.open(url)

    # Watchdog: shut down when no requests received for _IDLE_TIMEOUT seconds
    def _watchdog():
        while True:
            time.sleep(2)
            idle = time.monotonic() - server.last_request_time
            if idle >= _IDLE_TIMEOUT:
                print("\nNo active clients, shutting down.")
                server.shutdown()
                return

    watchdog = threading.Thread(target=_watchdog, daemon=True)
    watchdog.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.shutdown()
