
"""
models/chart.py
Complete birth chart model for the Kundali Engine.
Stores calculated:
    - Birth data
    - Astronomical data
    - Ascendant and Midheaven
    - Planetary positions
    - Houses
    - Parashari planetary aspects (Drishti)
    - Planet-to-planet aspects
    - Planet-to-house aspects
    - Vimshottari Mahadasha
    - Vimshottari Antardasha
    - Vimshottari Pratyantardasha
    - Vimshottari Sookshma Dasha
    - Vimshottari Prana Dasha
    - Vimshottari Deha Dasha
    - Yogas
    - Divisional charts

Dasha hierarchy:

    Mahadasha
        ↓
    Antardasha
        ↓
    Pratyantardasha
        ↓
    Sookshma Dasha
        ↓
    Prana Dasha
        ↓
    Deha Dasha

Version:
    2.5.0

Compatible with:
    Python 3.9+
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from astrology.aspects import Aspect
from astrology.dasha import Antardasha, Mahadasha
from astrology.pratyantardasha import Pratyantardasha
from astrology.sookshmadasha import SookshmaDasha
from astrology.pranadasha import PranaDasha
from astrology.dehadasha import DehaDasha

from models.birth_data import BirthData
from models.house import House
from models.planet import Planet


@dataclass
class BirthChart:
    """
    Complete Vedic birth chart.

    BirthChart is the central data object returned by the
    HoroscopeEngine after astronomical and astrological
    calculations have been completed.

    The object intentionally stores calculated data rather
    than performing major calculations itself. This keeps
    the model clean and allows calculation modules to remain
    independently testable.

    Dasha hierarchy:

        Mahadasha
            ↓
        Antardasha
            ↓
        Pratyantardasha
            ↓
        Sookshma Dasha
            ↓
        Prana Dasha
            ↓
        Deha Dasha
    """

    # =========================================================
    # INPUT DATA
    # =========================================================

    birth_data: Optional[BirthData] = None

    # =========================================================
    # ASTRONOMICAL DATA
    # =========================================================

    julian_day: float = 0.0

    ayanamsa: float = 0.0

    # =========================================================
    # ASCENDANT
    # =========================================================

    ascendant: float = 0.0

    ascendant_sign: str = ""

    ascendant_degree: float = 0.0

    # =========================================================
    # MIDHEAVEN
    # =========================================================

    midheaven: float = 0.0

    # =========================================================
    # PLANETS
    # =========================================================

    planets: Dict[str, Planet] = field(
        default_factory=dict
    )

    # =========================================================
    # HOUSES
    # =========================================================

    houses: Dict[int, House] = field(
        default_factory=dict
    )

    # =========================================================
    # PARASHARI DRISHTI / PLANETARY ASPECTS
    # =========================================================

    aspect_map: Dict[str, List[Aspect]] = field(
        default_factory=dict
    )

    # =========================================================
    # PLANET-TO-PLANET ASPECTS
    # =========================================================

    planetary_aspects: Dict[str, List[str]] = field(
        default_factory=dict
    )

    # =========================================================
    # PLANET-TO-HOUSE ASPECTS
    # =========================================================

    house_aspects: Dict[int, List[str]] = field(
        default_factory=dict
    )

    # =========================================================
    # VIMSHOTTARI MAHADASHA
    # =========================================================

    mahadashas: List[Mahadasha] = field(
        default_factory=list
    )

    current_mahadasha: Optional[Mahadasha] = None

    # =========================================================
    # VIMSHOTTARI ANTARDASHA
    # =========================================================

    antardashas: List[Antardasha] = field(
        default_factory=list
    )

    current_antardasha: Optional[Antardasha] = None

    # =========================================================
    # VIMSHOTTARI PRATYANTARDASHA
    # =========================================================

    pratyantardashas: List[Pratyantardasha] = field(
        default_factory=list
    )

    current_pratyantardasha: Optional[
        Pratyantardasha
    ] = None

    # =========================================================
    # VIMSHOTTARI SOOKSHMA DASHA
    # =========================================================

    sookshmadashas: List[SookshmaDasha] = field(
        default_factory=list
    )

    current_sookshmadasha: Optional[
        SookshmaDasha
    ] = None

    # =========================================================
    # VIMSHOTTARI PRANA DASHA
    # =========================================================

    pranadashas: List[PranaDasha] = field(
        default_factory=list
    )

    current_pranadasha: Optional[
        PranaDasha
    ] = None

    # =========================================================
    # VIMSHOTTARI DEHA DASHA
    # =========================================================

    dehadashas: List[DehaDasha] = field(
        default_factory=list
    )

    current_dehadasha: Optional[
        DehaDasha
    ] = None

    # =========================================================
    # YOGAS
    # =========================================================

    yogas: list = field(
        default_factory=list
    )

    # =========================================================
    # LEGACY / EXTENDED DASHA STORAGE
    # =========================================================

    dashas: list = field(
        default_factory=list
    )

    # =========================================================
    # DIVISIONAL CHARTS / VARGAS
    # =========================================================

    divisional_charts: dict = field(
        default_factory=dict
    )

    # =========================================================
    # PLANET METHODS
    # =========================================================

    def add_planet(
        self,
        planet: Planet,
    ) -> None:
        """Add or replace a planet in the chart."""

        self.planets[planet.name] = planet

    def get_planet(
        self,
        name: str,
    ) -> Optional[Planet]:
        """Return a planet by name."""

        return self.planets.get(name)

    def has_planet(
        self,
        name: str,
    ) -> bool:
        """Check whether a planet exists in the chart."""

        return name in self.planets

    # =========================================================
    # HOUSE METHODS
    # =========================================================

    def add_house(
        self,
        house: House,
    ) -> None:
        """Add or replace a house in the chart."""

        self.houses[house.number] = house

    def get_house(
        self,
        number: int,
    ) -> Optional[House]:
        """Return a house by number."""

        return self.houses.get(number)

    def has_house(
        self,
        number: int,
    ) -> bool:
        """Check whether a house exists in the chart."""

        return number in self.houses

    # =========================================================
    # ASPECT METHODS
    # =========================================================

    def add_aspect(
        self,
        aspect: Aspect,
    ) -> None:
        """Add a planetary aspect to the aspect map."""

        if aspect.planet not in self.aspect_map:
            self.aspect_map[aspect.planet] = []

        self.aspect_map[aspect.planet].append(
            aspect
        )

    def get_aspects(
        self,
        planet: str,
    ) -> List[Aspect]:
        """Return all aspects cast by a planet."""

        return self.aspect_map.get(
            planet,
            [],
        )

    def add_planetary_aspect(
        self,
        aspecting_planet: str,
        target_planet: str,
    ) -> None:
        """Record a planet-to-planet aspect."""

        if (
            aspecting_planet
            not in self.planetary_aspects
        ):
            self.planetary_aspects[
                aspecting_planet
            ] = []

        if (
            target_planet
            not in self.planetary_aspects[
                aspecting_planet
            ]
        ):
            self.planetary_aspects[
                aspecting_planet
            ].append(
                target_planet
            )

    def get_planetary_aspects(
        self,
        planet: str,
    ) -> List[str]:
        """Return planets receiving an aspect."""

        return self.planetary_aspects.get(
            planet,
            [],
        )

    def add_house_aspect(
        self,
        house_number: int,
        planet: str,
    ) -> None:
        """Record that a planet aspects a house."""

        if house_number not in self.house_aspects:
            self.house_aspects[house_number] = []

        if (
            planet
            not in self.house_aspects[house_number]
        ):
            self.house_aspects[
                house_number
            ].append(
                planet
            )

    def get_house_aspects(
        self,
        house_number: int,
    ) -> List[str]:
        """Return planets aspecting a house."""

        return self.house_aspects.get(
            house_number,
            [],
        )

    # =========================================================
    # MAHADASHA METHODS
    # =========================================================

    def add_mahadasha(
        self,
        mahadasha: Mahadasha,
    ) -> None:
        """Add a Mahadasha period."""

        self.mahadashas.append(
            mahadasha
        )

    # =========================================================
    # ANTARDASHA METHODS
    # =========================================================

    def add_antardasha(
        self,
        antardasha: Antardasha,
    ) -> None:
        """Add an Antardasha period."""

        self.antardashas.append(
            antardasha
        )

    # =========================================================
    # PRATYANTARDASHA METHODS
    # =========================================================

    def add_pratyantardasha(
        self,
        pratyantardasha: Pratyantardasha,
    ) -> None:
        """Add a Pratyantardasha period."""

        self.pratyantardashas.append(
            pratyantardasha
        )

    # =========================================================
    # SOOKSHMA DASHA METHODS
    # =========================================================

    def add_sookshmadasha(
        self,
        sookshmadasha: SookshmaDasha,
    ) -> None:
        """Add a Sookshma Dasha period."""

        self.sookshmadashas.append(
            sookshmadasha
        )

    # =========================================================
    # PRANA DASHA METHODS
    # =========================================================

    def add_pranadasha(
        self,
        pranadasha: PranaDasha,
    ) -> None:
        """Add a Prana Dasha period."""

        self.pranadashas.append(
            pranadasha
        )

    # =========================================================
    # DEHA DASHA METHODS
    # =========================================================

    def add_dehadasha(
        self,
        dehadasha: DehaDasha,
    ) -> None:
        """Add a Deha Dasha period."""

        self.dehadashas.append(
            dehadasha
        )

    # =========================================================
    # YOGA METHODS
    # =========================================================

    def add_yoga(
        self,
        yoga,
    ) -> None:
        """Add a calculated Yoga result."""

        self.yogas.append(
            yoga
        )

    # =========================================================
    # DIVISIONAL CHART METHODS
    # =========================================================

    def add_divisional_chart(
        self,
        name: str,
        chart,
    ) -> None:
        """Store a divisional chart."""

        self.divisional_charts[name] = chart

    def get_divisional_chart(
        self,
        name: str,
    ):
        """Return a divisional chart."""

        return self.divisional_charts.get(
            name
        )

    # =========================================================
    # VALIDATION / STATUS
    # =========================================================

    def planet_count(self) -> int:
        """Return the number of planets."""

        return len(self.planets)

    def house_count(self) -> int:
        """Return the number of houses."""

        return len(self.houses)

    def is_complete(self) -> bool:
        """
        Perform a basic structural completeness check.

        This does not validate astronomical correctness.
        """

        return (
            len(self.planets) > 0
            and len(self.houses) == 12
            and self.ascendant != 0.0
        )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __str__(self) -> str:
        """Return a concise human-readable representation."""

        return (
            f"BirthChart("
            f"{len(self.planets)} planets, "
            f"{len(self.houses)} houses, "
            f"{len(self.aspect_map)} aspect sources, "
            f"{len(self.mahadashas)} Mahadashas, "
            f"{len(self.antardashas)} Antardashas, "
            f"{len(self.pratyantardashas)} "
            f"Pratyantardashas, "
            f"{len(self.sookshmadashas)} "
            f"Sookshma Dashas, "
            f"{len(self.pranadashas)} "
            f"Prana Dashas, "
            f"{len(self.dehadashas)} "
            f"Deha Dashas)"
        )
