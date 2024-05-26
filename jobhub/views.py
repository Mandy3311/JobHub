from django.shortcuts import render, redirect,get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.core.exceptions import FieldError

from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from django.urls import reverse
from jobhub.models import ( PersonalInfo, ContactInfo, OtherInfo, Education, WorkExperience, ProjectExperience, UserProfile,
                            CompanyInfo, CompanyContactInfo, CompanyReview, IndividualReview, CompanyProfile,
                            JobSummary, JobHighlight, JobDetail, Job, Application)
from django.db.models import Q

from jobhub import forms
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json

@csrf_exempt 
def delete_experience(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        type = request.POST.get('type')
        if type == 'work-experience':
            try:
                work_experience = WorkExperience.objects.get(id=item_id)
                work_experience.delete()
                # get the user profile
                profile = UserProfile.objects.get(user=request.user)
                profile.work_experience.remove(work_experience)
                profile.save()
                return JsonResponse({'success': True})
            except WorkExperience.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Work experience not found.'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        elif type == 'project-experience':
            try:
                project_experience = ProjectExperience.objects.get(id=item_id)
                project_experience.delete()
                # get the user profile
                profile = UserProfile.objects.get(user=request.user)
                profile.project_experience.remove(project_experience)
                profile.save()
                return JsonResponse({'success': True})
            except ProjectExperience.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Project experience not found.'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        elif type == 'education':
            try:
                education = Education.objects.get(id=item_id)
                education.delete()
                # get the user profile
                profile = UserProfile.objects.get(user=request.user)
                profile.education.remove(education)
                profile.save()
                return JsonResponse({'success': True})
            except Education.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Education not found.'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
            
        return JsonResponse({'success': False, 'error': 'Invalid type.'})

@csrf_exempt 
def delete_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('user_id')
        try:
            staff = User.objects.get(id=staff_id)
            company_profile = CompanyProfile.objects.get(user=request.user)
            user_profile = UserProfile.objects.get(user=staff)
            company_profile.public_staff_list.remove(user_profile)
            company_profile.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            print("user not found")
            return JsonResponse({'success': False, 'error': 'User not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@csrf_exempt
def delete_review(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        company_user_id = request.POST.get('company_user_id')
        try:
            review = IndividualReview.objects.get(id=review_id)
            company_user = User.objects.get(id=company_user_id)
            company_profile = CompanyProfile.objects.get(user= company_user)
            # if the review's user is not the current user, return error
            if review.user != request.user:
                return JsonResponse({'success': False, 'error': 'You are not the author of this review.'})
            company_profile.individual_reviews.remove(review)
            
            _update_company_review(company_profile.company_review, company_profile.individual_reviews.all())
            company_profile.company_review.save()
            company_profile.save()
            return JsonResponse({'success': True, 'company_review': model_to_dict(company_profile.company_review)})
        except IndividualReview.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

# ================== Login and Register ==================
def  login(request):
    if request.method == "GET":
        form = forms.LoginForm()
        context = {'form': form}
        return render(request, "jobhub/login.html", context)
    
    form = forms.LoginForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        return render(request, "jobhub/login.html", context)
    

    user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
    if user is not None:
        auth_login(request, user)
        # Redirect to a success page.
        return redirect(reverse("base_user_profile"))
    
    # Return an 'invalid login' error message on form
    form.add_error(None, "Invalid username or password.")
    context = {'form': form}
    return render(request, "jobhub/login.html", context)        

def register(request):
    if request.method == "GET":
        form = forms.RegisterForm()
        context = {'form': form}
        return render(request, "jobhub/register.html", context)
    
    form = forms.RegisterForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        # print errorlist
        print(form.errors)
        return render(request, "jobhub/register.html", context)
    
    try:
        new_user = User.objects.create_user(username=form.cleaned_data["username"], 
                                            password=form.cleaned_data["password"], 
                                            email=form.cleaned_data["email"],
                                            first_name=form.cleaned_data["name"],
                                            last_name=form.cleaned_data["type"])
    except Exception as e:
        form.add_error(None, str(e))
        context = {'form': form}
        return render(request, "jobhub/register.html", context)
    
    new_user.save()

    if form.cleaned_data["type"] == "employer":

        company_info = CompanyInfo(name=getUserName(new_user),
                                    bio="A mysterious company.",
                                    industry="Unkown",
                                    size="Unkown Size"
                                    )
        company_info.save()
        company_contact_info = CompanyContactInfo(company=company_info,
                                    email=new_user.email,
                                    )
        company_contact_info.save()
        company_review = CompanyReview(company=company_info,
                                    user=new_user,
                                    overall_rating=0,
                                    interview_progression_rating=0,
                                    application_response_time_rating=0,
                                    benefits_during_interview_rating=0,
                                    interview_atmosphere_rating=0,
                                    interview_etiquette_rating=0,
                                    five_star_rating=0,
                                    four_star_rating=0,
                                    three_star_rating=0,
                                    two_star_rating=0,
                                    one_star_rating=0,
                                    )
        company_review.save()
        new_profile = CompanyProfile(
                                    user=new_user,
                                    company_info=company_info,
                                    company_contact_info=company_contact_info,
                                    company_review=company_review,
                                    picture=None,
                                    )
        new_profile.save()
    else:
        personal_info = PersonalInfo(name=getUserName(new_user),
                                    position="Unkown Position",
                                    bio="A mysterious person."
                                    )
        contact_info = ContactInfo(email=new_user.email)
        other_info = OtherInfo()
        other_info.save()
        personal_info.save()
        contact_info.save()

        new_profile = UserProfile(user=new_user,
                                    personal_info=personal_info,
                                    contact_info=contact_info,
                                    other_info=other_info,
                                    picture=None,
                                    )
        new_profile.save()

    user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
    if user is not None:
        auth_login(request, user)
        # Redirect to a success page.
        return _go_to_home_profile(request)
    form.add_error(None, "Successfully registered, but failed to login.")
    context = {'form': form}
    return render(request, "jobhub/register.html", context)

def getUserName(user):
    return user.first_name

def getUserType(user):
    return user.last_name

# log out function
def logout(request):
    auth_logout(request)
    return redirect(reverse("login"))

@login_required
@xframe_options_exempt
def base_user_profile(request):
    if getUserType(request.user) == "employer":
        return redirect(reverse("base_company_profile"))
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'profile': profile,
        'picture': profile.picture.url if profile.picture else None,
        'educations': profile.education.all(),
        'works': profile.work_experience.all(),
        'projects': profile.project_experience.all(),
        'applications': Application.objects.filter(user=request.user).order_by('-submitdate')[0:3]
    }

    if request.method == "GET":
        return render(request, "jobhub/base_user_profile.html", context)
    if "personal_info_submit" in request.POST:
        personalInfoForm = forms.PersonalInfoForm(request.POST)
        if not personalInfoForm.is_valid():
            context['form'] = personalInfoForm
            context['form_type'] = "personal_info"
            return render(request, "jobhub/base_user_profile.html", context)
        profile.personal_info.name = personalInfoForm.cleaned_data["editName"]
        request.user.first_name = personalInfoForm.cleaned_data["editName"]
        profile.personal_info.position = personalInfoForm.cleaned_data["editPosition"]
        profile.personal_info.company_name = personalInfoForm.cleaned_data["editCompany"]
        comapny_usernmae = personalInfoForm.cleaned_data["editCompanyId"]
        if comapny_usernmae != "":
            # search for user that match the username with company_usernmae and type is employer
            try:
                company_user = User.objects.get(username=comapny_usernmae, last_name="employer")
            except User.DoesNotExist:
                personalInfoForm.add_error("editCompanyId", "Company does not exist.")
                context['form'] = personalInfoForm
                context['form_type'] = "personal_info"
                return render(request, "jobhub/base_user_profile.html", context)
            profile.personal_info.company_id = company_user.id
        else:
            # try to remove the company_id
            profile.personal_info.company_id = None

        profile.personal_info.school = personalInfoForm.cleaned_data["editSchool"]
        profile.personal_info.bio = personalInfoForm.cleaned_data["editBio"]
        print( personalInfoForm.cleaned_data["editCompany"])

        if 'editPicture' in request.FILES:
            print("receive picture")
            profile.picture = request.FILES['editPicture']
        else:
            print("no picture")
        request.user.save()
        profile.personal_info.save()
        profile.save()
        context['profile'] = profile
        context['picture'] = profile.picture.url if profile.picture else None
        print(context['picture'])
    
    elif "contact_info_submit" in request.POST:
        contactInfoForm = forms.ContactInfoForm(request.POST)
        if not contactInfoForm.is_valid():
            context['form'] = contactInfoForm
            context['form_type'] = "contact_info"
            return render(request, "jobhub/base_user_profile.html", context)
        profile.contact_info.phone = contactInfoForm.cleaned_data["editPhone"]
        profile.contact_info.email = contactInfoForm.cleaned_data["editEmail"]
        profile.contact_info.address = contactInfoForm.cleaned_data["editAddress"]
        profile.contact_info.linkedin = contactInfoForm.cleaned_data["editLinkedIn"]
        if 'editResume' in request.FILES:
                profile.contact_info.resume = request.FILES['editResume']
        # profile.contact_info.resume = contactInfoForm.cleaned_data["editResume"]
        profile.contact_info.save()
        context['profile'] = profile
        # return render(request, "jobhub/base_user_profile.html", { "profile": profile
    
    if "skills_submit" in request.POST:
        skillsForm = forms.SkillsForm(request.POST)
        if not skillsForm.is_valid():
            context['form'] = skillsForm
            context['form_type'] = "skills"
            return render(request, "jobhub/base_user_profile.html", context)
        profile.other_info.skills = skillsForm.cleaned_data["editSkills"]
        profile.other_info.interests = skillsForm.cleaned_data["editInterests"]
        profile.other_info.save()
        context['profile'] = profile
        # return render(request, "jobhub/base_user_profile.html", { "profile": profile })

    if "education_add_submit" in request.POST:
        addEducationForm = forms.addEducationForm(request.POST)
        if not addEducationForm.is_valid():
            context['form'] = addEducationForm
            context['form_type'] = "education_" + addEducationForm.cleaned_data["addId"]
            return render(request, "jobhub/base_user_profile.html", context)
        id = addEducationForm.cleaned_data["addId"]# string type
        print('addEducation is valid')
        # use the id to get the education object if id > 0, return false if not exist
        if id != "-1":
            education = Education.objects.get(id=id)
            if education is None:
                addEducationForm.add_error(None, "Education does not exist.")
                context['form'] = addEducationForm
                context['form_type'] = "education_" + id
                return render(request, "jobhub/base_user_profile.html", context)
            # update the education object
            education.school = addEducationForm.cleaned_data["addSchool"]
            education.major = addEducationForm.cleaned_data["addMajor"]
            education.start_time = addEducationForm.cleaned_data["addStartDate"]
            education.gpa = addEducationForm.cleaned_data["addGPA"]
            education.end_time = addEducationForm.cleaned_data["addEndDate"]
            education.location = addEducationForm.cleaned_data["addLocation"]
            education.description = addEducationForm.cleaned_data["addDescription"]
            education.save()
        else:
            education = Education(school=addEducationForm.cleaned_data["addSchool"],
                                major=addEducationForm.cleaned_data["addMajor"],
                                gpa=addEducationForm.cleaned_data["addGPA"],
                                start_time=addEducationForm.cleaned_data["addStartDate"],
                                end_time=addEducationForm.cleaned_data["addEndDate"],
                                location=addEducationForm.cleaned_data["addLocation"],
                                description=addEducationForm.cleaned_data["addDescription"])
            education.save()
            profile.education.add(education)
            profile.save()
        context['profile'] = profile
        context['educations'] = profile.education.all()
    if "work_experience_add_submit" in request.POST:
        print("receive add")
        addWorkExperienceForm = forms.addWorkExperienceForm(request.POST)
        if not addWorkExperienceForm.is_valid():
            context['form'] = addWorkExperienceForm
            context['form_type'] = "work_" + addWorkExperienceForm.cleaned_data["addId"]
            print(addWorkExperienceForm.errors)
            return render(request, "jobhub/base_user_profile.html", context)
        id = addWorkExperienceForm.cleaned_data["addId"]
        print(id)
        # use the id to get the work_experience object if id > 0, return false if not exist
        if id != "-1":
            work_experience = WorkExperience.objects.get(id=id)
            if work_experience is None:
                addWorkExperienceForm.add_error(None, "Work experience does not exist.")
                context['form'] = addWorkExperienceForm
                context['form_type'] = "work_experience_" + id
                return render(request, "jobhub/base_user_profile.html", context)
            # update the work_experience object
            work_experience.company = addWorkExperienceForm.cleaned_data["addCompany"]
            work_experience.role = addWorkExperienceForm.cleaned_data["addRole"]
            work_experience.start_time = addWorkExperienceForm.cleaned_data["addStartDate"]
            work_experience.end_time = addWorkExperienceForm.cleaned_data["addEndDate"]
            work_experience.type = addWorkExperienceForm.cleaned_data["addType"]
            work_experience.description = addWorkExperienceForm.cleaned_data["addDescription"]
            work_experience.save()
        else:
            work_experience = WorkExperience(company=addWorkExperienceForm.cleaned_data["addCompany"],
                                role=addWorkExperienceForm.cleaned_data["addRole"],
                                start_time=addWorkExperienceForm.cleaned_data["addStartDate"],
                                end_time=addWorkExperienceForm.cleaned_data["addEndDate"],
                                type=addWorkExperienceForm.cleaned_data["addType"],
                                location=addWorkExperienceForm.cleaned_data["addLocation"],
                                description=addWorkExperienceForm.cleaned_data["addDescription"])
            work_experience.save()
            profile.work_experience.add(work_experience)
            profile.save()
        context['profile'] = profile
        context['works'] = profile.work_experience.all()
    if "project_add_submit" in request.POST:
        print("receive add")
        addProjectExperienceForm = forms.addProjectExperienceForm(request.POST)
        if not addProjectExperienceForm.is_valid():
            context['form'] = addProjectExperienceForm
            context['form_type'] = "project_" + addProjectExperienceForm.cleaned_data["addId"]
            print(addProjectExperienceForm.errors)
            return render(request, "jobhub/base_user_profile.html", context)
        id = addProjectExperienceForm.cleaned_data["addId"]
        print("role: ", addProjectExperienceForm.cleaned_data["addRole"])
        # use the id to get the project_experience object if id > 0, return false if not exist
        if id != "-1":
            project_experience = ProjectExperience.objects.get(id=id)
            if project_experience is None:
                addProjectExperienceForm.add_error(None, "Project experience does not exist.")
                context['form'] = addProjectExperienceForm
                context['form_type'] = "project_experience_" + id
                return render(request, "jobhub/base_user_profile.html", context)
            # update the project_experience object
            project_experience.project_name = addProjectExperienceForm.cleaned_data["addProject"]
            project_experience.role = addProjectExperienceForm.cleaned_data["addRole"]
            project_experience.start_time = addProjectExperienceForm.cleaned_data["addStartDate"]
            project_experience.end_time = addProjectExperienceForm.cleaned_data["addEndDate"]
            project_experience.location = addProjectExperienceForm.cleaned_data["addLocation"]
            project_experience.description = addProjectExperienceForm.cleaned_data["addDescription"]
            project_experience.save()
        else:
            project_experience = ProjectExperience(project_name=addProjectExperienceForm.cleaned_data["addProject"],
                                role= addProjectExperienceForm.cleaned_data["addRole"],
                                start_time=addProjectExperienceForm.cleaned_data["addStartDate"],
                                end_time=addProjectExperienceForm.cleaned_data["addEndDate"],
                                location=addProjectExperienceForm.cleaned_data["addLocation"],
                                description=addProjectExperienceForm.cleaned_data["addDescription"])
            project_experience.save()
            profile.project_experience.add(project_experience)
            profile.save()

        context['profile'] = profile
        context['projects'] = profile.project_experience.all()

        # return render(request, "jobhub/base_user_profile.html", { "profile": profile })
    # default
    return render(request, "jobhub/base_user_profile.html", context)

@login_required
@xframe_options_exempt
def base_company_profile(request):
    if getUserType(request.user) != "employer":
        return redirect(reverse("base_user_profile"))

    profile = CompanyProfile.objects.get(user=request.user)
    context = {
        'profile': profile,
        'picture': profile.picture.url if profile.picture else None,
        'staff_list': profile.public_staff_list.all(),
        'individual_reviews': profile.individual_reviews.all(),
        'jobs':list(Job.objects.filter(company_id=profile.id).order_by('-summary__post_time')[:3]),
    }
    print(list(Job.objects.filter(company_id=profile.id).order_by('-summary__post_time')[:3]))

    if request.method == "GET":
        return render(request, "jobhub/base_company_profile.html", context)
    if "company_info_submit" in request.POST:
        companyInfoForm = forms.CompanyInfoForm(request.POST)
        if not companyInfoForm.is_valid():
            context['form'] = companyInfoForm
            context['form_type'] = "company_info"
            return render(request, "jobhub/base_company_profile.html", context)
        profile.company_info.name = companyInfoForm.cleaned_data["editName"]
        request.user.first_name = companyInfoForm.cleaned_data["editName"]
        profile.company_info.industry = companyInfoForm.cleaned_data["editIndustry"]
        profile.company_info.size = companyInfoForm.cleaned_data["editSize"]
        profile.company_info.bio = companyInfoForm.cleaned_data["editBio"]

        if 'editPicture' in request.FILES:
            profile.picture = request.FILES['editPicture']

        request.user.save()
        profile.company_info.save()
        profile.save()
        context['profile'] = profile
        context['picture'] = profile.picture.url if profile.picture else None
    
    if "company_contact_info_submit" in request.POST:
        companyContactInfoForm = forms.CompanyContactInfoForm(request.POST)
        if not companyContactInfoForm.is_valid():
            context['form'] = companyContactInfoForm
            context['form_type'] = "company_contact_info"
            return render(request, "jobhub/base_company_profile.html", context)
        profile.company_contact_info.phone = companyContactInfoForm.cleaned_data["editPhone"]
        profile.company_contact_info.email = companyContactInfoForm.cleaned_data["editEmail"]
        profile.company_contact_info.address = companyContactInfoForm.cleaned_data["editAddress"]
        profile.company_contact_info.website = companyContactInfoForm.cleaned_data["editWebsite"]
        profile.company_contact_info.linkedin = companyContactInfoForm.cleaned_data["editLinkedIn"]
        profile.company_contact_info.save()
        context['profile'] = profile    

    if "company_staff_list_submit" in request.POST:
        addStaffForm = forms.addStaffForm(request.POST)
        if not addStaffForm.is_valid():
            context['form'] = addStaffForm
            context['form_type'] = "company_staff_list"
            return render(request, "jobhub/base_company_profile.html", context)
        username = addStaffForm.cleaned_data["addStaff"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            addStaffForm.add_error("addStaff", "User does not exist.")

            context['form'] = addStaffForm
            context['form_type'] = "company_staff_list"
            return render(request, "jobhub/base_company_profile.html", context)
        # find the user profile
        user_profile = UserProfile.objects.get(user=user)
        profile.public_staff_list.add(user_profile)
        profile.save()
        context['profile'] = profile
        context['staff_list'] = profile.public_staff_list.all()

    return render(request, "jobhub/base_company_profile.html", context)

def _go_to_home_profile(request):
    if getUserType(request.user) == "employer":
        return redirect(reverse("base_company_profile"))
    return redirect(reverse("base_user_profile"))

@login_required
@xframe_options_exempt
def other_user_profile(request):
    # if post, not allowed
    print('other_user_profile')
    if request.method == "GET":
        applicant_id = request.GET.get("applicant_id")
        if applicant_id is None:
            return _go_to_home_profile(request)
        # try to get the applicant
        try:
            applicant = User.objects.get(id=applicant_id)
        except User.DoesNotExist:
            return _go_to_home_profile(request)
        
        if request.user.id == int(applicant_id):
            return _go_to_home_profile(request)
        
        profile = UserProfile.objects.get(user=applicant)
        context = {
            'profile': profile,
            'picture': profile.picture.url if profile.picture else None,
            'educations': profile.education.all(),
            'works': profile.work_experience.all(),
            'projects': profile.project_experience.all(),
            'applications': [],
        }
        return render(request, "jobhub/base_user_profile.html", context)
    
    return _go_to_home_profile(request)

@login_required
def other_company_profile(request):
    if request.method == "GET":
        company_id = request.GET.get("company_id")
        if company_id is None:
            return _go_to_home_profile(request)
        # try to get the company_user
        try:
            company_user = User.objects.get(id=company_id)
        except User.DoesNotExist:
            return _go_to_home_profile(request)
        
        if request.user.id == int(company_id):
            return _go_to_home_profile(request)

        profile = CompanyProfile.objects.get(user=company_user)
        context = {
            'profile': profile,
            'picture': profile.picture.url if profile.picture else None,
            'staff_list': profile.public_staff_list.all(),
            'individual_reviews': profile.individual_reviews.all(),
            'jobs': Job.objects.filter(company_id=profile.id).order_by('-summary__post_time')[:3],
        }
        print(Job.objects.filter(company_id=profile.id).order_by('-summary__post_time')[:3])
        return render(request, "jobhub/base_company_profile.html", context)
    # put request
        # addId = forms.CharField(label="addId", max_length=100, widget=forms.HiddenInput())
    
    if "submit_individual_review" in request.POST:
        addReviewForm = forms.addReviewForm(request.POST)
        if not addReviewForm.is_valid():
            companyId = addReviewForm.cleaned_data["addId"]
            company_user = User.objects.get(id=companyId)
            company_profile = CompanyProfile.objects.get(user=company_user)
            context = {
                'profile': company_profile,
                'picture': company_profile.picture.url if company_profile.picture else None,
                'individual_reviews': company_profile.individual_reviews.all(),
                'form': addReviewForm,
                'form_type': "add_review",
                'jobs': Job.objects.filter(company_id=company_profile.id).order_by('-summary__post_time')[:3],
            }

            print(addReviewForm.errors)
            return render(request, "jobhub/base_company_profile.html", context)

        # get the company profile
        companyId = addReviewForm.cleaned_data["addId"]
        company_user = User.objects.get(id=companyId)
        company_profile = CompanyProfile.objects.get(user=company_user)
        company_review = company_profile.company_review        

        # create a new individual review
        individual_review = IndividualReview(title=addReviewForm.cleaned_data["addTitle"],
                                            user=request.user,
                                            overall_rating=addReviewForm.cleaned_data["addOverallRating"],
                                            interview_progression_rating=addReviewForm.cleaned_data["addInterviewProgressRating"],
                                            application_response_time_rating=addReviewForm.cleaned_data["addResponseTimeRating"],
                                            benefits_during_interview_rating=addReviewForm.cleaned_data["addBenefitRating"],
                                            interview_atmosphere_rating=addReviewForm.cleaned_data["addAtmosphereRating"],
                                            interview_etiquette_rating=addReviewForm.cleaned_data["addEtiquetteRating"],
                                            role=addReviewForm.cleaned_data["addRole"],
                                            review=addReviewForm.cleaned_data["addContent"])
        individual_review.save()
        company_profile.individual_reviews.add(individual_review)
        # get all individual reviews of the company
        individual_reviews = company_profile.individual_reviews.all()
        _update_company_review(company_review, individual_reviews)
        company_review.save()
        company_profile.save()
        context = {
            'profile': company_profile,
            'picture': company_profile.picture.url if company_profile.picture else None,
            'individual_reviews': company_profile.individual_reviews.all(),
            'jobs': Job.objects.filter(company_id = company_profile.id).order_by('-summary__post_time')[:3],
        }

    return redirect(reverse("other_company_profile") +"?company_id=" + str(company_user.id))

@login_required
def _update_company_review(company_review, individual_reviews):
    # iterate through all individual reviews
    overall_rating = 0
    interview_progression_rating = 0
    application_response_time_rating = 0
    benefits_during_interview_rating = 0
    interview_atmosphere_rating = 0
    interview_etiquette_rating = 0
    five_star_rating, four_star_rating, three_star_rating, two_star_rating, one_star_rating = 0, 0, 0, 0, 0 # 80%, 60% etc should be the percentage
    for individual_review in individual_reviews:
        overall_rating += individual_review.overall_rating
        interview_progression_rating += individual_review.interview_progression_rating
        application_response_time_rating += individual_review.application_response_time_rating
        benefits_during_interview_rating += individual_review.benefits_during_interview_rating
        interview_atmosphere_rating += individual_review.interview_atmosphere_rating
        interview_etiquette_rating += individual_review.interview_etiquette_rating
        if individual_review.overall_rating == 5:
            five_star_rating += 1
        elif individual_review.overall_rating == 4:
            four_star_rating += 1
        elif individual_review.overall_rating == 3:
            three_star_rating += 1
        elif individual_review.overall_rating == 2:
            two_star_rating += 1
        else:
            one_star_rating += 1
    if len(individual_reviews) == 0:
        company_review.overall_rating = 0
        company_review.interview_progression_rating = 0
        company_review.application_response_time_rating = 0
        company_review.benefits_during_interview_rating = 0
        company_review.interview_atmosphere_rating = 0
        company_review.interview_etiquette_rating = 0
        company_review.five_star_rating = 0
        company_review.four_star_rating = 0
        company_review.three_star_rating = 0
        company_review.two_star_rating = 0
        company_review.one_star_rating = 0
        return
    company_review.overall_rating = overall_rating/len(individual_reviews)
    company_review.interview_progression_rating = interview_progression_rating/len(individual_reviews)
    company_review.application_response_time_rating = application_response_time_rating/len(individual_reviews)
    company_review.benefits_during_interview_rating = benefits_during_interview_rating/len(individual_reviews)
    company_review.interview_atmosphere_rating = interview_atmosphere_rating/len(individual_reviews)
    company_review.interview_etiquette_rating = interview_etiquette_rating/len(individual_reviews)
    company_review.five_star_rating = five_star_rating/len(individual_reviews) * 100
    company_review.four_star_rating = four_star_rating/len(individual_reviews) * 100
    company_review.three_star_rating = three_star_rating/len(individual_reviews) * 100
    company_review.two_star_rating = two_star_rating/len(individual_reviews) * 100
    company_review.one_star_rating = one_star_rating/len(individual_reviews) * 100
    company_review.save()

def json_handler(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

@login_required
def home(request):
    return render(request, "jobhub/joblist.html")

@login_required
def joblist(request):
    return render(request, "jobhub/joblist.html")

def full_text_search(search_term):
    job_summaries = JobSummary.objects.filter(
        Q(job_type__icontains=search_term) | 
        Q(location__icontains=search_term) | 
        Q(note__icontains=search_term)
    )

    # Search in JobHighlight
    job_highlights = JobHighlight.objects.filter(
        content__icontains=search_term
    )

    # Search in JobDetail
    job_details = JobDetail.objects.filter(
        content__icontains=search_term
    )

    # Search in Job
    jobs = Job.objects.filter(
        Q(name__icontains=search_term) | 
        Q(summary__in=job_summaries) | 
        Q(highlight__in=job_highlights) | 
        Q(detail__in=job_details)
    )
    return jobs

def joblist_getlist(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            response_data = json.dumps({'error': 'Please login.'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        response_data = []
        try:
            filter_dict_str = request.GET.get('filter')
            if filter_dict_str != None:
                filter_dict = json.loads(filter_dict_str)

                if 'search' in filter_dict:
                    job_list = full_text_search(filter_dict['search'])
                    del filter_dict['search']
                    job_list = job_list.filter(**filter_dict)
                else:
                    job_list = Job.objects.filter(**filter_dict)
                
            else:
                job_list = Job.objects.all()
            job_list = job_list.order_by('-summary__post_time')
            
            for job in job_list:
                # Convert Job and its related objects to dictionaries
                job_dict = model_to_dict(job)
                job_dict['summary'] = model_to_dict(job.summary)
                
                # Handling company
                job_dict['company'] = {}
                job_dict['company']['company_info'] = model_to_dict(job.company.company_info)
                job_dict['company']['picture'] = job.company.picture.url if job.company.picture else '/static/jobhub/default_user.png'

                response_data.append(job_dict)
        except FieldError:
            response_data = json.dumps({'error': 'Invalid filter.'})
            return HttpResponseBadRequest(response_data, content_type='application/json')      
        except Exception:
            response_data = json.dumps({'error': 'Someting went wrong.'})
            return HttpResponseBadRequest(response_data, content_type='application/json') 

        response_data = json.dumps(response_data,default=json_handler)
        
        return HttpResponse(response_data,content_type='application/json')

    
    response_data = json.dumps({'error': 'Post is not supported'})
    return HttpResponseBadRequest(response_data, content_type='application/json')

def joblist_search(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            response_data = json.dumps({'error': 'Please login.'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        try:
            search = request.GET.get('search')

            job_list = full_text_search(search).order_by('-summary__post_time')
            response_data = []
            for job in job_list:
                # Convert Job and its related objects to dictionaries
                job_dict = model_to_dict(job)
                job_dict['summary'] = model_to_dict(job.summary)
                
                # Handling company
                job_dict['company'] = {}
                job_dict['company']['company_info'] = model_to_dict(job.company.company_info)
                job_dict['company']['picture'] = job.company.picture.url if job.company.picture else '/static/jobhub/default_user.png'

                response_data.append(job_dict)


            response_data = json.dumps(response_data,default=json_handler)
            return HttpResponse(response_data,content_type='application/json')
        
        except Exception:
            response_data = json.dumps({'error': 'Someting went wrong.'})
            return HttpResponseBadRequest(response_data, content_type='application/json') 

    response_data = json.dumps({'error': 'Post is not supported'})
    return HttpResponseBadRequest(response_data, content_type='application/json')  

def joblist_getdetail(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            response_data = json.dumps({'error': 'Please login.'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        
        response_data = []
        try:
            job_id = request.GET.get('job_id')
            job = Job.objects.get(id=job_id)

            try:
                application = Application.objects.get(user=request.user, job=job)
            except Exception:
                application = None

        except Job.DoesNotExist:
            job = None
            response_data = json.dumps({'error': 'Job not found'})
            return HttpResponseNotFound(response_data, content_type='application/json')
        except AttributeError:
            response_data = json.dumps({'error': 'Invalid Key'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        except Exception:
            response_data = json.dumps({'error': 'Something went wrong'})
            return HttpResponseBadRequest(response_data, content_type='application/json')        

        # Convert Job and its related objects to dictionaries
        job_dict = model_to_dict(job)
        job_dict['summary'] = model_to_dict(job.summary)
        job_dict['highlight'] = model_to_dict(job.highlight)
        job_dict['detail'] = model_to_dict(job.detail)
        
        # Handling company
        job_dict['company'] = {}
        job_dict['company']['user_id'] = job.company.user.id
        job_dict['company']['company_info'] = model_to_dict(job.company.company_info)
        job_dict['company']['company_contact_info'] = model_to_dict(job.company.company_contact_info)
        job_dict['company']['company_review'] = model_to_dict(job.company.company_review)
        
        if application:
            job_dict['application'] = model_to_dict(application)
            job_dict['application']['submitdate'] = application.submitdate.date()
        else:
            job_dict['application'] = None
        response_data = json.dumps(job_dict,default=json_handler)
        
        return HttpResponse(response_data,content_type='application/json')
    
    response_data = json.dumps({'error': 'Post is not supported'})
    return HttpResponseBadRequest(response_data, content_type='application/json')

def joblist_submit_application(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            response_data = json.dumps({'error': 'Please login.'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        
        try:
            job_id = request.GET.get('job_id')

            user = request.user
            job = Job.objects.get(id=job_id)

            if user.last_name=='employer':
                response_data = json.dumps({'error': 'Please use an applicant account.'})
                return HttpResponseBadRequest(response_data, content_type='application/json')

            if Application.objects.filter(user=user, job=job).exists():
                response_data = json.dumps({'error': 'You have already applied this job.'})
                return HttpResponseBadRequest(response_data, content_type='application/json')
            
            
            company = job.company

            new_application = Application(
                user=user,
                submitdate=timezone.now(), 
                status='all',  
                job=job,
                company=company
            )
            new_application.save()

        except Job.DoesNotExist:
            job = None
            response_data = json.dumps({'error': 'Job not found'})
            return HttpResponseNotFound(response_data, content_type='application/json')
        except AttributeError:
            response_data = json.dumps({'error': 'Invalid Key'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        except Exception:
            response_data = json.dumps({'error': 'Something went wrong'})
            return HttpResponseBadRequest(response_data, content_type='application/json')    

        response_data = json.dumps({'status': 'submitted'})
        return HttpResponse(response_data,content_type='application/json') 

    response_data = json.dumps({'error': 'Post is not supported'})
    return HttpResponseBadRequest(response_data, content_type='application/json')   

def joblist_withdraw_application(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            response_data = json.dumps({'error': 'Please login.'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        
        try:
            job_id = request.GET.get('job_id')

            user = request.user
            job = Job.objects.get(id=job_id)
            application = Application.objects.get(user=user, job=job)
            application.delete()

        except Job.DoesNotExist:
            job = None
            response_data = json.dumps({'error': 'Job not found'})
            return HttpResponseNotFound(response_data, content_type='application/json')
        except Application.DoesNotExist:
            response_data = json.dumps({'error': 'You did not apply this job.'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        except AttributeError:
            response_data = json.dumps({'error': 'Invalid Key'})
            return HttpResponseBadRequest(response_data, content_type='application/json')
        except Exception:
            response_data = json.dumps({'error': 'Something went wrong'})
            return HttpResponseBadRequest(response_data, content_type='application/json')    

        response_data = json.dumps({'status': 'deleted'})
        return HttpResponse(response_data,content_type='application/json') 

    response_data = json.dumps({'error': 'Post is not supported'})
    return HttpResponseBadRequest(response_data, content_type='application/json')    

@login_required
def a_application(request, filter_by):
    applications = Application.objects.filter(user=request.user) if filter_by == 'all' else Application.objects.filter(user=request.user, status=filter_by)
    if request.method == 'GET':
        return render(request, 'jobhub/application/applicant_application.html', {'applications': applications})
    try:
        review = IndividualReview()
        review.user = request.user
        review.time_posted = timezone.now()
        reviewform = forms.ReviewForm(request.POST)
        if not reviewform.is_valid():
            return render(request, 'jobhub/application/applicant_application.html', { 'form': reviewform, 'applications': applications})
        data = reviewform.cleaned_data
        review.role = data['role']
        review.overall_rating = data['overall_rating']
        review.interview_progression_rating = data['interview_progression']
        review.application_response_time_rating = data['response_time']
        review.benefits_during_interview_rating = data['benefits_in_interview']
        review.interview_atmosphere_rating = data['interview_atmosphere']
        review.interview_etiquette_rating = data['interviewer_etiquette']
        review.title = data['title']
        review.review = data['content']
        review.save()
        companyinfo = CompanyInfo.objects.filter(name=data['company'])[:1]
        companyprofile = CompanyProfile.objects.get(company_info = companyinfo)
        companyprofile.individual_reviews.add(review)
        company_review = companyprofile.company_review
        individual_reviews = companyprofile.individual_reviews.all()
        _update_company_review(company_review, individual_reviews)
        company_review.save()
        companyprofile.company_review = company_review
        companyprofile.save()
        context = { 'message': 'Submit successfully!', 'applications': applications }
    except Exception as e:
        context = { 'message': str(e), 'applications': applications }
        return render(request, 'jobhub/application/applicant_application.html', context)
    return render(request, 'jobhub/application/applicant_application.html', context)

def _my_json_error_response(message, status=200):
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)

def get_application(request, filter_by):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if (not filter_by) or filter_by == 'all':
        applications = Application.objects.filter(user=request.user)
    else:
        applications = Application.objects.filter(status=filter_by, user=request.user)
    
    response_data = {
        'applications': [],
        'counts': {
            'all': Application.objects.filter(user=request.user).count(),
            'reviewed': Application.objects.filter(status='reviewed', user=request.user).count(),
            'interviewed': Application.objects.filter(status='interviewed', user=request.user).count(),
            'hired': Application.objects.filter(status='hired', user=request.user).count(),
            'rejected': Application.objects.filter(status='rejected', user=request.user).count()
        }
    }

    for application in applications:
        application = {
            'user': application.user,
            'job_id': application.job.id,
            'submitdate': application.submitdate.isoformat(),
            'status': application.status,
            'job': application.job.name,
            'company_id': application.company.user.id,
            'company': application.company.company_info.name,
            'due_time': application.job.summary.due_time.isoformat(),
            'post_time': application.job.summary.post_time.isoformat(),
            'upper_pay': application.job.summary.estimate_pay_upper,
            'lower_pay': application.job.summary.estimate_pay_lower,
            'company_size': application.company.company_info.size,
            'company_industry': application.company.company_info.industry,
            'company_bio': application.company.company_info.bio,
        }
        response_data['applications'].append(application)
    response_json = json.dumps(response_data, default=str)
    return HttpResponse(response_json, content_type='application/json')

@login_required
def e_application(request, id, filter_by):
    id = 0 if not id else id
    if request.method == 'GET':
        return render(request, 'jobhub/application/employer_application.html', {'id': id, 'status': filter_by})
    try:
        job = Job()
        jobpostform = forms.JobPostForm(request.POST)
        if not jobpostform.is_valid():
            context = { 'form': jobpostform, 'id': id, 'status': filter_by}
            return render(request, 'jobhub/application/employer_application.html', context)
        job.company = CompanyProfile.objects.get(user=request.user)
        data = jobpostform.cleaned_data
        job.name = data['job_name']
        jobsummary = JobSummary()
        jobsummary.post_time = timezone.now()
        jobsummary.due_time = data['job_due_time']
        jobsummary.location = data['location']
        jobsummary.estimate_pay_lower = data['estimate_pay_lower']
        jobsummary.estimate_pay_upper = data['estimate_pay_upper']
        jobsummary.job_type = data['job_type']
        jobsummary.save()
        jobhighlight = JobHighlight()
        jobhighlight.content = data['job_responsibilities']
        jobhighlight.save()
        jobdetail = JobDetail()
        jobdetail.content = data['job_description']
        jobdetail.save()
        job.summary = jobsummary
        job.highlight = jobhighlight
        job.detail = jobdetail
        job.save()
        context = { 'message': 'Submit successfully!', 'id': id, 'status': filter_by }
    except Exception as e:
        context = { 'message': str(e), 'id': id, 'status': filter_by }
        return render(request, 'jobhub/application/employer_application.html', context)
    return render(request, 'jobhub/application/employer_application.html', context)

def get_applicant(request, id, filter_by):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    response_data = {
        'jobs': [],
        'applicants': [],
        'counts':[]
    }
    for j_item in Job.objects.filter(company__user=request.user):
        job = {
            'job_id': j_item.id,
            'job_name': j_item.name,
            'post_time': j_item.summary.post_time,
            'company_name': j_item.company.company_info.name
        }
        response_data['jobs'].append(job)
        if j_item.id == id:
            count = {
                'job_id': j_item.id,
                'applied': Application.objects.filter(job=j_item).count(),
                'reviewed': Application.objects.filter(job=j_item, status='reviewed').count(),
                'interviewed': Application.objects.filter(job=j_item, status='interviewed').count(),
                'hired': Application.objects.filter(job=j_item, status='hired').count(),
                'rejected': Application.objects.filter(job=j_item, status='rejected').count()
            }
            response_data['counts'].append(count)
            applications = Application.objects.filter(job=j_item, status=filter_by) if filter_by != 'all' else Application.objects.filter(job=j_item)
            for a_item in applications:
                applicant = {
                    'job_id': j_item.id,
                    'applicant_id': a_item.user.id,
                    'application_id': a_item.id,
                    'name': a_item.user.first_name,
                    'email': a_item.user.email,
                    'submit_date': a_item.submitdate
                }
                response_data['applicants'].append(applicant)
    response_json = json.dumps(response_data, default=str)
    return HttpResponse(response_json, content_type='application/json')

@csrf_exempt
@login_required
def update_application_status(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        application_id = data.get('applicationId')
        new_status = data.get('status')
        selected_id = data.get('selected_id')
        if not application_id or not new_status:
            return JsonResponse({'error': 'Missing application ID or status'}, status=400)
        try:
            application = Application.objects.get(id=application_id, company__user=request.user)
            application.status = new_status
            application.save()
            return HttpResponseRedirect(reverse('employer_application', kwargs={ 'id': selected_id, 'filter_by': new_status }))
        except Application.DoesNotExist:
            return JsonResponse({'error': 'Application not found'}, status=404)
        except Exception as e:
            print("Error occurred: ", str(e))
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def logout_action(request):
    auth_logout(request)
    return redirect(reverse('login'))
