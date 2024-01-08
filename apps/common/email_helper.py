from django.core.mail import send_mail


class EmailNotification:
    def __init__(self, subject, message, sender_email, receiver_email):
        self.subject = subject
        self.message = message
        self.sender_email = sender_email
        self.receiver_email = receiver_email

    def account_registration_email_notification(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently=True,
        )
        return True

    def account_verification_email_notification(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently=True,
        )
        return True

    def funds_deposit_email_notification(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently=True,
        )
        return True

    def funds_withdrawal_email_notification(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently=True,
        )
        return True

    def sender_funds_transfer_email_notification(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently=True,
        )
        return True

    def recipient_funds_transfer_email_notification(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently=True,
        )
        return True
