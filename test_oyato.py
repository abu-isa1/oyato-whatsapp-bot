

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
from customer import Customer
from order import Order


class TestOyatoDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db = Path(self.temp_dir.name) / "test_oyato.db"

        self.db_patch = patch.object(database, "DB_FILE", self.test_db)
        self.db_patch.start()

        database.initialize_database()

    def tearDown(self):
        self.db_patch.stop()
        self.temp_dir.cleanup()

    def make_order(self, order_id="OYA-0001"):
        customer = Customer(
            "Amina",
            "08012345678",
            "Chest: 38"
        )

        return Order(
            customer,
            "Agbada",
            "Cotton",
            "Classic",
            25000,
            order_id=order_id
        )

    def test_database_initializes(self):
        self.assertTrue(self.test_db.exists())

    def test_save_and_get_order(self):
        database.save_order(self.make_order())

        orders = database.get_all_orders()

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["item"], "Agbada")
        self.assertEqual(orders[0]["customer_name"], "Amina")

    def test_generate_order_ids(self):
        self.assertEqual(
            database.generate_order_id(),
            "OYA-0001"
        )

        database.save_order(self.make_order("OYA-0001"))

        self.assertEqual(
            database.generate_order_id(),
            "OYA-0002"
        )

    def test_update_order_status(self):
        database.save_order(self.make_order())

        result = database.update_status(
            "OYA-0001",
            "In Progress"
        )

        self.assertTrue(result)
        self.assertEqual(
            database.get_all_orders()[0]["status"],
            "In Progress"
        )

    def test_missing_order_returns_false(self):
        result = database.update_status(
            "OYA-9999",
            "Completed"
        )

        self.assertFalse(result)

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            database.update_status(
                "OYA-0001",
                "Unknown"
            )


if __name__ == "__main__":
    unittest.main()
