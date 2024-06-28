import json
from user import User, Admin
from datetime import datetime, timedelta


class Book:
    def __init__(self, title, author, ISBN, status='available', borrow_date=None, due_date=None):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.status = status
        self.borrow_date = borrow_date
        self.due_date = due_date

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "ISBN": self.ISBN,
            "status": self.status,
            "borrow_date": self.borrow_date,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['title'],
            data['author'],
            data['ISBN'],
            data['status'],
            data.get('borrow_date'),
            data.get('due_date')
        )
    
class Library:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, book, user):
        if isinstance(user, Admin):
            self.books.append(book)
            self.save_books()
        else:
            raise PermissionError("Only admins can add books.")

    def remove_book(self, ISBN, user):
        if isinstance(user, Admin):
            self.books = [book for book in self.books if book.ISBN != ISBN]
            self.save_books()
        else:
            raise PermissionError("Only admins can remove books.")

    def update_book(self, ISBN, title=None, author=None, status=None, user=None):
        if isinstance(user, Admin):
            for book in self.books:
                if book.ISBN == ISBN:
                    if title: book.title = title
                    if author: book.author = author
                    if status: book.status = status
                    self.save_books()
                    break
        else:
            raise PermissionError("Only admins can update books.")

    def find_books(self, title=None, author=None):
        found_books = []
        for book in self.books:
            if title == '' and author == '':
                found_books.append(book)
            if title and title.lower() in book.title.lower():
                found_books.append(book)
            elif author and author.lower() in book.author.lower():
                found_books.append(book)
        return found_books

    def save_books(self):
        with open('books.json', 'w') as file:
            json.dump([book.to_dict() for book in self.books], file)

    def load_books(self):
        try:
            with open('books.json', 'r') as file:
                self.books = [Book.from_dict(book) for book in json.load(file)]
        except FileNotFoundError:
            self.books = []
    
    def borrow_book(self, ISBN, user):
        for book in self.books:
            if book.ISBN == ISBN:
                if book.status == 'available':
                    book.status = 'borrowed'
                    book.borrower = user.username
                    book.borrow_date = datetime.now()
                    user.borrow_book(ISBN)
                    self.update_user_data(user)
                    self.save_books()
                    return True
                else:
                    return False
        return False

    def return_book(self, ISBN, user):
        for book in self.books:
            if book.ISBN == ISBN and book.borrower == user.username:
                book.status = 'available'
                book.borrower = None
                book.borrow_date = None
                user.return_book(ISBN)
                self.update_user_data(user)
                self.save_books()
                return True
        return False

    def update_user_data(self, user):
        with open('logins.json', 'r+') as file:
            users = json.load(file)
            for u in users:
                if u['username'] == user.username:
                    u['borrowed_books'] = user.borrowed_books
            file.seek(0)
            json.dump(users, file, indent=4)
            file.truncate()

    def get_due_date(self, book):
        if book.borrow_date:
            return book.borrow_date + timedelta(days=14)
        return None

    def get_borrowed_books_by_user(self, user):
        return [book for book in self.books if book.ISBN in user.borrowed_books]
