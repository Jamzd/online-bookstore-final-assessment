import pytest
import models

# -------------------------------
# Book tests
# -------------------------------
def test_book_creation():
    b = models.Book(title="Test Book", category="Tech", price=25.0, image="image.jpg")
    assert b.title == "Test Book"
    assert b.category == "Tech"
    assert b.price == 25.0
    assert b.image == "image.jpg"

def test_book_invalid_attributes():
    with pytest.raises(ValueError):
        models.Book(title="Bad Book", category="None", price=-5.0, image=None)

    b = models.Book(title="", category=None, price=0.0, image=None)
    assert b.title == ""
    assert b.category is None
    assert b.price == 0.0

def test_book_negative_price_raises():
    with pytest.raises(ValueError):
        models.Book(title="Bad Book", category="Test", price=-10, image="img.jpg")

# -------------------------------
# Cart tests
# -------------------------------
def test_cart_add_and_total():
    cart = models.Cart()
    book1 = models.Book(title="Book A", category="Fiction", price=10.0, image="img1.jpg")
    book2 = models.Book(title="Book B", category="Non-Fiction", price=5.0, image="img2.jpg")
    
    cart.add_book(book1, quantity=2)
    cart.add_book(book2, quantity=1)
    
    assert cart.get_total_items() == 3
    assert cart.get_total_price() == 10*2 + 5*1

def test_cart_add_same_book_multiple_times():
    cart = models.Cart()
    book = models.Book(title="Book C", category="Sci-Fi", price=15.0, image="img3.jpg")
    cart.add_book(book, 1)
    cart.add_book(book, 2)
    assert cart.get_total_items() == 3
    assert cart.get_total_price() == 15*3

def test_cart_remove_and_clear():
    cart = models.Cart()
    book = models.Book(title="Book D", category="History", price=12.0, image="img4.jpg")
    cart.add_book(book, 2)
    
    cart.remove_book("Book D")
    assert cart.get_total_items() == 0
    assert cart.is_empty()
    
    cart.remove_book("Nonexistent Book")
    assert cart.get_total_items() == 0
    
    cart.add_book(book, 2)
    cart.clear()
    assert cart.get_total_items() == 0
    assert cart.is_empty()

def test_cart_update_quantity():
    cart = models.Cart()
    book = models.Book(title="Book E", category="Art", price=8.0, image="img5.jpg")
    cart.add_book(book, 1)

    cart.update_quantity("Book E", 5)
    assert cart.get_total_items() == 5
    assert cart.get_total_price() == 8*5

    cart.update_quantity("Book E", 0)
    assert cart.get_total_items() == 0
    assert cart.is_empty()

    cart.add_book(book, 1)
    cart.update_quantity("Book E", -3)
    assert cart.get_total_items() == 0

    cart.update_quantity("Nonexistent Book", 3)
    assert cart.get_total_items() >= 0

def test_cart_add_invalid_quantity():
    cart = models.Cart()
    book = models.Book(title="Book F", category="Mystery", price=7.0, image="img6.jpg")
    
    with pytest.raises(TypeError):
        cart.add_book(book, quantity="two")

# -------------------------------
# CartItem tests
# -------------------------------
def test_cartitem_total_price():
    book = models.Book(title="Book G", category="Art", price=8.0, image="img7.jpg")
    item = models.CartItem(book, quantity=3)
    assert item.get_total_price() == 8*3
