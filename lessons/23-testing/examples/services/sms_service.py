class SMSService:
    """
    SMS yuborish servisi.
    Real loyihada Eskiz API, Twilio yoki boshqa SMS provider bilan ishlaydi.
    """

    def send_sms(self, phone, message):
        if not phone:
            raise ValueError("Phone number is required")

        return {
            "status": "sent",
            "phone": phone,
            "message": message
        }
