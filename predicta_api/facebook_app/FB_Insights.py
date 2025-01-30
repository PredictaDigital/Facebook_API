# views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import timedelta, datetime
from .utils import get_fb_oauth_details
from .models import FacebookInsights
from django.db import IntegrityError
from django.utils.timezone import now


# Helper function to fetch the Page Access Token
def get_page_access_token(user_access_token, page_id):
    endpoint = f"https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_access_token}"
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        page_access_token = response.json().get("access_token")
        return page_access_token
    else:
        return None
    

class FetchFBPageInsigths(APIView):
    def get(self, request):

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

        # Define the date range
        since_date = '2024-11-22'
        until_date = '2025-01-22'

        # Check if any insights exist for the given email
        created_at = None
        if FacebookInsights.objects.filter(email=email).exists():
            latest_insight = FacebookInsights.objects.filter(email=email).latest('data_created_date')
            created_at = latest_insight.data_created_date

        if created_at:  
            sincedate = created_at
        else:  
            sincedate = (now() - timedelta(days=92)).strftime('%Y-%m-%d')

        endpoint = f"https://graph.facebook.com/v22.0/{page_id}/insights"

        # Define the parameters for the request
        params = {
            'access_token': page_access_token,
            'metric': 'page_fans,page_fan_adds,page_fan_removes,page_views_total,page_video_views,page_video_view_time,'
                      'page_video_views_paid,page_video_views_organic,page_video_views_click_to_play,'
                      'page_posts_impressions,page_posts_impressions_paid,page_posts_impressions_organic,page_posts_impressions_viral,'
                      'page_posts_impressions_nonviral,page_impressions,page_impressions_unique,page_impressions_paid,'
                      'page_impressions_viral,page_impressions_nonviral,'
                      'page_post_engagements,page_actions_post_reactions_like_total,page_actions_post_reactions_anger_total,'
                      'page_actions_post_reactions_wow_total,page_actions_post_reactions_haha_total,'
                      'page_actions_post_reactions_love_total,page_actions_post_reactions_sorry_total',
            'since': sincedate,
            'until': now().strftime('%Y-%m-%d'),
            'period': 'day'
        }

        # Make the API request to Facebook
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch insights", "details": response.json()}, status=status.HTTP_400_BAD_REQUEST)

        analytics_data = response.json()
        list_type_data = analytics_data.get('data')

        # Prepare data for DB insertion
        result_data = {}
        for item in list_type_data:
            metric_name = item.get("name")
            for value in item.get("values"):
                end_time = value.get('end_time')
                if end_time in result_data:
                    result_data[end_time].update({metric_name: value.get('value')})
                else:
                    result_data[end_time] = {metric_name: value.get('value')}

        # Insert into the database
        records = []
        for end_time, metrics in result_data.items():
            records.append(
                FacebookInsights(
                    email=email,
                    page_id=page_id,
                    end_time=end_time,
                    page_fans=metrics.get("page_fans", 0),
                    page_fan_adds=metrics.get("page_fan_adds", 0),
                    page_fan_removes=metrics.get("page_fan_removes", 0),
                    page_views_total=metrics.get("page_views_total", 0),
                    page_video_views=metrics.get("page_video_views", 0),
                    page_video_view_time=metrics.get("page_video_view_time", 0),
                    page_video_views_paid=metrics.get("page_video_views_paid", 0),
                    page_video_views_organic=metrics.get("page_video_views_organic", 0),
                    page_video_views_click_to_play=metrics.get("page_video_views_click_to_play", 0),
                    page_posts_impressions=metrics.get("page_posts_impressions", 0),
                    page_posts_impressions_paid=metrics.get("page_posts_impressions_paid", 0),
                    page_posts_impressions_organic=metrics.get("page_posts_impressions_organic", 0),
                    page_posts_impressions_viral=metrics.get("page_posts_impressions_viral", 0),
                    page_posts_impressions_nonviral=metrics.get("page_posts_impressions_nonviral", 0),
                    page_impressions=metrics.get("page_impressions", 0),
                    page_impressions_unique=metrics.get("page_impressions_unique", 0),
                    page_impressions_paid=metrics.get("page_impressions_paid", 0),
                    page_impressions_viral=metrics.get("page_impressions_viral", 0),
                    page_impressions_nonviral=metrics.get("page_impressions_nonviral", 0),
                    page_post_engagements=metrics.get("page_post_engagements", 0),
                    page_actions_post_reactions_like_total=metrics.get("page_actions_post_reactions_like_total", 0),
                    page_actions_post_reactions_anger_total=metrics.get("page_actions_post_reactions_anger_total", 0),
                    page_actions_post_reactions_wow_total=metrics.get("page_actions_post_reactions_wow_total", 0),
                    page_actions_post_reactions_haha_total=metrics.get("page_actions_post_reactions_haha_total", 0),
                    page_actions_post_reactions_love_total=metrics.get("page_actions_post_reactions_love_total", 0),
                    page_actions_post_reactions_sorry_total=metrics.get("page_actions_post_reactions_sorry_total", 0),
                    data_created_date=now().date(),
                    data_created_time=now().time()
                )
            )

        try:
            FacebookInsights.objects.bulk_create(records)
        except IntegrityError as e:
            return Response({"error": "Database insert failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Facebook insights stored successfully"}, status=status.HTTP_201_CREATED)
