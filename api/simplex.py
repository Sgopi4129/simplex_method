import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backend.simplex import SimplexMethod


class handler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        self._send_json({})

    def do_POST(self):
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
