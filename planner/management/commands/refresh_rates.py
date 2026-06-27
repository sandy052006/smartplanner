"""
Management command: refresh_rates
-----------------------------------
Fetches the latest Indian government financial rates from online sources
and updates the DB cache.

Usage:
    python manage.py refresh_rates              # fetch fresh from web
    python manage.py refresh_rates --force      # force even if cache is fresh
    python manage.py refresh_rates --show       # just show current cached rates
    python manage.py refresh_rates --info       # show rate details + sources

Schedule this command via Windows Task Scheduler or cron for auto-refresh:
    # Windows Task Scheduler: run weekly
    # Linux cron: 0 6 1 * * /path/venv/bin/python manage.py refresh_rates

"""

import json
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fetch latest DA, HRA, and Income Tax rates from government sources and update the DB cache.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true',
                            help='Force refresh even if cache is still fresh')
        parser.add_argument('--show', action='store_true',
                            help='Show current cached rates without fetching')
        parser.add_argument('--info', action='store_true',
                            help='Show detailed rate info with sources')

    def handle(self, *args, **options):
        from planner.models import RateCache
        from planner.rate_service import get_all_rates, CACHE_TTL_DAYS

        if options['show'] or options['info']:
            self._show_cached(options['info'])
            return

        self.stdout.write(self.style.HTTP_INFO('\n[*] SmartPlanner Rate Refresh'))
        self.stdout.write('=' * 55)

        # Check existing cache age
        cache_obj = RateCache.objects.filter(key='india_govt_rates').first()
        if cache_obj and not options['force']:
            age_d = cache_obj.age_hours() / 24
            if age_d < CACHE_TTL_DAYS:
                self.stdout.write(
                    self.style.WARNING(
                        f'  Cache is only {age_d:.1f} days old (TTL={CACHE_TTL_DAYS}d). '
                        f'Skipping. Use --force to override.'
                    )
                )
                return

        self.stdout.write('  Fetching from online sources...')
        try:
            rates = get_all_rates(force_refresh=True)
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'  [!] Fetch failed: {exc}'))
            return

        # Report results
        da = rates.get('da', {})
        hra = rates.get('hra', {})
        tax = rates.get('tax', {})

        self.stdout.write(self.style.SUCCESS('\n  [OK] Rates updated successfully!\n'))

        self.stdout.write(f"  {'DA Rate':<30} {da.get('rate')}%  (from: {da.get('effective_from')})")
        self.stdout.write(f"  {'   Source':<30} {da.get('source')}")
        self.stdout.write('')
        self.stdout.write(f"  {'HRA - X Cities':<30} {hra.get('X', {}).get('rate')}%")
        self.stdout.write(f"  {'HRA - Y Cities':<30} {hra.get('Y', {}).get('rate')}%")
        self.stdout.write(f"  {'HRA - Z Cities':<30} {hra.get('Z', {}).get('rate')}%")
        self.stdout.write(f"  {'   Source':<30} {hra.get('source')}")
        self.stdout.write('')

        new_meta = tax.get('new_regime', {}).get('meta', {})
        old_meta = tax.get('old_regime', {}).get('meta', {})
        new_slabs = tax.get('new_regime', {}).get('slabs', [])
        self.stdout.write(f"  {'Tax FY':<30} {new_meta.get('fy')} (AY {new_meta.get('ay')})")
        self.stdout.write(f"  {'   New Regime Slabs':<30} {len(new_slabs)} slabs")
        self.stdout.write(f"  {'   87A Rebate Limit':<30} Rs.{new_meta.get('rebate_87a_limit', 0):,}")
        self.stdout.write(f"  {'   87A Max Rebate':<30} Rs.{new_meta.get('rebate_87a_max', 0):,}")
        self.stdout.write(f"  {'   Std Deduction':<30} Rs.{new_meta.get('std_deduction', 0):,}")
        self.stdout.write(f"  {'   Cess':<30} {new_meta.get('cess_rate')}%")
        self.stdout.write(f"  {'   Source':<30} {new_meta.get('source')}")
        self.stdout.write('')
        self.stdout.write(f"  Fetched at: {rates.get('fetched_at')}")
        self.stdout.write('=' * 55 + '\n')

    def _show_cached(self, detailed: bool):
        from planner.models import RateCache
        cache_obj = RateCache.objects.filter(key='india_govt_rates').first()
        if not cache_obj:
            self.stdout.write(self.style.WARNING('  No cached rates found. Run: python manage.py refresh_rates'))
            return

        data = cache_obj.data
        age_d = cache_obj.age_hours() / 24
        self.stdout.write(f'\nCached Rates  (age: {age_d:.1f} days, fetched: {cache_obj.fetched_at:%Y-%m-%d %H:%M})')
        self.stdout.write('=' * 60)

        if detailed:
            self.stdout.write(json.dumps(data, indent=2, default=str))
        else:
            da = data.get('da', {})
            hra = data.get('hra', {})
            tax = data.get('tax', {})
            self.stdout.write(f"  DA Rate:   {da.get('rate')}%  ({da.get('source')})")
            self.stdout.write(f"  HRA X/Y/Z: {hra.get('X', {}).get('rate')}% / {hra.get('Y', {}).get('rate')}% / {hra.get('Z', {}).get('rate')}%")
            new_meta = tax.get('new_regime', {}).get('meta', {})
            self.stdout.write(f"  Tax FY:    {new_meta.get('fy')}  ({new_meta.get('source')})")
        self.stdout.write('')
