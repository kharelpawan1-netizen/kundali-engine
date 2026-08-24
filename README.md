# 🪐 Kundali Analytics Platform (कुण्डली इन्जिन)

A high-precision, production-ready Vedic Astrology (Jyotish) Analytics Platform and calculation engine built with Python, FastAPI, Swiss Ephemeris, and Brihat Parashara Hora Shastra (BPHS) principles.

---

## 🌟 Core Features

### 1. High-Precision Astronomical Engine
- **Swiss Ephemeris Accuracy**: Real-time celestial mechanics, planetary longitude, latitude, distance, and daily velocity.
- **Ayanamsha Support**: Lahiri (Chitrapaksha), B.V. Raman, and KP (Krishnamurti) sidereal systems.
- **Lagna & Houses**: True Topocentric Ascendant (Lagna) and Whole-Sign Bhavas.
- **Nakshatra & Pada**: Exact 27 lunar mansions with Pada (1–4) and Nakshatra Lord mapping.
- **Combustion (Astangata)**: Exact classical proximity calculation from the Sun (Moon, Mars, Mercury, Jupiter, Venus, Saturn).
- **Retrograde & Motion**: Retrograde (`[R]`), Stationary, and Direct status with speed analytics.

### 2. Shodashavarga (All 16 Divisional Charts)
Computes all 16 BPHS divisional charts:
- **D1**: Rasi (Physical Existence & General Destiny)
- **D2**: Hora (Wealth & Assets)
- **D3**: Drekkana (Siblings & Courage)
- **D4**: Chaturthamsa (Net Fortune & Real Estate)
- **D7**: Saptamsa (Progeny & Children)
- **D9**: Navamsha (Spouse, Dharma & Root Soul Purpose)
- **D10**: Dasamsa (Career, Public Status & Leadership)
- **D12**: Dvadasamsa (Lineage & Ancestral Heritage)
- **D16**: Shodasamsa (Vehicles & General Comforts)
- **D20**: Vimsamsa (Spiritual Progress & Worship)
- **D24**: Chaturvimshamsa / Siddhamsa (Higher Learning & Knowledge)
- **D27**: Bhamsa / Saptavimsamsa (Inherent Strengths & Vulnerabilities)
- **D30**: Trimshamsa (Arishta & Overcoming Misfortunes)
- **D40**: Khavedamsa (Auspicious Matters)
- **D45**: Akshavedamsa (Character Purity)
- **D60**: Shastiamsa (Past Life Karma & Micro-Destiny)

### 3. Vimshottari Dasha Engine (120-Year Timeline)
- Full 6-level hierarchy:
  $$\text{Mahadasha} \rightarrow \text{Antardasha} \rightarrow \text{Pratyantardasha} \rightarrow \text{Sookshma} \rightarrow \text{Prana} \rightarrow \text{Deha}$$
- Real-time active dasha identification with start/end timestamps and remaining durations.

### 4. Classical Vedic Yogas Detection
- **Raja Yoga**: Kendra-Trikona lord associations and mutual aspect combinations.
- **Dhana Yoga**: 1st, 2nd, 5th, 9th, and 11th lord wealth combinations.
- **Gaja Kesari Yoga**: Auspicious Jupiter-Moon angular relationships.
- **Budha-Aditya Yoga**: Sun-Mercury intellect combinations.
- **Chandra-Mangala Yoga**: Moon-Mars wealth and commercial enterprise.
- **Guru Chandal Yoga**: Jupiter-Rahu conjunction analysis.
- **Neecha Bhanga Raja Yoga**: Classical cancellation of planetary debilitation.
- **Parivartana Yoga**: Mutual house lord exchange classifications (Maha, Khala, Dainya).

### 5. Advanced Astrological Analytics
- **Planetary Strengths (Balas)**: BPHS Cheshta Bala (motion), Dig Bala (direction), Naisargika Bala (natural), Natonnata Bala (diurnal), Paksha Bala (lunar phase), and Uccha Bala (exaltation).
- **Panchadha Maitri**: 7×7 interactive 5-fold compound relationship matrix (Great Friend, Friend, Neutral, Enemy, Bitter Enemy).
- **Shani Sade Sati**: Automated 7.5-year cycle calculation, Rising/Peak/Setting phases, and timeline projection.
- **Live Transits (Gochara)**: Real-time planetary transit overlay relative to natal Moon and Ascendant.

### 6. Interactive Web Dashboard (UI/UX)
- **Visual Chart Styles**: Dynamic vector rendering for both **North Indian (Diamond)** and **South Indian (Square)** formats.
- **Dual Themes**: Cosmic Dark Mode & Luminous Light Mode with persistent state.
- **77 Nepal Districts**: Pre-indexed database of all 77 districts of Nepal across 7 provinces with live search and coordinates.
- **Global City Search**: Fast offline database + online fallback geocoding with IANA timezone resolution.
- **Export & Print**: Publication-ready multi-page report formatting.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.9+
- Virtual environment (`venv`)

### 2. Installation
```powershell
git clone https://github.com/kharelpawan1-netizen/kundali-engine.git
cd kundali-engine
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Launch Dashboard
```powershell
python run_dashboard.py
```
The server will start at `http://127.0.0.1:8000` (with automatic port conflict fallback) and open the interactive dashboard in your browser.

---

## 📡 API Documentation

Access the interactive Swagger documentation at:
- **Swagger UI**: `http://127.0.0.1:8000/api/docs`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc`

### Key Endpoints
| Method | Route | Description |
|---|---|---|
| `POST` | `/api/chart` | Master horoscope calculation (Lagna, 9 Grahas, 16 Vargas, 6 Dashas, Yogas, Balas, Sade Sati) |
| `GET` | `/api/transits-current` | Real-time planetary positions and Gochara data |
| `GET` | `/api/cities?q={query}` | Search pre-indexed cities and global locations |
| `GET` | `/api/nepal-districts` | All 77 Nepal districts grouped by province |
| `POST` | `/api/geocode` | Geocode query with timezone resolution |
| `GET` | `/api/sample-profiles` | Pre-configured sample charts for instant testing |

---

## 🧪 Testing

Run the automated test suite with pytest:
```powershell
.venv\Scripts\pytest.exe
```
**Test Coverage**: 2,115 test cases passing across astronomical positions, vargas, dashas, yogas, dignity, and API endpoints.

---

## 📄 License
MIT License. Developed with pride by Pawan Kharel.
