from environs import Env
import unittest
import requests

env = Env()
env.read_env()


class Tests(unittest.TestCase):
    api_url = "http://127.0.0.1:5000/api"
    movie_object = {"categories": "Dr,Romance", "star": "Leo"}
    test_user = {"email": "kostantinosmavros28@gmail.com", "first_name": "kostas",
                 "password1": "kostaskostas", "password2": "kostaskostas"}

    def test_sign_up(self):
        sign_up = requests.post(
            Tests.api_url + "/sign_up", json=Tests.test_user)
        self.assertEqual(sign_up.status_code, 200)
        self.assertEqual(sign_up.json(), {
                         'message': 'Registration successfully completed!'})

    def test_available_movies(self):
        result = requests.get(Tests.api_url + "/movies")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.json()), 6)  # Six records

    def test_available_movies_with_criteria(self):
        result = requests.get(Tests.api_url + "/movies",
                              json=Tests.movie_object)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), [{"categories": "Drama,Romance", "id": 3, "movie_rating": 7.8,
                         "name": "Titanic", "release_year": "1997", "star": "Leonardo DiCaprio"}])

    def test_get_movie_details(self):
        result = requests.get(Tests.api_url + f"/movies/Avengers")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), [{"categories": "Action,Adventure,Sci-Fi", "id": 2, "movie_rating": 8.4, "name": "Avengers: Endgame", "release_year": "2019", "star": "Robert Downey Jr."}, {
                         "categories": "Action,Adventure,Sci-Fi", "id": 6, "movie_rating": 8.4, "name": "Avengers: Infinity War", "release_year": "2018", "star": "Robert Downey Jr."}])

    def test_rent_a_movie(self):
        login = requests.post(
            f"http://{env.str('USERNAME')}:{env.str('PASSWORD')}@127.0.0.1:5000/api/login")
        self.assertEqual(login.status_code, 200)
        header = {'x-access-token': login.json()['token']}

        rent = requests.post(
            Tests.api_url + f"/movies/{5}/rent", headers=header)
        self.assertEqual(login.status_code, 200)
        self.assertEqual(rent.json(), {
                         "message": "You have successfully rented the movie Avengers: Endgame.  The final amount will be calculated when you will return it."})

    def test_return_a_movie(self):
        login = requests.post(
            f"http://{env.str('USERNAME')}:{env.str('PASSWORD')}@127.0.0.1:5000/api/login")
        self.assertEqual(login.status_code, 200)
        header = {'x-access-token': login.json()['token']}

        rent = requests.patch(
            Tests.api_url + f"/movies/{5}/return", headers=header)
        self.assertEqual(login.status_code, 200)
        # rent and return same day
        self.assertEqual(rent.json(), {
                         "message": f"You have successfully returned the movie. The total amount of this rent is {0}"})

    def test_amount(self):
        result = requests.get(
            Tests.api_url + f"/movies/amount/{10}")  # ten days
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {"Amount": 6.5})


if __name__ == '__main__':
    unittest.main()
