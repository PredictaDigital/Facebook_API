# facebook_app/urls.py

from django.urls import path
from .views import GetAdAccountUsers
from .FacebookOAuth import FacebookOAuth,GetLatestTokenView
from .FacebookCallback import FacebookCallback
from .CustomerData import CustomerData
from .FB_get_token import RetrieveFBDetailsView
from .FB_Ads_Insights import FetchAdInsightsView
from .FB_ads_insights_by_age_gender import FetchAdInsightsViewbyAgeGender
from .FB_Ads_insights_by_device import FetchAdInsightsByDeviceView
from .FB_Ads_insights_by_location import FetchAdInsightsBylocation
from .FB_Campaign_Insights import FetchAdInsightsByCampaigns
from .FB_Followers_Statistics import FetchFollowersStatistics
from .FB_Followers_by_City import FetchFollowersCity
from .FB_Insights import FetchFBPageInsigths
from .FB_Posts_Insights import FetchFBPosts

urlpatterns = [
    path('facebook_oauth/', FacebookOAuth.as_view(), name='facebook_oauth'),
    path('callback/', FacebookCallback.as_view(), name='facebook_callback'),
    path('customer/<str:email>/', CustomerData.as_view(), name='get_customer_data_by_email'),
    path('get_ad_account_users/', GetAdAccountUsers.as_view(), name='get_ad_account_users'),
    path('get-token/', RetrieveFBDetailsView.as_view(), name='get_latest_token'),
    path('facebook_ads-insights/', FetchAdInsightsView.as_view(), name='get_ads_insights'),
    path('facebook_ads-insights-age-gender/', FetchAdInsightsViewbyAgeGender.as_view(), name='get_ads_insights_by_age_gnder'),
    path('facebook_ads-insights-device/', FetchAdInsightsByDeviceView.as_view(), name='get_ads_insights_by_device'),
    path('facebook_ads-insights-location/', FetchAdInsightsBylocation.as_view(), name='get_ads_insights_by_location'),
    path('facebook_campaign-insights/', FetchAdInsightsByCampaigns.as_view(), name='get_campaign_insights'),
    path('facebook_get-followers/', FetchFollowersStatistics.as_view(), name='get_followers'),
    path('facebook_get-followers-city/', FetchFollowersCity.as_view(), name='get_followers_city'),
    path('facebook_get-page-insigths/', FetchFBPageInsigths.as_view(), name='get_followers_city'),
    path('facebook_get-posts-insigths/', FetchFBPosts.as_view(), name='get_post'),
    #path('token/save', StoreFBData.as_view(), name='store-fb-data'),
]
