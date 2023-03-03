from flask import Flask, g, request
from flask_cors import CORS
from flask_login import LoginManager
import models
import os
from resources.user import user
from resources.car import car
from resources.project import project

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


CORS(user, origins=['http://localhost:3000', 'https://revheads.herokuapp.com', 'https://master.d3eyhgfcrvig42.amplifyapp.com'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')
CORS(car, origins=['http://localhost:3000', 'https://revheads.herokuapp.com', 'https://master.d3eyhgfcrvig42.amplifyapp.com'], supports_credentials=True)
app.register_blueprint(car, url_prefix='/api/v1/cars')
CORS(project, origins=['http://localhost:3000', 'https://revheads.herokuapp.com', 'https://master.d3eyhgfcrvig42.amplifyapp.com'], supports_credentials=True)
app.register_blueprint(project, url_prefix='/api/v1/projects')


if 'ON_HEROKU' in os.environ:
    print('\non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
