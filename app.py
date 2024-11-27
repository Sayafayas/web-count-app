import os
from flask import Flask
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
        cursor.execute("CREATE TABLE IF NOT EXISTS visit_count (day DATE, count INT)")
        cursor.execute("INSERT INTO visit_count (day, count) VALUES (CURDATE(), 1) ON DUPLICATE KEY UPDATE count = count + 1")
        db.commit()
        cursor.execute("SELECT count FROM visit_count WHERE day = CURDATE()")
        visit_count = cursor.fetchone()[0]
    return f"Website visit count for today: {visit_count}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
