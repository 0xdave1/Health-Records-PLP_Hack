from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Password123",
    "database": "school_health"
}

def get_db_connection():
    """Create and return a new database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        logger.error(f"Database connection failed: {err}")
        raise

@app.route('/register_school', methods=['POST'])
def register_school():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'email', 'password']):
            return jsonify({"error": "Missing required fields"}), 400

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Hash the password before storing
        hashed_password = generate_password_hash(data['password'])
        sql = "INSERT INTO schools (name, email, password) VALUES (%s, %s, %s)"
        values = (data['name'], data['email'], hashed_password)
        
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "School registered successfully!"}), 201
    
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

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
    
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

@app.route('/get_records', methods=['GET'])
def get_records():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT name, health_issue, DATE_FORMAT(date, '%Y-%m-%d') as date FROM health_records")
        result = cursor.fetchall()
        
        if not result:
            return jsonify([]), 200
            
        return jsonify(result), 200
    
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
