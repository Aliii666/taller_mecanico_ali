from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
try:
    from rest_framework_simplejwt.tokens import RefreshToken
except Exception:
    RefreshToken = None

from .serializers import RegistroSerializer, LoginSerializer, UsuarioSerializer


def get_tokens(user):
    if RefreshToken is None:
        return {'refresh': 'unavailable', 'access': 'unavailable'}
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'mensaje': 'Usuario creado exitosamente.',
                'usuario': UsuarioSerializer(usuario).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens(user)
            return Response({
                'mensaje': 'Inicio de sesión exitoso.',
                'tokens':  tokens,
                'usuario': UsuarioSerializer(user).data,
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'usuario': UsuarioSerializer(request.user).data})
