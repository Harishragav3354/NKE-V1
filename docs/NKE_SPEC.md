# NKE Epistemic Contract – v1

- Ontological unit: complete artifact = CODE + ERROR + CONTEXT.
- Learning: only from failures (no success / positive examples).
- Output: only `REJECTED` or `UNKNOWN`.
- No probabilities, no “likely to fail”, no success claims, no suggestions.
- Explanations: retrieval-only (nearest failure IDs + error_type).
- artifact_text is canonical and stored verbatim.
- Threshold T is calibrated from distances among failures only.
- If implementation conflicts with this contract, implementation is wrong, not the contract.