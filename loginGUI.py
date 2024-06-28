import tkinter as tk
import tkinter.messagebox as messagebox
from login import Login

from user import Admin, User

class LoginApp(tk.Tk):
    def __init__(self, on_login_success):
        super().__init__()
        self.login_system = Login()
        self.on_login_success = on_login_success

        self.title("Login")
        self.geometry("300x200")

        self.label_user = tk.Label(self, text="Usuário:")
        self.label_user.grid(row=0, column=0, padx=5, pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = tk.Label(self, text="Senha:")
        self.label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.show_password = False
        self.show_password_button = tk.Button(self, text='👁️', command=self.toggle_password)
        self.show_password_button.grid(row=1, column=2, padx=5, pady=5)

        self.button_login = tk.Button(self, text="Login", command=self.perform_login)
        self.button_login.grid(row=2, column=0, columnspan=3, pady=5)

        self.button_register = tk.Button(self, text="Registrar", command=self.perform_register)
        self.button_register.grid(row=3, column=0, columnspan=3, pady=5)


    def perform_login(self):
        username = self.entry_user.get()
        password = self.entry_password.get()

        logged_in_user = self.login_system.login(username, password)
        if logged_in_user:
            messagebox.showinfo("Sucesso", "Login efetuado com sucesso!")
            self.destroy()
            self.on_login_success(logged_in_user, self.login_system)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def perform_register(self):
        username = self.entry_user.get()
        password = self.entry_password.get()
        self.login_system.register(username, password)
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso! Realize o login.")

    def toggle_password(self):
        if self.show_password:
            self.entry_password.config(show="*")
        else:
            self.entry_password.config(show="")
        self.show_password = not self.show_password




