from django.contrib import admin
from hr import models
# Register your models here.

@admin.register(models.Hr)
class HrAdmin(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(models.JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','address','companyName','salaryLow', 'salaryHigh','applycount','lastDateToApply')    

@admin.register(models.CandidateApplication)
class CandidateApplicationAdmin(admin.ModelAdmin):
    list_display = ('id','user','job')    

@admin.register(models.SelectedCandidate)
class SelectedCandidateAdmin(admin.ModelAdmin):
        list_display = ('id','job','candidate')