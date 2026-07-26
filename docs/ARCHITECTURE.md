# Kundali Engine Architecture

Version: 2.2

---

# Vision

The Kundali Engine is a professional-grade, open-source Vedic astrology library built according to the principles of **Bṛhat Parāśara Horā Śāstra (BPHS)**.

Goals:

- Accurate astronomical calculations
- Classical BPHS implementation
- Clean, modular architecture
- Fully tested code
- Python 3.9 compatibility
- Extensible for research and future development

---

# High-Level Pipeline

Birth Data
↓
Timezone Resolution
↓
Julian Day
↓
Swiss Ephemeris
↓
Sidereal Longitude
↓
Signs
↓
Nakshatras
↓
Ascendant
↓
Whole Sign Houses
↓
Planet Positions
↓
Birth Chart (D1)
↓
Divisional Charts
↓
Strength Calculations
↓
Dasha Systems
↓
Yoga Detection
↓
Interpretation Engine

---

# Directory Structure

astronomy/
Astronomical calculations.

astrology/
Astrological algorithms.

models/
Domain models.

tests/
Unit tests.

docs/
Architecture and documentation.

---

# Module Responsibilities

astronomy/

constants.py
Universal astronomical constants.

julian.py
Julian day calculations.

timezone.py
Timezone handling.

swiss.py
Swiss Ephemeris wrapper.

signs.py
Zodiac calculations.

nakshatra.py
Nakshatra calculations.

ascendant.py
Ascendant calculations.

houses.py
House calculations.

---

astrology/

dasha/

yogas/

strength/

interpretation/

divisional/

---

models/

BirthData

Location

Graha

Planet

House

Chart

NakshatraInfo

SignInfo

ZodiacSign

---

# Design Principles

Single Responsibility Principle

Immutable data models

Strong typing

Pure functions whenever possible

Minimal side effects

High test coverage

Every module independently testable

---

# Coding Philosophy

Readable > Clever

Explicit > Implicit

Correctness > Performance

Maintainability > Shortness