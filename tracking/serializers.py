from rest_framework import serializers

class TrackingSerializer(serializers.Serializer):
    tracking_number = serializers.CharField(max_length=50)
