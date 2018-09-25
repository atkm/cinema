import os
import datetime

from flask import (
        Flask, url_for, redirect
        )
from cinema.models import db, migrate
import cinema.showtime_scraper 

from rq import Queue
from cinema.worker import redis_conn

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # TODO: move this to config.py, and import it through APP_SETTINGS env var.

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(os.environ['APP_SETTINGS'])
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

    # redis
    q = Queue(connection=redis_conn)

    @app.route('/')
    def root():
        #return redirect(url_for('shows.upcoming_shows'))
        return 'Hello!'

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        print(os.path.dirname(__file__))
        return 'Hello, World!'

    @app.route('/scrape')
    def scrape():
        job = q.enqueue_call(func = _scrape)
        return job.get_id()

    def _scrape():
        cinema_ls = cinema.showtime_scraper.cinema_ls
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        for cinema_name in cinema_ls:
            showtimes = cinema.showtime_scraper.scrape(cinema_name, 1)
            for s in cinema.showtime_scraper.create_showtimes(db.session, cinema_name, tomorrow, showtimes):
                db.session.add(s)
            db.session.commit() # commit for each theater
        # TODO: notify when done
        return None

    from . import shows
    app.register_blueprint(shows.bp)

    return app

