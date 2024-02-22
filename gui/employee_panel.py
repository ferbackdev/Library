import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
import sys,os, random
sys.path.insert(0, os.getcwd())
from database.connection import create_db_connection
from database.libraryManager import LibraryManager
from models.book import Book
from models.categorie import Category
from models.employee import Employee
from models.user import User
from models.loan import Loan
from shadow import Shadow

class EmployeePanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Pannello di Amministrazione")
        self.root.iconbitmap('icon.ico')
        self.db_connection = create_db_connection()
        # Inizializzazione del tema
        self.style = ttk.Style(self.root)
        self.root.set_theme("radiance")  # Scegli il tema desiderato
        self.root.geometry("900x600")
        self.root.resizable(width=True, height=False)
        # Inizializza il layout del pannello di amministrazione
        self.init_ui()
        
    def init_ui(self):
        #region Menu
        container = ttk.Frame(self.root)
        container.pack(fill=tk.X)
        # contenitore per tutto il contenuto della finestra
        manage_frame = ttk.Frame(container, border=5, borderwidth=5, relief="sunken")
        manage_frame.pack(fill=tk.X)
        user_var = tk.StringVar()
        user_list_menu = ["Gestione Utenti", "Aggiungi Utente"]
        user_menu = ttk.OptionMenu(manage_frame, user_var, "Gestione Utenti", *user_list_menu, command=self.manage_users)
        user_menu.pack(side=tk.LEFT, padx=5)
        category_var = tk.StringVar()
        category_list_menu = ["Gestione Categorie", "Aggiungi Categoria"]
        category_menu = ttk.OptionMenu(manage_frame, category_var, "Gestione Categorie", *category_list_menu, command=self.manage_categories)
        category_menu.pack(side=tk.LEFT, padx=5)
        employee_var = tk.StringVar()
        employee_list_menu = ["Gestione Dipendenti", "Aggiungi Dipendente"]
        employee_menu = ttk.OptionMenu(manage_frame, employee_var, "Gestione Dipendenti", *employee_list_menu, command=self.manage_employees)
        employee_menu.pack(side=tk.LEFT, padx=5)
        book_var = tk.StringVar()
        book_list_menu = ["Gestione Libri", "Aggiungi Libro"]
        book_menu = ttk.OptionMenu(manage_frame, book_var, "Gestione Libri", *book_list_menu, command=self.manage_books)
        book_menu.pack(side=tk.LEFT, padx=5)
        loan_var = tk.StringVar()
        loan_list_menu = ["Gestione Prestiti", "Aggiungi Prestito"]
        loan_menu = ttk.OptionMenu(manage_frame, loan_var, "Gestione Prestiti", *loan_list_menu, command=self.manage_loans)
        loan_menu.pack(side=tk.LEFT, padx=5)

        # Barra di ricerca
        search_label = ttk.Label(manage_frame, text="Cerca:")
        search_label.pack(side=tk.LEFT, padx=15)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(manage_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=8)
        self.search_button = ttk.Button(manage_frame, text="Cerca", command=self.search_treeview)
        self.search_button.pack(side=tk.LEFT, padx=8)
        
        # Bottone per il logout
        logout_button = ttk.Button(manage_frame, text="Logout", command=self.root.destroy)
        logout_button.pack(side=tk.RIGHT, padx=5)
        #endregion
        
        # Frame per treeview, scrollbar e text area
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        self.tree = ttk.Treeview(tree_frame, selectmode = 'extended', show="headings", style="Custom.Treeview")
        self.tree.pack(side='left', fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)
        
        #Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

    #region Gestione Doppio Click
    def on_double_click(self, event):
        y = 20
        x = 20
        # Dizionario per tracciare le entry
        self.entries = {}
        item = self.tree.selection()[0]
        values = self.tree.item(item)['values']
        tag = self.tree.item(item)['tags'][0]
        dialog = tk.Toplevel(self.root)
        dialog.title("Dettagli")
        dialog.geometry("400x550")
        dialog.iconbitmap('icon.ico')
        dialog.resizable(width=False, height=False)
        colonne_tree = self.tree['columns']
        #per ogni colonna crea un label e un entry con nomi e valori della riga selezionata
        for i, col in enumerate(colonne_tree):
            y += 40
            label = ttk.Label(dialog, text=col.capitalize())
            label.place(x=x, y=y) 
            var = tk.StringVar(dialog, values[i]) # valore della riga selezionata
            if "Data" in col or "Anno" in col:
                entry = DateEntry(dialog, textvariable=var)            
            elif col == "Password":
                entry = ttk.Entry(dialog, textvariable=var)
                entry.config(show="*", state="readonly")
            elif col == "Ruolo":
                entry = ttk.Combobox(dialog, values=["Admin", "Dipendente"], state="readonly", width=17)
                entry.current(1)
            elif col == "Categoria":
                entry = ttk.Combobox(dialog, values=Category.get_all_categories_names(self.db_connection), state="readonly", width=17)
                entry.current(1)
            elif col == "ID":
                entry = ttk.Entry(dialog, textvariable=var, state="readonly")
            elif col == "Utente":
                entry = ttk.Entry(dialog, textvariable=var, state="readonly")
            elif col == "Titolo Libro":
                entry = ttk.Entry(dialog, textvariable=var, state="readonly")
            elif col == "Stato":
                entry = ttk.Combobox(dialog, values=['Restituito','Scaduto'], state="readonly", width=17)  
                entry.current(0)      
            else:
                entry = ttk.Entry(dialog, textvariable=var)
            entry.place(x=x+150, y=y)
            self.entries[col] = var
        if tag == "book":
            dialog.geometry("380x450")
        elif tag == "category":
            dialog.geometry("370x230")
        elif tag == "employee":
            dialog.geometry("380x430")
        elif tag == "user":
            dialog.geometry("380x370")
        elif tag == "loan":
            dialog.geometry("370x400")
            
        #region Gestione Modifica Valori
        def update_values(tag):
            new_values = [var.get() for var in self.entries.values()]
            if tag == "book":
                Book.update_book(dialog, self.db_connection, new_values, values)
                Book.configure_book_treeview(self.db_connection, self.tree)
            elif tag == "category":
                Category.update_category(dialog, self.db_connection, new_values, values)
                Category.configure_category_treeview(self.db_connection, self.tree)  
            elif tag == "employee":
                Employee.update_employee(dialog, self.db_connection,"Dipendente", new_values, values)
                Employee.configure_employee_treeview(self.db_connection, self.tree) 
            elif tag == "user":
                User.update_user(dialog, self.db_connection, new_values, values)
                User.configure_user_treeview(self.db_connection, self.tree)
            elif tag == "loan":
                Loan.update_loan(dialog, self.db_connection, values)
                Loan.configure_loan_treeview(self.db_connection, self.tree)
        #endregion
        
        #region Gestione Eliminazione
        def delete_values(tag):
            if tag == "book":
                Book.delete_book(dialog, self.db_connection, values)
                Book.configure_book_treeview(self.db_connection, self.tree)
            elif tag == "category":
                Category.delete_category(dialog, self.db_connection, values)
                Category.configure_category_treeview(self.db_connection, self.tree)  
            elif tag == "employee":
                Employee.delete_employee(dialog, self.db_connection,"Dipendente", values)
                Employee.configure_employee_treeview(self.db_connection, self.tree) 
            elif tag == "user":
                User.delete_user(dialog, self.db_connection, values)
                User.configure_user_treeview(self.db_connection, self.tree)
            elif tag == "loan":
                Loan.delete_loan(dialog, self.db_connection, values)
                Loan.configure_loan_treeview(self.db_connection, self.tree)
        #endregion
                
        modifica_button = ttk.Button(dialog, text="Modifica", command=lambda: update_values(tag))
        modifica_button.place(x=60, y=y+80)
        elimina_button = ttk.Button(dialog, text="Elimina", command=lambda: delete_values(tag))
        elimina_button.place(x=200, y=y+80)
    #endregion

    def change_theme(self, theme_name):
        self.root.set_theme(theme_name)

    #region Gestione Ricerca
    def search_treeview(self):
        self.tree.selection_remove(self.tree.get_children())
        search_query = self.search_var.get().casefold()  
        for child in self.tree.get_children():
            valori = self.tree.item(child)['values']
            for name in valori:
                if type(name) == int:
                    name = str(name)
                if search_query in name.casefold():
                    self.tree.selection_add(child)
                    self.tree.focus(child)
                    self.tree.see(child)
    #endregion
    
    #region Gestione Utenti
    def manage_users(self, *args):
        # Ottieni il valore del pulsante selezionato
        user_list_menu = args[0]
        if user_list_menu == "Gestione Utenti":
            User.configure_user_treeview(self.db_connection, self.tree)   
        elif user_list_menu == "Aggiungi Utente":
            # Crea finestra di dialogo per l'inserimento dei dati
            dialog = tk.Toplevel(self.root)
            dialog.title("Aggiungi Utente")
            dialog.geometry("370x400")
            dialog.resizable(width=False, height=False)
            dialog.iconbitmap('icon.ico')
            ##inserire immagine
            img_canvas = tk.Canvas(dialog)
            img_canvas.pack()
            img_path = sys.path[0] + "\gui\img3.png"
            img = tk.PhotoImage(file=img_path)  # PIL solution
            img = img.subsample(3) #resize image by factor of 2 = half the original image
            img_canvas.create_image(0,0, anchor=tk.NW, image=img)
            label_img = tk.Label(img_canvas, image=img)
            label_img.image = img
            label_img.pack()
            # contenitore per tutto il contenuto della finestra
            self.container = ttk.Frame(
                dialog, 
                border=5,
                borderwidth=5,
                width=350,
                height=200, 
                relief="sunken"
                )
            self.container.place(x=10, y=180)
            Shadow(self.container, color='#F99B9F', size=1.02, offset_x=-1, offset_y=-1)
            # Crea i campi di input
            nome_label = ttk.Label(self.container, text="Nome:")
            nome_label.place(x=20, y=20)
            nome_var = tk.StringVar()
            nome_entry = ttk.Entry(self.container, textvariable=nome_var)
            nome_entry.place(x=150, y=20)
            cognome_label = ttk.Label(self.container, text="Cognome:")
            cognome_label.place(x=20, y=60)
            cognome_var = tk.StringVar()
            cognome_entry = ttk.Entry(self.container, textvariable=cognome_var)
            cognome_entry.place(x=150, y=60)
            email_label = ttk.Label(self.container, text="Email:")
            email_label.place(x=20, y=100)
            email_var = tk.StringVar()
            email_entry = ttk.Entry(self.container, textvariable=email_var)
            email_entry.place(x=150, y=100)
            def get_datas():
                send = True
                if nome_var.get() == "" or len(nome_var.get()) <=2 or nome_var.get().isnumeric():
                    messagebox.showerror("Errore", "Il nome è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if cognome_var.get() == "" or len(cognome_var.get()) <=2 or cognome_var.get().isnumeric():
                    messagebox.showerror("Errore", "Il cognome è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if email_var.get() == "" or len(email_var.get()) <= 5 or email_var.get().isnumeric() or "@" not in email_var.get():
                    messagebox.showerror("Errore", "L'email è obbligatoria e deve essere compilata correttamente.")
                    send = False
                if send == True:
                    User.add_user(dialog, self.db_connection, nome_var.get(), cognome_var.get(), email_var.get())
                    User.configure_user_treeview(self.db_connection, self.tree)
            # Crea il pulsante di conferma
            confirm_button = ttk.Button(self.container, text="Aggiungi", command=get_datas)
            confirm_button.place(x=100, y=140)
    #endregion
    
    #region Gestione Categorie        
    def manage_categories(self, *args):
        # Ottieni il valore del pulsante selezionato
        category_list_menu = args[0]
        if category_list_menu == "Gestione Categorie":
            Category.configure_category_treeview(self.db_connection, self.tree)
        elif category_list_menu == "Aggiungi Categoria":
            # Crea finestra di dialogo per l'inserimento dei dati
            dialog = tk.Toplevel(self.root)
            dialog.title("Aggiungi Categoria")
            dialog.geometry("355x400")
            dialog.resizable(width=False, height=False)
            dialog.iconbitmap('icon.ico')
            ##inserire immagine
            img_canvas = tk.Canvas(dialog, width=350, height=120)
            img_canvas.pack()
            img_path = sys.path[0] + "\gui\img3.png"
            img = tk.PhotoImage(file=img_path)  # PIL solution
            img = img.subsample(3) #resize image by factor of 2 = half the original image
            img_canvas.create_image(0,0, anchor=tk.NW, image=img)
            label_img = tk.Label(img_canvas, image=img)
            label_img.image = img
            label_img.pack()
            # contenitore per tutto il contenuto della finestra
            self.container = ttk.Frame(
                dialog, 
                border=5,
                borderwidth=5,
                width=330,
                height=200, 
                relief="sunken"
                )
            self.container.place(x=13, y=180)
            Shadow(self.container, color='#F99B9F', size=1.02, offset_x=-1, offset_y=-1)
            # Crea i campi di input
            nome_label = ttk.Label(self.container, text="Nome:")
            nome_label.place(x=20, y=20)
            nome_var = tk.StringVar()
            nome_entry = ttk.Entry(self.container, textvariable=nome_var)
            nome_entry.place(x=150, y=20)
            descrizione_label = ttk.Label(self.container, text="Descrizione:")
            descrizione_label.place(x=20, y=70)
            descrizione_var = tk.StringVar()
            descrizione_entry = ttk.Entry(self.container, textvariable=descrizione_var)
            descrizione_entry.place(x=150, y=70)
            def get_datas():
                send = True
                if nome_var.get() == "" or len(nome_var.get()) <=2 or nome_var.get().isnumeric():
                    messagebox.showerror("Errore", "Il nome è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if descrizione_var.get() == "" or len(descrizione_var.get()) <=2 or descrizione_var.get().isnumeric():
                    messagebox.showerror("Errore", "La descrizione è obbligatoria e deve essere compilata correttamente.")
                    send = False
                if send == True:
                    Category.add_category(dialog, self.db_connection, nome_var.get(), descrizione_var.get())
                    Category.configure_category_treeview(self.db_connection, self.tree)
            # Crea il pulsante di conferma
            confirm_button = ttk.Button(self.container, text="Aggiungi", command=get_datas)
            confirm_button.place(x=90, y=130)
    #endregion
    
    #region Gestione Dipendenti        
    def manage_employees(self, *args):
        # Ottieni il valore del pulsante selezionato
        employee_list_menu = args[0]
        if employee_list_menu == "Gestione Dipendenti":
            Employee.configure_employee_treeview(self.db_connection, self.tree)
        elif employee_list_menu == "Aggiungi Dipendente":
            # Crea finestra di dialogo per l'inserimento dei dati
            dialog = tk.Toplevel(self.root)
            dialog.title("Aggiungi Dipendente")
            dialog.geometry("380x560")
            dialog.iconbitmap('icon.ico')
            dialog.resizable(width=False, height=False)
            dialog.iconbitmap('icon.ico')
            ##inserire immagine
            img_canvas = tk.Canvas(dialog, width=350, height=120)
            img_canvas.pack()
            img_path = sys.path[0] + "\gui\img3.png"
            img = tk.PhotoImage(file=img_path)  # PIL solution
            img = img.subsample(3) #resize image by factor of 2 = half the original image
            img_canvas.create_image(0,0, anchor=tk.NW, image=img)
            label_img = tk.Label(img_canvas, image=img)
            label_img.image = img
            label_img.pack()
            # contenitore per tutto il contenuto della finestra
            self.container = ttk.Frame(
                dialog, 
                border=5,
                borderwidth=5,
                width=350,
                height=350, 
                relief="sunken"
                )
            self.container.place(x=13, y=180)
            Shadow(self.container, color='#F99B9F', size=1.02, offset_x=-1, offset_y=-1)
            #Verifica chei campi siano stati riempiti correttamente
            nome_label = ttk.Label(self.container, text="Nome:")
            nome_label.place(x=40, y=20)
            nome_var = tk.StringVar()
            nome_entry = ttk.Entry(self.container, textvariable=nome_var)
            nome_entry.place(x=170, y=20)
            cognome_label = ttk.Label(self.container, text="Cognome:")
            cognome_label.place(x=40, y=60)
            cognome_var = tk.StringVar()
            cognome_entry = ttk.Entry(self.container, textvariable=cognome_var)
            cognome_entry.place(x=170, y=60)
            email_label = ttk.Label(self.container, text="Email:")
            email_label.place(x=40, y=100)
            email_var = tk.StringVar()
            email_entry = ttk.Entry(self.container, textvariable=email_var)
            email_entry.place(x=170, y=100)
            user_label = ttk.Label(self.container, text="Username:")
            user_label.place(x=40, y=140)
            user_var = tk.StringVar()
            user_entry = ttk.Entry(self.container, textvariable=user_var)
            user_entry.place(x=170, y=140)
            password_label = ttk.Label(self.container, text="Password:")
            password_label.place(x=40, y=180)
            password_var = tk.StringVar()
            password_entry = ttk.Entry(self.container, textvariable=password_var, show="*")
            password_entry.place(x=170, y=180)
            ruolo_label = ttk.Label(self.container, text="Ruolo:")
            ruolo_label.place(x=40, y=220)
            ruolo_entry = ttk.Combobox(self.container, values=["Admin", "Dipendente"], state="readonly", width=17)
            ruolo_entry.current(1)
            ruolo_entry.place(x=170, y=220)   
            def get_datas():
                send = True
                if nome_var.get() == "" or len(nome_var.get()) <=2 or nome_var.get().isnumeric():
                    messagebox.showerror("Errore", "Il nome è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if cognome_var.get() == "" or len(cognome_var.get()) <=2 or cognome_var.get().isnumeric():
                    messagebox.showerror("Errore", "Il cognome è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if email_var.get() == "" or len(email_var.get()) <= 5 or email_var.get().isnumeric() or "@" not in email_var.get():
                    messagebox.showerror("Errore", "L'email è obbligatoria e deve essere compilata correttamente.")
                    send = False
                if user_var.get() == "" or len(user_var.get()) < 5 or user_var.get().isnumeric():
                    messagebox.showerror("Errore", "Il nome è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if password_var.get() == "" or len(password_var.get()) <= 8:
                    messagebox.showerror("Errore", "La password è obbligatoria e deve essere compilata correttamente.")
                    send = False
                if send == True:
                    Employee.add_employee(dialog, self.db_connection, "Dipendente", nome_var.get(), cognome_var.get(), email_var.get(), user_var.get(), password_var.get(), ruolo_entry.get())
                    Employee.configure_employee_treeview(self.db_connection, self.tree)
            # Crea il pulsante di conferma
            confirm_button = ttk.Button(self.container, text="Conferma", command=get_datas)
            confirm_button.place(x=100, y=275)
    #endregion
    
    #region Gestione Prestiti        
    def manage_loans(self, *args):
        # Ottieni il valore del pulsante selezionato
        loan_list_menu = args[0]
        if loan_list_menu == "Gestione Prestiti":
            Loan.configure_loan_treeview(self.db_connection, self.tree)
        elif loan_list_menu == "Aggiungi Prestito":
            # Crea finestra di dialogo per l'inserimento dei dati
            dialog = tk.Toplevel(self.root)
            dialog.title("Aggiungi Prestito")
            dialog.geometry("390x470")
            dialog.iconbitmap('icon.ico')
            dialog.resizable(width=False, height=False)
            dialog.iconbitmap('icon.ico')
            ##inserire immagine
            img_canvas = tk.Canvas(dialog, width=350, height=120)
            img_canvas.pack()
            img_path = sys.path[0] + "\gui\img3.png"
            img = tk.PhotoImage(file=img_path)  # PIL solution
            img = img.subsample(3) #resize image by factor of 2 = half the original image
            img_canvas.create_image(0,0, anchor=tk.NW, image=img)
            label_img = tk.Label(img_canvas, image=img)
            label_img.image = img
            label_img.pack()
            # contenitore per tutto il contenuto della finestra
            self.container = ttk.Frame(
                dialog, 
                border=5,
                borderwidth=5,
                width=350,
                height=300, 
                relief="sunken"
                )
            self.container.place(x=20, y=150)
            Shadow(self.container, color='#F99B9F', size=1.02, offset_x=-1, offset_y=-1)
            # Crea i campi di input
            user_nome_label = ttk.Label(self.container, text="Nome Utente:")
            user_nome_label.place(x=20, y=20)
            user_nome_var = tk.StringVar()
            user_nome_entry = ttk.Combobox(self.container, values=User.get_users_names(self.db_connection), width=25)
            user_nome_entry.current(1)
            user_nome_entry.place(x=150, y=20)
            book_titolo_label = ttk.Label(self.container, text="Titolo Libro:")
            book_titolo_label.place(x=20, y=60)
            book_titolo_var = tk.StringVar()
            book_titolo_entry = ttk.Combobox(self.container, values=Book.get_books_titles(self.db_connection), width=25)
            book_titolo_entry.current(1)
            book_titolo_entry.place(x=150, y=60)
            data_inizio_label = ttk.Label(self.container, text="Data Inizio:")
            data_inizio_label.place(x=20, y=100)
            data_inizio_var = tk.StringVar()
            data_inizio_entry = DateEntry(self.container, textvariable=data_inizio_var)
            data_inizio_entry.place(x=150, y=100)
            data_fine_label = ttk.Label(self.container, text="Data Fine:")
            data_fine_label.place(x=20, y=140)
            data_fine_var = tk.StringVar()
            data_fine_entry = DateEntry(self.container, textvariable=data_fine_var)
            data_fine_entry.place(x=150, y=140)
            stato_label = ttk.Label(self.container, text="Stato:")
            stato_label.place(x=20, y=180)
            #stato = tk.StringVar(self.container, "In Prestito")
            stato_entry = ttk.Combobox(self.container, values=['In Prestito'], state="readonly", width=17)
            stato_entry.current(0)
            stato_entry.place(x=150, y=180)
            def get_datas():                
                nome = user_nome_entry.get().split(" ")[0]
                cognome = user_nome_entry.get().split(" ")[1]
                Loan.add_loan(dialog, self.db_connection, nome, cognome, book_titolo_entry.get(), data_inizio_entry.get_date(), data_fine_entry.get_date(), stato_entry.get())
                Loan.configure_loan_treeview(self.db_connection, self.tree)
            # Crea il pulsante di conferma
            confirm_button = ttk.Button(self.container, text="Conferma", command=get_datas)
            confirm_button.place(x=110, y=240)
    #endregion
    
    #region Gestione Libri   
    def manage_books(self, *args):
        # Ottieni il valore del pulsante selezionato
        book_list_menu = args[0]
        if book_list_menu == "Gestione Libri":
            Book.configure_book_treeview(self.db_connection, self.tree)
        elif book_list_menu == "Aggiungi Libro":
            # Crea finestra di dialogo per l'inserimento dei dati
            dialog = tk.Toplevel(self.root)
            dialog.title("Aggiungi Libro")
            dialog.geometry("390x500")
            dialog.iconbitmap('icon.ico')
            dialog.resizable(width=False, height=False)
            dialog.iconbitmap('icon.ico')
            ##inserire immagine
            img_canvas = tk.Canvas(dialog, width=350, height=100)
            img_canvas.pack()
            img_path = sys.path[0] + "\gui\img3.png"
            img = tk.PhotoImage(file=img_path)  # PIL solution
            img = img.subsample(3) #resize image by factor of 2 = half the original image
            img_canvas.create_image(0,0, anchor=tk.NW, image=img)
            label_img = tk.Label(img_canvas, image=img)
            label_img.image = img
            label_img.pack()
            # contenitore per tutto il contenuto della finestra
            self.container = ttk.Frame(
                dialog, 
                border=5,
                borderwidth=5,
                width=350,
                height=390, 
                relief="sunken"
                )
            self.container.place(x=20, y=160)
            Shadow(self.container, color='#F99B9F', size=1.02, offset_x=-1, offset_y=-1)
            # Crea i campi di input
            titolo_label = ttk.Label(self.container, text="Titolo:")
            titolo_label.place(x=20, y=20)
            titolo_var = tk.StringVar()
            titolo_entry = ttk.Entry(self.container, textvariable=titolo_var)
            titolo_entry.place(x=150, y=20)
            autore_label = ttk.Label(self.container, text="Autore:")
            autore_label.place(x=20, y=60)
            autore_var = tk.StringVar()
            autore_entry = ttk.Entry(self.container, textvariable=autore_var)
            autore_entry.place(x=150, y=60)
            anno_label = ttk.Label(self.container, text="Anno:")
            anno_label.place(x=20, y=100)
            anno_var = tk.StringVar()
            anno_entry = ttk.Entry(self.container, textvariable=anno_var)
            anno_entry.place(x=150, y=100)
            isbn_label = ttk.Label(self.container, text="ISBN:")
            isbn_label.place(x=20, y=140)
            isbn_var = tk.StringVar()
            isbn_var = random.randint(1000000000000, 9999999999999)
            isbn_entry = ttk.Entry(self.container, textvariable=isbn_var)
            isbn_entry.insert(0, str(isbn_var))
            # set entry in read only mode
            isbn_entry.config(state='readonly')
            isbn_entry.place(x=150, y=140)
            quantita_label = ttk.Label(self.container, text="Quantità Tot:")
            quantita_label.place(x=20, y=180)
            quantita_var = tk.StringVar()
            quantita_entry = ttk.Entry(self.container, textvariable=quantita_var)
            quantita_entry.place(x=150, y=180)
            disponibilita_label = ttk.Label(self.container, text="Disponibilità:")
            disponibilita_label.place(x=20, y=220)
            disponibilita_var = tk.StringVar()
            disponibilita_entry = ttk.Entry(self.container, textvariable=disponibilita_var)
            disponibilita_entry.place(x=150, y=220)
            genere_label = ttk.Label(self.container, text="Genere:")
            genere_label.place(x=20, y=260)
            genere_entry = ttk.Combobox(self.container, values=Category.get_all_categories_names(self.db_connection), state="readonly", width=17)
            genere_entry.current(1)
            genere_entry.place(x=150, y=260)
            def get_datas():
                send = True
                if titolo_var.get() == "" or len(titolo_var.get()) <=2 or titolo_var.get().isnumeric():
                    messagebox.showerror("Errore", "Il titolo è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if autore_var.get() == "" or len(autore_var.get()) <=2 or autore_var.get().isnumeric():
                    messagebox.showerror("Errore", "L'autore è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if len(anno_var.get()) != 4 or anno_var.get().isalpha(): 
                    messagebox.showerror("Errore", "L'anno è obbligatorio e deve essere compilato correttamente.")
                    send = False
                if len(quantita_var.get()) < 1 or quantita_var.get().isalpha():
                    messagebox.showerror("Errore", "La quantità è obbligatoria e deve essere compilata correttamente.")
                    send = False
                if len(disponibilita_var.get()) < 1 or disponibilita_var.get().isalpha():
                    messagebox.showerror("Errore", "La disponibilità è obbligatoria e deve essere compilata correttamente.")
                    send = False
                if send == True:
                    Book.add_book(dialog, self.db_connection, titolo_var.get(), autore_var.get(), isbn_entry.get(), anno_entry.get(), quantita_entry.get(), disponibilita_entry.get(), genere_entry.get())
                    Book.configure_book_treeview(self.db_connection, self.tree)
            # Crea il pulsante di conferma
            confirm_button = ttk.Button(self.container, text="Conferma", command=get_datas)
            confirm_button.place(x=100, y=300)
    #endregion
              
# Questa parte permette di testare il pannello di amministrazione isolatamente
if __name__ == "__main__":
    root = ThemedTk(theme="radiance")  # Usa ThemedTk invece di tk.Tk per temi avanzati
    app = EmployeePanel(root)
    root.mainloop()