import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BACKEND_DIR = str(Path(__file__).resolve().parent)
if BACKEND_DIR in sys.path:
    sys.path.remove(BACKEND_DIR)

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from backend.simplex import SimplexMethod


def get_allowed_origins():
    raw = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["http://localhost:3000", "http://127.0.0.1:3000"]


class SimplexAPIHandler(BaseHTTPRequestHandler):
    def _allowed_origin(self):
        origin = self.headers.get("Origin")
        if origin in get_allowed_origins():
            return origin
        return get_allowed_origins()[0]

    def _send_json(self, payload, status=200):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", self._allowed_origin())
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        self._send_json({})

    def do_GET(self):
        if self.path == "/health":
            self._send_json({"status": "ok"})
            return
        self._send_json({"error": "Endpoint not found."}, 404)

    def do_POST(self):
        if self.path != "/solve":
            self._send_json({"error": "Endpoint not found."}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            result = SimplexMethod(
                data["objective"],
                data["constraints"],
                data["limits"],
                data.get("relations"),
                data.get("sense", "max"),
            ).solve()
            self._send_json({"solution": result["solution"], "maximum": result["maximum"]})
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            self._send_json({"error": str(error)}, 400)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), SimplexAPIHandler)
    print(f"Simplex API listening on port {port}")
    server.serve_forever()
