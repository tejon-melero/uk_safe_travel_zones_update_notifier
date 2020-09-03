import smtplib

from constant import (GMAIL_SMTP_SENDER_ACCOUNT_PASSWORD,
                      GMAIL_SMTP_SENDER_ACCOUNT_USERNAME,
                      GMAIL_SMTP_SESSION_HOST, GMAIL_SMTP_SESSION_PORT,
                      NOTIFICATION_EMAIL_RECIPIENT, NOTIFICATION_EMAIL_SUBJECT)


def gmail_notification(message):
    sender_address = GMAIL_SMTP_SENDER_ACCOUNT_USERNAME
    sender_pass = GMAIL_SMTP_SENDER_ACCOUNT_PASSWORD
    receiver_address = NOTIFICATION_EMAIL_RECIPIENT

    # message.attach(MIMEText(message, 'plain'))
    session = smtplib.SMTP(GMAIL_SMTP_SESSION_HOST, GMAIL_SMTP_SESSION_PORT)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password

    message = 'Subject: {}\n\n{}'.format(NOTIFICATION_EMAIL_SUBJECT, message)
    session.sendmail(sender_address, receiver_address, message)
    session.quit()
