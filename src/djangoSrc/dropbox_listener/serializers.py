from .models import DropBoxListener
from rest_framework import serializers


class DropBoxListenerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DropBoxListener
        fields = ['listen']
