import sqlite3
import sys 

CONNECTION_STRING =  'anapaula.db'

def query_by_region(connection_string, region):
    with sqlite3.connect(connection_string) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"""SELECT AVG(weekly_total."count") FROM (
                SELECT strftime('%W%Y', datetime), count(1) as "count" FROM trips WHERE region = '{region}' group by strftime('%W%Y', datetime)
            ) weekly_total;""")
            print(cursor.fetchall())
        except Exception as err:
                print(err)

def query_by_bounding_box(connection_string, bounding_box):
    with sqlite3.connect(connection_string) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"""SELECT AVG(weekly_total."count") FROM (
                                    SELECT strftime('%W%Y', datetime), count(1) as "count" FROM trips t
                                    WHERE (t.origin_latitude > {bounding_box[0]}
                                        and t.origin_longitude > {bounding_box[1]}
                                        and t.origin_latitude < {bounding_box[2]}
                                        and t.origin_longitude < {bounding_box[3]})
                                        or (t.destination_latitude > {bounding_box[0]}
                                        and t.destination_longitude > {bounding_box[1]}
                                        and t.destination_latitude < {bounding_box[2]}
                                        and t.destination_longitude < {bounding_box[3]})
                                    GROUP BY STRFTIME('%W%Y', datetime)
                                ) weekly_total;""")
            print(cursor.fetchall())
        except Exception as err:
            print(err)

def err_log():
    print('ERR processing argvs, \ntry: \n$ python insights.py -r "<region_name>"')
    print('or \n$ python insights.py -bb "<lat_min>,<long_min>;<lat_max>,<long_max>"')
    print('example: \n$ python insights.py -bb "-90,-180;90,180"')
    quit()

if len(sys.argv) == 3 and sys.argv[1] == '-r':
    try:
        query_by_region(CONNECTION_STRING, sys.argv[2])
    except:
        err_log()
elif len(sys.argv) == 3 and sys.argv[1] == '-bb':
    try:
        lat_min=sys.argv[2].split(';')[0].split(',')[0]
        long_min=sys.argv[2].split(';')[0].split(',')[1]
        lat_max=sys.argv[2].split(';')[1].split(',')[0]
        long_max=sys.argv[2].split(';')[1].split(',')[1]
        bounding_box = float(lat_min), float(long_min), float(lat_max), float(long_max)
        query_by_bounding_box(CONNECTION_STRING, bounding_box)
    except:
        err_log()
else:
    err_log()
