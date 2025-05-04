from flask import Flask, request, redirect, render_template, jsonify
from models import db, ShortURL
from utils import generate_short_code
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    if short_url:
        return redirect(short_url.url)
    return render_template('index.html', error="Short URL not found")


@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.form
    original_url = data.get('url')
    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    now = datetime.utcnow()

    short_url = ShortURL(
        url=original_url,
        short_code=short_code,
        created_at=now,
        updated_at=now
    )
    db.session.add(short_url)
    db.session.commit()

    return jsonify({
        "id": short_url.id,
        "url": short_url.url,
        "shortCode": short_url.short_code,
        "createdAt": short_url.created_at.isoformat(),
        "updatedAt": short_url.updated_at.isoformat()
    }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

