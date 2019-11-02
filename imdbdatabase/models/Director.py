from sqlalchemy import Text, Column, Integer, String

from imdbdatabase.database.DatabaseConstants import Base


class People(Base):
    id = Column('nconst', String, primary_key=True),
    name = Column('primaryName', Text),
    birth_year = Column('birthYear', Integer),
    death_year = Column('deathYear', Integer),
    profession = Column('primaryProfession', Text)
    #movies_directed = relationship("knownForTitles", secondary)