from rest_framework import serializers
from .models import Category, Product, AttributeKey, AttributeValue, Comment, Image
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category



class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user.is_authenticated:
            return obj.is_liked
        return False

    def get_comment_count(self, obj):
        return Comment.objects.filter(product=obj).count()

    def get_all_images(self, obj):
        return [image.url for image in obj.images.all()]

    def get_attributes(self, obj):
        attributes = AttributeValue.objects.filter(product=obj)
        return AttributeValueSerializer(attributes, many=True).data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=255, required=True)
