import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

actors = [
    {"name": "Chris", "age": 30, "gender": "male"},
    {"name": "Lindsey", "age": 25, "gender": "female"},
    {"name": "Leslie", "age": 27, "gender": "male"},
    {"name": "Winston", "age": 30, "gender": "male"},
    {"name": "Jessica", "age": 26, "gender": "female"}
]

movies = [
    {"title": "Black Widow", "release_date": "07-10-2021"},
    {"title": "The Boss Baby", "release_date": "03-31-2017"},
    {"title": "Jurassic Park", "release_date": "06-11-1993"},
    {"title": "Wrath of Man", "release_date": "05-07-2021"},
]

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL_TEST'].replace('postgres://', 'postgresql://')
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': "Karen",
            'age': 22,
            'gender': "female"
        }

        self.new_movie = {
            'title': 'Tome & Jerry',
            'release_date': '02-26-2021'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            self.db.session.execute('ALTER SEQUENCE "movie_id_seq" RESTART WITH 1')
            self.db.session.execute('ALTER SEQUENCE "actor_id_seq" RESTART WITH 1')

            for movie in movies:
                obj = Movie(title=movie['title'], release_date=movie['release_date'])
                self.db.session.add(obj)
                self.db.session.commit()

            for actor in actors:
                obj = Actor(name=actor['name'], age=actor['age'], gender=actor['gender'])
                self.db.session.add(obj)
                self.db.session.commit()

            self.db.session.close()

    def tearDown(self) -> None:
        with self.app.app_context():
            self.db.session.query(Actor).delete()
            self.db.session.query(Movie).delete()
            self.db.session.commit()
            self.db.session.close()
            self.db.drop_all()

    

    """
    Write Tests
    """

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_actors'], 5)
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], 4)
        self.assertTrue(data['movies'])

if __name__ == '__main__':
    unittest.main()