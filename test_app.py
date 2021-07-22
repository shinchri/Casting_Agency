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
        database = setup_db(self.app, self.database_path)
        database.create_all()

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
            self.db.session.execute('ALTER SEQUENCE "movie_id_seq" RESTART WITH 1')
            self.db.session.execute('ALTER SEQUENCE "actor_id_seq" RESTART WITH 1')
            self.db.create_all()

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

    def test_404_invalid_page_actors(self):
        res = self.client().get('/actors?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertFalse(data['success'])

    def test_405_making_post_request_on_get_actors(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')
        self.assertFalse(data['success'])

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], 4)
        self.assertTrue(data['movies'])

    def test_404_invalid_page_movies(self):
        res = self.client().get('/movies?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertFalse(data['success'])

    def test_405_making_delete_request_on_get_movies(self):
        res = self.client().delete('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')
        self.assertFalse(data['success'])

    def test_delete_actors(self):
        res = self.client().delete('/actors/2/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['success'])

    def test_404_delete_none_existing_actor(self):
        res = self.client().delete('/actors/10/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertFalse(data['success'])

    def test_delete_movies(self):
        res = self.client().delete('/movies/2/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['success'])

    def test_405_making_get_request_for_delete(self):
        res = self.client().get('/movies/3/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertFalse(data['success'])

    def test_create_actor(self):
        res = self.client().post('/actors/create', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor'], 6)
        self.assertTrue(data['success'])

    def test_422_invalid_json_for_actor(self):
        res = self.client().post('/actors/create', json={"title": "Romeo"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], "unprocessable")
        self.assertFalse(data['success'])

    def test_create_movie(self):
        res = self.client().post('/movies/create', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie'], 5)
        self.assertTrue(data['success'])

    def test_422_invalid_json_for_movie(self):
        res = self.client().post('/movies/create', json={"titles": "titles"}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertFalse(data['success'])

    def test_edit_actor(self):
        res = self.client().patch('/actors/1/edit', json={'name':"Santa", "age":11})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['actor']), 4)
        self.assertEqual(data['actor']['id'], 1)
        self.assertEqual(data['actor']['name'], "Santa")
        self.assertEqual(data['actor']['age'], 11)
        self.assertEqual(data['actor']['gender'], "male")
        self.assertTrue(data['actor'])
        self.assertTrue(data['success'])

    def test_404_edit_invalid_actor(self):
        res = self.client().patch('/actors/11/edit', json={'name':"Santa", "age":11})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    def test_edit_movie(self):
        res = self.client().patch('/movies/4/edit', json={'title':"Jurassic Park 2"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['movie']), 3)
        self.assertEqual(data['movie']['id'], 4)
        self.assertEqual(data['movie']['title'], "Jurassic Park 2")
        self.assertEqual(data['movie']['release_date'], "Fri, 07 May 2021 00:00:00 GMT")
        self.assertTrue(data['success'])

    def test_404_edit_invalid_movie(self):
        res = self.client().patch('/movies/40/edit', json={'title':"Jurassic Park 2"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertFalse(data['success'])

if __name__ == '__main__':
    unittest.main()