import eel
import os
import pathlib
import datetime
import sys
from dotenv import load_dotenv
import replicate
import imaplib
import email
import email.parser
import email.header

load_dotenv()

imap_user = os.environ["IMAP_USER"]
imap_pass = os.environ["IMAP_PASS"]
imap_host = os.environ["IMAP_HOST"]

imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)
imap.select('Inbox')

os.chdir(os.path.dirname(os.path.realpath(__file__)))

@eel.expose
def load_prevmail():
    (retcode, msgnums) = imap.search(None, "(SEEN)")
    assert retcode == "OK"

    mails = []
    for msg in  msgnums[0].split():
        mail = {}

        _, data = imap.fetch(msg, "(RFC822)")
        message = email.parser.BytesParser().parsebytes(data[0][1])

        mail["msgnumber"] = msg
        mail["from"] = message.get("From")
        mail["date"] = message.get("To")

        mimeSubject = message.get("Subject")
        decodedSubject = email.header.decode_header(mimeSubject)
        mail["subject"] = str(email.header.make_header(decodedSubject))
        
        mail["content"] = ""
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                mail["content"] += part.as_string()
        
        mails.append(mail)
    
    return mails

@eel.expose
def close_python(page, sockets_still_open):
    sys.exit(0)

@eel.expose
def testPrompt():
    output = replicate.run("replicate/llama-7b:ac808388e2e9d8ed35a5bf2eaa7d83f0ad53f9e3df31a42e4eb0a0c3249b3165",
                       input = {
                           "debug": False,
                           "top_p": 0.95,
                           "prompt": "Simply put, the theory of relativity states that",
                           "max_length": 500,
                           "temperature": 0.8,
                           "repetition_penalty": 1,
                           "max_length": 400
                       })

    outString = ""

    for item in output:
        outString += item
    
    outString = outString.capitalize()
    
    return outString

eel.init('web')
eel.start('main.html')