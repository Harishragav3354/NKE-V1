from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector

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

print("Encoding artifact...")
embedding = model.encode(artifact_text)

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
    INSERT INTO failures (
        assignment_id,
        code,
        error_type,
        error_message,
        artifact_text,
        context_hash,
        embedding
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (
    assignment_id,
    code,
    error_type,
    error_message,
    artifact_text,
    assignment_id + "_v1",
    embedding
))

conn.commit()
cur.close()
conn.close()

print("Inserted 1 real NKE failure successfully.")