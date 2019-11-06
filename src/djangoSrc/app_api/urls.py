from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from audio_transcription import views
from dropbox_listener import views as v_dropbox
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'audioFiles', views.AudioFilesViewSet)
router.register(r'dropboxListener', v_dropbox.DropBoxViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('transcribe/', views.FileUploadView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
