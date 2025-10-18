# models.py
import datetime
import random
import hashlib

# --------------------------
# BOOK & CART
# --------------------------
class Book:
    def __init__(self, title, category, price, image):
        if price < 0:
            raise ValueError("Price must be non-negative")
        self.title = title
        self.category = category
        self.price = price
        self.image = image


class CartItem:
    def __init__(self, book, quantity=1):
        self.book = book
        self.quantity = quantity
    
    def get_total_price(self):
        return self.book.price * self.quantity


class Cart:
    """Shopping cart holding books with quantities"""
    def __init__(self):
        self.items = {}

    def add_book(self, book, quantity=1):
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")
        if book.title in self.items:
            self.items[book.title].quantity += quantity
        else:
            self.items[book.title] = CartItem(book, quantity)

    def remove_book(self, book_title):
        if book_title in self.items:
            del self.items[book_title]

    def update_quantity(self, book_title, quantity):
        if book_title in self.items:
            if quantity <= 0:
                del self.items[book_title]
            else:
                self.items[book_title].quantity = quantity

    def get_total_price(self):
        total = 0
        for item in self.items.values():
            total += item.book.price * item.quantity
        return total

    def get_total_items(self):
        return sum(item.quantity for item in self.items.values())

    def clear(self):
        self.items = {}

    def get_items(self):
        return list(self.items.values())

    def is_empty(self):
        return len(self.items) == 0

# --------------------------
# USER & SECURITY
# --------------------------
import re

class User:
    def __init__(self, email, password, name, address):
        # stricter email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email")
        self.email = email
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.name = name
        self.address = address
        self.logged_in = False


    def verify_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.hashed_password

    def login(self, password):
        if self.verify_password(password):
            self.logged_in = True
            return True
        return False

    def logout(self):
        self.logged_in = False

    def add_order(self, order):
        self.orders.append(order)
        self.orders.sort(key=lambda x: x.order_date)

# --------------------------
# ORDER
# --------------------------
class Order:
    """Order with items, user, payment info, and date"""
    def __init__(self, user_email, items, shipping_info, payment_info, total_amount):
        self.order_id = f"ORD{random.randint(1000, 9999)}"
        self.user_email = user_email
        self.items = items.copy()
        self.shipping_info = shipping_info
        self.payment_info = payment_info
        self.total_amount = total_amount
        self.order_date = datetime.datetime.now()
        self.status = "Confirmed"

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_email': self.user_email,
            'items': [{'title': item.book.title, 'quantity': item.quantity, 'price': item.book.price} for item in self.items],
            'shipping_info': self.shipping_info,
            'total_amount': self.total_amount,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }

# --------------------------
# PAYMENT
# --------------------------
class PaymentGateway:
    """Mock payment gateway"""
    @staticmethod
    def process_payment(payment_info):
        card_number = payment_info.get('card_number', '')

        if card_number.endswith('1111'):
            return {
                'success': False,
                'message': 'Payment failed: Invalid card number',
                'transaction_id': None
            }

        transaction_id = f"TXN{random.randint(100000, 999999)}"
        return {
            'success': True,
            'message': 'Payment processed successfully',
            'transaction_id': transaction_id
        }

# --------------------------
# EMAIL
# --------------------------
class EmailService:
    """Mock email service"""
    @staticmethod
    def send_order_confirmation(user_email, order):
        # Mock sending email (just prints)
        print(f"\n=== EMAIL SENT ===")
        print(f"To: {user_email}")
        print(f"Subject: Order Confirmation - Order #{order.order_id}")
        print(f"Order Date: {order.order_date}")
        print(f"Total Amount: ${order.total_amount:.2f}")
        print(f"Items:")
        for item in order.items:
            print(f"  - {item.book.title} x{item.quantity} @ ${item.book.price:.2f}")
        print(f"Shipping Address: {order.shipping_info.get('address', 'N/A')}")
        print(f"==================\n")

        return {"to": user_email, "order_id": order.order_id, "status": "sent"}
