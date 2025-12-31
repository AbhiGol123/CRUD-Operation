from rest_framework import viewsets
from .models import Item, Question, Option
from .serializers import ItemSerializer, QuestionSerializer, OptionSerializer

class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return Item.objects.using('postgresql').filter(status='published').prefetch_related('questions__options')
    
    serializer_class = ItemSerializer
