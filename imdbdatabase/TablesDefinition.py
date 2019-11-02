from sqlalchemy import Column, Table, MetaData, String, Integer, Boolean, Text, Float

from imdbdatabase.DatabaseConstants import engine

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

title = {"file": "..\\dataset\\title.basics.tsv",
         "name": title_table.name}

people_table = Table('people', metadata,
                     Column('nconst', String, primary_key=True),
                     Column('primaryName', Text),
                     Column('birthYear', Integer),
                     Column('deathYear', Integer),
                     Column('primaryProfession', Text),
                     Column('knownForTitles', Text),)

people = {"file": "..\\dataset\\name.basics.tsv",
         "name": people_table.name}

title_crew_table = Table('title_crew', metadata,
                           Column('title', String),
                           Column('directors', String),
                           Column('writers', String))

crew = {"file": "..\\dataset\\title.crew.tsv",
         "name": title_crew_table.name}

title_rating_table = Table('title_ratings', metadata,
                           Column('tconst', String),
                           Column('averageRating', Float),
                           Column('numVotes', String))

rating = {"file": "..\\dataset\\title_ratings.tsv",
          "name": title_rating_table.name}

title_principals_table = Table('title_principals', metadata,
                               Column('tconst', String),
                               Column('ordering', Integer),
                               Column('nconst', String),
                               Column('category', String),
                               Column('job', String),
                               Column('characters', String))
principals = {"file": "../dataset/title.principals.tsv.tsv",
              "name": title_principals_table.name}

metadata.create_all(engine)
