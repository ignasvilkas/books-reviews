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
                   "demons while seeking justice for his fallen comrades.")
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "cover_image": "images/1984.jpg",
        "review": ("George Orwell’s '1984' remains a timeless exploration of totalitarianism and the chilling effects "
                   "of state surveillance on individual freedom. Set in a dystopian future, the story follows Winston "
                   "Smith as he grapples with his desire for truth and love in a world where privacy is obliterated.")
    },
    {
        "title": "On the Road",
        "author": "Jack Kerouac",
        "cover_image": "images/on_the_road.jpg",
        "review": ("'On the Road' is a seminal work of American literature that captures the spirit of the Beat "
                   "Generation through the lens of its iconic protagonist, Sal Paradise. Kerouac’s narrative chronicles "
                   "the adventures of Sal and his friends in search of meaning and freedom.")
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "cover_image": "images/the_great_gatsby.jpg",
        "review": ("In 'The Great Gatsby,' Fitzgerald explores themes of decadence and idealism in the context of 1920s America, "
                   "narrated through the eyes of Nick Carraway as he observes the mysterious Jay Gatsby.")
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "cover_image": "images/to_kill_a_mockingbird.jpg",
        "review": ("Harper Lee's 'To Kill a Mockingbird' delves into themes of racial injustice and moral growth, "
                   "as seen through the eyes of Scout Finch in the racially charged South of the 1930s.")
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "cover_image": "images/pride_and_prejudice.jpg",
        "review": ("'Pride and Prejudice' is a romantic novel that critiques the British landed gentry at the end of the 18th century, "
                   "focusing on Elizabeth Bennet's turbulent relationship with the enigmatic Mr. Darcy.")
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "cover_image": "images/the_catcher_in_the_rye.jpg",
        "review": ("J.D. Salinger's 'The Catcher in the Rye' tells the story of Holden Caulfield, a teenager navigating the complexities of adolescence "
                   "and his disdain for the adult world.")
    },
    {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "cover_image": "images/brave_new_world.jpg",
        "review": ("In 'Brave New World,' Huxley presents a dystopian future where society is engineered for maximum happiness, "
                   "raising questions about freedom and individuality.")
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "cover_image": "images/the_alchemist.jpg",
        "review": ("Paulo Coelho's 'The Alchemist' is an allegorical novel about a shepherd named Santiago who dreams of finding a hidden treasure, "
                   "embarking on a journey of self-discovery.")
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "cover_image": "images/the_hobbit.jpg",
        "review": ("'The Hobbit' follows the adventures of Bilbo Baggins as he joins a group of dwarves on a quest to reclaim their homeland from the dragon Smaug.")
    },
    {
        "title": "The Road",
        "author": "Cormac McCarthy",
        "cover_image": "images/the_road.jpg",
        "review": ("In 'The Road,' McCarthy depicts a post-apocalyptic world through the journey of a father and his son, exploring themes of survival and hope.")
    },
    {
        "title": "Fahrenheit 451",
        "author": "Ray Bradbury",
        "cover_image": "images/fahrenheit_451.jpg",
        "review": ("Ray Bradbury's 'Fahrenheit 451' explores a future society where books are banned and 'firemen' burn any that are found, raising questions about censorship and knowledge.")
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
