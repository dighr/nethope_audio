from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import AudioFiles


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AudioFilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioFiles
        fields = ['id', 'filename', 'timestamp', 'phonenumber', 'transcription', 'translation', 'processed']
        read_only_fields = ['id', 'filename', 'timestamp', 'phonenumber', 'transcription', 'translation']



