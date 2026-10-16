import re
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

    order_id = generate_order_id(load_orders())

    order = Order(
        customer,item,fabric,style,price,
        order_id=order_id)
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
        print(f"Order ID: {order.get('order_id', 'Legacy order')}")
        print(f"Status: {order.get('status', 'Pending')}")



def main():
    while True:
        print("\n====== OYATO ======")
        print("1. Create a clothing order")
        print("2. View saved orders")
        print("3. Update order status")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_order()
        elif choice == "2":
            view_orders()
        elif choice == "3":
            update_order_status()
        elif choice == "4":
            print("Thank you for using Oyato!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()


def update_order_status():
    orders = load_orders()

    if not orders:
        print("\nNo saved orders to update.")
        return

    order_id = input("Enter the order ID: ").strip().upper()

    order = next(
        (
            saved_order
            for saved_order in orders
            if saved_order.get("order_id") == order_id
        ),
        None
    )

    if order is None:
        print("Order not found.")
        return

    print(f"\nCurrent status: {order.get('status', 'Pending')}")
    print("1. Pending")
    print("2. In Progress")
    print("3. Completed")

    choices = {
        "1": "Pending",
        "2": "In Progress",
        "3": "Completed"
    }

    choice = input("Choose the new status: ").strip()

    if choice not in choices:
        print("Invalid choice.")
        return

    order["status"] = choices[choice]

    try:
        with ORDERS_FILE.open("w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)
    except OSError:
        print("Could not save the updated status.")
        return

    print(f"Order {order_id} updated to: {order['status']}")


def generate_order_id(orders):
    highest_number = 0

    for order in orders:
        order_id = order.get("order_id", "")
        match = re.fullmatch(r"OYA-(\d+)", order_id)

        if match:
            number = int(match.group(1))
            highest_number = max(highest_number, number)

    return f"OYA-{highest_number + 1:04d}"
    

if __name__ == "__main__":
    main()
