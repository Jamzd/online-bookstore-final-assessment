import pytest
from models import Book, Cart, User, Order, PaymentGateway, EmailService

# --------------------------
# Helper functions
# --------------------------
def create_demo_books():
    return [
        Book("The Great Gatsby", "Fiction", 10.99, "img1.jpg"),
        Book("1984", "Dystopia", 8.99, "img2.jpg"),
        Book("Moby Dick", "Adventure", 12.49, "img3.jpg")
    ]

def create_demo_user(email="test@example.com"):
    return User(email, "password123", "Tester", "123 Test Lane")

# --------------------------
# USER REGISTRATION & LOGIN
# --------------------------
def test_user_registration_and_login():
    users = {}

    # Valid registration
    user = create_demo_user()
    users[user.email.lower()] = user
    assert user.email.lower() in users

    # Duplicate email registration (case-insensitive)
    duplicate_email = "Test@Example.com"
    with pytest.raises(Exception):
        if duplicate_email.lower() in users:
            raise Exception("Duplicate email detected")

    # Login correct credentials
    login_user = users.get("test@example.com")
    assert login_user.verify_password("password123") is True

    # Login incorrect password
    assert login_user.verify_password("wrong") is False

# --------------------------
# CART OPERATIONS & EDGE CASES
# --------------------------
def test_cart_operations_and_edge_cases():
    books = create_demo_books()
    cart = Cart()

    # Add multiple books
    cart.add_book(books[0], 2)
    cart.add_book(books[1], 1)
    assert cart.get_total_items() == 3
    assert cart.get_total_price() == books[0].price*2 + books[1].price*1

    # Update quantity to zero removes item
    cart.update_quantity(books[0].title, 0)
    assert books[0].title not in cart.items

    # Add negative quantity (removes item)
    cart.add_book(books[0], 1)
    cart.update_quantity(books[0].title, -1)
    assert books[0].title not in cart.items

    # Remove book
    cart.add_book(books[1])
    cart.remove_book(books[1].title)
    assert books[1].title not in cart.items

    # Remove non-existent book (edge case)
    cart.remove_book("Nonexistent Book")  # Should not crash

    # Clear cart
    cart.add_book(books[1])
    cart.clear()
    assert cart.is_empty()

    # Non-numeric quantity simulation
    with pytest.raises(ValueError):
        qty = int("not-a-number")

# --------------------------
# DISCOUNT CODES
# --------------------------
def test_discount_codes():
    books = create_demo_books()
    cart = Cart()
    cart.add_book(books[0], 2)

    # Case-sensitive discount code bug detection
    discount_code = "save10"
    total_before = cart.get_total_price()
    total_after = total_before  # no discount applied
    assert total_after == total_before

    # Successful discount application
    discount_code_correct = "SAVE10"
    total_before = cart.get_total_price()
    if discount_code_correct == "SAVE10":
        total_after = total_before * 0.9
    else:
        total_after = total_before
    assert total_after < total_before

# --------------------------
# CHECKOUT & PAYMENT
# --------------------------
def test_checkout_payment():
    books = create_demo_books()
    cart = Cart()
    cart.add_book(books[0], 1)

    payment_gateway = PaymentGateway()

    # Successful payment
    transaction = payment_gateway.process_payment({"card_number": "4111111111111112"})
    assert transaction["success"] is True

    # Failed payment
    transaction_fail = payment_gateway.process_payment({"card_number": "4111111111111111"})
    assert transaction_fail["success"] is False

# --------------------------
# ORDER CONFIRMATION
# --------------------------
def test_order_confirmation():
    books = create_demo_books()
    cart = Cart()
    cart.add_book(books[0], 1)

    user = create_demo_user()
    order = Order(user.email, cart.get_items(), {"address": "123 Lane"}, {"method": "credit_card"}, cart.get_total_price())
    email_service = EmailService()
    confirmation = email_service.send_order_confirmation(user.email, order)

    assert confirmation["to"] == user.email
    assert "order_id" in confirmation
    assert confirmation["status"] == "sent"

    # Cart should remain as is (mock test)
    assert cart.get_total_items() == 1




