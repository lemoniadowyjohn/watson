from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable

KEY_FIELDS = ("component_id", "variant")


@dataclass(frozen=True)
class ReconciliationRow:
    component_id: str
    variant: str
    reconciliation_status: str
    reason_codes: str
    description_a: str = ""
    description_b: str = ""
    quantity_a: str = ""
    quantity_b: str = ""
    status_a: str = ""
    status_b: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "component_id": self.component_id,
            "variant": self.variant,
            "reconciliation_status": self.reconciliation_status,
            "reason_codes": self.reason_codes,
            "description_a": self.description_a,
            "description_b": self.description_b,
            "quantity_a": self.quantity_a,
            "quantity_b": self.quantity_b,
            "status_a": self.status_a,
            "status_b": self.status_b,
        }


def _text(value: object) -> str:
    return "" if value is None else " ".join(str(value).strip().split())


def _norm_text(value: object) -> str:
    return _text(value).casefold()


def _decimal(value: object) -> Decimal | None:
    text = _text(value).replace(",", ".")
    if not text:
        return None
    try:
        return Decimal(text)
    except InvalidOperation:
        return None


def _key(record: dict[str, object]) -> tuple[str, str]:
    return tuple(_text(record.get(field)) for field in KEY_FIELDS)  # type: ignore[return-value]


def _index(
    records: Iterable[dict[str, object]],
) -> tuple[
    dict[tuple[str, str], dict[str, object]],
    set[tuple[str, str]],
    list[dict[str, object]],
]:
    rows = list(records)
    keys = [_key(row) for row in rows]
    counts = Counter(keys)
    duplicates = {key for key, count in counts.items() if count > 1 and all(key)}
    valid: dict[tuple[str, str], dict[str, object]] = {}
    invalid: list[dict[str, object]] = []
    for row, key in zip(rows, keys):
        if not all(key):
            invalid.append(row)
        elif key not in duplicates:
            valid[key] = row
    return valid, duplicates, invalid


def _compare(
    a: dict[str, object],
    b: dict[str, object],
    quantity_tolerance: Decimal,
) -> list[str]:
    reasons: list[str] = []
    if _norm_text(a.get("description")) != _norm_text(b.get("description")):
        reasons.append("DESCRIPTION_DIFFERENCE")

    qa = _decimal(a.get("quantity"))
    qb = _decimal(b.get("quantity"))
    if qa is None or qb is None:
        if _text(a.get("quantity")) != _text(b.get("quantity")):
            reasons.append("QUANTITY_INVALID_OR_DIFFERENT")
    elif abs(qa - qb) > quantity_tolerance:
        reasons.append("QUANTITY_DIFFERENCE")

    if _norm_text(a.get("status")) != _norm_text(b.get("status")):
        reasons.append("STATUS_DIFFERENCE")
    return reasons


def _row(
    key: tuple[str, str],
    status: str,
    reasons: list[str],
    a: dict[str, object] | None = None,
    b: dict[str, object] | None = None,
) -> ReconciliationRow:
    a = a or {}
    b = b or {}
    return ReconciliationRow(
        component_id=key[0],
        variant=key[1],
        reconciliation_status=status,
        reason_codes=";".join(reasons),
        description_a=_text(a.get("description")),
        description_b=_text(b.get("description")),
        quantity_a=_text(a.get("quantity")),
        quantity_b=_text(b.get("quantity")),
        status_a=_text(a.get("status")),
        status_b=_text(b.get("status")),
    )


def reconcile_records(
    source_a: Iterable[dict[str, object]],
    source_b: Iterable[dict[str, object]],
    *,
    quantity_tolerance: Decimal = Decimal("0"),
) -> list[ReconciliationRow]:
    """Reconcile two record sets without mutating either source."""
    a_index, a_dupes, a_invalid = _index(source_a)
    b_index, b_dupes, b_invalid = _index(source_b)
    out: list[ReconciliationRow] = []

    for key in sorted(a_dupes | b_dupes):
        reasons = []
        if key in a_dupes:
            reasons.append("DUPLICATE_KEY_SOURCE_A")
        if key in b_dupes:
            reasons.append("DUPLICATE_KEY_SOURCE_B")
        out.append(_row(key, "INVALID", reasons))

    for source_name, invalid_rows in (("A", a_invalid), ("B", b_invalid)):
        for record in invalid_rows:
            key = _key(record)
            out.append(
                _row(
                    key,
                    "INVALID",
                    [f"MISSING_KEY_SOURCE_{source_name}"],
                    record if source_name == "A" else None,
                    record if source_name == "B" else None,
                )
            )

    blocked = a_dupes | b_dupes
    all_keys = sorted((set(a_index) | set(b_index)) - blocked)
    for key in all_keys:
        a = a_index.get(key)
        b = b_index.get(key)
        if a is None:
            out.append(_row(key, "ONLY_IN_B", ["MISSING_SOURCE_A"], b=b))
            continue
        if b is None:
            out.append(_row(key, "ONLY_IN_A", ["MISSING_SOURCE_B"], a=a))
            continue
        reasons = _compare(a, b, quantity_tolerance)
        out.append(_row(key, "MISMATCH" if reasons else "MATCH", reasons, a=a, b=b))
    return out
