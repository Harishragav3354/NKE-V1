


from mutator.test_runner import run_code

code = """
def add(a, b):
    return a - b
"""

error = run_code(code)
print("ERROR:", error)