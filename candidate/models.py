from django.db import models
from django.contrib.auth.models import User
from hr.models import CandidateApplication, JobPost  
# Create your models here.
class MyApplyJobList(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # Corrected to ForeignKey: A user can apply for many jobs
    job = models.ForeignKey(to=CandidateApplication, on_delete=models.CASCADE)
    dateYouApply = models.DateField(auto_now_add=True)

class isSortList(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # Corrected to ForeignKey: A job can have many shortlisted candidates
    job = models.ForeignKey(to=JobPost, on_delete=models.CASCADE)
    dateYouApply = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + " " + str(self.job.title)



