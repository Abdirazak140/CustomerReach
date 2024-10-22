from django.urls import path
from ..views import auth_views

urlpatterns = [
    path("login/", auth_views.login, name="api_login"),
    path("logout/", auth_views.logout, name="api_logout"),
    path("session/", auth_views.session, name="api_session"),
    path("whoami/", auth_views.whoami, name="api_whoami"),
]
