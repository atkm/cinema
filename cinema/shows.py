from flask import (
        Blueprint, render_template
        )
import datetime
import itertools

from cinema.models import db, Showtime, Theater, Film

bp = Blueprint('shows', __name__, url_prefix='/shows')

def _get_shows(session, days_begin, days_end):
    today = datetime.date.today()
    upper_bound = today + datetime.timedelta(days=days_end)
    lower_bound = today + datetime.timedelta(days=days_begin)
    return session.query(Showtime, Theater, Film)\
            .join(Theater).join(Film)\
            .filter(Showtime.showdate >= lower_bound)\
            .filter(Showtime.showdate <= upper_bound)


# TODO: why is this endpoint redirecting in test_shows_tomorrow? 
@bp.route('/')
def upcoming_shows():
    theaters = db.session.query(Theater.name).all()
    shows_tomorrow = _get_shows(db.session, 1, 1)
    shows_dict = dict()
    for t in theaters:
        shows_at_t = shows_tomorrow.filter(Theater.name == t.name)
        shows_dict[t.name] = [s.Film.name for s in shows_at_t.all()]
    return render_template('upcoming_shows.html', upcoming_shows=shows_dict)

@bp.route('/indie')
def indie_shows():
    """
    Compute the pairwise disjoint differences.
    """
    # shows from the past six days and this week
    shows_this_week = _get_shows(db.session, -6, 6)
    theaters = db.session.query(Theater.name).all()
    shows_dict = dict()
    for t in theaters:
        shows_at_t = shows_this_week\
                .filter(Theater.name == t.name)\
                .distinct()
        shows_dict[t.name] = set([s.Film.name for s in shows_at_t.all()])

    shows_dict_new = shows_dict.copy()
    for t_new, (t, s) in itertools.product(shows_dict_new, shows_dict.items()):
        if t_new != t:
            shows_dict_new[t_new] = shows_dict_new[t_new].difference(s)
    return render_template('upcoming_shows.html', upcoming_shows=shows_dict_new)
