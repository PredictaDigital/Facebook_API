from django.db import models

class FBAdsInsight(models.Model):
    email = models.EmailField(max_length=50)
    account_id = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    ad_id = models.CharField(max_length=50)
    ad_name = models.CharField(max_length=255)
    adset_id = models.CharField(max_length=50)
    adset_name = models.CharField(max_length=255)
    campaign_id = models.CharField(max_length=50)
    campaign_name = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    objective = models.CharField(max_length=100)
    account_currency = models.CharField(max_length=3)
    clicks = models.IntegerField(default=0)
    cpc = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpm = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpp = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    impressions = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    frequency = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    unique_ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    data_created_date = models.CharField(max_length=255)
    data_created_time = models.CharField(max_length=255)


    class Meta:
        db_table = 'FB_Ads_Insights'

# FB Ads Insights Model by age & Gender
class FBAdsInsightAgeGender(models.Model):
    email = models.EmailField(max_length=50)
    account_id = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    ad_id = models.CharField(max_length=50)
    ad_name = models.CharField(max_length=255)
    adset_id = models.CharField(max_length=50)
    adset_name = models.CharField(max_length=255)
    campaign_id = models.CharField(max_length=50)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    campaign_name = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    objective = models.CharField(max_length=100)
    account_currency = models.CharField(max_length=3)
    clicks = models.IntegerField(default=0)
    cpc = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpm = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpp = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    impressions = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    frequency = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    unique_ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    data_created_date = models.CharField(max_length=255)
    data_created_time = models.CharField(max_length=255)


    class Meta:
        db_table = 'FB_Ads_Insights_by_age_gender'


# FB Ads Insights Model by age & Gender
class FBAdsInsightByDevice(models.Model):
    email = models.EmailField(max_length=50)
    account_id = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    ad_id = models.CharField(max_length=50)
    ad_name = models.CharField(max_length=255)
    adset_id = models.CharField(max_length=50)
    adset_name = models.CharField(max_length=255)
    campaign_id = models.CharField(max_length=50)
    impression_device = models.CharField(max_length=100)
    device_platform = models.CharField(max_length=100)
    campaign_name = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    objective = models.CharField(max_length=100)
    account_currency = models.CharField(max_length=3)
    clicks = models.IntegerField(default=0)
    cpc = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpm = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpp = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    impressions = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    frequency = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    unique_ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    data_created_date = models.CharField(max_length=255)
    data_created_time = models.CharField(max_length=255)


    class Meta:
        db_table = 'FB_Ads_Insights_by_device'


# FB Ads Insights Model by age & Gender
class FBAdsInsightByLocation(models.Model):
    email = models.EmailField(max_length=50)
    account_id = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    ad_id = models.CharField(max_length=50)
    ad_name = models.CharField(max_length=255)
    adset_id = models.CharField(max_length=50)
    adset_name = models.CharField(max_length=255)
    campaign_id = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    campaign_name = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    objective = models.CharField(max_length=100)
    account_currency = models.CharField(max_length=3)
    clicks = models.IntegerField(default=0)
    cpc = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpm = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    cpp = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    impressions = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    frequency = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    unique_ctr = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    data_created_date = models.CharField(max_length=255)
    data_created_time = models.CharField(max_length=255)


    class Meta:
        db_table = 'FB_Ads_Insights_by_location'


# FB Ads Insights Model by Campaign
class FacebookCampaignInsight(models.Model):
    email = models.CharField(max_length=255)
    campaign_name = models.CharField(max_length=255)
    objective = models.CharField(max_length=255)
    status = models.CharField(max_length=255, blank=True)
    campaign_id = models.CharField(max_length=255)
    account_id = models.CharField(max_length=255)
    created_time = models.CharField(max_length=255)
    updated_time = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    stop_time = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=255, blank=True)
    effective_status = models.CharField(max_length=255, blank=True)
    clicks = models.IntegerField()
    cpc = models.DecimalField(max_digits=10, decimal_places=2)
    cpm = models.DecimalField(max_digits=10, decimal_places=2)
    ctr = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.DecimalField(max_digits=10, decimal_places=2)
    impressions = models.IntegerField()
    reach = models.IntegerField()
    spend = models.DecimalField(max_digits=10, decimal_places=2)
    data_created_date = models.CharField(max_length=255)
    data_created_time = models.CharField(max_length=255)


    class Meta:
        db_table = 'FB_campaign_insights'

#Facebook Followers
class FacebookFollowersInsight(models.Model):
    Id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    email = models.CharField(max_length=255)
    page_id = models.CharField(max_length=255)
    EndTime = models.DateTimeField()       # Stores the end time for the metric
    PageFollows = models.IntegerField()    # Stores the number of page followers
    data_created_date = models.CharField(max_length=255)
    data_created_time = models.CharField(max_length=255)

    class Meta:
        db_table = 'FB_Followers_statistics'  # Table name in the database

#Facebook Followers by city
class FacebookFollowersbycity(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    page_id = models.CharField(max_length=255)  # Page ID as a string
    email = models.EmailField(max_length=255)   # Email field
    city = models.CharField(max_length=255)     # City name as a string
    follower_count = models.IntegerField()      # Follower count as an integer
    end_time = models.DateTimeField()           # End time as a DateTime field
    data_created_date = models.DateField()      # Date the data was created
    data_created_time = models.TimeField()      # Time the data was created

    class Meta:
        db_table = 'FB_Followers_by_city'  # Table name in the database


# Facebook Insight
class FacebookInsights(models.Model):
    page_id = models.CharField(max_length=255)  # Page ID as a string
    email = models.EmailField(max_length=255)   # Email field
    end_time = models.CharField(max_length=50)
    page_fans = models.CharField(max_length=50, null=True, blank=True)
    page_fan_adds = models.CharField(max_length=50, null=True, blank=True)
    page_fan_removes = models.CharField(max_length=50, null=True, blank=True)
    page_views_total = models.CharField(max_length=50, null=True, blank=True)
    page_video_views = models.CharField(max_length=50, null=True, blank=True)
    page_video_view_time = models.CharField(max_length=50, null=True, blank=True)
    page_video_views_paid = models.CharField(max_length=50, null=True, blank=True)
    page_video_views_organic = models.CharField(max_length=50, null=True, blank=True)
    page_video_views_click_to_play = models.CharField(max_length=50, null=True, blank=True)
    page_posts_impressions = models.CharField(max_length=50, null=True, blank=True)
    page_posts_impressions_paid = models.CharField(max_length=50, null=True, blank=True)
    page_posts_impressions_organic = models.CharField(max_length=50, null=True, blank=True)
    page_posts_impressions_viral = models.CharField(max_length=50, null=True, blank=True)
    page_posts_impressions_nonviral = models.CharField(max_length=50, null=True, blank=True)
    page_impressions = models.CharField(max_length=50, null=True, blank=True)
    page_impressions_unique = models.CharField(max_length=50, null=True, blank=True)
    page_impressions_paid = models.CharField(max_length=50, null=True, blank=True)
    page_impressions_viral = models.CharField(max_length=50, null=True, blank=True)
    page_impressions_nonviral = models.CharField(max_length=50, null=True, blank=True)
    page_post_engagements = models.CharField(max_length=50, null=True, blank=True)
    page_actions_post_reactions_like_total = models.CharField(max_length=50, null=True, blank=True)
    page_actions_post_reactions_anger_total = models.CharField(max_length=50, null=True, blank=True)
    page_actions_post_reactions_wow_total = models.CharField(max_length=50, null=True, blank=True)
    page_actions_post_reactions_haha_total = models.CharField(max_length=50, null=True, blank=True)
    page_actions_post_reactions_love_total = models.CharField(max_length=50, null=True, blank=True)
    page_actions_post_reactions_sorry_total = models.CharField(max_length=50, null=True, blank=True)
    data_created_date = models.DateField()      # Date the data was created
    data_created_time = models.TimeField()      # Time the data was created

    class Meta:
        db_table = 'FB_Insights'  # Table name in the database

# FB Post Insigths
class FBPostInsights(models.Model):
    post_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)   # Email field
    created_time = models.CharField(max_length=255, null=True, blank=True)
    full_picture = models.TextField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    permalink_url = models.TextField(null=True, blank=True)
    promotable_id = models.CharField(max_length=255, null=True, blank=True)
    timeline_visibility = models.CharField(max_length=255, null=True, blank=True)
    status_type = models.CharField(max_length=255, null=True, blank=True)
    promotion_status = models.CharField(max_length=255, null=True, blank=True)
    is_hidden = models.CharField(max_length=10, null=True, blank=True)
    is_published = models.CharField(max_length=10, null=True, blank=True)
    is_instagram_eligible = models.CharField(max_length=10, null=True, blank=True)
    updated_time = models.CharField(max_length=255, null=True, blank=True)
    post_impressions = models.CharField(max_length=255, null=True, blank=True)
    post_clicks = models.CharField(max_length=255, null=True, blank=True)
    post_reactions_like_total = models.CharField(max_length=255, null=True, blank=True)
    post_reactions_love_total = models.CharField(max_length=255, null=True, blank=True)
    post_reactions_wow_total = models.CharField(max_length=255, null=True, blank=True)
    post_reactions_haha_total = models.CharField(max_length=255, null=True, blank=True)
    post_reactions_sorry_total = models.CharField(max_length=255, null=True, blank=True)
    post_reactions_anger_total = models.CharField(max_length=255, null=True, blank=True)
    post_impressions_fan = models.CharField(max_length=255, null=True, blank=True)
    post_impressions_paid = models.CharField(max_length=255, null=True, blank=True)
    post_impressions_organic = models.CharField(max_length=255, null=True, blank=True)
    post_video_views = models.CharField(max_length=255, null=True, blank=True)
    post_impressions_viral = models.CharField(max_length=255, null=True, blank=True)
    post_impressions_nonviral = models.CharField(max_length=255, null=True, blank=True)
    post_video_views_organic = models.CharField(max_length=255, null=True, blank=True)
    post_video_views_paid = models.CharField(max_length=255, null=True, blank=True)
    post_video_avg_time_watched = models.CharField(max_length=255, null=True, blank=True)
    data_created_date = models.DateField()      # Date the data was created
    data_created_time = models.TimeField()      # Time the data was created

    class Meta:
        db_table = 'FBPostInsights'  # Table name in the database



class FB_Oauth(models.Model):
    access_token = models.CharField(max_length=255)
    page_id = models.CharField(max_length=255)
    instagram_account = models.CharField(max_length=255)
    business_profiles = models.JSONField()
    ad_accounts = models.CharField(max_length=255)  # Ensure this is a CharField
    email = models.EmailField()

    class Meta:
        db_table = 'FB_Oauth'  # Custom table name
    
    @classmethod
    def get_latest_token_by_email(cls, email):
        """
        Fetch the latest token entry for the given email.
        """
        return cls.objects.filter(email=email).order_by('-id').first()

   