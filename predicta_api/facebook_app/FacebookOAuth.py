from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import FB_Oauth
from datetime import timedelta
import requests

class FacebookOAuth(APIView):
    def get(self, request):
        # Facebook App credentials
        client_id = "385745461007462"  # Your Facebook App ID
        
        # Get email from the query parameters
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Set the email in a cookie for future use
        response = Response({"message": "Redirecting to Facebook OAuth"})

        # Determine if the request is over HTTPS
        is_https = request.is_secure()

        response.set_cookie(
            'email', email, 
            max_age=timedelta(days=90),  # Cookie expires in 90 Days
            httponly=True,  # Cookie is only accessible by the server
            secure=is_https,  # Set secure flag only if using HTTPS
            samesite='Strict' if is_https else 'Lax'  # Set Lax if not using HTTPS
        )

        # Dynamically set the redirect URI (use environment or settings)
        redirect_uri = "http://localhost:8000/facebook_app/callback"  # Adjust to your callback URL
        scope = "email,pages_show_list,pages_manage_metadata,ads_management,ads_read,business_management,instagram_basic"  # Include Instagram and Business permissions

        # Create the authorization URL for Facebook OAuth
        auth_url = f"https://www.facebook.com/v22.0/dialog/oauth?{urlencode({
            'response_type': 'code',  # Get an authorization code
            'client_id': client_id,  # Your Facebook App ID
            'redirect_uri': redirect_uri,  # The callback URI after login
            'scope': scope,  # Requested permissions
        })}"

        # Perform the redirect to the Facebook OAuth authorization URL
        response['Location'] = auth_url
        response.status_code = 302
        return response

class GetLatestTokenView(APIView):
    def get(self, request):
        email = request.query_params.get('email')  # Extract email from query parameters
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        fb_oauth = FB_Oauth.get_latest_token_by_email(email)
        if not fb_oauth:
            return Response({"error": "No token found for the given email"}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the response with the latest token details
        return Response({
            "access_token": fb_oauth.access_token,
            "page_id": fb_oauth.page_id,
            "instagram_account": fb_oauth.instagram_account,
            "business_profiles": fb_oauth.business_profiles,
            "ad_accounts": fb_oauth.ad_accounts,
            "email": fb_oauth.email,
        }, status=status.HTTP_200_OK)
