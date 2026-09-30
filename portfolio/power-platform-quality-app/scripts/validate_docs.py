from pathlib import Path


ROOT = Path(__file__).parents[1]

REQUIRED = [
    "README.md",
    "schema/dataverse_tables.yaml",
    "docs/architecture.md",
    "flows/issue_approval_flow.md",
    "powerfx/issue_form.md",
    "governance/ALM_AND_SECURITY.md",
    "samples/issues.csv",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        raise SystemExit(f"missing required portfolio files: {missing}")

    sample = (ROOT / "samples/issues.csv").read_text(encoding="utf-8")
    if "synthetic." not in sample:
        raise SystemExit("sample records must remain explicitly synthetic")

    print("portfolio documentation validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
