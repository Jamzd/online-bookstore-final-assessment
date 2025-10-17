# File: tests/perf/test_perf_cprofile.py
import cProfile
from models import Book, Cart

def test_cart_total_cprofile():
    """Profile cart operations to identify bottlenecks"""
    cart = Cart()
    book = Book("Perf Book", "Test", 10.0, "image.jpg")

    def cart_operations():
        for _ in range(100):
            cart.add_book(book, quantity=2)
        cart.get_total_price()

    profiler = cProfile.Profile()
    profiler.enable()
    cart_operations()
    profiler.disable()

    profiler.print_stats(sort="cumtime")  # cumulative time

