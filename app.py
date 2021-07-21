import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=["GET"])
    def get_actors():
        return "Get Actors"
    
    @app.route('/movies', methods=["GET"])
    def get_movies():
        return "Get Movies"

    @app.route('/actors/<int:actor_id>/delete', methods=["DELETE"])
    def delete_actors(actor_id):
        return "Delete Actors"

    @app.route('/movies/<int:movie_id>/delete', methods=["DELETE"])
    def delete_movies(movie_id):
        return "Delete Movies"

    @app.route('/actors/create', methods=["POST"])
    def create_actors():
        return "Create Actors"

    @app.route('/movies/create', methods=["POST"])
    def create_movies():
        return "Create movies"

    @app.route('/actors/<int:actor_id>/edit', methods=["PATCH"])
    def edit_actors(actor_id):
        return "Edit Actors"

    @app.route('/movies/<int:movie_id>/edit', methods=["PATCH"])
    def edit_movies(movie_id):
        return "Edit Movies"


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

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)