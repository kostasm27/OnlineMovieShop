from app import db


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), primary_key=True,
                     nullable=False,  unique=True)
    categories = db.Column(db.String(50))
    release_year = db.Column(db.String(4))
    movie_rating = db.Column(db.Float)
    star = db.Column(db.String(150))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200),  unique=True)
    password = db.Column(db.String(600))


class Watch(db.Model):
    __tablename__ = 'watch'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50))
    rent_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
