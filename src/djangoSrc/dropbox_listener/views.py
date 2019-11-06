
from rest_framework import viewsets
from rest_framework.response import Response
from .models import DropBoxListener
from .serializers import DropBoxListenerSerializer


# Create your views here.
class DropBoxViewSet(viewsets.ModelViewSet):
    """
    API endpoint that start/close a listener in one of the dropbox fields
    """
    queryset = DropBoxListener.objects.all()
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
        count = 0
        while self._keep_runnning:
            print("running " + str(count))
            count += 1
            sleep(1)

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




