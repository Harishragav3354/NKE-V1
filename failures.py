from getpass import getpass
import hashlib
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer


def generate_synthetic_failures():
    return [
        {
            "assignment_id": "python_failure_v1",
            "error_type": "IndexError",
            "bug_type": "out_of_bounds_access",
            "code": "items = [10, 20, 30]\nprint(items[3])",
            "expected_issue": "List index is out of range."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "TypeError",
            "bug_type": "string_int_concat",
            "code": "age = 21\nmessage = 'Age: ' + age\nprint(message)",
            "expected_issue": "Cannot concatenate string and integer."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "AssertionError",
            "bug_type": "failed_assertion",
            "code": "result = 2 + 2\nassert result == 5",
            "expected_issue": "Assertion condition is false."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "ZeroDivisionError",
            "bug_type": "divide_by_zero",
            "code": "numerator = 10\ndenominator = 0\nprint(numerator / denominator)",
            "expected_issue": "Division by zero."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "KeyError",
            "bug_type": "missing_dictionary_key",
            "code": "student = {'name': 'Asha', 'age': 20}\nprint(student['grade'])",
            "expected_issue": "Key does not exist in dictionary."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "ValueError",
            "bug_type": "invalid_int_conversion",
            "code": "text = '12A'\nvalue = int(text)\nprint(value)",
            "expected_issue": "Invalid literal for integer conversion."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "AttributeError",
            "bug_type": "missing_method_call",
            "code": "name = 'python'\nprint(name.uppercase())",
            "expected_issue": "String object has no such attribute."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "IndexError",
            "bug_type": "loop_off_by_one",
            "code": "nums = [1, 2, 3]\nfor i in range(len(nums) + 1):\n    print(nums[i])",
            "expected_issue": "Loop goes one step too far."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "TypeError",
            "bug_type": "wrong_argument_type",
            "code": "def square(n):\n    return n * n\n\nprint(square(None))",
            "expected_issue": "Function receives an invalid type."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "ValueError",
            "bug_type": "empty_string_to_int",
            "code": "text = ''\nnum = int(text)\nprint(num)",
            "expected_issue": "Empty string cannot be converted to int."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "AttributeError",
            "bug_type": "none_object_method_call",
            "code": "user = None\nprint(user.strip())",
            "expected_issue": "NoneType object has no attribute."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "KeyError",
            "bug_type": "wrong_key_name",
            "code": "data = {'id': 101, 'score': 88}\nprint(data['marks'])",
            "expected_issue": "Requested key is not present."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "ZeroDivisionError",
            "bug_type": "mod_by_zero",
            "code": "x = 15\ny = 0\nprint(x % y)",
            "expected_issue": "Modulo by zero."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "AssertionError",
            "bug_type": "boundary_assertion",
            "code": "n = 0\nassert n > 0",
            "expected_issue": "Boundary condition fails."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "TypeError",
            "bug_type": "wrong_return_type",
            "code": "def add(a, b):\n    return str(a + b)\n\nresult = add(2, 3)\nassert isinstance(result, int)",
            "expected_issue": "Function returns the wrong type."
        },
        {
            "assignment_id": "python_failure_v1",
            "error_type": "IndexError",
            "bug_type": "pop_from_empty_list",
            "code": "stack = []\nitem = stack.pop()\nprint(item)",
            "expected_issue": "Operation assumes list has at least one element."
        },
    ]


def build_artifact_text(failure):
    return f"""CODE
{failure['code']}

ERROR
{failure['error_type']}: {failure['expected_issue']}

CONTEXT
{{"assignment_id":"{failure['assignment_id']}","bug_type":"{failure['bug_type']}"}}"""


def make_context_hash(failure):
    raw = f"{failure['assignment_id']}|{failure['bug_type']}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main():
    db_password = getpass("PostgreSQL password: ")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="nke_db",
        user="postgres",
        password=db_password
    )
    register_vector(conn)
    cur = conn.cursor()

    failures = generate_synthetic_failures()

    insert_query = """
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
    """

    inserted = 0

    for failure in failures:
        artifact_text = build_artifact_text(failure)
        embedding = model.encode(artifact_text).tolist()
        context_hash = make_context_hash(failure)

        cur.execute(
            insert_query,
            (
                failure["assignment_id"],
                failure["code"],
                failure["error_type"],
                failure["expected_issue"],
                artifact_text,
                context_hash,
                embedding
            )
        )
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted {inserted} synthetic failures successfully.")


if __name__ == "__main__":
    main()