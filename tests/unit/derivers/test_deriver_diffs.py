from datetime import datetime

from nortech.derivers import DeriverDiffs


def test_deriver_diffs():
    test_schema = {
        "id": 123,
        "hash": "abc123",
        "historyId": 456,
        "createdAt": datetime(2023, 1, 1),
        "updatedAt": datetime(2023, 1, 2),
    }
    test_deriver_diffs_dict = {
        "deriverSchemas": {"schema1": {"previousSchema": test_schema, "newSchema": test_schema}},
        "derivers": {"deriver1": {"previousSchema": test_schema, "newSchema": test_schema}},
    }

    deriver_diffs = DeriverDiffs.model_validate(test_deriver_diffs_dict)

    assert deriver_diffs.deriver_schemas["schema1"].old.id == 123
    assert deriver_diffs.deriver_schemas["schema1"].old.hash == "abc123"
    assert deriver_diffs.deriver_schemas["schema1"].old.history_id == 456
    assert deriver_diffs.deriver_schemas["schema1"].old.created_at == datetime(2023, 1, 1)
    assert deriver_diffs.deriver_schemas["schema1"].old.updated_at == datetime(2023, 1, 2)

    assert deriver_diffs.derivers["deriver1"].new.id == 123
    assert deriver_diffs.derivers["deriver1"].new.hash == "abc123"
    assert deriver_diffs.derivers["deriver1"].new.history_id == 456
    assert deriver_diffs.derivers["deriver1"].new.created_at == datetime(2023, 1, 1)
    assert deriver_diffs.derivers["deriver1"].new.updated_at == datetime(2023, 1, 2)
