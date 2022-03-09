from environs import Env
from app import db
from models import Movie
env = Env()
env.read_env()


Movies = (
    (1, 'Avatar', 'Sci-Fi,Action,Adventure,Fantasy',
     '2009', '7.8', 'Sam Worthington'),
    (2, 'Avengers: Endgame', 'Action,Adventure,Sci-Fi',
     '2019', '8.4', 'Robert Downey Jr.'),
    (3, 'Titanic', 'Drama,Romance', '1997', '7.8', 'Leonardo DiCaprio'),
    (4, 'Star Wars: Episode VII - The Force Awakens',
     "Animation,Action,Adventure,Drama,Fantasy,Sci-Fi", '2015', '7.8', 'Daisy Ridley'),
    (5, 'Spider-Man: No Way Home', 'Sci-Fi,Action,Adventure,Fantasy',
     '2021', '8.7', 'Tom Holland'),
    (6, 'Avengers: Infinity War', 'Action,Adventure,Sci-Fi',
     '2018', '8.4', 'Robert Downey Jr.')
)


def insert_data_into_db():
    """Inserts data into database if database is empty

    Args:
        conn (postegres cursor)
        query (str): current query to be executed

    Returns:
        row(list): The data from the query
    """
    for data in Movies:
        movie = Movie(id=data[0], name=data[1], categories=data[2],
                      release_year=data[3], movie_rating=data[4], star=data[5])
        db.session.add(movie)
        db.session.commit()
