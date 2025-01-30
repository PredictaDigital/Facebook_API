import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FBPostInsights
from .utils import get_fb_oauth_details
# from .serializers import FBPostInsightsSerializer

GRAPH_API_VERSION = 'v22.0'
PAGE_ID = '109818058023623'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ENDPOINT = f"https://graph.facebook.com/v22.0/{PAGE_ID}/posts"

# Helper function to fetch the Page Access Token
def get_page_access_token(user_access_token, page_id):
    endpoint = f"https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_access_token}"
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        page_access_token = response.json().get("access_token")
        return page_access_token
    else:
        return None
    
class FetchFBPosts(APIView):
    def get(self, request, *args, **kwargs):

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

        url = f"https://graph.facebook.com/v22.0/{page_id}/posts"

        # Define the parameters for the request
        params = {
            'access_token': page_access_token,
            'fields': 'created_time,id,full_picture,icon,message,permalink_url,promotable_id,timeline_visibility,status_type,'
                      'promotion_status,is_hidden,is_published,is_instagram_eligible,updated_time,'
                      'insights.metric(post_impressions,post_clicks,post_reactions_like_total,post_video_views,'
                      'post_reactions_love_total,post_reactions_wow_total,post_reactions_haha_total,'
                      'post_reactions_sorry_total,post_reactions_anger_total,post_impressions_fan,'
                      'post_impressions_paid,post_impressions_organic,post_impressions_viral,post_impressions_nonviral,'
                      'post_video_views_organic,post_video_views_paid,post_video_avg_time_watched)',
            'period': 'lifetime'
        }

        def fetch_all_posts(endpoint, params):
            all_posts = []
            while True:
                response = requests.get(endpoint, params=params)
                data = response.json()

                all_posts.extend(data.get('data', []))

                # Check for pagination
                next_page = data.get('paging', {}).get('next')
                if not next_page:
                    break
                endpoint = next_page
                params = {}

            return all_posts

        # Fetch the posts from the Facebook Graph API
        all_posts = fetch_all_posts(url, params)

        # Save posts to the database
        posts_to_save = []
        for item in all_posts:
            insights = item.get('insights', {}).get('data', [])
            post_impressions = next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_impressions'), 0)
            post_clicks = next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_clicks'), 0)
            post_reactions_like_total = next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_reactions_like_total'), 0)
            # Repeat for other metrics as needed

            # post = FBPostInsights(
            #     created_time=item.get("created_time"),
            #     post_id=item.get("id"),
            #     full_picture=item.get("full_picture"),
            #     icon=item.get("icon"),
            #     message=item.get("message"),
            #     permalink_url=item.get("permalink_url"),
            #     promotable_id=item.get("promotable_id"),
            #     timeline_visibility=item.get("timeline_visibility"),
            #     status_type=item.get("status_type"),
            #     promotion_status=item.get("promotion_status"),
            #     is_hidden=item.get("is_hidden"),
            #     is_published=item.get("is_published"),
            #     is_instagram_eligible=item.get("is_instagram_eligible"),
            #     updated_time=item.get("updated_time"),
            #     post_impressions=post_impressions,
            #     post_clicks=post_clicks,
            #     post_reactions_like_total=post_reactions_like_total,
            #     post_reactions_love_total=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_reactions_love_total'), 0),
            #     post_reactions_wow_total=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_reactions_wow_total'), 0),
            #     post_reactions_haha_total=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_reactions_haha_total'), 0),
            #     post_reactions_sorry_total=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_reactions_sorry_total'), 0),
            #     post_reactions_anger_total=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_reactions_anger_total'), 0),
            #     post_impressions_fan=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_impressions_fan'), 0),
            #     post_impressions_paid=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_impressions_paid'), 0),
            #     post_impressions_organic=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_impressions_organic'), 0),
            #     post_video_views=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_video_views'), 0),
            #     post_impressions_viral=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_impressions_viral'), 0),
            #     post_impressions_nonviral=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_impressions_nonviral'), 0),
            #     post_video_views_organic=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_video_views_organic'), 0),
            #     post_video_views_paid=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_video_views_paid'), 0),
            #     post_video_avg_time_watched=next((insight['values'][0]['value'] for insight in insights if insight['name'] == 'post_video_avg_time_watched'), 0)
            # )
            # posts_to_save.append(post)

        # Bulk create all the posts
        # FBPostInsights.objects.bulk_create(posts_to_save)

        return Response({'message': 'Data fetched and saved successfully.'}, status=status.HTTP_200_OK)
