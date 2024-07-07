from rest_framework import serializers
from .models import FAQ, Slider, Stream


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'image', 'created_at', 'updated_at']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'faq', 'answer',
                  'is_active', 'created_at', 'updated_at']


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['room_id', 'room_name', 'user_name', 'cover_image']
