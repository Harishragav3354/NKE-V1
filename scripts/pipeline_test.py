from mutator.test_runner import run_code
from nke_core.artifact import build_artifact

code = """
def add(a, b):
    return a - b
"""

error = run_code(code)
context = {"assignment": "add_function"}

artifact = build_artifact(code, error, context)
print(artifact)