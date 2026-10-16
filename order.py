
class Order:
    def __init__(self, customer, item, fabric, style, price):
        self.customer = customer
        self.item = item
        self.fabric = fabric
        self.style = style
        self.price = price

    def to_dict(self):
        return {
            "customer": self.customer.to_dict(),
            "item": self.item,
            "fabric": self.fabric,
            "style": self.style,
            "price": self.price
        }
