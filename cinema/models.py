from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

import datetime

"""
Theater table:

| id | name |
| -- | ---- |
|  * | varchar |

Film table: same as Theater

Showtime:

| theater_id | film_id |       datetime       |  count   |
|  --------  | ------- |  ------------------  |  ------  |
|     *      |    *    | timestamp + timezone | smallint |


"""

db = SQLAlchemy()
migrate = Migrate()

#Base = declarative_base()

class Theater(db.Model):
    __tablename__ = 'theater'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    showtimes = relationship("Showtime", backref='theater')

    def __str__(self):
        return f'Theater({self.name})'

    def __repr__(self):
        return self.__str__()

class Film(db.Model):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    showtimes = relationship("Showtime", backref='film')

    def __str__(self):
        return f'Film({self.name})'

    def __repr__(self):
        return self.__str__()


class Showtime(db.Model):
    __tablename__ = 'showtime'
    id = Column(Integer, primary_key=True)
    showdate = Column(Date)
    theater_id = Column(Integer, ForeignKey('theater.id'))
    film_id = Column(Integer, ForeignKey('film.id'))
    count = Column(Integer)

    def __str__(self):
        return f'Showtime({self.showdate}, {self.theater_id}, {self.film_id})'

    def __repr__(self):
        return self.__str__()

