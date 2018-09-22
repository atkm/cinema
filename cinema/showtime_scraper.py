import pkg_resources
import os
import requests
import datetime
import urllib.parse
from bs4 import BeautifulSoup

from cinema.models import Theater, Film, Showtime

with pkg_resources.resource_stream('cinema', 'resources/cinemas.txt') as f:
    cinema_ls = [line.decode('utf-8').strip() for line in f.readlines()]

def _get_html(cinema_name, days=0):
    """
    Get the showtimes on the date N days from today.
    """
    today = datetime.date.today()
    date = today + datetime.timedelta(days=days)
    q_str = 'https://www.google.com/search?'
    q_kwd = urllib.parse.urlencode({'q': ' '.join([cinema_name, date.strftime('%m/%d')])})
    cinema_html = requests.get(q_str + q_kwd).text
    return cinema_html

# wrap around _get_html to cache the html
def get_html(cinema_name, days=0):
    today = datetime.date.today()
    date = today + datetime.timedelta(days=days)
    fname = '{0}_{1}.html'.format(cinema_name.lower().replace(' ', '_'),
            date.strftime('%Y%m%d'))
    fpath = pkg_resources.resource_filename('cinema', f'resources/{fname}')
    # use a daily cache if available
    if os.path.isfile(fpath):
        with open(fpath) as f:
            return f.read()
    else:
        html = _get_html(cinema_name, days)
        with open(fpath, 'w') as f:
            f.write(html)
        return html


def parse_showtimes(cinema_html):
    soup = BeautifulSoup(cinema_html, 'html.parser')
    showtimes = soup.find_all('tbody')[1] # [0] is search options
    # The div/a class names look random... What are the chances that they rotate names around?
    film_names_class = 'X4s2nb'
    film_times_class = 'e3wEkd'
    each_showtime_class = 'ovxuVd'
    film_names = [a.text for a in showtimes.find_all('a', class_=film_names_class)]
    film_times = showtimes.find_all('div', class_=film_times_class)
    film_times = [[div.text for div in t.find_all('div', class_=each_showtime_class)] for t in film_times]
    showtimes = dict(zip(film_names, film_times))
    return showtimes

def scrape(cinema_name, days=0):
    cinema_html = get_html(cinema_name, days)
    #with open('cinema_nova.html','w') as f:
    #    f.write(cinema_nova.text)
    return parse_showtimes(cinema_html)


def _get_or_create(session, Model, **kw):
    obj = session.query(Model).filter_by(**kw).first()
    if obj:
        return obj
    else:
        return Model(**kw)

# TODO: 
# How to deal with international dates? 
def create_showtimes(session, cinema_name, date, showtimes):
    """
    Returns a generator of Showtimes for the given date and theater.
    date: datetime.date object.
    """
    # Don't do anything if the shows for this (theater, date) have already been added
    if not session.query(Showtime, Film, Theater)\
            .join(Film).join(Theater)\
            .filter(Showtime.showdate == date)\
            .filter(Theater.name == cinema_name)\
            .first():

        for title, time_ls in showtimes.items():
            # get_or_create
            theater = _get_or_create(session, Theater, name=cinema_name)
            film = _get_or_create(session, Film, name=title)
            yield Showtime(
                    showdate = date, # TODO i18n
                    theater = theater,
                    film = film,
                    count = len(time_ls),
                    )

    
if __name__ == '__main__':
    print(scrape('Cinema Nova'))

