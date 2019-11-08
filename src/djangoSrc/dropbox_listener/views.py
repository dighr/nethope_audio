
from rest_framework import viewsets
from rest_framework.response import Response
from .models import DropBoxListener as dbl
from .serializers import DropBoxListenerSerializer
from .DropBoxListener import DropBoxListener
from helpers import google_service,  utils


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


from threading import Thread
from time import sleep

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
        # dl = DropBoxListener()
        # dl.download_all_file()
        # output_files = dl.get_output_files()

        output_files = ['./Downloads/0c20191010153015n+8009378997_0.amr',
         './Downloads/0c20191010153327n18778669045_0.amr',
         './Downloads/0c20191010155022n7879579094_0.amr']
        for file in output_files:
            # Send transcription request, add them to a file
            transcript_response = google_service.transcribe_audio(file, 'es-ES')
            print(transcript_response)
            # Save the transcribed file in a bucket in google cloud

            # Send translation request, add them to another file
            paragraph = utils.transcript_response_to_paragraph(transcript_response)
            translation = google_service.translate_text_from(paragraph, 'es', 'en')

            print(translation)
            # Send the translation in a bucket in google cloud

            # add the appropriate values into the db
            pass

        # count = 0
        # while self._keep_runnning:
        #     print("running " + str(count))
        #     count += 1
        #     sleep(1)

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




