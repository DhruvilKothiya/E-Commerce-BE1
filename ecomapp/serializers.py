from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     name=serializers.SerializerMethodField(read_only=True)
#     _id=serializers.SerializerMethodField(read_only=True)
#     isAdmin=serializers.SerializerMethodField(read_only=True)
   
#     class Meta:
#         model=User
#         fields=['id','_id','username','email','name','isAdmin']
    
#     def get_name(self,obj):
#         firstname=obj.first_name
#         lastname=obj.last_name
#         name=firstname+' '+lastname
#         if name=='':
#             name=obj.email[:5]
#             return name
#         return name
    
#     def get__id(self,obj):
#         return obj.id

#     def get_isAdmin(self,obj):
#         return obj.is_staff
    
    
# class UserSerializerWithToken(UserSerializer):
#     token=serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model=User
#         fields=['id','_id','username','email','name','isAdmin','token',]
    
#     def get_token(self,obj):
#         token=RefreshToken.for_user(obj)
#         return str(token.access_token)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        extra_kwargs={'password': {'write_only': True}}
    
class UserSerializerwithRegister(LoginSerializer):
    class Meta:
        model=User
        fields=['id','_id','username','email','name','isAdmin']