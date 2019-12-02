import os
from rest_framework import viewsets
from rest_framework.response import Response
from .models import DropBoxListener as dbl
from .DropBoxListener import DropBoxListener, file_exists
from audio_transcription.models import AudioFiles
from .serializers import DropBoxListenerSerializer
from helpers import google_service,  utils, constants
from threading import Thread


# Create your views here.
class DropBoxViewSet(viewsets.ModelViewSet):
    """
    API endpoint that start/close a listener in one of the dropbox fields
    """
    queryset = dbl.objects.all()
    serializer_class = DropBoxListenerSerializer
    http_method_names = ['get', 'put', 'options']

    def update(self, request, *args, **kwargs):
        value = request.data['listen']
        if value is None or int(value) > 1 or int(value) < 0:
            return Response(status=404)

        Handle().handle(int(value))

        return super().update(request, *args, **kwargs)


# singlton class
class Handle:
    _thread = None
    _instance = None
    _keep_runnning = True

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(Handle, self).__new__(
                self, *args, **kwargs)
        return self._instance

    def threaded_function(self, arg):

            # Download all files if they don't exist locally or in the db
            dl = DropBoxListener()
            dl.download_all_file()
            output_files = dl.get_output_files()
            files = dl.files

            print('starting')
            for index, file in enumerate(output_files):
                try:
                    # Send transcription request, add them to a file
                    transcript_response = google_service.transcribe_audio(file, 'es-US')
                    transcript_text = utils.get_transcript(transcript_response)
                    print(transcript_text)
                    # Save the transcribed file in a bucket in google cloud
                    transcript_destination = self.save_to_bucket(transcript_text, files[index], constants.AUDIOS_TRANSCRIPTION)

                    # Send translation request, add them to another file
                    paragraph = utils.transcript_response_to_paragraph(transcript_response)
                    translation = google_service.translate_text_from(paragraph, 'es', 'en')

                    # Send the translation in a bucket in google cloud
                    translation_destination = self.save_to_bucket(translation, files[index], constants.AUDIOS_TRANSLATION)

                    # extract other values from file name
                    filename = os.path.basename(files[index]).split('.')[0]
                    epoch, phonenumber = utils.extract_info_from_name(filename)

                    # add the appropriate values into the db
                    if not file_exists(files[index]):
                        new_record = AudioFiles(filename=files[index], transcription=transcript_destination,
                                                translation=translation_destination, timestamp=epoch,
                                                phonenumber=phonenumber, processed=1)
                        new_record.save()

                except Exception as e:
                    print(e)

    def save_to_bucket(self, text, file_name, bucket):
        destination_name = os.path.splitext(file_name)[0] + '.txt'
        destination_name = destination_name.replace('/', '-')

        text_file = open('./tmp/tmp.txt', 'w')
        if type(text) == list:
            for t in text:
                text_file.write(t + '\n')
        else:
            text_file.write(str(text))
        text_file.close()

        google_service.upload_to_bucket(bucket, './tmp/tmp.txt', destination_name)

        return bucket + '/' + destination_name

    def handle(self, value):
        if self._thread is None or (not self._thread.is_alive()):
            self._thread = Thread(target=self.threaded_function, args=(10,))

        if value == 1 and (not self._thread.is_alive()):
            self._keep_runnning = True
            self._thread.start()

        if value == 0:
            self._keep_runnning = False
            self._thread = None
        # destroy the thread if the given value is not 0

        pass




