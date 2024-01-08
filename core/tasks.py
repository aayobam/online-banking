from celery import shared_task
from apps.common import mail_helper


@shared_task
def send_contact_mail_task(subject, message, sender_email, receiver_email, reply_to):
    contact_us = mail_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=reply_to
    )
    try:
        contact_us.contact_us_mail()
    except Exception as e:
        print('{0}: Could not send contact mail'.format(e))
    return "Contact mail sent successfully"


@shared_task
def send_order_booking_email_task(subject, message, receiver_email, from_email, reply_to):
    order_booking = mail_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        sender_email=from_email,
        receiver_email=receiver_email,
        reply_to=reply_to
    )
    try:
        order_booking.order_booking_mail()
    except Exception as e:
        print('{0}: Could not send order booking mail'.format(e))
    return "Online booking mail sent successfully."


@shared_task
def send_password_reset_task(subject, message, sender_email, receiver_email):
    password_reset = mail_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email
    )
    try:
        password_reset.password_reset_mail()
    except Exception as e:
        print("{0}: Could not send mail.".format(e))
    return "Password reset email sent."


@shared_task
def send_export_mail_task(subject, message, sender_email, receiver_email):
    send_export_mail = mail_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=None
    )
    try:
        send_export_mail.export_mail()
    except Exception as e:
        print("{0}: Could not send mail.".format(e))
    return "Export email sent."


@shared_task
def send_import_mail_task(subject, message, sender_email, receiver_email):
    send_export_mail = mail_helper.SendEmailClass(
        email_subject=subject,
        email_body=message,
        receiver_email=receiver_email,
        sender_email=sender_email,
        reply_to=None
    )
    try:
        send_export_mail.import_mail()
    except Exception as e:
        print("{0}: Could not send mail.".format(e))
    return "Export email sent."

