'''
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        username = os.getlogin()
        print(f"Logged-in User: {username}")  # Display username in console

    def do_GET(self):
        if self.path == "/username":
            username = os.getlogin()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(username.encode("utf-8"))
            return
        super().do_GET()

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8000)
    httpd = HTTPServer(server_address, CustomHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
'''

from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        username = os.getlogin()
        print(f"Logged-in User: {username}")  # Display username in console

    def do_GET(self):
        if self.path == "/username":
            username = os.getlogin()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(username.encode("utf-8"))
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/save-access":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                payload = json.loads(post_data)
                csv_data = payload.get("csv", "")

                if csv_data:
                    with open("config/access.csv", "w", encoding="utf-8") as f:
                        f.write(csv_data)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Access matrix saved.")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing CSV data.")
            except Exception as e:
                print("Error saving CSV:", e)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal server error.")

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8000)
    httpd = HTTPServer(server_address, CustomHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()