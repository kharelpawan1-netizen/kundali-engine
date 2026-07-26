# Kundali Engine Coding Standards

Version: 2.2

---

# Purpose

These standards ensure that the Kundali Engine remains:

- Readable
- Maintainable
- Testable
- BPHS-compliant
- Production quality

Every contributor should follow these standards.

---

# Python Version

Minimum Supported Version

Python 3.9

Do not use features introduced after Python 3.9 unless compatibility is intentionally dropped.

---

# Code Style

Formatting

Black

Maximum line length:

88 characters

Imports

isort

Linting

Ruff

No Ruff warnings should remain before committing.

---

# Type Hints

All public functions must use type hints.

Example

def julian_day(
    year: int,
    month: int,
    day: int,
) -> float:

Avoid untyped public APIs.

---

# Docstrings

Every public function requires a docstring.

Use Google-style or NumPy-style consistently.

Example

"""
Compute the Julian Day.

Parameters
----------
year : int

Returns
-------
float
"""

---

# Naming Conventions

Classes

PascalCase

Examples

BirthData

Planet

Chart

Graha

Functions

snake_case

Examples

julian_day()

longitude_to_sign()

nakshatra_pada()

Variables

snake_case

Examples

sidereal_longitude

planet_degree

house_number

Constants

UPPER_CASE

Examples

TOTAL_SIGNS

NAKSHATRA_SIZE

PADA_SIZE

---

# Enumerations

Use Enum for finite sets.

Examples

Graha

ZodiacSign

Element

Never compare magic strings.

Preferred

if graha == Graha.SUN

Avoid

if graha == "Sun"

---

# Dataclasses

Use dataclasses for immutable data.

Prefer

@dataclass(frozen=True)

unless mutation is required.

---

# Mutability

Prefer immutable models.

Pure functions are preferred.

Avoid modifying shared state.

---

# Function Size

Ideal

10–30 lines

Maximum

Approximately 75 lines

Large functions should be divided.

---

# Single Responsibility

Every module should have one responsibility.

Example

astronomy/signs.py

Only sign calculations.

Do not mix sign calculations with houses.

---

# Error Handling

Raise meaningful exceptions.

Good

raise ValueError(
    "Longitude must be between 0 and 360."
)

Avoid silent failures.

---

# Testing

Every new module requires tests.

Target coverage

90%+

Tests belong in

tests/

Examples

test_signs.py

test_nakshatra.py

test_ascendant.py

---

# Quality Checks

Before every commit

python -m compileall .

ruff check .

black . --check

isort . --check-only

pytest

All must pass.

---

# Git

Commit messages

Good

Add Ascendant calculations

Fix Julian day rounding

Refactor Nakshatra module

Avoid

update

changes

fix

---

# Dependencies

Allowed

Swiss Ephemeris

zoneinfo

pytest

Black

Ruff

isort

Avoid unnecessary external libraries.

---

# Performance

Correctness is more important than speed.

Optimize only after correctness is verified.

---

# BPHS Compliance

Whenever possible, document the classical source.

Example

"""
BPHS
Chapter 26
Verse 14
"""

Astronomical calculations may rely on Swiss Ephemeris.

Astrological interpretation should remain faithful to BPHS.

---

# Documentation

Every major module should contain

Purpose

Inputs

Outputs

Examples

Limitations

---

# Philosophy

Readable > Clever

Explicit > Implicit

Correctness > Performance

Maintainability > Shortness

Classical Accuracy > Modern Convenience

One source of truth.

One responsibility per module.

Every calculation should be testable.

Every interpretation should be traceable.

Build the engine as if it will be maintained for the next 20 years.