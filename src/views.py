from sys import exc_info
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request,  jsonify, request, make_response
import jwt
import datetime
from authentication import token_auth
from initialize_db import insert_data_into_db, pgConn, env

view = Blueprint('view', __name__)


@ view.route('/api/sign_up', methods=['POST'])
def sign_up():
    """Sign up route

    Args:
        content (json): email, first_name, password1, password2

    Returns:
        json: message if user register successfully
    """
    try:
        if request.method == "POST":
            content = request.get_json()
            email = content['email']
            first_name = content['first_name']
            password1 = content['password1']
            password2 = content['password2']

            conn = pgConn.cursor()
            conn.execute(
                "SELECT email FROM users WHERE email = %s", (email,))
            row = conn.fetchall()
            if row:
                return jsonify({'message': 'Account already exists.'})
            elif len(email) < 4:
                return jsonify({'message': 'Email must be greater than 3 characters.'})
            elif len(first_name) < 2:
                return jsonify({'message': 'First name must be greater than 1 character.'})
            elif password1 != password2:
                return jsonify({'message': 'Passwords don\'t match.'})
            elif len(password1) < 7:
                return jsonify({'message': 'Password must be at least 7 characters.'})
            conn.execute("INSERT INTO users (first_name,email,password) VALUES(%s,%s,%s)",
                         (first_name, email, generate_password_hash(password1, method='sha256')))
            pgConn.commit()
            conn.close()
            return jsonify({'message': 'Registration successfully completed!'})
    except Exception as ex:
        pgConn.rollback()
        return jsonify({"message": str(ex)})


@ view.route('/api/login', methods=['POST'])
def login():
    """Login route 

    Returns:
        token or error message if failed
    """
    try:
        if request.method == "POST":
            auth = request.authorization

            if not auth or not auth.username or not auth.password:
                return make_response('Authentication Failed.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

            conn = pgConn.cursor()
            conn.execute("SELECT * FROM users WHERE first_name = %s",
                         (auth.username,))
            row = conn.fetchone()
            if row:
                if check_password_hash(row[3], auth.password):
                    token = jwt.encode({'id': row[0], 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=30)}, env.str('SECRET_KEY'))
                    print(token)

                    return jsonify({'token': token.decode('UTF-8')})
                return make_response('Authentication Failed.', 401, {'WWW-Authenticate': 'Basic realm="Incorrect password, try again.'})
            return make_response('Authentication Failed.', 401, {'WWW-Authenticate': 'User does not exist.'})
    except Exception as ex:
        pgConn.rollback()
        return jsonify({"message": str(ex)})


@ view.route('/api/movies', methods=['GET'])
def available_movies():
    """This function is accessible to non-members.

    Args for criteria:
        json: keys(category, movie_rating, star), values(Drama, Sci-Fi, Leonardo DiCaprio)

    Returns:
        json: returns all available movies with and without criteria 
    """
    try:
        conn = pgConn.cursor()
        query = "SELECT * from movies"
        conn = insert_data_into_db(conn, query)
        row = conn.fetchall()
        content = request.get_json()
        if content:
            critetia_query = "SELECT * FROM movies where "
            for i, (key, value) in enumerate(content.items()):
                if isinstance(value, str):
                    critetia_query += key + ' LIKE ' + "'%" + value + "%' "
                # if criteria value is integer
                else:
                    critetia_query += key + '>=' + str(value)
                if i+1 != len(content.items()):
                    critetia_query += 'and '
            conn.execute(critetia_query)
            row = conn.fetchall()
        if not row:
            return jsonify({"message": "No movies found"})
        # column names
        colnames = [col[0] for col in conn.description]
        results = []
        for data in row:
            results.append(dict(zip(colnames, data)))
        conn.close()
        return jsonify(results)
    except Exception as ex:
        pgConn.rollback()
        return jsonify({"message": str(ex)})


@ view.route('/api/movies/<movie_name>', methods=['GET'])
def get_details(movie_name):
    """ This function is accessible to non-members.
    Args:
        movie_name (str): The movie that the user desires to get more information

    Returns:
        json: Details about a specific movie based on movie_name
    """
    try:
        conn = pgConn.cursor()
        query = "SELECT * from movies where name"
        query += ' LIKE ' + "'%" + movie_name + "%' "
        conn.execute(query)
        row = conn.fetchall()
        if not row:
            return jsonify({"message": "This movie does not exist"})
        colnames = [col[0] for col in conn.description]
        results = []
        for data in row:
            results.append(dict(zip(colnames, data)))
        conn.close()
        return jsonify(results)
    except Exception as ex:
        pgConn.rollback()
        return jsonify({"message": str(ex)})


@ view.route('/api/movies/<movie_id>/rent', methods=['POST'])
@token_auth
def rent_movie(current_user, movie_id):
    """Rent route (This function is accessible to members only.)

    Args:
        current_user (dict): credentials current user 
        movie_id (str): The movie that the user desires to rent

    Returns:
        json: success message if the user has succesfully rented the movie or error message if something went wrong
    """
    try:
        if request.method == "POST":
            conn = pgConn.cursor()
            conn.execute("SELECT * from movies where id = %s", movie_id)
            row = conn.fetchone()
            movie_name = row[1]
            if not row:
                return jsonify({"message": "This movie id does not exist"})
            conn.execute(
                "SELECT movie_id, rent_date, return_date from watch where movie_id = %s and rent_date is not null and return_date is null and user_id = %s", (movie_id, current_user[0]))
            row = conn.fetchone()
            if row:
                return jsonify({"message":  "You have already rented this movie. Return it in order to be able to rent it again."})
            conn.execute("INSERT INTO watch(movie_id,user_id,username,rent_date,return_date) VALUES (%s, %s, %s, %s, %s)", (movie_id,
                                                                                                                            current_user[0], current_user[1], datetime.date.today(), None))
            pgConn.commit()
            conn.close()
            return jsonify({"message": f"You have successfully rented the movie {movie_name}.  The final amount will be calculated when you will return it."})
    except Exception as ex:
        pgConn.rollback()
        return jsonify({"message": str(ex)})


@ view.route('/api/movies/<movie_id>/return', methods=['PATCH'])
@token_auth
def return_movie(current_user, movie_id):
    """Return route "Rent route (This function is accessible to members only.)

    Args:
        current_user (dict): credentials current user 
        movie_id (str): The movie that the user wants to return

    Returns:
        json: success message if the user has succesfully returned the movie or error message if something went wrong
    """
    try:
        if request.method == "PATCH":
            conn = pgConn.cursor()
            conn.execute("SELECT * from movies where id = %s", movie_id)
            row = conn.fetchone()
            if not row:
                return jsonify({"message": "This movie id does not exist"})
            conn.execute(
                "SELECT movie_id, rent_date, return_date from watch where movie_id = %s and rent_date is not null and return_date is null and user_id = %s", (movie_id, current_user[0]))
            row = conn.fetchone()
            if row:
                time = datetime.date.today() - row[1]
                total_amount = get_amount(time.days).get_json()
                conn.execute(
                    "UPDATE watch set return_date = %s where user_id = %s and movie_id = %s", (datetime.date.today(), current_user[0], movie_id))
                pgConn.commit()
                return jsonify({"message": f"You have successfully returned the movie. The total amount of this rent is {total_amount['Amount']}"})
            conn.close()
            return jsonify({"message": "Rent this movie in order to return it."})
    except Exception as ex:
        pgConn.rollback()
        return jsonify({"message": str(ex)})


@ view.route('/api/movies/amount/<int:days>', methods=['GET'])
def get_amount(days):
    """ Amount route (This function is accessible to non-members.)

    Args:
        days (int): The number of days that the user will rent a movie

    Returns:
        json: The Amount that user has to pay based on the number of days
    """
    return jsonify({'Amount': (3 + (days-3)*0.5 if days > 3 else days)})
