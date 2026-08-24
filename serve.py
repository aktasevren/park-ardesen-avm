#!/usr/bin/env python3
import http.server, socketserver, sys, os
from http.server import ThreadingHTTPServer
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
        '.avif':'image/avif', '.webm':'video/webm', '.mp4':'video/mp4',
        '.js':'text/javascript', '.mjs':'text/javascript', '.css':'text/css',
        '.woff2':'font/woff2', '.woff':'font/woff', '.svg':'image/svg+xml',
        '.json':'application/json', '.glb':'model/gltf-binary', '.wasm':'application/wasm'}
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        self.send_header('Access-Control-Allow-Origin','*')
        super().end_headers()
    def log_message(self, fmt, *a): pass
class TS(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
with TS(("127.0.0.1", PORT), H) as httpd:
    print(f"Serving {os.getcwd()} at http://127.0.0.1:{PORT}/ (threaded)")
    httpd.serve_forever()
