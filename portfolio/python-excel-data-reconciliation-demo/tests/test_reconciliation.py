from decimal import Decimal

from reconcile_demo.reconciliation import reconcile_records


def by_key(rows):
    return {(row.component_id, row.variant): row for row in rows}


def test_match_normalizes_text_and_numeric_values():
    rows = reconcile_records(
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "Front  bracket",
                "quantity": "10",
                "status": "Open",
            }
        ],
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "front bracket",
                "quantity": "10.0",
                "status": "open",
            }
        ],
    )
    assert rows[0].reconciliation_status == "MATCH"
    assert rows[0].reason_codes == ""


def test_mismatch_emits_explicit_reason_codes():
    rows = reconcile_records(
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "Bracket",
                "quantity": "10",
                "status": "Open",
            }
        ],
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "Bracket B",
                "quantity": "12",
                "status": "Closed",
            }
        ],
    )
    assert rows[0].reconciliation_status == "MISMATCH"
    assert set(rows[0].reason_codes.split(";")) == {
        "DESCRIPTION_DIFFERENCE",
        "QUANTITY_DIFFERENCE",
        "STATUS_DIFFERENCE",
    }


def test_quantity_tolerance_is_configurable():
    rows = reconcile_records(
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "X",
                "quantity": "10",
                "status": "Open",
            }
        ],
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "X",
                "quantity": "10.04",
                "status": "Open",
            }
        ],
        quantity_tolerance=Decimal("0.05"),
    )
    assert rows[0].reconciliation_status == "MATCH"


def test_records_present_on_only_one_side_are_preserved_as_exceptions():
    rows = by_key(
        reconcile_records(
            [
                {
                    "component_id": "A1",
                    "variant": "V1",
                    "description": "X",
                    "quantity": "1",
                    "status": "Open",
                }
            ],
            [
                {
                    "component_id": "B1",
                    "variant": "V2",
                    "description": "Y",
                    "quantity": "1",
                    "status": "Open",
                }
            ],
        )
    )
    assert rows[("A1", "V1")].reconciliation_status == "ONLY_IN_A"
    assert rows[("B1", "V2")].reconciliation_status == "ONLY_IN_B"


def test_duplicate_keys_are_invalid_not_silently_overwritten():
    rows = reconcile_records(
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "X",
                "quantity": "1",
                "status": "Open",
            },
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "Y",
                "quantity": "2",
                "status": "Open",
            },
        ],
        [
            {
                "component_id": "A1",
                "variant": "V1",
                "description": "X",
                "quantity": "1",
                "status": "Open",
            }
        ],
    )
    assert rows[0].reconciliation_status == "INVALID"
    assert "DUPLICATE_KEY_SOURCE_A" in rows[0].reason_codes


def test_missing_business_key_is_invalid():
    rows = reconcile_records(
        [
            {
                "component_id": "",
                "variant": "V1",
                "description": "X",
                "quantity": "1",
                "status": "Open",
            }
        ],
        [],
    )
    assert rows[0].reconciliation_status == "INVALID"
    assert rows[0].reason_codes == "MISSING_KEY_SOURCE_A"
