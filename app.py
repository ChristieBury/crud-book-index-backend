from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_heroku import Heroku 

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://gvwqejzdwenlje:c292a430dd2b1d5c9abadd98904bee03f68f1f72c39b6a67f4ab56ba25a63bf5@ec2-52-203-160-194.compute-1.amazonaws.com:5432/da134895dapgcv"

heroku = Heroku(app)
db = SQLAlchemy(app)

#creating the empty table
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    author = db.Column(db.String)

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return '<Title%r>' % self.title #f"{self.title}"

@app.route('/')
def home():
    return "<h1>Hi from Flask</h1>"

#filling the slots/rows in the table
@app.route('/book/input', methods=['POST'])
def books_imput():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        reg = Book(title, author)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify('Something went terribly wrong')

@app.route('/books', methods = ['GET'])
def return_books():
    all_books = db.session.query(Book.id, Book.title, 
    Book.author).all()
    return jsonify(all_books)

@app.route('/book/<id>', methods = ['GET'])
def return_single_books(id):
    one_book = db.session.query(Book.id, Book.title, 
    Book.author).filter(Book.id == id).first()
    return jsonify(one_book)

#the D in the CRUD
@app.route('/delete/<id>', methods = ['DELETE'])
def book_delete(id):
    if request.content_type == 'application/json':
        record = db.session.query(Book).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify('completed Delete action')
    return jsonify('Delete failed')

    #update in CRUD
@app.route('/update_book/<id>', methods = ['PUT'])
def book_update(id):
    if request.content_type == 'application/json':
        put_data = request.get_json()
        title = put_data.get('title')
        author = put_data.get('author')
        record = db.session.query(Book).get(id)
        record.title = title
        record.author = author
        db.session.commit()
        return jsonify('Completed Update')
    return jsonify('Failed Update')
#this should be always the end
if __name__ == '__main__':
    app.debug = True
    app.run()

