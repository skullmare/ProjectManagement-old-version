from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomPasswordResetConfirmSerializer


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token, *args, **kwargs):
        # Render the password reset form
        return render(request, template_name="reset_password_form.html")

    def post(self, request, uid, token, *args, **kwargs):
        try:
            # Decode the UID and get the user
            uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response(
                {"detail": "Invalid token or user ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(user, token):
            serializer = CustomPasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"detail": "Password reset successful."}, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST
        )


class ActivationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token, *args, **kwargs):
        try:
            # Decode the UID and get the user
            uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(
                request,
                template_name="account_activate_result.html",
                context={
                    "title": "Ваш аккаунт успешно активирован!",
                    "desc": "Теперь вы можете войти и начать пользоваться нашим сервисом.",
                },
                status=status.HTTP_200_OK,
            )
        return render(
            request,
            template_name="account_activate_result.html",
            context={
                "title": "Ошибка 400",
                "desc": "Эта ссылка недействительна. Попробуйте зарегистрироваться еще раз или обратитесь в техническую поддержку!",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
