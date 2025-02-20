import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
class TestRefreshTokenView:
    url = reverse("token_refresh")

    def test_refresh_token_missing(self, api_client):
        """Test case where refresh token is not provided."""
        response = api_client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Refresh token not provided or expired"

    @patch("rest_framework_simplejwt.tokens.RefreshToken")
    def test_invalid_refresh_token(self, mock_refresh_token, api_client):
        """Test case where refresh token is invalid."""
        mock_refresh_token.side_effect = Exception("Invalid token")
        response = api_client.post(self.url, HTTP_COOKIE="refresh_token=invalidtoken")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        assert response.data["detail"] == "Invalid refresh token"

    @patch("accounts.utils.create_cookie_response")
    def test_valid_refresh_token(self, mock_create_cookie_response, create_user, api_client):
        """Test case where refresh token is valid and new one is generated."""
        refresh_token = str(RefreshToken.for_user(create_user))
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.data = {"message": "Token refreshed successfully."}
        mock_create_cookie_response.return_value = mock_response
        
        response = api_client.post(self.url, HTTP_COOKIE=f"refresh_token={refresh_token}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Token refreshed successfully."

    @patch("rest_framework_simplejwt.tokens.RefreshToken")
    def test_invalid_refresh_token_user_id_missing(self, mock_refresh_token, api_client):
        """Test case where refresh token is valid but user_id is missing."""
        mock_refresh_token.return_value = MagicMock(
            **{
                'get.return_value': None
            }
        )

        response = api_client.post(self.url, HTTP_COOKIE="refresh_token=invalidtoken")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Invalid refresh token"
    
    def test_refresh_token_view_with_non_existent_user(self, api_client, create_user):
        refresh_token = str(RefreshToken.for_user(create_user))
        create_user.delete()
        response = api_client.post(self.url, HTTP_COOKIE=f"refresh_token={refresh_token}")

        # Assert that the response is Unauthorized (401) and contains the expected error message
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'User not found'