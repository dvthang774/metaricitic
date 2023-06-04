import csv
import psycopg2


conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=postgres user=postgres")
cur = conn.cursor()

def import_to_metacritic():
    with open('{}-b.csv', 'r').format('2023-05-08') as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
    #         print(row[:6])
            cur.execute(
            """INSERT INTO metacritic(name, platform, release_date, metascore, user_score, year) VALUES (%s, %s, %s, %s, %s, %s)""",
                row
        )
    conn.commit()

def import_to_user_review():
    return
