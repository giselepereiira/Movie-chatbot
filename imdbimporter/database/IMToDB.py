from imdbimporter.database.DatabaseConstants import engine, session, metadata
from imdbimporter.database.TablesDefinition import title, people, crew

# Define which tables should be imported
to_import = [title, people, crew]

def copy_from(file, table, engine_or_conn):
    file.readline()
    conn, autoclose = connection_from(engine_or_conn)
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

def connection_from(engine_or_conn):
    if hasattr(engine_or_conn, 'cursor'):
        return engine_or_conn, False
    if hasattr(engine_or_conn, 'connection'):
        return engine_or_conn.connection, False
    return engine_or_conn.raw_connection(), True

# Execute import
for i in to_import:
    with open(i["file"], encoding="utf8") as fp:
        copy_from(fp, i["name"], engine)
