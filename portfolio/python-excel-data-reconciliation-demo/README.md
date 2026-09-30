# Python / Excel Data Reconciliation Demo

A sanitized portfolio implementation of a common industrial-data task: reconcile two tabular sources, validate required fields and business keys, classify discrepancies, and produce a reviewable exception report instead of silently overwriting uncertain data.

## Why this project exists

Spreadsheet-heavy engineering and quality processes often depend on records coming from different exports or manually maintained files. The hard part is not reading Excel: it is making matching rules, discrepancies and review decisions explicit and reproducible.

This repository demonstrates the same **type of deterministic reconciliation and validation engineering** used in professional Python/OpenPyXL/Excel work, using only synthetic data. It does not publish employer/customer data or claim that this sample is the original employer implementation.

## Workflow

```text
Source A (CSV/XLSX) ─┐
                     ├─> normalize + validate keys
Source B (CSV/XLSX) ─┘
                          ↓
                  deterministic matching
                          ↓
              field-by-field comparison
                          ↓
              status + reason-code output
                    /               \
               matched           exceptions
                                  ↓
                         reviewable XLSX report
```

## Demonstrated controls

- explicit composite business key (`component_id`, `variant`);
- duplicate-key detection;
- missing-key validation;
- normalized text/numeric comparison;
- configurable tolerance for numeric quantity differences;
- deterministic reason codes;
- separate `MATCH`, `MISMATCH`, `ONLY_IN_A`, `ONLY_IN_B`, `INVALID` states;
- exception-first output suitable for human review;
- CSV and XLSX input/output support;
- pytest regression tests;
- no hidden modification of source files.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
python -m reconcile_demo.cli \
  data/synthetic/source_a.csv \
  data/synthetic/source_b.csv \
  --output out/reconciliation.xlsx
```

The output workbook contains:

- `results` — one row per reconciled key with status and reason codes;
- `exceptions` — only non-matching/invalid records;
- `summary` — counts by reconciliation status.

## Verification

Pre-release local verification on 2026-09-30:

- 6/6 tests passed;
- Python compilation passed;
- end-to-end synthetic CLI run passed;
- output workbook contained `results`, `exceptions`, and `summary` sheets.

GitHub Actions repeats install, tests, compilation, and CLI smoke testing.

## Claim boundary

**Evidence level:** public sanitized portfolio implementation.

Defensible CV/interview wording:

> Built Python/OpenPyXL/Excel tools for deterministic data reconciliation, validation and reviewable exception reporting in professional workflow contexts; public portfolio sample uses synthetic data.

Do not infer from this repository that a specific employer dataset, architecture or production system has been published.

## Repository structure

```text
src/reconcile_demo/
  reconciliation.py   matching, validation and comparison logic
  io.py               CSV/XLSX readers and XLSX report writer
  cli.py              command-line entry point
tests/
  test_reconciliation.py
data/synthetic/
  source_a.csv
  source_b.csv
docs/
  EVIDENCE_MATRIX.md
```

## Design choices

The implementation intentionally favors transparent rules over fuzzy or AI-based matching. Ambiguous records are surfaced as exceptions. This makes the workflow easier to audit, test and explain in an engineering or quality context.
