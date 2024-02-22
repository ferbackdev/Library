from database.libraryManager import LibraryManager
from tkinter import messagebox

class Employee:
    @staticmethod   
    def configure_employee_treeview(db_connection, tree):
        # Pulisci la Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Ottieni i nomi delle colonne dal database
        employee_istance = Employee()
        columns = Employee.get_employee_columns(db_connection)
        # Ottieni i dati dei libri dal database
        employee_manager = LibraryManager(db_connection)
        all_employees = employee_manager.get_all_employees(user_role="Admin")
        tree.config(columns=columns)
        # Configura le intestazioni delle colonne
        for col in columns:
            tree.heading(col, text=col.capitalize(), command=lambda _x=col: Employee.treeview_sort_column(tree, _x, False))
            tree.column(col, width=100)
            tree.tag_configure('employee', background='lightgrey')
        # Inserisci i libri nella Treeview
        for employee in all_employees:
            if isinstance(employee, dict):
                values = [employee[col] for col in tree['columns']]
            else:  # assumendo che employee sia una tupla o una lista
                values = employee
            tree.insert('', 'end', values=values, tags=('employee',))
            
    @staticmethod        
    def treeview_sort_column( tree, column, reverse): # Treeview, colonna, ordine inverso
        #use column index to sort by integer
        get_index = tree.heading(column)['text']
        lista = [(tree.set(key, column), key) for key in tree.get_children('')]  
        #converti stinghe in minuscolo
        lista = [(x[0].lower(), x[1]) for x in lista]
        lista.sort(reverse=reverse)
        try:
            lista.sort(key=lambda t: int(t[0]))
        except Exception:
            pass
        for index, (val, k) in enumerate(lista):
            tree.move(k, '', index)
        tree.heading(column, command=lambda: Employee.treeview_sort_column(tree, column, not reverse))  

        

    @staticmethod
    def get_employee_columns(db_connection):
        istance = LibraryManager(db_connection)
        columns_info = istance.get_employees_columns()
        try: 
            # Estrai solo i nomi delle colonne, che si trovano nella prima posizione di ogni tupla
            column_names = [column[0] for column in columns_info]
            return column_names[1:]
        except Exception as e:
            print(f"Errore durante il recupero dei nomi delle colonne: {e}")
            
    @staticmethod
    def add_employee(dialog, db_connection, user_role, nome, cognome, email, username, password, ruolo):
        try:
            # Aggiungi l'utente al database
            employee_manager = LibraryManager(db_connection)
            employee_manager.add_employee(user_role, nome, cognome, username, email, password, ruolo)
            # Mostra un messaggio di conferma
            messagebox.showinfo("Dipendente", "Dipendente aggiunto con successo.")
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta del dipendente: {e}")
    
    @staticmethod
    def delete_employee(dialog, db_connection, user_role, values):
        try:
            # Elimina il dipendente dal database
            employee_manager = LibraryManager(db_connection)
            _, _, email, username, _, _, _ = values
            employee_manager.delete_employee(user_role, email, username)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Dipendente", "Dipendente eliminato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'eliminazione del dipendente: {e}")
            
    @staticmethod
    def update_employee(dialog, db_connection, user_role, new_values, old_values):
        try:
            # Aggiorna il dipendente nel database
            employee_manager = LibraryManager(db_connection)
            nome, cognome, email, username, _, ruolo, _ = new_values
            _, _, _, vecchio_username, _, _, _ = old_values
            employee_manager.update_employee(user_role, nome, cognome, email, username, ruolo, vecchio_username)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Dipendente", "Dipendente aggiornato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiornamento del dipendente: {e}")