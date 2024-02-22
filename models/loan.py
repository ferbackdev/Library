from database.libraryManager import LibraryManager
from tkinter import messagebox

class Loan:
    @staticmethod
    def configure_loan_treeview(db_connection,tree):
        # Pulisci la Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Ottieni i nomi delle colonne dal database
        loan_istance = Loan()
        columns = Loan.get_loan_columns(db_connection)
        # Ottieni i dati dei libri dal database
        loan_manager = LibraryManager(db_connection)
        all_loans = loan_manager.get_all_loans()
        tree.config(columns=columns)
        # Configura le intestazioni delle colonne
        for col in columns:
            tree.heading(col, text=col.capitalize(), command=lambda _x=col: Loan.treeview_sort_column(tree, _x, False))
            tree.column(col, width=100)
            tree.tag_configure('loan', background='lightgrey')
        # Inserisci i libri nella Treeview
        for loan in all_loans:
            if isinstance(loan, dict):
                values = [loan[col] for col in tree['columns']]
            else:  # assumendo che book sia una tupla o una lista
                values = loan
            tree.insert('', 'end', values=values, tags=('loan',))
        tree.update() # Aggiorna la Treeview
        return True
    
            
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
        tree.heading(column, command=lambda: Loan.treeview_sort_column(tree, column, not reverse)) 

    @staticmethod
    def get_loan_columns(db_connection):
        istance = LibraryManager(db_connection)
        columns_info = istance.get_loans_columns()
        try:
            # Sostituisci i nomi delle colonne foreign key con i nomi più descrittivi
            column_names = []
            for column in columns_info:
                if column[0] == "ID_Libro":
                    column_names.append("Titolo Libro")  # Sostituisci con il nome più descrittivo
                elif column[0] == "ID_Utente":
                    column_names.append("Utente")  # Sostituisci con il nome più descrittivo
                elif column[0] == "ID_Prestito":
                    column_names.append("Identificato Prestito")  # Sostituisci con il nome più descrittivo
                else:
                    column_names.append(column[0])  # Mantieni il nome originale per le altre colonne
            return column_names
        except Exception as e:
            print(f"Errore durante il recupero dei nomi delle colonne: {e}")
            
    @staticmethod
    def add_loan(dialog, db_connection, nome, cognome, book_titolo, data_inizio, data_fine, stato):
        try:
            # Aggiungi il prestito al database
            loan_manager = LibraryManager(db_connection)
            loan_manager.add_loan(nome, cognome, book_titolo, data_inizio, data_fine, stato)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Prestito", "Prestito aggiunto con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta del prestito: {e}")
            
    @staticmethod
    def delete_loan(dialog, db_connection, values):
        try:
            # Elimina il prestito dal database
            loan_manager = LibraryManager(db_connection)
            identificativo, _, _, _, _, _ = values
            loan_manager.delete_loan(identificativo)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Prestito", "Prestito eliminato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'eliminazione del prestito: {e}")
            
    @staticmethod
    def update_loan(dialog, db_connection, new_values):
        try:
            # Aggiorna il prestito nel database
            loan_manager = LibraryManager(db_connection)
            id_prestito, _, _, data_inizio, data_fine, stato = new_values
            loan_manager.update_loan(id_prestito, data_inizio, data_fine, stato)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Prestito", "Prestito aggiornato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiornamento del prestito: {e}")