import json
import urllib.request
import urllib.error
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .forms import SignUpForm, ProfileForm, GoalForm, SettingsForm
from .models import Profile, Goal
from .city_data import (
    get_city_data,
    ALL_INDIAN_CITY_NAMES, ALL_FOREIGN_CITY_NAMES,
)
from .rate_service import get_all_rates, calculate_tax
from decimal import Decimal, InvalidOperation
from datetime import date


def fetch_weather(city_name: str) -> dict:
    """Fetch weather from wttr.in (free, no API key needed)."""
    try:
        url = f"https://wttr.in/{urllib.request.quote(city_name)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'SmartPlanner/1.0'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            current = data['current_condition'][0]
            weather = data['weather'][0]

            temp_c = int(current['temp_C'])
            feels_like = int(current['FeelsLikeC'])
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_kmph = current['windspeedKmph']
            max_temp = int(weather['maxtempC'])
            min_temp = int(weather['mintempC'])

            # Map weather code to emoji
            wcode = int(current.get('weatherCode', 113))
            emoji = '☀️'
            if wcode in [395, 392, 389, 386]: emoji = '⛈️'
            elif wcode in [377, 374, 371, 368, 365, 362, 338, 335, 332, 329, 326, 323, 320, 317, 314, 311, 308, 305, 302, 299, 296, 293]: emoji = '🌧️'
            elif wcode in [260, 248]: emoji = '🌫️'
            elif wcode in [230, 227]: emoji = '❄️'
            elif wcode in [182, 179, 176]: emoji = '🌨️'
            elif wcode in [143]: emoji = '🌁'
            elif wcode in [119, 122]: emoji = '☁️'
            elif wcode in [116]: emoji = '⛅'

            return {
                'success': True,
                'temp_c': temp_c,
                'feels_like': feels_like,
                'desc': desc,
                'humidity': humidity,
                'wind_kmph': wind_kmph,
                'max_temp': max_temp,
                'min_temp': min_temp,
                'emoji': emoji,
            }
    except Exception:
        return {'success': False}


def get_city_image_url(city_data_entry: dict, city_name: str) -> str:
    """Generate Unsplash image URL for the city."""
    if city_data_entry and city_data_entry.get('search_term'):
        term = city_data_entry['search_term'].replace(' ', ',').replace(',,', ',')
    else:
        term = f"{city_name},city,skyline"
    return f"https://source.unsplash.com/1200x500/?{term}"


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Let's set up your profile to get started.")
            return redirect('planner:profile_setup')
    else:
        form = SignUpForm()
    return render(request, 'planner/signup.html', {'form': form})


@login_required
def dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    income = profile.income or Decimal('0')
    city_raw = profile.city.strip() if profile.city else ''

    # ── Lookup city data ────────────────────────────────────────
    city_lookup = get_city_data(city_raw) if city_raw else {'type': 'unknown', 'data': None}
    city_info = city_lookup['data']
    city_type = city_lookup['type']  # 'indian', 'foreign', 'unknown'

    # ── Weather ─────────────────────────────────────────────────
    weather = {}
    city_image_url = ''
    if city_raw:
        weather = fetch_weather(city_raw)
        city_image_url = get_city_image_url(city_info, city_raw)

    # ── Budget Calculations ──────────────────────────────────────
    if city_type == 'indian' and city_info:
        cost_index = city_info['cost_index']
        city_category = city_info['category']
        hra_percent = city_info['hra_percent']
        currency_symbol = '₹'

        # Government-aligned cost allocation
        base_need_pct = Decimal('0.50')
        adjusted_need_pct = min(base_need_pct * cost_index, Decimal('0.70'))

    elif city_type == 'foreign' and city_info:
        cost_index = city_info['cost_index']
        city_category = 'INT'
        hra_percent = 0
        currency_symbol = city_info.get('currency_symbol', '$')

        base_need_pct = Decimal('0.50')
        adjusted_need_pct = min(base_need_pct * cost_index / Decimal('2'), Decimal('0.70'))

    else:
        cost_index = Decimal('1.0')
        city_category = 'Z'
        hra_percent = 9
        currency_symbol = '₹'
        adjusted_need_pct = Decimal('0.50')

    if profile.lifestyle == 'extreme':
        save_pct, want_pct = Decimal('0.40'), Decimal('0.10')
    elif profile.lifestyle == 'comfortable':
        save_pct, want_pct = Decimal('0.15'), Decimal('0.35')
    else:  # moderate
        save_pct, want_pct = Decimal('0.25'), Decimal('0.25')

    remaining_pct = Decimal('1.0') - adjusted_need_pct
    total_want_save = want_pct + save_pct
    final_want_pct = (want_pct / total_want_save) * remaining_pct if total_want_save > 0 else Decimal('0')
    final_save_pct = (save_pct / total_want_save) * remaining_pct if total_want_save > 0 else Decimal('0')

    allocations = {
        'needs': (income * adjusted_need_pct).quantize(Decimal('0.01')),
        'wants': (income * final_want_pct).quantize(Decimal('0.01')),
        'savings': (income * final_save_pct).quantize(Decimal('0.01')),
        'income': income,
        'currency': currency_symbol,
    }
    chart_data = {
        'labels': ["Needs", "Wants", "Savings"],
        'data': [float(allocations['needs']), float(allocations['wants']), float(allocations['savings'])],
    }

    # ── LIVE RATES (DA, HRA, Tax Slabs) from rate_service ────────
    # Reads from DB cache (30-day TTL) or fetches fresh from online sources
    live_rates = get_all_rates(force_refresh=False)
    live_da     = live_rates.get('da', {})
    live_hra    = live_rates.get('hra', {})
    live_tax    = live_rates.get('tax', {})
    rates_fetched_at = live_rates.get('fetched_at', '')

    # Use live HRA for the user's city category
    if city_category in ('X', 'Y', 'Z'):
        hra_percent = live_hra.get(city_category, {}).get('rate', hra_percent)
    live_da_rate = live_da.get('rate', 55)

    # ── Income Tax (Indian cities or unknown) ────────────────────
    tax_info = {}
    new_regime_slabs = live_tax.get('new_regime', {}).get('slabs', [])
    new_regime_meta  = live_tax.get('new_regime', {}).get('meta', {})
    old_regime_slabs = live_tax.get('old_regime', {}).get('slabs', [])
    old_regime_meta  = live_tax.get('old_regime', {}).get('meta', {})

    if (city_type == 'indian' or city_type == 'unknown') and income > 0:
        annual_income = float(income) * 12
        tax_info = calculate_tax(annual_income, new_regime_slabs, new_regime_meta)
        tax_info['da_percent'] = live_da_rate
        tax_info['hra_category'] = city_category
        tax_info['hra_percent'] = hra_percent

        # Find which slab the user's TAXABLE income currently falls in
        taxable = max(0, annual_income - new_regime_meta.get('std_deduction', 0))
        current_slab = None
        for slab in new_regime_slabs:
            lo = slab.get('min', 0)
            hi = slab.get('max')          # None means no upper bound
            if hi is None:
                if taxable > lo:
                    current_slab = slab
                    break
            elif lo <= taxable <= hi:
                current_slab = slab
                break
        # If taxable is 0 (zero income after deduction), show the nil slab
        if current_slab is None and new_regime_slabs:
            current_slab = new_regime_slabs[0]
        tax_info['current_slab'] = current_slab
    else:
        tax_info['current_slab'] = None

    # ── Goals ───────────────────────────────────────────────────
    goals = profile.goals.all().order_by('-created_at')
    goals_with_suggestions = []
    for goal in goals:
        days_left = (goal.target_date - date.today()).days
        time_to_goal_years = days_left / 365.25
        if time_to_goal_years > 5:
            suggestion = (
                "Long-term goal: Consider Equity Mutual Funds or Nifty 50 Index ETFs "
                "for inflation-beating returns (~12% CAGR historically)."
            )
        elif time_to_goal_years > 2:
            suggestion = (
                "Mid-term goal: Hybrid Funds or Corporate Bond Funds offer a good "
                "risk-return balance (~8-10% returns)."
            )
        elif time_to_goal_years > 0.5:
            suggestion = (
                "Short-term goal: Liquid Funds or Fixed Deposits in a high-yield savings "
                "account keep your money safe and accessible (~6-7%)."
            )
        else:
            suggestion = (
                "Upcoming goal: Keep funds liquid in a savings account — "
                "don't take any market risk at this stage."
            )
        goals_with_suggestions.append({'goal': goal, 'suggestion': suggestion})

    # ── Personalized Tips (DA/HRA-aware) ────────────────────────
    tips = []
    if profile.lifestyle == 'extreme':
        tips.append(f"Automate 40% of your salary to savings on payday — 'out of sight, out of mind'.")
        tips.append("Challenge yourself with a 'no-spend week' every month to accelerate goals.")
        tips.append(f"Claim HRA exemption ({hra_percent}% of basic pay for your city class) to cut tax.")
    elif profile.lifestyle == 'comfortable':
        tips.append("Use 'Pay Yourself First' — save first, spend the rest.")
        tips.append("Cancel unused subscriptions. Even ₹500/month saves ₹6,000 a year.")
        tips.append("Consider NPS for additional 80CCD(1B) deduction of ₹50,000 (old regime).")
    else:  # moderate
        tips.append("Review your 'wants' spend monthly. Redirect even 5% more to savings.")
        tips.append("The 30-day rule: wait 30 days before any non-essential purchase.")
        tips.append(f"Budget 2025: No tax up to ₹12L under new regime. Check if switching regime saves you more.")

    # Add DA-specific tip if applicable
    if city_type == 'indian':
        tips.append(
            f"DA is currently {live_da_rate}% ({live_da.get('effective_from', '')}). "
            f"For central govt employees this raises your effective income — plan accordingly."
        )

    context = {
        'profile': profile,
        'allocations': allocations,
        'chart_data': chart_data,
        'goals_with_suggestions': goals_with_suggestions,
        'personalized_tips': tips,
        'has_goals': goals.exists(),
        # City data
        'city_info': city_info,
        'city_type': city_type,
        'city_category': city_category,
        'city_image_url': city_image_url,
        'weather': weather,
        # Live rate data
        'tax_info': tax_info,
        'hra_percent': hra_percent,
        'live_da': live_da,
        'live_hra': live_hra,
        'live_tax_meta': new_regime_meta,
        'new_regime_slabs': new_regime_slabs,
        'old_regime_slabs': old_regime_slabs,
        'old_regime_meta': old_regime_meta,
        'rates_fetched_at': rates_fetched_at,
        # City search lists
        'indian_cities': ALL_INDIAN_CITY_NAMES,
        'foreign_cities': ALL_FOREIGN_CITY_NAMES,
    }
    return render(request, 'planner/dashboard.html', context)


@login_required
def refresh_rates_view(request):
    """Force-refresh government rates from online sources (available to any logged-in user)."""
    if request.method == 'POST':
        try:
            rates = get_all_rates(force_refresh=True)
            da = rates.get('da', {})
            messages.success(
                request,
                f"✅ Rates refreshed! DA: {da.get('rate')}% "
                f"({da.get('effective_from')}). "
                f"Tax slabs: FY {rates.get('tax', {}).get('new_regime', {}).get('meta', {}).get('fy', '?')}. "
                f"Source: {da.get('source', 'online')}."
            )
        except Exception as e:
            messages.error(request, f"❌ Could not refresh rates: {e}. Using cached data.")
    return redirect('planner:dashboard')


@login_required
def profile_setup_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('planner:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'planner/profile_form.html', {
        'form': form,
        'indian_cities': ALL_INDIAN_CITY_NAMES,
        'foreign_cities': ALL_FOREIGN_CITY_NAMES,
    })


@login_required
def settings_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('planner:settings')
    else:
        form = SettingsForm(instance=profile)
    return render(request, 'planner/settings.html', {'form': form, 'profile': profile})


@login_required
def goal_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.profile = profile
            goal.save()
            messages.success(request, f"Your new goal '{goal.title}' has been added successfully!")
            return redirect('planner:dashboard')
    else:
        form = GoalForm()
    return render(request, 'planner/goal_form.html', {'form': form})


@login_required
def edit_goal(request, goal_id):
    try:
        goal = Goal.objects.get(id=goal_id, profile=request.user.profile)
    except Goal.DoesNotExist:
        messages.error(request, "Goal not found or you don't have permission to edit it.")
        return redirect('planner:dashboard')

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your goal '{goal.title}' has been updated successfully.")
            return redirect('planner:dashboard')
        # form.errors will be shown in template
    else:
        form = GoalForm(instance=goal)

    # Pass the date as ISO string for the HTML date input
    goal_date_str = goal.target_date.strftime('%Y-%m-%d') if goal.target_date else ''
    return render(request, 'planner/goal_form.html', {
        'form': form,
        'edit_mode': True,
        'goal_date_str': goal_date_str,
        'goal': goal,
    })


@login_required
def delete_goal(request, goal_id):
    if request.method == 'POST':
        try:
            goal = Goal.objects.get(id=goal_id, profile=request.user.profile)
            goal_title = goal.title
            goal.delete()
            messages.success(request, f"✅ Goal '{goal_title}' has been deleted.")
        except Goal.DoesNotExist:
            # Already deleted or doesn't belong to this user — just redirect silently
            messages.info(request, "Goal was already removed.")
    return redirect('planner:dashboard')


@login_required
def update_goal_progress(request, goal_id):
    if request.method == 'POST':
        try:
            goal = Goal.objects.get(id=goal_id, profile=request.user.profile)
        except Goal.DoesNotExist:
            messages.error(request, "Goal not found.")
            return redirect('planner:dashboard')

        try:
            added_amount = Decimal(request.POST.get('add_amount', '0'))
        except InvalidOperation:
            added_amount = Decimal('0')

        if added_amount > 0:
            goal.current_amount += added_amount
            if goal.current_amount >= goal.target_amount:
                goal.is_achieved = True
                messages.success(request, f"🎉 Goal '{goal.title}' has been achieved! Congratulations!")
            else:
                messages.success(request, f"₹{added_amount} added to '{goal.title}'. Keep going!")
            goal.save()
        else:
            messages.error(request, "Please enter a valid amount greater than 0.")
    return redirect('planner:dashboard')


def city_autocomplete(request):
    """AJAX endpoint for city name suggestions."""
    query = request.GET.get('q', '').lower()
    results = []
    if len(query) >= 2:
        for name in ALL_INDIAN_CITY_NAMES:
            if query in name.lower():
                results.append({'name': name, 'type': 'Indian'})
        for name in ALL_FOREIGN_CITY_NAMES:
            if query in name.lower():
                results.append({'name': name, 'type': 'International'})
    return JsonResponse({'cities': results[:10]})
