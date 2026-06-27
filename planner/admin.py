from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Goal, RateCache


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'income', 'lifestyle', 'theme', 'language', 'created_at')
    search_fields = ('user__username', 'city')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'target_amount', 'current_amount', 'target_date', 'is_achieved')
    list_filter = ('is_achieved',)


@admin.register(RateCache)
class RateCacheAdmin(admin.ModelAdmin):
    list_display = ('key', 'fetched_at', 'age_display', 'fetch_ok', 'refresh_action')
    readonly_fields = ('fetched_at', 'age_display', 'data_pretty')
    actions = ['force_refresh']

    @admin.display(description='Age')
    def age_display(self, obj):
        h = obj.age_hours()
        if h < 1:
            return f"{int(h * 60)} min ago"
        elif h < 24:
            return f"{int(h)} hrs ago"
        else:
            return f"{int(h / 24)} days ago"

    @admin.display(description='Refresh')
    def refresh_action(self, obj):
        return format_html(
            '<a class="button" href="/admin/planner/ratecache/{}/refresh/" '
            'style="padding:4px 10px;background:#6366f1;color:white;border-radius:4px;'
            'text-decoration:none;font-size:12px;">🔄 Refresh Now</a>',
            obj.pk
        )

    @admin.display(description='Data (JSON)')
    def data_pretty(self, obj):
        import json
        formatted = json.dumps(obj.data, indent=2)
        return format_html('<pre style="font-size:11px;max-height:400px;overflow:auto;">{}</pre>', formatted)

    @admin.action(description='Force refresh selected rates from online sources')
    def force_refresh(self, request, queryset):
        from .rate_service import get_all_rates
        get_all_rates(force_refresh=True)
        self.message_user(request, "✅ Rates refreshed from online sources.")
