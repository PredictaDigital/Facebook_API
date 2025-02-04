from django.db import models
import requests


class InstagramMediaInsight(models.Model):
    ig_id = models.CharField(max_length=50, unique=True, verbose_name="Instagram Post ID")
    post_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="Post Date")  # Stored as text
    email = models.CharField(max_length=255)
    media_type = models.CharField(max_length=50, verbose_name="Media Type")
    comments_count = models.CharField(max_length=20, default="0", verbose_name="Comments Count")  # Converted to text
    like_count = models.CharField(max_length=20, default="0", verbose_name="Like Count")  # Converted to text
    permalink = models.CharField(max_length=500, verbose_name="Permalink")
    username = models.CharField(max_length=100, verbose_name="Username")
    caption = models.TextField(null=True, blank=True, verbose_name="Caption")
    media_product_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Media Product Type")
    is_comment_enabled = models.CharField(max_length=10, default="True", verbose_name="Comments Enabled")  # Stored as "True"/"False"
    media_url = models.CharField(max_length=500, null=True, blank=True, verbose_name="Media URL")

    # Insights (Stored as text)
    impressions = models.CharField(max_length=20, default="0", verbose_name="Impressions")
    reach = models.CharField(max_length=20, default="0", verbose_name="Reach")
    profile_visits = models.CharField(max_length=20, default="0", verbose_name="Profile Visits")
    profile_activity = models.CharField(max_length=20, default="0", verbose_name="Profile Activity")
    replies = models.CharField(max_length=20, default="0", verbose_name="Replies")
    saved = models.CharField(max_length=20, default="0", verbose_name="Saved")
    video_views = models.CharField(max_length=20, default="0", verbose_name="Video Views")
    shares = models.CharField(max_length=20, default="0", verbose_name="Shares")
    total_interactions = models.CharField(max_length=20, default="0", verbose_name="Total Interactions")
    follows = models.CharField(max_length=20, default="0", verbose_name="Follows")

    created_at = models.CharField(max_length=100, verbose_name="Created At")  # Stored as text
    updated_at = models.CharField(max_length=100, verbose_name="Updated At")  # Stored as text

    data_created_date = models.CharField(max_length=255)
    data_created_time = models.CharField(max_length=255)


    class Meta:
        db_table = 'Instagram_Media_Insights'


class InstagramPageInsight(models.Model):
    end_time = models.DateTimeField()  # End time of the insights
    follower_count = models.IntegerField(default=0)  # Follower count
    impressions = models.IntegerField(default=0)  # Impressions
    reach = models.IntegerField(default=0)  # Reach
    page_id = models.CharField(max_length=255)  # Facebook Page ID
    email = models.EmailField(max_length=254)  # Email of the user
    data_created_date = models.DateField(auto_now_add=True)  # Date when data was created
    data_created_time = models.TimeField(auto_now_add=True)  # Time when data was created

    class Meta:
        db_table = 'Instagram_Page_Insight'


class InstagramPageStatisticsLifetime(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # Instagram Page ID
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    followers_count = models.CharField(max_length=50)  # Changed to CharField
    follows_count = models.CharField(max_length=50)  # Changed to CharField
    media_count = models.CharField(max_length=50)  # Changed to CharField
    website = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField
    profile_picture_url = models.CharField(max_length=500)
    biography = models.CharField(max_length=2000)  # Changed to CharField
    created_at = models.CharField(max_length=50)  # Store timestamp as a string
    email = models.EmailField(max_length=254)  # Email of the user
    data_created_date = models.DateField(auto_now_add=True)  # Date when data was created
    data_created_time = models.TimeField(auto_now_add=True)  # Time when data was created

    class Meta:
        db_table = 'Instagram_Page_Statistics_Lifetime'



