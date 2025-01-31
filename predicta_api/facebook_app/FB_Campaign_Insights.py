from rest_framework.response import Response
from rest_framework.views import APIView
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from datetime import timedelta
from datetime import datetime
import time
from .utils import get_fb_oauth_details  # Import the utility function
from rest_framework import status
from .models import FacebookCampaignInsight
import requests

class FetchAdInsightsByCampaigns(APIView):
    def get(self, request):
        email = request.COOKIES.get('email')
        fb_details = get_fb_oauth_details(email)

        if not fb_details:
            return Response({"error": "No details found for the given email"}, status=status.HTTP_404_NOT_FOUND)

        # Store the details in individual variables (if needed)
        access_token = fb_details.get("access_token")
        ad_account = fb_details.get("ad_account")

        if not access_token or not ad_account:
            return Response(
                {"error": "Access token or ad account ID is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if any insights exist for the given email
        created_at = 'null'
        if FacebookCampaignInsight.objects.filter(email=email).exists():
            # Fetch the latest insight for the given email
            latest_insight = FacebookCampaignInsight.objects.filter(email=email).latest('data_created_date')
            created_at = latest_insight.data_created_date

        # Get today's date dynamically
        today = datetime.today()

        if created_at != 'null':  # Check if created_at is not null
            # delete existing data
            FacebookCampaignInsight.objects.filter(email=email).delete()
            now = datetime.today()
            # Subtract 36 months (approximately 3 years)
            sincedates = now - timedelta(weeks=160.774)  # Rough estimate (36 months)
            sincedate = sincedates.strftime('%Y-%m-%d')
        else:  # Calculate the date 36 months ago if created_at is null
            now = datetime.today()
            # Subtract 36 months (approximately 3 years)
            sincedates = now - timedelta(weeks=160.774)  # Rough estimate (36 months)
            sincedate = sincedates.strftime('%Y-%m-%d')

        # Initialize API
        FacebookAdsApi.init('385745461007462', '39838a1fd0b95af866f368acc81f77b0', access_token)
        ad_account = AdAccount(ad_account)

        # Define Fields
        fields = [
            'name', 'objective', 'status', 'id', 'account_id',
            'created_time', 'updated_time', 'buying_type', 'start_time',
            'stop_time', 'effective_status'
        ]

        metrics = ['clicks', 'cpc', 'cpm', 'ctr', 'impressions', 'reach', 'spend', 'frequency']

        today = datetime.today()
        time_range = {"since": sincedate, "until": today.strftime('%Y-%m-%d')}
        current_time = time.strftime("%H:%M:%S")

        # Initialize an empty list to hold all campaigns
        all_campaigns = []

        # Fetch the campaigns with pagination
        campaigns = ad_account.get_campaigns(fields=fields)

        # Process each page of campaigns
        while True:
            # Add the current page's campaigns to the all_campaigns list
            all_campaigns.extend(campaigns)

            # If there is another page, fetch the next page
            if 'paging' in campaigns and 'next' in campaigns['paging']:
                # Fetch the next page of campaigns
                campaigns = requests.get(campaigns['paging']['next']).json()
            else:
                break  # Stop if there are no more pages

        # Initialize an empty list to hold insights data
        all_insights_data = []

        # For each campaign, fetch its insights separately
        for campaign in all_campaigns:
            # Fetch insights for the campaign
            campaign_id = campaign.get('id')
            print(campaign_id)
            insights = campaign.get_insights(fields=metrics, params={'time_range': time_range})
            print(insights)

            # Check if insights is None or empty and handle it
            if not insights:
                # If insights is empty or None, create a default dict with 0 for all fields
                insights = [{
                    'clicks': 0,
                    'cpc': 0,
                    'cpm': 0,
                    'ctr': 0,
                    'impressions': 0,
                    'reach': 0,
                    'spend': 0,
                    'frequency': 0
                }]

            # Process each page of insights
            while True:
                for insight in insights:
                    # Store insights in the database
                    FacebookCampaignInsight.objects.create(
                        email=email,
                        campaign_name=campaign.get('name', ''),
                        objective=campaign.get('objective', ''),
                        status=campaign.get('status', ''),
                        campaign_id=campaign.get('id', ''),
                        account_id=campaign.get('account_id', ''),
                        created_time=campaign.get('created_time', today),
                        updated_time=campaign.get('updated_time', today),
                        start_time=campaign.get('start_time', today),
                        stop_time=campaign.get('stop_time', today),
                        buying_type=campaign.get('buying_type', ''),
                        effective_status=campaign.get('effective_status', ''),
                        clicks=insight.get('clicks', 0),
                        cpc=insight.get('cpc', 0),
                        cpm=insight.get('cpm', 0),
                        ctr=insight.get('ctr', 0),
                        frequency=insight.get('frequency', 0),
                        impressions=insight.get('impressions', 0),
                        reach=insight.get('reach', 0),
                        spend=insight.get('spend', 0),
                        data_created_date=today.strftime('%Y-%m-%d'),
                        data_created_time=current_time
                    )
                    # Append the insights to the response data
                    all_insights_data.append({
                        'campaign_name': campaign.get('name', ''),
                        'objective': campaign.get('objective', ''),
                        'status': campaign.get('status', ''),
                        'campaign_id': campaign.get('id', ''),
                        'account_id': campaign.get('account_id', ''),
                        'created_time': campaign.get('created_time', today),
                        'updated_time': campaign.get('updated_time', today),
                        'start_time': campaign.get('start_time', today),
                        'stop_time': campaign.get('stop_time', today),
                        'buying_type': campaign.get('buying_type', ''),
                        'effective_status': campaign.get('effective_status', ''),
                        'clicks': insight.get('clicks', 0),
                        'cpc': insight.get('cpc', 0),
                        'cpm': insight.get('cpm', 0),
                        'ctr': insight.get('ctr', 0),
                        'frequency': insight.get('frequency', 0),
                        'impressions': insight.get('impressions', 0),
                        'reach': insight.get('reach', 0),
                        'spend': insight.get('spend', 0),
                        'data_created_date': today.strftime('%Y-%m-%d'),
                        'data_created_time': current_time
                    })

                # Check if there are more pages of insights
                if 'paging' in insights and 'next' in insights['paging']:
                    insights = requests.get(insights['paging']['next']).json()  # Fetch the next page of insights
                else:
                    break  # Exit the loop if no more pages

        # Return the collected insights data as a response
        return Response(all_insights_data)
