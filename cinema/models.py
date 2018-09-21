from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base

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

class Film(db.Model):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    showtimes = relationship("Showtime", backref='film')

class Showtime(db.Model):
    __tablename__ = 'showtime'
    id = Column(Integer, primary_key=True)
    showdate = Column(Date)
    theater_id = Column(Integer, ForeignKey('theater.id'))
    film_id = Column(Integer, ForeignKey('film.id'))
    count = Column(Integer)
