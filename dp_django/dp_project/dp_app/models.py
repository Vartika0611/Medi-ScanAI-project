from django.contrib.auth.models import User
from django.db import models


from django.db import models
from django.contrib.auth.models import User

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=255)
    predicted_disease = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_disease}"


from django.db import models

class History(models.Model):
    fever = models.IntegerField()
    headache = models.IntegerField()
    nausea = models.IntegerField()
    vomiting = models.IntegerField()
    fatigue = models.IntegerField()
    joint_pain = models.IntegerField()
    skin_rash = models.IntegerField()
    cough = models.IntegerField()
    weight_loss = models.IntegerField()
    yellow_eyes = models.IntegerField()
    predicted_disease = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_disease} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
    
    from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"



from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name