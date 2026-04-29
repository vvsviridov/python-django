from django.urls import path
from .views import hw_view, GroupListView


app_name = 'myaapiapp'

urlpatterns = [
    path('hello/', hw_view, name='hello'),
    path('groups/', GroupListView.as_view(), name='groups'),
]
