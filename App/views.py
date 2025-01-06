from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,permissions
from rest_framework.decorators import api_view
# from .products import products
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from django.utils.timezone import now as timezone_now


# for sending mails and generate token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from ecomproject import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import threading

# Password Reset Token Generator
token_generator = PasswordResetTokenGenerator()       

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        threading.Thread.__init__(self)
        self.email_message = email_message

    def run(self):
        self.email_message.send()




# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    return Response("Hello World")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProducts(request):
    products = Products.objects.prefetch_related('images').all()
    serializer = ProductSerializer(products, many=True) 
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProduct(request, pk):
    try:
        # Fetch the product by primary key
        product = Products.objects.prefetch_related('images').get(id=pk)
    except Products.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the product
    serializer = ProductSerializer(product, many=False)
    response_data = serializer.data

     # Ensure the images contain only relative URLs
    for image in response_data.get('images', []):
        if image.get('image'):
            image['image'] = image['image']

    return Response(response_data)


class LoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def get_user(self, email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        user_request_data = request.data
        email = user_request_data.get("username")
        password = user_request_data.get("password")

        if not email or not password:
            return Response({
                "status": "failure",
                "message": "Email and password are required",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user
        user_db_details = self.get_user(email)
        print("user_db_details",user_db_details)
        if not user_db_details:
            return Response({
                "status": "error",
                "message": "User not found",
            }, status=status.HTTP_404_NOT_FOUND)

        if not user_db_details.is_active:
            return Response({
                "status": "failure",
                "message": "User is not active",
            }, status=status.HTTP_403_FORBIDDEN)

        # Authenticate the user
        user = authenticate(username=email, password=password)
        if user is None:
            return Response({
                "status": "failure",
                "message": "Email and password do not match",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Generate tokens manually
        refresh_token, access_token = self.generate_tokens(user_db_details)

        # Update the last login time
        user_db_details.last_login = timezone_now()
        user_db_details.save()

        # Serialize user data
        serializer = self.serializer_class(user_db_details)
        response = {
            "refresh": refresh_token,
            "access": access_token,
            "message": "Login Successfully",
            "user": serializer.data,
        }

        return Response(response, status=status.HTTP_200_OK)

    @staticmethod
    def generate_tokens(user):
        """
        Manually generate refresh and access tokens for the user.
        """
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return str(refresh), str(access)

#For Authentication user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfiles(request):
    user = request.user
    serializer = LoginSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializer = LoginSerializer(users, many=True)
    return Response(serializer.data)    


@api_view(['POST'])
def registerUser(request):
    data=request.data
    try:
        user= User.objects.create(first_name=data['fname'],last_name=data['lname'],username=data['email'],email=data['email'],password=make_password(data['password']),is_active=False)

        # generate token for sending mail
        email_subject="Activate Your Account"
        message=render_to_string(
            "activate.html",
           {
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
           }

        )
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[data['email']])
        email_message.send()
        EmailThread(email_message).start()
        # message={'details':"Activate Your Account please check click link in gmail for account activation"}
        # return Response(message)     
        serialize=UserSerializerwithRegister(user,many=False)
        return Response(serialize.data)
    
    except Exception as e:
        message={'details':"User with this email already exits or somthing went wrong"}
        # print(message)
        return Response(message )
    

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            return render(request,"activatesuccess.html")
        else:
            return render(request,"activatefail.html")   
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def requestPasswordReset(request):
    email = request.data.get('email', None)
    if not email:
        return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_link = f"http://127.0.0.1:8000/users/reset-password-confirm/{uidb64}/{token}/"

        email_subject = 'Reset Your Password'
        email_body = f'Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_link}'
        email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, [user.email])
        email.send()

        return Response({'detail': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'No user found with this email.'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PasswordResetConfirmView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password', None)
        if not new_password:
            return Response({'detail': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'detail': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchProducts(request):
    query = request.query_params.get('query', None)
    if query:
        # Update the filter to use 'productname' instead of 'name'
        products = Products.objects.filter(productname__icontains=query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)






