window.addEventListener("beforeunload", () => { eel.close_python })

let mails;
let notes;
let map;

window.onload = function () {
    map = L.map('map').setView([12.8406, 80.1534], 13);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var stuSplit = L.latLng(12.8406, 80.1534);
    var myMarker = L.marker(stuSplit,
        { title: 'unselected' })
        .addTo(map);

    myModal = document.getElementById('mapModal');
    myModal.addEventListener('shown.bs.modal', event => {
        map.invalidateSize();
    });

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

function markAsRead(i) {
    eel.markAsRead(mails[i]['msgnumber']);
    mails.splice(i, 1);
    displayMail(mails);
}

function deleteMail(i) {
    eel.deleteMail(mails[i]['msgnumber']);
    mails.splice(i, 1);
    displayMail(mails);
}

function displayMail(mailsObject) {
    mails = mailsObject;
    console.log(mails);
    newMailsContainer = document.getElementById("newMailsContainer");
    newMailsContainer.classList.add('vstack');
    newMailsContainer.classList.remove('hstack');
    newMailsContainer.innerHTML = '';
    for (let i = 0; i < mailsObject.length; i++) {
        let mailObject = mailsObject[mailsObject.length - i - 1];

        if (mailObject['textOnly'] == true) {
            mailBody = `<p style='max-height:100%; overflow-y:scroll; text-align:left;'>${mailObject['minicontent'].replaceAll("\r\n", "<br>").replaceAll("\n", "<br>")}</p>`;
        } else {
            mailBody = `<iframe src="${mailObject["content"]}"  frameborder="0" class="embed-responsive-item" width="100%" height="100%"></iframe>`;
        }

        newMailsContainer.innerHTML += `
        <div class="row border border-black newMailBar border-2 align-items-center justify-content-between" id = "${i}MsgBar" onclick = 'mailBarClicked(${i});'>
            <div class="col-2 text-truncate" style='margin-top:8px;'>
                <p class="h5">${mailObject["from"]}</p>
            </div>
            <div class="col-8 text-truncate" style='text-align:left;'>
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
                <div style="display:flex; justify-content:space-between; width:100%;">
                    <div style="display:flex;column-gap:3px;">
                        <button class="btn btn-primary" style="margin-top: 5px;">
                            Set Reminder
                        </button>
                        <button class="btn btn-primary" style="margin-top: 5px;" onclick="openMap(${i});">
                            Maps
                        </button>
                        <button class="btn btn-primary" style="margin-top: 5px;">
                            Calendar
                        </button>
                        <button class="btn btn-primary" style="margin-top: 5px;" onclick="summarizeMail(${i});">
                            Summary
                        </button>
                    </div>
                    <div style="display:flex;column-gap:3px;">
                        <button class="btn btn-primary" style="margin-top: 5px;" onclick="saveMail(${i});">
                            Save
                        </button>
                        <button class="btn btn-primary" style="margin-top: 5px;" onclick="markAsRead(${i});">
                            Mark As Read
                        </button>
                        <button class="btn btn-danger" style="margin-top: 5px;" onclick="deleteMail(${i});">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
            <div class="card-footer text-body-secondary">
                ${mailObject["date"]}
            </div>
        </div>
        `
    }
}

function saveMail(mailIdx) {
    eel.saveMail(mails[mailIdx]);
}

function fetchSavedMail() {
    eel.fetchSavedMail()(displayMail);
}

function summarizeMail(emailIndex) {
    myModalElement = document.getElementById('summaryModal');
    modalTitle = document.getElementById('summaryModalTitle');
    modalContent = document.getElementById('summaryModalContent');
    myModal = new bootstrap.Modal(document.getElementById('summaryModal'));

    modalContent.innerHTML = `
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;

    myModal.show();

    textContent = mails[emailIndex]['minicontent'];
    eel.summarizeEmail(textContent)(function (summaryText) {
        modalTitle.innerHTML = mails[emailIndex]['subject'];
        modalContent.innerHTML = `<textarea class="form-control" style='height:40vh;' id='modaltextarea'>${summaryText}</textarea>`;
    });
}

function saveNote() {
    noteTitle = document.getElementById('summaryModalTitle').innerHTML;
    noteText = document.getElementById('modaltextarea').value;
    eel.saveNote(noteTitle, noteText);
}

function deleteNote(noteIndex) {
    noteTitle = notes[noteIndex]['title'];
    noteText = notes[noteIndex]['text'];
    eel.deleteNote(noteText, noteTitle)(fetchNotes);
}

function fetchNotes() {
    eel.fetchNotes()(function (notesArray) {
        notes = notesArray;
        notesContainer = document.getElementById("newMailsContainer");
        notesContainer.innerHTML = '';
        notesContainer.classList.remove('vstack');
        notesContainer.classList.add('hstack');

        for (let i = 0; i < notesArray.length; i++) {
            noteObject = notesArray[i];
            notesContainer.innerHTML += `
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">${noteObject['title']}</h5>
                    <p class="card-text">${noteObject['text']}</p>
                    <button class="btn btn-danger" onclick="deleteNote(${i});">
                        Delete
                    </button>
                </div>
            </div>
            `;
        }
    });
}

function openMap(emailIndex) {
    emailObject = mails[emailIndex];
    emailText = emailObject['minicontent'];

    mapModalTitle = document.getElementById('mapModalTitle');

    eel.getLocationLatLong(emailText)(function (coords) {
        mapModalElement = document.getElementById('mapModal');
        mapModal = new bootstrap.Modal(mapModalElement);
        mapModal.show();

        mapModalTitle.innerHTML = coords[2];

        map.flyTo([coords[0], coords[1]]);
        map.invalidateSize();
    });
}