import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # TODO: move this to config.py, and import it through APP_SETTINGS env var.
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'],
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # db
    from .models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        print(os.path.dirname(__file__))
        return 'Hello, World!'

    return app
