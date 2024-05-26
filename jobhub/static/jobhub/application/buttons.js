function setupCancelConfirmation(buttonClass, modalId, message) {
    console.log(message)
    var clickedButton = document.querySelector(buttonClass);
    var modal = document.getElementById(modalId);
    var modalText = document.getElementById("confirmModalText");
    var closeButton = modal.querySelector(".close-button-1");
    var cancelModalButton = modal.querySelector(".close-button-2");
    var confirmButton = modal.querySelector(".confirm-button");

    clickedButton.onclick = function() {
        modalText.textContent = message;
        modal.style.display = "block";
    }

    closeButton.onclick = function() {
        modal.style.display = "none";
    };

    if (confirmButton) {
        confirmButton.onclick = function() {
            document.querySelector('form').reset();
            modal.style.display = "none";
        };
    };

    if (cancelModalButton) {
        cancelModalButton.onclick = function() {
            modal.style.display = "none";
        };
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}
window.setupCancelConfirmation = setupCancelConfirmation

function openProfileModal(userId, applicationId, selected_id) {
    var iframe = document.getElementById("profileIframe");
    var modal = document.getElementById("profileModal");
    var closeButton = modal.querySelector(".close-button-1");
    var confirmButton = modal.querySelector(".confirm-button");
    
    iframe.src = `/other_user_profile/?applicant_id=${userId}`;
    modal.style.display = "block";

    closeButton.onclick = function() {
        modal.style.display = "none";
    };

    confirmButton.onclick = function() {
        changeApplicationStatus(applicationId, 'reviewed', selected_id);
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}
window.openProfileModal = openProfileModal;

function employerControls(buttonClass, modalId, message, newStatus) {
    var cancelButtons = document.querySelectorAll(buttonClass);
    var modal = document.getElementById(modalId);
    var modalText = document.getElementById("processModalText");
    var closeButton = modal.querySelector(".close-button-1");
    var cancelModalButton = modal.querySelector(".close-button-2");
    var confirmButton = modal.querySelector(".confirm-button");

    cancelButtons.forEach(function(btn) {
        btn.onclick = function(event) {
            modalText.textContent = message;
            modal.style.display = "block";
        };
    });

    confirmButton.onclick = function() {
        changeApplicationStatus(applicationId, newStatus);
        modal.style.display = "none";
    };

    closeButton.onclick = function() {
        modal.style.display = "none";
    };

    if (cancelModalButton) {
        cancelModalButton.onclick = function() {
            modal.style.display = "none";
        };
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}
