from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.models import User, VerifyCode
from apps.authentication.serializer import JWTObtainPairSerializer, SignUpPersonalDataSerializer
from apps.tools.utils.mailing import send_verification_token
from config.utils.api_exceptions import APIValidation


class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTObtainPairSerializer
    permission_classes = [AllowAny, ]


class SignUpPersonalDataAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        try:
            serializer = SignUpPersonalDataSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({"detail": "Continue registration step-by-step", 'user': user.username})
        except Exception as exc:
            raise APIValidation("Bad request!", status_code=status.HTTP_400_BAD_REQUEST)


class SignUpContactDataAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, username):
        user = get_object_or_404(User, username=username)

        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        if phone_number:
            # verify with Phone Number
            pass
        elif email:
            try:
                user.email = email
                user.save()
                send_verification_token(user=user, template_name='verification.html', subject='Verification Code')
                return Response({"detail": "Verification code sent to you email",
                                 "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            except Exception as exc:
                raise APIValidation("Incorrect email!", status_code=status.HTTP_400_BAD_REQUEST)


class SignUpVerifyCodeAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        email_user = User.objects.filter(email=email)
        if email_user:
            email_user = email_user.first()
        else:
            raise APIValidation("Code is incorrect", status_code=status.HTTP_400_BAD_REQUEST)

        verify_obj = VerifyCode.objects.filter(code=code)
        if verify_obj:
            verify_obj = verify_obj.first()

            user = verify_obj.user
            if user == email_user:
                user.is_active = True
                user.save()
                verify_obj.delete()
                return Response({"detail": "Successfully verified",
                                 "user": user.username})
        else:
            raise APIValidation("Code is incorrect", status_code=status.HTTP_400_BAD_REQUEST)
