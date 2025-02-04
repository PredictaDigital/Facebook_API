from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from django.http import HttpResponse
from .models import InstagramMediaInsight, InstagramPageInsight, InstagramPageStatisticsLifetime
from facebook_app.models import FB_Oauth
from datetime import datetime, timedelta
import requests
import time
from django.conf import settings

# Utility function to get OAuth details for Facebook or Instagram
def get_fb_oauth_details(request):
    """
    Retrieve the latest Facebook OAuth details based on the provided email.
    Returns a dictionary of details or None if no data is found.
    """
    email = request.COOKIES.get('email')
    fb_oauth = FB_Oauth.objects.filter(email=email).order_by('-id').first()  # Get the latest entry
    if not fb_oauth:
        return None
    return {
        "access_token": fb_oauth.access_token,
        "page_id": fb_oauth.page_id,
        "ad_account": fb_oauth.ad_accounts,
        "business_profiles": fb_oauth.business_profiles,
        "instagram_account": fb_oauth.instagram_account,
        "email": fb_oauth.email
    }

# Function to fetch Instagram Media Insights
def fetch_instagram_insights(request):
    """
    Fetch Instagram insights from the Graph API and save them in the database.
    Returns a list of processed data.
    """
    fb_oauth_details = get_fb_oauth_details(request)
    if not fb_oauth_details:
        return []

    access_token = fb_oauth_details['access_token']
    page_id = fb_oauth_details['instagram_account']
    email = fb_oauth_details['email']
    
    endpoint = f"https://graph.facebook.com/v22.0/{page_id}/media"
    params = {
        'access_token': access_token,
        'fields': 'id,ig_id,timestamp,media_type,comments_count,like_count,permalink,username,caption,' 
                  'media_product_type,is_comment_enabled,media_url,insights.metric(impressions,reach,' 
                  'profile_visits,profile_activity,replies,saved,video_views,shares,total_interactions,follows)', 
        'limit': 5000
    }

    # Clear old data
    InstagramMediaInsight.objects.filter(email=email).delete()

    all_data = []
    while endpoint:
        response = requests.get(endpoint, params=params if 'after' not in endpoint else None)
        analytics_data = response.json()

        if 'data' not in analytics_data:
            return []

        list_type_data = analytics_data['data']

        # Get current date and time
        today = datetime.now()
        current_date = today.strftime('%Y-%m-%d')
        current_time = today.strftime('%H:%M:%S')

        for item in list_type_data:
            insights = item.get('insights', {}).get('data', [])

            # Extract insights safely
            def get_insight_value(insight_name):
                return next((insight['values'][0]['value'] for insight in insights if insight['name'] == insight_name), 0)

            # Save data in Django model
            post = InstagramMediaInsight.objects.create(
                ig_id=item.get("ig_id"),
                post_date=parse_datetime(item.get("timestamp")),
                media_type=item.get("media_type"),
                email = email,
                comments_count=item.get("comments_count"),
                like_count=item.get("like_count"),
                permalink=item.get("permalink"),
                username=item.get("username"),
                caption=item.get("caption"),
                media_product_type=item.get("media_product_type"),
                is_comment_enabled=item.get("is_comment_enabled", True),
                media_url=item.get("media_url"),
                impressions=get_insight_value("impressions"),
                reach=get_insight_value("reach"),
                profile_visits=get_insight_value("profile_visits"),
                profile_activity=get_insight_value("profile_activity"),
                replies=get_insight_value("replies"),
                saved=get_insight_value("saved"),
                video_views=get_insight_value("video_views"),
                shares=get_insight_value("shares"),
                total_interactions=get_insight_value("total_interactions"),
                follows=get_insight_value("follows"),
                data_created_date=current_date,  # Store the current date
                data_created_time=current_time,  # Store the current time
            )

            all_data.append({
                "ig_id": post.ig_id,
                "username": post.username,
                "caption": post.caption,
                "like_count": post.like_count,
                "comments_count": post.comments_count
            })

        # Check if there's a next page in pagination
        endpoint = analytics_data.get('paging', {}).get('next')

    return all_data

def fetch_insta_page_insights(request):
    """
    Fetch Facebook Page Insights from the Graph API and save them in the database.
    Returns a list of processed data.
    """
    fb_oauth_details = get_fb_oauth_details(request)
    if not fb_oauth_details:
        return []

    access_token = fb_oauth_details['access_token']
    insta_id = fb_oauth_details['instagram_account']  # Instagram account ID
    email = fb_oauth_details['email']

    # Get the latest stored date in the database
    created_at = None
    if InstagramPageInsight.objects.filter(email=email).exists():
        pdata = InstagramPageInsight.objects.filter(email=email).latest('data_created_date')
        created_at = pdata.data_created_date
        if created_at and created_at == datetime.now().date():
            print("Data already fetched for today. Stopping process.")
            return []  # Stop if today's data is already present
        else:
            created_at += timedelta(days=1)
    else:
        created_at = datetime.now().date() - timedelta(days=29)  # Start from 30 days ago if no data exists

    since_date = created_at
    until_date = datetime.now().date()

    print("Fetching data from:", since_date, "to", until_date)

    # Define the API endpoint and parameters
    endpoint = f"https://graph.facebook.com/v21.0/{insta_id}/insights"
    params = {
        'access_token': access_token,
        'metric': 'follower_count,impressions,reach',
        'period': 'day',
        'since': since_date.strftime('%Y-%m-%d'),
        'until': until_date.strftime('%Y-%m-%d'),
    }

    all_data = []
    data_inserted = False  # Flag to check if any new data was added

    # Handle pagination
    while endpoint:
        response = requests.get(endpoint, params=params)
        analytics_data = response.json()

        if 'data' not in analytics_data:
            print(f"No insights data found for Instagram account {insta_id}")
            break

        list_type_data = analytics_data.get('data', [])
        result_data = {}

        # Process insights data
        for item in list_type_data:
            metric_name = item.get("name")
            for value in item.get("values"):
                end_time = parse_datetime(value.get('end_time')).date()

                # If data for this `end_time` already exists, stop the process
                if InstagramPageInsight.objects.filter(end_time=end_time, email=email).exists():
                    print(f"Data already exists for {end_time}. Stopping process.")
                    return all_data  # Stop further execution

                if end_time in result_data:
                    result_data[end_time].update({metric_name: value.get('value')})
                else:
                    result_data[end_time] = {metric_name: value.get('value')}

        # Insert unique data into the database
        today = datetime.now().date()

        for end_time, metrics in result_data.items():
            post = InstagramPageInsight.objects.create(
                end_time=end_time,
                follower_count=metrics.get('follower_count', 0),
                impressions=metrics.get('impressions', 0),
                reach=metrics.get('reach', 0),
                page_id=insta_id,
                email=email,
                data_created_date=today,  # Store the current date
                data_created_time=datetime.now().strftime('%H:%M:%S'),  # Store the current time
            )

            all_data.append({
                "end_time": post.end_time,
                "follower_count": post.follower_count,
                "impressions": post.impressions,
                "reach": post.reach
            })

            data_inserted = True  # Mark that we have inserted new data

        # Stop pagination if data was inserted and we have reached today's date
        if data_inserted:
            break

        # Check if there's a next page in pagination
        endpoint = analytics_data.get('paging', {}).get('next')

    return all_data


def fetch_page_summary(request):
    """
    Fetch Facebook Page Insights, store them in the Django model, and print the data.
    """
    fb_oauth_details = get_fb_oauth_details(request)
    if not fb_oauth_details:
        return {"error": "OAuth details not found"}

    access_token = fb_oauth_details['access_token']
    page_id = fb_oauth_details['instagram_account']  # Instagram account ID
    email = fb_oauth_details['email']

    # Define the API endpoint and parameters
    API_VERSION = 'v22.0'
    endpoint = f'https://graph.facebook.com/{API_VERSION}/{page_id}'
    params = {
        'access_token': access_token,
        'fields': 'id, name, username, followers_count, follows_count, media_count, website, profile_picture_url, biography'
    }

    response = requests.get(endpoint, params=params)
    analytics_data = response.json()

    if "error" in analytics_data:
        return {"error": analytics_data["error"].get("message", "Unknown error")}

    # Print fetched data
    print("Fetched Instagram Page Insights:")
    for key, value in analytics_data.items():
        print(f"{key}: {value}")

    # Store data in Django model
    instance, created = InstagramPageStatisticsLifetime.objects.update_or_create(
        id=analytics_data['id'],
        defaults={
            "name": analytics_data['name'],
            "email": email,
            "username": analytics_data['username'],
            "followers_count": analytics_data['followers_count'],
            "follows_count": analytics_data['follows_count'],
            "media_count": analytics_data['media_count'],
            "website": analytics_data.get('website', ''),  # Handle missing fields
            "profile_picture_url": analytics_data.get('profile_picture_url', ''),
            "biography": analytics_data.get('biography', ''),
            "created_at": datetime.now().date(),
            "data_created_date":datetime.now().date(),  # Store the current date
            "data_created_time":datetime.now().strftime('%H:%M:%S'),  # Store the current time
        }
    )

    return analytics_data

# Combined API View to call both Instagram and Facebook Insights functions
class FetchSocialMediaInsightsView(APIView):
    """
    API endpoint to fetch both Instagram and Facebook insights and save them in the database.
    """
    def get(self, request):
        # Fetch data
        start_time = time.time()  # Start the timer

        instagram_data = fetch_instagram_insights(request)
        instagram_Page_insigths = fetch_insta_page_insights(request)
        instagram_Page_statitsics = fetch_page_summary(request)

        end_time = time.time()  # End the timer
        execution_time = end_time - start_time  # Calculate total execution time

        # If no data is returned, handle it gracefully
        if not instagram_data and not instagram_Page_insigths and not instagram_Page_statitsics:
            return Response({"message": "No data available"}, status=status.HTTP_204_NO_CONTENT)

        return Response({
            "message": "Data fetched successfully",
            "Instagram Media": instagram_data,
            "Instagram Page Insights": instagram_Page_insigths,
            "Instagram Page Stats": instagram_Page_statitsics,
            "Execution Time" : execution_time
        }, status=status.HTTP_200_OK)