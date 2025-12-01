class InventoryService:
    """
    Ombor (Inventory) servisi.
    Bu servis mahsulotlar sonini boshqarish uchun ishlatiladi.
    """

    def __init__(self):
        # Fake database
        self.stock = {
            "item_1": 20,
            "item_2": 50,
            "item_3": 0
        }

    def check_stock(self, item_id):
        return self.stock.get(item_id, 0)

    def reduce_stock(self, item_id, quantity):
        if self.stock.get(item_id, 0) < quantity:
            raise ValueError("Not enough stock")

        self.stock[item_id] -= quantity
        return {
            "status": "updated",
            "item_id": item_id,
            "remaining": self.stock[item_id]
        }
