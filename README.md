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

**NOTE**: You may have to change the "CASTING_ASSISTANT", "CASTING_DIRECTOR", AND "EXECUTIVE_PRODUCER" with the ACCESS_TOKEN you will get in the "API Reference" section below. This token is needed to run ```test_app.py```  

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

##### Populate the database
```$ psql -U postgres capstone < casting_agency.pgsql```

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
- ***Base URL***: ```https://heroku-capstone-app-131.herokuapp.com/``` (deployed on heroku)
    - This will be different if you deploy it yourself (Please look at how to deploy your application onto Heroku in the "Deploy on Heroku" section below.)
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

#### Getting ACCESS_TOKEN for Testing Endpoints

- We will use [Auth0](https://auth0.com/) to create JWT

1. Create Tenant
2. Create Application
    - Note the "Domain"
    - Note the "Client ID"
    - Create "Allowed Callback URLs"
        - ex) http://127.0.0.1:8080/callback
    - Create "Allowed Web Origins"
        - ex) http://127.0.0.1:5000
    - Save
3. Create APIs
    - Note the "API Audience" (API Identifier)
    - Enable RBAC
    - Add Permissions in the Access Token
    - Go to "Permissions" tab, and create following permissions:
        - ```get:actors```
        - ```get:movies```
        - ```delete:actors```
        - ```delete:movies```
        - ```post:actors```
        - ```post:movies```
        - ```patch:actors```
        - ```patch:movies```
    - Save
4. Create Roles ("User Management")
    - Create following Roles:
        - ```Casting Assistant```
        - ```Casting Director```
        - ```Executive Producer```
    - Click each Role and assign the permissions allowed for each role (take a look at Getting Started section)
5. Create User for each Role
    - Make sure to remember the username and password
    - Assign Role to the users created (3 users in total)

6. Paste the following into the browser:
```url
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

- Make sure you replace YOUR_DOMAIN, API_IDENTIFIER, YOUR_CLIENT_ID, and YOUR_CALLBACK_URL with values you got from above steps.

- When you paste the above into the address, you will be asked to login. Use the users you created and password to log in. You will be sent to your callback uri. Token can be found in the url.

- Make note of the ACCESS_TOKEN, you will need them for testing/using the endpoints.
    - Do not copy the expires_in and token_type. Only copy the token.

- You can test the endpoints permissions with [JWT Debugger](https://jwt.io/)

#### Endpoints

GET /actors
- Used to retreive all actors
- ```curl -X GET http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}"```
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
- ```curl -X GET http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}"```
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
- ```curl -X DELETE http://127.0.0.1:5000/actors/1/delete -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}"```
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
- ```curl -X DELETE http://127.0.0.1:5000/movies/5/delete -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}"```
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
- ```curl -X POST http://127.0.0.1:5000/actors/create -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}" -d '{"name": "Jessie","age": 15,"gender": "male"}'```
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
- ```curl -X POST http://127.0.0.1:5000/movies/create -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}" -d '{"title": "Terminator", "release_date": "06-10-2005"}'```
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
- ```curl -X PATCH http://127.0.0.1:5000/actors/3/edit -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}" -d '{"name": "Chris", "age": 15, "gender": "male"}'```
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
- ```curl -X PATCH http://127.0.0.1:5000/movies/4/edit -H "Content-Type: application/json" -H "authorization: Bearer {ACCESS_TOKEN}" -d '{"title": "Batman", "release_date": "06-04-2020"}'```
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
$ dropdb capstone_test
$ createdb capstone_test -U postgres
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

You also need to set the variables for ACCESS_TOKEN for each roles.

#### Testing Endpoints with [Postman](https://www.postman.com/)

Import the postman collection ```./capstone.postman_collection.json``` and run the test.

- You may ned to reset and repopulate the database ```capstone```

- The variable ```host``` is set as ```localhost:5000```. If you want to test endpoint for the application deployed on heroku, you will have to change the variable value.

- In the collection ```capstone```, there are three folders (one for each role). You may need to change the token (ACCESS_TOKEN) as the one provided may be expired.

#### Deploy on Heroku

- Create the Heroku app:
```heroku create {NAME_OF_YOUR_APP}```

Note the git url. It may be needed later.

- Add git remote for Heroku to local repository
```git remote add heroku {HEROKU_GIT_URL}```

This may return ```fatal: remote heroku already exists.```. It just mean that the remote heroku has been set already, so you can just ignore it and continue.

- Add postgresql add-on for the database on heroku
```bash
heroku addons:create heroku-postgresql:hobby-dev --app {NAME_OF_YOUR_APPLICATION}
```

- You can run the following command to check your configuration variables:
```bash
heroku config --app {NAME_OF_YOUR_APPLICATION}
```

- Go fix the configuration in Heroku
    - in the browser, go to Heroku Dashboard and go to the settings. Reveal your config variables and add following required environment variables :
        - ```AUTH0_DOMAIN```
        - ```API_AUDIENCE```
    - The above variables can be found in the "**Getting ACCESS_TOKEN for Testing Endpoints**" section above.

- Push it to Heroku
```git push heroku main``` or if this doesn't work try:
```git push heroku master```

- Run migrations:
```heroku run python manage.py db upgrade --app {NAME_OF_YOUR_APPLICATION}```

- The application is now up!
