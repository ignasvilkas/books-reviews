from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover_image = db.Column(db.String(300), nullable=False)
    review = db.Column(db.Text, nullable=True)
    reviews = db.relationship('Review', backref='book', cascade="all, delete-orphan", lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

# Initialize static data
initial_books = [
    {
        "title": "Terminal List",
        "author": "Jack Carr",
        "cover_image": "images/terminal_list.jpg",
        "review": ("In 'Terminal List,' former Navy SEAL James Reece embarks on a personal journey of revenge "
                   "after discovering a conspiracy that leads to the deaths of his entire platoon. This gripping "
                   "thriller combines military action with psychological depth, as Reece struggles with his inner "
                   "demons while seeking justice for his fallen comrades. Carr's firsthand experience in the Navy "
                   "adds authenticity to the narrative, creating a pulse-pounding story filled with unexpected "
                   "twists and high-stakes drama. It's a tale of betrayal, loyalty, and the complexities of warfare "
                   "that will keep readers on the edge of their seats until the final page.")
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "cover_image": "images/1984.jpg",
        "review": ("George Orwell’s '1984' remains a timeless exploration of totalitarianism and the chilling effects "
                   "of state surveillance on individual freedom. Set in a dystopian future, the story follows Winston "
                   "Smith, a low-ranking member of the Party, as he grapples with his desire for truth and love in "
                   "a world where privacy is obliterated, and the government manipulates reality. Orwell's haunting "
                   "prose and vivid imagery craft a chilling atmosphere that resonates with modern readers, urging "
                   "them to reflect on the importance of personal autonomy in the face of oppressive regimes. The "
                   "novel serves as a stark warning against the erosion of truth and the loss of individuality, making "
                   "it a crucial read in today’s society.")
    },
    {
        "title": "On the Road",
        "author": "Jack Kerouac",
        "cover_image": "images/on_the_road.jpg",
        "review": ("'On the Road' is a seminal work of American literature that captures the spirit of the Beat "
                   "Generation through the lens of its iconic protagonist, Sal Paradise. Kerouac’s semi-autobiographical "
                   "narrative chronicles the adventures of Sal and his friends as they traverse the United States in "
                   "search of meaning, connection, and freedom. The novel is a vibrant tapestry of experiences, friendships, "
                   "and the open road, infused with a sense of urgency and spontaneity that reflects the restlessness of "
                   "youth. Kerouac's free-spirited prose and rich descriptions evoke the beauty of the American landscape, "
                   "inviting readers to join in the quest for self-discovery and the celebration of life’s fleeting moments. "
                   "It’s an exhilarating ride that remains relevant to anyone seeking to break free from societal constraints.")
    }
]

# Load initial data
with app.app_context():
    db.create_all()
    for book_data in initial_books:
        if not Book.query.filter_by(title=book_data["title"]).first():
            book = Book(**book_data)
            db.session.add(book)
    db.session.commit()

# Routes
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cover_image = request.form['cover_image']
        review = request.form['review']
        new_book = Book(title=title, author=author, cover_image=cover_image, review=review)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        review_content = request.form['review']
        new_review = Review(content=review_content, book_id=book.id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('book_details', book_id=book.id))
    return render_template('book_details.html', book=book)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
