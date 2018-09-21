from flask import (
        Blueprint, render_template
        )
import datetime

from cinema.models import db, Showtime, Theater, Film

bp = Blueprint('shows', __name__, url_prefix='/shows')

def _get_future_shows(session, days):
    today = datetime.date.today()
    upper_bound = today + datetime.timedelta(days=days)
    return session.query(Showtime, Theater, Film)\
            .join(Theater).join(Film)\
            .filter(Showtime.showdate >= today)\
            .filter(Showtime.showdate <= upper_bound)

# TODO: write test for the resulting html 
@bp.route('/')
def upcoming_shows():
    theaters = db.session.query(Theater.name).all()
    shows_tomorrow = _get_future_shows(db.session, 1)
    shows_dict = dict()
    for t in theaters:
        shows_at_t = shows_tomorrow.filter(Theater.name == t.name)
        shows_dict[t.name] = [s.Film.name for s in shows_at_t.all()]
    print(shows_dict)
    return render_template('upcoming_shows.html', upcoming_shows=shows_dict)

@bp.route('/indie')
def indie_shows():
    """
    The symmetric difference of indie theaters.
    """
    # TODO: get unique shows for each theater
    shows_within_one_week = _get_future_shows(db.session, 7)
    theaters = db.session.query(Theater.name).all()
    shows_dict = dict()
    for t in theaters:
        shows_at_t = shows_within_one_week\
                .filter(Theater.name == t.name)\
                .distinct()
        shows_dict[t.name] = [s.Film.name for s in shows_at_t.all()]
