from typing import Any

from nortech.derivers.values.physical_units_schema import PhysicalQuantity


def get_physical_quantity(deriver_io: Any) -> PhysicalQuantity:
    physical_quantity = deriver_io[1].json_schema_extra["physical_quantity"]

    if physical_quantity is None:
        raise ValueError(f"Physical quantity is None for ${deriver_io[0]}")

    return PhysicalQuantity(**physical_quantity)
