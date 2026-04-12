def build_artifact(code: str, error: str, context: dict) -> str:
    context_str = str(context)

    artifact = f"""CODE:
{code}

ERROR:
{error}

CONTEXT:
{context_str}
"""
    return artifact