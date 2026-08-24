"""
api/cities_db.py

Curated fast offline city & district database with coordinates and IANA timezones.
Includes every single one of the 77 districts of Nepal (all 7 provinces),
major towns and cities of Nepal, as well as major international cities.
"""

from __future__ import annotations

from typing import Dict, List, Optional


# ============================================================
# ALL 77 DISTRICTS OF NEPAL (7 PROVINCES)
# ============================================================

NEPAL_DISTRICTS_DATA: List[Dict[str, any]] = [
    # --- Koshi Province (14 Districts) ---
    {"name": "Bhojpur District, Nepal", "city": "Bhojpur", "district": "Bhojpur", "province": "Koshi", "country": "Nepal", "latitude": 27.1711, "longitude": 87.0458, "timezone": "Asia/Kathmandu", "elevation": 1540.0},
    {"name": "Dhankuta District, Nepal", "city": "Dhankuta", "district": "Dhankuta", "province": "Koshi", "country": "Nepal", "latitude": 26.9833, "longitude": 87.3333, "timezone": "Asia/Kathmandu", "elevation": 1200.0},
    {"name": "Ilam District, Nepal", "city": "Ilam", "district": "Ilam", "province": "Koshi", "country": "Nepal", "latitude": 26.9089, "longitude": 87.9264, "timezone": "Asia/Kathmandu", "elevation": 1208.0},
    {"name": "Jhapa District (Bhadrapur / Birtamod / Damak), Nepal", "city": "Jhapa", "district": "Jhapa", "province": "Koshi", "country": "Nepal", "latitude": 26.5455, "longitude": 88.0934, "timezone": "Asia/Kathmandu", "elevation": 90.0},
    {"name": "Khotang District (Diktel), Nepal", "city": "Khotang", "district": "Khotang", "province": "Koshi", "country": "Nepal", "latitude": 27.2144, "longitude": 86.7897, "timezone": "Asia/Kathmandu", "elevation": 1650.0},
    {"name": "Morang District (Biratnagar), Nepal", "city": "Morang", "district": "Morang", "province": "Koshi", "country": "Nepal", "latitude": 26.4525, "longitude": 87.2718, "timezone": "Asia/Kathmandu", "elevation": 80.0},
    {"name": "Okhaldhunga District, Nepal", "city": "Okhaldhunga", "district": "Okhaldhunga", "province": "Koshi", "country": "Nepal", "latitude": 27.3167, "longitude": 86.5000, "timezone": "Asia/Kathmandu", "elevation": 1561.0},
    {"name": "Panchthar District (Phidim), Nepal", "city": "Panchthar", "district": "Panchthar", "province": "Koshi", "country": "Nepal", "latitude": 27.1500, "longitude": 87.7667, "timezone": "Asia/Kathmandu", "elevation": 1180.0},
    {"name": "Sankhuwasabha District (Khandbari), Nepal", "city": "Sankhuwasabha", "district": "Sankhuwasabha", "province": "Koshi", "country": "Nepal", "latitude": 27.3750, "longitude": 87.2083, "timezone": "Asia/Kathmandu", "elevation": 1040.0},
    {"name": "Solukhumbu District (Salleri / Namche), Nepal", "city": "Solukhumbu", "district": "Solukhumbu", "province": "Koshi", "country": "Nepal", "latitude": 27.5000, "longitude": 86.5833, "timezone": "Asia/Kathmandu", "elevation": 2162.0},
    {"name": "Sunsari District (Dharan / Itahari / Inaruwa), Nepal", "city": "Sunsari", "district": "Sunsari", "province": "Koshi", "country": "Nepal", "latitude": 26.6000, "longitude": 87.1500, "timezone": "Asia/Kathmandu", "elevation": 116.0},
    {"name": "Taplejung District (Fungling), Nepal", "city": "Taplejung", "district": "Taplejung", "province": "Koshi", "country": "Nepal", "latitude": 27.3500, "longitude": 87.6667, "timezone": "Asia/Kathmandu", "elevation": 1820.0},
    {"name": "Terhathum District (Myanglung), Nepal", "city": "Terhathum", "district": "Terhathum", "province": "Koshi", "country": "Nepal", "latitude": 27.1333, "longitude": 87.5333, "timezone": "Asia/Kathmandu", "elevation": 1500.0},
    {"name": "Udayapur District (Gaighat), Nepal", "city": "Udayapur", "district": "Udayapur", "province": "Koshi", "country": "Nepal", "latitude": 26.7917, "longitude": 86.7000, "timezone": "Asia/Kathmandu", "elevation": 160.0},

    # --- Madhesh Province (8 Districts) ---
    {"name": "Saptari District (Rajbiraj), Nepal", "city": "Saptari", "district": "Saptari", "province": "Madhesh", "country": "Nepal", "latitude": 26.5422, "longitude": 86.7511, "timezone": "Asia/Kathmandu", "elevation": 75.0},
    {"name": "Siraha District (Lahan), Nepal", "city": "Siraha", "district": "Siraha", "province": "Madhesh", "country": "Nepal", "latitude": 26.6528, "longitude": 86.2089, "timezone": "Asia/Kathmandu", "elevation": 80.0},
    {"name": "Dhanusha District (Janakpur), Nepal", "city": "Dhanusha", "district": "Dhanusha", "province": "Madhesh", "country": "Nepal", "latitude": 26.7288, "longitude": 85.9244, "timezone": "Asia/Kathmandu", "elevation": 70.0},
    {"name": "Mahottari District (Jaleshwar / Bardibas), Nepal", "city": "Mahottari", "district": "Mahottari", "province": "Madhesh", "country": "Nepal", "latitude": 26.6436, "longitude": 85.8000, "timezone": "Asia/Kathmandu", "elevation": 60.0},
    {"name": "Sarlahi District (Malangwa / Lalbandi), Nepal", "city": "Sarlahi", "district": "Sarlahi", "province": "Madhesh", "country": "Nepal", "latitude": 26.8569, "longitude": 85.5581, "timezone": "Asia/Kathmandu", "elevation": 80.0},
    {"name": "Rautahat District (Gaur / Chandrapur), Nepal", "city": "Rautahat", "district": "Rautahat", "province": "Madhesh", "country": "Nepal", "latitude": 26.7644, "longitude": 85.2783, "timezone": "Asia/Kathmandu", "elevation": 75.0},
    {"name": "Bara District (Kalaiya / Simara), Nepal", "city": "Bara", "district": "Bara", "province": "Madhesh", "country": "Nepal", "latitude": 27.0306, "longitude": 85.0028, "timezone": "Asia/Kathmandu", "elevation": 85.0},
    {"name": "Parsa District (Birgunj), Nepal", "city": "Parsa", "district": "Parsa", "province": "Madhesh", "country": "Nepal", "latitude": 27.0134, "longitude": 84.8773, "timezone": "Asia/Kathmandu", "elevation": 80.0},

    # --- Bagmati Province (13 Districts) ---
    {"name": "Kathmandu District, Nepal", "city": "Kathmandu", "district": "Kathmandu", "province": "Bagmati", "country": "Nepal", "latitude": 27.7172, "longitude": 85.3240, "timezone": "Asia/Kathmandu", "elevation": 1400.0},
    {"name": "Lalitpur District (Patan), Nepal", "city": "Lalitpur", "district": "Lalitpur", "province": "Bagmati", "country": "Nepal", "latitude": 27.6667, "longitude": 85.3167, "timezone": "Asia/Kathmandu", "elevation": 1400.0},
    {"name": "Bhaktapur District, Nepal", "city": "Bhaktapur", "district": "Bhaktapur", "province": "Bagmati", "country": "Nepal", "latitude": 27.6710, "longitude": 85.4298, "timezone": "Asia/Kathmandu", "elevation": 1401.0},
    {"name": "Kavrepalanchok District (Dhulikhel / Banepa / Panauti), Nepal", "city": "Kavrepalanchok", "district": "Kavrepalanchok", "province": "Bagmati", "country": "Nepal", "latitude": 27.6167, "longitude": 85.5500, "timezone": "Asia/Kathmandu", "elevation": 1550.0},
    {"name": "Chitwan District (Bharatpur / Narayangarh / Ratnanagar), Nepal", "city": "Chitwan", "district": "Chitwan", "province": "Bagmati", "country": "Nepal", "latitude": 27.6833, "longitude": 84.4333, "timezone": "Asia/Kathmandu", "elevation": 208.0},
    {"name": "Makwanpur District (Hetauda), Nepal", "city": "Makwanpur", "district": "Makwanpur", "province": "Bagmati", "country": "Nepal", "latitude": 27.4287, "longitude": 85.0326, "timezone": "Asia/Kathmandu", "elevation": 345.0},
    {"name": "Dhading District (Dhading Besi / Malekhu), Nepal", "city": "Dhading", "district": "Dhading", "province": "Bagmati", "country": "Nepal", "latitude": 27.8667, "longitude": 84.9000, "timezone": "Asia/Kathmandu", "elevation": 600.0},
    {"name": "Nuwakot District (Bidur / Battar / Trishuli), Nepal", "city": "Nuwakot", "district": "Nuwakot", "province": "Bagmati", "country": "Nepal", "latitude": 27.9167, "longitude": 85.1667, "timezone": "Asia/Kathmandu", "elevation": 1000.0},
    {"name": "Rasuwa District (Dhunche / Syaphrubesi), Nepal", "city": "Rasuwa", "district": "Rasuwa", "province": "Bagmati", "country": "Nepal", "latitude": 28.1167, "longitude": 85.3000, "timezone": "Asia/Kathmandu", "elevation": 2030.0},
    {"name": "Sindhupalchok District (Chautara / Melamchi), Nepal", "city": "Sindhupalchok", "district": "Sindhupalchok", "province": "Bagmati", "country": "Nepal", "latitude": 27.7833, "longitude": 85.7167, "timezone": "Asia/Kathmandu", "elevation": 1450.0},
    {"name": "Dolakha District (Charikot / Jiri), Nepal", "city": "Dolakha", "district": "Dolakha", "province": "Bagmati", "country": "Nepal", "latitude": 27.6667, "longitude": 86.0333, "timezone": "Asia/Kathmandu", "elevation": 1970.0},
    {"name": "Ramechhap District (Manthali), Nepal", "city": "Ramechhap", "district": "Ramechhap", "province": "Bagmati", "country": "Nepal", "latitude": 27.4000, "longitude": 86.0667, "timezone": "Asia/Kathmandu", "elevation": 474.0},
    {"name": "Sindhuli District (Sindhulimadi / Kamalamai), Nepal", "city": "Sindhuli", "district": "Sindhuli", "province": "Bagmati", "country": "Nepal", "latitude": 27.2500, "longitude": 85.9667, "timezone": "Asia/Kathmandu", "elevation": 462.0},

    # --- Gandaki Province (11 Districts) ---
    {"name": "Kaski District (Pokhara / Lekhnath), Nepal", "city": "Kaski", "district": "Kaski", "province": "Gandaki", "country": "Nepal", "latitude": 28.2096, "longitude": 83.9856, "timezone": "Asia/Kathmandu", "elevation": 822.0},
    {"name": "Gorkha District, Nepal", "city": "Gorkha", "district": "Gorkha", "province": "Gandaki", "country": "Nepal", "latitude": 28.0000, "longitude": 84.6333, "timezone": "Asia/Kathmandu", "elevation": 1143.0},
    {"name": "Lamjung District (Besisahar), Nepal", "city": "Lamjung", "district": "Lamjung", "province": "Gandaki", "country": "Nepal", "latitude": 28.2333, "longitude": 84.4167, "timezone": "Asia/Kathmandu", "elevation": 760.0},
    {"name": "Tanahun District (Damauli / Byas / Bandipur), Nepal", "city": "Tanahun", "district": "Tanahun", "province": "Gandaki", "country": "Nepal", "latitude": 27.9667, "longitude": 84.2833, "timezone": "Asia/Kathmandu", "elevation": 400.0},
    {"name": "Syangja District (Putalibazar / Waling), Nepal", "city": "Syangja", "district": "Syangja", "province": "Gandaki", "country": "Nepal", "latitude": 28.1000, "longitude": 83.8667, "timezone": "Asia/Kathmandu", "elevation": 850.0},
    {"name": "Parbat District (Kusma), Nepal", "city": "Parbat", "district": "Parbat", "province": "Gandaki", "country": "Nepal", "latitude": 28.2167, "longitude": 83.6833, "timezone": "Asia/Kathmandu", "elevation": 850.0},
    {"name": "Baglung District, Nepal", "city": "Baglung", "district": "Baglung", "province": "Gandaki", "country": "Nepal", "latitude": 28.2667, "longitude": 83.6000, "timezone": "Asia/Kathmandu", "elevation": 1020.0},
    {"name": "Myagdi District (Beni), Nepal", "city": "Myagdi", "district": "Myagdi", "province": "Gandaki", "country": "Nepal", "latitude": 28.3500, "longitude": 83.5667, "timezone": "Asia/Kathmandu", "elevation": 830.0},
    {"name": "Mustang District (Jomsom / Muktinath), Nepal", "city": "Mustang", "district": "Mustang", "province": "Gandaki", "country": "Nepal", "latitude": 28.7833, "longitude": 83.7333, "timezone": "Asia/Kathmandu", "elevation": 2743.0},
    {"name": "Manang District (Chame), Nepal", "city": "Manang", "district": "Manang", "province": "Gandaki", "country": "Nepal", "latitude": 28.5500, "longitude": 84.2333, "timezone": "Asia/Kathmandu", "elevation": 2670.0},
    {"name": "Nawalpur District (Nawalparasi East / Kawasoti / Gaindakot), Nepal", "city": "Nawalpur", "district": "Nawalpur", "province": "Gandaki", "country": "Nepal", "latitude": 27.6500, "longitude": 84.1333, "timezone": "Asia/Kathmandu", "elevation": 170.0},

    # --- Lumbini Province (12 Districts) ---
    {"name": "Rupandehi District (Bhairahawa / Butwal / Lumbini / Tilottama), Nepal", "city": "Rupandehi", "district": "Rupandehi", "province": "Lumbini", "country": "Nepal", "latitude": 27.5000, "longitude": 83.4500, "timezone": "Asia/Kathmandu", "elevation": 105.0},
    {"name": "Kapilvastu District (Taulihawa / Krishnanagar), Nepal", "city": "Kapilvastu", "district": "Kapilvastu", "province": "Lumbini", "country": "Nepal", "latitude": 27.5500, "longitude": 83.0500, "timezone": "Asia/Kathmandu", "elevation": 100.0},
    {"name": "Parasi District (Nawalparasi West / Ramgram / Sunwal), Nepal", "city": "Parasi", "district": "Parasi", "province": "Lumbini", "country": "Nepal", "latitude": 27.5333, "longitude": 83.6667, "timezone": "Asia/Kathmandu", "elevation": 105.0},
    {"name": "Palpa District (Tansen / Rampur), Nepal", "city": "Palpa", "district": "Palpa", "province": "Lumbini", "country": "Nepal", "latitude": 27.8667, "longitude": 83.5500, "timezone": "Asia/Kathmandu", "elevation": 1350.0},
    {"name": "Arghakhanchi District (Sandhikharka), Nepal", "city": "Arghakhanchi", "district": "Arghakhanchi", "province": "Lumbini", "country": "Nepal", "latitude": 27.9833, "longitude": 83.1333, "timezone": "Asia/Kathmandu", "elevation": 1300.0},
    {"name": "Gulmi District (Tamghas / Resunga), Nepal", "city": "Gulmi", "district": "Gulmi", "province": "Lumbini", "country": "Nepal", "latitude": 28.0667, "longitude": 83.2500, "timezone": "Asia/Kathmandu", "elevation": 1500.0},
    {"name": "Dang District (Ghorahi / Tulsipur / Lamahi), Nepal", "city": "Dang", "district": "Dang", "province": "Lumbini", "country": "Nepal", "latitude": 28.0500, "longitude": 82.5000, "timezone": "Asia/Kathmandu", "elevation": 600.0},
    {"name": "Pyuthan District (Pyuthan Khalanga / Bijuwar), Nepal", "city": "Pyuthan", "district": "Pyuthan", "province": "Lumbini", "country": "Nepal", "latitude": 28.1000, "longitude": 82.8833, "timezone": "Asia/Kathmandu", "elevation": 1350.0},
    {"name": "Rolpa District (Liwang), Nepal", "city": "Rolpa", "district": "Rolpa", "province": "Lumbini", "country": "Nepal", "latitude": 28.3000, "longitude": 82.6333, "timezone": "Asia/Kathmandu", "elevation": 1375.0},
    {"name": "Rukum East District (Rukumkot), Nepal", "city": "Rukum East", "district": "Rukum East", "province": "Lumbini", "country": "Nepal", "latitude": 28.6000, "longitude": 82.6333, "timezone": "Asia/Kathmandu", "elevation": 1560.0},
    {"name": "Banke District (Nepalgunj / Kohalpur), Nepal", "city": "Banke", "district": "Banke", "province": "Lumbini", "country": "Nepal", "latitude": 28.0500, "longitude": 81.6167, "timezone": "Asia/Kathmandu", "elevation": 150.0},
    {"name": "Bardiya District (Gulariya / Rajapur), Nepal", "city": "Bardiya", "district": "Bardiya", "province": "Lumbini", "country": "Nepal", "latitude": 28.2333, "longitude": 81.3333, "timezone": "Asia/Kathmandu", "elevation": 140.0},

    # --- Karnali Province (10 Districts) ---
    {"name": "Surkhet District (Birendranagar), Nepal", "city": "Surkhet", "district": "Surkhet", "province": "Karnali", "country": "Nepal", "latitude": 28.6000, "longitude": 81.6333, "timezone": "Asia/Kathmandu", "elevation": 720.0},
    {"name": "Dailekh District (Narayan / Dullu), Nepal", "city": "Dailekh", "district": "Dailekh", "province": "Karnali", "country": "Nepal", "latitude": 28.8333, "longitude": 81.7167, "timezone": "Asia/Kathmandu", "elevation": 1400.0},
    {"name": "Jajarkot District (Khalanga), Nepal", "city": "Jajarkot", "district": "Jajarkot", "province": "Karnali", "country": "Nepal", "latitude": 28.7000, "longitude": 82.2000, "timezone": "Asia/Kathmandu", "elevation": 1225.0},
    {"name": "Salyan District (Salyan Khalanga / Luham), Nepal", "city": "Salyan", "district": "Salyan", "province": "Karnali", "country": "Nepal", "latitude": 28.3667, "longitude": 82.1667, "timezone": "Asia/Kathmandu", "elevation": 1500.0},
    {"name": "Rukum West District (Musikot / Chaurjahari), Nepal", "city": "Rukum West", "district": "Rukum West", "province": "Karnali", "country": "Nepal", "latitude": 28.6333, "longitude": 82.4833, "timezone": "Asia/Kathmandu", "elevation": 1450.0},
    {"name": "Kalikot District (Manma), Nepal", "city": "Kalikot", "district": "Kalikot", "province": "Karnali", "country": "Nepal", "latitude": 29.1333, "longitude": 81.6167, "timezone": "Asia/Kathmandu", "elevation": 1440.0},
    {"name": "Jumla District (Chandannath / Khalanga), Nepal", "city": "Jumla", "district": "Jumla", "province": "Karnali", "country": "Nepal", "latitude": 29.2744, "longitude": 82.1839, "timezone": "Asia/Kathmandu", "elevation": 2514.0},
    {"name": "Mugu District (Gamgadhi / Rara), Nepal", "city": "Mugu", "district": "Mugu", "province": "Karnali", "country": "Nepal", "latitude": 29.5500, "longitude": 82.1667, "timezone": "Asia/Kathmandu", "elevation": 2300.0},
    {"name": "Humla District (Simikot), Nepal", "city": "Humla", "district": "Humla", "province": "Karnali", "country": "Nepal", "latitude": 29.9667, "longitude": 81.8333, "timezone": "Asia/Kathmandu", "elevation": 2946.0},
    {"name": "Dolpa District (Dunai), Nepal", "city": "Dolpa", "district": "Dolpa", "province": "Karnali", "country": "Nepal", "latitude": 28.9333, "longitude": 82.9000, "timezone": "Asia/Kathmandu", "elevation": 2140.0},

    # --- Sudurpashchim Province (9 Districts) ---
    {"name": "Kailali District (Dhangadhi / Tikapur / Attariya), Nepal", "city": "Kailali", "district": "Kailali", "province": "Sudurpashchim", "country": "Nepal", "latitude": 28.6853, "longitude": 80.5960, "timezone": "Asia/Kathmandu", "elevation": 109.0},
    {"name": "Kanchanpur District (Bhimdatta / Mahendranagar), Nepal", "city": "Kanchanpur", "district": "Kanchanpur", "province": "Sudurpashchim", "country": "Nepal", "latitude": 28.9667, "longitude": 80.1833, "timezone": "Asia/Kathmandu", "elevation": 198.0},
    {"name": "Dadeldhura District (Amargadhi), Nepal", "city": "Dadeldhura", "district": "Dadeldhura", "province": "Sudurpashchim", "country": "Nepal", "latitude": 29.3000, "longitude": 80.5833, "timezone": "Asia/Kathmandu", "elevation": 1745.0},
    {"name": "Baitadi District (Dasharathchand / Patan), Nepal", "city": "Baitadi", "district": "Baitadi", "province": "Sudurpashchim", "country": "Nepal", "latitude": 29.5333, "longitude": 80.4667, "timezone": "Asia/Kathmandu", "elevation": 1600.0},
    {"name": "Darchula District (Khalanga), Nepal", "city": "Darchula", "district": "Darchula", "province": "Sudurpashchim", "country": "Nepal", "latitude": 29.8500, "longitude": 80.5333, "timezone": "Asia/Kathmandu", "elevation": 950.0},
    {"name": "Doti District (Dipayal Silgadhi), Nepal", "city": "Doti", "district": "Doti", "province": "Sudurpashchim", "country": "Nepal", "latitude": 29.2667, "longitude": 80.9333, "timezone": "Asia/Kathmandu", "elevation": 570.0},
    {"name": "Achham District (Mangalsen / Sanfebagar), Nepal", "city": "Achham", "district": "Achham", "province": "Sudurpashchim", "country": "Nepal", "latitude": 29.1333, "longitude": 81.2667, "timezone": "Asia/Kathmandu", "elevation": 1350.0},
    {"name": "Bajhang District (Jayaprithvi / Chainpur), Nepal", "city": "Bajhang", "district": "Bajhang", "province": "Sudurpashchim", "country": "Nepal", "latitude": 29.5333, "longitude": 81.2000, "timezone": "Asia/Kathmandu", "elevation": 1300.0},
    {"name": "Bajura District (Martadi), Nepal", "city": "Bajura", "district": "Bajura", "province": "Sudurpashchim", "country": "Nepal", "latitude": 29.4500, "longitude": 81.4833, "timezone": "Asia/Kathmandu", "elevation": 1580.0},
]


# ============================================================
# MAJOR NEPAL CITIES (INDIVIDUAL POPULAR SEARCHES)
# ============================================================

NEPAL_MAJOR_CITIES: List[Dict[str, any]] = [
    {"name": "Kathmandu, Nepal", "city": "Kathmandu", "district": "Kathmandu", "province": "Bagmati", "country": "Nepal", "latitude": 27.7172, "longitude": 85.3240, "timezone": "Asia/Kathmandu", "elevation": 1400.0},
    {"name": "Pokhara, Nepal", "city": "Pokhara", "district": "Kaski", "province": "Gandaki", "country": "Nepal", "latitude": 28.2096, "longitude": 83.9856, "timezone": "Asia/Kathmandu", "elevation": 822.0},
    {"name": "Lalitpur (Patan), Nepal", "city": "Lalitpur", "district": "Lalitpur", "province": "Bagmati", "country": "Nepal", "latitude": 27.6667, "longitude": 85.3167, "timezone": "Asia/Kathmandu", "elevation": 1400.0},
    {"name": "Bhaktapur, Nepal", "city": "Bhaktapur", "district": "Bhaktapur", "province": "Bagmati", "country": "Nepal", "latitude": 27.6710, "longitude": 85.4298, "timezone": "Asia/Kathmandu", "elevation": 1401.0},
    {"name": "Biratnagar, Nepal", "city": "Biratnagar", "district": "Morang", "province": "Koshi", "country": "Nepal", "latitude": 26.4525, "longitude": 87.2718, "timezone": "Asia/Kathmandu", "elevation": 80.0},
    {"name": "Birgunj, Nepal", "city": "Birgunj", "district": "Parsa", "province": "Madhesh", "country": "Nepal", "latitude": 27.0134, "longitude": 84.8773, "timezone": "Asia/Kathmandu", "elevation": 80.0},
    {"name": "Bharatpur (Chitwan), Nepal", "city": "Bharatpur", "district": "Chitwan", "province": "Bagmati", "country": "Nepal", "latitude": 27.6833, "longitude": 84.4333, "timezone": "Asia/Kathmandu", "elevation": 208.0},
    {"name": "Narayangarh, Nepal", "city": "Narayangarh", "district": "Chitwan", "province": "Bagmati", "country": "Nepal", "latitude": 27.6939, "longitude": 84.4239, "timezone": "Asia/Kathmandu", "elevation": 210.0},
    {"name": "Butwal, Nepal", "city": "Butwal", "district": "Rupandehi", "province": "Lumbini", "country": "Nepal", "latitude": 27.7000, "longitude": 83.4500, "timezone": "Asia/Kathmandu", "elevation": 150.0},
    {"name": "Bhairahawa (Siddharthanagar), Nepal", "city": "Bhairahawa", "district": "Rupandehi", "province": "Lumbini", "country": "Nepal", "latitude": 27.5000, "longitude": 83.4500, "timezone": "Asia/Kathmandu", "elevation": 105.0},
    {"name": "Dharan, Nepal", "city": "Dharan", "district": "Sunsari", "province": "Koshi", "country": "Nepal", "latitude": 26.8124, "longitude": 87.2834, "timezone": "Asia/Kathmandu", "elevation": 349.0},
    {"name": "Itahari, Nepal", "city": "Itahari", "district": "Sunsari", "province": "Koshi", "country": "Nepal", "latitude": 26.6667, "longitude": 87.2833, "timezone": "Asia/Kathmandu", "elevation": 116.0},
    {"name": "Nepalgunj, Nepal", "city": "Nepalgunj", "district": "Banke", "province": "Lumbini", "country": "Nepal", "latitude": 28.0500, "longitude": 81.6167, "timezone": "Asia/Kathmandu", "elevation": 150.0},
    {"name": "Dhangadhi, Nepal", "city": "Dhangadhi", "district": "Kailali", "province": "Sudurpashchim", "country": "Nepal", "latitude": 28.6853, "longitude": 80.5960, "timezone": "Asia/Kathmandu", "elevation": 109.0},
    {"name": "Hetauda, Nepal", "city": "Hetauda", "district": "Makwanpur", "province": "Bagmati", "country": "Nepal", "latitude": 27.4287, "longitude": 85.0326, "timezone": "Asia/Kathmandu", "elevation": 345.0},
    {"name": "Janakpur, Nepal", "city": "Janakpur", "district": "Dhanusha", "province": "Madhesh", "country": "Nepal", "latitude": 26.7288, "longitude": 85.9244, "timezone": "Asia/Kathmandu", "elevation": 70.0},
    {"name": "Birtamod, Nepal", "city": "Birtamod", "district": "Jhapa", "province": "Koshi", "country": "Nepal", "latitude": 26.6333, "longitude": 87.9833, "timezone": "Asia/Kathmandu", "elevation": 120.0},
    {"name": "Damak, Nepal", "city": "Damak", "district": "Jhapa", "province": "Koshi", "country": "Nepal", "latitude": 26.6667, "longitude": 87.7000, "timezone": "Asia/Kathmandu", "elevation": 115.0},
    {"name": "Tansen (Palpa), Nepal", "city": "Tansen", "district": "Palpa", "province": "Lumbini", "country": "Nepal", "latitude": 27.8667, "longitude": 83.5500, "timezone": "Asia/Kathmandu", "elevation": 1350.0},
    {"name": "Banepa, Nepal", "city": "Banepa", "district": "Kavrepalanchok", "province": "Bagmati", "country": "Nepal", "latitude": 27.6333, "longitude": 85.5167, "timezone": "Asia/Kathmandu", "elevation": 1460.0},
    {"name": "Dhulikhel, Nepal", "city": "Dhulikhel", "district": "Kavrepalanchok", "province": "Bagmati", "country": "Nepal", "latitude": 27.6167, "longitude": 85.5500, "timezone": "Asia/Kathmandu", "elevation": 1550.0},
    {"name": "Ghorahi (Dang), Nepal", "city": "Ghorahi", "district": "Dang", "province": "Lumbini", "country": "Nepal", "latitude": 28.0500, "longitude": 82.5000, "timezone": "Asia/Kathmandu", "elevation": 600.0},
    {"name": "Tulsipur (Dang), Nepal", "city": "Tulsipur", "district": "Dang", "province": "Lumbini", "country": "Nepal", "latitude": 28.1333, "longitude": 82.3000, "timezone": "Asia/Kathmandu", "elevation": 725.0},
    {"name": "Birendranagar (Surkhet), Nepal", "city": "Birendranagar", "district": "Surkhet", "province": "Karnali", "country": "Nepal", "latitude": 28.6000, "longitude": 81.6333, "timezone": "Asia/Kathmandu", "elevation": 720.0},
    {"name": "Mahendranagar (Bhimdatta), Nepal", "city": "Mahendranagar", "district": "Kanchanpur", "province": "Sudurpashchim", "country": "Nepal", "latitude": 28.9667, "longitude": 80.1833, "timezone": "Asia/Kathmandu", "elevation": 198.0},
    {"name": "Lahan, Nepal", "city": "Lahan", "district": "Siraha", "province": "Madhesh", "country": "Nepal", "latitude": 26.7297, "longitude": 86.4831, "timezone": "Asia/Kathmandu", "elevation": 88.0},
    {"name": "Rajbiraj, Nepal", "city": "Rajbiraj", "district": "Saptari", "province": "Madhesh", "country": "Nepal", "latitude": 26.5422, "longitude": 86.7511, "timezone": "Asia/Kathmandu", "elevation": 75.0},
    {"name": "Lumbini Sanskritik, Nepal", "city": "Lumbini", "district": "Rupandehi", "province": "Lumbini", "country": "Nepal", "latitude": 27.4833, "longitude": 83.2833, "timezone": "Asia/Kathmandu", "elevation": 98.0},
    {"name": "Panauti, Nepal", "city": "Panauti", "district": "Kavrepalanchok", "province": "Bagmati", "country": "Nepal", "latitude": 27.5833, "longitude": 85.5167, "timezone": "Asia/Kathmandu", "elevation": 1450.0},
    {"name": "Khandbari, Nepal", "city": "Khandbari", "district": "Sankhuwasabha", "province": "Koshi", "country": "Nepal", "latitude": 27.3750, "longitude": 87.2083, "timezone": "Asia/Kathmandu", "elevation": 1040.0},
]


# ============================================================
# INTERNATIONAL CITIES (INDIA, USA, UK, EUROPE, ASIA, ETC.)
# ============================================================

INTERNATIONAL_CITIES: List[Dict[str, any]] = [
    # --- India ---
    {"name": "New Delhi, India", "city": "New Delhi", "country": "India", "latitude": 28.6139, "longitude": 77.2090, "timezone": "Asia/Kolkata", "elevation": 216.0},
    {"name": "Mumbai, India", "city": "Mumbai", "country": "India", "latitude": 19.0760, "longitude": 72.8777, "timezone": "Asia/Kolkata", "elevation": 14.0},
    {"name": "Bangalore (Bengaluru), India", "city": "Bangalore", "country": "India", "latitude": 12.9716, "longitude": 77.5946, "timezone": "Asia/Kolkata", "elevation": 920.0},
    {"name": "Kolkata, India", "city": "Kolkata", "country": "India", "latitude": 22.5726, "longitude": 88.3639, "timezone": "Asia/Kolkata", "elevation": 9.0},
    {"name": "Chennai, India", "city": "Chennai", "country": "India", "latitude": 13.0827, "longitude": 80.2707, "timezone": "Asia/Kolkata", "elevation": 6.0},
    {"name": "Hyderabad, India", "city": "Hyderabad", "country": "India", "latitude": 17.3850, "longitude": 78.4867, "timezone": "Asia/Kolkata", "elevation": 542.0},
    {"name": "Ahmedabad, India", "city": "Ahmedabad", "country": "India", "latitude": 23.0225, "longitude": 72.5714, "timezone": "Asia/Kolkata", "elevation": 53.0},
    {"name": "Pune, India", "city": "Pune", "country": "India", "latitude": 18.5204, "longitude": 73.8567, "timezone": "Asia/Kolkata", "elevation": 560.0},
    {"name": "Jaipur, India", "city": "Jaipur", "country": "India", "latitude": 26.9124, "longitude": 75.7873, "timezone": "Asia/Kolkata", "elevation": 431.0},
    {"name": "Varanasi (Kashi), India", "city": "Varanasi", "country": "India", "latitude": 25.3176, "longitude": 82.9739, "timezone": "Asia/Kolkata", "elevation": 81.0},
    {"name": "Vrindavan, India", "city": "Vrindavan", "country": "India", "latitude": 27.5806, "longitude": 77.7006, "timezone": "Asia/Kolkata", "elevation": 170.0},
    {"name": "Haridwar, India", "city": "Haridwar", "country": "India", "latitude": 29.9457, "longitude": 78.1642, "timezone": "Asia/Kolkata", "elevation": 314.0},
    {"name": "Rishikesh, India", "city": "Rishikesh", "country": "India", "latitude": 30.0869, "longitude": 78.2676, "timezone": "Asia/Kolkata", "elevation": 372.0},
    {"name": "Ujjain, India", "city": "Ujjain", "country": "India", "latitude": 23.1765, "longitude": 75.7885, "timezone": "Asia/Kolkata", "elevation": 491.0},
    {"name": "Ayodhya, India", "city": "Ayodhya", "country": "India", "latitude": 26.7922, "longitude": 82.1998, "timezone": "Asia/Kolkata", "elevation": 102.0},
    {"name": "Lucknow, India", "city": "Lucknow", "country": "India", "latitude": 26.8467, "longitude": 80.9462, "timezone": "Asia/Kolkata", "elevation": 123.0},
    {"name": "Patna, India", "city": "Patna", "country": "India", "latitude": 25.5941, "longitude": 85.1376, "timezone": "Asia/Kolkata", "elevation": 53.0},
    {"name": "Chandigarh, India", "city": "Chandigarh", "country": "India", "latitude": 30.7333, "longitude": 76.7794, "timezone": "Asia/Kolkata", "elevation": 321.0},
    {"name": "Guwahati, India", "city": "Guwahati", "country": "India", "latitude": 26.1445, "longitude": 91.7362, "timezone": "Asia/Kolkata", "elevation": 55.0},
    {"name": "Indore, India", "city": "Indore", "country": "India", "latitude": 22.7196, "longitude": 75.8577, "timezone": "Asia/Kolkata", "elevation": 553.0},
    {"name": "Bhopal, India", "city": "Bhopal", "country": "India", "latitude": 23.2599, "longitude": 77.4126, "timezone": "Asia/Kolkata", "elevation": 527.0},
    {"name": "Kochi (Cochin), India", "city": "Kochi", "country": "India", "latitude": 9.9312, "longitude": 76.2673, "timezone": "Asia/Kolkata", "elevation": 5.0},
    {"name": "Thiruvananthapuram, India", "city": "Thiruvananthapuram", "country": "India", "latitude": 8.5241, "longitude": 76.9366, "timezone": "Asia/Kolkata", "elevation": 10.0},
    {"name": "Coimbatore, India", "city": "Coimbatore", "country": "India", "latitude": 11.0168, "longitude": 76.9558, "timezone": "Asia/Kolkata", "elevation": 411.0},
    {"name": "Nagpur, India", "city": "Nagpur", "country": "India", "latitude": 21.1458, "longitude": 79.0882, "timezone": "Asia/Kolkata", "elevation": 310.0},
    {"name": "Surat, India", "city": "Surat", "country": "India", "latitude": 21.1702, "longitude": 72.8311, "timezone": "Asia/Kolkata", "elevation": 13.0},
    {"name": "Vadodara, India", "city": "Vadodara", "country": "India", "latitude": 22.3072, "longitude": 73.1812, "timezone": "Asia/Kolkata", "elevation": 39.0},
    {"name": "Dehradun, India", "city": "Dehradun", "country": "India", "latitude": 30.3165, "longitude": 78.0322, "timezone": "Asia/Kolkata", "elevation": 640.0},
    {"name": "Amritsar, India", "city": "Amritsar", "country": "India", "latitude": 31.6340, "longitude": 74.8723, "timezone": "Asia/Kolkata", "elevation": 234.0},

    # --- USA ---
    {"name": "New York, USA", "city": "New York", "country": "USA", "latitude": 40.7128, "longitude": -74.0060, "timezone": "America/New_York", "elevation": 10.0},
    {"name": "Los Angeles, USA", "city": "Los Angeles", "country": "USA", "latitude": 34.0522, "longitude": -118.2437, "timezone": "America/Los_Angeles", "elevation": 89.0},
    {"name": "San Francisco / Bay Area, USA", "city": "San Francisco", "country": "USA", "latitude": 37.7749, "longitude": -122.4194, "timezone": "America/Los_Angeles", "elevation": 16.0},
    {"name": "San Jose (Silicon Valley), USA", "city": "San Jose", "country": "USA", "latitude": 37.3382, "longitude": -121.8863, "timezone": "America/Los_Angeles", "elevation": 25.0},
    {"name": "Seattle, USA", "city": "Seattle", "country": "USA", "latitude": 47.6062, "longitude": -122.3321, "timezone": "America/Los_Angeles", "elevation": 53.0},
    {"name": "Chicago, USA", "city": "Chicago", "country": "USA", "latitude": 41.8781, "longitude": -87.6298, "timezone": "America/Chicago", "elevation": 182.0},
    {"name": "Houston, USA", "city": "Houston", "country": "USA", "latitude": 29.7604, "longitude": -95.3698, "timezone": "America/Chicago", "elevation": 15.0},
    {"name": "Dallas, USA", "city": "Dallas", "country": "USA", "latitude": 32.7767, "longitude": -96.7970, "timezone": "America/Chicago", "elevation": 131.0},
    {"name": "Austin, USA", "city": "Austin", "country": "USA", "latitude": 30.2672, "longitude": -97.7431, "timezone": "America/Chicago", "elevation": 149.0},
    {"name": "Boston, USA", "city": "Boston", "country": "USA", "latitude": 42.3601, "longitude": -71.0589, "timezone": "America/New_York", "elevation": 43.0},
    {"name": "Washington DC, USA", "city": "Washington", "country": "USA", "latitude": 38.9072, "longitude": -77.0369, "timezone": "America/New_York", "elevation": 22.0},
    {"name": "Miami, USA", "city": "Miami", "country": "USA", "latitude": 25.7617, "longitude": -80.1918, "timezone": "America/New_York", "elevation": 2.0},
    {"name": "Atlanta, USA", "city": "Atlanta", "country": "USA", "latitude": 33.7490, "longitude": -84.3880, "timezone": "America/New_York", "elevation": 320.0},
    {"name": "Denver, USA", "city": "Denver", "country": "USA", "latitude": 39.7392, "longitude": -104.9903, "timezone": "America/Denver", "elevation": 1609.0},
    {"name": "Phoenix, USA", "city": "Phoenix", "country": "USA", "latitude": 33.4484, "longitude": -112.0740, "timezone": "America/Phoenix", "elevation": 331.0},

    # --- UK & Europe ---
    {"name": "London, United Kingdom", "city": "London", "country": "United Kingdom", "latitude": 51.5074, "longitude": -0.1278, "timezone": "Europe/London", "elevation": 25.0},
    {"name": "Manchester, United Kingdom", "city": "Manchester", "country": "United Kingdom", "latitude": 53.4808, "longitude": -2.2426, "timezone": "Europe/London", "elevation": 38.0},
    {"name": "Birmingham, United Kingdom", "city": "Birmingham", "country": "United Kingdom", "latitude": 52.4862, "longitude": -1.8904, "timezone": "Europe/London", "elevation": 140.0},
    {"name": "Edinburgh, United Kingdom", "city": "Edinburgh", "country": "United Kingdom", "latitude": 55.9533, "longitude": -3.1883, "timezone": "Europe/London", "elevation": 47.0},
    {"name": "Paris, France", "city": "Paris", "country": "France", "latitude": 48.8566, "longitude": 2.3522, "timezone": "Europe/Paris", "elevation": 35.0},
    {"name": "Berlin, Germany", "city": "Berlin", "country": "Germany", "latitude": 52.5200, "longitude": 13.4050, "timezone": "Europe/Berlin", "elevation": 34.0},
    {"name": "Frankfurt, Germany", "city": "Frankfurt", "country": "Germany", "latitude": 50.1109, "longitude": 8.6821, "timezone": "Europe/Berlin", "elevation": 112.0},
    {"name": "Munich, Germany", "city": "Munich", "country": "Germany", "latitude": 48.1351, "longitude": 11.5820, "timezone": "Europe/Berlin", "elevation": 519.0},
    {"name": "Amsterdam, Netherlands", "city": "Amsterdam", "country": "Netherlands", "latitude": 52.3676, "longitude": 4.9041, "timezone": "Europe/Amsterdam", "elevation": 2.0},
    {"name": "Zurich, Switzerland", "city": "Zurich", "country": "Switzerland", "latitude": 47.3769, "longitude": 8.5417, "timezone": "Europe/Zurich", "elevation": 408.0},
    {"name": "Rome, Italy", "city": "Rome", "country": "Italy", "latitude": 41.9028, "longitude": 12.4964, "timezone": "Europe/Rome", "elevation": 21.0},
    {"name": "Madrid, Spain", "city": "Madrid", "country": "Spain", "latitude": 40.4168, "longitude": -3.7038, "timezone": "Europe/Madrid", "elevation": 667.0},
    {"name": "Dublin, Ireland", "city": "Dublin", "country": "Ireland", "latitude": 53.3498, "longitude": -6.2603, "timezone": "Europe/Dublin", "elevation": 20.0},

    # --- Canada ---
    {"name": "Toronto, Canada", "city": "Toronto", "country": "Canada", "latitude": 43.6532, "longitude": -79.3832, "timezone": "America/Toronto", "elevation": 76.0},
    {"name": "Vancouver, Canada", "city": "Vancouver", "country": "Canada", "latitude": 49.2827, "longitude": -123.1207, "timezone": "America/Vancouver", "elevation": 70.0},
    {"name": "Montreal, Canada", "city": "Montreal", "country": "Canada", "latitude": 45.5017, "longitude": -73.5673, "timezone": "America/Toronto", "elevation": 36.0},
    {"name": "Calgary, Canada", "city": "Calgary", "country": "Canada", "latitude": 51.0447, "longitude": -114.0719, "timezone": "America/Edmonton", "elevation": 1045.0},
    {"name": "Ottawa, Canada", "city": "Ottawa", "country": "Canada", "latitude": 45.4215, "longitude": -75.6972, "timezone": "America/Toronto", "elevation": 70.0},

    # --- Australia & New Zealand ---
    {"name": "Sydney, Australia", "city": "Sydney", "country": "Australia", "latitude": -33.8688, "longitude": 151.2093, "timezone": "Australia/Sydney", "elevation": 19.0},
    {"name": "Melbourne, Australia", "city": "Melbourne", "country": "Australia", "latitude": -37.8136, "longitude": 144.9631, "timezone": "Australia/Melbourne", "elevation": 31.0},
    {"name": "Brisbane, Australia", "city": "Brisbane", "country": "Australia", "latitude": -27.4698, "longitude": 153.0251, "timezone": "Australia/Brisbane", "elevation": 28.0},
    {"name": "Perth, Australia", "city": "Perth", "country": "Australia", "latitude": -31.9505, "longitude": 115.8605, "timezone": "Australia/Perth", "elevation": 31.0},
    {"name": "Auckland, New Zealand", "city": "Auckland", "country": "New Zealand", "latitude": -36.8485, "longitude": 174.7633, "timezone": "Pacific/Auckland", "elevation": 20.0},

    # --- Middle East & Asia ---
    {"name": "Dubai, United Arab Emirates", "city": "Dubai", "country": "UAE", "latitude": 25.2048, "longitude": 55.2708, "timezone": "Asia/Dubai", "elevation": 5.0},
    {"name": "Abu Dhabi, UAE", "city": "Abu Dhabi", "country": "UAE", "latitude": 24.4539, "longitude": 54.3773, "timezone": "Asia/Dubai", "elevation": 13.0},
    {"name": "Doha, Qatar", "city": "Doha", "country": "Qatar", "latitude": 25.2854, "longitude": 51.5310, "timezone": "Asia/Qatar", "elevation": 10.0},
    {"name": "Singapore", "city": "Singapore", "country": "Singapore", "latitude": 1.3521, "longitude": 103.8198, "timezone": "Asia/Singapore", "elevation": 15.0},
    {"name": "Kuala Lumpur, Malaysia", "city": "Kuala Lumpur", "country": "Malaysia", "latitude": 3.1390, "longitude": 101.6869, "timezone": "Asia/Kuala_Lumpur", "elevation": 66.0},
    {"name": "Bangkok, Thailand", "city": "Bangkok", "country": "Thailand", "latitude": 13.7563, "longitude": 100.5018, "timezone": "Asia/Bangkok", "elevation": 1.5},
    {"name": "Tokyo, Japan", "city": "Tokyo", "country": "Japan", "latitude": 35.6762, "longitude": 139.6503, "timezone": "Asia/Tokyo", "elevation": 40.0},
    {"name": "Hong Kong", "city": "Hong Kong", "country": "Hong Kong", "latitude": 22.3193, "longitude": 114.1694, "timezone": "Asia/Hong_Kong", "elevation": 32.0},
    {"name": "Colombo, Sri Lanka", "city": "Colombo", "country": "Sri Lanka", "latitude": 6.9271, "longitude": 79.8612, "timezone": "Asia/Colombo", "elevation": 7.0},
    {"name": "Dhaka, Bangladesh", "city": "Dhaka", "country": "Bangladesh", "latitude": 23.8103, "longitude": 90.4125, "timezone": "Asia/Dhaka", "elevation": 4.0},
]


# Combined unified lookup table
CITIES_DATA: List[Dict[str, any]] = NEPAL_MAJOR_CITIES + NEPAL_DISTRICTS_DATA + INTERNATIONAL_CITIES


def search_cities(query: str, limit: int = 15) -> List[Dict[str, any]]:
    """
    Search cities and districts by name, district, city, province, or country.
    Supports smart prefix and substring matching.
    """
    if not query:
        return CITIES_DATA[:limit]

    q = query.strip().lower()
    matches: List[Dict[str, any]] = []
    seen_names = set()

    def add_match(item: Dict[str, any]):
        if item["name"] not in seen_names:
            matches.append(item)
            seen_names.add(item["name"])

    # 1. Direct starts-with on city name, district name, or full title
    for item in CITIES_DATA:
        name_lower = item["name"].lower()
        city_lower = item.get("city", "").lower()
        district_lower = item.get("district", "").lower()

        if (
            city_lower.startswith(q)
            or district_lower.startswith(q)
            or name_lower.startswith(q)
        ):
            add_match(item)
            if len(matches) >= limit:
                return matches

    # 2. Substring matching in full name, district, province, or country
    for item in CITIES_DATA:
        name_lower = item["name"].lower()
        district_lower = item.get("district", "").lower()
        province_lower = item.get("province", "").lower()

        if (
            q in name_lower
            or q in district_lower
            or q in province_lower
        ):
            add_match(item)
            if len(matches) >= limit:
                return matches

    # 3. Special "nepal districts" or "nepal" keyword query
    if "district" in q or "nepal" in q:
        for item in NEPAL_DISTRICTS_DATA:
            add_match(item)
            if len(matches) >= limit:
                return matches

    return matches
