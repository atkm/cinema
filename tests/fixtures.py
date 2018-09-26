import pytest
import pkg_resources
import redis
from rq import SimpleWorker, Queue, Connection

import cinema
from cinema.models import db as _db
from cinema.worker import redis_conn

TEST_DATABASE_URI = "postgresql://postgres@localhost/cinema_testing"

# Flask fixtures ref: http://alexmic.net/flask-sqlalchemy-pytest/

with pkg_resources.resource_stream('cinema', 'resources/cinemas-test.txt') as f:
    cinema_ls_short = [line.decode('utf-8').strip() for line in f.readlines()]

test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        }

# Should scope=module?
@pytest.fixture(scope='session')
def test_app():
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
def test_session(test_db):
    connection = test_db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = test_db.create_scoped_session(options=options)
    test_db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

# this works: SimpleWorker([redis_q], connection=redis_q.connection),
# where redis_q = Queue(connection = redis_conn) defined in worker.py
@pytest.fixture
def test_worker(test_db):
    with Connection(redis_conn):
        worker = SimpleWorker([Queue('default')])
        worker.work(burst=True) # Burst tells the worker to stop when there is no work on the queue

@pytest.fixture(scope='module',
        params = cinema.showtime_scraper.cinema_ls)
def cinema_html_tomorrow_with_name(request):
    cinema_name = request.param
    html = cinema.showtime_scraper.get_html(cinema_name, 1)
    # can you set an attribute to a string?
    yield (cinema_name, html)

@pytest.fixture(scope='module')
def cinema_html_tomorrow(cinema_html_tomorrow_with_name):
    _, html = cinema_html_tomorrow_with_name
    yield html
 
