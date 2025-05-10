from django.urls import path
from . import views

app_name = 'mapapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/pins/', views.get_pins, name='get_pins'),
    path('api/pins/create/', views.create_pin, name='create_pin'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]