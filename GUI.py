import tkinter as tk
from tkinter import messagebox, Scrollbar, Text
from library import Library, Book
from loginGUI import LoginApp
from user import Admin, User
import datetime

class LibraryApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.library = Library()
        self.user = user

        self.title("Livraria Sagás")
        self.geometry("400x300")  # Default size for the main window

        self.main_menu()

    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("400x300")  # Reset the window size for the main menu

        self.label_main = tk.Label(self, text="Menu Principal")
        self.label_main.pack(pady=10)

        self.button_find = tk.Button(self, text="Procurar Livros", command=self.find_books_menu)
        self.button_find.pack(pady=5)

        self.button_borrow = tk.Button(self, text="Emprestar Livros", command=self.borrow_book_menu)
        self.button_borrow.pack(pady=5)

        self.button_return = tk.Button(self, text="Retornar Livros", command=self.return_book_menu)
        self.button_return.pack(pady=5)

        self.button_my_books = tk.Button(self, text="Meus Livros", command=self.my_books_menu)
        self.button_my_books.pack(pady=5)

        if isinstance(self.user, Admin):
            self.button_add = tk.Button(self, text="Adicionar Livro", command=self.add_book_menu)
            self.button_add.pack(pady=5)

            self.button_remove = tk.Button(self, text="Remover Livro", command=self.remove_book_menu)
            self.button_remove.pack(pady=5)

            self.button_update = tk.Button(self, text="Atualizar info de um Livro", command=self.update_book_menu)
            self.button_update.pack(pady=5)

    def add_book_menu(self):
        self.clear_widgets()

        self.label_title = tk.Label(self, text="Título")
        self.label_title.pack()
        self.entry_title = tk.Entry(self)
        self.entry_title.pack()

        self.label_author = tk.Label(self, text="Autor")
        self.label_author.pack()
        self.entry_author = tk.Entry(self)
        self.entry_author.pack()

        self.label_ISBN = tk.Label(self, text="ISBN")
        self.label_ISBN.pack()
        self.entry_ISBN = tk.Entry(self)
        self.entry_ISBN.pack()

        self.label_status = tk.Label(self, text="Status (disponível/emprestado)")
        self.label_status.pack()
        self.entry_status = tk.Entry(self)
        self.entry_status.pack()

        self.button_submit = tk.Button(self, text="Adicionar Livro", command=self.add_book)
        self.button_submit.pack(pady=5)

        self.button_back = tk.Button(self, text="Menu Principal", command=self.main_menu)
        self.button_back.pack(pady=5)

    def remove_book_menu(self):
        self.clear_widgets()

        self.label_ISBN = tk.Label(self, text="ISBN")
        self.label_ISBN.pack()
        self.entry_ISBN = tk.Entry(self)
        self.entry_ISBN.pack()

        self.button_submit = tk.Button(self, text="Remover Livro", command=self.remove_book)
        self.button_submit.pack(pady=5)

        self.button_back = tk.Button(self, text="Menu Principal", command=self.main_menu)
        self.button_back.pack(pady=5)

    def update_book_menu(self):
        self.clear_widgets()

        self.label_ISBN = tk.Label(self, text="ISBN")
        self.label_ISBN.pack()
        self.entry_ISBN = tk.Entry(self)
        self.entry_ISBN.pack()

        self.label_title = tk.Label(self, text="Novo Título (Opcional)")
        self.label_title.pack()
        self.entry_title = tk.Entry(self)
        self.entry_title.pack()

        self.label_author = tk.Label(self, text="Novo Autor (Opcional)")
        self.label_author.pack()
        self.entry_author = tk.Entry(self)
        self.entry_author.pack()

        self.label_status = tk.Label(self, text="Novo Status (Opcional)")
        self.label_status.pack()
        self.entry_status = tk.Entry(self)
        self.entry_status.pack()

        self.button_submit = tk.Button(self, text="Atualizar info", command=self.update_book)
        self.button_submit.pack(pady=5)

        self.button_back = tk.Button(self, text="Menu Principal", command=self.main_menu)
        self.button_back.pack(pady=5)

    def find_books_menu(self):
        self.clear_widgets()

        self.geometry("600x400")
        self.label_title = tk.Label(self, text="Título (Opcional)")
        self.label_title.pack()
        self.entry_title = tk.Entry(self)
        self.entry_title.pack()

        self.label_author = tk.Label(self, text="Autor (Opcional)")
        self.label_author.pack()
        self.entry_author = tk.Entry(self)
        self.entry_author.pack()

        self.button_submit = tk.Button(self, text="Procurar Livro", command=self.find_books)
        self.button_submit.pack(pady=5)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.results_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.results_frame, anchor='nw')

        self.results_frame.bind("<Configure>", self.on_frame_configure)

        self.button_back = tk.Button(self, text="Menu Principal", command=self.main_menu)
        self.button_back.pack(pady=5)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def find_books_menu2(self):
            self.clear_widgets()

            self.geometry("600x400")
            self.label_title = tk.Label(self, text="Título (Opcional)")
            self.label_title.pack()
            self.entry_title = tk.Entry(self)
            self.entry_title.pack()

            self.label_author = tk.Label(self, text="Autor (Opcional)")
            self.label_author.pack()
            self.entry_author = tk.Entry(self)
            self.entry_author.pack()

            self.button_submit = tk.Button(self, text="Procurar Livro", command=self.find_books)
            self.button_submit.pack(pady=5)

            self.label_copy_ISBN = tk.Label(self, text="Copie o código ISBN do livro desejado")
            self.label_copy_ISBN.pack()

            self.canvas = tk.Canvas(self)
            self.canvas.pack(side='left', fill='both', expand=True)

            self.scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
            self.scrollbar.pack(side='right', fill='y')

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.results_frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.results_frame, anchor='nw')

            self.results_frame.bind("<Configure>", self.on_frame_configure)

            self.button_back = tk.Button(self, text="Voltar", command=self.borrow_book_menu)
            self.button_back.pack(pady=5)

    def borrow_book_menu(self):
        self.clear_widgets()

        self.label_ISBN = tk.Label(self, text="ISBN")
        self.label_ISBN.pack()
        self.entry_ISBN = tk.Entry(self)
        self.entry_ISBN.pack()

        self.button_submit = tk.Button(self, text="Emprestar Livro", command=self.borrow_book)
        self.button_submit.pack(pady=5)

        self.button_submit = tk.Button(self, text="Procurar Livro", command=self.find_books_menu2)
        self.button_submit.pack(pady=5)

        self.button_back = tk.Button(self, text="Menu Principal", command=self.main_menu)
        self.button_back.pack(pady=5)

    def return_book_menu(self):
        self.clear_widgets()

        self.button_get_ISBN = tk.Button(self, text="Meus Livros", command=self.my_books_menu2)
        self.button_get_ISBN.pack()

        self.label_ISBN = tk.Label(self, text="ISBN")
        self.label_ISBN.pack()
        self.entry_ISBN = tk.Entry(self)
        self.entry_ISBN.pack()

        self.button_submit = tk.Button(self, text="Devolver Livro", command=self.return_book)
        self.button_submit.pack(pady=5)

        self.button_back = tk.Button(self, text="Menu Principal", command=self.main_menu)
        self.button_back.pack(pady=5)
    
    def my_books_menu(self):
        self.clear_widgets()

        self.geometry("600x400")

        borrowed_books = self.library.get_borrowed_books_by_user(self.user)

        self.label_main = tk.Label(self, text="Meus Livros")
        self.label_main.pack(pady=10)

        self.frame_books = tk.Frame(self)
        self.frame_books.pack(pady=10)

        for book in borrowed_books:
            due_date = book.due_date
            if due_date:
                due_date_str = due_date.strftime("%d-%m-%Y %H:%M")
            else:
                due_date_str = "Não especificado"
            
            book_frame = tk.Frame(self.frame_books)
            book_frame.pack(fill='x', pady=5)

            book_info = f"{book.title} de {book.author} (ISBN: {book.ISBN}) - Data de Retorno: {due_date_str}"
            label = tk.Label(book_frame, text=book_info, anchor='w', justify='left')
            label.pack(side='left', padx=10)

            copy_button = tk.Button(book_frame, text="Copiar ISBN", command=lambda ISBN=book.ISBN: self.copy_to_clipboard(ISBN))
            copy_button.pack(side='right')

        self.button_back = tk.Button(self, text="Menu Principal", command=self.main_menu)
        self.button_back.pack(pady=5)

    def my_books_menu2(self):
        self.clear_widgets()

        self.geometry("600x400")

        borrowed_books = self.library.get_borrowed_books_by_user(self.user)

        self.label_main = tk.Label(self, text="Meus Livros")
        self.label_main.pack(pady=10)

        self.frame_books = tk.Frame(self)
        self.frame_books.pack(pady=10)

        for book in borrowed_books:
            due_date = book.due_date
            if due_date:
                due_date_str = due_date.strftime("%d-%m-%Y %H:%M")
            else:
                due_date_str = "Não especificado"
            
            book_frame = tk.Frame(self.frame_books)
            book_frame.pack(fill='x', pady=5)

            book_info = f"{book.title} de {book.author} (ISBN: {book.ISBN}) - Data de Retorno: {due_date_str}"
            label = tk.Label(book_frame, text=book_info, anchor='w', justify='left')
            label.pack(side='left', padx=10)

            copy_button = tk.Button(book_frame, text="Copiar ISBN", command=lambda ISBN=book.ISBN: self.copy_to_clipboard(ISBN))
            copy_button.pack(side='right')
        
        self.label_copy_ISBN_2 = tk.Label(self, text="Copie o código ISBN do livro desejado")
        self.label_copy_ISBN_2.pack()

        self.button_back = tk.Button(self, text="Voltar", command=self.return_book_menu)
        self.button_back.pack(pady=5)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        ISBN = self.entry_ISBN.get()
        status = self.entry_status.get()
        if title and author and ISBN:
            book = Book(title, author, ISBN, status)
            try:
                self.library.add_book(book, self.user)
                messagebox.showinfo("Sucesso", "Livro Adicionado!")
            except PermissionError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def remove_book(self):
        ISBN = self.entry_ISBN.get()
        if ISBN:
            try:
                self.library.remove_book(ISBN, self.user)
                messagebox.showinfo("Sucesso", "Livro Removido")
            except PermissionError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "ISBN é necessário.")

    def update_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        ISBN = self.entry_ISBN.get()
        status = self.entry_status.get()
        if ISBN:
            try:
                self.library.update_book(ISBN, title, author, status, self.user)
                messagebox.showinfo("Sucesso", "Livro Atualizado!")
            except PermissionError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "ISBN é necessário.")

    def find_books(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        books = self.library.find_books(title, author)

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if books:
            for book in books:
                book_frame = tk.Frame(self.results_frame)
                book_frame.pack(fill='x', pady=5)

                book_info = f"Título: {book.title}\nAutor: {book.author}\nISBN: {book.ISBN}\nStatus: {book.status}"
                label = tk.Label(book_frame, text=book_info, anchor='w', justify='left')
                label.pack(side='left', padx=10)

                copy_button = tk.Button(book_frame, text="Copiar ISBN", command=lambda ISBN=book.ISBN: self.copy_to_clipboard(ISBN))
                copy_button.pack(side='right')
        else:
            label = tk.Label(self.results_frame, text="Nenhum livro encontrado com esses filtros.", anchor='w', justify='left')
            label.pack(pady=10)
            
    def borrow_book(self):
        ISBN = self.entry_ISBN.get()
        if ISBN:
            try:
                if self.library.borrow_book(ISBN, self.user):
                    messagebox.showinfo("Sucesso", "Livro Emprestado")
                else:
                    messagebox.showerror("Erro", "Livro não está disponível ou não existe")
            except PermissionError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "ISBN é necessário.")

    def return_book(self):
        ISBN = self.entry_ISBN.get()
        if ISBN:
            try:
                if self.library.return_book(ISBN, self.user):
                    messagebox.showinfo("Sucesso", "Livro Devolvido!")
                else:
                    messagebox.showerror("Erro", "Livro não era seu ou não existe!")
            except PermissionError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "ISBN é necessário")
        
    def copy_to_clipboard(self, ISBN):
        self.clipboard_clear()
        self.clipboard_append(ISBN)
        self.update() 
        messagebox.showinfo("Sucesso", f"ISBN {ISBN} copiado para a área de transferência!")


if __name__ == '__main__':
    def on_login_success(user, login_system):
        app = LibraryApp(user)
        app.mainloop()

    login_app = LoginApp(on_login_success)
    login_app.mainloop()
