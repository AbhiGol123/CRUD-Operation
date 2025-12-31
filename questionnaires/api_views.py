from rest_framework import viewsets
from rest_framework.response import Response
from .models import Questionnaire
from .serializers import QuestionnaireSerializer

class QuestionnaireViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Questionnaire.objects.all().prefetch_related('questions__options')
    serializer_class = QuestionnaireSerializer

    def list(self, request, *args, **kwargs):
        # Override list to return the requested envelope
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "success": True,
            "statusCode": 0,
            "path": request.path,
            "message": "Success",
            "metadata": {},
            "result": serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "success": True,
            "statusCode": 0,
            "path": request.path,
            "message": "Success",
            "metadata": {},
            "result": [serializer.data]
        })
