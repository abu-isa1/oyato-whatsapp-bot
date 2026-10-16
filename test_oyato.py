
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from customer import Customer
from order import Order
import main


class TestOyato(unittest.TestCase):

    def test_customer_details(self):
        customer = Customer(
            "Amina",
            "08012345678",
            "Chest: 38, Length: 56"
        )

        self.assertEqual(customer.name, "Amina")
        self.assertEqual(customer.phone, "08012345678")

    def test_customer_to_dict(self):
        customer = Customer("Amina", "08012345678", "Chest: 38")

        self.assertEqual(
            customer.to_dict(),
            {
                "name": "Amina",
                "phone": "08012345678",
                "measurements": "Chest: 38"
            }
        )

    def test_order_to_dict(self):
        customer = Customer("Amina", "08012345678", "Chest: 38")
        order = Order(customer, "Agbada", "Cotton", "Classic", 25000)

        data = order.to_dict()

        self.assertEqual(data["item"], "Agbada")
        self.assertEqual(data["fabric"], "Cotton")
        self.assertEqual(data["price"], 25000)
        self.assertEqual(data["customer"]["name"], "Amina")

    def test_save_order(self):
        customer = Customer("Amina", "08012345678", "Chest: 38")
        order = Order(customer, "Agbada", "Cotton", "Classic", 25000)

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "orders.json"

            with patch.object(main, "ORDERS_FILE", test_file):
                main.save_order(order)

            with test_file.open("r", encoding="utf-8") as file:
                saved_orders = json.load(file)

        self.assertEqual(len(saved_orders), 1)
        self.assertEqual(saved_orders[0]["item"], "Agbada")

    
    def test_order_has_id_and_status(self):
        customer = Customer(
            "Amina",
            "08012345678",
            "Chest: 38"
        )

        order = Order(
            customer,
            "Agbada",
            "Cotton",
            "Classic",
            25000,
            order_id="OYA-0007"
        )

        data = order.to_dict()

        self.assertEqual(data["order_id"], "OYA-0007")
        self.assertEqual(data["status"], "Pending")

    
    def test_update_order_status(self):
        customer = Customer(
            "Amina",
            "08012345678",
            "Chest: 38"
        )
        order = Order(
            customer,
            "Agbada",
            "Cotton",
            "Classic",
            25000,
            order_id="OYA-0001"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "orders.json"

            with test_file.open("w", encoding="utf-8") as file:
                json.dump([order.to_dict()], file)

            with patch.object(main, "ORDERS_FILE", test_file):
                with patch(
                    "builtins.input",
                    side_effect=["OYA-0001", "2"]
                ):
                    main.update_order_status()

            with test_file.open("r", encoding="utf-8") as file:
                saved_orders = json.load(file)

        self.assertEqual(
            saved_orders[0]["status"],
            "In Progress"
        )
    
    def test_generate_first_order_id(self):
        self.assertEqual(main.generate_order_id([]), "OYA-0001")

    def test_generate_next_order_id(self):
        orders = [
            {"order_id": "OYA-0001"},
            {"order_id": "OYA-0002"},
            {"order_id": "OYA-0005"}
        ]

        self.assertEqual(
            main.generate_order_id(orders),
            "OYA-0006"
        )


    




if __name__ == "__main__":
    unittest.main()
