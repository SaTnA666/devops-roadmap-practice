from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class AutoPartsAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/parts':
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            parts = [
                {"id": 1, "name": "Тормозные колодки Brembo", "car": "Toyota Camry", "price": 4500},
                {"id": 2, "name": "Масляный фильтр MANN", "car": "Universal", "price": 800},
                {"id": 3, "name": "Свечи зажигания NGK", "car": "Ford Focus", "price": 2100}
            ]
            
            self.wfile.write(json.dumps(parts, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8080), AutoPartsAPI)
    print("API Магазина Автозапчастей запущено на порту 8080...")
    server.serve_forever()