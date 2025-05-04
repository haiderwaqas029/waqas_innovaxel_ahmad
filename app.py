from flask import Flask, request, jsonify, render_template, redirect
import random
import string
from datetime import datetime

app = Flask(__name__)

# In-memory storage for URL data
urls = {}
access_count = {}

def generate_short_code(length=6):
    """Generates a random short code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Create a new short URL"""
    data = request.get_json()
    long_url = data.get('url')

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    # Ensure URL starts with http:// or https://
    if not (long_url.startswith('http://') or long_url.startswith('https://')):
        long_url = 'http://' + long_url

    # Generate a unique short code
    while True:
        short_code = generate_short_code()
        if short_code not in urls:
            break

    # Store the URL
    urls[short_code] = {
        'id': short_code,
        'url': long_url,
        'shortCode': short_code,
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    access_count[short_code] = 0  # Initialize access count

    return jsonify(urls[short_code]), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect short URL to original URL"""
    url_data = urls.get(short_code)
    
    if url_data:
        # Initialize access count if it doesn't exist
        if short_code not in access_count:
            access_count[short_code] = 0
        access_count[short_code] += 1
        return redirect(url_data['url'])
    
    return jsonify({"error": "Short code not found"}), 404

@app.route('/shorten/<short_code>', methods=['GET'])
def retrieve_url(short_code):
    """Retrieve original URL from short code"""
    url_data = urls.get(short_code)
    
    if url_data:
        return jsonify(url_data)
    
    return jsonify({"error": "Short code not found"}), 404

@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    """Update an existing short URL"""
    data = request.get_json()
    new_url = data.get('url')

    if not new_url:
        return jsonify({"error": "URL is required"}), 400

    # Ensure URL starts with http:// or https://
    if not (new_url.startswith('http://') or new_url.startswith('https://')):
        new_url = 'http://' + new_url

    url_data = urls.get(short_code)

    if not url_data:
        return jsonify({"error": "Short code not found"}), 404

    # Update the URL
    url_data['url'] = new_url
    url_data['updatedAt'] = datetime.now().isoformat()

    return jsonify(url_data)

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    """Delete an existing short URL"""
    if short_code in urls:
        # Delete from both dictionaries
        del urls[short_code]
        if short_code in access_count:
            del access_count[short_code]
        return '', 204
    
    return jsonify({"error": "Short code not found"}), 404

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_statistics(short_code):
    """Get statistics for a short URL"""
    url_data = urls.get(short_code)
    
    if url_data:
        return jsonify({
            **url_data,
            "accessCount": access_count.get(short_code, 0)
        })
    
    return jsonify({"error": "Short code not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
