from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard, name='dashboard'),

    # Auth
    path('signup/', views.signup_view, name='signup'),

    # Profile
    path('profile/edit/', views.profile_setup_view, name='profile_setup'),

    # Settings (theme, language)
    path('settings/', views.settings_view, name='settings'),

    # Goal operations
    path('goal/create/', views.goal_view, name='create_goal'),
    path('goal/<int:goal_id>/update/', views.update_goal_progress, name='update_goal_progress'),
    path('goal/<int:goal_id>/edit/', views.edit_goal, name='edit_goal'),
    path('goal/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),

    # API
    path('api/city/', views.city_autocomplete, name='city_autocomplete'),

    # Rate refresh (force-fetch from online sources)
    path('rates/refresh/', views.refresh_rates_view, name='refresh_rates'),
]
