import psycopg2

conn = psycopg2.connect(
    dbname="nke_db",
    user="postgres",
    password="YOUR_PASSWORD",
    host="localhost",
    port="5432"  # or 5433 if that's your actual PostgreSQL port
)

cur = conn.cursor()

for row in failures:
    cur.execute(
        """
        INSERT INTO failures (assignment_id, code, error_type, error_message, artifact_text, context_hash, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (...)
    )

conn.commit()
cur.close()
conn.close()