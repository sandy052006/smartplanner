"""
SmartPlanner City Data
======================
Indian cities classified per 7th Central Pay Commission (CPC) HRA rules.
X, Y, Z classification based on population census & government gazette.

HRA Rates (7th CPC):
  - X Class Cities: 27% of Basic Pay
  - Y Class Cities: 18% of Basic Pay
  - Z Class Cities:  9% of Basic Pay

Sources:
  - Ministry of Finance, Govt. of India — 7th CPC Implementation
  - Central Government HRA Orders
  - Income Tax Act, 1961 (New Regime FY 2024-25)
"""

from decimal import Decimal

# ─────────────────────────────────────────────────────────────
#  INDIAN CITY DATABASE
# ─────────────────────────────────────────────────────────────

INDIAN_CITIES = {
    # ── X CLASS CITIES (Population > 50 lakh, HRA = 27%) ────
    'mumbai': {
        'display_name': 'Mumbai',
        'state': 'Maharashtra',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.28'),
        'avg_rent_1bhk': 25000,
        'avg_grocery_monthly': 8000,
        'transport_monthly': 2000,
        'description': 'Financial capital of India. Highest cost of living.',
        'currency': '₹',
        'search_term': 'Mumbai,India,cityscape',
    },
    'delhi': {
        'display_name': 'Delhi',
        'state': 'Delhi (NCT)',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.22'),
        'avg_rent_1bhk': 18000,
        'avg_grocery_monthly': 7000,
        'transport_monthly': 1800,
        'description': 'National Capital Territory. Hub of government & IT.',
        'currency': '₹',
        'search_term': 'New Delhi,India,skyline',
    },
    'new delhi': {
        'display_name': 'New Delhi',
        'state': 'Delhi (NCT)',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.22'),
        'avg_rent_1bhk': 18000,
        'avg_grocery_monthly': 7000,
        'transport_monthly': 1800,
        'description': 'National Capital Territory. Hub of government & IT.',
        'currency': '₹',
        'search_term': 'New Delhi,India,skyline',
    },
    'bangalore': {
        'display_name': 'Bengaluru',
        'state': 'Karnataka',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.24'),
        'avg_rent_1bhk': 22000,
        'avg_grocery_monthly': 7500,
        'transport_monthly': 2200,
        'description': 'Silicon Valley of India. Major IT & startup hub.',
        'currency': '₹',
        'search_term': 'Bangalore,India,city',
    },
    'bengaluru': {
        'display_name': 'Bengaluru',
        'state': 'Karnataka',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.24'),
        'avg_rent_1bhk': 22000,
        'avg_grocery_monthly': 7500,
        'transport_monthly': 2200,
        'description': 'Silicon Valley of India. Major IT & startup hub.',
        'currency': '₹',
        'search_term': 'Bangalore,India,city',
    },
    'chennai': {
        'display_name': 'Chennai',
        'state': 'Tamil Nadu',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.18'),
        'avg_rent_1bhk': 15000,
        'avg_grocery_monthly': 6500,
        'transport_monthly': 1500,
        'description': 'Detroit of India. Manufacturing & IT services hub.',
        'currency': '₹',
        'search_term': 'Chennai,India,Marina Beach',
    },
    'hyderabad': {
        'display_name': 'Hyderabad',
        'state': 'Telangana',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.16'),
        'avg_rent_1bhk': 16000,
        'avg_grocery_monthly': 6000,
        'transport_monthly': 1600,
        'description': 'Cyberabad. Fastest growing IT city in India.',
        'currency': '₹',
        'search_term': 'Hyderabad,India,Charminar',
    },
    'kolkata': {
        'display_name': 'Kolkata',
        'state': 'West Bengal',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.10'),
        'avg_rent_1bhk': 12000,
        'avg_grocery_monthly': 5500,
        'transport_monthly': 1200,
        'description': 'Cultural capital of India. Relatively affordable metro.',
        'currency': '₹',
        'search_term': 'Kolkata,India,Howrah Bridge',
    },
    'ahmedabad': {
        'display_name': 'Ahmedabad',
        'state': 'Gujarat',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.08'),
        'avg_rent_1bhk': 12000,
        'avg_grocery_monthly': 5500,
        'transport_monthly': 1300,
        'description': 'Commercial capital of Gujarat. Textile & chemical hub.',
        'currency': '₹',
        'search_term': 'Ahmedabad,India,Sabarmati',
    },
    'pune': {
        'display_name': 'Pune',
        'state': 'Maharashtra',
        'category': 'X',
        'hra_percent': 27,
        'cost_index': Decimal('1.20'),
        'avg_rent_1bhk': 18000,
        'avg_grocery_monthly': 7000,
        'transport_monthly': 1800,
        'description': 'Oxford of the East. IT & automotive manufacturing.',
        'currency': '₹',
        'search_term': 'Pune,India,city',
    },

    # ── Y CLASS CITIES (Population 5–50 lakh, HRA = 18%) ────
    'jaipur': {
        'display_name': 'Jaipur',
        'state': 'Rajasthan',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.02'),
        'avg_rent_1bhk': 9000,
        'avg_grocery_monthly': 5000,
        'transport_monthly': 1000,
        'description': 'Pink City of India. Tourism & handicraft economy.',
        'currency': '₹',
        'search_term': 'Jaipur,India,Hawa Mahal',
    },
    'lucknow': {
        'display_name': 'Lucknow',
        'state': 'Uttar Pradesh',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('0.98'),
        'avg_rent_1bhk': 8000,
        'avg_grocery_monthly': 4800,
        'transport_monthly': 900,
        'description': 'City of Nawabs. State capital & growing IT hub.',
        'currency': '₹',
        'search_term': 'Lucknow,India,Bara Imambara',
    },
    'chandigarh': {
        'display_name': 'Chandigarh',
        'state': 'Chandigarh (UT)',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.08'),
        'avg_rent_1bhk': 11000,
        'avg_grocery_monthly': 5500,
        'transport_monthly': 1200,
        'description': 'The City Beautiful. Planned city & IT services hub.',
        'currency': '₹',
        'search_term': 'Chandigarh,India,Rock Garden',
    },
    'surat': {
        'display_name': 'Surat',
        'state': 'Gujarat',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.03'),
        'avg_rent_1bhk': 9500,
        'avg_grocery_monthly': 5000,
        'transport_monthly': 1000,
        'description': 'Diamond City. Textile & diamond trading center.',
        'currency': '₹',
        'search_term': 'Surat,India,city',
    },
    'nagpur': {
        'display_name': 'Nagpur',
        'state': 'Maharashtra',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.00'),
        'avg_rent_1bhk': 9000,
        'avg_grocery_monthly': 4800,
        'transport_monthly': 900,
        'description': 'Orange City. Geographical center of India.',
        'currency': '₹',
        'search_term': 'Nagpur,India,city',
    },
    'indore': {
        'display_name': 'Indore',
        'state': 'Madhya Pradesh',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.00'),
        'avg_rent_1bhk': 9000,
        'avg_grocery_monthly': 4700,
        'transport_monthly': 900,
        'description': 'Commercial capital of MP. Fastest growing city.',
        'currency': '₹',
        'search_term': 'Indore,India,Rajwada',
    },
    'bhopal': {
        'display_name': 'Bhopal',
        'state': 'Madhya Pradesh',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('0.97'),
        'avg_rent_1bhk': 8500,
        'avg_grocery_monthly': 4500,
        'transport_monthly': 850,
        'description': 'City of Lakes. State capital of Madhya Pradesh.',
        'currency': '₹',
        'search_term': 'Bhopal,India,Upper Lake',
    },
    'patna': {
        'display_name': 'Patna',
        'state': 'Bihar',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('0.94'),
        'avg_rent_1bhk': 7500,
        'avg_grocery_monthly': 4200,
        'transport_monthly': 800,
        'description': 'Ancient city on Ganges. State capital of Bihar.',
        'currency': '₹',
        'search_term': 'Patna,India,Ganga river',
    },
    'kochi': {
        'display_name': 'Kochi',
        'state': 'Kerala',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.06'),
        'avg_rent_1bhk': 10000,
        'avg_grocery_monthly': 5200,
        'transport_monthly': 1000,
        'description': 'Queen of Arabian Sea. IT & marine trade hub.',
        'currency': '₹',
        'search_term': 'Kochi,India,harbour',
    },
    'coimbatore': {
        'display_name': 'Coimbatore',
        'state': 'Tamil Nadu',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.02'),
        'avg_rent_1bhk': 9000,
        'avg_grocery_monthly': 4800,
        'transport_monthly': 900,
        'description': 'Manchester of South India. Textile manufacturing center.',
        'currency': '₹',
        'search_term': 'Coimbatore,India,city',
    },
    'gurgaon': {
        'display_name': 'Gurugram',
        'state': 'Haryana',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.18'),
        'avg_rent_1bhk': 20000,
        'avg_grocery_monthly': 7000,
        'transport_monthly': 2000,
        'description': 'Millennium City. Corporate HQ & financial district.',
        'currency': '₹',
        'search_term': 'Gurugram,India,skyline',
    },
    'gurugram': {
        'display_name': 'Gurugram',
        'state': 'Haryana',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.18'),
        'avg_rent_1bhk': 20000,
        'avg_grocery_monthly': 7000,
        'transport_monthly': 2000,
        'description': 'Millennium City. Corporate HQ & financial district.',
        'currency': '₹',
        'search_term': 'Gurugram,India,skyline',
    },
    'noida': {
        'display_name': 'Noida',
        'state': 'Uttar Pradesh',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.14'),
        'avg_rent_1bhk': 16000,
        'avg_grocery_monthly': 6500,
        'transport_monthly': 1700,
        'description': 'New Okhla Industrial Development Area. IT & media hub.',
        'currency': '₹',
        'search_term': 'Noida,India,city',
    },
    'visakhapatnam': {
        'display_name': 'Visakhapatnam',
        'state': 'Andhra Pradesh',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.02'),
        'avg_rent_1bhk': 9000,
        'avg_grocery_monthly': 4800,
        'transport_monthly': 950,
        'description': 'City of Destiny. Major seaport & steel manufacturing.',
        'currency': '₹',
        'search_term': 'Visakhapatnam,India,beach',
    },
    'vadodara': {
        'display_name': 'Vadodara',
        'state': 'Gujarat',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.01'),
        'avg_rent_1bhk': 9000,
        'avg_grocery_monthly': 4700,
        'transport_monthly': 900,
        'description': 'Cultural capital of Gujarat. Chemical & engineering hub.',
        'currency': '₹',
        'search_term': 'Vadodara,India,Laxmi Vilas Palace',
    },
    'agra': {
        'display_name': 'Agra',
        'state': 'Uttar Pradesh',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('0.96'),
        'avg_rent_1bhk': 8000,
        'avg_grocery_monthly': 4500,
        'transport_monthly': 850,
        'description': 'Home of the Taj Mahal. Tourism & leather industry.',
        'currency': '₹',
        'search_term': 'Agra,India,Taj Mahal',
    },
    'varanasi': {
        'display_name': 'Varanasi',
        'state': 'Uttar Pradesh',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('0.95'),
        'avg_rent_1bhk': 7500,
        'avg_grocery_monthly': 4200,
        'transport_monthly': 800,
        'description': 'Spiritual capital of India. Oldest living city in the world.',
        'currency': '₹',
        'search_term': 'Varanasi,India,Ganga Ghat',
    },
    'thiruvananthapuram': {
        'display_name': 'Thiruvananthapuram',
        'state': 'Kerala',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('1.04'),
        'avg_rent_1bhk': 9500,
        'avg_grocery_monthly': 5000,
        'transport_monthly': 950,
        'description': 'Capital of God\'s Own Country. IT & tourism center.',
        'currency': '₹',
        'search_term': 'Thiruvananthapuram,Kerala,India',
    },
    'amritsar': {
        'display_name': 'Amritsar',
        'state': 'Punjab',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('0.99'),
        'avg_rent_1bhk': 8500,
        'avg_grocery_monthly': 4600,
        'transport_monthly': 900,
        'description': 'Holy city of the Sikhs. Home of the Golden Temple.',
        'currency': '₹',
        'search_term': 'Amritsar,India,Golden Temple',
    },
    'ranchi': {
        'display_name': 'Ranchi',
        'state': 'Jharkhand',
        'category': 'Y',
        'hra_percent': 18,
        'cost_index': Decimal('0.95'),
        'avg_rent_1bhk': 7500,
        'avg_grocery_monthly': 4300,
        'transport_monthly': 800,
        'description': 'City of Waterfalls. Capital of Jharkhand.',
        'currency': '₹',
        'search_term': 'Ranchi,India,Jharkhand',
    },

    # ── Z CLASS CITIES (Other cities, HRA = 9%) ─────────────
    'mysuru': {
        'display_name': 'Mysuru',
        'state': 'Karnataka',
        'category': 'Z',
        'hra_percent': 9,
        'cost_index': Decimal('0.92'),
        'avg_rent_1bhk': 7000,
        'avg_grocery_monthly': 4200,
        'transport_monthly': 750,
        'description': 'City of Palaces. Heritage & tourism economy.',
        'currency': '₹',
        'search_term': 'Mysore,India,Palace',
    },
    'mysore': {
        'display_name': 'Mysuru',
        'state': 'Karnataka',
        'category': 'Z',
        'hra_percent': 9,
        'cost_index': Decimal('0.92'),
        'avg_rent_1bhk': 7000,
        'avg_grocery_monthly': 4200,
        'transport_monthly': 750,
        'description': 'City of Palaces. Heritage & tourism economy.',
        'currency': '₹',
        'search_term': 'Mysore,India,Palace',
    },
    'shimla': {
        'display_name': 'Shimla',
        'state': 'Himachal Pradesh',
        'category': 'Z',
        'hra_percent': 9,
        'cost_index': Decimal('0.90'),
        'avg_rent_1bhk': 7000,
        'avg_grocery_monthly': 4000,
        'transport_monthly': 700,
        'description': 'Queen of Hills. Summer capital & tourism destination.',
        'currency': '₹',
        'search_term': 'Shimla,India,hill station',
    },
    'dehradun': {
        'display_name': 'Dehradun',
        'state': 'Uttarakhand',
        'category': 'Z',
        'hra_percent': 9,
        'cost_index': Decimal('0.93'),
        'avg_rent_1bhk': 7500,
        'avg_grocery_monthly': 4200,
        'transport_monthly': 800,
        'description': 'Gateway to Himalayan pilgrimage sites. Education hub.',
        'currency': '₹',
        'search_term': 'Dehradun,India,valley',
    },
    'guwahati': {
        'display_name': 'Guwahati',
        'state': 'Assam',
        'category': 'Z',
        'hra_percent': 9,
        'cost_index': Decimal('0.91'),
        'avg_rent_1bhk': 7000,
        'avg_grocery_monthly': 4100,
        'transport_monthly': 750,
        'description': 'Gateway to Northeast India. River port city.',
        'currency': '₹',
        'search_term': 'Guwahati,India,Brahmaputra',
    },
    'jodhpur': {
        'display_name': 'Jodhpur',
        'state': 'Rajasthan',
        'category': 'Z',
        'hra_percent': 9,
        'cost_index': Decimal('0.90'),
        'avg_rent_1bhk': 6500,
        'avg_grocery_monthly': 4000,
        'transport_monthly': 700,
        'description': 'Blue City & Sun City of Rajasthan. Mehrangarh Fort.',
        'currency': '₹',
        'search_term': 'Jodhpur,India,Mehrangarh Fort',
    },
}

# Indian Income Tax Slabs (New Regime FY 2024-25, per Union Budget 2024)
INDIA_TAX_SLABS_NEW_REGIME = [
    {'min': 0, 'max': 300000, 'rate': 0, 'label': 'Up to ₹3 lakh'},
    {'min': 300001, 'max': 700000, 'rate': 5, 'label': '₹3L – ₹7L'},
    {'min': 700001, 'max': 1000000, 'rate': 10, 'label': '₹7L – ₹10L'},
    {'min': 1000001, 'max': 1200000, 'rate': 15, 'label': '₹10L – ₹12L'},
    {'min': 1200001, 'max': 1500000, 'rate': 20, 'label': '₹12L – ₹15L'},
    {'min': 1500001, 'max': None, 'rate': 30, 'label': 'Above ₹15L'},
]

# Indian Income Tax Slabs (Old Regime FY 2024-25)
INDIA_TAX_SLABS_OLD_REGIME = [
    {'min': 0, 'max': 250000, 'rate': 0, 'label': 'Up to ₹2.5 lakh'},
    {'min': 250001, 'max': 500000, 'rate': 5, 'label': '₹2.5L – ₹5L'},
    {'min': 500001, 'max': 1000000, 'rate': 20, 'label': '₹5L – ₹10L'},
    {'min': 1000001, 'max': None, 'rate': 30, 'label': 'Above ₹10L'},
]

# GST Rates (India)
GST_RATES = {
    'essentials': 0,
    'food_basic': 5,
    'consumer_goods': 12,
    'services': 18,
    'luxury': 28,
}

# DA (Dearness Allowance) — Central Govt — updated Jan 2024
CENTRAL_GOVT_DA_PERCENT = 50  # 50% of Basic Pay (effective Jan 2024)

# ─────────────────────────────────────────────────────────────
#  FOREIGN CITY DATABASE
# ─────────────────────────────────────────────────────────────

FOREIGN_CITIES = {
    # ── UNITED STATES ────────────────────────────────────────
    'new york': {
        'display_name': 'New York City',
        'country': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'exchange_rate_inr': 83.5,
        'cost_index': Decimal('2.80'),
        'avg_rent_1bhk': 3500,
        'avg_grocery_monthly': 600,
        'tax_system': {
            'name': 'US Federal + State + City Tax',
            'federal_brackets': [
                {'rate': 10, 'up_to': 11600},
                {'rate': 12, 'up_to': 47150},
                {'rate': 22, 'up_to': 100525},
                {'rate': 24, 'up_to': 191950},
                {'rate': 32, 'up_to': 243725},
                {'rate': 35, 'up_to': 609350},
                {'rate': 37, 'up_to': None},
            ],
            'state_tax_rate': 6.85,
            'city_tax_rate': 3.876,
            'social_security': 6.2,
            'medicare': 1.45,
            'sales_tax': 8.875,
            'notes': 'NYC has one of highest combined tax rates in USA. No HRA. Health insurance typically employer-provided.',
        },
        'search_term': 'New York City,USA,Manhattan skyline',
        'description': 'Global financial hub. Home to Wall Street & NYSE.',
    },
    'san francisco': {
        'display_name': 'San Francisco',
        'country': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'exchange_rate_inr': 83.5,
        'cost_index': Decimal('3.10'),
        'avg_rent_1bhk': 3800,
        'avg_grocery_monthly': 700,
        'tax_system': {
            'name': 'US Federal + California State Tax',
            'federal_brackets': [
                {'rate': 10, 'up_to': 11600},
                {'rate': 12, 'up_to': 47150},
                {'rate': 22, 'up_to': 100525},
                {'rate': 32, 'up_to': 191950},
            ],
            'state_tax_rate': 13.3,
            'city_tax_rate': 0,
            'social_security': 6.2,
            'medicare': 1.45,
            'sales_tax': 8.625,
            'notes': 'California has highest state income tax in USA (up to 13.3%). No city income tax.',
        },
        'search_term': 'San Francisco,USA,Golden Gate Bridge',
        'description': 'Tech capital of the world. Silicon Valley gateway.',
    },
    'los angeles': {
        'display_name': 'Los Angeles',
        'country': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'exchange_rate_inr': 83.5,
        'cost_index': Decimal('2.60'),
        'avg_rent_1bhk': 2800,
        'avg_grocery_monthly': 600,
        'tax_system': {
            'name': 'US Federal + California State Tax',
            'federal_brackets': [
                {'rate': 10, 'up_to': 11600},
                {'rate': 12, 'up_to': 47150},
                {'rate': 22, 'up_to': 100525},
                {'rate': 32, 'up_to': 191950},
            ],
            'state_tax_rate': 13.3,
            'city_tax_rate': 0,
            'social_security': 6.2,
            'medicare': 1.45,
            'sales_tax': 10.25,
            'notes': 'California state tax applies. Entertainment industry hub.',
        },
        'search_term': 'Los Angeles,USA,Hollywood skyline',
        'description': 'Entertainment capital of the world. Home of Hollywood.',
    },

    # ── UNITED KINGDOM ────────────────────────────────────────
    'london': {
        'display_name': 'London',
        'country': 'United Kingdom',
        'currency': 'GBP',
        'currency_symbol': '£',
        'exchange_rate_inr': 106.5,
        'cost_index': Decimal('2.70'),
        'avg_rent_1bhk': 2200,
        'avg_grocery_monthly': 350,
        'tax_system': {
            'name': 'UK Income Tax + National Insurance',
            'brackets': [
                {'label': 'Personal Allowance', 'rate': 0, 'up_to': 12570},
                {'label': 'Basic Rate', 'rate': 20, 'up_to': 50270},
                {'label': 'Higher Rate', 'rate': 40, 'up_to': 125140},
                {'label': 'Additional Rate', 'rate': 45, 'up_to': None},
            ],
            'national_insurance': 8.0,
            'vat': 20.0,
            'council_tax': 'Varies by borough (£1,000–£3,500/yr)',
            'notes': 'NHS provides free public healthcare. No separate city income tax. Capital Gains Tax applies on investments.',
        },
        'search_term': 'London,UK,Tower Bridge Thames',
        'description': 'Global financial center. Home to the Bank of England.',
    },
    'manchester': {
        'display_name': 'Manchester',
        'country': 'United Kingdom',
        'currency': 'GBP',
        'currency_symbol': '£',
        'exchange_rate_inr': 106.5,
        'cost_index': Decimal('1.90'),
        'avg_rent_1bhk': 1400,
        'avg_grocery_monthly': 300,
        'tax_system': {
            'name': 'UK Income Tax + National Insurance',
            'brackets': [
                {'label': 'Personal Allowance', 'rate': 0, 'up_to': 12570},
                {'label': 'Basic Rate', 'rate': 20, 'up_to': 50270},
                {'label': 'Higher Rate', 'rate': 40, 'up_to': 125140},
                {'label': 'Additional Rate', 'rate': 45, 'up_to': None},
            ],
            'national_insurance': 8.0,
            'vat': 20.0,
            'council_tax': 'Approx £1,500–£2,200/yr',
            'notes': 'More affordable than London. Northern Powerhouse city.',
        },
        'search_term': 'Manchester,UK,skyline',
        'description': 'Northern powerhouse. Media, tech & sports hub.',
    },

    # ── UNITED ARAB EMIRATES ──────────────────────────────────
    'dubai': {
        'display_name': 'Dubai',
        'country': 'United Arab Emirates',
        'currency': 'AED',
        'currency_symbol': 'AED',
        'exchange_rate_inr': 22.7,
        'cost_index': Decimal('2.20'),
        'avg_rent_1bhk': 5000,
        'avg_grocery_monthly': 500,
        'tax_system': {
            'name': 'UAE Zero Income Tax',
            'income_tax_rate': 0,
            'vat': 5.0,
            'corporate_tax': 9.0,
            'social_insurance': 0,
            'notes': '🎉 NO personal income tax in UAE. 5% VAT on most goods/services. 9% corporate tax (2023). High cost of living offset by tax-free income.',
        },
        'search_term': 'Dubai,UAE,Burj Khalifa skyline',
        'description': 'Zero-tax emirate. Global business & luxury hub.',
    },
    'abu dhabi': {
        'display_name': 'Abu Dhabi',
        'country': 'United Arab Emirates',
        'currency': 'AED',
        'currency_symbol': 'AED',
        'exchange_rate_inr': 22.7,
        'cost_index': Decimal('2.00'),
        'avg_rent_1bhk': 4500,
        'avg_grocery_monthly': 450,
        'tax_system': {
            'name': 'UAE Zero Income Tax',
            'income_tax_rate': 0,
            'vat': 5.0,
            'corporate_tax': 9.0,
            'social_insurance': 0,
            'notes': '🎉 NO personal income tax. UAE capital. Significant oil revenue economy. More affordable than Dubai.',
        },
        'search_term': 'Abu Dhabi,UAE,Sheikh Zayed Mosque',
        'description': 'UAE capital. Oil-rich emirate. Tax-free living.',
    },

    # ── SINGAPORE ─────────────────────────────────────────────
    'singapore': {
        'display_name': 'Singapore',
        'country': 'Singapore',
        'currency': 'SGD',
        'currency_symbol': 'S$',
        'exchange_rate_inr': 62.0,
        'cost_index': Decimal('2.40'),
        'avg_rent_1bhk': 2800,
        'avg_grocery_monthly': 400,
        'tax_system': {
            'name': 'Singapore Progressive Income Tax',
            'brackets': [
                {'label': 'Up to S$20,000', 'rate': 0},
                {'label': 'S$20,001 – S$30,000', 'rate': 2},
                {'label': 'S$30,001 – S$40,000', 'rate': 3.5},
                {'label': 'S$40,001 – S$80,000', 'rate': 7},
                {'label': 'S$80,001 – S$120,000', 'rate': 11.5},
                {'label': 'S$120,001 – S$160,000', 'rate': 15},
                {'label': 'S$160,001 – S$200,000', 'rate': 18},
                {'label': 'S$200,001 – S$320,000', 'rate': 19},
                {'label': 'S$320,001 – S$500,000', 'rate': 22},
                {'label': 'Above S$500,000', 'rate': 24},
            ],
            'cpf_employee': 20.0,
            'gst': 9.0,
            'notes': 'CPF (Central Provident Fund) at 20% of salary for retirement & healthcare. GST raised to 9% in 2024.',
        },
        'search_term': 'Singapore,Marina Bay Sands,skyline',
        'description': 'Asian financial hub. Extremely clean & efficient city.',
    },

    # ── CANADA ────────────────────────────────────────────────
    'toronto': {
        'display_name': 'Toronto',
        'country': 'Canada',
        'currency': 'CAD',
        'currency_symbol': 'C$',
        'exchange_rate_inr': 61.5,
        'cost_index': Decimal('2.10'),
        'avg_rent_1bhk': 2400,
        'avg_grocery_monthly': 500,
        'tax_system': {
            'name': 'Canada Federal + Ontario Provincial Tax',
            'federal_brackets': [
                {'rate': 15, 'up_to': 55867},
                {'rate': 20.5, 'up_to': 111733},
                {'rate': 26, 'up_to': 154906},
                {'rate': 29, 'up_to': 220000},
                {'rate': 33, 'up_to': None},
            ],
            'provincial_tax_rate': 11.16,
            'cpp': 5.95,
            'ei': 1.66,
            'hst': 13.0,
            'notes': 'Canada Pension Plan (CPP) at 5.95%. Employment Insurance (EI) at 1.66%. Universal healthcare covered.',
        },
        'search_term': 'Toronto,Canada,CN Tower skyline',
        'description': 'Financial capital of Canada. Multicultural & welcoming.',
    },
    'vancouver': {
        'display_name': 'Vancouver',
        'country': 'Canada',
        'currency': 'CAD',
        'currency_symbol': 'C$',
        'exchange_rate_inr': 61.5,
        'cost_index': Decimal('2.30'),
        'avg_rent_1bhk': 2700,
        'avg_grocery_monthly': 520,
        'tax_system': {
            'name': 'Canada Federal + BC Provincial Tax',
            'federal_brackets': [
                {'rate': 15, 'up_to': 55867},
                {'rate': 20.5, 'up_to': 111733},
                {'rate': 26, 'up_to': 154906},
                {'rate': 33, 'up_to': None},
            ],
            'provincial_tax_rate': 7.7,
            'cpp': 5.95,
            'ei': 1.66,
            'gst': 5.0,
            'pst': 7.0,
            'notes': 'Lower provincial tax than Ontario. Very high real estate. Beautiful natural surroundings.',
        },
        'search_term': 'Vancouver,Canada,mountains skyline',
        'description': 'Most beautiful city in Canada. Gateway to Pacific.',
    },

    # ── AUSTRALIA ─────────────────────────────────────────────
    'sydney': {
        'display_name': 'Sydney',
        'country': 'Australia',
        'currency': 'AUD',
        'currency_symbol': 'A$',
        'exchange_rate_inr': 54.5,
        'cost_index': Decimal('2.20'),
        'avg_rent_1bhk': 2400,
        'avg_grocery_monthly': 500,
        'tax_system': {
            'name': 'Australian Income Tax + Medicare',
            'brackets': [
                {'label': 'Up to A$18,200', 'rate': 0},
                {'label': 'A$18,201 – A$45,000', 'rate': 19},
                {'label': 'A$45,001 – A$120,000', 'rate': 32.5},
                {'label': 'A$120,001 – A$180,000', 'rate': 37},
                {'label': 'Above A$180,000', 'rate': 45},
            ],
            'medicare_levy': 2.0,
            'superannuation': 11.0,
            'gst': 10.0,
            'notes': 'Superannuation (employer-paid pension) at 11%. Medicare Levy for public healthcare. No state income tax.',
        },
        'search_term': 'Sydney,Australia,Opera House Harbour',
        'description': 'Australia\'s largest city. Finance & tourism center.',
    },
    'melbourne': {
        'display_name': 'Melbourne',
        'country': 'Australia',
        'currency': 'AUD',
        'currency_symbol': 'A$',
        'exchange_rate_inr': 54.5,
        'cost_index': Decimal('2.10'),
        'avg_rent_1bhk': 2100,
        'avg_grocery_monthly': 480,
        'tax_system': {
            'name': 'Australian Income Tax + Medicare',
            'brackets': [
                {'label': 'Up to A$18,200', 'rate': 0},
                {'label': 'A$18,201 – A$45,000', 'rate': 19},
                {'label': 'A$45,001 – A$120,000', 'rate': 32.5},
                {'label': 'A$120,001 – A$180,000', 'rate': 37},
                {'label': 'Above A$180,000', 'rate': 45},
            ],
            'medicare_levy': 2.0,
            'superannuation': 11.0,
            'gst': 10.0,
            'notes': 'Most liveable city in world rankings. Slightly cheaper than Sydney.',
        },
        'search_term': 'Melbourne,Australia,CBD skyline',
        'description': 'Cultural capital of Australia. Tech & education hub.',
    },

    # ── GERMANY ───────────────────────────────────────────────
    'berlin': {
        'display_name': 'Berlin',
        'country': 'Germany',
        'currency': 'EUR',
        'currency_symbol': '€',
        'exchange_rate_inr': 90.0,
        'cost_index': Decimal('1.80'),
        'avg_rent_1bhk': 1400,
        'avg_grocery_monthly': 350,
        'tax_system': {
            'name': 'German Einkommensteuer (Income Tax)',
            'brackets': [
                {'label': 'Up to €11,604', 'rate': 0},
                {'label': '€11,605 – €17,005', 'rate': 14},
                {'label': '€17,006 – €66,760', 'rate': '14–42 (progressive)'},
                {'label': '€66,761 – €277,825', 'rate': 42},
                {'label': 'Above €277,825', 'rate': 45},
            ],
            'solidarity_surcharge': 5.5,
            'social_security_total': 20.0,
            'health_insurance': 7.3,
            'vat': 19.0,
            'notes': 'Solidarity surcharge (Solidaritätszuschlag) at 5.5% of tax. Strong social security & public healthcare.',
        },
        'search_term': 'Berlin,Germany,Brandenburg Gate',
        'description': 'Tech startup capital of Europe. Affordable & creative.',
    },
    'munich': {
        'display_name': 'Munich',
        'country': 'Germany',
        'currency': 'EUR',
        'currency_symbol': '€',
        'exchange_rate_inr': 90.0,
        'cost_index': Decimal('2.10'),
        'avg_rent_1bhk': 1800,
        'avg_grocery_monthly': 380,
        'tax_system': {
            'name': 'German Einkommensteuer (Income Tax)',
            'brackets': [
                {'label': 'Up to €11,604', 'rate': 0},
                {'label': '€11,605 – €66,760', 'rate': '14–42 (progressive)'},
                {'label': '€66,761 – €277,825', 'rate': 42},
                {'label': 'Above €277,825', 'rate': 45},
            ],
            'church_tax': 8.0,
            'social_security_total': 20.0,
            'health_insurance': 7.3,
            'vat': 19.0,
            'notes': 'BMW, Siemens HQ. Germany\'s most expensive city. High quality of life.',
        },
        'search_term': 'Munich,Germany,Marienplatz',
        'description': 'Bavaria\'s capital. BMW & engineering powerhouse.',
    },

    # ── JAPAN ─────────────────────────────────────────────────
    'tokyo': {
        'display_name': 'Tokyo',
        'country': 'Japan',
        'currency': 'JPY',
        'currency_symbol': '¥',
        'exchange_rate_inr': 0.55,
        'cost_index': Decimal('2.00'),
        'avg_rent_1bhk': 130000,
        'avg_grocery_monthly': 40000,
        'tax_system': {
            'name': 'Japan National Income Tax + Residence Tax',
            'national_brackets': [
                {'label': 'Up to ¥1,950,000', 'rate': 5},
                {'label': '¥1,950,001 – ¥3,300,000', 'rate': 10},
                {'label': '¥3,300,001 – ¥6,950,000', 'rate': 20},
                {'label': '¥6,950,001 – ¥9,000,000', 'rate': 23},
                {'label': '¥9,000,001 – ¥18,000,000', 'rate': 33},
                {'label': '¥18,000,001 – ¥40,000,000', 'rate': 40},
                {'label': 'Above ¥40,000,000', 'rate': 45},
            ],
            'residence_tax': 10.0,
            'consumption_tax': 10.0,
            'social_insurance': 14.0,
            'notes': 'Residence tax flat 10% on top of national tax. Consumption tax (VAT) at 10%. Strong pension & healthcare systems.',
        },
        'search_term': 'Tokyo,Japan,Mount Fuji skyline',
        'description': 'World\'s largest metropolitan area. Innovation hub.',
    },
}


def get_city_data(city_name: str) -> dict:
    """
    Look up city data. Returns dict with 'type' (indian/foreign/unknown)
    and the relevant data.
    """
    key = city_name.lower().strip()

    if key in INDIAN_CITIES:
        return {'type': 'indian', 'data': INDIAN_CITIES[key]}
    elif key in FOREIGN_CITIES:
        return {'type': 'foreign', 'data': FOREIGN_CITIES[key]}
    else:
        # Try partial match
        for city_key, city_data in INDIAN_CITIES.items():
            if key in city_key or city_key in key:
                return {'type': 'indian', 'data': city_data}
        for city_key, city_data in FOREIGN_CITIES.items():
            if key in city_key or city_key in key:
                return {'type': 'foreign', 'data': city_data}

        return {'type': 'unknown', 'data': None}


def calculate_indian_tax(annual_income_inr: float) -> dict:
    """Calculate approximate income tax under new regime (FY 2024-25)."""
    tax = 0
    prev_limit = 0
    breakdown = []
    income = float(annual_income_inr)

    for slab in INDIA_TAX_SLABS_NEW_REGIME:
        if income <= prev_limit:
            break
        upper = slab['max'] if slab['max'] else income
        taxable_in_slab = min(income, upper) - prev_limit
        if taxable_in_slab > 0 and slab['rate'] > 0:
            slab_tax = taxable_in_slab * slab['rate'] / 100
            breakdown.append({
                'label': slab['label'],
                'rate': slab['rate'],
                'taxable': taxable_in_slab,
                'tax': slab_tax,
            })
            tax += slab_tax
        prev_limit = upper

    # Section 87A rebate: if income <= 7L, tax = 0
    rebate = 0
    if income <= 700000 and tax <= 25000:
        rebate = tax
        tax = 0

    cess = tax * 0.04  # 4% health & education cess
    total_tax = tax + cess

    return {
        'annual_tax': round(total_tax, 2),
        'monthly_tax': round(total_tax / 12, 2),
        'effective_rate': round((total_tax / income * 100) if income > 0 else 0, 2),
        'cess': round(cess, 2),
        'rebate_87a': round(rebate, 2),
        'breakdown': breakdown,
    }


# All Indian cities list (for autocomplete)
ALL_INDIAN_CITY_NAMES = sorted(set(
    v['display_name'] for v in INDIAN_CITIES.values()
))

# All foreign cities list (for autocomplete)
ALL_FOREIGN_CITY_NAMES = sorted(set(
    v['display_name'] for v in FOREIGN_CITIES.values()
))
