
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from audio_transcription.serializers import AudioFilesSerializer, UserSerializer, GroupSerializer
from .models import AudioFiles


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AudioFilesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Audios to be viewed or edited.
    """
    queryset = AudioFiles.objects.all()
    serializer_class = AudioFilesSerializer
