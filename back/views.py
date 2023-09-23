from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
# from .models import User
from rest_framework.authtoken.models import Token
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.views import APIView


class UserProfileView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        username = request.data['username']

    # Check if a user with the same phone number already exists
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            return Response({"message": "A user with this phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if UserProfile.objects.filter(username=username).exists():
            return Response({"message": "A user with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # Try to authenticate the user
            user = authenticate(
                request, username=username, password=password)

            if user is None:
                raise AuthenticationFailed(
                    'User not found or invalid credentials')

            # Generate JWT token
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')

            # Set the token as a cookie
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)

            return response
        except Exception as e:
            # Handle exceptions, such as database errors
            return Response({'error': str(e)}, status=400)
