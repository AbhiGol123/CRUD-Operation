from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import QuestionnaireViewSet

router = DefaultRouter()
router.register(r'questionnaires', QuestionnaireViewSet, basename='api-questionnaire')

urlpatterns = [
    path('', include(router.urls)),
]
