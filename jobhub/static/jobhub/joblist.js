"use strict"

let filter_args = {};

document.addEventListener('DOMContentLoaded', function() {
    let modal = $('#myModal');
    let btn = $('#apply-button');
    btn.off('click');
    let span  = $("#submit-application-cancel");

    // Open the modal
    btn.on('click', function() {
        $('#submit-message').empty();
        submit_application();
        modal.css('display', 'block');
    });
    // Close the modal
    span.on('click' ,function() {
        modal.css('display', 'none');
    });
});


function submit_application(){
    let job_id = $('#main').attr('job_id');
    $.ajax({
        url: '/joblist/submit', // URL to which the request is sent
        type: 'GET', // Type of request (GET, POST, etc.)
        dataType: 'json', // The type of data expected from the server
        data: { // Data to be sent to the server
            job_id: job_id
        },
        success: function(response) {
            // Code to execute when the request is successful
            submit_window();
            get_detail(job_id);
        },
        error: function(xhr, status, error) {
            // Code to execute if the request fails
            console.log(xhr);
            console.log(xhr['responseJSON']['error']);
            submit_window(xhr['responseJSON']['error']);
        }
    });    
}

function withdraw_application(){
    let job_id = $('#main').attr('job_id');
    $.ajax({
        url: '/joblist/withdraw', // URL to which the request is sent
        type: 'GET', // Type of request (GET, POST, etc.)
        dataType: 'json', // The type of data expected from the server
        data: { // Data to be sent to the server
            job_id: job_id
        },
        success: function(response) {
            // Code to execute when the request is successful
            submit_window('Application Withdrawed.');
            get_detail(job_id);

        },
        error: function(xhr, status, error) {
            // Code to execute if the request fails
            console.log(xhr);
            console.log(xhr['responseJSON']['error']);
            submit_window(xhr['responseJSON']['error']);
        }
    });    
}

function submit_window(message = "Application Submitted.Good luck!"){
    $('<h3>', {text: message}).appendTo($('#submit-message'))
}

function display_tool_bar(display=true){
    let tool_bar = $('#tools-bar');
    if(display==true){
        tool_bar.show();
    }
    else{
        tool_bar.hide();
    }
    
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

/******************************* AJAX ******************************/
window.onload = page_ready;
// window.setInterval(get_jobs, 5000);

function page_ready(){
    for (const [key, value] of new URLSearchParams(window.location.search)) {
        filter_args[key] = value;
    }
    console.log(filter_args);
    get_jobs(filter_args);
    init_filter();  

}


function filter_button_onlick(button_id,exclusive_button_ids,key,value) {
    let not_active = $(button_id).hasClass('toggle-button');

    // deactivate all
    for (let id of exclusive_button_ids){
        if($(id).hasClass('toggle-button-active')){
            $(id).removeClass('toggle-button-active').addClass('toggle-button');
            delete filter_args[key];
        }
    }
    
    if (not_active) {
        filter_args[key] = value;
        $(button_id).removeClass('toggle-button').addClass('toggle-button-active');
    } else {
        delete filter_args[key];
        $(button_id).removeClass('toggle-button-active').addClass('toggle-button');
    }
    console.log(filter_args);
    get_jobs(filter_args);
}

function bind_filter_group(filter_config){
    let button_ids = Object.keys(filter_config);
    for (let id of button_ids){
        $(id).click(function(){
            filter_button_onlick(id,button_ids,filter_config[id]['key'],filter_config[id]['value']);
        });
    }
}

function init_filter(){

    $('#search-form').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        $.ajax({
            url: '/joblist/search', // The URL to send the data to
            type: 'GET', // The HTTP method to use for the request
            data: $(this).serialize(), // Serialize the form data for sending
            success: function(response) {
                // Handle success - 'response' contains whatever the server sends back
                console.log('Search successful:', response)

                // Reset filter
                $(".toggle-button-active").each(function(index) {
                    $(this).removeClass('toggle-button-active').addClass('toggle-button');
                });
                filter_args = {};

                filter_args['search'] = $('#search-input').val();
                update_jobs(response);
                if(response.length > 0){
                    get_detail(response[0]['id']);
                }
                else{
                    update_empty_jobs();
                }

            },
            error: function(xhr, status, error) {
                // Handle errors
                console.log('Search failed:', error);
            }
        });
    });

    let job_type_buttons = {
        '#filter-full-time': {
            'key':'summary__job_type',
            'value':'full-time'
        },
        '#filter-part-time': {
            'key':'summary__job_type',
            'value':'part-time'
        },
        '#filter-internship': {
            'key':'summary__job_type',
            'value':'internship'
        },
    }
    bind_filter_group(job_type_buttons);

    let job_date_buttons = {
        '#filter-24-hours': {
            'key':'summary__post_time__gte',
            'value':new Date(new Date().setDate(new Date().getDate() - 1)).toISOString().split('T')[0]
        },
        '#filter-week': {
            'key':'summary__post_time__gte',
            'value':new Date(new Date().setDate(new Date().getDate() - 7)).toISOString().split('T')[0]
        },
        '#filter-month': {
            'key':'summary__post_time__gte',
            'value':new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0]
        },
    }
    bind_filter_group(job_date_buttons);
}

function get_jobs(filter = undefined){
    $.ajax({
        url: '/joblist/getlist', // URL to which the request is sent
        type: 'GET', // Type of request (GET, POST, etc.)
        dataType: 'json', // The type of data expected from the server
        data: {
            filter:JSON.stringify(filter),
        },
        success: function(response) {
            // Code to execute when the request is successful
            update_jobs(response);
            if(response.length > 0){
                get_detail(response[0]['id']);
            }
            else{
                update_empty_jobs();

            }
        },
        error: function(xhr, status, error) {
            // Code to execute if the request fails
            console.log('Error: ' + error);
        }
    });    
}

function update_jobs(response){
    // Removes all existing jobs
    let list = $('#list')
    list.empty()
    for (let item of response) {
        make_job_element(item).appendTo(list)
    }
}

function update_empty_jobs(){
    // Removes all existing jobs
    let list = $('#list');
    list.empty();
    $('<div>', { text: 'No Job Found',class:'email-item email-item-selected pure-g'}).appendTo(list);
    let main = $('#main');
    main.empty();
    display_tool_bar(false);
}

function make_job_element(job_json){
    // Create the main div
    let main_div = $('<div>', {class: 'email-item email-item-selected pure-g',id: `job_${job_json['id']}`});
    console.log(job_json);
    // Create the inner div for the image
    let img_div = $('<div>', {class: 'pure-u'}).appendTo(main_div);
    $('<img>', {
        width: '64',
        height: '64',
        alt: "Tilo Mitra's avatar",
        class: 'email-avatar',
        src: job_json['company']['picture']
    }).appendTo(img_div);

    // Create the inner div for the text content
    let text_div = $('<div>', {class: 'pure-u-3-4'}).appendTo(main_div);
    $('<h5>', {class: 'email-name', text: job_json['company']['company_info']['name']}).appendTo(text_div);
    $('<h4>', {class: 'email-subject', text: job_json['name']}).appendTo(text_div);
    $('<p>', {class: 'email-desc', text: 'Post Time: ' + job_json['summary']['post_time']}).appendTo(text_div);

    main_div.click(function() {
        console.log("Clicked on job:", job_json['name']);
        get_detail(job_json['id']);
    });

    return main_div
}



function get_detail(job_id){
    $.ajax({
        url: '/joblist/getdetail', // URL to which the request is sent
        type: 'GET', // Type of request (GET, POST, etc.)
        dataType: 'json', // The type of data expected from the server
        data: { // Data to be sent to the server
            job_id: job_id
        },
        success: function(response) {
            // Code to execute when the request is successful
            console.log(response);
            update_detail(response,job_id);

            update_job_css(response);
        },
        error: function(xhr, status, error) {
            // Code to execute if the request fails
            console.log('Error: ' + error);
        }
    });    
}


function update_detail(response,job_id){
    // Removes all existing jobs
    let main = $('#main');
    main.empty();
    main.attr('job_id',job_id);


    let item = response;
    make_detail_header(item).appendTo(main)
    make_detail_body(item).appendTo(main)

    update_apply_button(item);
    display_tool_bar(true);
}

function update_apply_button(job_json){
    let application = job_json['application'];
    let btn = $('#apply-button');
    btn.off('click');
    btn.empty()
    let modal = $('#myModal');
    
    if(application!=null){
        btn.text('WITHDRAW');
        btn.on('click',function() {
            $('#submit-message').empty();   
            withdraw_application();
            modal.css('display', 'block');
        }) ;
    }
    else{
        btn.text('APPLY');
        btn.on('click',function() {
            $('#submit-message').empty();
            submit_application();
            modal.css('display', 'block');
        }) ;
    }

}

function update_job_css(response){
    let job_id = `job_${response['id']}`;
    $('.email-item').each(function(){
        if(job_id == $(this).attr('id')){
            $(this).attr('class', 'email-item email-item-unread pure-g')
        }
        else{
            $(this).attr('class', 'email-item email-item-selected pure-g')
        }
    })
}

function make_detail_header(job_json){
    let application = job_json['application'];

    // Create the header container div
    let header_div = $('<div>', {class: 'email-content-header pure-g',id:'main-header'});


    // Create the first inner div and its contents
    let text_div = $('<div>', {class: 'pure-u-1-2'}).appendTo(header_div);
    $('<h1>', {class: 'email-content-title', text: job_json['name']}).appendTo(text_div);
    let paragraph = $('<p>', {class: 'email-content-subtitle'}).appendTo(text_div);
    $('<a>', {text: job_json['company']['company_info']['name'], href:`/other_company_profile/?company_id=${job_json['company']['user_id']}`}).appendTo(paragraph);

    
    let date_text = application? `Applied: ${application['submitdate']}`:'Not Applied';
    $('<span>', {class: 'pure-g', text: date_text}).appendTo(paragraph);

    

    // Create the second inner div and its buttons
    let button_div = $('<div>', {class: 'email-content-controls pure-u-1-2'}).appendTo(header_div);

    let button_link = $('<a>',{href: `mailto:${job_json['company']['company_contact_info']['email']}?subject=Inquiry from Job Applicant`}).appendTo(button_div)
    $('<button>', { class: 'secondary-button pure-button',
                    text: 'Contact Recruiter', 
                    }).appendTo(button_link);

    // Append the main div to the body or another element in your DOM
    return header_div;
}

function make_detail_body(job_json){
    let body_div = $('<div>', {class: 'email-content-body'});

    $('<h2>', {class: 'content-subhead-right', text: 'Job Description'}).appendTo(body_div);

    make_detail_summary_card(job_json).appendTo(body_div);
    make_detail_card(job_json,'highlight').appendTo(body_div);
    make_detail_card(job_json,'detail').appendTo(body_div);

    $('<h2>', {class: 'content-subhead-right', text: 'About the Company'}).appendTo(body_div);
    make_detail_company_card(job_json).appendTo(body_div)
    return body_div;
}

function make_detail_summary_card(job_json){

    let summary_card_div = $('<div>', {class: 'card'})
    $('<h3>', {text: 'Role Summary'}).appendTo(summary_card_div);

    let grid_div = $('<div>', {class: 'pure-g'}).appendTo(summary_card_div);

    let grid_left_div = $('<div>', {class: 'pure-u-1 pure-u-md-1-2'}).appendTo(grid_div);
    $('<span>', {text: `Application deadline: ${job_json['summary']['due_time']}`}).appendTo(grid_left_div);
    grid_left_div.append('<br>');
    $('<span>', {text: `Posted date: ${job_json['summary']['post_time']}`}).appendTo(grid_left_div);

    let grid_right_div = $('<div>', {class: 'pure-u-1 pure-u-md-1-2'}).appendTo(grid_div);
    $('<span>', {text: `Estimated Pay: $${job_json['summary']['estimate_pay_lower']} - ${job_json['summary']['estimate_pay_upper']} per year`}).appendTo(grid_right_div);
    grid_right_div.append('<br>');
    $('<span>', {text: `Location: ${job_json['summary']['location']}`}).appendTo(grid_right_div);

    $('<p>', {text: `${job_json['summary']['note']}`}).appendTo(grid_div);

    return summary_card_div
}

function make_detail_card(job_json,key){

    let card_div = $('<div>', {class: 'card'})
    $('<h3>', {text: `Role ${capitalizeFirstLetter(key)}`}).appendTo(card_div);

    let grid_div = $('<div>', {class: 'pure-g'}).appendTo(card_div);

    $('<p>', {text: `${job_json[key]['content']}`}).appendTo(grid_div);

    return card_div
}


function make_detail_company_card(job_json){

    let company_card_div = $('<div>', {class: 'card'})
    $('<h3>', {text: 'Company Summary'}).appendTo(company_card_div);

    let grid_div = $('<div>', {class: 'pure-g'}).appendTo(company_card_div);

    let grid_left_div = $('<div>', {class: 'pure-u-1 pure-u-md-1-2'}).appendTo(grid_div);
    $('<span>', {text: `Name: ${job_json['company']['company_info']['name']}`}).appendTo(grid_left_div);
    grid_left_div.append('<br>');
    $('<span>', {text: `Employees: ${job_json['company']['company_info']['size']}`}).appendTo(grid_left_div);

    let grid_right_div = $('<div>', {class: 'pure-u-1 pure-u-md-1-2'}).appendTo(grid_div);
    $('<span>', {text: `Industry: ${job_json['company']['company_info']['industry']}`}).appendTo(grid_right_div);
    grid_right_div.append('<br>');
    $('<span>', {text: `Contact: ${job_json['company']['company_contact_info']['email']}`}).appendTo(grid_right_div);

    $('<p>', {text: `${job_json['company']['company_info']['bio']}`}).appendTo(grid_div);

    return company_card_div
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}