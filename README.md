# Negative Knowledge Engine (NKE) – v1

NKE is a failure-only boundary learning system.

- Stores only failure artifacts (CODE + ERROR + CONTEXT)
- Embeds them into a vector space
- Learns a failure region boundary from negatives only
- For a new input, outputs `REJECTED` or `UNKNOWN` with case-based evidence

Initial domain: Python student / junior developer assignments that fail tests or raise exceptions.