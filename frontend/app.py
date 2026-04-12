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


def analyze_code(code: str, context: dict):
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"code": code, "context": context},
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json()
        return False, {
            "error": f"Unexpected status code: {response.status_code}",
            "body": response.text
        }
    except Exception as e:
        return False, {"error": str(e)}


# ─── Header ───────────────────────────────────────────────────────────────────

st.title("🧠 Negative Knowledge Engine (NKE) – v1")
st.caption("Failure-only boundary learning demo")

# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.subheader("Backend Status")
    if st.button("Check Backend"):
        ok, result = check_backend()
        if ok:
            st.success("✅ Backend is running")
            st.json(result)
        else:
            st.error("❌ Backend not reachable")
            st.json(result)

    st.markdown("---")
    st.subheader("NKE Rules")
    st.markdown("""
- Only failures stored
- Artifact = CODE + ERROR + CONTEXT
- Output: `REJECTED` or `UNKNOWN` only
- No success prediction
- No fix suggestions
    """)

# ─── Input Section ────────────────────────────────────────────────────────────

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

analyze = st.button("⚡ Analyze with NKE")

# ─── Analysis ─────────────────────────────────────────────────────────────────

if analyze:
    if not code_input.strip():
        st.warning("⚠️ Please paste some Python code before analyzing.")
    else:
        context = {"assignment": assignment_name}

        with st.spinner("Sending to NKE backend...", show_time=True):
            ok, result = analyze_code(code_input, context)

        if ok:
            st.success("✅ Analysis complete")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Decision")
                if result["decision"] == "REJECTED":
                    st.error(f"🚫 {result['decision']}")
                else:
                    st.info(f"❓ {result['decision']}")

                st.markdown("### Captured Error")
                st.code(result["error"], language="text")

            with col2:
                st.markdown("### Context")
                st.json(result["context"])

            st.markdown("### Artifact")
            st.code(result["artifact"], language="text")

        else:
            st.error("❌ Backend call failed")
            st.json(result)

# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption("NKE v1 — Failure memory engine. No predictions. No fixes. Only exclusions.")