function getList(status) {
    let endpoint = `/applicant_application/get-application/${status}`;
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(xhr)
    }

    xhr.open("GET", endpoint, true)
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response)
        return
    }

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateList (items) {
    console.log(items.applications)
    let list1 = document.getElementById("all-applications")
    while (list1.hasChildNodes()) {
        list1.firstChild.remove()
    }

    let list2 = document.getElementById("tracking-board")
    while (list2.hasChildNodes()) {
        list2.firstChild.remove()
    }
    if (items.applications.length === 0) {
        let details = `<p>No application to display.</p>`;
        const application_card = document.createElement('div')
        application_card.setAttribute('class', 'card-container job-card pure-g')
        application_card.innerHTML =  `${ details }`;
        list1.append(application_card)
    } else {
        items.applications.forEach(application => list1.append(makeApplicationCard(application)))
    }
    const counts = {
        'all': items.counts.all,
        'reviewed': items.counts.reviewed,
        'interviewed': items.counts.interviewed,
        'hired': items.counts.hired,
        'rejected': items.counts.rejected
    }
    list2.append(makeTrackingBoard(counts))
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

function makeApplicationCard(item) {
    const application_card = document.createElement('div')
    application_card.setAttribute('class', 'card-container job-card pure-g')
    let details = `
    <div class="card pure-u-1">
        <div class="card-header pure-g">
            <div class="pure-u-1-2">
                <h1 class="card-header">${ item.job }</h1>
                <h2 class="card-header">${ item.company }</h2>
            </div>
            <div class="application-control pure-u-1-2">
                <a href="/joblist/?id=${item.job_id}">
                    <button class="withdraw-btn">Withdraw application</button>
                </a>
                <a href="mailto:contact@example.com?subject=Inquiry from Job Applicant">
                    <button class="contact-btn">Contact ${ item.company }</button>
                </a>
            </div>
        </div>
        <hr>
        <div class="sections pure-g">
            <div class="section pure-1-3">
                <h3>Application status</h3>
                <p>Applied: ${ convertIsoToLocalDateTime(item.submitdate) }</p>
                <p>Status: ${ item.status }</p>
            </div>
            <div class="section pure-1-3">
                <h3>About the role</h3>
                <p>Application deadline: ${ convertIsoToLocalDateTime(item.due_time) }</p>
                <p>Posted date: ${ convertIsoToLocalDateTime(item.post_time) }</p>
                <p>Estimated pay: ${ item.lower_pay } - ${ item.upper_pay } per year</p>
                <a href="/joblist/?id=${item.job_id}">view full description</a>
            </div>
            <div class="section pure-1-3">
                <h3>About the company</h3>
                <p>Employees: ${ item.company_size }</p>
                <p>Industry: ${ item.company_industry }</p>
                <p>Bio: ${ item.company_bio }</p>
                <a href="/other_company_profile/?company_id=${item.company_id}">view full description</a>
            </div>
        </div>
    </div>
    `;
    application_card.innerHTML = `${ details }`;
    return application_card
}

function makeTrackingBoard(item) {
    const tracking_board = document.createElement('div')
    tracking_board.setAttribute('class', 'card-container')
    let details = `
    <div class="card">
        <div class="card-header">Applications Tracking</div>
        <div class="card-item">Applied<span>${ item.all }</span></div>
        <div class="card-item">Reviewed<span>${ item.reviewed }</span></div>
        <div class="card-item">Interviewed<span>${ item.interviewed }</span></div>
        <div class="card-item">Hired<span>${ item.hired }</span></div>
        <div class="card-item">Rejected<span>${ item.rejected }</span></div>
    </div>
    `;
    tracking_board.innerHTML = `${ details }`
    return tracking_board
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
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
