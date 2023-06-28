import imaplib
import smtplib
from dotenv import dotenv_values

vals = dotenv_values(".env")
sender_email = "nesi@transgender.army"

# imap = imaplib.IMAP4("box.courvix.com", 993)
# imap.login(sender_email, vals["PASSWORD"])


def send_email(receiver, subject, message):
    with smtplib.SMTP("box.courvix.com", 587) as server:
        server.starttls()
        server.login(sender_email, vals["PASSWORD"])
        server.sendmail(sender_email, receiver, f"Subject: {subject}\nFrom: {sender_email}\nTo: {receiver}\n\n{message}\n\nSent through monkey bot https://discord.gg/p9R9vzJ97m")
        print("sent")


def inbox():
    imap.select("INBOX")

    status, email_ids = imap.search(None, "ALL")
    email_id_list = email_ids[0].split()

    for email_id in email_id_list:
        status, email_data = imap.fetch(email_id, '(RFC822)')
        email_content = email_data[0][1].decode('utf-8')
        print(f'Email ID: {email_id}\n{email_content}')
