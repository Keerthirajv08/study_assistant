from django.urls import path
from . import views

urlpatterns = [
    #Home and main pages
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),

    #User authentication and registration
    path('signup/', views.signup_view, name='signup'),

    #Chat functionality
    path('chat/', views.new_chat, name='new_chat'),
    path('chat/<int:session_id>/', views.chat_view, name='chat_view'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    path('chat/history/', views.chat_history, name='chat_history'),

    #Study features
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('topics/', views.study_topics_view, name='study_topics'),
    path('api/study-tips/', views.get_study_tips, name='get_study_tips'), 
]


