import imaplib
import email
from base64 import b64decode
from time import sleep
import win11toast
import os
from dotenv import load_dotenv

load_dotenv()

imap_user = os.environ["IMAP_USER"]
imap_pass = os.environ["IMAP_PASS"]
imap_host = os.environ["IMAP_HOST"]

imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)
imap.select('Inbox')

SEEN = []

def main():
    global imap

    while True:
        (retcode, msgnums) = imap.search(None, "(UNSEEN)")
        print(msgnums)

        assert retcode == "OK"

        if msgnums == [b'']:
            print("No Mails found")
        
        else:
            foundNew = False
            for msgnum in msgnums[0].split():
                if msgnum not in SEEN:
                    foundNew = True
                    SEEN.append(msgnum)
            
            for seenMail in SEEN:
                if seenMail not in msgnums[0].split():
                    SEEN.remove(seenMail)

            if foundNew:
                buttons = [
                    "Dismiss", 
                    {'activationType': 'protocol', 'arguments': 'https://google.com', 'content': 'Open Google'}, 
                    "Desktop"
                ]
                retval = win11toast.toast("GenAIHackathon", 
                               "You have new unread mails in your inbox", 
                               buttons = buttons, 
                               icon = 'D:/Projects/GenAIHackathon/mail.avif')
                if (type(retval) == dict and retval['arguments'] != 'http:Dismiss'):
                    pass
                else:
                    print("User dismissed the notification")
            else:
                print("Already notified abt the mails")

        sleep(10)

try:
    main()
except:
    pass
finally:
    imap.close()