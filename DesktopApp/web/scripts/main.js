window.addEventListener("beforeunload", () => { eel.close_python })

let mails;

window.onload = refresh;

function refresh() {
    document.getElementById("newMailsContainer").innerHTML = `
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;
    document.getElementById("buttonsContainer").innerHTML = `
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    `;
    eel.load_prevmail()(displayPrevMail);
    eel.loadNewMail()(displayNewMail);
}

function displayNewMail(mailsObject) {
    console.log(mailsObject);
    newMailsContainer = document.getElementById("newMailsContainer");
    newMailsContainer.innerHTML = '';
    for (let i = 0; i < mailsObject.length; i++) {
        let mailObject = mailsObject[i];
        newMailsContainer.innerHTML += `
        <div class="row border border-black newMailBar border-2 align-items-center">
            <div class="col-2 text-truncate" style='margin-top:8px;'>
                <p class="h5">${mailObject["from"]}</p>
            </div>
            <div class="col-10 text-truncate">
                <b> ${mailObject["subject"]} </b> - ${mailObject["content"]}
            </div>
        </div>
        `
    }
}

function displayPrevMail(mailsObject) {
    mails = mailsObject;
    buttonsContainer = document.getElementById("buttonsContainer");
    buttonsContainer.innerHTML = '';
    for (let i = 0; i < mailsObject.length; i++) {
        let mailObject = mailsObject[i];
        buttonsContainer.innerHTML += `
        <button class='btn btn-primary text-truncate' style='margin-bottom:5px;'>
            ${mailObject['subject']}
        </button>
        `
    }
}