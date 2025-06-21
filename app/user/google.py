from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend  # Импортируем бэкенд
from django.shortcuts import render
from requests_oauthlib import OAuth2Session
from rest_framework_simplejwt.tokens import RefreshToken

from app import settings as appsettings
from user.models import CustomUser

# Настройки Google OAuth2
client_id = appsettings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
client_secret = appsettings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
redirect_uri = appsettings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://accounts.google.com/o/oauth2/token"


def google_auth(request):
    google = OAuth2Session(
        client_id, redirect_uri=redirect_uri, scope=["openid", "email", "profile"]
    )
    authorization_url, state = google.authorization_url(
        authorization_base_url, access_type="offline", prompt="select_account"
    )
    request.session["oauth_state"] = state
    return render(request, "google_auth.html", {"authorization_url": authorization_url})


def google_auth_complete(request):
    google = OAuth2Session(
        client_id, redirect_uri=redirect_uri, state=request.session.get("oauth_state")
    )
    token = google.fetch_token(  # noqa: F841
        token_url,
        client_secret=client_secret,
        authorization_response=request.build_absolute_uri(),
    )

    # Получаем данные пользователя из Google
    user_info = google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    google_id = user_info.get("id")
    email = user_info.get("email")
    first_name = user_info.get("given_name")
    last_name = user_info.get("family_name")

    # Поиск или создание пользователя
    try:
        # Ищем пользователя по google_id
        user = CustomUser.objects.get(google_id=google_id)
    except CustomUser.DoesNotExist:
        try:
            # Если пользователь не найден по google_id, ищем по email
            user = CustomUser.objects.get(email=email)
            # Обновляем google_id для существующего пользователя
            user.google_id = google_id
            user.save()
        except CustomUser.DoesNotExist:
            # Создаем нового пользователя
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                google_id=google_id,
            )

    # Залогинить пользователя в системе
    # Указываем бэкенд аутентификации
    backend = ModelBackend()  # noqa: F841
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    # Генерация JWT токенов
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Рендеринг страницы
    response = render(request, "google_auth_complete.html", {})

    # Установка токенов в cookies
    response.set_cookie(
        "access_token",
        access_token,
        httponly=False,  # Доступен через JavaScript
        secure=False,  # Разрешить использование на HTTP (для тестов)
        samesite="Lax",
        max_age=3600,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=False,  # Доступен через JavaScript
        secure=False,  # Разрешить использование на HTTP (для тестов)
        samesite="Lax",
        max_age=86400,
    )
    return response
