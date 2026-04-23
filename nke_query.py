from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector

THRESHOLD = 0.15

code = "def add(a, b): return a - b"
error_type = "AssertionError"
error_message = "expected 5 got -1"
assignment_id = "add_function"

artifact_text = f"""CODE
{code}

ERROR
{error_type}: {error_message}

CONTEXT
{{"assignment":"{assignment_id}"}}"""

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding query artifact...")
query_embedding = model.encode(artifact_text)

print("Connecting to PostgreSQL...")
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    dbname="nke_db",
    user="postgres",
    password="nke1904"
)
register_vector(conn)

cur = conn.cursor()
cur.execute("""
    SELECT
        id,
        assignment_id,
        error_type,
        error_message,
        artifact_text,
        embedding <=> %s AS distance
    FROM failures
    ORDER BY embedding <=> %s
    LIMIT 3
""", (query_embedding, query_embedding))

rows = cur.fetchall()

if not rows:
    print("Decision: UNKNOWN")
    print("Reason: no failures in memory")
else:
    nearest = rows[0]
    dmin = float(nearest[5])

    if dmin <= THRESHOLD:
        print("Decision: REJECTED")
    else:
        print("Decision: UNKNOWN")

    print(f"Nearest distance: {dmin:.6f}")
    print("Top matches:")
    for row in rows:
        print({
            "id": row[0],
            "assignment_id": row[1],
            "error_type": row[2],
            "error_message": row[3],
            "distance": float(row[5])
        })

cur.close()
conn.close()