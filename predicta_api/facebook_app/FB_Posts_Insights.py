import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FBPostInsights
from .utils import get_fb_oauth_details
from django.utils.timezone import now

def get_page_access_token(user_access_token, page_id):
    endpoint = f"https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_access_token}"
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        return response.json().get("access_token")
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

        page_access_token = get_page_access_token(user_access_token, page_id)

        if not page_access_token:
            return Response({"error": "Failed to retrieve Page Access Token."}, status=status.HTTP_400_BAD_REQUEST)

        url = f"https://graph.facebook.com/v22.0/{page_id}/posts"
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
                next_page = data.get('paging', {}).get('next')
                if not next_page:
                    break
                endpoint = next_page
                params = {}
            return all_posts

        all_posts = fetch_all_posts(url, params)

        def get_insight_value(insights, metric_name):
            return next((insight['values'][0]['value'] for insight in insights if insight['name'] == metric_name), 0)

        existing_posts = {post.post_id: post for post in FBPostInsights.objects.filter(post_id__in=[p["id"] for p in all_posts])}
        new_posts = []
        updated_posts = []

        for item in all_posts:
            insights = item.get('insights', {}).get('data', [])

            post_data = {
                "email": email,
                "created_time": item.get("created_time"),
                "full_picture": item.get("full_picture"),
                "icon": item.get("icon"),
                "message": item.get("message"),
                "permalink_url": item.get("permalink_url"),
                "promotable_id": item.get("promotable_id"),
                "timeline_visibility": item.get("timeline_visibility"),
                "status_type": item.get("status_type"),
                "promotion_status": item.get("promotion_status"),
                "is_hidden": item.get("is_hidden"),
                "is_published": item.get("is_published"),
                "is_instagram_eligible": item.get("is_instagram_eligible"),
                "updated_time": item.get("updated_time"),
                "post_impressions": get_insight_value(insights, 'post_impressions'),
                "post_clicks": get_insight_value(insights, 'post_clicks'),
                "post_reactions_like_total": get_insight_value(insights, 'post_reactions_like_total'),
                "post_reactions_love_total": get_insight_value(insights, 'post_reactions_love_total'),
                "post_reactions_wow_total": get_insight_value(insights, 'post_reactions_wow_total'),
                "post_reactions_haha_total": get_insight_value(insights, 'post_reactions_haha_total'),
                "post_reactions_sorry_total": get_insight_value(insights, 'post_reactions_sorry_total'),
                "post_reactions_anger_total": get_insight_value(insights, 'post_reactions_anger_total'),
                "post_impressions_fan": get_insight_value(insights, 'post_impressions_fan'),
                "post_impressions_paid": get_insight_value(insights, 'post_impressions_paid'),
                "post_impressions_organic": get_insight_value(insights, 'post_impressions_organic'),
                "post_video_views": get_insight_value(insights, 'post_video_views'),
                "post_impressions_viral": get_insight_value(insights, 'post_impressions_viral'),
                "post_impressions_nonviral": get_insight_value(insights, 'post_impressions_nonviral'),
                "post_video_views_organic": get_insight_value(insights, 'post_video_views_organic'),
                "post_video_views_paid": get_insight_value(insights, 'post_video_views_paid'),
                "post_video_avg_time_watched": get_insight_value(insights, 'post_video_avg_time_watched'),
                "data_created_date": now().date(),
                "data_created_time": now().time()
            }

            post_id = item.get("id")
            if post_id in existing_posts:
                existing_post = existing_posts[post_id]
                for key, value in post_data.items():
                    setattr(existing_post, key, value)
                updated_posts.append(existing_post)
            else:
                new_posts.append(FBPostInsights(post_id=post_id, **post_data))

        if new_posts:
            FBPostInsights.objects.bulk_create(new_posts)

        if updated_posts:
            FBPostInsights.objects.bulk_update(updated_posts, [
                "email", "created_time", "full_picture", "icon", "message", "permalink_url", "promotable_id",
                "timeline_visibility", "status_type", "promotion_status", "is_hidden", "is_published", 
                "is_instagram_eligible", "updated_time", "post_impressions", "post_clicks",
                "post_reactions_like_total", "post_reactions_love_total", "post_reactions_wow_total",
                "post_reactions_haha_total", "post_reactions_sorry_total", "post_reactions_anger_total",
                "post_impressions_fan", "post_impressions_paid", "post_impressions_organic",
                "post_video_views", "post_impressions_viral", "post_impressions_nonviral",
                "post_video_views_organic", "post_video_views_paid", "post_video_avg_time_watched",
                "data_created_date", "data_created_time"
            ])

        return Response({
            'message': f'Posts fetched successfully. {len(new_posts)} new, {len(updated_posts)} updated.',
            'data': all_posts
        }, status=status.HTTP_200_OK)
