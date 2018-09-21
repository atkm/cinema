import os
import datetime

from flask import (
        Flask, url_for, redirect
        )
from cinema.models import db, migrate
import cinema.showtime_scraper 


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
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def root():
        return redirect(url_for('shows.upcoming_shows'))

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        print(os.path.dirname(__file__))
        return 'Hello, World!'

    @app.route('/scrape')
    def scrape():
        cinema_ls = cinema.showtime_scraper.cinema_ls
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        for cinema_name in cinema_ls:
            showtimes = cinema.showtime_scraper.scrape(cinema_name, 'Tomorrow')
            for s in cinema.showtime_scraper.create_showtimes(db.session, cinema_name, tomorrow, showtimes):
                db.session.add(s)
            db.session.commit() # commit for each theater
        return 'Done!'

    from . import shows
    app.register_blueprint(shows.bp)

    return app

