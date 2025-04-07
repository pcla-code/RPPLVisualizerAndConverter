import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Get the username of the account running this script
username = os.getlogin()

class UsernameHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/get-username":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # ✅ Allow requests from any origin
            self.end_headers()
            self.wfile.write(f'{{"username": "{username}"}}'.encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    server_address = ("0.0.0.0", 9000)  # ✅ Listen on all network interfaces
    httpd = HTTPServer(server_address, UsernameHandler)
    print(f"User accessing visualizer: {username}")
    httpd.serve_forever()
