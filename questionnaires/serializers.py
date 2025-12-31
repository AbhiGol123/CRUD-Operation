from rest_framework import serializers
from .models import Questionnaire, QuestionnaireQuestion, QuestionnaireOption
import json

class QuestionnaireOptionSerializer(serializers.ModelSerializer):
    assessment_question_id = serializers.UUIDField(source='question.id', read_only=True)
    content = serializers.CharField(source='text')
    emoji_code = serializers.CharField(source='emoji')
    
    class Meta:
        model = QuestionnaireOption
        fields = ['id', 'assessment_question_id', 'content', 'emoji_code', 'created_at', 'updated_at']

class QuestionnaireQuestionSerializer(serializers.ModelSerializer):
    assessment_id = serializers.UUIDField(source='questionnaire.id', read_only=True)
    content = serializers.CharField(source='text')
    assessment_question_answers = QuestionnaireOptionSerializer(source='options', many=True)
    archived_at = serializers.SerializerMethodField()

    class Meta:
        model = QuestionnaireQuestion
        fields = ['id', 'assessment_id', 'content', 'created_at', 'updated_at', 'archived_at', 'assessment_question_answers']

    def get_archived_at(self, obj):
        return {} # As requested in example

class QuestionnaireSerializer(serializers.ModelSerializer):
    is_draft = serializers.SerializerMethodField(read_only=True)
    published = serializers.SerializerMethodField(read_only=True)
    active = serializers.SerializerMethodField(read_only=True)
    image_file_name = serializers.SerializerMethodField(read_only=True)
    image_fingerprint = serializers.SerializerMethodField(read_only=True)
    image_updated_at = serializers.DateTimeField(source='updated_at', read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    last_answered_at = serializers.SerializerMethodField(read_only=True)
    assessment_questions = QuestionnaireQuestionSerializer(source='questions', many=True)

    class Meta:
        model = Questionnaire
        fields = [
            'id', 'title', 'description', 'final_statement', 'is_draft', 'published', 'active',
            'image_file_name', 'image_fingerprint', 'image_updated_at', 'created_at', 'updated_at',
            'image', 'last_answered_at', 'assessment_questions'
        ]

    def get_is_draft(self, obj):
        return obj.status == 'inactive'

    def get_published(self, obj):
        return obj.status == 'active'

    def get_active(self, obj):
        return obj.status == 'active'

    def get_image_file_name(self, obj):
        return obj.image.name if obj.image else ""

    def get_image_fingerprint(self, obj):
        return "" # Placeholder

    def get_image(self, obj):
        if not obj.image:
            return {"medium": "", "thumb": ""}
        return {
            "medium": obj.image.url,
            "thumb": obj.image.url # Use same for now
        }

    def get_last_answered_at(self, obj):
        return obj.updated_at # Placeholder

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        questionnaire = Questionnaire.objects.create(**validated_data)
        
        for q_data in questions_data:
            options_data = q_data.pop('options', [])
            question = QuestionnaireQuestion.objects.create(questionnaire=questionnaire, **q_data)
            for o_data in options_data:
                QuestionnaireOption.objects.create(question=question, **o_data)
        
        return questionnaire
