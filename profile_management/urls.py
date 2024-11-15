from django.urls import path
from . import views

app_name = 'profile_management'  # Define a namespace for this app

urlpatterns = [
    path('ai/', views.ai, name='ai'),
    path("members/", views.members, name="members"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("connect/<str:username>/", views.connect, name="connect"),
    path("disconnect/<str:username>/", views.disconnect, name="disconnect"),
    path('<str:username>/', views.profile, name='profile'),
]
