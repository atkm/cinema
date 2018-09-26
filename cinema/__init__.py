import os
import datetime
import time

from flask import (
        Flask, url_for, redirect, g
        )
import cinema.showtime_scraper 

import rq
from rq import Queue
from rq.job import Job


def _scrape():
    # TODO: create a connection instead of sharing with the app
    # See the official tutorial.
    from cinema.models import db
    cinema_ls = cinema.showtime_scraper.cinema_ls
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    for cinema_name in cinema_ls:
        showtimes = cinema.showtime_scraper.scrape(cinema_name, 1)
        for s in cinema.showtime_scraper.create_showtimes(db.session, cinema_name, tomorrow, showtimes):
            db.session.add(s)
        db.session.commit() # commit for each theater
    # TODO: notify when done
    return "Done!"

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

    # redis
    from cinema.worker import redis_conn
    redis_q = Queue(connection=redis_conn)

    @app.route('/')
    def root():
        #return redirect(url_for('shows.upcoming_shows'))
        return 'Hello!'

    @app.route('/scrape')
    def scrape():
        job = redis_q.enqueue(_scrape)
        return job.get_id()

    @app.route('/scrape/<job_id>')
    def job_result(job_id):
        job = Job.fetch(job_id, redis_conn)
        while not job.is_finished:
            time.sleep(2)
        return job.result

    from . import shows
    app.register_blueprint(shows.bp)

    return app

