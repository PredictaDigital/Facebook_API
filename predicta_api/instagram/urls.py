from django.urls import path
from .views import FetchSocialMediaInsightsView

urlpatterns = [
    path('fetch-instagram-insights/', FetchSocialMediaInsightsView.as_view(), name='fetch-instagram-insights'),
]
