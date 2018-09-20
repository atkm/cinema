from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base

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

class Film(db.Model):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Showtime(db.Model):
    __tablename__ = 'showtime'
    id = Column(Integer, primary_key=True)
    showtime = Column(DateTime(timezone=True))
    theater_id = Column(Integer, ForeignKey('theater.id'))
    theater = relationship("Theater")
    film_id = Column(Integer, ForeignKey('film.id'))
    film = relationship("Film")
