"""
api/cities_db.py

Curated fast offline city database with coordinates and IANA timezones.
Covers major cities in Nepal, India, USA, UK, Canada, Australia, Europe, and Asia.
"""

from __future__ import annotations

from typing import Dict, List, Optional


CITIES_DATA: List[Dict[str, any]] = [
    # --- Nepal ---
    {"name": "Kathmandu, Nepal", "city": "Kathmandu", "country": "Nepal", "latitude": 27.7172, "longitude": 85.3240, "timezone": "Asia/Kathmandu", "elevation": 1400.0},
    {"name": "Pokhara, Nepal", "city": "Pokhara", "country": "Nepal", "latitude": 28.2096, "longitude": 83.9856, "timezone": "Asia/Kathmandu", "elevation": 822.0},
    {"name": "Lalitpur (Patan), Nepal", "city": "Lalitpur", "country": "Nepal", "latitude": 27.6667, "longitude": 85.3167, "timezone": "Asia/Kathmandu", "elevation": 1400.0},
    {"name": "Bhaktapur, Nepal", "city": "Bhaktapur", "country": "Nepal", "latitude": 27.6710, "longitude": 85.4298, "timezone": "Asia/Kathmandu", "elevation": 1401.0},
    {"name": "Biratnagar, Nepal", "city": "Biratnagar", "country": "Nepal", "latitude": 26.4525, "longitude": 87.2718, "timezone": "Asia/Kathmandu", "elevation": 80.0},
    {"name": "Birgunj, Nepal", "city": "Birgunj", "country": "Nepal", "latitude": 27.0134, "longitude": 84.8773, "timezone": "Asia/Kathmandu", "elevation": 80.0},
    {"name": "Bharatpur (Chitwan), Nepal", "city": "Bharatpur", "country": "Nepal", "latitude": 27.6833, "longitude": 84.4333, "timezone": "Asia/Kathmandu", "elevation": 208.0},
    {"name": "Butwal, Nepal", "city": "Butwal", "country": "Nepal", "latitude": 27.7000, "longitude": 83.4500, "timezone": "Asia/Kathmandu", "elevation": 150.0},
    {"name": "Dharan, Nepal", "city": "Dharan", "country": "Nepal", "latitude": 26.8124, "longitude": 87.2834, "timezone": "Asia/Kathmandu", "elevation": 349.0},
    {"name": "Nepalgunj, Nepal", "city": "Nepalgunj", "country": "Nepal", "latitude": 28.0500, "longitude": 81.6167, "timezone": "Asia/Kathmandu", "elevation": 150.0},
    {"name": "Dhangadhi, Nepal", "city": "Dhangadhi", "country": "Nepal", "latitude": 28.6853, "longitude": 80.5960, "timezone": "Asia/Kathmandu", "elevation": 109.0},
    {"name": "Hetauda, Nepal", "city": "Hetauda", "country": "Nepal", "latitude": 27.4287, "longitude": 85.0326, "timezone": "Asia/Kathmandu", "elevation": 345.0},
    {"name": "Janakpur, Nepal", "city": "Janakpur", "country": "Nepal", "latitude": 26.7288, "longitude": 85.9244, "timezone": "Asia/Kathmandu", "elevation": 70.0},
    {"name": "Bhairahawa (Siddharthanagar), Nepal", "city": "Bhairahawa", "country": "Nepal", "latitude": 27.5000, "longitude": 83.4500, "timezone": "Asia/Kathmandu", "elevation": 105.0},
    {"name": "Itahari, Nepal", "city": "Itahari", "country": "Nepal", "latitude": 26.6667, "longitude": 87.2833, "timezone": "Asia/Kathmandu", "elevation": 116.0},

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


def search_cities(query: str, limit: int = 10) -> List[Dict[str, any]]:
    """
    Search cities by name, city, or country prefix/substring.
    """
    if not query:
        return CITIES_DATA[:limit]

    q = query.strip().lower()
    matches = []

    # Direct start matches first
    for item in CITIES_DATA:
        if item["name"].lower().startswith(q) or item["city"].lower().startswith(q):
            matches.append(item)
            if len(matches) >= limit:
                return matches

    # Substring matches second
    for item in CITIES_DATA:
        if item not in matches and (q in item["name"].lower() or q in item["country"].lower()):
            matches.append(item)
            if len(matches) >= limit:
                return matches

    return matches
