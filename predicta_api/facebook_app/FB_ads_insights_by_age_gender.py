import requests
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FBAdsInsightAgeGender
from .utils import get_fb_oauth_details  # Import the utility function
import json
import time

class FetchAdInsightsViewbyAgeGender(APIView):
    def get(self, request):
        email = request.COOKIES.get('email') 
        fb_details = get_fb_oauth_details(email)

        if not fb_details:
            return Response({"error": "No details found for the given email"}, status=status.HTTP_404_NOT_FOUND)

        access_token = fb_details.get("access_token")
        ad_account = fb_details.get("ad_account")

        if not access_token or not ad_account:
            return Response({"error": "Access token or ad account ID is missing."}, status=status.HTTP_400_BAD_REQUEST)

        created_at = 'null'
        if FBAdsInsightAgeGender.objects.filter(email=email).exists():
            latest_insight = FBAdsInsightAgeGender.objects.filter(email=email).latest('data_created_date')
            created_at = latest_insight.data_created_date

        today = datetime.today()
        if created_at != 'null':  
            FBAdsInsightAgeGender.objects.filter(email=email).delete()
            sincedates = today - timedelta(weeks=160.774)
        else:
            sincedates = today - timedelta(weeks=160.774)

        sincedate = sincedates.strftime('%Y-%m-%d')

        time_range = {"since": sincedate, "until": today.strftime('%Y-%m-%d')}
        url = f"https://graph.facebook.com/v22.0/{ad_account}/insights"

        fields = [
            'ad_id', 'ad_name', 'adset_id', 'adset_name', 'campaign_id', 'campaign_name', 'account_id', 'account_name',
            'reach', 'impressions', 'clicks', 'spend', 'frequency', 'account_currency', 'buying_type', 'unique_ctr',
            'ctr', 'cpc', 'cpm', 'cpp', 'objective', 'created_time', 'updated_time'
        ]
        
        breakdowns = ['age', 'gender']
        url_with_params = f"{url}?fields={','.join(fields)}&time_range={json.dumps(time_range)}&level=ad&access_token={access_token}&breakdowns={','.join(breakdowns)}&limit=50000"

        all_insights = []
        while url_with_params:
            response = requests.get(url_with_params)
            if response.status_code != 200:
                return Response({"error": "Failed to fetch insights", "details": response.json()}, status=status.HTTP_400_BAD_REQUEST)

            data = response.json()
            insights = data.get("data", [])
            all_insights.extend(insights)

            url_with_params = data.get("paging", {}).get("next", None)

        for insight in all_insights:
            FBAdsInsightAgeGender.objects.create(
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
                data_created_date=today.strftime('%Y-%m-%d'),
                data_created_time=time.strftime("%H:%M:%S"),
                age=insight.get("age", 'null'),
                gender=insight.get("gender", 'null'),
            )

        return Response({"message": "Insights fetched successfully.", "total_records": len(all_insights)}, status=status.HTTP_200_OK)
