from django.shortcuts import render , redirect ,  get_object_or_404
from hr.models import JobPost , CandidateApplication , SelectedCandidate , Hr
from django.contrib.auth.decorators import login_required
from candidate.models import isSortList
from django.urls import reverse


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
def candidate_view(request, pk):
    # This line attempts to get the JobPost or raises a 404 error if it doesn't exist
    job = get_object_or_404(JobPost, id=pk)

    applications = CandidateApplication.objects.filter(job=job)
    selectedCandidate = SelectedCandidate.objects.filter(job=job)

    return render(request, 'hr/candidate.html', {
        'applications': applications,
        'job': job,
        'selectedCandidate': selectedCandidate
    })


@login_required
def selectCandidate(request):
    if request.method == 'POST':
        candidateid_str = request.POST.get('candidateid')
        jobpostid_str = request.POST.get('jobpostid')

        try:
            candidate = get_object_or_404(CandidateApplication, id=candidateid_str)
            jobpost = get_object_or_404(JobPost, id=jobpostid_str)
        except (ValueError, TypeError):
            return redirect('hr_dash')

        if not SelectedCandidate.objects.filter(candidate=candidate).exists():
            # Create a new SelectedCandidate entry
            SelectedCandidate(job=jobpost, candidate=candidate).save()
            
            # --- This is the new, crucial code to update the status ---
            candidate.status = 'selected'
            candidate.save()
            # --------------------------------------------------------

            isSortList(user=candidate.user, job=jobpost).save()

        # Corrected redirect using the 'reverse' function
        return redirect(reverse('candidate_details', kwargs={'pk': jobpost.id}))
    
    return redirect('hr_dash')
    


@login_required
def deleteCandidate(request):
    if request.method == 'POST':
        candidateid_str = request.POST.get('candidateid')
        jobpostid_str = request.POST.get('jobpostid')
        
        try:
            # Use get_object_or_404 for safer object retrieval
            candidate = get_object_or_404(CandidateApplication, id=candidateid_str)
            job = get_object_or_404(JobPost, id=jobpostid_str)
        except (ValueError, TypeError):
            # Handles cases where the ID is not a number
            return redirect('hr_dash')
            
        candidate.delete()
        job.applycount = job.applycount - 1
        job.save()

    return redirect('hr_dash')