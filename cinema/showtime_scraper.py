import pkg_resources
import os
import requests
import datetime
import urllib.parse
from bs4 import BeautifulSoup

with pkg_resources.resource_stream('cinema', 'resources/cinemas.txt') as f:
    cinema_ls = [line.decode('utf-8').strip() for line in f.readlines()]

def _get_html(cinema_name):
    q_str = 'https://www.google.com/search?'
    q_kwd = urllib.parse.urlencode({'q': cinema_name})
    cinema_html = requests.get(q_str + q_kwd).text
    return cinema_html

def get_html(cinema_name):
    fname = '{0}_{1}.html'.format(cinema_name.lower().replace(' ', '_'),
            datetime.date.today().strftime('%Y%m%d'))
    fpath = os.path.join(os.path.dirname(__file__), 'resources', fname)
    # use a daily cache if available
    if os.path.isfile(fpath):
        with open(fpath) as f:
            return f.read()
    else:
        html = _get_html(cinema_name)
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

def scrape(cinema_name):
    cinema_html = get_html(cinema_name)
    #with open('cinema_nova.html','w') as f:
    #    f.write(cinema_nova.text)
    return parse_showtimes(cinema_html)
    
if __name__ == '__main__':
    print(scrape('Cinema Nova'))
