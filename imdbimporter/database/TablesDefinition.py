from sqlalchemy import func, Column, Table, MetaData, String, Integer, Boolean, Text, ForeignKey, orm, create_engine

from imdbimporter.database.DatabaseConstants import engine

metadata = MetaData()

title_table = Table('title', metadata,
  Column('tconst', String, primary_key=True),
  Column('titleType', Text),
  Column('primaryTitle', Text),
  Column('originalTitle', Text),
  Column('isAdult', Boolean),
  Column('startYear', Integer),
  Column('endYear', Integer),
  Column('runtimeMinutes', Integer),
  Column('genres', Text),)

title = {"file": "C:\\Users\\Gisele\\git\\TDX-UC-NLP-DSAcademy\\dataset\\title.basics.tsv",
         "name": title_table.name}

people_table = Table('people', metadata,
                     Column('nconst', String, primary_key=True),
                     Column('primaryName', Text),
                     Column('birthYear', Integer),
                     Column('deathYear', Integer),
                     Column('primaryProfession', Text),
                     Column('knownForTitles', Text),)

people = {"file": "C:\\Users\\Gisele\\git\\TDX-UC-NLP-DSAcademy\\dataset\\name.basics.tsv",
         "name": people_table.name}

title_crew_table = Table('title_crew', metadata,
                           Column('title', String),
                           Column('directors', String),
                           Column('writers', String))

crew = {"file": "C:\\Users\\Gisele\\git\\TDX-UC-NLP-DSAcademy\\dataset\\title.crew.tsv",
         "name": title_crew_table.name}

metadata.create_all(engine)
