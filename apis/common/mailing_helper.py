from django.core.mail import EmailMessage


# Maling class.
class SendEmailClass():

    def __init__(self, email_subject, email_body, sender_email, receiver_email, reply_to: list):
        self.email_subject = email_subject
        self.email_body = email_body
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.reply_to = reply_to

    def account_verification_mail(self):
        msg = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.sender_email,
            to=[str(self.receiver_email)],
            reply_to=None
        )
        msg.send(fail_silently=True)
        return True

    def account_verification_status_mail(self):
        msg = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.sender_email,
            to=[str(self.receiver_email)],
            reply_to=None
        )
        msg.send(fail_silently=True)
        return True

    def transaction_mail(self):
        msg = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.sender_email,
            to=[str(self.receiver_email)],
            reply_to=None
        )
        msg.send(fail_silently=True)
        return True

    def password_reset_token_mail(self):
        msg = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.sender_email,
            to=[str(self.receiver_email)],
            reply_to=None
        )
        msg.send(fail_silently=True)
        return True

    def password_reset_complete_mail(self):
        msg = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.sender_email,
            to=[str(self.receiver_email)],
            reply_to=None
        )
        msg.send(fail_silently=True)
        return True
