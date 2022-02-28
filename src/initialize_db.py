from environs import Env
import psycopg2
env = Env()
env.read_env()


pgConn = psycopg2.connect(dbname=env.str('DB_NAME'), user=env.str('DB_USERNAME'),
                          password=env.str('DB_PASSWORD'), host=env.str('DB_HOST'), port=env.str('DB_PORT'))

Movies = (
    (1, 'Avatar', 'Sci-Fi', '2009', '7.8', 'Sam Worthington'),
    (2, 'Avengers: Endgame', 'Sci-Fi', '2019', '8.4', 'Robert Downey Jr.'),
    (3, 'Titanic', 'Drama', '1997', '7.8', 'Leonardo DiCaprio'),
    (4, 'Star Wars: Episode VII - The Force Awakens',
     'Sci-Fi', '2015', '7.8', 'Daisy Ridley'),
    (5, 'Spider-Man: No Way Home', 'Sci-Fi', '2021', '8.7', 'Tom Holland'),
    (6, 'Avengers: Infinity War', 'Sci-Fi', '2018', '8.4', 'Robert Downey Jr.')
)


def insert_data_into_db(conn, query, *params):
    """Inserts data into database if database is empty

    Args:
        conn (postegres cursor)
        query (str): current query to be executed

    Returns:
        row(list): The data from the query
    """
    args = [arg for arg in params]
    conn = pgConn.cursor()
    conn.execute("SELECT * from movies")
    row = conn.fetchall()
    if not len(row):
        conn.executemany(
            "INSERT INTO movies(id,name,category,release_year,movie_rating,star) VALUES (%s, %s, %s, %s, %s, %s)", Movies)
        pgConn.commit()
        conn.execute(query, args) if args else conn.execute(query)
    else:
        conn.execute(query, args) if args else conn.execute(query)
    return conn
