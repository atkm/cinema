import os

from flask import (
        Flask, url_for, redirect, g
        )

def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(os.environ['APP_SETTINGS'])
    else:
        # load the test config if passed in
        app.config.from_mapping(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # db
    from cinema.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def root():
        #return redirect(url_for('shows.upcoming_shows'))
        return 'Hello!'

    
    from . import shows
    app.register_blueprint(shows.bp)
    from . import scrape
    app.register_blueprint(scrape.bp)

    return app

