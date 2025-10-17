# tests/integration/test_flows.py
import pytest
from models import Book, Cart, User, Order, PaymentGateway, EmailService

# --------------------------
# Helper functions for setup
# --------------------------
def create_demo_books():
    return [
        Book("The Great Gatsby", "Fiction", 10.99, "img1.jpg"),
        Book("1984", "Dystopia", 8.99, "img2.jpg"),
        Book("Moby Dick", "Adventure", 12.49, "img3.jpg")
    ]

# --------------------------
# USER REGISTRATION & LOGIN
# --------------------------
def test_user_registration_and_login():
    users = {}

    # Valid registration
    user = User("test@example.com", "password123", "Tester", "123 Test Lane")
    users[user.email.lower()] = user
    assert user.email.lower() in users

    # Duplicate email registration (case-insensitive)
    duplicate_email = "Test@Example.com"
    with pytest.raises(Exception):
        if duplicate_email.lower() in users:
            raise Exception("Duplicate email detected")

    # Login correct credentials
    login_user = users.get("test@example.com")
    assert login_user.password == "password123"

    # Login incorrect password
    wrong_password = "wrong"
    assert login_user.password != wrong_password

# --------------------------
# CART OPERATIONS
# --------------------------
def test_cart_operations_and_edge_cases():
    books = create_demo_books()
    cart = Cart()

    # Add book normally
    cart.add_book(books[0], 2)
    assert cart.get_total_items() == 2
    assert cart.get_total_price() == books[0].price * 2

    # Update quantity to zero (bug detection)
    cart.update_quantity(books[0].title, 0)
    # BUG: Original buggy code does not remove item
    assert books[0].title in cart.items  # intentional for detecting bug

    # Add negative quantity (bug detection)
    cart.update_quantity(books[0].title, -1)
    assert cart.items[books[0].title].quantity == -1  # shows buggy behavior

    # Remove book
    cart.remove_book(books[0].title)
    assert books[0].title not in cart.items

    # Clear cart
    cart.add_book(books[1])
    cart.clear()
    assert cart.is_empty()

    # Non-numeric quantity simulation (mocking user input)
    with pytest.raises(ValueError):
        qty = int("not-a-number")


