from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # ... other url patterns ...
    path('get-random-textcontent/', views.get_random_textcontent, name='get_random_textcontent'),
    path('track-textcontent-click/', views.track_textcontent_click, name='track_textcontent_click'),
    path('get-user-textcontents/', views.get_user_textcontents, name='get_user_textcontents'),
    path('ask-ai-about-story/', views.ask_ai_about_story, name='ask_ai_about_story'),
    path('question-handle/', views.question_handle, name='question_handle'),
    path('get_question/', views.get_question, name='get_question'),
]
