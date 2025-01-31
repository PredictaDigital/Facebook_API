from rest_framework import serializers
from .models import FacebookCampaignInsight

class FacebookCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookCampaignInsight
        fields = '__all__'
