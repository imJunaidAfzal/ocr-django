from django.urls import path
from . import views

# APP_NAME = 'ocr_api'
urlpatterns = [
    path('', views.ImageToText.as_view(), name='img_to_text'),
    path('search/', views.SearchText.as_view(), name='search'),
    path('replace/', views.SearchAndReplaceText.as_view(), name='search_replace'),
    path('download/', views.DownloadOutput.as_view(), name='download'),
]
