from re import L
from initialize_db import insert_data_into_db, env
from authentication import token_auth
from models import User, Watch, Movie
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request,  jsonify, request, make_response
import jwt
import datetime


@app.route('/api/sign_up', methods=['POST'])
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

            # user = User.query
            user = User.query.filter_by(email=email).first()

            if user:
                return jsonify({'message': 'Account already exists.'})
            elif len(email) < 4:
                return jsonify({'message': 'Email must be greater than 3 characters.'})
            elif len(first_name) < 2:
                return jsonify({'message': 'First name must be greater than 1 character.'})
            elif password1 != password2:
                return jsonify({'message': 'Passwords don\'t match.'})
            elif len(password1) < 7:
                return jsonify({'message': 'Password must be at least 7 characters.'})
            else:
                user = User.query.filter_by(first_name=first_name).first()
                if user:
                    return jsonify({'message': 'This name already taken'})

            new_user = User(
                first_name=first_name, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Registration successfully completed!'})
    except Exception as ex:
        return jsonify({"message": str(ex)})


@app.route('/api/login', methods=['POST'])
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

            user = User.query.filter_by(first_name=auth.username).first()

            if user:
                if check_password_hash(user.password, auth.password):
                    token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=30)}, env.str('SECRET_KEY'))

                    return jsonify({'token': token.decode('UTF-8')})
                return make_response('Authentication Failed.', 401, {'WWW-Authenticate': 'Basic realm="Incorrect password, try again.'})
            return make_response('Authentication Failed.', 401, {'WWW-Authenticate': 'User does not exist.'})
    except Exception as ex:
        return jsonify({"message": str(ex)})


@app.route('/api/movies', methods=['GET'])
def available_movies():
    """This function is accessible to non-members.

    Args for criteria:
        json: keys(categories, movie_rating, star), values(Drama, Sci-Fi, Leonardo DiCaprio)

    Returns:
        json: returns all available movies with and without criteria
    """
    try:
        colDict = {"name": Movie.name, "categories": Movie.categories,
                   "movie_rating": Movie.movie_rating, "release_year": Movie.release_year, "star":  Movie.star}

        movie = Movie.query.all()

        if not movie:
            insert_data_into_db()
            movie = Movie.query.all()
        content = request.get_json()
        if content:
            criteria = []
            for i, (key, value) in enumerate(content.items()):
                if isinstance(value, str):
                    if ',' in value:
                        temp_list = value.split(',')
                        for value in temp_list:
                            value = "%{}%".format(value)
                            criteria.append(colDict[key].like(value))
                    else:
                        value = "%{}%".format(value)
                    if key in colDict:
                        criteria.append(colDict[key].like(value))
                # if criteria value is integer
                else:
                    if key in colDict:
                        criteria.append(colDict[key] >= value)
            movie = Movie.query.filter(criteria[0]).all()
            for i in range(1, len(criteria)):
                query = Movie.query.filter(criteria[i]).all()
                movie = list(set.intersection(set(movie), set(query)))

        if not movie:
            return jsonify({"message": "No movies found"})
        results = []
        for data in movie:
            results.append(dict((column.name, getattr(data, column.name))
                                for column in data.__table__.columns))
        return jsonify(results)
    except Exception as ex:
        return jsonify({"message": str(ex)})


@ app.route('/api/movies/<movie_name>', methods=['GET'])
def get_details(movie_name):
    """ This function is accessible to non-members.
    Args:
        movie_name (str): The movie that the user desires to get more information

    Returns:
        json: Details about a specific movie based on movie_name
    """
    try:
        movie_name = "%{}%".format(movie_name)
        movie = Movie.query.filter(Movie.name.like(movie_name)).all()
        if not movie:
            return jsonify({"message": "This movie does not exist"})
        results = []
        for data in movie:
            results.append(dict((column.name, getattr(data, column.name))
                                for column in data.__table__.columns))
        return jsonify(results)
    except Exception as ex:
        return jsonify({"message": str(ex)})


@ app.route('/api/movies/user/rented-movies', methods=['GET'])
@ token_auth
def get_rented_movies(current_user):
    """ Rented Movies route (This function is accessible to members only.)
    Returns:
        json: Rented movies of the current_user 
    """
    try:
        user = Watch.query.filter_by(user_id=current_user.id).all()
        print(user)
        if not user:
            return jsonify({"message": "You have not rented any movies yet."})
        results = []
        for data in user:
            results.append(dict((column.name, getattr(data, column.name))
                                for column in data.__table__.columns))
        return jsonify(results)
    except Exception as ex:
        return jsonify({"message": str(ex)})


@ app.route('/api/movies/<movie_id>/rent', methods=['POST'])
@ token_auth
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
            movie = Movie.query.filter_by(id=movie_id).first()
            if not movie:
                return jsonify({"message": "This movie id does not exist"})
            watch = Watch.query.filter_by(
                movie_id=movie_id, user_id=current_user.id).first()
            # conn.execute(
            #     "SELECT movie_id, rent_date, return_date from watch where movie_id = %s and rent_date is not null and return_date is null and user_id = %s", (movie_id, current_user[0]))
            # row = conn.fetchone()
            if watch:
                return jsonify({"message":  "You have already rented this movie. Return it in order to be able to rent it again."})
            new_rent = Watch(
                movie_id=movie_id, user_id=current_user.id, username=current_user.first_name, rent_date=datetime.date.today(), return_date=None)
            db.session.add(new_rent)
            # ("INSERT INTO watch(movie_id,user_id,username,rent_date,return_date) VALUES (%s, %s, %s, %s, %s)", (movie_id,
            # pgConn.commit()
            db.session.commit()
            return jsonify({"message": f"You have successfully rented the movie {movie.name}.  The final amount will be calculated when you will return it."})
    except Exception as ex:
        return jsonify({"message": str(ex)})


@ app.route('/api/movies/<movie_id>/return', methods=['PATCH'])
@ token_auth
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
            movie = Movie.query.filter_by(id=movie_id).first()
            if not movie:
                return jsonify({"message": "This movie id does not exist"})
            watch = Watch.query.filter_by(
                id=movie_id, user_id=current_user.id, return_date=None).first()
            if watch:
                time = datetime.date.today() - watch.rent_date
                total_amount = get_amount(time.days).get_json()
                watch.return_date = datetime.date.today()
                db.session.commit()
                return jsonify({"message": f"You have successfully returned the movie. The total amount of this rent is {total_amount['Amount']}"})
            return jsonify({"message": "Rent this movie in order to return it."})
    except Exception as ex:
        return jsonify({"message": str(ex)})


@ app.route('/api/movies/amount/<int:days>', methods=['GET'])
def get_amount(days):
    """ Amount route (This function is accessible to non-members.)

    Args:
        days (int): The number of days that the user will rent a movie

    Returns:
        json: The Amount that user has to pay based on the number of days
    """
    return jsonify({'Amount': (3 + (days-3)*0.5 if days > 3 else days)})
