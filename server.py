import http.server
import socketserver
import os
import mimetypes

PORT = 8085
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class PortfolioHTTPHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def guess_type(self, path):
        if path.lower().split('?')[0].endswith('.pdf'):
            return 'application/pdf'
        return super().guess_type(path)

    def end_headers(self):
        clean_path = self.path.split('?')[0].lower()
        if clean_path.endswith('.pdf'):
            filename = os.path.basename(self.path.split('?')[0])
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == '__main__':
    mimetypes.add_type('application/pdf', '.pdf')
    server_address = ("", PORT)
    httpd = ThreadingHTTPServer(server_address, PortfolioHTTPHandler)
    print(f"Portfolio HTTP Server running on http://localhost:{PORT}")
    httpd.serve_forever()
