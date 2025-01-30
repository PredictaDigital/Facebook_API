from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import FB_Oauth  # Assuming you're using a model for storing Facebook OAuth details

class FacebookCallback(APIView):
    def get(self, request):
        # Step 1: Get the authorization code from the query parameters
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the email from the cookie
        email = request.COOKIES.get('email')
        if not email:
            return Response({"error": "Email not found in cookie"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Set up your Facebook App credentials
        client_id = "385745461007462"  # Your Facebook App ID
        client_secret = "39838a1fd0b95af866f368acc81f77b0"  # Your Facebook App Secret
        redirect_uri = "http://localhost:8000/facebook_app/callback"  # Your redirect URI without email

        # Step 3: Exchange the authorization code for an access token
        token_url = "https://graph.facebook.com/v22.0/oauth/access_token"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "client_secret": client_secret,
            "code": code,
        }

        response = requests.get(token_url, params=params)
        try:
            response_data = response.json()
        except ValueError:
            return Response({"error": "Invalid JSON response from Facebook"}, status=response.status_code)

        if response.status_code == 200:
            access_token = response_data.get("access_token")

            # Step 4: Fetch the user's Facebook pages using the access token
            pages_url = "https://graph.facebook.com/v22.0/me/accounts"
            pages_params = {
                "access_token": access_token,
            }

            pages_response = requests.get(pages_url, params=pages_params)
            try:
                pages_data = pages_response.json()
            except ValueError:
                return Response({"error": "Invalid JSON response from Facebook for pages"}, status=pages_response.status_code)

            if pages_response.status_code == 200:
                # Step 5: Get the first page ID (if available)
                page_id = None
                page_access_token = None
                if "data" in pages_data:
                    page = pages_data["data"][0]  # Assuming the first page is selected
                    page_id = page.get("id")
                    page_access_token = page.get("access_token")  # Fetch the Page Access Token

                if not page_access_token:
                    return Response({"error": "Page access token not found"}, status=status.HTTP_400_BAD_REQUEST)

                # Step 6: Fetch the user's business profiles using the User Access Token
                business_url = "https://graph.facebook.com/v22.0/me/businesses"
                business_params = {
                    "access_token": access_token,  # Using User Access Token
                }

                business_response = requests.get(business_url, params=business_params)
                try:
                    business_data = business_response.json()
                except ValueError:
                    return Response({"error": "Invalid JSON response from Facebook for business profiles"}, status=business_response.status_code)

                if business_response.status_code == 200:
                    # Step 7: Get the business profiles (if available)
                    business_profiles = []
                    ad_accounts = {}  # To store ad accounts associated with each business
                    if "data" in business_data:
                        for business in business_data["data"]:
                            business_id = business.get("id")
                            business_profiles.append(business_id)  # Collect all business profile IDs

                            # Fetch ad accounts for each business
                            ad_accounts_url = f"https://graph.facebook.com/v22.0/{business_id}/adaccounts"
                            ad_accounts_params = {
                                "access_token": access_token,
                            }

                            ad_accounts_response = requests.get(ad_accounts_url, params=ad_accounts_params)
                            try:
                                ad_accounts_data = ad_accounts_response.json()
                            except ValueError:
                                return Response({"error": "Invalid JSON response from Facebook for ad accounts"}, status=ad_accounts_response.status_code)

                            if ad_accounts_response.status_code == 200:
                                ad_accounts[business_id] = [ad.get("id") for ad in ad_accounts_data.get("data", [])]
                            else:
                                ad_accounts[business_id] = []

                    # Fetch additional ad accounts and business info
                    adaccounts_url = "https://graph.facebook.com/v22.0/me?fields=adaccounts{business}"
                    adaccounts_params = {
                        "access_token": access_token,
                    }

                    adaccounts_response = requests.get(adaccounts_url, params=adaccounts_params)
                    try:
                        adaccounts_data = adaccounts_response.json()
                    except ValueError:
                        return Response({"error": "Invalid JSON response from Facebook for additional ad accounts"}, status=adaccounts_response.status_code)

                    if adaccounts_response.status_code == 200:
                        additional_ad_accounts = adaccounts_data.get("adaccounts", {}).get("data", [])
                        for ad_account in additional_ad_accounts:
                            business_info = ad_account.get("business", {})
                            if business_info:
                                ad_accounts.setdefault(business_info.get("id"), []).append(ad_account.get("id"))

                    # Print the business and ad account data (for debugging)
                    print("Business Profiles:", business_profiles)
                    print("Ad Accounts:", ad_accounts)

                    # Step 8: Fetch the Instagram account connected to the page
                    instagram_url = f"https://graph.facebook.com/v22.0/{page_id}"
                    instagram_params = {
                        "fields": "instagram_business_account",
                        "access_token": page_access_token,  # Use the Page Access Token
                    }

                    instagram_response = requests.get(instagram_url, params=instagram_params)
                    try:
                        instagram_data = instagram_response.json()
                    except ValueError:
                        return Response({"error": "Invalid JSON response from Facebook for Instagram ID"}, status=instagram_response.status_code)

                    if instagram_response.status_code == 200:
                        instagram_account = instagram_data.get("instagram_business_account", {}).get("id")
                    else:
                        instagram_account = None
                
                  # Create the datafb dictionary
                    datafb = {
                        "access_token": access_token,
                        "page_id": page_id,
                        "instagram_account": instagram_account,  # Add Instagram account ID
                        "business_profiles": business_profiles,
                        "ad_accounts": ad_accounts,  # Return the ad accounts for each business
                        "email": email  # Return the email for association
                    }

                    # Extract ad_accounts from datafb
                    ad_accounts = datafb.get("ad_accounts", {})
                    # business_id = "167384841988076"  # The business ID we want to check
                    ad_account_list = ad_accounts.get(business_id, [])
                    ad_account_id = ad_account_list[0]
                    ad_account_id = ad_account_id.strip('"')

                    # Insert data dynamically into the database
                    data = FB_Oauth(
                        access_token=access_token,
                        page_id=page_id,
                        instagram_account=instagram_account,
                        business_profiles=business_profiles,
                        ad_accounts=ad_account_id,
                        email=email
                    )
                    data.save()

                    # Return the response with the data variable
                    return Response(datafb, status=status.HTTP_200_OK)


                return Response({"error": business_data.get('error', 'Failed to fetch business profiles')}, status=business_response.status_code)

            return Response({"error": pages_data.get('error', 'Failed to fetch page ID')}, status=pages_response.status_code)

        return Response({"error": response_data.get('error', 'Failed to fetch access token')}, status=response.status_code)
