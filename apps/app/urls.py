from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # ... other url patterns ...
    path('get-random-textcontent/', views.get_random_textcontent, name='get_random_textcontent'),
    path('track-textcontent-click/', views.track_textcontent_click, name='track_textcontent_click'),
    path('get-user-textcontents/', views.get_user_textcontents, name='get_user_textcontents'),
]
