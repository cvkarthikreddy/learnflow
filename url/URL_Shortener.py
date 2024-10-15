from flask import Flask, redirect, request, render_template, jsonify
import sqlite3
import string
import random

app = Flask(__name__)

# Define the base URL for the shortened URLs
BASE_URL = 'http://127.0.0.1:5000/'

# Initialize the SQLite database
def initialize_db():
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_url TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Generate a random short code
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Insert a long URL and return a short URL
def insert_url_mapping(long_url):
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    short_code = generate_short_url()
    short_url = BASE_URL + short_code
    cursor.execute('''
        INSERT INTO urls (long_url, short_url)
        VALUES (?, ?)
    ''', (long_url, short_url))
    conn.commit()
    conn.close()
    return short_url

# Retrieve the long URL from the short URL
def get_long_url(short_url):
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Handle shortening URL requests
@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_url = insert_url_mapping(long_url)
    return jsonify({'short_url': short_url})

# Handle redirecting short URLs to the long URLs
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    short_url = BASE_URL + short_code
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return 'URL not found', 404

# Initialize the database
initialize_db()

if __name__ == '__main__':
    app.run(debug=True)
