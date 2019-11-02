from imdbdatabase.DatabaseConstants import session, connection_from
from imdbdatabase.TableCreationHelper import createConnections
from imdbdatabase.TablesDefinition import title, people, rating, principals

# Define which tables should be imported
to_import = [title, people, rating, principals]

def copy_from(file, table):
    file.readline()
    conn, autoclose = connection_from()
    cursor = conn.cursor()

    if session.query("count(*) from " + table).scalar() == 0:
        print("Start importing data from " + file.name)
        cursor.copy_from(file, table)
        print("Finished importing data.")
    else:
        print(table + " already populated. Skipping...")

    if autoclose:
        conn.commit()
        conn.close()

# Execute import
for i in to_import:
    with open(i["file"]) as fp:
        copy_from(fp, i["name"])

createConnections()
