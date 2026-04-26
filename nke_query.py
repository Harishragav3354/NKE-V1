import os
import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

# Load model globally so it stays in memory across API requests
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2') # 

# Calibrated 75th-percentile threshold for V1
THRESHOLD = 0.3827787041664079 # [cite: 197]

def build_artifact_text(code: str, error_type: str, error_message: str, assignment_id: str) -> str:
    """Constructs the canonical deterministic text artifact."""
    return f"CODE:\n{code}\nERROR:\n{error_type}: {error_message}\nCONTEXT:\nAssignment: {assignment_id}\nBug Type: {error_type}" # [cite: 347, 348]

def analyze_failure(code: str, error_type: str, error_message: str, assignment_id: str) -> dict:
    """
    Encodes the submission, queries the negative knowledge base, 
    and returns an epistemic exclusion decision.
    """
    # 1. Build and encode artifact
    artifact_text = build_artifact_text(code, error_type, error_message, assignment_id)
    query_embedding = model.encode(artifact_text).tolist()

    # 2. Database connection
    db_password = os.getenv("nke1904", "postgres")
    
    try:
        with psycopg.connect(dbname="nke_db", user="postgres", password="nke1904", host="localhost", port="5432") as conn:
            # Register pgvector for Psycopg 3
            register_vector(conn)
            
            with conn.cursor() as cur:
                # Querying error_message directly from the table
                cur.execute("""
                    SELECT id, assignment_id, error_type, error_message, embedding <=> %s::vector AS distance
                    FROM failures
                    ORDER BY distance ASC
                    LIMIT 3;
                """, (query_embedding,))
                
                results = cur.fetchall()
    except Exception as e:
        raise RuntimeError(f"Database query failed: {e}")

    # 3. Process results
    top_matches = []
    nearest_distance = None

    if results:
        nearest_distance = float(results[0][4])
        for r in results:
            top_matches.append({
                "id": r[0],
                "assignment_id": r[1],
                "error_type": r[2],
                "error_message": r[3],
                "distance": float(r[4])
            })

    # 4. Enforce Epistemic Boundary
    decision = "UNKNOWN" # 
    if nearest_distance is not None and nearest_distance <= THRESHOLD: # [cite: 354]
        decision = "REJECTED" # 

    return {
        "decision": decision,
        "nearest_distance": nearest_distance,
        "top_matches": top_matches
    }