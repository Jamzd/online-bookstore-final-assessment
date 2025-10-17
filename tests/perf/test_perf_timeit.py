# File: tests/perf/test_perf_timeit.py
import timeit
from models import Book, Cart

def test_cart_total_timeit():
    """Measure time for adding books and computing total"""
    cart = Cart()
    book = Book("Perf Book", "Test", 10.0, "image.jpg")

    def cart_operations():
        cart.add_book(book, quantity=5)
        cart.get_total_price()

    # Time 1000 operations
    duration = timeit.timeit(cart_operations, number=1000)
    
    # Assert the operation is reasonably fast
    assert duration < 1.0  # adjust threshold if needed
    
    # Optional: verify correctness
    total = cart.get_total_price()
    assert total == 5 * 10.0  # last operation's total
