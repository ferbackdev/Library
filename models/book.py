from database.libraryManager import LibraryManager
from tkinter import messagebox

class Book:
    def __init__(self):
        pass
        
    @staticmethod
    def configure_book_treeview(db_connection, tree):
        # Pulisci la Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Ottieni i nomi delle colonne dal database
        book_istance = Book()
        columns = Book.get_book_columns(db_connection)
        # Ottieni i dati dei libri dal database
        book_manager = LibraryManager(db_connection)
        all_books = book_manager.get_all_books()
        tree.config(columns=columns)
        # Configura le intestazioni delle colonne
        for col in columns:
            tree.heading(col, text=col.capitalize(), command=lambda _x=col: Book.treeview_sort_column(tree, _x, False))
            tree.column(col, width=100)
            tree.tag_configure('book')
        # Inserisci i libri nella Treeview
        for book in all_books:
            if isinstance(book, dict):
                values = [book[col] for col in tree['columns']]
            else:  # assumendo che book sia una tupla o una lista
                values = book
            tree.insert('', 'end', values=values, tags=('book',))
            
    @staticmethod       
    def treeview_sort_column(tree, column, reverse): # Treeview, colonna, ordine inverso
        #use column index to sort by integer
        get_index = tree.heading(column)['text']
        lista = [(tree.set(key, column), key) for key in tree.get_children('')] 
        #converti stinghe in minuscolo
        lista = [(x[0].lower(), x[1]) for x in lista]
        # Ordina la lista in base al valore, in base al tipo di dati della colonna e in base all'ordine inverso. 
        # Se il tipo di dati è un intero, ordina in base al valore intero e non alla stringa. 
        lista.sort(reverse=reverse)
        try:
            lista.sort(key=lambda t: int(t[0]))
        except Exception:
            pass
        for index, (val, k) in enumerate(lista):
            tree.move(k, '', index)
        tree.heading(column, command=lambda: Book.treeview_sort_column(tree, column, not reverse))  
        
    @staticmethod
    def get_book_columns(db_connection):
        istance = LibraryManager(db_connection)
        columns_info = istance.get_books_columns()
        try:
            column_names = [column[0] for column in columns_info]
            # cambiare nome tabella da ID_Categoria a Nome Categoria
            column_names = []
            for column in columns_info:
                if column[0] == "ID_Categoria":
                    column_names.append("Categoria")  # Sostituisci con il nome più descrittivo
                else:
                    column_names.append(column[0])
            return column_names[1:]
        except Exception as e:
            print(f"Errore durante il recupero dei nomi delle colonne: {e}")
            
    @staticmethod
    def update_book(dialog, db_connection, new_values, value):
        try:
            #descompatta args
            titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria = new_values 
            _, _, vecchio_isbn, _, _, _, _ = value
            # Aggiorna il libro nel database
            book_manager = LibraryManager(db_connection)
            book_manager.update_book(titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria, vecchio_isbn)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Libro", "Libro aggiornato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiornamento del libro: {e}")
            
    @staticmethod
    def add_book(dialog, db_connection, titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria):
        try:
            # Aggiungi il libro al database
            book_manager = LibraryManager(db_connection)
            book_manager.add_book(titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Libro", "Libro aggiunto con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta del libro: {e}")
            
    @staticmethod
    def delete_book(dialog, db_connection, values):
        try:
            # Elimina il libro dal database
            book_manager = LibraryManager(db_connection)
            _, _, isbn_libro, _, _, _, _ = values
            book_manager.delete_book(isbn_libro)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Libro", "Libro eliminato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'eliminazione del libro: {e}")
            
    @staticmethod
    def get_books_titles(db_connection):
        try:
            # Ottieni i titoli dei libri dal database
            book_manager = LibraryManager(db_connection)
            books_titles = book_manager.get_books_titles()
            all_books_titles = [item for title in books_titles for item in title if item]
            return all_books_titles
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il recupero dei titoli dei libri: {e}")
            
    @staticmethod
    def get_book_by_title(db_connection, title):
        try:
            # Ottieni il libro dal database
            book_manager = LibraryManager(db_connection)
            book_id = book_manager.get_book_by_title(title)
            return book_id
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il recupero del libro: {e}")
 
            
    