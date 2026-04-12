import json
import requests
import streamlit as st

st.set_page_config(
    page_title="NKE v1",
    page_icon="🧠",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"


def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if response.status_code == 200:
            return True, response.json()
        return False, {"error": f"Unexpected status code: {response.status_code}"}
    except Exception as e:
        return False, {"error": str(e)}


def build_preview_artifact(code: str, error: str, context: dict) -> str:
    return f"""CODE:
{code}

ERROR:
{error}

CONTEXT:
{context}
"""


st.title("🧠 Negative Knowledge Engine (NKE) – v1")
st.caption("Failure-only boundary learning demo shell")

with st.sidebar:
    st.subheader("Backend Status")
    if st.button("Check Backend"):
        ok, result = check_backend()
        if ok:
            st.success("Backend is running")
            st.json(result)
        else:
            st.error("Backend is not reachable")
            st.json(result)

    st.markdown("---")
    st.subheader("NKE Rules")
    st.markdown(
        """
- Only failures
- Artifact = CODE + ERROR + CONTEXT
- Output only: `REJECTED` or `UNKNOWN`
- No success prediction
- No fix suggestions
        """
    )

st.markdown("## Submit Code")

default_code = """def add(a, b):
    return a - b
"""

code_input = st.text_area(
    "Paste Python code",
    value=default_code,
    height=250,
    placeholder="Paste Python code here..."
)

assignment_name = st.text_input(
    "Assignment / Context Label",
    value="add_function"
)

error_input = st.text_input(
    "Captured Error (temporary manual input)",
    value="AssertionError: expected 5 got 1"
)

analyze = st.button("Analyze with NKE")

if analyze:
    context = {"assignment": assignment_name}

    with st.spinner("Preparing artifact...", show_time=True):
        artifact = build_preview_artifact(
            code=code_input,
            error=error_input,
            context=context
        )

    st.success("Artifact prepared")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Artifact Preview")
        st.code(artifact, language="text")

    with col2:
        st.markdown("### Current Decision")
        st.warning("Backend analyze endpoint not connected yet")
        st.write("Temporary status: `PENDING`")

        st.markdown("### Context")
        st.json(context)

st.markdown("---")
st.markdown("## Next Integration Step")
st.info(
    "Next, connect this button to the backend `/analyze` endpoint once the artifact runner and API are ready."
)