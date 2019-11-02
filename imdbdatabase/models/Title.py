from sqlalchemy import Column, String, Integer

from imdbdatabase.database.DatabaseConstants import Base


class Title(Base):
    __tablename__ = 'title'

    id = Column('tconst', String, primary_key=True)
    title = Column('originalTitle', String)
    type = Column('titleType', String)
    year = Column('startYear', Integer)
    time = Column('runtimeMinutes', Integer)
    genre = Column('genres', String)