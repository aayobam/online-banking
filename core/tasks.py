from celery import shared_task
from apis.common import mailing_helper


@shared_task
def send_verification_otp_mail_task(subject, message, sender_email, receiver_email, reply_to):
    contact_us = mailing_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=reply_to
    )
    try:
        contact_us.account_verification_mail()
    except Exception as e:
        print('{0}: Could not send account activation otp.'.format(e))
    return "Mail activation otp sent successfully."


@shared_task
def send_verification_status_mail_task(subject, message, sender_email, receiver_email, reply_to):
    contact_us = mailing_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=reply_to
    )
    try:
        contact_us.account_verification_mail()
    except Exception as e:
        print('{0}: Could not send account verification status mail.'.format(e))
    return "Mail verification status sent."


@shared_task
def send_transaction_mail_task(subject, message, sender_email, receiver_email, reply_to):
    send_export_mail = mailing_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=reply_to
    )
    try:
        send_export_mail.transaction_mail()
    except Exception as e:
        print('{0}: Could not send account verification status mail.'.format(e))
    return "Account verification status mail sent."


@shared_task
def send_password_reset_token_task(subject, message, sender_email, receiver_email, reply_to):
    password_reset = mailing_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=reply_to
    )
    try:
        password_reset.password_reset_token_mail()
    except Exception as e:
        print("{0}: Could not send password reset otp mail.".format(e))
    return "Password reset otp email sent."


@shared_task
def send_password_reset_complete_task(subject, message, sender_email, receiver_email, reply_to):
    password_reset = mailing_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=reply_to
    )
    try:
        password_reset.password_reset_complete_mail()
    except Exception as e:
        print("{0}: Could not send password reset complete mail.".format(e))
    return "Password reset complete mail sent."
