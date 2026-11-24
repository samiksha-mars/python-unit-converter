#!/usr/bin/env python3
"""Convert values between common units of length, weight, temperature, and volume."""

import argparse
import sys

# Linear units: factor to convert one unit into the category's base unit.
LINEAR_UNITS = {
    "length": {  # base unit: metre
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.344,
    },
    "weight": {  # base unit: kilogram
        "mg": 1e-6,
        "g": 0.001,
        "kg": 1.0,
        "t": 1000.0,
        "oz": 0.028349523125,
        "lb": 0.45359237,
        "st": 6.35029318,
    },
    "volume": {  # base unit: litre (US customary units)
        "ml": 0.001,
        "l": 1.0,
        "m3": 1000.0,
        "tsp": 0.00492892159375,
        "tbsp": 0.01478676478125,
        "floz": 0.0295735295625,
        "cup": 0.2365882365,
        "pt": 0.473176473,
        "qt": 0.946352946,
        "gal": 3.785411784,
    },
}

TEMPERATURE_UNITS = ("c", "f", "k")


def find_category(unit):
    """Return the category name ("length", "temperature", ...) for a unit."""
    unit = unit.lower()
    if unit in TEMPERATURE_UNITS:
        return "temperature"
    for category, units in LINEAR_UNITS.items():
        if unit in units:
            return category
    raise ValueError(f"Unknown unit: {unit!r} (use --list to see supported units)")


def _to_celsius(value, unit):
    if unit == "c":
        return value
    if unit == "f":
        return (value - 32) * 5 / 9
    return value - 273.15  # kelvin


def _from_celsius(value, unit):
    if unit == "c":
        return value
    if unit == "f":
        return value * 9 / 5 + 32
    return value + 273.15  # kelvin


def convert(value, from_unit, to_unit):
    """Convert value from one unit to another within the same category."""
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    source = find_category(from_unit)
    target = find_category(to_unit)
    if source != target:
        raise ValueError(f"Cannot convert {source} ({from_unit}) to {target} ({to_unit})")

    if source == "temperature":
        return _from_celsius(_to_celsius(value, from_unit), to_unit)

    factors = LINEAR_UNITS[source]
    return value * factors[from_unit] / factors[to_unit]


def list_units():
    """Return a human-readable listing of all supported units."""
    lines = []
    for category, units in LINEAR_UNITS.items():
        lines.append(f"{category}: {', '.join(units)}")
    lines.append(f"temperature: {', '.join(TEMPERATURE_UNITS)}")
    return "\n".join(sorted(lines))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert a value between units of length, weight, temperature, and volume."
    )
    parser.add_argument("value", type=float, nargs="?", help="the number to convert")
    parser.add_argument("from_unit", nargs="?", help="unit to convert from, e.g. km")
    parser.add_argument("to_unit", nargs="?", help="unit to convert to, e.g. mi")
    parser.add_argument("--list", action="store_true", help="list supported units and exit")
    args = parser.parse_args(argv)

    if args.list:
        print(list_units())
        return 0

    if args.value is None or args.from_unit is None or args.to_unit is None:
        parser.error("value, from_unit and to_unit are required (or use --list)")

    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"{args.value:g} {args.from_unit} = {result:.6g} {args.to_unit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
