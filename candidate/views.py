from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from hr.models import JobPost , CandidateApplication , Hr
from candidate.models import MyApplyJobList

# Create your views here.
@login_required
def candidate_dashboard(request):
    jobpost = JobPost.objects.all()
    # if Hr.objects.filter(user=request.user).exists():   
        # return redirect('hr_dash')
    # jobs = JobPost.objects.all()
    # print(jobs)
    return render(request,'candidate/dashboard.html', {'jobpost': jobpost})

@login_required
def myJobListviews(request):
    # if Hr.objects.filter(user=request.user).exists():
    #     return redirect('hr_dash')
    myjobList = MyApplyJobList.objects.filter(user=request.user)
    print(myjobList)
    return render(request,'candidate/myjoblist.html', {'myjobList': myjobList})

@login_required
def applyforjob(request,pk):
   
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            college = request.POST.get('college')
            passing_year = request.POST.get('passing_year')
            yearOfExperience = request.POST.get('yearOfExperience')
            resume = request.FILES.get('resume')
            
            job = JobPost.objects.get(id=pk)
            if CandidateApplication.objects.filter(user=request.user,job=job).exists():
                return redirect('candidate_dashboard')
            candidate_application = CandidateApplication(user=request.user, job=job, passingYear=passing_year, yearOfExp=yearOfExperience, resume=resume)
            candidate_application.save()

            MyApplyJobList(user=request.user,job=candidate_application).save()
            return redirect('candidate_dashboard')
        return render(request, 'candidate/apply.html')
