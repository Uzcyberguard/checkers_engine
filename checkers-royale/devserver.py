"""
Local stand-in for the Vercel Python functions.

On Vercel each file in api/ becomes its own function and the path maps to the
filename. This serves the same modules on one port so `npm run dev` has an API
to talk to. Production never runs this file.

    python devserver.py            # http://127.0.0.1:5328
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from _lib.service import ApiError, ROUTES  # noqa: E402

PORT = int(os.environ.get("PORT", "5328"))


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _respond(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _handle(self):
        parsed = urlparse(self.path)
        name = parsed.path.rsplit("/", 1)[-1] or "new"
        action = ROUTES.get(name)
        if action is None:
            self._respond(404, {"error": "no such endpoint: {}".format(name)})
            return

        length = int(self.headers.get("Content-Length") or 0)
        if length:
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except ValueError:
                self._respond(400, {"error": "body must be valid JSON"})
                return
        else:
            payload = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        try:
            self._respond(200, action(payload))
        except ApiError as exc:
            self._respond(exc.status, {"error": exc.message})
        except Exception as exc:  # pragma: no cover
            import traceback

            traceback.print_exc()
            self._respond(500, {"error": "engine failure: {}".format(exc)})

    def do_POST(self):
        self._handle()

    def do_GET(self):
        self._handle()

    def do_OPTIONS(self):
        self._respond(200, {"ok": True})

    def log_message(self, fmt, *args):
        sys.stderr.write("  api %s\n" % (fmt % args))


if __name__ == "__main__":
    print(f"engine API listening on http://127.0.0.1:{PORT}")
    print(f"routes: {', '.join('/api/' + name for name in sorted(ROUTES))}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
