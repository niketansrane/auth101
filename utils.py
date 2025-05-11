import random
from datetime import datetime, timedelta

# List of random book titles
book_titles = [
    "The Great Gatsby",
    "1984",
    "To Kill a Mockingbird",
    "Pride and Prejudice",
    "The Catcher in the Rye",
    "Moby Dick",
    "War and Peace",
    "The Hobbit",
    "Crime and Punishment",
    "The Odyssey"
]

# Generate random borrow and due dates


def get_random_books():
    books = []
    for title in book_titles:
        borrow_date = datetime.now() - timedelta(days=random.randint(0, 10))  # Borrowed within the last 10 days
        due_date = borrow_date + timedelta(days=random.randint(1, 30))  # Due within the next 30 days
        books.append({
            "title": title,
            "borrow_date": borrow_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d")
        })
    return random.sample(books, k=4)