import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
import datetime

from auth import AuthError, requires_auth

RES_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origins=["*"])

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def get_actors():
        selected_page = request.args.get('page', 1, type=int)
        current_index = selected_page - 1
        actors = Actor.query.order_by(Actor.id).limit(RES_PER_PAGE).offset(current_index*RES_PER_PAGE).all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
            "actors": [actor.format() for actor in actors],
            "total_actors": len(Actor.query.all()),
            "success": True
        })
    
    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def get_movies():
        selected_page = request.args.get('page', 1, type=int)
        current_index = selected_page - 1
        movies = Movie.query.order_by(Movie.id).limit(RES_PER_PAGE).offset(current_index*RES_PER_PAGE).all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
            "movies": [movie.format() for movie in movies],
            "total_movies": len(Movie.query.all()),
            "success": True
        })

    @app.route('/actors/<int:actor_id>/delete', methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actors(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor == None:
                abort(404)

            actor.delete()

            return jsonify({
                "deleted": actor_id,
                "success": True
            })
        except Exception as e:
            if e.code == 404:
                abort(404)
            abort(422)

    @app.route('/movies/<int:movie_id>/delete', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movies(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie == None:
                abort(404)

            movie.delete()

            return jsonify({
                "deleted": movie_id,
                "success": True
            })
        except Exception as e:
            if e.code == 404:
                abort(404)
            abort(422)

    @app.route('/actors/create', methods=["POST"])
    @requires_auth('post:actors')
    def create_actors():
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        #new_movie_list = body.get('movie_list', [])

        try:
            actor = Actor(new_name, new_age, new_gender)
            actor.insert()

            return jsonify({
                "success": True,
                "actor": actor.id
            })
        except Exception:
            abort(422)

    @app.route('/movies/create', methods=["POST"])
    @requires_auth('post:movies')
    def create_movies():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            if new_release_date == None:
                movie = Movie(new_title, datetime.datetime.utcnow())
            else:
                movie = Movie(new_title, new_release_date)

            movie.insert()

            return jsonify({
                "success": True,
                "movie": movie.id
            })

        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>/edit', methods=["PATCH"])
    @requires_auth('patch:actors')
    def edit_actors(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            
            if not actor:
                abort(404)
            
            body = request.get_json()

            actor.name = body.get('name', actor.name)
            actor.age = body.get('age', actor.age)
            actor.gender = body.get('gender', actor.gender)

            actor.update()

            return jsonify({
                "actor": actor.format(),
                "success": True
            })

        except Exception as e:
            if e.code == 404:
                abort(404)
            abort(422)

    @app.route('/movies/<int:movie_id>/edit', methods=["PATCH"])
    @requires_auth('patch:movies')
    def edit_movies(movie_id):
        
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie == None:
                abort(404)

            body = request.get_json()

            movie.title = body.get('title', movie.title)
            movie.release_date = body.get('release_date', movie.release_date)

            movie.update()

            return jsonify({
                "movie": movie.format(),
                "success": True
            })
            
        except Exception as e:
            if e.code == 404:
                abort(404)
            abort(422)


    #errors (400, 404, 405, 422)
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            "success": False,
            "error": error.error['code'],
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)