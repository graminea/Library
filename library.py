import json
from datetime import datetime, timedelta
from user import User, Admin

class Book:
    def __init__(self, title, author, ISBN, status='disponível', borrow_date=None, due_date=None, borrower=None):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.status = status
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.borrower = borrower

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "ISBN": self.ISBN,
            "status": self.status,
            "borrow_date": self.borrow_date.isoformat() if self.borrow_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "borrower": self.borrower
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['title'],
            data['author'],
            data['ISBN'],
            data['status'],
            datetime.fromisoformat(data['borrow_date']) if data.get('borrow_date') else None,
            datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            data.get('borrower')
        )

class Library:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, book, user):
        if isinstance(user, Admin):
            self.books.append(book)
            self.save_books()
            self.log_action(user.username, f"Added book {book.title} (ISBN: {book.ISBN})")
        else:
            raise PermissionError("Somente Admins podem adicionar livros.")

    def remove_book(self, ISBN, user):
        if isinstance(user, Admin):
            self.books = [book for book in self.books if book.ISBN != ISBN]
            self.save_books()
            self.log_action(user.username, f"Removed book with ISBN {ISBN}")
        else:
            raise PermissionError("Somente Admins podem remover livros.")

    def update_book(self, ISBN, title=None, author=None, status=None, user=None):
        if isinstance(user, Admin):
            for book in self.books:
                if book.ISBN == ISBN:
                    old_title = book.title
                    old_author = book.author
                    if title: book.title = title
                    if author: book.author = author
                    if status: book.status = status
                    self.save_books()
                    self.log_action(user.username, f"Updated book {old_title} (ISBN: {ISBN}) to {book.title}, {book.author}, {book.status}")
                    break
        else:
            raise PermissionError("Somente Admins podem atualizar livros.")

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
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def load_books(self):
        try:
            with open('books.json', 'r') as file:
                self.books = [Book.from_dict(book) for book in json.load(file)]
        except FileNotFoundError:
            self.books = []

    def borrow_book(self, ISBN, user):
        for book in self.books:
            if book.ISBN.strip() == ISBN.strip():  # Check ISBN matching with stripped whitespace
                print(f"Book found: {book.title}")
                if book.status == 'disponivel':
                    book.status = 'emprestado'
                    book.borrower = user.username
                    book.borrow_date = datetime.now()
                    book.due_date = book.borrow_date + timedelta(days=14)
                    user.borrow_book(ISBN)
                    self.update_user_data(user)
                    self.save_books()
                    self.log_action(user.username, f"Emprestou {book.title} (ISBN: {book.ISBN})")
                    return True
                else:
                    print(f"Book status is {book.status}, not available for borrowing.")
                    return False
        print(f"Book with ISBN {ISBN} not found in the library.")
        return False

    def return_book(self, ISBN, user):
        for book in self.books:
            if book.ISBN == ISBN and book.borrower == user.username:
                book.status = 'disponivel'
                book.borrower = None
                book.borrow_date = None
                book.due_date = None
                user.return_book(ISBN)
                self.update_user_data(user)
                self.save_books()
                self.log_action(user.username, f"Devolveu {book.title} (ISBN: {book.ISBN})")
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
        return book.due_date

    def get_borrowed_books_by_user(self, user):
        return [book for book in self.books if book.borrower == user.username]

    def log_action(self, username, action):
        with open('logs.txt', 'a') as file:
            file.write(f"{datetime.now().strftime("%d-%m-%Y %H:%M")} - {username} - {action}\n")
