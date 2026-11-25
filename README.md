# Python Unit Converter

A small command-line tool that converts values between common units of length, weight,
temperature, and volume. Uses only the Python standard library.

## Features

- Length: `mm`, `cm`, `m`, `km`, `in`, `ft`, `yd`, `mi`
- Weight: `mg`, `g`, `kg`, `t`, `oz`, `lb`, `st`
- Volume (US customary): `ml`, `l`, `m3`, `tsp`, `tbsp`, `floz`, `cup`, `pt`, `qt`, `gal`
- Temperature: `c`, `f`, `k`
- Case-insensitive unit names, negative values supported
- `--list` shows every supported unit
- Clear error when converting between incompatible categories (e.g. `kg` to `mi`)
  or for temperatures below absolute zero

## Usage

```bash
# Convert 10 kilometres to miles
python3 converter.py 10 km mi
# 10 km = 6.21371 mi

# Temperatures (negative values work too)
python3 converter.py -40 c f
# -40 c = -40 f

# List all supported units
python3 converter.py --list
```

## Tests

```bash
python3 -m unittest
```
