function getList(id, status) {
    if (!status) {status = 'all'};
    let endpoint = `/employer_application/get-applicant/${id}/${status}`;
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return;
        updatePage(xhr, id, status);
    }
    xhr.open("GET", endpoint, true);
    xhr.send();
}

function changeApplicationStatus(applicationId, status, selected_id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            getList(selected_id, status);
            window.location.href=`/employer_application/${selected_id}/${status}`
        }
    };
    xhr.open("POST", "/update_application_status/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ applicationId: applicationId, status: status, selected_id: selected_id }));
}
window.changeApplicationStatus = changeApplicationStatus

function updatePage(xhr, id, status) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        updateList(response, id, status);
        return;
    }
    if (xhr.status === 0) {
        displayError("Cannot connect to server");
        return;
    }
    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`);
        return;
    }
    let response = JSON.parse(xhr.responseText);
    if (response.hasOwnProperty('error')) {
        displayError(response.error);
        return;
    }
    displayError(response);
}

function updateList (items, id, status) {
    if (items.jobs.length === 0) {
        const job_item = document.createElement('div');
        job_item.innerHTML = `<div class="card-container job-card"><div class="card"><p>No job to display.</p></div></div>`;
        jobList.append(job_item);
    }else {
        if (!id){ id = items.jobs.last().job_id; };
        let jobList = document.getElementById("all-jobs");
        while (jobList.hasChildNodes()) {jobList.firstChild.remove()};
        let applicantList = document.getElementById("all-applicants");
        while (applicantList.hasChildNodes()) {applicantList.firstChild.remove()};
        items.jobs.forEach(job => {
            jobList.append(makeJobItem(job, id, status));
            items.applicants.filter(applicant => applicant.job_id == job.job_id).forEach(applicant => {
                applicantList.append(makeApplicantCard(applicant, job))
            });
        });
        let trackingBoard = document.getElementById("tracking-board");
        while (trackingBoard.hasChildNodes()) {trackingBoard.firstChild.remove()};
        items.counts.forEach(count => trackingBoard.append(makeTrackingBoard(count)));
    }
}

function makeJobItem(item, id, status) {
    let url = `/employer_application/${ item.job_id }/${ status }`;
    const job_item = document.createElement('div');
    job_item.innerHTML = `
    <a href="${ url }" class="email-item job-item pure-g">
        <div class="pure-u-3-4">
            <h5 class="email-name">Role Id: ${ item.job_id }</h5>
            <h4 class="email-subject">${ item.job_name }</h4>
            <p class="email-desc">Posted: ${ convertIsoToLocalDateTime(item.post_time) }</p>
        </div>
    </a>`;
    if (item.job_id === parseInt(id)) { job_item.classList.add("selected-job") };
    return job_item;
}

function makeApplicantCard(applicant, job) {
    const applicant_card = document.createElement('div');
    applicant_card.innerHTML = `
    <div class="card-container job-card">
        <div class="card">
            <div class="card-header pure-g">
                <div class="pure-u-1-2">
                <a class="card-header profile-url">${applicant.name}</a>
                </div>
                <div class="applied-date pure-u-1-2">
                    <h2>${ convertIsoToLocalDateTime(applicant.submit_date) }</h2>
                </div>
            </div>
            <hr>
            <div class="applicant-control">
                <a href="mailto:${ applicant.email }?subject=Interview Invitation&body=Dear ${ applicant.name },%0D%0A%0D%0AWe would like to invite you for an interview for the ${ job.job_name } position. Please let us know your available times.%0D%0A%0D%0ASincerely,%0D%0A${ job.company_name }">
                    <button class="schedule-btn">Interview</button>
                </a>
                <a href="mailto:${ applicant.email }?subject=Job Offer&body=Dear ${ applicant.name },%0D%0A%0D%0AWe are pleased to offer you the ${ job.job_name } position. Please find attached the job offer details.%0D%0A%0D%0ASincerely,%0D%0A${ job.company_name }">
                    <button class="hire-btn">Hire</button>
                </a>
                <a href="mailto:${ applicant.email }?subject=Application Status Update&body=Dear ${ applicant.name },%0D%0A%0D%0AThank you for your interest in the ${ job.job_name } position. After careful consideration, we regret to inform you that we have decided to move forward with other candidates at this time.%0D%0A%0D%0AWe appreciate the effort you put into your application and wish you all the best in your future endeavors.%0D%0A%0D%0ASincerely,%0D%0A${ job.company_name }">
                    <button class="reject-btn">Reject</button>
                </a>
            </div>
        </div>
    </div>`;
    const profileLink = applicant_card.querySelector('.profile-url');
    profileLink.addEventListener('click', function() {
        window.openProfileModal(applicant.applicant_id, applicant.application_id, id);
    });
    applicant_card.querySelector('.schedule-btn').addEventListener('click', function() {
        changeApplicationStatus(applicant.application_id, 'interviewed', id);
    });
    applicant_card.querySelector('.hire-btn').addEventListener('click', function() {
        changeApplicationStatus(applicant.application_id, 'hired', id);
    });
    applicant_card.querySelector('.reject-btn').addEventListener('click', function() {
        changeApplicationStatus(applicant.application_id, 'rejected', id);
    });
    return applicant_card;
}

function makeTrackingBoard(item) {
    const tracking_board = document.createElement('div');
    tracking_board.innerHTML =
    `<div class="card-container">
        <div class="card">
            <div class="card-header">Applications Tracking</div>
            <div class="card-item">Applied<span>${ item.applied }</span></div>
            <div class="card-item">Reviewed<span>${ item.reviewed }</span></div>
            <div class="card-item">Interviewed<span>${ item.interviewed }</span></div>
            <div class="card-item">Hired<span>${ item.hired }</span></div>
            <div class="card-item">Rejected<span>${ item.rejected }</span></div>
        </div>
    </div> `;
    return tracking_board;
}

function convertIsoToLocalDateTime(isoStr) {
    let dateObj = new Date(isoStr);
    let month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
    let day = dateObj.getDate().toString().padStart(2, '0');
    let year = dateObj.getFullYear();
    let hours = dateObj.getHours();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    let minutes = dateObj.getMinutes().toString().padStart(2, '0');
    return `${month}/${day}/${year} ${hours}:${minutes} ${ampm}`;
}

function deleteItem(id) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updatePage(xhr)
    }

    xhr.open("POST", deleteItemURL(id), true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`csrfmiddlewaretoken=${getCSRFToken()}`)
}
