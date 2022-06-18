import pandas as pd
import uuid
import sqlite3
import csv
import glob

TEMP_CSV_CHUNK_SIZE = 100_000
CONNECTION_STRING =  '/mnt/c/Users/Ana/Desktop/anapaula2.db'

def database_migration_trips(connection_string):
    with sqlite3.connect(connection_string) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM trips LIMIT 1")
            cursor.fetchall()
        except:
            cursor.execute("""DROP TABLE IF EXISTS trips;""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS trips(
                    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    region TEXT,
                    datetime DATETIME,
                    origin_latitude REAL,
                    origin_longitude REAL,
                    destination_latitude REAL,
                    destination_longitude REAL,
                    data_source TEXT,
                    cluster_id UUID
                );""")

def database_migration_trip_chunks(connection_string):
    with sqlite3.connect(connection_string) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM trip_clusters LIMIT 1")
            cursor.fetchall()
        except:
            cursor.execute("""DROP TABLE IF EXISTS trip_clusters;""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS trip_clusters(
                    cluster_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hour INTEGER,
                    origin_ints INTEGER,
                    destination_ints INTEGER
                );""")

def process_input_into_csv_chunks():
    all_csv_input_files = glob.glob('INPUT/*.csv')
    for csv_file in all_csv_input_files:
        df = pd.read_csv(csv_file)
        # Process columns
        df['region'] = df['region'].str.lower()
        df['origin_coord'] = df['origin_coord'].apply(lambda x: x.replace('POINT (', '').replace(')', '') if x and type(x) != float else x)
        df[['origin_latitude', 'origin_longitude']] = df['origin_coord'].str.split(' ', 1, expand=True).astype(float)
        df['destination_coord'] = df['destination_coord'].apply(lambda x: x.replace('POINT (', '').replace(')', '') if x and type(x) != float else x)
        df[['destination_latitude', 'destination_longitude']] = df['destination_coord'].str.split(' ', 1, expand=True).astype(float)
        df['data_source'] = df['datasource']
        # df['cluster_id'] = None
        # df['trip_id'] = df.apply(lambda _: uuid.uuid4(), axis=1)
        # df['trip_id'] = None
        df = df.drop(['origin_coord', 'destination_coord', 'datasource'], axis=1)

        # Reorder columns
        # df = df[df.columns.tolist()[-1:] + df.columns.tolist()[:-1]]

        # Save temp csv files in chunks
        for i in range(0, len(df), TEMP_CSV_CHUNK_SIZE):
            df[i : i + TEMP_CSV_CHUNK_SIZE].to_csv('TEMP/' + str(i) + '.csv', index=False, header=False, chunksize=10_000)

def insert_data_from_temp_csvs_into_db(connection_string):
    with sqlite3.connect(connection_string) as conn:
        cursor = conn.cursor()

        temp_csv_files = glob.glob('TEMP/*.csv')
        for temp_csv_file in temp_csv_files:
            print(temp_csv_file)
            rows = csv.reader(open(temp_csv_file))
            try:
                cursor.executemany("INSERT INTO trips VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, NULL);", rows)
            except Exception as err:
                print(err)

def clusterize_trips(connection_string):
    with sqlite3.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trips")
        cursor.execute("SELECT count(*) FROM trips")
        print(cursor.fetchall())


if __name__ == "__main__":
    process_input_into_csv_chunks()
    database_migration_trips(CONNECTION_STRING)
    database_migration_trip_chunks(CONNECTION_STRING)
    insert_data_from_temp_csvs_into_db(CONNECTION_STRING)
    clusterize_trips(CONNECTION_STRING)


