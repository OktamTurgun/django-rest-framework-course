class EmailService:
    """
    Email xabarlar yuborish servisi.
    Real loyihada SMTP yoki SendGrid / Amazon SES ishlatiladi.
    """

    def send_email(self, to, subject, message):
        if not to:
            raise ValueError("Recipient email required")

        # Fake sending
        return {
            "status": "sent",
            "to": to,
            "subject": subject
        }
