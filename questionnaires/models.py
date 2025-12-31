from django.db import models

class Questionnaire(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='questionnaires/', blank=True, null=True)
    final_statement = models.TextField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class QuestionnaireQuestion(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, default='❓')

    def __str__(self):
        return self.text

class QuestionnaireOption(models.Model):
    question = models.ForeignKey(QuestionnaireQuestion, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, default='😊')

    def __str__(self):
        return f"{self.emoji} {self.text}"
