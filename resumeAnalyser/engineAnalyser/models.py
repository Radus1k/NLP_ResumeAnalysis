from django.db import models

# Create your models here.


class ResumeModel(models.Model):
    resume = models.FileField(upload_to='resumes/')
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
