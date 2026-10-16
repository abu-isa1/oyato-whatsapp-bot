
class Customer:
    def __init__(self, name, phone, measurements):
        self.name = name
        self.phone = phone
        self.measurements = measurements

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "measurements": self.measurements
        }
