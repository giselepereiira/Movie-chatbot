from imdbdatabase.DatabaseConstants import connection_from


def createConnections():

    connection, autoclose = connection_from()
    cursor = connection.cursor()

    print('Deleting non-movies')

    # Consider only movies
    cursor.execute('''DELETE FROM title WHERE \"titleType\" != 'movie' ''')

    print('Deleting people that had no participation in movies.')

    cursor.execute('''DELETE FROM people 
        WHERE nconst IN (select p.nconst from people p 
        LEFT JOIN title_principals tp on p.nconst = tp.nconst
        WHERE tp.nconst IS NULL)''')

    cursor.execute('''DELETE FROM title_principals 
    WHERE tconst IN (select tp.tconst from title_principals tp 
    LEFT JOIN title t on tp.tconst = t.tconst
    WHERE t.tconst IS NULL);''')

    cursor.execute('''DELETE FROM title_principals 
    WHERE nconst IN (select tp.nconst from title_principals tp 
    LEFT JOIN people p on tp.nconst = p.nconst
    WHERE p.nconst IS NULL);''')
    connection.commit()

    # Merge column rating to table titles

    print('Merging column rating...')

    cursor.execute('''ALTER TABLE title ADD "rating" float''')
    cursor.execute('''UPDATE title 
    SET rating = title_ratings."averageRating" 
    FROM title_ratings 
    WHERE title_ratings.tconst = title.tconst''')

    print('Creating indexes on title_principals...')

    cursor.execute(
        '''alter table title_principals add constraint title_fk FOREIGN key (tconst) references title(tconst);'''
    )

    cursor.execute(
        '''alter table title_principals add constraint people_fk FOREIGN key (nconst) references people(nconst);'''
    )

    cursor.execute('''alter table title_principals add column id SERIAL primary key''')

    connection.commit()

    print('Creating full text search indexes to speed up search.')

    cursor.execute('''CREATE EXTENSION btree_gist''')

    # Create full text search index on primaryName column
    cursor.execute('''ALTER TABLE people ADD "primary_name_vector" tsvector''')
    cursor.execute('''UPDATE people SET "primary_name_vector" = to_tsvector("primaryName")''')
    cursor.execute('''CREATE INDEX primary_name_index ON people USING gin(primary_name_vector)''')
    # Create full text search index on primaryName column

    cursor.execute('''ALTER TABLE title ADD "primary_title_vector" tsvector''')
    cursor.execute('''UPDATE title SET "primary_title_vector" = to_tsvector("primaryTitle")''')
    cursor.execute('''CREATE INDEX primary_title_index ON title USING gin(primary_title_vector)''')

    connection.commit()

    cursor.close()
    connection.close()