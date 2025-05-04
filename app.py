from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# URL Model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    access_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(db.String(30), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Helper function
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    short_code = generate_short_code()
    timestamp = datetime.utcnow().isoformat()

    new_url = URL(
        url=original_url,
        short_code=short_code,
        created_at=timestamp,
        updated_at=timestamp
    )
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'id': new_url.id,
        'url': new_url.url,
        'shortCode': new_url.short_code,
        'createdAt': new_url.created_at,
        'updatedAt': new_url.updated_at
    }), 201

# Retrieve URL metadata (via API)
@app.route('/shorten/<short_code>', methods=['GET'])
def retrieve_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    url.access_count += 1
    db.session.commit()

    return jsonify({
        'id': url.id,
        'url': url.url,
        'shortCode': url.short_code,
        'createdAt': url.created_at,
        'updatedAt': url.updated_at,
        'accessCount': url.access_count
    }), 200

# Redirect to original URL
@app.route('/<short_code>')
def redirect_to_original(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        url.access_count += 1
        db.session.commit()
        return redirect(url.url)
    return "Short URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)

