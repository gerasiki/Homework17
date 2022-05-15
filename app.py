# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movies_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

    def __repr__(self):
        return self.title


class MoviesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

movies_schema = MoviesSchema(many=True)
movie_schema = MoviesSchema()

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

@movies_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies = Movie.query

        if director_id:
            movies = movies.filter(Movie.director_id == director_id)
        if genre_id:
            movies = movies.filter(Movie.genre_id == genre_id)
        movies = movies.all()
        return movies_schema.dump(movies), 200

    def post(self):
        data = request.get_json()
        movie = Movie(**data)
        db.session.add(movie)
        db.session.commit()
        db.session.close()

        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        return movie_schema.dump(movie), 200

    def put(self, mid):
        data = request.get_json()
        movie = Movie.query.get(mid)
        movie.id = data['id']
        movie.title = data['title']
        movie.description = data['description']
        movie.trailer = data['trailer']
        movie.year = data['year']
        movie.rating = data['rating']
        movie.genre_id = data['genre_id']
        movie.director_id = data['director_id']

        db.session.add(movie)
        db.session.commit()
        db.session.close()

        return '', 204

    def delete(self, mid):
        movie = Movie.query.get(mid)

        db.session.delete(movie)
        db.session.commit()
        db.session.close()


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        data = request.get_json()
        director = Director(**data)
        db.session.add(director)
        db.session.commit()
        db.session.close()

        return "", 201

@director_ns.route('/<int:mid>')
class DirectorView(Resource):
    def get(self, mid):
        director = Director.query.get(mid)
        return director_schema.dump(director), 200

    def put(self, mid):
        data = request.get_json()
        director = Director.query.get(mid)
        director.id = data['id']
        director.name = data['name']

        db.session.add(director)
        db.session.commit()
        db.session.close()

        return '', 204

    def delete(self, mid):
        director = Director.query.get(mid)

        db.session.delete(director)
        db.session.commit()
        db.session.close()


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        data = request.get_json()
        genre = Genre(**data)
        db.session.add(genre)
        db.session.commit()
        db.session.close()

        return "", 201

@genre_ns.route('/<int:mid>')
class GenreView(Resource):
    def get(self, mid):
        genre = Genre.query.get(mid)
        return genre_schema.dump(genre), 200

    def put(self, mid):
        data = request.get_json()
        genre = Genre.query.get(mid)
        genre.id = data['id']
        genre.name = data['name']

        db.session.add(genre)
        db.session.commit()
        db.session.close()

        return '', 204

    def delete(self, mid):
        genre = Genre.query.get(mid)

        db.session.delete(genre)
        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    app.run()
