import streamlit as st
import requests

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="NKE V1 | Epistemic Exclusion", layout="centered")

st.title("Negative Knowledge Engine (NKE)")
st.caption("Memory of known failures. No predictions. No fixes. Only exclusions.")
st.markdown("---")

# --- Artifact Input ---
st.markdown("### Submission Artifact")
col1, col2 = st.columns(2)
with col1:
    assignment_id = st.text_input("Assignment ID", value="add_function")
with col2:
    error_type = st.text_input("Error Type", value="AssertionError")

error_message = st.text_input("Error Message", value="expected 5 got -1")
code = st.text_area("Code Snippet", value="def add(a, b):\n    return a - b", height=150)

# --- Engine Execution ---
if st.button("Evaluate Epistemic Boundary", type="primary"):
    # Ontological unit = full artifact only [cite: 461]
    payload = {
        "code": code,
        "error_type": error_type,
        "error_message": error_message,
        "assignment_id": assignment_id
    }

    with st.spinner("Querying negative memory space..."):
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            decision = data.get("decision")
            distance = data.get("nearest_distance")
            matches = data.get("top_matches", [])

            st.markdown("---")
            
            # --- Output Presentation ---
            if decision == "REJECTED":
                st.error("## 🛑 DECISION: REJECTED")
                st.write(f"**Boundary Margin (Nearest Distance):** `{distance:.4f}`")
                
                st.markdown("### 🔍 Exclusion Precedent")
                st.markdown("This artifact resides within a known failure region. See historical precedents below:")
                
                # Explanations must be retrieval-based [cite: 464]
                for m in matches:
                    st.warning(f"**Failure ID #{m['id']}** | Context: `{m['assignment_id']}`\n\n**{m['error_type']}**: {m['error_message']}\n\n*(Vector Distance: {m['distance']:.4f})*")
            
            else:
                st.success("## ⚪ DECISION: UNKNOWN")
                if distance is not None:
                    st.write(f"**Boundary Margin (Nearest Distance):** `{distance:.4f}`")
                
                # UNKNOWN does not mean correct [cite: 463]
                st.write("No matching failure precedents found within the exclusion threshold. NKE makes no claims regarding the correctness or success of this artifact.")

        except requests.exceptions.RequestException as e:
            st.error(f"API Connection Error: {e}")
            st.info("Ensure the FastAPI backend is actively running on http://127.0.0.1:8000")