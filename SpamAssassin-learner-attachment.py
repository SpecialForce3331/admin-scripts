#!/usr/bin/python
#
# Send spam letter as attachment to your special mailbox, when run this script, he will connect to mailbox, get all letters,
# get they attachments and learn it as spam
#
__author__ = 'sizov'
import imaplib
import email
import os
import time
import subprocess

imaplib.IMAP4.debug = imaplib.IMAP4_SSL.debug = 1

username, passwd = ('spam@test.ru', '123456')
SPAM_DIR = os.path.join(os.environ['HOME'] + '/spam/')

con = imaplib.IMAP4_SSL('mail.test.ru', 993)
con.login(username, passwd)
con.select()

typ, data = con.search(None, 'all')

for num in data[0].split():
    typ, data = con.fetch(num, '(RFC822)')
    text = data[0][1]
    msg = email.message_from_string(text)

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = 'spam' + str(time.time())
        data = part.get_payload(decode=True)
        if data:
            continue
        with open(SPAM_DIR + filename, 'w') as f:
            print(filename, 'was written')
            f.write(str(part))
    con.store(num, '+FLAGS', '(\\Deleted)')

con.expunge()
con.close()
subprocess.check_call(['/usr/bin/sa-learn', '--spam', SPAM_DIR])

for file in os.listdir(SPAM_DIR):
    os.remove(SPAM_DIR + file)
