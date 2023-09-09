export FLASK_APP=project
export FILL_DB=0
flask db init
flask db migrate
flask db upgrade
export FILL_DB=1
flask run