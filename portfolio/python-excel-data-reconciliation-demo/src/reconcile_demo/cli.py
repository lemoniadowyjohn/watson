from __future__ import annotations

import argparse
from decimal import Decimal

from .io import read_records, write_report
from .reconciliation import reconcile_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile two CSV/XLSX datasets")
    parser.add_argument("source_a")
    parser.add_argument("source_b")
    parser.add_argument("--output", default="reconciliation.xlsx")
    parser.add_argument("--quantity-tolerance", default="0")
    args = parser.parse_args()

    rows = reconcile_records(
        read_records(args.source_a),
        read_records(args.source_b),
        quantity_tolerance=Decimal(args.quantity_tolerance),
    )
    write_report(rows, args.output)
    exceptions = sum(row.reconciliation_status != "MATCH" for row in rows)
    print(f"Wrote {args.output}: {len(rows)} reconciled keys, {exceptions} exception rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
