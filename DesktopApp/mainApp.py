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
from bs4 import BeautifulSoup

load_dotenv()

imap_user = os.environ["IMAP_USER"]
imap_pass = os.environ["IMAP_PASS"]
imap_host = os.environ["IMAP_HOST"]

imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

@eel.expose
def load_prevmail():
    imap.select('Inbox', readonly=True)

    (retcode, msgnums) = imap.search(None, "(SEEN)")
    assert retcode == "OK"

    mails = []
    for msg in  msgnums[0].split():
        mail = {}

        _, data = imap.fetch(msg, "(RFC822)")
        message = email.parser.BytesParser().parsebytes(data[0][1])

        mail["msgnumber"] = msg
        mail["from"] = message.get("From")
        mail["to"] = message.get("To")
        mail["date"] = message.get("Date")

        mimeSubject = message.get("Subject")
        decodedSubject = email.header.decode_header(mimeSubject)
        mail["subject"] = str(email.header.make_header(decodedSubject))
        
        mail["content"] = ""
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                mail["content"] += part.as_string()
        
        mails.append(mail)
    
    imap.unselect()

    return mails

@eel.expose
def SearchMail(searchString):
    imap.select('Inbox', readonly=True)

    (retcode, msgnums) = imap.search(None, "(TEXT %s)" % searchString)
    assert retcode == "OK"

    mails = []
    for msg in  msgnums[0].split():
        mail = {}

        _, data = imap.fetch(msg, "(RFC822)")
        message = email.parser.BytesParser().parsebytes(data[0][1])

        mail["msgnumber"] = msg
        mail["from"] = message.get("From")
        mail["to"] = message.get("To")
        mail["date"] = message.get("Date")

        mimeSubject = message.get("Subject")
        decodedSubject = email.header.decode_header(mimeSubject)
        mail["subject"] = str(email.header.make_header(decodedSubject))
        
        mail["minicontent"] = ""
        mail["content"] = ""

        for part in message.walk():
            if part.get_content_type() == "text/plain":
                mail["minicontent"] += part.get_payload(decode=True).decode()
            elif part.get_content_type() == "text/html":
                if not pathlib.Path('./web/userData').exists(): pathlib.Path('./web/userData').mkdir(parents=True)
                with open(f'./web/userData/{msg.decode()}-mail.html', 'w', encoding='utf-8') as file:
                    file.write(part.get_payload(decode=True).decode())
                mail["content"] = f'./userData/{msg.decode()}-mail.html'
                
        
        if mail['content'] == '':
            mail['textOnly'] = True
        
        mails.append(mail)
    
    imap.unselect()

    return mails

@eel.expose
def loadNewMail():
    imap.select('Inbox', readonly=True)

    (retcode, msgnums) = imap.search(None, "(UNSEEN)")
    assert retcode == "OK"

    mails = []
    for msg in  msgnums[0].split():
        mail = {}

        _, data = imap.fetch(msg, "(RFC822)")
        message = email.parser.BytesParser().parsebytes(data[0][1])

        mail["msgnumber"] = msg
        mail["from"] = message.get("From")
        mail["to"] = message.get("To")
        mail["date"] = message.get("Date")

        mimeSubject = message.get("Subject")
        decodedSubject = email.header.decode_header(mimeSubject)
        mail["subject"] = str(email.header.make_header(decodedSubject))
        
        mail["minicontent"] = ""
        mail["content"] = ""

        for part in message.walk():
            if part.get_content_type() == "text/plain":
                mail["minicontent"] += part.get_payload(decode=True).decode()
            elif part.get_content_type() == "text/html":
                if not pathlib.Path('./web/userData').exists(): pathlib.Path('./web/userData').mkdir(parents=True)
                with open(f'./web/userData/{msg.decode()}-mail.html', 'w', encoding='utf-8') as file:
                    file.write(part.get_payload(decode=True).decode())
                mail["content"] = f'./userData/{msg.decode()}-mail.html'
                
        
        if mail['content'] == '':
            mail['textOnly'] = True
        
        mails.append(mail)
    
    imap.unselect()

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