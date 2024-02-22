from database.libraryManager import LibraryManager
from tkinter import messagebox

class Category:
    @staticmethod
    def configure_category_treeview(db_connection, tree):
        # Pulisci la Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Ottieni i nomi delle colonne dal database
        category_istance = Category()
        columns = Category.get_category_columns(db_connection)
        # Ottieni i dati dei libri dal database
        category_manager = LibraryManager(db_connection)
        all_categories = category_manager.get_all_categories()
        tree.config(columns=columns)
        # Configura le intestazioni delle colonne
        for col in columns:
            tree.heading(col, text=col.capitalize(), command=lambda _x=col: Category.treeview_sort_column(tree, _x, False))
            tree.column(col, width=100)
            tree.tag_configure('category', background='lightgrey')
        # Inserisci i libri nella Treeview
        for category in all_categories:
            if isinstance(category, dict):
                values = [category[col] for col in tree['columns']]
            else:  # assumendo che category sia una tupla o una lista
                values = category
            tree.insert('', 'end', values=values, tags=('category',))
            
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
        tree.heading(column, command=lambda: Category.treeview_sort_column(tree, column, not reverse)) 
        
    @staticmethod
    def get_category_columns(db_connection):
        istance = LibraryManager(db_connection)
        columns_info = istance.get_categories_columns()
        try:
            column_names = [column[0] for column in columns_info]
            return column_names[1:]
        except Exception as e:
            print(f"Errore durante il recupero dei nomi delle colonne: {e}")
            
    @staticmethod
    def add_category(db_connection, nome, descrizione):
        try:
            # Aggiungi la categoria al database
            category_manager = LibraryManager(db_connection)
            category_manager.add_category(nome, descrizione)
            # Mostra un messaggio di conferma
            messagebox.showinfo("Categoria", "Categoria aggiunta con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta della categoria: {e}")
            
    @staticmethod
    def delete_category(dialog, db_connection, values):
        try:
            # Elimina la categoria dal database
            category_manager = LibraryManager(db_connection)
            nome, _ = values
            category_manager.delete_category(nome)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Categoria", "Categoria eliminata con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'eliminazione della categoria: forse ci sono libri associati a questa categoria.")
            
    @staticmethod
    def update_category(dialog, db_connection, new_values, old_values):
        try:
            # Aggiorna la categoria nel database
            category_manager = LibraryManager(db_connection)
            nome, descrizione = new_values
            vecchio_nome, _ = old_values
            category_manager.update_category(nome, descrizione, vecchio_nome)
            # Mostra un messaggio di conferma
            dialog.destroy()
            messagebox.showinfo("Categoria", "Categoria aggiornata con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiornamento della categoria: {e}")
            
    @staticmethod
    def get_all_categories_names(db_connection):
        try:
            # Ottieni i nomi delle categorie dal database
            category_manager = LibraryManager(db_connection)
            all_categories_names = category_manager.get_all_categories_names()
            #[item for result in combo_input() for item in result if item]
            all_categories_names = [item for category in all_categories_names for item in category if item]
            return all_categories_names
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il recupero delle categorie: {e}")