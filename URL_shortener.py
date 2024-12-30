import hashlib
import string
import random
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Dictionary to store the long URL and corresponding shortened URL
url_mapping = {}

# Function to generate a short URL
def generate_short_url(long_url):
    # Create a hash of the long URL
    hash_object = hashlib.md5(long_url.encode())
    short_hash = hash_object.hexdigest()[:6]  # Take first 6 characters of the hash
    return short_hash

# Route for the home page
@app.route('/')
def home():
    return render_template_string('''
    <h1>URL Shortener</h1>
    <form action="/shorten" method="post">
        <label for="url">Enter your URL to shorten:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">Shorten</button>
    </form>
    ''')

# Route to handle URL shortening
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    
    if long_url in url_mapping:
        short_url = url_mapping[long_url]
    else:
        short_url = generate_short_url(long_url)
        url_mapping[long_url] = short_url  # Store mapping in dictionary
    
    short_url_link = request.host_url + short_url
    return f'<h1>Shortened URL:</h1><p>Your shortened URL is: <a href="{short_url_link}">{short_url_link}</a></p>'

# Route to handle redirection from the short URL
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    # Find the long URL corresponding to the short URL
    for long_url, short in url_mapping.items():
        if short == short_url:
            return redirect(long_url)
    
    return "URL not found", 404

# Run the Flask web application
if __name__ == '__main__':
    app.run(debug=True)
