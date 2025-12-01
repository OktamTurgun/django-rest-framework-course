class PaymentGateway:
    """
    Mock Payment Gateway service.
    Real loyihada bu external API (Payme, Click, Stripe) bilan integratsiya bo‘ladi.
    """

    def process_payment(self, amount, card_number, expire_date):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero")

        # Fake processing
        return {
            "status": "success",
            "transaction_id": "TXN123456",
            "amount": amount
        }
