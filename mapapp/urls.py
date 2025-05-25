from django.urls import path
from . import views

app_name = 'mapapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/pins/', views.get_pins, name='get_pins'),
    path('api/pins/create/', views.create_pin, name='create_pin'),
    path('api/pins/<int:pin_id>/reviews/', views.get_reviews, name='get_reviews'),
    path('api/pins/<int:pin_id>/reviews/create/', views.create_review, name='create_review'),
    path('api/pins/<int:pin_id>/delete/', views.delete_pin, name='delete_pin'),
    path('api/pins/<int:pin_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('api/favorites/', views.get_favorites, name='get_favorites'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/', views.my_profile, name='my_profile'),
    # Messaging URLs
    path('messages/', views.inbox_view, name='inbox'),
    path('messages/conversation/<int:conversation_id>/', views.conversation_view, name='conversation'),
    path('messages/conversation/new/<str:username>/', views.conversation_view, name='new_conversation'),
    path('messages/conversation/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('messages/conversation/<int:conversation_id>/new-messages/', views.get_new_messages, name='get_new_messages'),
    path('messages/unread-count/', views.get_unread_count, name='unread_message_count'),
]