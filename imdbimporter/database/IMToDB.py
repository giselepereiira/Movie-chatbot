from imdbimporter.database.DatabaseConstants import session, connection_from
from imdbimporter.database.TableCreationHelper import createConnections
from imdbimporter.database.TablesDefinition import title, people, crew

# Define which tables should be imported
to_import = [title, people, crew]


def copy_from(file, table):
    file.readline()
    conn, autoclose = connection_from()
    cursor = conn.cursor()

    if session.query("count(*) from " + table).scalar() == 0:
        print("Start importing data from " + file.name)
        cursor.copy_from(file, table)
        print("Finished importing data.")

        if autoclose:
            conn.commit()
            conn.close()
    else:
        print(table + " already populated. Skipping...")

# Execute import
# for i in to_import:
#   with open(i["file"], encoding="utf8") as fp:
#      copy_from(fp, i["name"])

createConnections()
