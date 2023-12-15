#----------------------------------------------------------------------
# run-visualization.py
# Authors: Amanda Sparks and Luke Shannon
#----------------------------------------------------------------------

import argparse
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default='Concurrency.log', help='Log file name')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port to host visualization on')
    args = parser.parse_args()
    
    webbrowser.open_new(f"http://localhost:{args.port}/?file={args.file}")

    httpd = HTTPServer(('localhost', args.port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()