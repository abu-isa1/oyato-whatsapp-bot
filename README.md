# Oyato — Nigerian Fashion Order Management

Oyato is a Python project exploring how technology can make it easier for Nigerian customers to place clothing orders with tailors.

The current version is a command-line prototype that collects customer details, records clothing preferences, and saves orders locally in JSON format.

## Problem

Customers and tailors need a clearer way to record clothing orders, including the garment, fabric, style, measurements, and agreed price. Poor record-keeping can lead to misunderstandings and mistakes.

## Current Features

- Create clothing orders.
- Record customer names and phone numbers.
- Store clothing measurements and design preferences.
- Record fabric types and agreed prices in Nigerian naira.
- Save orders to a JSON file.
- View previously saved orders.
- Validate some user inputs.
- Run automated tests for core functionality.

## Technologies

- Python 3
- Object-oriented programming
- JSON
- Python `unittest`

## Getting Started

### Requirements

Python 3 installed on your computer.

### Run the application

```bash
python3 main.py
```

### Run the tests

```bash
python3 -m unittest -v test_oyato.py
```

## Project Structure

- `main.py` — application menu and order management.
- `customer.py` — customer data model.
- `order.py` — clothing order data model.
- `test_oyato.py` — automated tests.
- `orders.json` — locally stored orders, created when an order is saved.

## Planned Improvements

- Connect customers and tailors through WhatsApp.
- Add a database for persistent order management.
- Improve input validation and error handling.
- Add order status tracking.
- Protect customer information and measurements.
- Explore features that help customers communicate clothing preferences more clearly.

## Project Status

Early-stage prototype. The current version is intended for learning, experimentation, and further development; it is not yet a production-ready service.

## About the Project

Oyato is an ongoing project focused on exploring practical technology solutions for Nigerian fashion businesses.
