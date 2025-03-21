import jwt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .utils import create_cookie_response
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.models import User


class RefreshTokenView(APIView):
    def post(self, request):
        print(request.user, 'user tokek')
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            raise AuthenticationFailed('Refresh token not provided or expired')
        try:
            token = RefreshToken(refresh_token)
            user_id = token.get('user_id')
            # Retrieve the user from the database
            user = User.objects.get(id=user_id)

            # Generate a new refresh token for the user
            new_refresh_token = RefreshToken.for_user(user)
            response = create_cookie_response(
                key='refresh_token',
                value=str(new_refresh_token),
                message='Token refreshed successfully.',
                status_code=status.HTTP_200_OK,
                access_token=str(new_refresh_token.access_token),
                is_profile_professional = user.profile.is_professional
            )
            return response
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Exception type: {type(e)}")
            raise AuthenticationFailed('Invalid refresh token')