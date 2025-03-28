import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)  # Mengizinkan semua origin

# Konfigurasi database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            database=os.environ.get("DB_NAME", "test_db"),
            user=os.environ.get("DB_USER", "student"),
            password=os.environ.get("DB_PASSWORD", "password")
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!"})

# Endpoint untuk membaca data dari tabel 'items'
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM items;")
        rows = cur.fetchall()
        
        items = [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]
        return jsonify(items)
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if conn:
            conn.close()

# Endpoint untuk menambahkan data ke tabel 'items'
@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({"error": "Missing name or description"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;", 
            (data['name'], data['description'])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        
        return jsonify({
            "id": new_id, 
            "name": data['name'], 
            "description": data['description']
        }), 201
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)