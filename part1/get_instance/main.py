# У вас есть модель с книгами и несколько
# записей в БД. Напишите представление которое
# обрабатывает эндпоинт /books/{bookid}
# и возвращает одну книгу, используя сериализацию и
# возвращает данные в формате:
#
# {
#   "author": "Джоан Роулинг",
#   "id": 1,
#   "name": "Гарри Поттер",
#   "year": 1992
# }
#
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    author = fields.Str()
    year = fields.Int()


db.create_all()
b1 = Book(id=1, name="Гарри Поттер", author="Джоан Роулинг", year=1992)
b2 = Book(id=2, name="Граф Монте Кристо", author="Александр Дюма", year=1854)

with db.session.begin():
    db.session.add_all([b1, b2])


@app.route("/books/<int:bid>")
def get_book(bid: int):
    book = Book.query.get(bid)
    bs = BookSchema().dump(book)
    return jsonify(bs)


if __name__ == '__main__':
    app.run(debug=True)
