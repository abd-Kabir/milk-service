
class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTObtainPairSerializer
    permission_classes = [AllowAny, ]
