from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import (
    create_cookie_response,
    delete_cookie_response
)
from rest_framework.exceptions import AuthenticationFailed

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'User registered successfully.'}, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        response = create_cookie_response(
            key='refresh_token',
            value=str(refresh),
            message='User logged in successfully.',
            status_code=status.HTTP_200_OK,
            access_token=str(refresh.access_token),
            is_profile_professional = user.profile.is_professional
        )
        print(request.user, 'user')
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    response = delete_cookie_response(
        key='refresh_token',
        message='User logged out successfully.',
        status_code=status.HTTP_200_OK
    )
    return response


class Account(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckAuthView(APIView):
    # Only allow authenticated users to access this view
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # If the user is authenticated, return a success message
        return Response({
            'message': 'You are authenticated.',
            'username': request.user.username,
            'email': request.user.email,
        })


class DecodeTokenView(APIView):
    def get(self, request):
        # Get the access token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Authorization header missing or invalid.')

        access_token = auth_header.split(' ')[1]

        try:
            # Decode the token
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
            return Response({
                'message': 'Token decoded successfully.',
                'payload': payload,
            })
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')