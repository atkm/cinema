import pytest
import datetime
import time

import cinema
import cinema.showtime_scraper
from cinema.models import Theater, Film, Showtime
from cinema.models import db as _db

TEST_DATABASE_URI = "postgresql://postgres@localhost/cinema_testing"

# Flask fixtures ref: http://alexmic.net/flask-sqlalchemy-pytest/

# Should scope=module?
@pytest.fixture(scope='session')
def test_app(request):
    test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
            }
    flask_app = cinema.create_app(test_config)

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
    yield flask_app
    ctx.pop()

@pytest.fixture(scope='session')
def test_client(test_app):
    yield test_app.test_client()

@pytest.fixture(scope='session')
def test_db(test_app):
    _db.app = test_app
    _db.create_all()
 
    yield _db
 
    _db.drop_all()

# Creates a scoped session for each test
@pytest.fixture
def session(test_db):
    connection = test_db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = test_db.create_scoped_session(options=options)
    test_db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='module',
        params = cinema.showtime_scraper.cinema_ls)
def cinema_html_tomorrow_with_name(request):
    cinema_name = request.param
    html = cinema.showtime_scraper.get_html(cinema_name, 'Tomorrow')
    # can you set an attribute to a string?
    yield (cinema_name, html)

@pytest.fixture(scope='module')
def cinema_html_tomorrow(cinema_html_tomorrow_with_name):
    _, html = cinema_html_tomorrow_with_name
    yield html
    
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

# Note: the lifetime of the db fixture spans a pytest session.
def test_insert_showtimes(session, cinema_html_tomorrow_with_name):
    cinema_name, html = cinema_html_tomorrow_with_name
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    showtimes = cinema.showtime_scraper.parse_showtimes(html)
    for s in cinema.showtime_scraper.create_showtimes(session, cinema_name, tomorrow, showtimes):
        session.add(s)
    session.commit()
    assert session.query(Film.id).count() > 0
    assert session.query(Theater.id).count() > 0
    assert session.query(Theater.name).scalar() == cinema_name
    assert session.query(Showtime.id).count() > 0


def test_scrape_endpoint(session, test_client):
    response = test_client.get('/scrape')
    time.sleep(2) # TODO: should poll instead of waiting
    # Theaters exist in db, and
    # Each theater has a showtime associated with it
    for cinema_name in cinema.showtime_scraper.cinema_ls:
        theater = session.query(Theater).filter_by(name = cinema_name).first()
        assert theater
        assert theater.showtimes

# TODO: send a request to /scrape twice. Ensure there are no duplicate entries.
def test_no_duplicate_inserts():
    pass
