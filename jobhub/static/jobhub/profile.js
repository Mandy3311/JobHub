function editBasicPersonalInfo() {
    $("#basic-personl-info").hide();
    $('#basic-personl-info-form').show();
}

function cancelEditBasicPersonalInfo() {
    $("#basic-personl-info-form").hide();
    $('#basic-personl-info').show();
}

function editContactInfo() {
    $("#contact-info").hide();
    $('#contact-info-form').show();
}

function cancelEditContactInfo() {
    $("#contact-info-form").hide();
    $('#contact-info').show();
}
var education_id = 0; // 0 none, -1 add

function format_date(date_str) {
    // convert this type of  Nov. 21, 2023 to 2023-11-21
    var date = new Date(date_str);
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    // if month or day is less than 10, add a 0 in front
    if (month < 10) {
        month = '0' + month;
    }
    if (day < 10) {
        day = '0' + day
    }
    return year + '-' + month + '-' + day
}


function setEducationEditValues(id) {
    if (id == -1) {
        $('#education-addSchool').val('');
        $('#education-addMajor').val('');
        $('#education-addStartDate').val('');
        $('#education-addEndDate').val('');
        $('#education-addGPA').val('');
        $('#education-addLocation').val('');
        $('#education-addDescription').val('');
        return;
    }
    $('#education-addSchool').val($('#education-' + id + '-school').text());
    $('#education-addMajor').val($('#education-' + id + '-major').text());
    $('#education-addStartDate').val(format_date($('#education-' + id + '-start').text()));
    $('#education-addEndDate').val(format_date($('#education-' + id + '-end').text()));
    $('#education-addGPA').val($('#education-' + id + '-gpa').text());
    $('#education-addLocation').val($('#education-' + id + '-location').text());
    $('#education-addDescription').val($('#education-' + id + '-description').text());
}

function editEducation(id) {
    if (education_id != 0) {
        cancelEditEducation();
    }
    education_id = id;
    console.log('new edu selected', id);
    // # set the education_id element's hidden value to id
    $("#education_id").val(id);
    setEducationEditValues(id);

    if (id == -1) {
        $("#education-add").hide();
        $('#education-add-form').show();
        return;
    }
    $("#education-" + id).hide();
    $('#education-add-form').show();

    // set the education forms after #education-" + id
    $("#education-add-form").insertAfter("#education-" + id);
}

var work_experience_id = 0; // 0 none, -1 add

function setWorkExperienceEditValues(id) {
// {% endblock %}
    if (id == -1) {
        $('#work-addCompany').val('');
        $('#work-addRole').val('');
        $('#work-addStartDate').val('');
        $('#work-addEndDate').val('');
        $('#work-addType').val('');
        $('#work-addLocation').val('');
        $('#work-addDescription').val('');
        return;
    }
    $('#work-addCompany').val($('#work-experience-' + id + '-company').text());
    $('#work-addRole').val($('#work-experience-' + id + '-role').text());
    $('#work-addStartDate').val(format_date($('#work-experience-' + id + '-start').text()));
    $('#work-addEndDate').val(format_date($('#work-experience-' + id + '-end').text()));
    $('#work-addType').val($('#work-experience-' + id + '-type').text());
    $('#work-addLocation').val($('#work-experience-' + id + '-location').text());
    $('#work-addDescription').val($('#work-experience-' + id + '-description').text());
}

function editWorkExperience(id) {
    if (work_experience_id != 0) {
        cancelEditWorkExperience();
    }
    work_experience_id = id;
    $("#work_id").val(id);
    setWorkExperienceEditValues(id);
    if (id == -1) {
        $("#work-experience-add").hide();
        $('#work-experience-form').show();
        return;
    }
    $("#work-experience-" + id).hide();
    $('#work-experience-form').show();

    $("#work-experience-form").insertAfter("#work-experience-" + id);
}

var project_experience_id = 0; // 0 none, -1 add

function setProjectExperienceEditValues(id) {
    if (id == -1) {
        $('#project-addProject').val('');
        $('#project-addRole').val('');
        $('#project-addStartDate').val('');
        $('#project-addEndDate').val('');
        $('#project-addLocation').val('');
        $('#project-addDescription').val('');
        return;
    }
    $('#project-addProject').val($('#project-experience-' + id + '-name').text());
    $('#project-addRole').val($('#project-experience-' + id + '-role').text());
    $('#project-addStartDate').val(format_date($('#project-experience-' + id + '-start').text()));
    $('#project-addEndDate').val(format_date($('#project-experience-' + id + '-end').text()));
    $('#project-addLocation').val($('#project-experience-' + id + '-location').text());
    $('#project-addDescription').val($('#project-experience-' + id + '-description').text());
}
function editProjectExperience(id) {
    if (project_experience_id != 0) {
        cancelEditProjectExperience();
    }
    project_experience_id = id;
    $("#project_id").val(id);
    setProjectExperienceEditValues(id);
    if (id == -1) {
        $("#project-experience-add").hide();
        $('#project-experience-form').show();
        return;
    }
    $("#project-experience-" + id).hide();
    $('#project-experience-form').show();

    $("#project-experience-form").insertAfter("#project-experience-" + id);
}

function cancelEditProjectExperience() {
    var id = project_experience_id;
    if (id == -1) {
        $("#project-experience-add").show();
        $('#project-experience-form').hide();
    }
    $("#project-experience-form").hide();
    $("#project-experience-" + id).show();

    // set form back to project-add-block
    $("#project-experience-form").insertAfter("#project-experience-add");
    project_experience_id = 0;
}

function cancelEditWorkExperience() {
    if (work_experience_id == -1) {
        $("#work-experience-add").show();
        $('#work-experience-form').hide();
    }
    $("#work-experience-form").hide();
    $("#work-experience-" + work_experience_id).show();
    
    $("#work-experience-form").insertAfter("#work-experience-add");
    work_experience_id = 0;
}

function cancelEditEducation() {
    var id = education_id;
    if (id == -1) {
        $("#education-add").show();
        $('#education-add-form').hide();
    }
    $("#education-add-form").hide();
    $("#education-" + id).show();

    // set form back to edu-add-block
    $("#education-add-form").insertAfter("#education-add");
    education_id = 0;
}

function filterIndividualReviews(){
    var job_title = $('#job-title').val();
    var rating = $('#rating').val();
    var time_frame = $('#time-frame').val();
    // get all elements with class individual-review
    var individual_reviews = $('.individual-review');
    // filter the reviews. if the review matches the filter, show it. otherwise, hide it. ignore the time-frame
    // <div class="card individual-review" data-job-title="{{ review.role }}" data-rating="{{ review.overall_rating }}">
    for (var i = 0; i < individual_reviews.length; i++) {
        var review = $(individual_reviews[i]);
        var review_job_title = review.data('job-title');
        var review_rating = review.data('rating');
        var review_date = review.data('date');
        if (review_job_title == job_title || job_title == 'all') {
            if (review_rating == rating || rating == 'all') {
                if (isDateInTimeFrame(review_date, time_frame)) {
                    review.show();
                } else {
                    review.hide();
                }
            } else {
                review.hide();
            }
        } else {
            review.hide();
        }
    }
}

function isDateInTimeFrame(date, time_frame) {
    var today = new Date();
    var today_year = today.getFullYear();
    var today_month = today.getMonth();
    var today_date = today.getDate();
    var today_str = today_year + '-' + today_month + '-' + today_date;
    var today_date = new Date(today_str);
    var date_date = new Date(date); 
    var time_diff = today_date - date_date;
    var days_diff = time_diff / (1000 * 3600 * 24);
    if (time_frame == 'all') {
        return true;
    }
    if (time_frame == '1-month') {
        return days_diff <= 30;
    }
    if (time_frame == '6-months') {
        return days_diff <= 30 * 6;
    }
    if (time_frame == '1-year') {
        return days_diff <= 365;
    }
    if (time_frame == '3-years') {
        return days_diff <= 365 * 3;
    }
    return false;
}
function copyUserId() {
    var userId = $('#userId').text();
    var $temp = $("<textarea>");
    $('body').append($temp);
    $temp.val(userId).select();
    document.execCommand("copy");
    $temp.remove();
    alert("User ID copied: " + userId); // Optional
}
function deleteStaff(user_id) {
    var url = '/delete_staff/';

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'user_id': user_id,
        },
        success: function (data) {
            if (data['success']) {
                $('#staff-' + user_id).remove();
                $('#staff-' + user_id + '-add').remove();

            } else {
                alert(data['error']);
            }
        },
        error: function (data) {
            alert('Error: ' + data);
        }
    });
}
function deleteReview(review_id, company_user_id) {
    var url = '/delete_review/';

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'review_id': review_id,
            'company_user_id': company_user_id,
        },
        success: function (data) {
            if (data['success']) {
                $('#review-' + review_id).remove();
                var overall_rating = data['company_review']['overall_rating'].toFixed(1);
                $('#overall_rating').text(overall_rating);
                // iterate set the fill color of the stars according to the overall_rating
                // Assuming each star SVG has a class 'star-svg' and an id like 'star-1', 'star-2', etc.

                $('.star-svg').each(function(index) {
                    var starIndex = index + 1; // because index is zero-based
                    if (starIndex <= overall_rating) {
                        // Fill the star
                        $(this).find('path').attr('fill', '#FFD700');
                    } else {
                        // Unfill the star
                        $(this).find('path').attr('fill', '#C4C4C4');
                    }
                    // reload the element
                    
                });

                // change the bar progress
                $('#five_star_progress').css('width', data['company_review']['five_star_rating'] + '%');
                $('#four_star_progress').css('width', data['company_review']['four_star_rating'] + '%');
                $('#three_star_progress').css('width', data['company_review']['three_star_rating'] + '%');
                $('#two_star_progress').css('width', data['company_review']['two_star_rating'] + '%');
                $('#one_star_progress').css('width', data['company_review']['one_star_rating'] + '%');

                $('#interview_progression_rating').text(data['company_review']['interview_progression_rating'].toFixed(1));
                $('#application_response_time_rating').text(data['company_review']['application_response_time_rating'].toFixed(1));
                $('#benefits_during_interview_rating').text(data['company_review']['benefits_during_interview_rating'].toFixed(1));
                $('#interview_atmosphere_rating').text(data['company_review']['interview_atmosphere_rating'].toFixed(1));
                $('#interview_etiquette_rating').text(data['company_review']['interview_etiquette_rating'].toFixed(1));

            } else {
                alert(data['error']);
            }
        },
        error: function (data) {
            alert('Error: ' + data);
        }
    });
}

function deleteCard(type, item_id) {
    var url = '/delete_experience/';

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'type': type,
            'item_id': item_id,
        },
        success: function (data) {
            if (data['success']) {
                $('#' + type + '-' + item_id).remove();
            } else {
                alert(data['error']);
            }
        },
        error: function (data) {
            alert('Error: ' + data);
        }
    });
}

$(document).ready(function () {
    var form_type = $('body').data('form-type');
    // split format_type with _
    var form_type_split = form_type.split('_');
    // if the first part is 'education' and the second part is a number
    if (form_type_split[0] == 'education') {
        if (form_type_split[1] == 'add') {
            editEducation(-1);
        } else {
            var id = parseInt(form_type_split[1]);
            editEducation(id);
        }
    }
    if (form_type_split[0] == 'work') {
        if (form_type_split[1] == 'add') {
            editWorkExperience(-1);
        } else {
            var id = parseInt(form_type_split[1]);
            editWorkExperience(id);
        }
    }
    if (form_type_split[0] == 'project') {
        if (form_type_split[1] == 'add') {
            editProjectExperience(-1);
        } else {
            var id = parseInt(form_type_split[1]);
            editProjectExperience(id);
        }
    }

    // contact info
    $("#contact-info-edit").click(function () {
        $("#contact-info").hide();

        $('#contact-info-form').show();
    });
    $("#contact-info-cancel").click(function () {
        $("#contact-info-form").hide();
        $('#contact-info').show();
    });

    // skills
    $("#skills-edit").click(function () {
        $("#skills").hide();
        $('#skills-form').show();
    });
    $("#skills-cancel").click(function () {
        $("#skills-form").hide();
        $('#skills').show();
    });

    // interests
    // $("#interests-edit").click(function() {
    //     $("#interests").hide();
    //     $('#interests-form').show();
    // });
    // $("#interests-cancel").click(function() {
    //     $("#interests-form").hide();
    //     $('#interests').show();
    // });
    // education
    // $("#education-edit").click(function() {
    //     $("#education").hide();
    //     $('#education-add').hide();
    //     $('#education-form').show();
    // });
    // $("#education-cancel").click(function() {
    //     $("#education-form").hide();
    //     $('#education').show();
    //     $('#education-add').show();
    // });
    // $("#education-add").click(function() {
    //     $(this).hide();
    //     $("#education-form").show();
    // });

    // work experience
    // Binding click events similar to the education part
    // $(".work-experience-edit").click(function () {
    //     var id = $(this).data("id");
    //     editWorkExperience(id);
    // });

    // $("#work-experience-cancel").click(function () {
    //     cancelEditWorkExperience();
    // });

    // $("#work-experience-add").click(function () {
    //     $(this).hide();
    //     $("#work-experience-form").show();
    //     editWorkExperience(-1);
    // });

    // // project experience
    // $("#project-experience-edit").click(function () {
    //     $("#project-experience").hide();
    //     $('#project-experience-add').hide();
    //     $('#project-experience-form').show();
    // });
    // $("#project-experience-cancel").click(function () {
    //     $("#project-experience-form").hide();
    //     $('#project-experience').show();
    //     $('#project-experience-add').show();
    // });
    // $("#project-experience-add").click(function () {
    //     $(this).hide();
    //     $("#project-experience-form").show();
    // });

    // ------------------ company profile ------------------
    // basic company info
    $("#basic-company-info-edit").click(function () {
        $("#basic-company-info").hide();
        $('#basic-company-info-form').show();
    });
    $("#basic-company-info-cancel").click(function () {
        $("#basic-company-info-form").hide();
        $('#basic-company-info').show();
    });

    // company contact info
    $("#company-contact-info-edit").click(function () {
        $("#company-contact-info").hide();
        $('#company-contact-info-form').show();
    });
    $("#company-contact-info-cancel").click(function () {
        $("#company-contact-info-form").hide();
        $('#company-contact-info').show();
    });

    // staff list
    $("#staff-list-edit").click(function () {
        $("#staff-list").hide();
        $('#staff-list-form').show();
    });
    $("#staff-list-cancel").click(function () {
        $("#staff-list-form").hide();
        $('#staff-list').show();
    });



    // add review button
    $('#addReviewButton').click(function () {
        $(this).hide();
        $('#addReviewForm').show();
    });

    $('#cancelButton').click(function () {
        $('#addReviewForm').hide();
        $('#addReviewButton').show();
    });
});
