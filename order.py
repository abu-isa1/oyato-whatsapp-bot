

class Order:
    def __init__(
        self,
        customer,
        item,
        fabric,
        style,
        price,
        order_id="OYA-0001",
        status="Pending"
    ):
        self.customer = customer
        self.item = item
        self.fabric = fabric
        self.style = style
        self.price = price
        self.order_id = order_id
        self.status = status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer": self.customer.to_dict(),
            "item": self.item,
            "fabric": self.fabric,
            "style": self.style,
            "price": self.price,
            "status": self.status
        }
