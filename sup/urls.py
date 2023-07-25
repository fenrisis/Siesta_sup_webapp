from django.urls import path
from . import views

app_name = 'sup'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('rent/', views.rent_sups, name='rent_sups'),
]