
import json
from pathlib import Path

from customer import Customer
from order import Order

ORDERS_FILE = Path(__file__).with_name("orders.json")


def load_orders():
    if not ORDERS_FILE.exists():
        return []

    try:
        with ORDERS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved orders.")
        return []


def save_order(order):
    orders = load_orders()
    orders.append(order.to_dict())

    with ORDERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)


def get_price():
    while True:
        try:
            price = float(input("Enter the agreed price (NGN): ₦"))
            if price < 0:
                print("Price cannot be negative.")
                continue
            return price
        except ValueError:
            print("Please enter a valid number.")


def create_order():
    print("\n--- New Clothing Order ---")

    name = input("Customer name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    phone = input("Phone number: ").strip()
    if not phone:
        print("Phone number cannot be empty.")
        return

    measurements = input(
        "Measurements (e.g. chest, length, waist): "
    ).strip()

    item = input("Clothing item (e.g. Agbada): ").strip()
    fabric = input("Fabric type: ").strip()
    style = input("Style or design description: ").strip()

    if not item or not fabric or not style:
        print("Item, fabric, and style are required.")
        return

    price = get_price()

    customer = Customer(name, phone, measurements)
    order = Order(customer, item, fabric, style, price)

    try:
        save_order(order)
    except OSError:
        print("Could not save the order. Please try again.")
        return

    print("\nOrder saved successfully!")
    print(f"Customer: {name}")
    print(f"Item: {item}")
    print(f"Agreed price: ₦{price:,.2f}")


def view_orders():
    orders = load_orders()

    if not orders:
        print("\nNo saved orders yet.")
        return

    print("\n--- Saved Orders ---")

    for number, order in enumerate(orders, start=1):
        customer = order.get("customer", {})
        print(f"\nOrder {number}")
        print(f"Customer: {customer.get('name', 'Unknown')}")
        print(f"Phone: {customer.get('phone', 'Unknown')}")
        print(f"Item: {order.get('item', 'Unknown')}")
        print(f"Fabric: {order.get('fabric', 'Unknown')}")
        print(f"Style: {order.get('style', 'Unknown')}")
        print(f"Price: ₦{order.get('price', 0):,.2f}")


def main():
    while True:
        print("\n====== OYATO ======")
        print("1. Create a clothing order")
        print("2. View saved orders")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_order()
        elif choice == "2":
            view_orders()
        elif choice == "3":
            print("Thank you for using Oyato!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
