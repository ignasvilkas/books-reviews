from app import db, Book, Review
from app import app  # Assuming `app` is the Flask instance in `app.py`

with app.app_context():
    # Remove all reviews and books
    Review.query.delete()
    Book.query.delete()
    db.session.commit()
    print("All books and reviews have been deleted.")
