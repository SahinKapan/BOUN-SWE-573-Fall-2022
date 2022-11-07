from django.urls import include, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'login'

urlpatterns = [
    re_path(r'^register/$',views.register,name='register'),
    re_path(r'^user_login/$',views.user_login,name='user_login'),
]
