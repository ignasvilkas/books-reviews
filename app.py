# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Book, Review

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

# Add sample data once
def add_sample_data():
    sample_books = [
        Book(
            title="Terminal List",
            author="Jack Carr",
            cover_image="https://m.media-amazon.com/images/I/71La9HeC1-L._AC_UF894,1000_QL80_.jpg",
            amazon_link="https://www.amazon.com/s?tag=faketag&k=terminal+list+jack+carr"
        ),
        Book(
            title="1984",
            author="George Orwell",
            cover_image="https://m.media-amazon.com/images/I/61ZewDE3beL._AC_UF894,1000_QL80_.jpg",
            amazon_link="https://www.amazon.com/s?tag=faketag&k=1984+george+orwell"
        ),
        Book(
            title="On the Road",
            author="Jack Kerouac",
            cover_image="https://m.media-amazon.com/images/I/71g1iYhvtKL._AC_UF894,1000_QL80_.jpg",
            amazon_link="https://www.amazon.com/s?tag=faketag&k=on+the+road+jack+kerouac"
        ),
    ]
    db.session.bulk_save_objects(sample_books)
    db.session.commit()

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template('book_details.html', book=book, reviews=reviews)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cover_image = request.form['cover_image']
        amazon_link = request.form['amazon_link']
        new_book = Book(title=title, author=author, cover_image=cover_image, amazon_link=amazon_link)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

if __name__ == "__main__":
    app.run(debug=True)
