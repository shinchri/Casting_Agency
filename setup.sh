export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL='postgres://postgres@localhost:5432/capstone'
export DATABASE_URL_TEST='postgres://postgres@localhost:5432/capstone_test'
export API_AUDIENCE='casting_agency'
export AUTH0_DOMAIN='dev-oops.us.auth0.com'

pip3 install -r requirements.txt
