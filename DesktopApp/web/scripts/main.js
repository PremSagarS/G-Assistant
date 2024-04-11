window.addEventListener("beforeunload", () => { eel.close_python })

let mails;

window.onload = function () {
    eel.load_prevmail()(display_mail);
}

function display_mail(mailsObject) {
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