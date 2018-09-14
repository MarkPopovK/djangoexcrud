from rest_framework import serializers
from .models import *


class PointSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TrackPoint
        fields = ('pk', 'start', 'owner', 'date')
