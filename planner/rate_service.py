"""
SmartPlanner Live Rate Service
================================
Fetches the latest Indian government financial rates from official/reliable sources:
  • DA (Dearness Allowance)  — Ministry of Finance / 7th Pay Commission
  • HRA (House Rent Allowance) — 7th CPC classification
  • Income Tax Slabs         — Income Tax Act (Budget 2025, FY 2025-26)
  • GST rates                — GST Council

Strategy (per rate):
  1. Check Django DB cache (< CACHE_TTL_DAYS old) → use if fresh
  2. Try PRIMARY URL(s) → parse with BeautifulSoup
  3. Try SECONDARY URL(s) → fallback parse
  4. Use KNOWN-GOOD hardcoded values (updated for Budget 2025)
  5. Always store successful fetches back to DB cache

Each rate entry has:
  { 'value': ..., 'source': 'url or "hardcoded"', 'as_of': 'date-string', 'fetched_at': datetime }
"""

import re
import json
import logging
from datetime import datetime, timedelta, date

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

logger = logging.getLogger(__name__)

# ── How long to trust a cached rate before re-fetching ──────────────────────
CACHE_TTL_DAYS = 30          # re-fetch after 30 days
REQUEST_TIMEOUT = 6          # seconds per HTTP call
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'en-IN,en;q=0.9',
}

# ═══════════════════════════════════════════════════════════════════════════════
#  HARDCODED FALLBACK VALUES  (updated for Budget 2025 / FY 2025-26)
# ═══════════════════════════════════════════════════════════════════════════════

# DA Rate: 55% effective January 2025 (Cabinet approved Feb 27 2025)
FALLBACK_DA = {
    'rate': 55,
    'effective_from': 'January 2025',
    'next_revision': 'July 2025',
    'source': 'hardcoded',
    'as_of': '2025-02-27',
    'note': 'Cabinet approved on 27 Feb 2025. Revised bi-annually (Jan & Jul).',
}

# HRA: Unchanged since 7th CPC (OM dated 7 Jul 2017)
# Note: HRA linked to DA — if DA >= 50% then X=27%, Y=18%, Z=9%
# DA is currently 55% so the higher HRA slab is active.
FALLBACK_HRA = {
    'X': {'rate': 27, 'min_da_trigger': 50, 'description': '8 metro cities, pop > 50 lakh'},
    'Y': {'rate': 18, 'min_da_trigger': 50, 'description': '97 cities, pop 5–50 lakh'},
    'Z': {'rate': 9,  'min_da_trigger': 50, 'description': 'All other cities'},
    'source': 'hardcoded',
    'as_of': '2017-07-07',
    'effective_from': 'July 2017 (DA-linked, active when DA >= 50%)',
    'note': (
        'Per MoF OM F.No.2/5/2017-E.II(B) dt 07-Jul-2017: HRA rates step up '
        'to 27/18/9% once DA crosses 50%. DA is currently 55% (Jan 2025), '
        'so higher HRA slab is in effect.'
    ),
}

# Income Tax — New Regime FY 2025-26 (Budget presented 1 Feb 2025)
# Key change from FY 2024-25: slabs restructured, 87A rebate raised to ₹60,000
# (Effectively zero tax up to ₹12 lakh annual income under new regime)
FALLBACK_TAX_SLABS_NEW_2526 = [
    {'min': 0,        'max': 400000,  'rate': 0,  'label': 'Up to ₹4 lakh'},
    {'min': 400001,   'max': 800000,  'rate': 5,  'label': '₹4L – ₹8L'},
    {'min': 800001,   'max': 1200000, 'rate': 10, 'label': '₹8L – ₹12L'},
    {'min': 1200001,  'max': 1600000, 'rate': 15, 'label': '₹12L – ₹16L'},
    {'min': 1600001,  'max': 2000000, 'rate': 20, 'label': '₹16L – ₹20L'},
    {'min': 2000001,  'max': 2400000, 'rate': 25, 'label': '₹20L – ₹24L'},
    {'min': 2400001,  'max': None,    'rate': 30, 'label': 'Above ₹24L'},
]

FALLBACK_TAX_META_NEW = {
    'fy': '2025-26',
    'ay': '2026-27',
    'regime': 'New Regime (Default from FY 2023-24)',
    'rebate_87a_limit': 1200000,       # income limit for 87A
    'rebate_87a_max': 60000,           # max rebate amount (Budget 2025)
    'cess_rate': 4,                    # Health & Education Cess
    'std_deduction': 75000,            # Standard deduction under new regime (Budget 2024)
    'budget_date': '2025-02-01',
    'source': 'hardcoded',
    'note': (
        'Finance Bill 2025 (Budget 1 Feb 2025). '
        'Section 87A rebate up to ₹60,000 → effective zero tax for income ≤ ₹12L. '
        '4% Health & Education Cess on total tax. '
        'Standard deduction ₹75,000 available under new regime.'
    ),
}

# Old Regime FY 2025-26 (unchanged slabs, deductions via 80C/80D/HRA etc.)
FALLBACK_TAX_SLABS_OLD_2526 = [
    {'min': 0,       'max': 250000,  'rate': 0,  'label': 'Up to ₹2.5 lakh'},
    {'min': 250001,  'max': 500000,  'rate': 5,  'label': '₹2.5L – ₹5L'},
    {'min': 500001,  'max': 1000000, 'rate': 20, 'label': '₹5L – ₹10L'},
    {'min': 1000001, 'max': None,    'rate': 30, 'label': 'Above ₹10L'},
]

FALLBACK_TAX_META_OLD = {
    'fy': '2025-26',
    'ay': '2026-27',
    'regime': 'Old Regime',
    'rebate_87a_limit': 500000,
    'rebate_87a_max': 12500,
    'cess_rate': 4,
    'source': 'hardcoded',
    'note': (
        'Old regime slabs unchanged. Key deductions: 80C (₹1.5L), '
        '80D (₹25K health insurance), HRA, LTA, NPS 80CCD(1B) ₹50K. '
        'Most beneficial when total deductions > ₹3.75L.'
    ),
}

# ═══════════════════════════════════════════════════════════════════════════════
#  FETCH HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _get_soup(url: str) -> BeautifulSoup | None:
    """Fetch URL and return BeautifulSoup object, or None on failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except Exception as exc:
        logger.warning(f"[RateService] Could not fetch {url}: {exc}")
        return None


def _safe_int(text: str, default: int = 0) -> int:
    """Parse first integer from a string."""
    m = re.search(r'\d+', str(text).replace(',', ''))
    return int(m.group()) if m else default


# ═══════════════════════════════════════════════════════════════════════════════
#  DA RATE FETCHERS
# ═══════════════════════════════════════════════════════════════════════════════

def _parse_da_from_7thpay(soup: BeautifulSoup) -> int | None:
    """Parse DA rate from 7thpaycommissionnews.in/da-table/"""
    if not soup:
        return None
    # Look for a table row with current year
    current_year = datetime.now().year
    prev_year = current_year - 1
    # Find all table rows
    for row in soup.find_all('tr'):
        cells = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
        row_text = ' '.join(cells)
        # Look for a row containing the most recent year and a DA% value
        if (str(current_year) in row_text or str(prev_year) in row_text):
            for cell in cells:
                pct = re.search(r'\b(\d{2,3})\b', cell)
                if pct:
                    val = int(pct.group(1))
                    if 40 <= val <= 120:   # sanity: DA is in 40-120% range
                        return val
    return None


def _parse_da_from_bankbazaar(soup: BeautifulSoup) -> int | None:
    """Parse DA rate from BankBazaar DA table."""
    if not soup:
        return None
    # BankBazaar has structured tables with DA rates
    tables = soup.find_all('table')
    current_year = str(datetime.now().year)
    prev_year = str(datetime.now().year - 1)
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
            text = ' '.join(cells)
            if current_year in text or prev_year in text:
                # Look for percentage value
                for cell in cells:
                    m = re.search(r'(\d{2,3})%?', cell)
                    if m:
                        val = int(m.group(1))
                        if 40 <= val <= 120:
                            return val
    return None


def fetch_da_rate() -> dict:
    """
    Fetch current DA rate. Returns dict with rate + metadata.
    Tries multiple reliable sources before falling back.
    """
    sources_tried = []

    # Source 1: 7th Pay Commission news site (most up-to-date for DA)
    url1 = 'https://www.7thpaycommissionnews.in/da-table/'
    sources_tried.append(url1)
    soup1 = _get_soup(url1)
    rate = _parse_da_from_7thpay(soup1)
    if rate:
        logger.info(f"[RateService] DA rate {rate}% fetched from {url1}")
        return {**FALLBACK_DA, 'rate': rate, 'source': url1,
                'as_of': datetime.now().strftime('%Y-%m-%d')}

    # Source 2: BankBazaar DA table
    url2 = 'https://www.bankbazaar.com/tax/dearness-allowance.html'
    sources_tried.append(url2)
    soup2 = _get_soup(url2)
    rate = _parse_da_from_bankbazaar(soup2)
    if rate:
        logger.info(f"[RateService] DA rate {rate}% fetched from {url2}")
        return {**FALLBACK_DA, 'rate': rate, 'source': url2,
                'as_of': datetime.now().strftime('%Y-%m-%d')}

    # Source 3: ClearTax
    url3 = 'https://cleartax.in/s/dearness-allowance'
    sources_tried.append(url3)
    soup3 = _get_soup(url3)
    if soup3:
        # Look for the current DA % in the page text
        text = soup3.get_text()
        # Pattern: "55% DA" or "DA of 55%"
        m = re.search(r'(\d{2,3})\s*%\s*(?:da|dearness\s*allowance)', text, re.IGNORECASE)
        if not m:
            m = re.search(r'(?:da|dearness\s*allowance)[^.]*?(\d{2,3})\s*%', text, re.IGNORECASE)
        if m:
            rate = int(m.group(1))
            if 40 <= rate <= 120:
                return {**FALLBACK_DA, 'rate': rate, 'source': url3,
                        'as_of': datetime.now().strftime('%Y-%m-%d')}

    logger.warning(f"[RateService] All DA sources failed: {sources_tried}. Using fallback.")
    return FALLBACK_DA.copy()


# ═══════════════════════════════════════════════════════════════════════════════
#  HRA RATE FETCHERS
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_hra_rates(current_da_rate: int = 55) -> dict:
    """
    HRA rates are linked to DA rate per 7th CPC OM.
    DA >= 50%: X=27%, Y=18%, Z=9%
    DA 25–49%: X=24%, Y=16%, Z=8%
    DA < 25%:  X=16%, Y=8%,  Z=8%
    Source: Ministry of Finance OM F.No.2/5/2017-E.II(B)
    """
    if current_da_rate >= 50:
        x, y, z = 27, 18, 9
        trigger = 'DA ≥ 50% (current: {}%)'.format(current_da_rate)
    elif current_da_rate >= 25:
        x, y, z = 24, 16, 8
        trigger = 'DA 25–49% (current: {}%)'.format(current_da_rate)
    else:
        x, y, z = 16, 8, 8
        trigger = 'DA < 25% (current: {}%)'.format(current_da_rate)

    result = {
        'X': {'rate': x, 'description': '8 metro cities, pop > 50 lakh'},
        'Y': {'rate': y, 'description': '97 cities, pop 5–50 lakh'},
        'Z': {'rate': z, 'description': 'All other cities'},
        'source': 'MoF OM F.No.2/5/2017-E.II(B) (DA-linked formula)',
        'as_of': '2017-07-07',
        'effective_from': trigger,
        'note': (
            f'HRA computed from DA. Since DA = {current_da_rate}%, '
            f'the {trigger} slab applies. '
            'Source: 7th CPC OM, Ministry of Finance.'
        ),
    }
    return result


# ═══════════════════════════════════════════════════════════════════════════════
#  INCOME TAX SLAB FETCHERS
# ═══════════════════════════════════════════════════════════════════════════════

def _parse_tax_slabs_from_cleartax(soup: BeautifulSoup) -> list | None:
    """Try to parse new regime tax slabs from ClearTax."""
    if not soup:
        return None
    try:
        text = soup.get_text()
        # Look for slab patterns like "4 lakh to 8 lakh" "5%"
        # This is heuristic — adjust if ClearTax changes layout
        slabs = []
        # Pattern: ₹X lakh to ₹Y lakh → Z%
        pattern = r'(?:₹|Rs\.?)\s*([\d.]+)\s*[Ll]akh?\s*(?:to|–|-)\s*(?:₹|Rs\.?)?\s*([\d.]+)\s*[Ll]akh?\D{0,10}?(\d{1,2})\s*%'
        matches = re.findall(pattern, text)
        if len(matches) >= 4:
            for mn, mx, rate in matches:
                slabs.append({
                    'min': int(float(mn) * 100000),
                    'max': int(float(mx) * 100000),
                    'rate': int(rate),
                    'label': f'₹{mn}L – ₹{mx}L',
                })
            return slabs
    except Exception as exc:
        logger.warning(f"[RateService] Tax slab parse error: {exc}")
    return None


def fetch_income_tax_slabs() -> dict:
    """
    Fetch income tax slabs for the current FY.
    Returns dict with new_regime and old_regime slabs + metadata.
    """
    # Source 1: ClearTax (comprehensive, well-structured)
    url1 = 'https://cleartax.in/s/income-tax-slabs'
    soup1 = _get_soup(url1)
    new_slabs = _parse_tax_slabs_from_cleartax(soup1)

    if new_slabs and len(new_slabs) >= 4:
        logger.info(f"[RateService] Tax slabs parsed from {url1}")
        meta = {**FALLBACK_TAX_META_NEW, 'source': url1,
                'as_of': datetime.now().strftime('%Y-%m-%d')}
        return {
            'new_regime': {'slabs': new_slabs, 'meta': meta},
            'old_regime': {'slabs': FALLBACK_TAX_SLABS_OLD_2526,
                           'meta': FALLBACK_TAX_META_OLD},
        }

    # Fallback to verified Budget 2025 values
    logger.info("[RateService] Using hardcoded Budget 2025 tax slabs.")
    return {
        'new_regime': {
            'slabs': FALLBACK_TAX_SLABS_NEW_2526,
            'meta': FALLBACK_TAX_META_NEW,
        },
        'old_regime': {
            'slabs': FALLBACK_TAX_SLABS_OLD_2526,
            'meta': FALLBACK_TAX_META_OLD,
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  TAX CALCULATOR (using live slabs)
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_tax(annual_income: float, slabs: list, meta: dict) -> dict:
    """
    Calculate income tax given a slab list + metadata.
    Handles 87A rebate and 4% cess.
    """
    income = float(annual_income)

    # Apply standard deduction if new regime
    if meta.get('std_deduction') and meta.get('regime', '').lower().startswith('new'):
        taxable = max(0, income - meta['std_deduction'])
    else:
        taxable = income

    tax = 0.0
    breakdown = []
    prev_limit = 0

    for slab in slabs:
        if taxable <= prev_limit:
            break
        upper = slab['max'] if slab['max'] else taxable
        taxable_in_slab = min(taxable, upper) - prev_limit
        if taxable_in_slab > 0 and slab['rate'] > 0:
            slab_tax = taxable_in_slab * slab['rate'] / 100
            breakdown.append({
                'label': slab['label'],
                'rate': slab['rate'],
                'taxable': round(taxable_in_slab, 2),
                'tax': round(slab_tax, 2),
            })
            tax += slab_tax
        prev_limit = upper

    # Section 87A Rebate
    rebate_87a = 0.0
    rebate_limit = meta.get('rebate_87a_limit', 500000)
    rebate_max = meta.get('rebate_87a_max', 12500)
    if income <= rebate_limit and tax <= rebate_max:
        rebate_87a = tax
        tax = 0.0
    elif income <= rebate_limit:
        rebate_87a = min(tax, rebate_max)
        tax = max(0, tax - rebate_87a)

    # 4% Health & Education Cess
    cess_rate = meta.get('cess_rate', 4)
    cess = tax * cess_rate / 100
    total_tax = tax + cess

    return {
        'annual_income': round(income, 2),
        'taxable_income': round(taxable, 2),
        'std_deduction': meta.get('std_deduction', 0),
        'annual_tax': round(total_tax, 2),
        'monthly_tax': round(total_tax / 12, 2),
        'effective_rate': round((total_tax / income * 100) if income > 0 else 0, 2),
        'cess': round(cess, 2),
        'cess_rate': cess_rate,
        'rebate_87a': round(rebate_87a, 2),
        'rebate_87a_limit': rebate_limit,
        'breakdown': breakdown,
        'regime': meta.get('regime', ''),
        'fy': meta.get('fy', ''),
        'source': meta.get('source', 'hardcoded'),
        'note': meta.get('note', ''),
        'budget_date': meta.get('budget_date', ''),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT — Used by views.py
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_rates(force_refresh: bool = False) -> dict:
    """
    Get all current rates. Uses DB cache when available and fresh.
    Returns dict with da, hra, tax_slabs keys.
    """
    from .models import RateCache  # import here to avoid circular

    cache_key = 'india_govt_rates'
    cache_obj = None

    if not force_refresh:
        try:
            cache_obj = RateCache.objects.filter(key=cache_key).first()
            if cache_obj:
                age = timezone.now() - cache_obj.fetched_at
                if age.days < CACHE_TTL_DAYS:
                    data = cache_obj.data
                    logger.debug("[RateService] Using DB cached rates.")
                    return data
        except Exception as e:
            logger.warning(f"[RateService] Cache read error: {e}")

    # ── Fetch fresh data ─────────────────────────────────────────────────────
    logger.info("[RateService] Fetching fresh rates from online sources...")
    da_data = fetch_da_rate()
    hra_data = fetch_hra_rates(current_da_rate=da_data['rate'])
    tax_data = fetch_income_tax_slabs()

    result = {
        'da': da_data,
        'hra': hra_data,
        'tax': tax_data,
        'fetched_at': timezone.now().isoformat(),
        'cache_ttl_days': CACHE_TTL_DAYS,
    }

    # ── Store to DB cache ────────────────────────────────────────────────────
    try:
        RateCache.objects.update_or_create(
            key=cache_key,
            defaults={'data': result, 'fetched_at': timezone.now()},
        )
        logger.info("[RateService] Rates saved to DB cache.")
    except Exception as e:
        logger.warning(f"[RateService] Cache write error: {e}")

    return result
