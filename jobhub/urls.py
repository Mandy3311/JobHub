from django.urls import path
from jobhub import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("other_company_profile/", views.other_company_profile, name="other_company_profile"),
    path("other_user_profile/", views.other_user_profile, name="other_user_profile"),

    path("joblist/", views.joblist,name='joblist'),
    path("joblist/getlist", views.joblist_getlist,name='joblist_getlist'),
    path("joblist/getdetail", views.joblist_getdetail,name='joblist_getdetail'),
    path("joblist/search", views.joblist_search,name='joblist_search'),

    path("joblist/submit", views.joblist_submit_application,name='joblist_submit'),
    path("joblist/withdraw", views.joblist_withdraw_application,name='joblist_withdraw'),

    path("base_user_profile/", views.base_user_profile, name="base_user_profile"),
    path("base_company_profile/", views.base_company_profile, name="base_company_profile"),
    path("delete_experience/", views.delete_experience, name="delete_experience"),
    path("delete_staff/", views.delete_staff, name="delete_staff"),
    path("delete_review/", views.delete_review, name="delete_review"),

    path('applicant_application/<str:filter_by>/', views.a_application, name='applicant_application'),
    path('applicant_application/get-application/<str:filter_by>/', views.get_application, name='get-application'),
    path("employer_application/<int:id>/<str:filter_by>/", views.e_application, name="employer_application"),
    path('employer_application/get-applicant/<int:id>/<str:filter_by>/', views.get_applicant, name='get-applicant'),
    path('update_application_status/', views.update_application_status, name='update_application_status'),
    
    path("logout/", views.logout_action, name="logout"),
]