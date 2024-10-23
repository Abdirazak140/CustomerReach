from django.urls import path
from ..views import auth_views

urlpatterns = [
    path("login/", auth_views.login_view, name="api_login"),
    path("logout/", auth_views.custom_logout, name="logout"),
    path("session/", auth_views.session_view, name="api_session"),
    path("whoami/", auth_views.custom_whoami, name="api_whoami"),
]
