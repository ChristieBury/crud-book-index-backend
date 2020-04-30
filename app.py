from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_heroku import Heroku 

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://hgbwdehzfqbbpc:548c06f48e310caebb0335c08418d3f9ca6d580dbc057c1b2de6a65b2b192641@ec2-52-207-93-32.compute-1.amazonaws.com:5432/d93q2ki6dp74qp"
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
def books_input():
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
    # if request.content_type == 'application/json':
        record = db.session.query(Book).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify('completed Delete action')
    # return jsonify('Delete failed')

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

