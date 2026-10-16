

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
import main
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
    
    def test_track_order_found(self):
        database.save_order(self.make_order())

        with patch("builtins.input", return_value="OYA-0001"):
            with patch("builtins.print") as mock_print:
                main.track_order()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("OYA-0001", printed_text)
        self.assertIn("Pending", printed_text)
    

    
    def test_track_order_not_found(self):
        with patch("builtins.input", return_value="OYA-9999"):
            with patch("builtins.print") as mock_print:
                main.track_order()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Order not found", printed_text)
    
    
    def test_track_order_after_status_update(self):
        database.save_order(self.make_order())
        database.update_status("OYA-0001", "Completed")

        with patch("builtins.input", return_value="OYA-0001"):
            with patch("builtins.print") as mock_print:
                main.track_order()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Completed", printed_text)
        self.assertIn("Your clothing is ready!", printed_text)

    
    def test_search_orders_by_phone(self):
        database.save_order(self.make_order("OYA-0001"))

        results = database.search_orders_by_phone("08012345678")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["order_id"], "OYA-0001")
        self.assertEqual(results[0]["phone"], "08012345678")

    def test_search_orders_by_phone_not_found(self):
        results = database.search_orders_by_phone("08099999999")

        self.assertEqual(results, [])
    
    
    def test_search_orders_by_phone_displays_order(self):
        database.save_order(self.make_order())

        with patch("builtins.input", return_value="08012345678"):
            with patch("builtins.print") as mock_print:
                main.search_orders_by_phone()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("OYA-0001", printed_text)
        self.assertIn("Agbada", printed_text)
        self.assertIn("Pending", printed_text)

    def test_search_orders_by_phone_displays_not_found(self):
        with patch("builtins.input", return_value="08099999999"):
            with patch("builtins.print") as mock_print:
                main.search_orders_by_phone()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("No orders found", printed_text)

    def test_search_orders_by_phone_rejects_empty_input(self):
        with patch("builtins.input", return_value=""):
            with patch("builtins.print") as mock_print:
                main.search_orders_by_phone()

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Please enter a phone number", printed_text)

    
    def test_search_orders_by_phone_finds_multiple_orders(self):
        database.save_order(self.make_order("OYA-0001"))

        customer = Customer("Amina", "08012345678", "Chest: 38")
        second_order = Order(
            customer,
            "Buba",
            "Linen",
            "Modern",
            15000,
            order_id="OYA-0002"
        )
        database.save_order(second_order)

        results = database.search_orders_by_phone("08012345678")

        self.assertEqual(len(results), 2)
        self.assertEqual(
            [order["order_id"] for order in results],
            ["OYA-0001", "OYA-0002"]
        )

    
    def test_get_phone_number_accepts_international_number(self):
        with patch(
            "builtins.input",
            return_value="+1 (202) 555-0123"
        ):
            result = main.get_phone_number()

        self.assertEqual(result, "+1 (202) 555-0123")

    def test_get_phone_number_rejects_too_few_digits(self):
        with patch(
            "builtins.input",
            side_effect=["12345", "08012345678"]
        ):
            with patch("builtins.print") as mock_print:
                result = main.get_phone_number()

        self.assertEqual(result, "08012345678")
        mock_print.assert_called_once_with(
            "Enter a valid phone number."
        )

    def test_get_phone_number_rejects_letters(self):
        with patch(
            "builtins.input",
            side_effect=["abc1234567", "08012345678"]
        ):
            with patch("builtins.print") as mock_print:
                result = main.get_phone_number()

        self.assertEqual(result, "08012345678")
        mock_print.assert_called_once_with(
            "Enter a valid phone number."
        )

    
    def test_get_price_accepts_valid_price(self):
        with patch(
            "builtins.input",
            return_value="25000"
        ):
            result = main.get_price()

        self.assertEqual(result, 25000)

    
    def test_get_price_rejects_negative_price(self):
        with patch(
            "builtins.input",
            side_effect=["-500", "25000"]
        ):
            with patch("builtins.print") as mock_print:
                result = main.get_price()

        self.assertEqual(result, 25000)
        mock_print.assert_called_once_with(
            "Enter a valid, non-negative whole-naira price."
        )

    
    def test_get_price_rejects_letters(self):
        with patch(
            "builtins.input",
            side_effect=["hello", "25000"]
        ):
            with patch("builtins.print") as mock_print:
                result = main.get_price()

        self.assertEqual(result, 25000)
        mock_print.assert_called_once_with(
            "Please enter a valid number."
        )

 
    def test_get_price_rejects_non_finite_values(self):
        with patch(
            "builtins.input",
            side_effect=["inf", "-inf", "nan", "25000"]
        ):
            with patch("builtins.print") as mock_print:
                result = main.get_price()

        self.assertEqual(result, 25000)
        self.assertEqual(mock_print.call_count, 3)


    def test_get_price_rejects_decimal_price(self):
        with patch(
            "builtins.input",
            side_effect=["25000.50", "25000"]
        ):
            with patch("builtins.print") as mock_print:
                result = main.get_price()

        self.assertEqual(result, 25000)
        mock_print.assert_called_once_with(
        "Enter a valid, non-negative whole-naira price."
    )


    def test_get_price_rejects_decimal_with_zero_fraction(self):
        with patch(
            "builtins.input",
            side_effect=["25000.0", "25000"]
        ):
            with patch("builtins.print") as mock_print:
                result = main.get_price()

        self.assertEqual(result, 25000)
        mock_print.assert_called_once_with(
            "Enter a valid, non-negative whole-naira price."
        )



if __name__ == "__main__":
    unittest.main()
