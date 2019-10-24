import io

from imdbimporter.database.DatabaseConstants import connection_from


def createConnections():
    connection, autoclose = connection_from()
    cursor = connection.cursor()

    # cursor.execute(
    #    'ALTER TABLE people ALTER COLUMN knownForTitles TYPE text[] USING string_to_array(knownForTitles, \',\')')
    print('Creating names table indexes...')

    cursor.execute('''DROP TABLE IF EXISTS people_title''')

    cursor.execute(
        '''CREATE TABLE people_title
        (   
            PRIMARY KEY(id_names, id_titles),
            id_names text,
            id_titles text
        )'''
    )

    print('Creating many-to-many relationships (people_title)...')

    cursor.execute("SELECT count(*) FROM people")
    nrows = cursor.fetchone()[0]

    rows_to_fetch = 5000

    for i in range(0, nrows, rows_to_fetch):
        query = "SELECT nconst, \"knownForTitles\" FROM people ORDER BY nconst OFFSET " + str(i) + " LIMIT " + str(
            rows_to_fetch)
        cursor.execute(query)
        counter = 0

        data = io.StringIO()

        row = cursor.fetchall()
        counter = counter + len(row)
        if not row:
            break

        for column in row:
            if column[1]:
                for tconst in set(column[1].split(',')):
                    relationship = '\t'.join([column[0], tconst]) + '\n'
                    data.write(relationship)

        data.seek(0)
        cursor.copy_from(data, 'people_title')
        connection.commit()
        print('{} names have been processed'.format(counter), end='\r')

    cursor.close()
    connection.close()
