from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=100, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == "":
            raise ValidationError("Username cannot be empty.")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password == "":
            raise ValidationError("Password cannot be empty.")
        return password
    
class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=100, widget=forms.PasswordInput())
    confirm = forms.CharField(label="confirm", max_length=100, widget=forms.PasswordInput())
    email = forms.CharField(label="email", max_length=100)
    name = forms.CharField(label="name", max_length=100)
    type = forms.CharField(label="type", max_length=100)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == "":
            raise ValidationError("Username cannot be empty.")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password == "":
            raise ValidationError("Password cannot be empty.")
        return password
    
    def clean_confirm(self):
        confirm = self.cleaned_data.get('confirm')
        if confirm == "":
            raise ValidationError("Confirm cannot be empty.")
        if confirm != self.cleaned_data.get('password'):
            raise ValidationError("Confirm does not match password.")
        return confirm
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == "":
            raise ValidationError("Email cannot be empty.")
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == "":
            raise ValidationError("First name cannot be empty.")
        return name
    
    def clean_type(self):
        type = self.cleaned_data.get('type')
        if type == "":
            raise ValidationError("Type cannot be empty.")
        # type should be either "employer" or "applicant"
        if type != "employer" and type != "applicant":
            raise ValidationError("Type should be either employer or applicant.")
        return type
    
# ================== User Profile ==================
class PersonalInfoForm(forms.Form):
    editName = forms.CharField(label="editName", max_length=100)
    editPosition = forms.CharField(label="editPosition", max_length=100)
    # editCompany and editSchool are not required
    editCompany = forms.CharField(label="editCompany", max_length=100, required=False)
    editCompanyId = forms.CharField(label="editCompanyId", max_length=100, required=False)
    editSchool = forms.CharField(label="editSchool", max_length=100, required=False)
    # editBio are from textarea
    editBio = forms.CharField(label="editBio", max_length=1000, widget=forms.Textarea)
    editPicture = forms.ImageField(label="editPicture", max_length=100, required=False)

    def clean_editName(self):
        editName = self.cleaned_data.get('editName')
        if editName == "":
            raise ValidationError("Name cannot be empty.")
        return editName
    
    def clean_editPosition(self):
        editPosition = self.cleaned_data.get('editPosition')
        if editPosition == "":
            raise ValidationError("Position cannot be empty.")
        return editPosition
    
    def clean_editBio(self):
        editBio = self.cleaned_data.get('editBio')
        if editBio == "":
            raise ValidationError("Bio cannot be empty.")
        return editBio
    
class ContactInfoForm(forms.Form):
    editPhone = forms.CharField(label="editPhone", max_length=100)
    editEmail = forms.CharField(label="editEmail", max_length=100)
    editAddress = forms.CharField(label="editAddress", max_length=100)
    editLinkedIn = forms.CharField(label="editLinkedIn", max_length=100)
    editResume = forms.FileField(label="Resume", required=False)

    def clean_editPhone(self):
        editPhone = self.cleaned_data.get('editPhone')
        if editPhone == "":
            raise ValidationError("Phone cannot be empty.")
        # should be like xxx-xxx-xxxx
        if len(editPhone) != 12 or editPhone[3] != '-' or editPhone[7] != '-' or not editPhone[:3].isdigit() or not editPhone[4:7].isdigit() or not editPhone[8:].isdigit():
            raise ValidationError("Phone number should be like xxx-xxx-xxxx.")
        return editPhone
    
    def clean_editEmail(self):
        editEmail = self.cleaned_data.get('editEmail')
        if editEmail == "":
            raise ValidationError("Email cannot be empty.")
        return editEmail
    
    def clean_editAddress(self):
        editAddress = self.cleaned_data.get('editAddress')
        if editAddress == "":
            raise ValidationError("Address cannot be empty.")
        return editAddress
    
    def clean_editLinkedIn(self):
        editLinkedIn = self.cleaned_data.get('editLinkedIn')
        if editLinkedIn == "":
            raise ValidationError("LinkedIn cannot be empty.")
        return editLinkedIn
    
    # def clean_editResume(self):
    #     editResume = self.cleaned_data.get('editResume')
    #     if editResume == "":
    #         raise ValidationError("Resume cannot be empty.")
    #     return editResume

class SkillsForm(forms.Form):
    editSkills = forms.CharField(label="editSkills", max_length=1000, widget=forms.Textarea)
    editInterests = forms.CharField(label="editInterests", max_length=1000, widget=forms.Textarea)

    def clean_editSkills(self):
        editSkills = self.cleaned_data.get('editSkills')
        if editSkills == "":
            raise ValidationError("Skills cannot be empty.")
        return editSkills
    
    def clean_editInterests(self):
        editInterests = self.cleaned_data.get('editInterests')
        if editInterests == "":
            raise ValidationError("Interests cannot be empty.")
        return editInterests

class addEducationForm(forms.Form):
    addId = forms.CharField(label="addId", max_length=100, widget=forms.HiddenInput())
    addSchool = forms.CharField(label="addSchool", max_length=100)
    addMajor = forms.CharField(label="addMajor", max_length=100)
    addStartDate = forms.DateField(label="addStartDate")
    addEndDate = forms.DateField(label="addEndDate")
    addGPA = forms.CharField(label="addGPA", max_length=100)
    addLocation = forms.CharField(label="addLocation", max_length=100)
    addDescription = forms.CharField(label="addDescription", max_length=1000, widget=forms.Textarea)

    def clean_addId(self):
        addId = self.cleaned_data.get('addId')
        if addId == "":
            raise ValidationError("Id cannot be empty.")
        return addId

    def clean_addSchool(self):
        print("clean_addSchool")
        addSchool = self.cleaned_data.get('addSchool')
        if addSchool == "":
            raise ValidationError("School cannot be empty.")
        return addSchool
    
    def clean_addMajor(self):
        addMajor = self.cleaned_data.get('addMajor')
        if addMajor == "":
            raise ValidationError("Major cannot be empty.")
        return addMajor
    
    def clean_addStartDate(self):
        addStartDate = self.cleaned_data.get('addStartDate')
        if addStartDate == "":
            raise ValidationError("Start date cannot be empty.")
        return addStartDate
    
    def clean_addEndDate(self):
        addEndDate = self.cleaned_data.get('addEndDate')
        if addEndDate == "":
            raise ValidationError("End date cannot be empty.")
        return addEndDate
    
    def clean_addGPA(self):
        addGPA = self.cleaned_data.get('addGPA')
        if addGPA == "":
            raise ValidationError("GPA cannot be empty.")
        # should be in range [0, 4] and is a number
        try:
            addGPA = float(addGPA)
        except ValueError:
            raise ValidationError("GPA should be a number.")
        if addGPA < 0 or addGPA > 4:
            raise ValidationError("GPA should be in range [0, 4].")
        return addGPA
    
    def clean_addLocation(self):
        addLocation = self.cleaned_data.get('addLocation')
        if addLocation == "":
            raise ValidationError("Location cannot be empty.")
        return addLocation
    
    def clean_addDescription(self):
        addDescription = self.cleaned_data.get('addDescription')
        if addDescription == "":
            raise ValidationError("Description cannot be empty.")
        return addDescription

class addWorkExperienceForm(forms.Form):
    addId = forms.CharField(label="addId", max_length=100, widget=forms.HiddenInput())
    addCompany = forms.CharField(label="addCompany", max_length=100)
    addRole = forms.CharField(label="addRole", max_length=100)
    addStartDate = forms.DateField(label="addStartDate")
    addEndDate = forms.DateField(label="addEndDate")
    addType = forms.CharField(label="addType", max_length=100)
    addLocation = forms.CharField(label="addLocation", max_length=100)
    addDescription = forms.CharField(label="addDescription", max_length=1000, widget=forms.Textarea)

    def clean_addId(self):
        addId = self.cleaned_data.get('addId')
        if addId == "":
            raise ValidationError("Id cannot be empty.")
        return addId

    def clean_addCompany(self):
        addCompany = self.cleaned_data.get('addCompany')
        if addCompany == "":
            raise ValidationError("Company cannot be empty.")
        return addCompany
    
    def clean_addRole(self):
        addRole = self.cleaned_data.get('addRole')
        if addRole == "":
            raise ValidationError("Role cannot be empty.")
        return addRole
    
    def clean_addStartDate(self):
        addStartDate = self.cleaned_data.get('addStartDate')
        if addStartDate == "":
            raise ValidationError("Start date cannot be empty.")
        return addStartDate
    
    def clean_addEndDate(self):
        addEndDate = self.cleaned_data.get('addEndDate')
        if addEndDate == "":
            raise ValidationError("End date cannot be empty.")
        return addEndDate
    
    def clean_addType(self):
        addType = self.cleaned_data.get('addType')
        if addType == "":
            raise ValidationError("Type cannot be empty.")
        return addType
    
    def clean_addLocation(self):
        addLocation = self.cleaned_data.get('addLocation')
        if addLocation == "":
            raise ValidationError("Location cannot be empty.")
        return addLocation
    
    def clean_addDescription(self):
        addDescription = self.cleaned_data.get('addDescription')
        if addDescription == "":
            raise ValidationError("Description cannot be empty.")
        return addDescription
    
class addProjectExperienceForm(forms.Form):
    addId = forms.CharField(label="addId", max_length=100, widget=forms.HiddenInput())
    addProject = forms.CharField(label="addProject", max_length=100)
    addRole = forms.CharField(label="addRole", max_length=100)
    addStartDate = forms.DateField(label="addStartDate")
    addEndDate = forms.DateField(label="addEndDate")
    addLocation = forms.CharField(label="addLocation", max_length=100)
    addDescription = forms.CharField(label="addDescription", max_length=1000, widget=forms.Textarea)

    def clean_addId(self):
        addId = self.cleaned_data.get('addId')
        if addId == "":
            raise ValidationError("Id cannot be empty.")
        return addId

    def clean_addProject(self):
        addProject = self.cleaned_data.get('addProject')
        if addProject == "":
            raise ValidationError("Project cannot be empty.")
        return addProject
    
    def clean_addRole(self):
        addRole = self.cleaned_data.get('addRole')
        if addRole == "":
            raise ValidationError("Role cannot be empty.")
        return addRole

    def clean_addStartDate(self):
        addStartDate = self.cleaned_data.get('addStartDate')
        if addStartDate == "":
            raise ValidationError("Start date cannot be empty.")
        return addStartDate
    
    def clean_addEndDate(self):
        addEndDate = self.cleaned_data.get('addEndDate')
        if addEndDate == "":
            raise ValidationError("End date cannot be empty.")
        return addEndDate
    
    def clean_addLocation(self):
        addLocation = self.cleaned_data.get('addLocation')
        if addLocation == "":
            raise ValidationError("Location cannot be empty.")
        return addLocation
    
    def clean_addDescription(self):
        addDescription = self.cleaned_data.get('addDescription')
        if addDescription == "":
            raise ValidationError("Description cannot be empty.")
        return addDescription
    
# # ================== Company Profile ==================
class CompanyInfoForm(forms.Form):
    editName = forms.CharField(label="editName", max_length=100)
    editIndustry = forms.CharField(label="editIndustry", max_length=100)
    editSize = forms.CharField(label="editSize", max_length=100)
    editBio = forms.CharField(label="editBio", max_length=1000, widget=forms.Textarea)
    editPicture = forms.ImageField(label="editPicture", max_length=100, required=False)

    def clean_editName(self):
        editName = self.cleaned_data.get('editName')
        if editName == "":
            raise ValidationError("Name cannot be empty.")
        return editName
    
    def clean_editIndustry(self):
        editIndustry = self.cleaned_data.get('editIndustry')
        if editIndustry == "":
            raise ValidationError("Industry cannot be empty.")
        return editIndustry
    
    def clean_editSize(self):
        editSize = self.cleaned_data.get('editSize')
        if editSize == "":
            raise ValidationError("Size cannot be empty.")
        return editSize
    
    def clean_editBio(self):
        editBio = self.cleaned_data.get('editBio')
        if editBio == "":
            raise ValidationError("Bio cannot be empty.")
        return editBio
    
class CompanyContactInfoForm(forms.Form):
    editPhone = forms.CharField(label="editPhone", max_length=100)
    editEmail = forms.CharField(label="editEmail", max_length=100)
    editAddress = forms.CharField(label="editAddress", max_length=100)
    editWebsite = forms.CharField(label="editWebsite", max_length=100)
    editLinkedIn = forms.CharField(label="editLinkedIn", max_length=100)

    def clean_editPhone(self):
        editPhone = self.cleaned_data.get('editPhone')
        if editPhone == "":
            raise ValidationError("Phone cannot be empty.")
        # should be like xxx-xxx-xxxx
        if len(editPhone) != 12 or editPhone[3] != '-' or editPhone[7] != '-' or not editPhone[:3].isdigit() or not editPhone[4:7].isdigit() or not editPhone[8:].isdigit():
            raise ValidationError("Phone number should be like xxx-xxx-xxxx.")
        return editPhone
    
    def clean_editEmail(self):
        editEmail = self.cleaned_data.get('editEmail')
        if editEmail == "":
            raise ValidationError("Email cannot be empty.")
        return editEmail
    
    def clean_editAddress(self):
        editAddress = self.cleaned_data.get('editAddress')
        if editAddress == "":
            raise ValidationError("Address cannot be empty.")
        return editAddress
    
    def clean_editWebsite(self):
        editWebsite = self.cleaned_data.get('editWebsite')
        if editWebsite == "":
            raise ValidationError("Website cannot be empty.")
        return editWebsite
    
    def clean_editLinkedIn(self):
        editLinkedIn = self.cleaned_data.get('editLinkedIn')
        if editLinkedIn == "":
            raise ValidationError("LinkedIn cannot be empty.")
        return editLinkedIn
    
class addStaffForm(forms.Form):
    addStaff = forms.CharField(label="addStaff", max_length=100)

    def clean_addStaff(self):
        addStaff = self.cleaned_data.get('addStaff')
        if addStaff == "":
            raise ValidationError("Staff cannot be empty.")
        return addStaff
    
class addReviewForm(forms.Form):
    addId = forms.IntegerField(label="addId", widget=forms.HiddenInput())
    addRole = forms.CharField(label="addRole", max_length=100)
    addOverallRating = forms.IntegerField(label="addOverallRating")
    addInterviewProgressRating = forms.IntegerField(label="addInterviewProgressRating")
    addResponseTimeRating = forms.IntegerField(label="addResponseTimeRating")
    addBenefitRating = forms.IntegerField(label="addBenefitRating")
    addAtmosphereRating = forms.IntegerField(label="addAtmosphereRating")
    addEtiquetteRating = forms.IntegerField(label="addEtiquetteRating")
    addTitle = forms.CharField(label="addTitle", max_length=100)
    addContent = forms.CharField(label="addContent", max_length=1000, widget=forms.Textarea)

    def clean_addId(self):
        addId = self.cleaned_data.get('addId')
        if addId == "":
            raise ValidationError("Id cannot be empty.")
        return addId

    def clean_addRole(self):
        addRole = self.cleaned_data.get('addRole')
        if addRole == "":
            raise ValidationError("Role cannot be empty.")
        return addRole
    
    def clean_addOverallRating(self):
        addOverallRating = self.cleaned_data.get('addOverallRating')
        if addOverallRating == "":
            raise ValidationError("Overall rating cannot be empty.")
        return addOverallRating
    
    def clean_addInterviewProgressRating(self):
        addInterviewProgressRating = self.cleaned_data.get('addInterviewProgressRating')
        if addInterviewProgressRating == "":
            raise ValidationError("Interview Progression rating cannot be empty.")
        return addInterviewProgressRating
    
    def clean_addResponseTimeRating(self):
        addResponseTimeRating = self.cleaned_data.get('addResponseTimeRating')
        if addResponseTimeRating == "":
            raise ValidationError("Response Time rating cannot be empty.")
        return addResponseTimeRating
    
    def clean_addBenefitRating(self):
        addBenefitRating = self.cleaned_data.get('addBenefitRating')
        if addBenefitRating == "":
            raise ValidationError("Benefit rating cannot be empty.")
        return addBenefitRating
    
    def clean_addAtmosphereRating(self):
        addAtmosphereRating = self.cleaned_data.get('addAtmosphereRating')
        if addAtmosphereRating == "":
            raise ValidationError("Atmosphere rating cannot be empty.")
        return addAtmosphereRating
    
    def clean_addEtiquetteRating(self):
        addEtiquetteRating = self.cleaned_data.get('addEtiquetteRating')
        if addEtiquetteRating == "":
            raise ValidationError("Etiquette rating cannot be empty.")
        return addEtiquetteRating
    
    def clean_addTitle(self):
        addTitle = self.cleaned_data.get('addTitle')
        if addTitle == "":
            raise ValidationError("Title cannot be empty.")
        return addTitle
    
    def clean_addContent(self):
        addContent = self.cleaned_data.get('addContent')
        if addContent == "":
            raise ValidationError("Content cannot be empty.")
        return addContent

# # ================== Applications ==================

class ReviewForm(forms.Form):
    company = forms.CharField(max_length=100)
    role = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Software Engineer Intern'}))
    overall_rating = forms.ChoiceField(choices=[(i, f"{i} Star" if i == 1 else f"{i} Stars") for i in range(1, 6)])
    interview_progression = forms.ChoiceField(choices=[(i, f"{i} Star" if i == 1 else f"{i} Stars") for i in range(1, 6)])
    response_time = forms.ChoiceField(choices=[(i, f"{i} Star" if i == 1 else f"{i} Stars") for i in range(1, 6)])
    benefits_in_interview = forms.ChoiceField(choices=[(i, f"{i} Star" if i == 1 else f"{i} Stars") for i in range(1, 6)])
    interview_atmosphere = forms.ChoiceField(choices=[(i, f"{i} Star" if i == 1 else f"{i} Stars") for i in range(1, 6)])
    interviewer_etiquette = forms.ChoiceField(choices=[(i, f"{i} Star" if i == 1 else f"{i} Stars") for i in range(1, 6)])
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

class JobPostForm(forms.Form):
    job_name = forms.CharField(max_length=255)
    job_due_time = forms.DateField()
    location = forms.CharField(max_length=255)
    estimate_pay_lower = forms.IntegerField(min_value=0)
    estimate_pay_upper = forms.IntegerField()
    job_type = forms.CharField(max_length=255)
    job_responsibilities = forms.CharField(max_length=1023, widget=forms.Textarea)
    job_description = forms.CharField(max_length=1023, widget=forms.Textarea)