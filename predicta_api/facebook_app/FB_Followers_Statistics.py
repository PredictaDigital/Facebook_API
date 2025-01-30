import requests
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_fb_oauth_details
from .models import FacebookFollowersInsight
import json
import time  # Import time module for measuring load time

# Helper function to fetch the Page Access Token
def get_page_access_token(user_access_token, page_id):
    endpoint = f"https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_access_token}"
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        page_access_token = response.json().get("access_token")
        return page_access_token
    else:
        return None

class FetchFollowersStatistics(APIView):
    def get(self, request):
        start_time = time.time()  # Start measuring time

        # Fetch the access token and page ID using the utility function
        email = request.COOKIES.get('email')
        fb_details = get_fb_oauth_details(email)

        if not fb_details:
            return Response({"error": "No details found for the given email"}, status=status.HTTP_404_NOT_FOUND)

        user_access_token = fb_details.get("access_token")
        page_id = fb_details.get("page_id")

        if not user_access_token or not page_id:
            return Response({"error": "User access token or page ID is missing."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the page access token
        page_access_token = get_page_access_token(user_access_token, page_id)

        if not page_access_token:
            return Response({"error": "Failed to retrieve Page Access Token."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if any insights exist for the given email
        created_at = 'null'
        if FacebookFollowersInsight.objects.filter(email=email).exists():
            # Fetch the latest insight for the given email
            latest_insight = FacebookFollowersInsight.objects.filter(email=email).latest('data_created_date')
            created_at = latest_insight.data_created_date
        
        if created_at != 'null':  # Check if created_at is not null
            # delete existing data
            now = datetime.today()
            # Subtract 93 Days (approximately 3 years)
            sincedates = now - timedelta(weeks=13.2857)  # Rough estimate (93 Days)
            sincedate = created_at
        else:  # Calculate the date 93 Days ago if created_at is null
            now = datetime.today()
            # Subtract 93 Days (approximately 3 years)
            sincedates = now - timedelta(weeks=13.2857)  # Rough estimate (93 Days)
            sincedate = sincedates.strftime('%Y-%m-%d')

        # Get today's date dynamically
        today = datetime.today()
        current_time = time.strftime("%H:%M:%S")

        # Prepare the request parameters
        endpoint = f"https://graph.facebook.com/v22.0/{page_id}/insights"
        params = {
            'access_token': page_access_token,
            'metric': 'page_follows',
            'since': sincedate,
            'until': today.strftime('%Y-%m-%d'),
            'period': 'day'
        }

        # Make the API request to Facebook Graph API
        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            return Response(
                {"error": "Failed to fetch insights", "details": response.json()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse the response data
        analytics_data = response.json()
        
        # Collect the insights data in a list (instead of saving it to the database)
        insights = []
        for metric_data in analytics_data['data']:
            for value in metric_data['values']:
                end_time = datetime.strptime(value['end_time'], "%Y-%m-%dT%H:%M:%S%z")
                page_follows = value['value']
                
                # Save data to the database
                FacebookFollowersInsight.objects.create(
                    page_id = page_id,
                    email = email,
                    EndTime=end_time,
                    PageFollows=page_follows,
                    data_created_date=today.strftime('%Y-%m-%d'),
                    data_created_time=current_time
                )

                # Append the data to the insights list for response
                insights.append({
                    "end_time": end_time,
                    "page_follows": page_follows
                })

        # Calculate load time
        load_time = time.time() - start_time  # End time minus start time
        

        # Return the insights data and load time in the response
        return Response({
            "insights": insights,
            "load_time_seconds": round(load_time, 2)  # Round to 2 decimal places for better readability
        }, status=status.HTTP_200_OK)
