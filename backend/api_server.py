import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from simplex import SimplexMethod


class SimplexAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        self._send_json({})

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
