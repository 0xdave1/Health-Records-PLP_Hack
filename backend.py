from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
import logging
from werkzeug.security import generate_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    "host": "localhost",  # Hard-coded for now
    "user": "root",
    "password": "Password123",  # Update this with your MySQL root password
    "database": "school_health"
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        logger.error(f"Database connection failed: {err}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_school', methods=['POST'])
def register_school():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'email', 'password']):
            return jsonify({"error": "Missing required fields"}), 400
            
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Check if school already exists
        cursor.execute("SELECT id FROM schools WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({"error": "School already registered"}), 409
        
        # Hash password and insert school
        hashed_password = generate_password_hash(data['password'])
        sql = "INSERT INTO schools (name, email, password) VALUES (%s, %s, %s)"
        values = (data['name'], data['email'], hashed_password)
        
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "School registered successfully!"}), 201
    
    except Exception as e:
        logger.error(f"Error registering school: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'age', 'class']):
            return jsonify({"error": "Missing required fields"}), 400
            
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        sql = "INSERT INTO students (name, age, class_name) VALUES (%s, %s, %s)"
        values = (data['name'], data['age'], data['class'])
        
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "Student added successfully!"}), 201
    
    except Exception as e:
        logger.error(f"Error adding student: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

@app.route('/get_records', methods=['GET'])
def get_records():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT h.name, h.health_issue, DATE_FORMAT(h.date, '%Y-%m-%d') as date 
            FROM health_records h 
            ORDER BY h.date DESC
        """)
        records = cursor.fetchall()
        
        if not records:
            return jsonify([]), 200
            
        return jsonify(records), 200
    
    except Exception as e:
        logger.error(f"Error fetching records: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

if __name__ == '__main__':
    try:
        # Test database connection on startup
        db = get_db_connection()
        db.close()
        logger.info("Database connection successful")
        
        port = int(os.getenv('PORT', 5000))
        app.run(debug=True, host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Startup error: {e}")
