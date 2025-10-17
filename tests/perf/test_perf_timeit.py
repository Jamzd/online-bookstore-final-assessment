# File: tests/perf/test_perf_timeit.py
import timeit
from models import Book, Cart

def test_cart_total_timeit():
    """Measure time for adding books and computing total"""
    cart = Cart()
    book = Book("Perf Book", "Test", 10.0, "image.jpg")

    # Time adding books and calculating total
    duration = timeit.timeit(lambda: cart.add_book(book, quantity=5) or cart.get_total_price(), number=1000)
    
    print(f"Time for 1000 add+total operations: {duration:.6f} seconds")
    
    # Basic assertion to ensure test passes
    assert duration < 1.0  # Adjust threshold as reasonable

