from rest_framework import serializers

class PdfSummarySerializer(serializers.Serializer):
    pdf_file = serializers.FileField()
