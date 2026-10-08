from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from app.models import Product
from app.serializers import ProductSerializer



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
