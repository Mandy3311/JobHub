from django.db import models
from django.contrib.auth.models import User

# ================== User Profile ==================
class PersonalInfo(models.Model):
    name = models.CharField(max_length=255, blank=False)
    position = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    company_id = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name + " - " + self.position + " - " + self.bio

from django.core.validators import FileExtensionValidator
class ContactInfo(models.Model):
    phone = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=False)
    address = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return self.email + " - " + self.phone + " - " + self.address + " - " + self.linkedin

class OtherInfo(models.Model):
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.skills + " - " + self.interests

class Education(models.Model):
    school = models.CharField(max_length=255, blank=False)
    major = models.CharField(max_length=255, blank=False)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    start_time = models.DateField(blank=False)
    end_time = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.school + " - " + self.major + " - " + self.location + " - " + self.description

class WorkExperience(models.Model):
    company = models.CharField(max_length=255, blank=False)
    role = models.CharField(max_length=255, blank=False)
    start_time = models.DateField(blank=False)
    end_time = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.company + " - " + self.role + " - " + self.type + " - " + self.location + " - " + self.description
    
class ProjectExperience(models.Model):
    project_name = models.CharField(max_length=255, blank=False)
    role = models.CharField(max_length=255, blank=True)
    start_time = models.DateField(blank=False)
    end_time = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.project_name + " - " + self.role + " - " + self.location + " - " + self.description

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE)
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE)
    other_info = models.OneToOneField(OtherInfo, on_delete=models.CASCADE)
    education = models.ManyToManyField(Education)
    work_experience = models.ManyToManyField(WorkExperience)
    project_experience = models.ManyToManyField(ProjectExperience)
    picture = models.ImageField(upload_to="profile_pictures", blank=True)


    def __str__(self):
        return self.user.username + " - " + self.personal_info.name + " - " + self.contact_info.email + " - " + self.other_info.skills

# ==================  Company Profile  ==================    
class CompanyInfo(models.Model):
    name = models.CharField(max_length=255, blank=False)
    bio = models.TextField(blank=True)
    industry = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name + " - " + self.bio + " - " + self.industry + " - " + self.size

class CompanyContactInfo(models.Model):
    company = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=False)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.company.name + " - " + self.email + " - " + self.phone + " - " + self.address + " - " + self.website + " - " + self.linkedin

class CompanyReview(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)
    # // overall rating is the average of the following ratings, which is round 1
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=False)
    interview_progression_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=False)
    application_response_time_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=False)
    benefits_during_interview_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=False)
    interview_atmosphere_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=False)
    interview_etiquette_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=False)
    five_star_rating = models.IntegerField(blank=False)
    four_star_rating = models.IntegerField(blank=False)
    three_star_rating = models.IntegerField(blank=False)
    two_star_rating = models.IntegerField(blank=False)
    one_star_rating = models.IntegerField(blank=False)

    def __str__(self):
        # return self.company.name + " - " + self.user.username + " - " + self.time_posted + " - " + self.overall_rating + " - " + self.interview_progression_rating + " - " + self.application_response_time_rating + " - " + self.benefits_during_interview_rating + " - " + self.interview_atmosphere_rating + " - " + self.interview_etiquette_rating + " - " + self.five_star_rating + " - " + self.four_star_rating + " - " + self.three_star_rating + " - " + self.two_star_rating + " - " + self.one_star_rating
        return self.company.name + " - " + self.user.username + " - " + self.time_posted + " - " + self.overall_rating + " - " + self.interview_progression_rating + " - " + self.application_response_time_rating + " - " + self.benefits_during_interview_rating + " - " + self.interview_atmosphere_rating + " - " + self.interview_etiquette_rating + " - " + self.five_star_rating + " - " + self.four_star_rating + " - " + self.three_star_rating + " - " + self.two_star_rating + " - " + self.one_star_rating + " - " + self.review

class IndividualReview(models.Model):
    title = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=False)
    time_posted = models.DateTimeField(auto_now_add=True)
    overall_rating = models.IntegerField(blank=False)
    interview_progression_rating = models.IntegerField(blank=False)
    application_response_time_rating = models.IntegerField(blank=False)
    benefits_during_interview_rating = models.IntegerField(blank=False)
    interview_atmosphere_rating = models.IntegerField(blank=False)
    interview_etiquette_rating = models.IntegerField(blank=False)
    review = models.TextField(blank=True)

    def __str__(self):
        return self.title + " - " + self.user.username + " - " + self.time_posted + " - " + self.overall_rating + " - " + self.interview_progression_rating + " - " + self.application_response_time_rating + " - " + self.benefits_during_interview_rating + " - " + self.interview_atmosphere_rating + " - " + self.interview_etiquette_rating + " - " + self.review

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_info = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)
    company_contact_info = models.OneToOneField(CompanyContactInfo, on_delete=models.CASCADE)
    company_review = models.OneToOneField(CompanyReview, on_delete=models.CASCADE)
    individual_reviews = models.ManyToManyField(IndividualReview)
    public_staff_list = models.ManyToManyField(UserProfile)
    picture = models.ImageField(upload_to="profile_pictures", blank=True)

    def __str__(self):
        return self.company_info.name + " - " + self.company_contact_info.email + " - " + self.company_contact_info.phone + " - " + self.company_contact_info.address + " - " + self.company_contact_info.website + " - " + self.company_contact_info.linkedin
    

# ==================  Job List  ==================

class JobSummary(models.Model):
    job_type = models.CharField(max_length=255, blank=True)
    post_time = models.DateField(blank=False)
    due_time = models.DateField(blank=False)
    location = models.CharField(max_length=255, blank=True)
    estimate_pay_lower = models.PositiveIntegerField(blank=False)
    estimate_pay_upper = models.PositiveIntegerField(blank=False)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Posted: {self.post_time} - Due: {self.due_time} - Location: {self.location}"

class JobHighlight(models.Model):
    content = models.CharField(max_length=1023, blank=True)
    def __str__(self):
        # Truncate content to a reasonable length for display
        return f"Highlight: {self.content[:50]}..." if len(self.content) > 50 else self.content

class JobDetail(models.Model):
    content = models.CharField(max_length=1023, blank=True)
    def __str__(self):
        # Truncate content to a reasonable length for display
        return f"Detail: {self.content[:50]}..." if len(self.content) > 50 else self.content

class Job(models.Model):
    name = models.CharField(max_length=255, blank=False)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    summary = models.OneToOneField(JobSummary, on_delete=models.CASCADE)
    highlight = models.OneToOneField(JobHighlight, on_delete=models.CASCADE)
    detail = models.OneToOneField(JobDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + str(self.summary)
    
# ==================  Applications  ==================

class Application(models.Model):
    STATUS_CHOICES = [
        ('all', 'All'),
        ('reviewed', 'Reviewed'),
        ('interviewed', 'Interviewed'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES,default='all')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'id={self.id}'
