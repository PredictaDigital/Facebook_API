from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_fb_oauth_details  # Import the utility function

class RetrieveFBDetailsView(APIView):
    def get(self, request):
        # Retrieve the email from cookies
        email = request.COOKIES.get('email')  # Replace 'email' with the actual cookie name if different
        
        # Check if email is provided in cookies
        if not email:
            return Response({"error": "Email is required in cookies"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Facebook details for the given email using the utility function
        fb_details = get_fb_oauth_details(email)

        # If no details found, return a 404 response
        if not fb_details:
            return Response({"error": "No details found for the given email"}, status=status.HTTP_404_NOT_FOUND)

        # Store the details in individual variables (if needed)
        access_token = fb_details.get("access_token")
        page_id = fb_details.get("page_id")
        ad_account = fb_details.get("ad_account")
        business_profiles = fb_details.get("business_profiles")
        instagram_account = fb_details.get("instagram_account")

        # Print the variables (or use them for further processing)
        print(f"Access Token: {access_token}")
        print(f"Page ID: {page_id}")
        print(f"Ad Account: {ad_account}")
        print(f"Business Profiles: {business_profiles}")
        print(f"Instagram Account: {instagram_account}")

        # Return the Facebook details in the response
        return Response(fb_details, status=status.HTTP_200_OK)
