#----------------------------------------------------------------------
# run-visualization.py
# Authors: Amanda Sparks and Luke Shannon
#----------------------------------------------------------------------

import argparse
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='Concurrency.log', help='Log file name')
    args = parser.parse_args()
    
    webbrowser.open_new(f"http://localhost:8000/?file={args.file}")

    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()