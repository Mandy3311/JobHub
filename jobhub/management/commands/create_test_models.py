from django.core.management.base import BaseCommand
from jobhub.models import *

user_json = {
    'user':{
        'username':'john_doe',
        'last_name':'applicant',
        'first_name':'John Doe' ,
        'email': 'john@example.com', 
        'password': 'password123'
    },
    'personal_info':{
        'name':'John Doe', 
        'position': 'Software Developer', 
        'school': 'Tech High School', 
        'bio': 'Experienced Developer'
    },
    'contact_info':{
        'email':'john@example.com',
        'phone': '1234567890', 
        'address': '123 Main St, Tech City', 
        'linkedin': 'https://www.linkedin.com/in/johndoe'
    },
    'other_info':{
        'skills':'Python, Java, SQL', 
        'interests': 'AI, Machine Learning'
    },
    'education':{
        'school':'Tech University',
        'major':'Computer Science', 
        'start_time': '2015-09-01',
        'end_time': '2019-05-31', 
        'location': 'Tech City', 
        'description': 'Bachelor in Computer Science'
    },
    'work_experience':{
        'company':'Tech Corp', 
        'role':'Software Developer', 
        'start_time': '2019-06-01', 
        'type': 'Full-time', 
        'location': 'Tech City', 
        'description': 'Worked on several key projects'
    },
    'project_experience':{
        'project_name':'AI Project', 
        'role': 'Developer', 
        'start_time': '2020-01-01', 
        'end_time': '2020-12-31', 
        'location': 'Tech City', 
        'description': 'Developed an AI model'
    }
}

def create_user(user_json):
    user, created = User.objects.get_or_create(**user_json['user'])
    personal_info, created = PersonalInfo.objects.get_or_create(**user_json['personal_info'])
    contact_info, created = ContactInfo.objects.get_or_create(**user_json['contact_info'])
    other_info, created = OtherInfo.objects.get_or_create(**user_json['other_info'])
    education, created = Education.objects.get_or_create(**user_json['education'])
    work_experience, created = WorkExperience.objects.get_or_create(**user_json['work_experience'])
    project_experience, created = ProjectExperience.objects.get_or_create(**user_json['project_experience'])
    user_profile, created = UserProfile.objects.get_or_create(user=user,
                                                             personal_info=personal_info, 
                                                             contact_info= contact_info, 
                                                             other_info= other_info)
    user_profile.education.add(education)
    user_profile.work_experience.add(work_experience)
    user_profile.project_experience.add(project_experience)

def create():
    # =============================== Users ===========================================
    # Users
    user1, created = User.objects.get_or_create(username='john_doe',last_name='applicant',first_name='1' ,defaults={'email': 'john@example.com', 'password': 'password123'})
    user2, created = User.objects.get_or_create(username='jane_doe',last_name='employer',first_name='2' ,defaults={'email': 'jane@example.com', 'password': 'password123'})
    user3, created = User.objects.get_or_create(username='xuan_zhu',last_name='applicant',first_name='3' ,defaults={'email': 'xuan@example.com', 'password': 'xuanpassword'})

    # Personal Info
    personal_info1, created = PersonalInfo.objects.get_or_create(name='John Doe', defaults={'position': 'Software Developer', 'school': 'Tech High School', 'bio': 'Experienced Developer'})
    personal_info2, created = PersonalInfo.objects.get_or_create(name='Jane Doe', defaults={'position': 'Graphic Designer', 'school': 'Art High School', 'bio': 'Creative Designer'})
    personal_info3, created = PersonalInfo.objects.get_or_create(name='Xuan Zhu', defaults={'position': 'Data Scientist', 'school': 'Data High School', 'bio': 'Professional Scientist'})

    # Contact Info
    contact_info1, created = ContactInfo.objects.get_or_create(email='john@example.com', defaults={'phone': '1234567890', 'address': '123 Main St, Tech City', 'linkedin': 'https://www.linkedin.com/in/johndoe'})
    contact_info2, created = ContactInfo.objects.get_or_create(email='jane@example.com', defaults={'phone': '0987654321', 'address': '456 Elm St, Design City', 'linkedin': 'https://www.linkedin.com/in/janedoe'})
    contact_info3, created = ContactInfo.objects.get_or_create(email='xuan@example.com', defaults={'phone': '0923092323', 'address': '789 Fifth St, Tech City', 'linkedin': 'https://www.linkedin.com/in/xuanzhu'})

    # Other Info
    other_info1, created = OtherInfo.objects.get_or_create(skills='Python, Java, SQL', defaults={'interests': 'AI, Machine Learning'})
    other_info2, created = OtherInfo.objects.get_or_create(skills='Photoshop, Illustrator', defaults={'interests': 'Graphic Design, Typography'})
    other_info3, created = OtherInfo.objects.get_or_create(skills='Python, Tableau, R', defaults={'interests': 'Machine Learning, Data Visualization'})

    # Education
    education1, created = Education.objects.get_or_create(school='Tech University', major='Computer Science', defaults={'start_time': '2015-09-01', 'end_time': '2019-05-31', 'location': 'Tech City', 'description': 'Bachelor in Computer Science'})
    education2, created = Education.objects.get_or_create(school='Design University', major='Graphic Design', defaults={'start_time': '2016-09-01', 'end_time': '2020-05-31', 'location': 'Design City', 'description': 'Bachelor in Graphic Design'})
    education3, created = Education.objects.get_or_create(school='Data University', major='Data Scientist', defaults={'start_time': '2016-09-01', 'end_time': '2020-05-31', 'location': 'Data City', 'description': 'Bachelor in Data Science'})

    # Work Experience
    work_experience1, created = WorkExperience.objects.get_or_create(company='Tech Corp', role='Software Developer', defaults={'start_time': '2019-06-01', 'type': 'Full-time', 'location': 'Tech City', 'description': 'Worked on several key projects'})
    work_experience2, created = WorkExperience.objects.get_or_create(company='Design Studio', role='Graphic Designer', defaults={'start_time': '2020-07-01', 'type': 'Full-time', 'location': 'Design City', 'description': 'Lead designer for major campaigns'})
    work_experience3, created = WorkExperience.objects.get_or_create(company='Databricks', role='Data Scientist', defaults={'start_time': '2020-08-01', 'type': 'Full-time', 'location': 'Data City', 'description': 'Analyze Markting data'})

    # Project Experience
    project_experience1, created = ProjectExperience.objects.get_or_create(project_name='AI Project', defaults={'role': 'Developer', 'start_time': '2020-01-01', 'end_time': '2020-12-31', 'location': 'Tech City', 'description': 'Developed an AI model'})
    project_experience2, created = ProjectExperience.objects.get_or_create(project_name='Brand Design', defaults={'role': 'Lead Designer', 'start_time': '2021-02-01', 'location': 'Design City', 'description': 'Created brand identity for clients'})
    project_experience3, created = ProjectExperience.objects.get_or_create(project_name='Data Analysis', defaults={'role': 'Sr Data Scientist', 'start_time': '2021-03-01', 'location': 'Data City', 'description': 'Provide insightful data analysis'})

    # User Profiles
    user_profile1, created = UserProfile.objects.get_or_create(user=user1, defaults={'personal_info': personal_info1, 'contact_info': contact_info1, 'other_info': other_info1})
    user_profile1.education.add(education1)
    user_profile1.work_experience.add(work_experience1)
    user_profile1.project_experience.add(project_experience1)

    user_profile2, created = UserProfile.objects.get_or_create(user=user2, defaults={'personal_info': personal_info2, 'contact_info': contact_info2, 'other_info': other_info2})
    user_profile2.education.add(education2)
    user_profile2.work_experience.add(work_experience2)
    user_profile2.project_experience.add(project_experience2)

    user_profile3, created = UserProfile.objects.get_or_create(user=user3, defaults={'personal_info': personal_info3, 'contact_info': contact_info3, 'other_info': other_info3})
    user_profile3.education.add(education3)
    user_profile3.work_experience.add(work_experience3)
    user_profile3.project_experience.add(project_experience3)


    # =============================== Companies ===========================================

    company_info1, created = CompanyInfo.objects.get_or_create(
        name='Tech_Innovations', 
        defaults={
            'bio': 'Leading in AI technology.', 
            'industry': 'Technology', 
            'size': '500-1000 employees'
        }
    )

    company_contact1, created = CompanyContactInfo.objects.get_or_create(
        company=company_info1, 
        defaults={
            'phone': '1234567890', 
            'email': 'contact@techinnovations.com', 
            'address': '123 Tech Street, Tech City', 
            'website': 'https://www.techinnovations.com', 
            'linkedin': 'https://www.linkedin.com/company/tech-innovations'
        }
    )

    user4, created = User.objects.get_or_create(username=company_info1.name, last_name='employer', first_name='Tech Innovations', defaults={'email': company_contact1.email, 'password': 'techcompany123'})

    company_review1, created = CompanyReview.objects.get_or_create(
        company=company_info1, 
        user=user4, 
        defaults={
            'overall_rating': 4.5, 
            'interview_progression_rating': 4.6, 
            'application_response_time_rating': 4.2, 
            'benefits_during_interview_rating': 4.0, 
            'interview_atmosphere_rating': 4.7, 
            'interview_etiquette_rating': 4.5, 
            'five_star_rating': 150, 
            'four_star_rating': 80, 
            'three_star_rating': 30, 
            'two_star_rating': 10, 
            'one_star_rating': 5
        }
    )

    individual_review1, created = IndividualReview.objects.get_or_create(
        title='Great Experience', 
        user=user1, 
        defaults={
            'role': 'Software Developer', 
            'overall_rating': 5, 
            'interview_progression_rating': 5, 
            'application_response_time_rating': 4, 
            'benefits_during_interview_rating': 5, 
            'interview_atmosphere_rating': 5, 
            'interview_etiquette_rating': 5, 
            'review': 'My experience with the company was exceptional. The interview process was smooth and the team was very professional.'
        }
    )

    company_profile1, created = CompanyProfile.objects.get_or_create(
        user=user4, 
        defaults={
            'company_info': company_info1, 
            'company_contact_info': company_contact1, 
            'company_review': company_review1
        }
    )

    # Add the individual reviews and public staff list to the company profile
    company_profile1.individual_reviews.add(individual_review1)
    company_profile1.public_staff_list.add(user_profile1)



    # Company Info
    company_info2, created = CompanyInfo.objects.get_or_create(
        name='EcoGreen Solutions', 
        defaults={
            'bio': 'Pioneering sustainable energy solutions.', 
            'industry': 'Renewable Energy', 
            'size': '200-500 employees'
        }
    )

    # Company Contact Info
    company_contact2, created = CompanyContactInfo.objects.get_or_create(
        company=company_info2, 
        defaults={
            'phone': '9876543210', 
            'email': 'info@ecogreensolutions.com', 
            'address': '456 Green Way, Eco City', 
            'website': 'https://www.ecogreensolutions.com', 
            'linkedin': 'https://www.linkedin.com/company/ecogreen-solutions'
        }
    )

    # Company Review
    company_review2, created = CompanyReview.objects.get_or_create(
        company=company_info2, 
        user=user2, 
        defaults={
            'overall_rating': 4.2, 
            'interview_progression_rating': 4.0, 
            'application_response_time_rating': 3.8, 
            'benefits_during_interview_rating': 4.5, 
            'interview_atmosphere_rating': 4.3, 
            'interview_etiquette_rating': 4.4, 
            'five_star_rating': 120, 
            'four_star_rating': 70, 
            'three_star_rating': 25, 
            'two_star_rating': 15, 
            'one_star_rating': 8
        }
    )

    # Individual Review
    individual_review2, created = IndividualReview.objects.get_or_create(
        title='Innovative and Inspiring Workplace', 
        user=user2, 
        defaults={
            'role': 'Environmental Engineer', 
            'overall_rating': 5, 
            'interview_progression_rating': 4, 
            'application_response_time_rating': 4.5, 
            'benefits_during_interview_rating': 4.5, 
            'interview_atmosphere_rating': 4.5, 
            'interview_etiquette_rating': 4.5, 
            'review': 'Working at EcoGreen Solutions has been a transformative experience. The focus on innovation and sustainability is truly inspiring.'
        }
    )

    # Company Profile
    company_profile2, created = CompanyProfile.objects.get_or_create(
        user=user2, 
        defaults={
            'company_info': company_info2, 
            'company_contact_info': company_contact2, 
            'company_review': company_review2
        }
    )

    # Add the individual reviews and public staff list to the company profile
    company_profile2.individual_reviews.add(individual_review2)
    company_profile2.public_staff_list.add(user_profile2)

    # =============================== Jobs ===========================================

    # Job Summaries
    job_summary1, created = JobSummary.objects.get_or_create(
        post_time='2023-02-01', 
        due_time='2023-02-20', 
        defaults={
            'job_type': 'full-time',
            'location': 'Los Angeles', 
            'estimate_pay_lower': 60000, 
            'estimate_pay_upper': 80000, 
            'note': 'Flexible hours'
        }
    )

    job_summary2, created = JobSummary.objects.get_or_create(
        post_time='2023-03-05', 
        due_time='2023-04-05', 
        defaults={
            'job_type': 'part-time',
            'location': 'Chicago', 
            'estimate_pay_lower': 70000, 
            'estimate_pay_upper': 90000, 
            'note': 'Remote work available'
        }
    )

    job_summary3, created = JobSummary.objects.get_or_create(
        post_time='2023-04-10', 
        due_time='2023-05-10', 
        defaults={
            'job_type': 'internship',
            'location': 'Boston', 
            'estimate_pay_lower': 55000, 
            'estimate_pay_upper': 75000, 
            'note': 'Part-time position'
        }
    )

    job_summary4, created = JobSummary.objects.get_or_create(
        post_time='2023-06-15', 
        due_time='2023-07-30', 
        defaults={
            'job_type': 'full-time',
            'location': 'New York', 
            'estimate_pay_lower': 80000, 
            'estimate_pay_upper': 100000, 
            'note': 'Opportunity for extension'
        }
    )

    job_summary5, created = JobSummary.objects.get_or_create(
        post_time='2023-08-01', 
        due_time='2023-09-15', 
        defaults={
            'job_type': 'full-time',
            'location': 'San Francisco', 
            'estimate_pay_lower': 90000, 
            'estimate_pay_upper': 110000, 
            'note': 'Work on exciting new projects'
        }
    )

    # Job Highlights
    job_highlight1, created = JobHighlight.objects.get_or_create(content='Join a dynamic team of innovators.')
    job_highlight2, created = JobHighlight.objects.get_or_create(content='Opportunity to work with leading industry experts.')
    job_highlight3, created = JobHighlight.objects.get_or_create(content='Be part of a groundbreaking project.')
    job_highlight4, created = JobHighlight.objects.get_or_create(content='Cutting-edge technology projects.')
    job_highlight5, created = JobHighlight.objects.get_or_create(content='Collaborative and innovative work environment.')

    # Job Details
    job_detail1, created = JobDetail.objects.get_or_create(content='Responsibilities include project management and team leadership.')
    job_detail2, created = JobDetail.objects.get_or_create(content='Focus on developing cutting-edge software solutions.')
    job_detail3, created = JobDetail.objects.get_or_create(content='Involves extensive research and development in renewable energy.')
    job_detail4, created = JobDetail.objects.get_or_create(content='Engage in complex problem-solving scenarios.')
    job_detail5, created = JobDetail.objects.get_or_create(content='Lead design and implementation of new features.')


    # Jobs
    job1, created = Job.objects.get_or_create(
        name='Project Manager',
        defaults={
            'company': company_profile1,
            'summary': job_summary1,
            'highlight': job_highlight1,
            'detail': job_detail1
        }
    )

    job2, created = Job.objects.get_or_create(
        name='Software Developer',
        defaults={
            'company': company_profile1,  # or company_profile2 if it belongs to a different company
            'summary': job_summary2,
            'highlight': job_highlight2,
            'detail': job_detail2
        }
    )

    job3, created = Job.objects.get_or_create(
        name='Research Analyst',
        defaults={
            'company': company_profile1,  # assuming this job belongs to company_profile2
            'summary': job_summary3,
            'highlight': job_highlight3,
            'detail': job_detail3
        }
    )
    
    job4, created = Job.objects.get_or_create(
        name='Contract Developer',
        defaults={
            'company': company_profile2,  # Assume this job belongs to company_profile2
            'summary': job_summary4,
            'highlight': job_highlight4,
            'detail': job_detail4
        }
    )

    job5, created = Job.objects.get_or_create(
        name='Freelance UX Designer',
        defaults={
            'company': company_profile2,  # Assume this job belongs to company_profile2
            'summary': job_summary5,
            'highlight': job_highlight5,
            'detail': job_detail5
        }
    )




class Command(BaseCommand):
    help = 'Generates test data for your app'

    def handle(self, *args, **kwargs):
        # Your data creation logic here
        create()
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
        