from django.urls import path

from . import views

app_name = 'openai_example'

urlpatterns = [
    path('', views.home, name='openai_home'),
    path('chat/', views.chat_demo, name='chat_demo'),
    path('images/', views.image_demo, name='image_demo'),
]
