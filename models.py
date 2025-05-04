from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    access_count = db.Column(db.Integer, default=0)

