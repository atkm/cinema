import pytest
from tests.fixtures import test_app, test_worker, test_db, test_client, test_session, _wait_for_scrape, cinema_html_tomorrow_with_name, cinema_html_tomorrow

import cinema
from cinema.models import Theater

def test_scrape_endpoint(test_session, test_client, test_worker):
    _wait_for_scrape(test_client, test_worker)
    # Theaters exist in db, and
    # Each theater has a showtime associated with it
    for cinema_name in cinema.showtime_scraper.cinema_ls:
        theater = test_session.query(Theater).filter_by(name = cinema_name).first()
        assert theater
        assert theater.showtimes

# TODO: write a test that uses a real worker
