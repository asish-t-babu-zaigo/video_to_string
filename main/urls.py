from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload_video', video_to_text,name='upload_video'),
    path('<int:id>',my_view),

]