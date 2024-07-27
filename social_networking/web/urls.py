from django.urls import path, include
from web.views import login_view, registration, logout_user

urlpatterns = [
    path('feeds/', include('feeds.urls')),
    path('login/', login_view, name= 'login'), 
    path('registration', registration, name='registration'),
    path('logout/', logout_user, name='logout_user'),
]
