window.addEventListener("beforeunload", () => { eel.close_python })

let mails;

window.onload = function () {
    refresh();
};

function SearchMail() {
    document.getElementById("newMailsContainer").innerHTML = `
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;
    let searchString = document.getElementById("MailSearchTextBox").value;
    eel.SearchMail(searchString)(displayMail);

    return false;
}

function refresh() {
    document.getElementById("newMailsContainer").innerHTML = `
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;
    eel.loadNewMail()(displayMail);
}

function fetchPreviousMail() {
    document.getElementById("newMailsContainer").innerHTML = `
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;
    eel.load_prevmail()(displayMail);
}

function mailBarClicked(i) {
    let card = document.getElementById(i + "MsgContentCard");
    displayToggle(card);
}

function displayToggle(element) {
    if (element.style.display == 'none') {
        element.style.display = '';
    } else {
        element.style.display = 'none';
    }
}

function displayMail(mailsObject) {
    console.log(mailsObject);
    newMailsContainer = document.getElementById("newMailsContainer");
    newMailsContainer.innerHTML = '';
    for (let i = 0; i < mailsObject.length; i++) {
        let mailObject = mailsObject[i];

        if (mailObject['textOnly'] == true) {
            mailBody = `<p style='max-height:100%; overflow-y:scroll; text-align:left;'>${mailObject['minicontent'].replaceAll("\r\n", "<br>").replaceAll("\n", "<br>")}</p>`;
        } else {
            mailBody = `<iframe src="${mailObject["content"]}"  frameborder="0" class="embed-responsive-item" width="100%" height="100%"></iframe>`;
        }

        newMailsContainer.innerHTML += `
        <div class="row border border-black newMailBar border-2 align-items-center" id = "${i}MsgBar" onclick = 'mailBarClicked(${i});'>
            <div class="col-2 text-truncate" style='margin-top:8px;'>
                <p class="h5">${mailObject["from"]}</p>
            </div>
            <div class="col-10 text-truncate" style='text-align:left;'>
                <b> ${mailObject["subject"]} </b> - ${mailObject["minicontent"]}
            </div>
        </div>
        <div class="card text-center" style="display: none;" id = "${i}MsgContentCard">
            <div class="card-header">
                ${mailObject["from"]}
            </div>
            <div class="card-body">
                <h5 class="card-title">${mailObject["subject"]}</h5>
                <div class="embed-responsive" style="height:50vh;">${mailBody}</div>
                <button class="btn btn-primary" style="margin-top:3px;">Summary</button>
            </div>
            <div class="card-footer text-body-secondary">
                ${mailObject["date"]}
            </div>
        </div>
        `
    }
}