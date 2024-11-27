import os
from flask import Flask, render_template, jsonify
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get database configuration from environment variables
db_host = os.getenv('MYSQL_HOST', 'localhost')
db_user = os.getenv('MYSQL_USER', 'root')
db_password = os.getenv('MYSQL_PASSWORD', '')
db_name = os.getenv('MYSQL_DATABASE', 'webcountdb')

# Establish a connection to the MySQL database using the environment variables
db = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

@app.route('/')
def home():
    with db.cursor() as cursor:
        # Create the visit_count table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visit_count (
                day DATE PRIMARY KEY,
                count INT
            )
        """)
        # Insert a record for today's date or update the count if it already exists
        cursor.execute("""
            INSERT INTO visit_count (day, count)
            VALUES (CURDATE(), 1)
            ON DUPLICATE KEY UPDATE count = count + 1
        """)
        db.commit()
        # Get the current visit count for today
        cursor.execute("SELECT count FROM visit_count WHERE day = CURDATE()")
        visit_count = cursor.fetchone()[0]
    
    # Render the HTML template and pass the visit count to it
    return render_template('index.html', visit_count=visit_count)

@app.route('/reset', methods=['POST'])
def reset():
    with db.cursor() as cursor:
        # Reset the visit count to zero for today
        cursor.execute("""
            UPDATE visit_count
            SET count = 0
            WHERE day = CURDATE()
        """)
        db.commit()
        # Get the updated visit count
        cursor.execute("SELECT count FROM visit_count WHERE day = CURDATE()")
        visit_count = cursor.fetchone()[0]
    
    # Return the updated visit count as JSON
    return jsonify({'visit_count': visit_count})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)