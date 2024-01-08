import PyPDF2
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openai

from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

def summarize_pdf(request):
    configure()
    summary_text = None

    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']

        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

        openai.api_key = os.getenv('api_key')
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=150,
            temperature=0.7
        )
        summary_text = response['choices'][0]['text']

    return render(request, 'summarize.html', {'summary_text': summary_text})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PdfSummarySerializer

class PdfSummaryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        configure()
        serializer = PdfSummarySerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['pdf_file']

            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

            openai.api_key = os.getenv('api_key')
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=text,
                max_tokens=150,
                temperature=0.7
            )
            summary_text = response['choices'][0]['text']

            return Response({'summary_text': summary_text}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)