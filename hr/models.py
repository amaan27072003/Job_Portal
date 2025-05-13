from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Hr(models.Model):
    user = models.OneToOneField(to = User, on_delete=models.CASCADE)

class JobPost(models.Model):
    user = models.ForeignKey(to = User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    companyName = models.CharField(max_length=200)
    salaryLow = models.IntegerField(default=0)
    salaryHigh = models.IntegerField(default=0)
    applycount = models.IntegerField(default=0)
    lastDateToApply = models.DateField()

    def __str__(self):
        return str(self.title)

STATUS_CHOICES = (
    ('pending', 'pending'),
    ('selected', 'selected'),
)

class CandidateApplication(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    job = models.OneToOneField(to=JobPost, on_delete=models.CASCADE)
    passingYear = models.IntegerField()
    yearOfExp = models.IntegerField(default=0)
    resume = models.FileField(upload_to='resume/')
    status = models.CharField(choices = STATUS_CHOICES, max_length=20, default='pending')

    def __str__(self):
        return str(self.user.username)+" "+str(self.job.title)

class SelectedCandidate(models.Model):
    job = models.ForeignKey(to = JobPost, on_delete=models.CASCADE)
    candidate = models.OneToOneField(to = CandidateApplication, on_delete=models.CASCADE)
   
    
