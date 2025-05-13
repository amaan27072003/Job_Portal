from django.shortcuts import render , redirect
from hr.models import JobPost , CandidateApplication , SelectedCandidate , Hr
from django.contrib.auth.decorators import login_required
from candidate.models import isSortList


@login_required
def hrHome_views(request):
    # if Hr.objects.filter(user=request.user).exists():
        jobposts = JobPost.objects.filter(user=request.user)
        print(jobposts)
        return render(request, 'hr/hrdashboard.html' , {'jobposts': jobposts})
    # return redirect('candidate_dashboard')
   
@login_required   
def post_job_views(request):
    mssg = None
    if request.method == 'POST':    
        job_title = request.POST.get('job-title')
        address = request.POST.get('address')
        company_name = request.POST.get('company-name')
        salary_low = request.POST.get('salary-low')
        salary_high = request.POST.get('salary-high')
        last_date = request.POST.get('last-date')
        # mssg = 'Job Posted Successfully'
        Job_Post = JobPost(user=request.user, title=job_title, address=address, companyName=company_name, salaryLow=salary_low, salaryHigh=salary_high, lastDateToApply=last_date)
        Job_Post.save()
        mssg = 'Job Posted Successfully' # new code added. 
        return render(request,'hr/postjob.html',{'mssg':mssg})#new code added.
    return render(request, 'hr/postjob.html', {'mssg': mssg})  

@login_required
def candidate_view(request,pk):
    if JobPost.objects.filter(id=pk).exists():
        job = JobPost.objects.get(id=pk)
        applications = CandidateApplication.objects.filter(job=job)
        selectedCandidate = SelectedCandidate.objects.filter(job=job)
        print(selectedCandidate)
        # return render(request, 'hr/candidate.html', {'applications': applications , 'selectedapplication': selectedCandidate, 'jobpost':job }) 
        return render(request, 'hr/candidate.html', {'applications': applications,'job':job , 'selectedCandidate': selectedCandidate })
    
    return render('hr_dash')                                                 
    # return redirect('hr_dash')


@login_required
def selectCandidate(request):
    if request.method == 'POST':
        candidateid = request.POST.get('candidateid')
        jobpostid = request.POST.get('jobpostid')
        candidate = CandidateApplication.objects.get(id= candidateid)
        # job = JobPost.objects.get(id = jobpostid)
    #     SelectedCandidate(job=job,candidate=candidate).save()
    #     return redirect('hr_dash')
    # return redirect('hr_dash')  

        # new code
        jobpost = JobPost.objects.get(id = jobpostid)   
        if SelectedCandidate.objects.filter(candidate=candidate).exists()==False:
            SelectedCandidate(job=jobpost,candidate=candidate).save()
            isSortList(user=candidate.user,job=jobpost).save() 
        # return redirect(f'/candidate_details/{jobpostid}/') 
        # return redirect('candidate_details')
        return redirect('/candidate_details/'+str(jobpostid)+"/")
    return redirect('hr_dash')
        
    


@login_required
def deleteCandidate(request):
    if request.method == 'POST':
        candidateid = request.POST.get('candidateid')
        jobpostid = request.POST.get('jobpostid')
        job = JobPost.objects.get(id = jobpostid)
        CandidateApplication.objects.get(id= candidateid).delete()
        job.applycount = job.applycount -1
        job.save()

    return redirect('hr_dash')