from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, Product
from .serializers import VendorSerializer, ProductSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Vendor Registration
class VendorRegisterView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def perform_create(self, serializer):
        user = self.request.user
        vendor = serializer.save(user=user)
        user.is_vendor = True
        user.save()
        return vendor


# Vendor Login with JWT
class VendorLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username
            })
        return Response({'error': 'Invalid credentials'}, status=400)


# Product CRUD (Vendor only)
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_vendor:
            return Product.objects.filter(vendor__user=self.request.user)
        return Product.objects.none()

    def perform_create(self, serializer):
        vendor = Vendor.objects.get(user=self.request.user)
        serializer.save(vendor=vendor)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)
