from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/book_reviews_db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover_image = db.Column(db.String(200))
    amazon_link = db.Column(db.String(200))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
