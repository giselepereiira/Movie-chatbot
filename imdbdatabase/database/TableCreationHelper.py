from imdbdatabase.database.DatabaseConstants import connection_from


def createConnections():

    connection, autoclose = connection_from()
    cursor = connection.cursor()

    print('Deleting non-movies')

    # Consider only movies
    cursor.execute('''DELETE FROM title WHERE \"titleType\" != 'movie' ''')

    connection.commit()

    # Merge two columns to table titles: language and rating
    cursor.execute('''ALTER TABLE title ADD "rating" float''')
    cursor.execute('''ALTER TABLE title ADD "language" varchar(10)''')
    cursor.execute('''UPDATE title 
    SET rating = title_ratings."averageRating" 
    FROM title_ratings 
    WHERE title_ratings.tconst = title.tconst''')

    cursor.execute('''UPDATE title 
    SET \"language\" = title_akas.\"language\" 
    FROM title_akas 
    WHERE title_akas.\"titleId\" = title.tconst
    AND title_akas.\"title" = title.\originalTitle\"''')

    print('Creating names table indexes...')

    # Create people_title relation
    cursor.execute('''DROP TABLE IF EXISTS people_title''')

    cursor.execute(
        '''CREATE TABLE people_title
        (
            PRIMARY KEY(id_names, id_titles),
            id_names text,
            id_titles text
        )'''
    )

    cursor.execute(
        '''alter table title_principals add constraint title_fk FOREIGN key (tconst) references title(tconst) ON DELETE CASCADE;'''
    )

    cursor.execute(
        '''alter table title_principals add constraint people_fk FOREIGN key (nconst) references people(nconst) ON DELETE CASCADE;'''
    )

    cursor.execute('''alter table title_principals add column id SERIAL primary key''')

    connection.commit()

    print('Table and foreign keys were created')

    print('Deleting people that had no participation in movies and are not actor/actress or director.')

    cursor.execute('''DELETE FROM people 
    WHERE "primaryProfession" NOT ILIKE '%%actor%%' 
    AND "primaryProfession" NOT ILIKE '%%actress%%' 
    AND p."primaryProfession" NOT ILIKE '%%director%%')
    AND nconst IN (select nconst from people f 
    LEFT JOIN title_principals d on f.nconst = d.id_names
    WHERE d.nconst IS NULL)''')
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