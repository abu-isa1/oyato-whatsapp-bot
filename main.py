
from customer import Customer
from order import Order
import database


def get_required_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_phone_number():
    while True:
        phone = input("Phone number: ").strip()
        allowed_characters = set("0123456789+ -()")

        if (
            all(char in allowed_characters for char in phone)
            and sum(char.isdigit() for char in phone) >= 7
        ):
            return phone

        print("Enter a valid phone number.")


def get_price():
    while True:
        try:
            price = float(input("Enter agreed price (NGN): ₦"))

            if price < 0 or price == float("inf") or price != price:
                print("Enter a valid, non-negative price.")
                continue

            return price

        except ValueError:
            print("Please enter a valid number.")


def create_order():
    print("\n--- New Clothing Order ---")

    name = get_required_input("Customer name: ")
    phone = get_phone_number()
    measurements = get_required_input("Measurements: ")
    item = get_required_input("Clothing item: ")
    fabric = get_required_input("Fabric type: ")
    style = get_required_input("Style or design: ")
    price = get_price()

    order_id = database.generate_order_id()

    customer = Customer(name, phone, measurements)
    order = Order(
        customer,
        item,
        fabric,
        style,
        price,
        order_id=order_id
    )

    try:
        database.save_order(order)
    except Exception as error:
        print(f"Could not save the order: {error}")
        return

    print("\nOrder saved successfully!")
    print(f"Order ID: {order_id}")
    print(f"Customer: {name}")
    print(f"Item: {item}")
    print(f"Price: ₦{price:,.2f}")


def view_orders():
    orders = database.get_all_orders()

    if not orders:
        print("\nNo saved orders yet.")
        return

    print("\n--- Saved Orders ---")

    for order in orders:
        print(f"\nOrder ID: {order['order_id']}")
        print(f"Customer: {order['customer_name']}")
        print(f"Phone: {order['phone']}")
        print(f"Item: {order['item']}")
        print(f"Fabric: {order['fabric']}")
        print(f"Style: {order['style']}")
        print(f"Price: ₦{order['price']:,.2f}")
        print(f"Status: {order['status']}")


def update_order_status():
    orders = database.get_all_orders()

    if not orders:
        print("\nNo saved orders to update.")
        return

    order_id = input("Enter order ID: ").strip().upper()

    if not any(order["order_id"] == order_id for order in orders):
        print("Order not found.")
        return

    print("\n1. Pending")
    print("2. In Progress")
    print("3. Completed")

    choices = {
        "1": "Pending",
        "2": "In Progress",
        "3": "Completed"
    }

    choice = input("Choose new status: ").strip()

    if choice not in choices:
        print("Invalid choice.")
        return

    updated = database.update_status(order_id, choices[choice])

    if updated:
        print(f"Order {order_id} updated to {choices[choice]}.")
    else:
        print("Could not find that order.")



def track_order():
    print("\n--- Track Your Clothing Order ---")

    order_id = input("Enter your order ID: ").strip().upper()

    if not order_id:
        print("Please enter an order ID.")
        return

    orders = database.get_all_orders()

    for order in orders:
        if order["order_id"] == order_id:
            print("\n--- Order Details ---")
            print(f"Order ID: {order['order_id']}")
            print(f"Clothing item: {order['item']}")
            print(f"Status: {order['status']}")

            if order["status"] == "Pending":
                print("Your order is waiting to be started.")
            elif order["status"] == "In Progress":
                print("Your tailor is working on your clothing.")
            elif order["status"] == "Completed":
                print("Your clothing is ready!")

            return

    print("Order not found. Please check your order ID.")




def main():
    database.initialize_database()

    while True:
        print("\n====== OYATO ======")
        print("1. Create a clothing order")
        print("2. View saved orders")
        print("3. Update order status")
        print("4. Track an order")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_order()
        elif choice == "2":
            view_orders()
        elif choice == "3":
            update_order_status()
        elif choice == "4":
            track_order()
        elif choice == "5":
            print("Thank you for using Oyato!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()

