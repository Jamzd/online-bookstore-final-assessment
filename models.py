# models.py

import hashlib
import re

# --------------------------
# User class
# --------------------------
class User:
    """Secure User account management class with session handling"""
    
    def __init__(self, email, password, name="", address=""):
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        self.email = email.lower()  # normalize for duplicates
        
        # Store hashed password
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self._raw_password = None  # prevent storing plaintext
        
        self.name = name
        self.address = address
        self.orders = []
        self.logged_in = False  # track session state

    # --------------------------
    # Password handling
    # --------------------------
    def verify_password(self, password):
        return self.hashed_password == hashlib.sha256(password.encode()).hexdigest()

    # --------------------------
    # Session handling
    # --------------------------
    def login(self, password):
        if self.verify_password(password):
            self.logged_in = True
            return True
        return False

    def logout(self):
        self.logged_in = False

    # --------------------------
    # Order handling
    # --------------------------
    def add_order(self, order):
        self.orders.append(order)
        self.orders.sort(key=lambda x: getattr(x, "order_date", None))

    def get_order_history(self):
        return self.orders


# --------------------------
# Book class
# --------------------------
class Book:
    def __init__(self, title, category, price, image):
        if price < 0:
            raise ValueError("Price must be non-negative")
        self.title = title
        self.category = category
        self.price = price
        self.image = image


# --------------------------
# CartItem class
# --------------------------
class CartItem:
    def __init__(self, book, quantity=1):
        self.book = book
        self.quantity = quantity
    
    def get_total_price(self):
        return self.book.price * self.quantity


# --------------------------
# Cart class
# --------------------------
class Cart:
    """A shopping cart for books"""
    
    def __init__(self):
        self.items = {}  # key: book title, value: CartItem

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

    def update_quantity(self, title, quantity):
        if title in self.items:
            if quantity <= 0:
                del self.items[title]
            else:
                self.items[title].quantity = quantity

    def get_total_price(self):
        return sum(item.book.price * item.quantity for item in self.items.values())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.values())

    def clear(self):
        self.items = {}

    def get_items(self):
        return list(self.items.values())

    def is_empty(self):
        return len(self.items) == 0


# --------------------------
# Order class
# --------------------------
class Order:
    """Order management class"""
    def __init__(self, order_id, user_email, items, shipping_info, payment_info, total_amount):
        import datetime
        self.order_id = order_id
        self.user_email = user_email
        self.items = items.copy()  # Copy of cart items
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
# PaymentGateway class
# --------------------------
class PaymentGateway:
    """Mock payment gateway for processing payments"""
    
    @staticmethod
    def process_payment(payment_info):
        """Mock payment processing - returns success/failure with mock logic"""
        card_number = payment_info.get('card_number', '')
        
        # Mock logic: cards ending in '1111' fail, others succeed
        if card_number.endswith('1111'):
            return {
                'success': False,
                'message': 'Payment failed: Invalid card number',
                'transaction_id': None
            }
        
        import random
        import time
        
        time.sleep(0.1)
        
        transaction_id = f"TXN{random.randint(100000, 999999)}"
        
        return {
            'success': True,
            'message': 'Payment processed successfully',
            'transaction_id': transaction_id
        }


# --------------------------
# EmailService class
# --------------------------
class EmailService:
    """Mock email service for sending order confirmations"""
    
    @staticmethod
    def send_order_confirmation(user_email, order):
        """Mock email sending - just prints to console in this implementation"""
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
        
        return True

