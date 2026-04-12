def run_code(code: str):
    try:
        local_env = {}
        exec(code, {}, local_env)

        if "add" in local_env:
            result = local_env["add"](2, 3)
            assert result == 5, f"AssertionError: expected 5 got {result}"

        return "NO_ERROR"

    except Exception as e:
        return f"{type(e).__name__}: {e}"