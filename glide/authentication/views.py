from rest_framework import generics
from .serializers   import RegisterSerializer
from users.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    