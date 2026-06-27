from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal

# A simple Profile to store user's location, income and chosen strategy
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # link to Django user
    city = models.CharField(max_length=100, blank=True)      # city for cost adjustment
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # monthly income
    job = models.CharField(max_length=100, blank=True)
    LIFESTYLE_CHOICES = [
        ('extreme', 'Extreme Saver'),
        ('moderate', 'Moderate Planner'),
        ('comfortable', 'Comfortable Saver'),
    ]
    lifestyle = models.CharField(max_length=20, choices=LIFESTYLE_CHOICES, default='moderate')
    created_at = models.DateTimeField(auto_now_add=True)

    # Theme & Language preferences
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('custom', 'Custom'),
    ]
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')

    LANGUAGE_CHOICES = [
        # Indian Languages
        ('en', 'English'),
        ('hi', 'हिन्दी (Hindi)'),
        ('bn', 'বাংলা (Bengali)'),
        ('te', 'తెలుగు (Telugu)'),
        ('mr', 'मराठी (Marathi)'),
        ('ta', 'தமிழ் (Tamil)'),
        ('gu', 'ગુજરાતી (Gujarati)'),
        ('kn', 'ಕನ್ನಡ (Kannada)'),
        ('ml', 'മലയാളം (Malayalam)'),
        ('pa', 'ਪੰਜਾਬੀ (Punjabi)'),
        ('or', 'ଓଡ଼ିଆ (Odia)'),
        # Foreign Languages
        ('es', 'Español (Spanish)'),
        ('fr', 'Français (French)'),
        ('de', 'Deutsch (German)'),
        ('ja', '日本語 (Japanese)'),
        ('zh', '中文 (Chinese)'),
        ('ar', 'العربية (Arabic)'),
        ('pt', 'Português (Portuguese)'),
        ('ru', 'Русский (Russian)'),
        ('ko', '한국어 (Korean)'),
        ('it', 'Italiano (Italian)'),
    ]
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')

    # Custom theme colors
    custom_primary = models.CharField(max_length=7, default='#6366f1')   # hex color
    custom_bg = models.CharField(max_length=7, default='#0f172a')        # hex color
    custom_surface = models.CharField(max_length=7, default='#1e293b')   # hex color
    custom_text = models.CharField(max_length=7, default='#f8fafc')      # hex color
    custom_accent = models.CharField(max_length=7, default='#10b981')    # hex color

    def __str__(self):
        return f"{self.user.username} Profile"

# Goal model - lets users create savings goals
class Goal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='goals')  # owner
    title = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)  # target rupees
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # saved so far
    target_date = models.DateField()  # when they want to reach it
    is_achieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percent(self):
        # returns progress as integer percent
        if self.target_amount <= 0:
            return 0
        return min(100, int((self.current_amount / self.target_amount) * 100))

    def months_until_target(self):
        # quick month difference (at least 1)
        today = timezone.now().date()
        months = (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month)
        return max(1, months)

    def monthly_needed(self):
        # how much to save each month to hit goal (using Decimal for precision)
        months = self.months_until_target()
        remaining = max(Decimal('0'), self.target_amount - self.current_amount)
        if months > 0:
            return (remaining / Decimal(months)).quantize(Decimal('0.01'))
        return remaining

    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"


class RateCache(models.Model):
    """
    Caches fetched government rates (DA, HRA, Income Tax slabs) to avoid
    hammering external sources on every request. Refreshed every 30 days
    (or on demand via 'python manage.py refresh_rates').
    """
    key = models.CharField(max_length=100, unique=True)  # e.g. 'india_govt_rates'
    data = models.JSONField(default=dict)                 # full rate payload
    fetched_at = models.DateTimeField(auto_now_add=True)  # when last fetched
    source_url = models.CharField(max_length=500, blank=True)  # primary source used
    fetch_ok = models.BooleanField(default=True)          # was last fetch successful?

    class Meta:
        verbose_name = 'Rate Cache'
        verbose_name_plural = 'Rate Caches'

    def __str__(self):
        return f"{self.key} (fetched {self.fetched_at:%Y-%m-%d %H:%M})"

    def age_hours(self):
        delta = timezone.now() - self.fetched_at
        return delta.total_seconds() / 3600

    def is_stale(self, ttl_days: int = 30) -> bool:
        return self.age_hours() > (ttl_days * 24)


# --- Django Signals ---
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
