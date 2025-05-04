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

    # Generate a unique short code
    short_code = generate_short_code()

    # Store the URL
    urls[short_code] = {
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
        access_count[short_code] += 1  # Increment access count
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
    """Update an existing short URL with a new short code"""
    data = request.get_json()
    new_short_code = data.get('shortCode')

    if not new_short_code:
        return jsonify({"error": "New short code is required"}), 400

    url_data = urls.get(short_code)

    if not url_data:
        return jsonify({"error": "Short code not found"}), 404

    # Update the short code and other properties
    url_data['shortCode'] = new_short_code
    url_data['updatedAt'] = datetime.now().isoformat()

    # Move the access count to the new short code if it exists
    if short_code in access_count:
        access_count[new_short_code] = access_count[short_code]
        del access_count[short_code]

    # Remove the old short code and add the new one
    del urls[short_code]
    urls[new_short_code] = url_data

    return jsonify(url_data)

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    """Delete an existing short URL"""
    if short_code in urls:
        del urls[short_code]
        del access_count[short_code]
        return '', 204
    
    return jsonify({"error": "Short code not found"}), 404

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_statistics(short_code):
    """Get statistics (access count) for a short URL"""
    if short_code in access_count:
        return jsonify({
            "shortCode": short_code,
            "accessCount": access_count[short_code]
        })
    
    return jsonify({"error": "Short code not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
