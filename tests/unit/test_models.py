# tests/unit/test_models.py
import pytest
import models

def test_book_creation():
    b = models.Book(title="Test Book", category="Tech", price=25.0, image="image.jpg")
    assert b.title == "Test Book"
    assert b.category == "Tech"
    assert b.price == 25.0
    assert b.image == "image.jpg"

def test_cart_add_and_total():
    cart = models.Cart()
    book1 = models.Book(title="Book A", category="Fiction", price=10.0, image="img1.jpg")
    book2 = models.Book(title="Book B", category="Non-Fiction", price=5.0, image="img2.jpg")
    
    cart.add_book(book1, quantity=2)
    cart.add_book(book2, quantity=1)
    
    assert cart.get_total_items() == 3  # total quantity
    assert cart.get_total_price() == 10*2 + 5*1

def test_cart_remove_and_clear():
    cart = models.Cart()
    book = models.Book(title="Book C", category="Sci-Fi", price=15.0, image="img3.jpg")
    cart.add_book(book, 1)
    
    # Remove book
    cart.remove_book("Book C")
    assert cart.get_total_items() == 0
    assert cart.is_empty()
    
    # Add multiple items and clear
    cart.add_book(book, 2)
    cart.clear()
    assert cart.get_total_items() == 0
    assert cart.is_empty()

def test_cart_update_quantity():
    cart = models.Cart()
    book = models.Book(title="Book D", category="History", price=12.0, image="img4.jpg")
    cart.add_book(book, 1)
    cart.update_quantity("Book D", 5)
    assert cart.get_total_items() == 5
    assert cart.get_total_price() == 12*5

def test_cartitem_total_price():
    book = models.Book(title="Book E", category="Art", price=8.0, image="img5.jpg")
    item = models.CartItem(book, quantity=3)
    assert item.get_total_price() == 8*3

