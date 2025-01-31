import requests
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FBAdsInsightByDevice  
from .utils import get_fb_oauth_details
import json
import time

class FetchAdInsightsByDeviceView(APIView):
    def get(self, request):
        email = request.COOKIES.get('email')
        fb_details = get_fb_oauth_details(email)

        if not fb_details:
            return Response({"error": "No details found for the given email"}, status=status.HTTP_404_NOT_FOUND)

        access_token = fb_details.get("access_token")
        ad_account = fb_details.get("ad_account")

        if not access_token or not ad_account:
            return Response({"error": "Access token or ad account ID is missing."}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.today()
        start_date = today - timedelta(days=36 * 30)  # Fetch data for last 3 years (approx.)

        fields = [
            'ad_id', 'ad_name', 'adset_id', 'adset_name', 'campaign_id', 'campaign_name', 'account_id', 'account_name',
            'reach', 'impressions', 'clicks', 'spend', 'frequency', 'account_currency', 'buying_type', 'unique_ctr',
            'ctr', 'cpc', 'cpm', 'cpp', 'objective', 'created_time', 'updated_time'
        ]
        
        breakdowns = ['impression_device', 'device_platform']
        base_url = f"https://graph.facebook.com/v22.0/{ad_account}/insights"

        all_insights = []
        current_time = time.strftime("%H:%M:%S")

        # Fetch data day by day to avoid missing insights
        date = start_date
        while date <= today:
            sincedate = date.strftime('%Y-%m-%d')
            untildate = (date + timedelta(days=1)).strftime('%Y-%m-%d')

            print(f"Fetching data for: {sincedate} to {untildate}")

            params = {
                "fields": ",".join(fields),
                "time_range": json.dumps({"since": sincedate, "until": untildate}),
                "level": "ad",
                "breakdowns": ",".join(breakdowns),
                "access_token": access_token,
                "limit": 5000  # Fetch up to 5000 records per request
            }

            url = base_url
            while url:
                response = requests.get(url, params=params if url == base_url else {})
                print("Fetching Insights:", url)
                print("Status Code:", response.status_code)

                if response.status_code != 200:
                    return Response(
                        {"error": "Failed to fetch insights", "details": response.json()},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                data = response.json()
                insights = data.get("data", [])
                all_insights.extend(insights)

                # Handle pagination
                url = data.get("paging", {}).get("next", None)

            # Move to the next day
            date += timedelta(days=1)

        print(f"Total records fetched: {len(all_insights)}")

        # Save insights to database
        for insight in all_insights:
            FBAdsInsightByDevice.objects.create(
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
                impression_device=insight.get("impression_device", ''),
                device_platform=insight.get("device_platform", ''),
                data_created_date=today.strftime('%Y-%m-%d'),
                data_created_time=current_time
            )

        return Response(
            {"message": "All insights fetched successfully.", "total_records": len(all_insights)},
            status=status.HTTP_200_OK
        )
