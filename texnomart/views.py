from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Category, Product, AttributeKey, AttributeValue
from .serializers import CategorySerializer, ProductSerializer, AttributeKeySerializer, AttributeValueSerializer
from twilio.rest import Client
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
import json
import os
from rest_framework.views import APIView
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .filters import ProductFilter, CategoryFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from texnomart.serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.filters import SearchFilter
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class ProductListPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'category__name']

    def get(self, request, *args, **kwargs):
        cache_key = 'product_list'
        products = cache.get(cache_key)

        if not products:
            queryset = self.filter_queryset(self.get_queryset())
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            products = serializer.data
            cache.set(cache_key, products, timeout=60)
            return paginator.get_paginated_response(products)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(self.queryset, request)
        return paginator.get_paginated_response(products)


class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ['name']

    def get(self, request, *args, **kwargs):
        cache_key = 'category_list'
        categories = cache.get(cache_key)
        if not categories:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            categories = serializer.data
            cache.set(cache_key, categories, timeout=60)
        return Response(categories)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'




class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductEditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class CategoryEditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class AttributeKeyListView(generics.ListAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer

class AttributeValueListView(generics.ListAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer

class CategoryProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return Product.objects.filter(category=category)


def get_cached_category_data(slug):
    cache_key = f'category_data_{slug}'
    category_data = cache.get(cache_key)
    if not category_data:
        category = get_object_or_404(Category, slug=slug)
        category_data = CategorySerializer(category).data
        cache.set(cache_key, category_data, timeout=300)
    return category_data



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
