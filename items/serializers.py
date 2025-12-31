from rest_framework import serializers
from .models import Item, Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'emoji']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'emoji', 'options']

class ItemSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'price', 'email', 
            'mobile_number', 'image', 'status', 'is_updated', 
            'created_at', 'questions'
        ]
