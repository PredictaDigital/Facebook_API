import requests
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FBAdsInsightByLocation
from .utils import get_fb_oauth_details
import json
import time

class FetchAdInsightsBylocation(APIView):
    def get(self, request):
        # Fetch the access token and ad account ID using the utility function
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
        if FBAdsInsightByLocation.objects.filter(email=email).exists():
            # Fetch the latest insight for the given email
            latest_insight = FBAdsInsightByLocation.objects.filter(email=email).latest('data_created_date')
            created_at = latest_insight.data_created_date

        # Get today's date dynamically
        today = datetime.today()

        if created_at != 'null':  # Check if created_at is not null
            # delete existing data
            FBAdsInsightByLocation.objects.filter(email=email).delete()
            now = datetime.today()
            # Subtract 36 months (approximately 3 years)
            sincedates = now - timedelta(weeks=160.774)  # Rough estimate (36 months)
            sincedate = sincedates.strftime('%Y-%m-%d')
        else:  # Calculate the date 36 months ago if created_at is null
            now = datetime.today()
            # Subtract 36 months (approximately 3 years)
            sincedates = now - timedelta(weeks=160.774)  # Rough estimate (36 months)
            sincedate = sincedates.strftime('%Y-%m-%d')

        print("Until date:", sincedate)

        current_time = time.strftime("%H:%M:%S")
        time_range = {"since": sincedate, "until": today.strftime('%Y-%m-%d')}

        # Facebook Graph API endpoint
        url = f"https://graph.facebook.com/v22.0/{ad_account}/insights"

        # Fields and parameters, including breakdowns for country and region
        fields = [
            'ad_id', 'ad_name', 'adset_id', 'adset_name', 'campaign_id', 'campaign_name', 'account_id', 'account_name',
            'reach', 'impressions', 'clicks', 'spend', 'frequency', 'account_currency', 'buying_type', 'unique_ctr',
            'ctr', 'cpc', 'cpm', 'cpp', 'objective', 'created_time', 'updated_time'
        ]
        
        # Breakdown parameters for country and region
        breakdowns = ['country', 'region']
        
        # Set limit for how many records to fetch per request (Facebook Graph API typically has a max limit)
        limit = 1000  # Adjust this limit based on your needs
        
        # Construct the URL with query parameters directly
        url_with_params = f"{url}?fields={','.join(fields)}&breakdowns={','.join(breakdowns)}&time_range={json.dumps(time_range)}&level=ad&access_token={access_token}&limit={limit}"

        all_insights = []
        
        # Fetch insights data and handle pagination
        while url_with_params:
            response = requests.get(url_with_params)
            print("Status Code:", response.status_code)
            print("Response Content:", response.text)

            if response.status_code != 200:
                return Response(
                    {"error": "Failed to fetch insights", "details": response.json()},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Parse the current page of insights
            data = response.json()
            insights = data.get("data", [])
            all_insights.extend(insights)

            # Check if there is a next page (pagination)
            url_with_params = data.get("paging", {}).get("next", None)

            # Optional: Delay to avoid hitting rate limits (e.g., 1 second)
            time.sleep(1)

        print(f"Total records fetched: {len(all_insights)}")

        # Save all insights to the database (including breakdowns for country and region)
        for insight in all_insights:
            FBAdsInsightByLocation.objects.create(
                account_id=insight.get("account_id"),
                account_name=insight.get("account_name"),
                email=email,
                ad_id=insight.get("ad_id"),
                ad_name=insight.get("ad_name"),
                adset_id=insight.get("adset_id"),
                adset_name=insight.get("adset_name"),
                campaign_id=insight.get("campaign_id"),
                campaign_name=insight.get("campaign_name"),
                buying_type=insight.get("buying_type"),
                created_time=insight.get("created_time"),
                updated_time=insight.get("updated_time"),
                objective=insight.get("objective"),
                account_currency=insight.get("account_currency"),
                clicks=insight.get("clicks", 0),
                cpc=insight.get("cpc", 0.0),
                cpm=insight.get("cpm", 0.0),
                cpp=insight.get("cpp", 0.0),
                ctr=insight.get("ctr", 0.0),
                impressions=insight.get("impressions", 0),
                reach=insight.get("reach", 0),
                spend=insight.get("spend", 0.0),
                frequency=insight.get("frequency", 0.0),
                unique_ctr=insight.get("unique_ctr", 0.0),
                country=insight.get("country", 'null'),
                region=insight.get("region", 'null'),
                data_created_date=today.strftime('%Y-%m-%d'),
                data_created_time=current_time
            )

        # Prepare the response data
        response_data = {
            "message": "Insights fetched successfully.",
            "data": all_insights,
            "ldata": created_at,
            "untill": sincedate
        }

        return Response(response_data, status=status.HTTP_200_OK)
