from database.libraryManager import LibraryManager
from tkinter import messagebox

class User:
    @staticmethod
    def configure_user_treeview(db_connection, tree):
        # Pulisci la Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Ottieni i nomi delle colonne dal database
        user_istance = User()
        columns = User.get_user_columns(db_connection)
        # Ottieni i dati dei libri dal database
        user_manager = LibraryManager(db_connection)
        all_users = user_manager.get_all_users()
        tree.config(columns=columns)
        # Configura le intestazioni delle colonne
        for col in columns:
            tree.heading(col, text=col.capitalize(), command=lambda _x=col: User.treeview_sort_column(tree, _x, False))
            tree.column(col, width=100)
            tree.tag_configure('user', background='lightgrey')
        # Inserisci i libri nella Treeview
        for user in all_users:
            if isinstance(user, dict):
                values = [user[col] for col in tree['columns']]
            else:  # assumendo che book sia una tupla o una lista
                values = user
            tree.insert('', 'end', values=values, tags=('user',))

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
        tree.heading(column, command=lambda: User.treeview_sort_column(tree, column, not reverse)) 

    @staticmethod
    def get_user_columns(db_connection):
        istance = LibraryManager(db_connection)
        columns_info = istance.get_users_columns()
        try:
            column_names = [column[0] for column in columns_info]
            return column_names[1:]
        except Exception as e:
            print(f"Errore durante il recupero dei nomi delle colonne: {e}")
    
    @staticmethod        
    def add_user(dialog, db_connection, nome, cognome, email):
        try:
            # Aggiungi l'utente al database
            user_manager = LibraryManager(db_connection)
            user_manager.add_user(nome, cognome, email)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Utente", "Utente aggiunto con successo.")    
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta dell'utente: {e}")
            
    @staticmethod
    def delete_user(dialog, db_connection, values):
        try:
            # Elimina l'utente dal database
            user_manager = LibraryManager(db_connection)
            _, _, email, _ = values
            user_manager.delete_user(email)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Utente", "Utente eliminato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'eliminazione dell'utente: {e}")
            
    @staticmethod
    def update_user(dialog, db_connection, new_values, old_values):
        try:
            # Aggiorna l'utente nel database
            user_manager = LibraryManager(db_connection)
            nome, cognome, email, data_reg = new_values 
            vecchio_nome, vecchio_cognome, vecchia_email, _ = old_values
            user_manager.update_user(nome, cognome, email, data_reg, vecchia_email)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Utente", "Utente aggiornato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiornamento dell'utente: {e}")
            
    @staticmethod
    def get_user_id(db_connection, nome, cognome):
        try:
            # Cerca l'utente nel database
            user_manager = LibraryManager(db_connection)
            user = user_manager.get_user_id(nome, cognome)
            # Mostra un messaggio di conferma
            messagebox.showinfo("Utente", "Utente trovato con successo.")
            return user
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la ricerca dell'utente: {e}")
            
    @staticmethod
    def get_users_names(db_connection):
        try:
            # Ottieni i nomi degli utenti dal database
            user_manager = LibraryManager(db_connection)
            users_names = user_manager.get_users_names()
            return users_names
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il recupero dei nomi degli utenti: {e}")
            