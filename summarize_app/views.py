from django.shortcuts import render
from django.http import HttpResponse
import openai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

def summarize_pdf(request):
    configure()
    summary_text = None

    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']       
        text = extract_text_from_pdf(pdf_file)        
        openai.api_key = os.getenv('api_key')
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"need the summary of the below text\n\n{text}",
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        summary_text = response['choices'][0]['text']
    return render(request, 'summarize_pdf.html', {'summary_text': summary_text})

def extract_text_from_pdf(pdf_file):
    configure()    
    text = ''
    try:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    except Exception as e:        
        print(f"Error extracting text from PDF: {e}")
    return text


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PdfSummarySerializer

class PdfSummaryAPIView(APIView):
    configure()
    def post(self, request, *args, **kwargs):
        serializer = PdfSummarySerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['pdf_file']
            text = extract_text_from_pdf(pdf_file)
            
            openai.api_key = os.getenv('api_key')
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"need the summary of the below text\n\n{text}",
                temperature=0.7,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            summary_text = response['choices'][0]['text']
            return Response({'summary_text': summary_text}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
