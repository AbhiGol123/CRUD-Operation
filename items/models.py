from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    is_updated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    item = models.ForeignKey(Item, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, default='❓')

    def __str__(self):
        return f"{self.emoji} {self.text}"

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, default='🔹')

    def __str__(self):
        return f"{self.emoji} {self.text}"
