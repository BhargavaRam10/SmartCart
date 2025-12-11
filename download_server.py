"""
Simple HTTP server to download CSV files
Run this script and open http://localhost:8000 in your browser
"""

import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs

PORT = 8000

class CSVDownloadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Serve HTML page with download links
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>SmartCart - CSV Download</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 50px auto;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    .container {
                        background-color: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    h1 {
                        color: #1f77b4;
                    }
                    .download-link {
                        display: inline-block;
                        margin: 10px 0;
                        padding: 12px 24px;
                        background-color: #1f77b4;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                    }
                    .download-link:hover {
                        background-color: #1565a0;
                    }
                    .file-info {
                        background-color: #f0f2f6;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 15px 0;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🛒 SmartCart - CSV File Downloads</h1>
                    <p>Click the links below to download CSV files:</p>
                    
                    <div class="file-info">
                        <h3>Market Basket Analysis Sample</h3>
                        <p><strong>File:</strong> market_basket_sample.csv</p>
                        <p><strong>Description:</strong> Comprehensive sample dataset with 100 orders, 200+ customers, and 50+ products</p>
                        <a href="/data/market_basket_sample.csv" class="download-link" download>Download market_basket_sample.csv</a>
                    </div>
                    
                    <div class="file-info">
                        <h3>Original Sample Transactions</h3>
                        <p><strong>File:</strong> sample_transactions.csv</p>
                        <p><strong>Description:</strong> Original sample transaction data</p>
                        <a href="/data/sample_transactions.csv" class="download-link" download>Download sample_transactions.csv</a>
                    </div>
                    
                    <div class="file-info">
                        <h3>Sample Customers</h3>
                        <p><strong>File:</strong> sample_customers.csv</p>
                        <p><strong>Description:</strong> Customer metadata</p>
                        <a href="/data/sample_customers.csv" class="download-link" download>Download sample_customers.csv</a>
                    </div>
                    
                    <hr style="margin: 30px 0;">
                    <p style="color: #666; font-size: 14px;">
                        Server running on <strong>http://localhost:8000</strong><br>
                        Press Ctrl+C to stop the server
                    </p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode())
        else:
            # Serve files normally
            super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), CSVDownloadHandler) as httpd:
        print(f"🚀 Download server started!")
        print(f"📥 Open your browser and go to: http://localhost:{PORT}")
        print(f"📁 Files available for download:")
        print(f"   - market_basket_sample.csv")
        print(f"   - sample_transactions.csv")
        print(f"   - sample_customers.csv")
        print(f"\n⏹️  Press Ctrl+C to stop the server\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Thank you!")

