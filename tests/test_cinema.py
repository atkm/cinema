import pytest
from tests.fixtures import test_app, test_db, test_client, test_session, cinema_html_tomorrow_with_name, cinema_html_tomorrow

import pkg_resources
import datetime
import time
from bs4 import BeautifulSoup

import cinema
import cinema.showtime_scraper
from cinema.models import Theater, Film, Showtime


   
def test_empty_db(test_client):
    rv = test_client.get('/hello')
    assert b'Hello, World!' == rv.data

def assert_dict_nonempty(d):
    assert len(d) > 0
    for v in d.values():
        assert len(v) > 0

# TODO: test lengths of titles list and showtimes list match

def test_showtime_parser(cinema_html_tomorrow):
    showtimes_dict = cinema.showtime_scraper.parse_showtimes(cinema_html_tomorrow)
    assert_dict_nonempty(showtimes_dict)

# TODO: write a test where the database is not empty
def test_showtime_parser_amc(test_session):
    amc_theater = 'AMC Metreon 16'
    date = datetime.date(2018,9,23)
    fname = f'amc_metreon_16_{date.strftime("%Y%m%d")}.html'
    html = pkg_resources.resource_stream('cinema', f'resources/{fname}')
    showtimes = cinema.showtime_scraper.parse_showtimes(html)
    shows = ['The House With A Clock In Its Walls',
            'The Predator',
            'The Nun',
            'A Simple Favor',
            'Life Itself',
            'Crazy Rich Asians',
            'Fahrenheit 11/9',
            'Assassination Nation',
            'Searching',
            'Mission: Impossible – Fallout',
            ]
    # ensure parse_showtimes is working
    for s in shows:
        assert s in showtimes

    shows_created = set()
    for s in cinema.showtime_scraper.create_showtimes(test_session, amc_theater, date, showtimes):
        shows_created.add(s.film.name)
        test_session.add(s)
    # ensure create_showtimes is working
    assert shows_created == set(shows)
    test_session.commit()

    # ensure commiting showtimes to the db is working
    amc_shows = test_session.query(Showtime, Film, Theater)\
            .join(Film).join(Theater)\
            .filter(Theater.name == amc_theater)\
            .filter(Showtime.showdate == date)\
            .all()
    set([s.Film.name for s in amc_shows]) == set(shows)

# Note: the lifetime of the db fixture spans a pytest session.
def test_insert_showtimes(test_session, cinema_html_tomorrow_with_name):
    cinema_name, html = cinema_html_tomorrow_with_name
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    showtimes = cinema.showtime_scraper.parse_showtimes(html)
    for s in cinema.showtime_scraper.create_showtimes(test_session, cinema_name, tomorrow, showtimes):
        test_session.add(s)
    test_session.commit()
    assert test_session.query(Film.id).count() > 0
    assert test_session.query(Theater.id).count() > 0
    assert test_session.query(Theater.name).scalar() == cinema_name
    assert test_session.query(Showtime.id).count() > 0


def test_scrape_endpoint(test_session, test_client):
    response = test_client.get('/scrape')
    assert response.status_code == 200
    data = response.data.decode()
    assert data == 'Done!'
    # Theaters exist in db, and
    # Each theater has a showtime associated with it
    for cinema_name in cinema.showtime_scraper.cinema_ls:
        theater = test_session.query(Theater).filter_by(name = cinema_name).first()
        assert theater
        assert theater.showtimes


# TODO: send a request to /scrape twice. Ensure there are no duplicate entries.
def test_no_duplicate_inserts(test_session, test_client):
    response1 = test_client.get('/scrape')
    assert response1.status_code == 200

    showtimes_dict = dict()
    for cinema_name in cinema.showtime_scraper.cinema_ls:
        theater = test_session.query(Theater).filter_by(name = cinema_name).first()
        assert theater
        assert theater.showtimes
        showtimes_dict[cinema_name] = theater.showtimes


    response2 = test_client.get('/scrape')
    assert response2.status_code == 200

    for cinema_name in cinema.showtime_scraper.cinema_ls:
        theater = test_session.query(Theater).filter_by(name = cinema_name).first()
        assert cinema_name in showtimes_dict
        assert theater.showtimes == showtimes_dict[cinema_name]

