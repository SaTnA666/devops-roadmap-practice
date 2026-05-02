import json
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

# DevOps-магия: мы не пишем пароли в коде! Мы берем их из системы (от Docker Compose)
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "shop_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "superpassword")
DB_NAME = os.environ.get("DB_NAME", "autoparts_db")

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)

def init_db():
    # Даем базе пару секунд на запуск
    time.sleep(2) 
    conn = get_db_connection()
    cur = conn.cursor()
    # Создаем таблицу, если ее еще нет
    cur.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            car VARCHAR(100),
            price INTEGER
        )
    ''')
    # Если таблица пустая, заливаем туда стартовые данные
    cur.execute('SELECT COUNT(*) FROM parts')
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO parts (name, car, price) VALUES ('Тормозные колодки Brembo', 'Toyota Camry', 4500)")
        cur.execute("INSERT INTO parts (name, car, price) VALUES ('Масляный фильтр MANN', 'Universal', 800)")
        cur.execute("INSERT INTO parts (name, car, price) VALUES ('Фара левая', 'Lada Vesta', 3200)")
    
    conn.commit()
    cur.close()
    conn.close()

class AutoPartsAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/parts':
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            # Теперь мы берем данные реально из базы!
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, car, price FROM parts")
            rows = cur.fetchall()
            
            parts = [{"id": row[0], "name": row[1], "car": row[2], "price": row[3]} for row in rows]
            
            cur.close()
            conn.close()
            
            self.wfile.write(json.dumps(parts, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    print("Подключение к базе данных...")
    try:
        init_db()
        print("База данных успешно инициализирована!")
    except Exception as e:
        print(f"Ошибка БД: {e}")
        
    server = HTTPServer(('0.0.0.0', 8080), AutoPartsAPI)
    print("API Магазина запущено на порту 8080...")
    server.serve_forever()