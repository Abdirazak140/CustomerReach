from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from backend.djangolol.api.models import auth_models
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

@require_POST
def login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse({"detail": "Provide a username and password please!"})
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"detail":"Invalid credentials!"}, status = 400)
    login(request, user)
    return JsonResponse({"details":"Logged in successfully"})

def logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({"details":"Not logged in!"}, status = 400)
    logout(request)
    return JsonResponse({"details":"Logged out successfully"})

@ensure_csrf_cookie
def session(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isauthenticated":False})
    return JsonResponse({"isauthenticated":True})

def whoami(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isauthenticated":False})
    return JsonResponse({"username":request.user.username})