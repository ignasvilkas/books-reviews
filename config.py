import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/book_reviews_db")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
