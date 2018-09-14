from rest_framework import serializers
from .models import *


class PointSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    random = serializers.ReadOnlyField(source='test')

    class Meta:
        model = TrackPoint
        fields = ('pk', 'start', 'owner', 'date', 'random')
