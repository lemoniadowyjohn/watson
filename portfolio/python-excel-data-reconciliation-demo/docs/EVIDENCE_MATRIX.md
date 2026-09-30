# Evidence Matrix

| Claim | Implementation | Test / evidence |
|---|---|---|
| Deterministic composite-key reconciliation | `reconciliation.py` | unit tests for match/one-sided records |
| Duplicate keys are not silently overwritten | `_index()` duplicate detection | `test_duplicate_keys_are_invalid_not_silently_overwritten` |
| Missing keys are explicit validation failures | `_index()` invalid-record path | `test_missing_business_key_is_invalid` |
| Differences produce machine-readable reason codes | `_compare()` | `test_mismatch_emits_explicit_reason_codes` |
| Numeric tolerance is configurable | `quantity_tolerance` | `test_quantity_tolerance_is_configurable` |
| Human review is preserved | `exceptions` worksheet | report writer + CLI smoke test |
| CSV/XLSX are supported | `io.read_records()` | code path + CI smoke test |

This project is a sanitized portfolio implementation using synthetic records. It supports the candidate's ability to discuss Python/OpenPyXL reconciliation patterns without publishing employer data or claiming that this repository is the original employer implementation.
