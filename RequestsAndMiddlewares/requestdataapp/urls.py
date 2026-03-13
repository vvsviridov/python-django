from django.urls import path

from .views import process_get_view, user_bio_view, upload_file_view

app_name = 'requestdataapp'

urlpatterns = [
    path("get/", process_get_view, name="get-view"),
    path("bio/", user_bio_view, name="bio-form"),
    path("upload/", upload_file_view, name="file-upload"),
]
