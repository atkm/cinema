from flask import Blueprint
import datetime
import time
from cinema.worker import redis_conn
from rq import Queue

redis_q = Queue(connection=redis_conn)

bp = Blueprint('scrape', __name__, url_prefix='/scrape')

def _scrape():
    # TODO: create a connection instead of sharing with the app
    # See the official tutorial.
    from cinema.models import db
    import cinema.showtime_scraper
    cinema_ls = cinema.showtime_scraper.cinema_ls
    # INFO: the heroku server uses UTC
    for cinema_name in cinema_ls:
        try:
            for k in range(7):
                date = datetime.date.today() + datetime.timedelta(days=k)
                showtimes = cinema.showtime_scraper.scrape(cinema_name, k)
                for s in cinema.showtime_scraper.create_showtimes(db.session, cinema_name, date, showtimes):
                    db.session.add(s)
                db.session.commit() # commit for each theater
        except:
            print(f'Scraping {cinema_name} for {date} failed.')
            continue
    # TODO: notify when done
    return "Done!"

@bp.route('/')
def scrape():
    job = redis_q.enqueue(_scrape)
    return job.get_id()

@bp.route('/<job_id>')
def job_result(job_id):
    job = redis_q.fetch_job(job_id)
    while not job.is_finished:
        time.sleep(2)
    return job.result

