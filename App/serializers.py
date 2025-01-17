from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Products

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Images
        fields = ['id', 'image']
class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = '__all__'
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        extra_kwargs={'password': {'write_only': True}}
    
class UserSerializerwithRegister(LoginSerializer):
    class Meta:
        model=User
        fields='__all__'
        
        
class CartQtySerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'