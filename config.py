"""
Project configuration.
"""

from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent

# Swiss Ephemeris directory
EPHEMERIS_DIR = str(PROJECT_ROOT / "data" / "ephemeris")

# Default settings
DEFAULT_AYANAMSA = "Lahiri"

DEFAULT_NODE = "Mean"

DEFAULT_HOUSE_SYSTEM = "P"

DEFAULT_TIMEZONE = "UTC"
