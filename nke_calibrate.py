from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Connecting to PostgreSQL...")
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="nke_db",
    user="postgres",
    password="nke1904"
)
register_vector(conn)
cur = conn.cursor()

cur.execute("""
    SELECT id, embedding
    FROM failures
    ORDER BY id
""")
rows = cur.fetchall()

if len(rows) < 2:
    print("Need at least 2 failures to calibrate.")
    cur.close()
    conn.close()
    raise SystemExit

distances = []

for row in rows:
    failure_id = row[0]
    embedding = row[1]

    cur.execute("""
        SELECT embedding <=> %s AS distance
        FROM failures
        WHERE id <> %s
        ORDER BY embedding <=> %s
        LIMIT 1
    """, (embedding, failure_id, embedding))

    nn = cur.fetchone()
    if nn and nn[0] is not None:
        distances.append(float(nn[0]))

distances = np.array(distances, dtype=float)

print("Nearest-neighbor distances:", distances.tolist())
print("50th percentile:", float(np.percentile(distances, 50)))
print("75th percentile:", float(np.percentile(distances, 75)))
print("90th percentile:", float(np.percentile(distances, 90)))

cur.close()
conn.close()