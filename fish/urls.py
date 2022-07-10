from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='register'),

    path('room/<str:pk>/', views.room_page, name='room_page'),
    path('create-room/', views.room_form, name='room_form'),
    path('profile/<str:pk>', views.profile_page, name='profile_page'),

    path('messages-component', views.message_component, name='message_component'),
    path('rooms-component', views.rooms_component, name='rooms_component'),
    path('topic-component', views.topics_component, name='topic_component'),
]