import pytest
from tests.fixtures import test_app, test_client, test_worker, test_db, test_session, _wait_for_scrape, fake_redis

import cinema
from bs4 import BeautifulSoup
import itertools

# Need to provide test_session so the backend can use it, even though the test body doesn't use it.
def test_shows_tomorrow(test_client, test_session, fake_redis):

    response = test_client.get('/scrape', follow_redirects=True)
    assert response.status_code == 200

    response = test_client.get('/shows', follow_redirects=True)
    soup = BeautifulSoup(response.data, 'html.parser')
    table_headers = [th.text for th in soup.find_all('th')]
    for cinema_name in cinema.showtime_scraper.cinema_ls:
        assert cinema_name in table_headers

def test_pairwise_disjoint(test_client, test_session, test_worker, fake_redis):
    # TODO: create a database fixture instead of hitting the scrape endpoint.

    response = test_client.get('/scrape', follow_redirects=True)
    assert response.status_code == 200

    response = test_client.get('/shows/indie')
    soup = BeautifulSoup(response.data, 'html.parser')
    tables = soup.find_all('table')
    assert tables
    shows = [set([td.text for td in t.find_all('td')]) for t in tables]
    for s1, s2 in itertools.combinations(shows, 2):
        assert s1.isdisjoint(s2)
