import io

from imdbimporter.database.DatabaseConstants import connection_from


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
        '''alter table people_title add constraint title_fk FOREIGN key (id_titles) references title(tconst) ON DELETE CASCADE;'''
    )

    cursor.execute(
        '''alter table people_title add constraint people_fk FOREIGN key (id_names) references people(nconst) ON DELETE CASCADE;'''
    )

    connection.commit()

    print('Table and foreign keys were created')

    cursor.execute("SELECT tconst FROM title")
    titles = cursor.fetchall()

    title_ids = set()
    for i in titles:
        title_ids.add(i[0])

    print('Creating many-to-many relationships (people_title)...')

    cursor.execute("SELECT count(*) FROM people")
    nrows = cursor.fetchone()[0]

    rows_to_fetch = 5000
    counter = 0

    for i in range(0, nrows, rows_to_fetch):
        query = "SELECT nconst, \"knownForTitles\" " \
                "FROM people " \
                "ORDER BY nconst " \
                "OFFSET " + str(i) + " " \
                                     "LIMIT " + str(rows_to_fetch)
        cursor.execute(query)

        data = io.StringIO()

        row = cursor.fetchall()
        counter = counter + len(row)
        if not row:
            break

        for column in row:
            if column[1]:
                for tconst in set(column[1].split(',')):
                    if tconst in title_ids:
                        relationship = '\t'.join([column[0], tconst]) + '\n'
                        data.write(relationship)

        data.seek(0)
        cursor.copy_from(data, 'people_title')
        connection.commit()
        print(str(counter) + ' names out of ' + str(nrows) + ' have been processed.')

    # Remove people that have no connections with movies

    print('Deleting people that had no participation in movies and are not actor/actress or director.')

    cursor.execute('''DELETE FROM people 
    WHERE "primaryProfession" NOT ILIKE '%%actor%%' 
    AND "primaryProfession" NOT ILIKE '%%actress%%' 
    AND p."primaryProfession" NOT ILIKE '%%director%%')
    AND nconst IN (select nconst from people f 
    LEFT JOIN people_title d on f.nconst = d.id_names
    WHERE d.id_names IS NULL)''')
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