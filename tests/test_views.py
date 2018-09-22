import pytest
from tests.fixtures import test_app, test_client, test_db, test_session

import cinema
from bs4 import BeautifulSoup
import itertools

# Need to provide test_session so the backend can use it, even though the test body doesn't use it.
def test_shows_tomorrow(test_client, test_session):
    test_client.get('/scrape')
    response = test_client.get('/shows', follow_redirects=True)
    soup = BeautifulSoup(response.data, 'html.parser')
    table_headers = [th.text for th in soup.find_all('th')]
    for cinema_name in cinema.showtime_scraper.cinema_ls:
        assert cinema_name in table_headers

def test_pairwise_disjoint(test_client, test_session):
    # TODO: create a database fixture instead of hitting the scrape endpoint.
    test_client.get('/scrape')
    response = test_client.get('/shows/indie')
    soup = BeautifulSoup(response.data, 'html.parser')
    tables = soup.find_all('table')
    shows = [set([td.text for td in t.find_all('td')]) for t in tables]
    for s1, s2 in itertools.combinations(shows, 2):
        assert s1.isdisjoint(s2)
