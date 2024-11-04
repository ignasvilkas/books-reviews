from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "cover_image": "images/great_gatsby.jpg",
        "review": ("Set in the Roaring Twenties, 'The Great Gatsby' is a tale of love, wealth, and the American Dream. "
                   "Through the eyes of Nick Carraway, we explore the lavish lifestyle of Jay Gatsby, a mysterious millionaire, "
                   "and his obsession with the beautiful Daisy Buchanan. Fitzgerald's poignant prose and vivid imagery paint "
                   "a picture of a society consumed by excess and the unattainable nature of dreams. This classic novel serves "
                   "as a critical reflection on the disillusionment that often accompanies success and the fragility of human "
                   "relationships.")
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "cover_image": "images/to_kill_a_mockingbird.jpg",
        "review": ("'To Kill a Mockingbird' is a powerful exploration of racial injustice in the Deep South, told through the "
                   "innocent eyes of Scout Finch. As her father, Atticus Finch, defends a black man accused of raping a white "
                   "woman, Scout learns about the complexities of human nature, morality, and empathy. Harper Lee's timeless "
                   "narrative, rich with Southern charm and poignant social commentary, invites readers to confront their own "
                   "prejudices and consider the importance of standing up for what is right.")
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "cover_image": "images/pride_and_prejudice.jpg",
        "review": ("In 'Pride and Prejudice,' Jane Austen presents a delightful tale of love and societal expectations in "
                   "19th century England. The story follows the spirited Elizabeth Bennet as she navigates issues of class, "
                   "marriage, and individuality, ultimately leading to a deeper understanding of herself and her feelings "
                   "for the enigmatic Mr. Darcy. Austen's witty dialogue and keen observations of human behavior make this "
                   "novel a timeless classic, inviting readers to reflect on the complexities of love and the importance "
                   "of personal growth.")
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "cover_image": "images/catcher_in_the_rye.jpg",
        "review": ("J.D. Salinger's 'The Catcher in the Rye' is a poignant exploration of teenage angst and alienation. "
                   "The novel follows Holden Caulfield, a disenchanted adolescent, as he grapples with the complexities "
                   "of adulthood and his deep-seated desire to protect the innocence of childhood. Salinger's distinctive "
                   "narrative style and raw emotion resonate with readers, making this coming-of-age story a profound "
                   "reflection on the challenges of growing up and finding one's place in the world.")
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "cover_image": "images/the_alchemist.jpg",
        "review": ("'The Alchemist' is a captivating tale of self-discovery and the pursuit of dreams. Following the journey "
                   "of Santiago, a young shepherd, the story unfolds as he seeks a hidden treasure in the Egyptian pyramids. "
                   "Coelho's lyrical prose and philosophical insights encourage readers to listen to their hearts and pursue "
                   "their own personal legends. This inspiring novel resonates with anyone who has ever dared to chase their "
                   "dreams.")
    },
    {
        "title": "The Picture of Dorian Gray",
        "author": "Oscar Wilde",
        "cover_image": "images/picture_of_dorian_gray.jpg",
        "review": ("In 'The Picture of Dorian Gray,' Oscar Wilde crafts a mesmerizing tale of vanity, moral corruption, "
                   "and the quest for eternal youth. Dorian Gray, a young man whose portrait ages while he remains youthful, "
                   "finds himself drawn into a hedonistic lifestyle that ultimately leads to his downfall. Wilde's masterful "
                   "use of language and exploration of the duality of human nature make this novel a timeless exploration of "
                   "the consequences of excess and the search for identity.")
    },
    {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "cover_image": "images/brave_new_world.jpg",
        "review": ("Aldous Huxley’s 'Brave New World' presents a chilling vision of a dystopian future where individuality "
                   "is sacrificed for societal stability. Set in a world governed by technology and conformity, the story "
                   "follows Bernard Marx as he grapples with his dissatisfaction with the rigid norms of his society. Huxley's "
                   "thought-provoking narrative raises important questions about the cost of progress and the value of human "
                   "emotion in a controlled world.")
    },
    {
        "title": "Fahrenheit 451",
        "author": "Ray Bradbury",
        "cover_image": "images/fahrenheit_451.jpg",
        "review": ("In 'Fahrenheit 451,' Ray Bradbury envisions a future where books are banned, and 'firemen' burn any that "
                   "are found. The story follows Guy Montag, a fireman who begins to question the oppressive society in which "
                   "he lives. Through Montag's journey, Bradbury explores themes of censorship, the importance of literature, "
                   "and the power of individual thought. This classic novel serves as a powerful warning against the dangers "
                   "of complacency in the face of authoritarianism.")
    },
    {
        "title": "The Road",
        "author": "Cormac McCarthy",
        "cover_image": "images/the_road.jpg",
        "review": ("'The Road' is a haunting tale of survival in a post-apocalyptic world. Following a father and his young son, "
                   "the story explores themes of love, hope, and the enduring human spirit amidst desolation. McCarthy's spare, "
                   "poetic prose immerses readers in the stark realities of their journey, making the bond between parent and child "
                   "the focal point of a narrative filled with despair and fleeting moments of beauty.")
    },
    {
        "title": "Life of Pi",
        "author": "Yann Martel",
        "cover_image": "images/life_of_pi.jpg",
        "review": ("In 'Life of Pi,' Yann Martel tells the extraordinary story of Pi Patel, a young boy stranded on a lifeboat "
                   "with a Bengal tiger after a shipwreck. The novel is a rich exploration of faith, survival, and the human spirit, "
                   "blending adventure with philosophical reflection. Martel's narrative invites readers to ponder the nature of reality "
                   "and the power of storytelling in shaping our understanding of the world.")
    },
      {
        "title": "The Night Circus",
        "author": "Erin Morgenstern",
        "cover_image": "images/the_night_circus.jpg",
        "review": ("In 'The Night Circus,' Erin Morgenstern weaves a mesmerizing tale of magic and competition set in a "
                   "mysterious circus that appears only at night. The story follows two young illusionists, Celia and Marco, "
                   "who are bound to a fierce rivalry that transcends the confines of the circus. With enchanting prose and "
                   "vivid imagery, Morgenstern creates a world where dreams and reality intertwine, making this novel a "
                   "captivating exploration of love, ambition, and the transformative power of imagination.")
    }
]




with app.app_context():
    db.create_all()
    for book_data in initial_books:
        if not Book.query.filter_by(title=book_data["title"]).first():
            book = Book(**book_data)
            db.session.add(book)
    db.session.commit()

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
