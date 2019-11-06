
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import TemplateHTMLRenderer
from audio_transcription.serializers import AudioFilesSerializer, UserSerializer, GroupSerializer

from .models import AudioFiles
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from helpers import constants
from helpers import google_service as gs


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
    http_method_names = ['get', 'put']



class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file_str = request.FILES['file']
        filename, file_extension = os.path.splitext(file_str.name)

        # check if file type is a supported audio, if not respond with an error
        if file_extension not in constants.SUPPORTED_AUDIO_ENCODING:
            return Response(status=406)

        # Upload file !import because some files needs to be converted to wav
        path = default_storage.save(file_str.name, ContentFile(file_str.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        # transcribe using the uploaded file
        transcription = gs.transcribe_audio(tmp_file, 'en_US')
        print(transcription)
        # return the transcription
        # do some stuff with uploaded file
        return Response(status=204)


# @api_view(['POST'])
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#
#     serializer = SnippetSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
