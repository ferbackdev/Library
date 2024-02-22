import sys,os
sys.path.insert(0, os.getcwd())
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
from database.libraryManager import LibraryManager
from gui.admin_panel import AdminPanel
from gui.employee_panel import EmployeePanel
from database.connection import create_db_connection
from shadow import Shadow

class LoginWindow(ThemedTk):
    def __init__(self, db_connection, theme='radiance'):
        super().__init__(theme=theme)
        self.title("Login - Sistema di Gestione Biblioteca")
        self.geometry("500x500")
        self.resizable(width=False, height=False)
        self.db_connection = db_connection
        self.library_manager = LibraryManager(self.db_connection)
        self.iconbitmap('icon.ico')
        self.init_ui()

    def init_ui(self):
        #label titolo
        #ttk.Label(self, text="Sistema di Gestione Biblioteca", font=("Arial", 20), foreground='#C43800').pack(pady=20)
        # contenitore per tutto il contenuto della finestra
        self.container = ttk.Frame(
            self, 
            border=5,
            borderwidth=5, 
            relief="sunken"
            )
        self.container.pack(side="top", fill="both", padx=20, pady=10)
        Shadow(self.container, color='#C43800', size=1.02)
        #inserire immagine
        img_canvas = tk.Canvas(self.container, width=210, height=120)
        img_canvas.pack()
        img_path = sys.path[0] + "\gui\img3.png"
        img = tk.PhotoImage(file=img_path)
        img = img.subsample(2) #resize image by factor of 2 = half the original image
        img_canvas.create_image(0,0, anchor=tk.NW, image=img)
        #img_canvas.pack()
        label = tk.Label(img_canvas, image=img)
        label.image = img
        label.pack()
        # Frame di login
        login_frame = ttk.Frame(self.container)
        login_frame.pack(pady=10)
        # Campi di input per username e password
        ttk.Label(login_frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(login_frame, text="Password").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        # Pulsante di login
        self.login_button = ttk.Button(login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = self.library_manager.hash_password(password)
        # Controlla se le credenziali sono corrette
        employee = self.library_manager.check_employee(username, hashed_password)  
        if employee == 'Admin':
            messagebox.showinfo("Login", "Accesso come admin")
            self.destroy()
            admin = ThemedTk(theme="radiance")
            root = AdminPanel(admin)  # classe sia definita in admin_panel.py
            admin.mainloop()
        elif employee == 'Dipendente':
            messagebox.showinfo("Login", "Accesso come dipendente")
            self.destroy()
            employees = ThemedTk(theme="radiance")
            root = EmployeePanel(employees)  # classe sia definita in employee_panel.py
            employees.mainloop()      
        else:
            messagebox.showerror("Errore", "Ruolo non riconosciuto.")
            self.username_entry.delete(0, 'end')

if __name__ == '__main__':
    db_connection = create_db_connection()
    login_window = LoginWindow(db_connection)
    login_window.mainloop()
