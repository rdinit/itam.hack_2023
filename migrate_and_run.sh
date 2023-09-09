export FLASK_APP=project
export SECRET_KEY=test-string
export SQLALCHEMY_DATABASE_URI='postgresql://postgres:password@postgres_server:5432/test1'
export FILL_DB=0
flask db init
flask db migrate
flask db upgrade
export FILL_DB=1
flask run