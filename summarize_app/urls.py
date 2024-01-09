from django.urls import path
from .views import *
urlpatterns = [
    path('', summarize_pdf, name='summarize_pdf'),

    #api
    path('api1/', PdfSummaryAPIView.as_view(), name='api_summarize_pdf'),
]

