# Casting_Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your progress.

### Installing Dependencies
1. **Python 3.9** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

2. **Virtual Environment** -  Creating a virtual environment for the python project is recommended. Refer to the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

3. **PIP Dependencies** - After you set up the virtual environment setup and have it running, install dependencies by running the below command within the ```/Casting_Agency``` folder.

```bash
$ ./setup.sh
```

The above will set the environment variables and install all dependencies in the requirements.txt.

If ```Permission denied``` shows up, set execute permission on ```setup.sh```, and run the above command again. You can set execute permission by running the below command:

```bash
$ chmod +x setup.sh
```

4. **Key Dependencies**

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in ```app.py``` and can reference ```models.py```.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Psycopg2-binary](https://pypi.org/project/psycopg2-binary/) is a PostgreSQL database adapter for the Python

### Database Setup

For this project, Postgres is used as our database. Make sure you download the Postgres [here](https://www.postgresql.org/download/).

##### Create a database
```bash
$ createdb capstone -U postgres
```

```capstone``` is the name of our database and ```postgres``` is our user.

##### Destroy a database

Use the below command to destroy the database if needed:
```$ createdb capstone -U postgres```

### Running the server

From within the ```./Casting_Agency``` directory, first ensure you are working using your created virtual environment.

To run the server, execute:
```bash
$ flask run --reload
```

The ```--reload``` flag will detect file changes and restart the server automatically.

The application will be running on port 5000.

### API Reference

#### Getting Started
- ***Base URL***: ```http://127.0.0.1:5000``` (when ran locally)
- ***Authentication***: [Auth0](https://auth0.com/docs/quickstart/backend/python/01-authorization) is used to create JWT, and RBAC is used for each role
- ***Resources available***: ```Actor``` and ```Movie```

|  Actor       |  ---------           |
|  -------     |   -------            |
|  **Field**   |  **Type**            |
|     id       |  Integer, primary Key|
|    name      |   String             |
|     age      |   Integer            |
|    gender    |    String            |

|  Movie       |  ---------           |
|  -------     |   -------            |
|  **Field**   |  **Type**            |
|     id       |  Integer, primary Key|
|    name      |    String            |
| release_date |    String, nullable  |

- ***Roles and Permissions***:

    - ***Casting Assistant*** (casting_assistant)
        - Can view actors and movies (**get:actors**, **get:movies**)

    - ***Casting Director*** (casting_director)
        - All permissions a Casting Assitant has and...
        - Add or delete an actor from the database (**post:actors**, **delete:actors**)
        - Modify actors or movies (**patch:actors**, **patch:movies**)

    - ***Executive Producer*** (executive_producer)
        - All permissions a Casting Director has and...
        - Add or delete a movie from the database (**post:movies**, **delete:movies**)

#### Error Handling

Errors are returned as JSON object. For example:

```json
{
    "success": false,
    "error": 400,
    "message": "bad request"
}
```

The API returns the following error types:
- 400: Bad Request
- 401: Unauthorized Error
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable

#### Endpoints

GET /actors
- Used to retreive all actors
- ```curl -X GET http://127.0.0.1:5000/actors -H "Content-Type: application/json"```
- For pagination, ```page``` parameter is used. Defaults to 1.
- Requires ```get:actors``` permission.
- Example Result:
```json
{
    "actors": [
        {
            "age": 31,
            "gender": "male",
            "id": 1,
            "name": "Chris"
        }
    ],
    "success": true,
    "total_actors": 1
}

```

GET /movies
- Used to retreive all movies.
- ```curl -X GET http://127.0.0.1:5000/movies -H "Content-Type: application/json"```
- For pagination, ```page``` parameter is used. Defaults to 1.
- Requires ```get:movies``` permission.
- Example Result:
```json
{
    "movies": [
        {
            "id": 4,
            "release_date": "Thu, 04 Jun 2020 00:00:00 GMT",
            "title": "Avator"
        },
        {
            "id": 6,
            "release_date": "Thu, 22 Jul 2021 16:01:52 GMT",
            "title": "Black Widow"
        }
    ],
    "success": true,
    "total_movies": 2
}
```

DELETE /actors/{actor_id}/delete
- Used to delete a specific actor
- ```curl -X DELETE http://127.0.0.1:5000/actors/1/delete -H "Content-Type: application/json"```
- Requires ```delete:actors``` permission.
- Example Result:
```json
{
    "deleted": 1,
    "success": true
}
```

DELETE /movies/{movie_id}/delete
- Used to delete a specific movie
- ```curl -X DELETE http://127.0.0.1:5000/movies/5/delete -H "Content-Type: application/json"```
- Requires ```delete:movies``` permission.
- Example Result:
```json
{
    "deleted": 5,
    "success": true
}
```

POST /actors/create
- Used to create a new actor
- ```curl -X POST http://127.0.0.1:5000/actors/create -H "Content-Type: application/json" -d '{"name": "Jessie","age": 15,"gender": "male"}'```
- Requires ```post:actors``` permission.
- Example Result:
```json
{
    "success": true,
    "actor": 5
}
```

POST /movies/create
- Used to create a new movie
- ```curl -X POST http://127.0.0.1:5000/movies/create -H "Content-Type: application/json" -d '{"title": "Terminator", "release_date": "06-10-2005"}'```
- Requires ```post:movies``` permission.
- Example Result:
```json
{
    "success": true,
    "movie": 3
}
```

PATCH /actors/{actor_id}/edit
- Used to edit a specific actor
- ```curl -X PATCH http://127.0.0.1:5000/actors/3/edit -H "Content-Type: application/json" -d '{"name": "Chris", "age": 15, "gender": "male"}'```
- Requires ```patch:actors``` permission.
- Example Result:
```json
{
    "actor": {
        "age": 15,
        "gender": "male",
        "id": 3,
        "name": "Chris"
    },
    "success": true
}
```

PATCH /movies/{movie_id}/edit
- Used to edit a specific movie
- ```curl -X PATCH http://127.0.0.1:5000/movies/4/edit -H "Content-Type: application/json" -d '{"title": "Batman", "release_date": "06-04-2020"}'```
- Requires ```patch:movies``` permission.
- Example Result:
```json
{
    "movie": {
        "id": 4,
        "release_date": "Thu, 04 Jun 2020 00:00:00 GMT",
        "title": "Avator"
    },
    "success": true
}
```

#### Testing

##### Unit Test

To run the tests, run:
```bash
$ dropdb capstone
$ createdb capstone -U postgres
$ psql capstone < casting_agency.pgsql
$ python test_app.py
```

Before running the above command, make sure you have ran the setup.sh script to set the environment variables.

You can also explicitly set the variable DATABASE_URL_TEST by running the below command:

```bash
$ export DATABASE_URL_TEST='postgres://postgres@localhost:5432/capstone_test'
```

and test it by running:
```bash
$ echo $DATABASE_URL_TEST
```

#### Testing Endpoints with [Postman](https://www.postman.com/)

Import the postman collection ```./capstone.postman_collection.json``` and run the test.