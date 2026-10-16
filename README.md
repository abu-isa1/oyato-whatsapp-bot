# Oyato — Nigerian Fashion Order Management

Oyato is a Python-based clothing order management project designed to explore how technology can help Nigerian tailors and their customers record and manage clothing orders more reliably.

**Project status:** Early-stage command-line prototype under active development.

## The Problem

Clothing orders often involve several details, including fabric, garment style, measurements, customer contact information, agreed prices, and delivery progress. Poor record-keeping can cause misunderstandings between customers and tailors.

Oyato explores a simple digital approach to organizing this information and tracking orders.

## Current Features

- Create clothing orders and record customer details.
- Record clothing preferences, measurements, fabric details, and agreed prices.
- Validate phone numbers and whole-naira prices.
- Store and retrieve orders using an SQLite database.
- Generate order IDs.
- View saved orders.
- Update order statuses and track order progress.
- Search for orders using a phone number.
- Run automated tests with Python's `unittest` framework.

## Technology

- Python
- SQLite
- Object-oriented programming
- Automated testing with `unittest`
- Git and GitHub

## Getting Started

### Requirements

Install Python 3 on your computer.

### Run the application

```bash
python main.py
```

### Run the automated tests

```bash
python -m unittest -v
```

## Project Structure

- `main.py` — application menu, input validation, and order workflows.
- `customer.py` — customer-related data and behavior.
- `order.py` — clothing order data and behavior.
- `database.py` — database operations and persistent order storage.
- `test_oyato.py` — automated tests for core functionality.

## What I Am Learning

Through Oyato, I am practising how to:

- Break a practical problem into smaller software tasks.
- Organize Python code into separate modules.
- Store and retrieve structured data.
- Validate user input and handle invalid entries.
- Write automated tests and debug failures.
- Use Git and GitHub to track and publish development progress.

## Next Steps

Planned improvements include clearer user feedback, stronger testing, easier demonstrations, and exploring ways to help customers and tailors communicate about clothing orders.

## Limitations

Oyato is currently a command-line prototype. It is not yet a deployed web or mobile application, and WhatsApp integration is not yet implemented. The project is being developed incrementally, with reliability and practical usefulness as priorities.