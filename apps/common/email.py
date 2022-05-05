from django.core.mail import send_mail



class EmailNotification:
    def __init__(self, subject, message, sender_email, receiver_email):
        self.subject = subject
        self.message = message
        self.sender_email = sender_email
        self.receiver_email = receiver_email

    def registeration_email(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently= True
        )

    def transaction_email(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.sender_email,
            recipient_list=[str(self.receiver_email)],
            fail_silently=True
        )