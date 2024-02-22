import hashlib

class _LibraryDB:
    def __init__(self, db_connection):
        self._connection = db_connection
        self._cursor = self._connection.cursor()
        
    #region LIBRI
    # estrarre colonne
    def _get_books_columns(self):
        query = "SHOW COLUMNS FROM Libri"
        self._cursor.execute(query)
        columns_info = self._cursor.fetchall()
        return columns_info
    
    # inserire nuovo libro
    def _add_book(self, titolo, autore, isbn, anno_pubblicazione, quantita_totale, quantita_disp, categoria):
        self._cursor.execute("SELECT ID_Categoria FROM Categorie WHERE Nome = %s", (categoria,))
        categoria_id = self._cursor.fetchone()[0] # Fetchone returns a tuple, so we need to get the first element
        query = """
        INSERT INTO Libri (Titolo, Autore, ISBN, Anno_Pubblicazione, Quantita_Totale, Quantita_Disponibile, ID_Categoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self._cursor.execute(query, (titolo, autore, isbn, anno_pubblicazione, quantita_totale, quantita_disp, categoria_id))
        self._connection.commit()

    def _update_book(self, titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria, vecchio_isbn):
        query = """
        UPDATE Libri SET 
        Titolo = %s, Autore = %s, ISBN = %s, Anno_Pubblicazione = %s, Quantita_Totale = %s, Quantita_Disponibile = %s, 
        ID_Categoria = (SELECT ID_Categoria FROM Categorie WHERE Nome = %s) 
        WHERE ISBN = %s
        """
        self._cursor.execute(query, (titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria, vecchio_isbn))
        self._connection.commit()
        
    # aggiornare la quantita di un libro
    def _update_book_quantity(self, id_libro, quantita_aggiuntiva):
        query = """
        UPDATE Libri
        SET Quantita_Totale = Quantita_Totale + %s,
            Quantita_Disponibile = Quantita_Disponibile + %s
        WHERE ID_Libro = %s
        """
        self._cursor.execute(query, (quantita_aggiuntiva, quantita_aggiuntiva, id_libro))
        self._connection.commit()

    # rimuovere un libro
    def _delete_book(self, isbn_libro):
        query = "DELETE FROM Libri WHERE ID_Libro = (SELECT ID_Libro FROM Libri WHERE ISBN = %s)"
        self._cursor.execute(query, (isbn_libro,))
        self._connection.commit()
        
    # selezionare libri(per titolo)
    def _get_books_titles(self):
        query = "SELECT Titolo FROM Libri"
        self._cursor.execute(query)
        return list(self._cursor.fetchall())
    
    # selezionare libro per titolo
    def _get_book_by_title(self, titolo):
        query = "SELECT ID_Libro FROM Libri WHERE Titolo = %s"
        self._cursor.execute(query, (titolo,))
        return self._cursor.fetchone()
    
    def _search_books_by_title(self, title):
        query = "SELECT * FROM Libri WHERE Titolo LIKE %s"
        self._cursor.execute(query, ('%' + title + '%',))
        return self._cursor.fetchall()

    def _search_books_by_author(self, author):
        query = "SELECT * FROM Libri WHERE Autore LIKE %s"
        self._cursor.execute(query, ('%' + author + '%',))
        return self._cursor.fetchall()

    def _search_books_by_isbn(self, isbn):
        query = """SELECT Titolo, Autore, ISBN, Anno_Pubblicazione, Quantita_Totale, Quantita_Disponibile, Nome 
                    FROM Libri 
                    INNER JOIN Categorie ON Libri.ID_Categoria = Categorie.ID_Categoria
                    WHERE ISBN = %s"""
        self._cursor.execute(query, (isbn,))
        return self._cursor.fetchall()
    
    def _get_all_books(self):
        query = """SELECT Titolo, Autore, ISBN, Anno_Pubblicazione, Quantita_Totale, Quantita_Disponibile, Nome 
                FROM Libri
                INNER JOIN Categorie ON Libri.ID_Categoria = Categorie.ID_Categoria"""
        self._cursor.execute(query)
        results = self._cursor.fetchall()
        return results
    #endregion

class _CategoriaDB:
    def __init__(self, db_connection):
        self._connection = db_connection
        self._cursor = self._connection.cursor()
        
    #region Categorie    
    def _get_categories_columns(self):
        query = "SHOW COLUMNS FROM Categorie"
        self._cursor.execute(query)
        columns_info = self._cursor.fetchall()
        return columns_info
    
    def _add_category(self, nome, descrizione):
        query = "INSERT INTO Categorie (Nome, Descrizione) VALUES (%s, %s)"
        self._cursor.execute(query, (nome, descrizione))
        self._connection.commit()
        #return self._cursor.lastrowid

    def _get_category(self, id_categoria):
        query = "SELECT * FROM Categorie WHERE ID_Categoria = %s"
        self._cursor.execute(query, (id_categoria,))
        return self._cursor.fetchone()

    def _update_category(self, nome, descrizione, vecchio_nome):
        query = "UPDATE Categorie SET Nome = %s, Descrizione = %s WHERE ID_Categoria = (SELECT ID_Categoria FROM Categorie WHERE Nome = %s)"
        self._cursor.execute(query, (nome, descrizione, vecchio_nome))
        self._connection.commit()
        
    def _delete_category(self, nome):
        query = "DELETE FROM Categorie WHERE ID_Categoria = (SELECT ID_Categoria FROM Categorie WHERE Nome = %s)"
        self._cursor.execute(query, (nome,))
        self._connection.commit()
        
    def _search_categories_by_name(self, nome):
        query = "SELECT * FROM Categorie WHERE Nome LIKE %s"
        self._cursor.execute(query, ('%' + nome + '%',))
        return self._cursor.fetchall()
    
    def _search_categories_by_description(self, descrizione):
        query = "SELECT * FROM Categorie WHERE Descrizione LIKE %s"
        self._cursor.execute(query, ('%' + descrizione + '%',))
        return self._cursor.fetchall()
    
    def _search_categories_by_book(self, id_libro):
        query = "SELECT * FROM Categorie WHERE ID_Categoria = (SELECT ID_Categoria FROM Libri WHERE ID_Libro = %s)"
        self._cursor.execute(query, (id_libro,))
        return self._cursor.fetchall()
     
    def _get_all_categories(self):
        query = "SELECT Nome, Descrizione FROM Categorie"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def _get_all_categories_names(self):
        query = "SELECT Nome FROM Categorie"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    #endregion

class _UtentiDB():
    def __init__(self, db_connection):
        self._connection = db_connection
        self._cursor = self._connection.cursor()
    
    #region Utenti
    def _get_users_columns(self):
        query = "SHOW COLUMNS FROM Utenti"
        self._cursor.execute(query)
        columns_info = self._cursor.fetchall()
        return columns_info
    
    # inserire nuovo utente
    def _add_user(self, nome, cognome, email):
        query = """
        INSERT INTO Utenti (Nome, Cognome, Email, Data_Registrazione)
        VALUES (%s, %s, %s, NOW())
        """
        self._cursor.execute(query, (nome, cognome, email))
        self._connection.commit()
        
    # aggiornare un utente
    def _update_user(self, nome, cognome, email, data_reg, vecchia_email):
        query = """
        UPDATE Utenti
        SET Nome = %s, Cognome = %s, Email = %s, Data_Registrazione = %s
        WHERE ID_Utente = (SELECT ID_Utente FROM Utenti WHERE Email = %s)
        """
        self._cursor.execute(query, (nome, cognome, email, data_reg, vecchia_email))
        self._connection.commit()
        
    #rimuovere un utente
    def _delete_user(self, email):
        query = "DELETE FROM Utenti WHERE ID_Utente = (SELECT ID_Utente FROM Utenti WHERE Email = %s)"
        self._cursor.execute(query, (email,))
        self._connection.commit()
    
    def _get_users_names(self):
        query = "SELECT Nome, Cognome FROM Utenti"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def _get_user_id(self, nome, cognome):
        query = "SELECT ID_Utente FROM Utenti WHERE Nome = %s AND Cognome = %s"
        self._cursor.execute(query, (nome, cognome))
        return self._cursor.fetchone()
               
    def _search_user_by_name(self, name, cognome):
        query = "SELECT ID_Utenti FROM Utenti WHERE Nome = %s AND Cognome = %s"
        self._cursor.execute(query, (name, cognome))
        return self._cursor.fetchone()

    def _search_users_by_email(self, email):
        query = "SELECT * FROM Utenti WHERE Email = %s"
        self._cursor.execute(query, (email,))
        return self._cursor.fetchall()
    
    def _search_users_by_id(self, id_utente):
        query = "SELECT * FROM Utenti WHERE ID_Utente = %s"
        self._cursor.execute(query, (id_utente,))
        return self._cursor.fetchall()
    
    def _search_users_by_loan(self, id_prestito):
        query = "SELECT * FROM Utenti WHERE ID_Utente = (SELECT ID_Utente FROM Prestiti WHERE ID_Prestito = %s)"
        self._cursor.execute(query, (id_prestito,))
        return self._cursor.fetchall()
    
    def _search_users_by_loan_history(self, id_libro):
        query = "SELECT Nome, Cognome, Email, Data_Registrazione FROM Utenti WHERE ID_Utente = (SELECT ID_Utente FROM Prestiti WHERE ID_Libro = %s)"
        self._cursor.execute(query, (id_libro,))
        return self._cursor.fetchall()
    
    def _get_all_users(self):
        query = "SELECT Nome, Cognome, Email, Data_Registrazione FROM Utenti"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    #endregion

class _PrestitiDB():
    def __init__(self, db_connection):
        self._connection = db_connection
        self._cursor = self._connection.cursor()
        
    #region Prestiti
    def _get_loans_columns(self):
        # le colonne id_utente e id_libro devono essere sostuite con la colonna nome_utente e titolo_libro
        query = "SHOW COLUMNS FROM Prestiti"
        self._cursor.execute(query)
        columns_info = self._cursor.fetchall()
        return columns_info
    
    #Creare un nuovo prestito
    def _add_loan(self, nome, cognome, book_titolo, data_inizio, data_fine, stato):
        # Assicurati che il libro sia disponibile prima di aggiungere un prestito
        query = """
        SELECT Quantita_Disponibile FROM Libri
        WHERE ID_Libro = (SELECT ID_Libro FROM Libri WHERE Titolo = %s)
        """
        self._cursor.execute(query, (book_titolo,))
        quantita_disp = self._cursor.fetchone()[0]
        if quantita_disp == 0:
            raise ValueError("Il libro selezionato non è disponibile.")
        else:
            # Aggiungi il prestito al database
            query = """
            INSERT INTO Prestiti (ID_Utente, ID_Libro, Data_Inizio, Data_Fine, Stato)
            VALUES ((SELECT ID_Utente FROM Utenti WHERE Nome = %s AND Cognome = %s), (SELECT ID_Libro FROM Libri WHERE Titolo = %s), %s, %s, %s)
            """
            self._cursor.execute(query, (nome, cognome, book_titolo, data_inizio, data_fine, stato))
            self._connection.commit()
            # Aggiorna la quantità disponibile del libro
            query = """
            UPDATE Libri
            SET Quantita_Disponibile = Quantita_Disponibile - 1
            WHERE ID_Libro = (SELECT ID_Libro FROM Libri WHERE Titolo = %s)
            """
            self._cursor.execute(query, (book_titolo,))
            self._connection.commit()
        
     # Aggiornare un prestito (es: restituzione di un libro)
    def _update_loan(self, id_prestito, data_inizio, data_fine, stato):
        query = """
        UPDATE Prestiti
        SET Data_Inizio = %s, Data_Fine = %s, Stato = "%s" WHERE ID_Prestito = %s
        """
        self._cursor.execute(query, (data_inizio, data_fine, stato, id_prestito))
        self._connection.commit()
        if stato == "Restituito":
            print("Libro restituito con successo.")
            # Aggiorna la quantità disponibile del libro
            query = """
            UPDATE Libri
            SET Quantita_Disponibile = Quantita_Disponibile + 1
            WHERE ID_Libro = (SELECT ID_Libro FROM Prestiti WHERE ID_Prestito = %s)
            """
            self._cursor.execute(query, (id_prestito,))
            self._connection.commit()

    def _delete_loan(self, id_prestito):
        query = "DELETE FROM Prestiti WHERE ID_Prestito = %s"
        self._cursor.execute(query, (id_prestito,))
        self._connection.commit()
        
    def _search_active_loans(self):
        query = "SELECT * FROM Prestiti WHERE Restituito = FALSE"
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def _search_user_loans_history(self,id_utente):
        query = "SELECT * FROM Prestiti WHERE ID_Utente = %s"
        self._cursor.execute(query, (id_utente,))
        return self._cursor.fetchall()

    def _search_overdue_loans(self, today_date):
        query = "SELECT * FROM Prestiti WHERE Data_Fine < %s AND Restituito = FALSE"
        self._cursor.execute(query, (today_date,))
        return self._cursor.fetchall()
    
    def _get_all_loans(self):
        # unire il nome e il cognome dell'utente e creo un alias con CONCAT
        # Seleziono titolo dalla tabella libri e creo un alias con AS
        # Uso INNER JOIN per unire le tabelle prestiti, utenti e libri
        query = """
        SELECT
            Prestiti.ID_Prestito,
            CONCAT(Utenti.Nome, ' ', Utenti.Cognome) AS Utente, 
            Libri.Titolo AS Titolo_Libro, 
            Prestiti.Data_Inizio,
            Prestiti.Data_Fine,
            Prestiti.Stato
        FROM 
            Prestiti
        INNER JOIN 
            Utenti ON Prestiti.ID_Utente = Utenti.ID_Utente
        INNER JOIN 
            Libri ON Prestiti.ID_Libro = Libri.ID_Libro
        """
        self._cursor.execute(query)
        return self._cursor.fetchall()
    #endregion
      
class _DipendentiDB():
    def __init__(self, db_connection):
        self._connection = db_connection
        self._cursor = self._connection.cursor()
      
    #region Dipendenti  
    def _get_employees_columns(self):
        query = "SHOW COLUMNS FROM Dipendenti"
        self._cursor.execute(query)
        columns_info = self._cursor.fetchall()
        return columns_info
    
    def _hash_password(self,password):
        # Utilizzare il metodo di hashing preferito
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # check login dipendente
    def _check_employee(self, username, hashed_password):
        self._cursor.execute(
        "SELECT Ruolo FROM dipendenti WHERE username = %s AND password = %s",
        (username, hashed_password)
        )
        result = self._cursor.fetchone()
        print(result)
        return result[0]

        
    # Aggiungere un nuovo dipendente
    def _add_employee(self, user_role, nome, cognome, email, username, password, ruolo):
        if user_role == 'Admin':
            query = """
            INSERT INTO Dipendenti (Nome, Cognome, Email, Username, Password, Ruolo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Assicurati di criptare la password prima di passarla a questa funzione
            self._cursor.execute(query, (nome, cognome, email, username, password, ruolo))
            self._connection.commit()
        else:
            raise PermissionError("Operazione non autorizzata: solo gli amministratori possono rimuovere dipendenti.")

    def _update_employee(self, user_role, nome, cognome, email, username, ruolo, vecchio_username):
        if user_role == 'Admin':
            query = """
            UPDATE Dipendenti
            SET Nome = %s, Cognome = %s, Email = %s, Username = %s, Ruolo = %s
            WHERE ID_Dipendente = (SELECT ID_Dipendente FROM Dipendenti WHERE Username = %s)
            """
            self._cursor.execute(query, (nome, cognome, email, username, ruolo, vecchio_username))
            self._connection.commit()
        else:
            raise PermissionError("Operazione non autorizzata: solo gli amministratori possono rimuovere dipendenti.")

    # Rimuovere un dipendente
    def _delete_employee_if_admin(self, user_role, email, username):
        if user_role == 'Admin':
            query = "DELETE FROM Dipendenti WHERE ID_Dipendente = (SELECT ID_Dipendente FROM Dipendenti WHERE Email = %s AND Username = %s)"
            self._cursor.execute(query, (email, username))
            self._connection.commit()
        else:
            raise PermissionError("Operazione non autorizzata: solo gli amministratori possono rimuovere dipendenti.")

    # Promuovere un dipendente
    def _promote_employee(self, user_role, nome, cognome, nuovo_ruolo):
        if user_role == 'Admin':
            query = """
            UPDATE Dipendenti
            SET Ruolo = %s
            WHERE ID_Dipendente = (SELECT ID_Dipendente FROM Dipendenti WHERE Nome = %s AND Cognome = %s)
            """
            self._cursor.execute(query, (nuovo_ruolo, nome, cognome))
        else:
            raise PermissionError("Operazione non autorizzata: solo gli amministratori possono rimuovere dipendenti.")
    
    def _update_password(self, user_role, nome, cognome, nuova_password):
        if user_role == 'Admin':
            query = """
            UPDATE Dipendenti
            SET Password = %s
            WHERE ID_Dipendente = (SELECT ID_Dipendente FROM Dipendenti WHERE Nome = %s AND Cognome = %s)
            """
            self._cursor.execute(query, (nuova_password, nome, cognome))
        else:
            raise PermissionError("Operazione non autorizzata: solo gli amministratori possono modificare dipendenti.")
        
    def _get_all_employees(self, user_role):
        if user_role == 'Admin':
            query = "SELECT Nome, Cognome, Email, Username, Password, Ruolo, Data_Assunzione FROM Dipendenti"
            self._cursor.execute(query)
            results = self._cursor.fetchall()
            return results
        else:
            query = "SELECT Nome, Cognome, Email, Ruolo, Data_Assunzione FROM Dipendenti"
            self._cursor.execute(query)
            results = self._cursor.fetchall()
            return results

    def _search_employees_by_name(self, name):
        query = "SELECT * FROM Dipendenti WHERE Nome LIKE %s OR Cognome LIKE %s"
        self._cursor.execute(query, ('%' + name + '%', '%' + name + '%'))
        return self._cursor.fetchall()
    
    def _search_employees_by_email(self, email):
        query = "SELECT * FROM Dipendenti WHERE Email = %s"
        self._cursor.execute(query, (email,))
        return self._cursor.fetchall()
    
    def _search_employees_by_role(self, role):
        query = "SELECT * FROM Dipendenti WHERE Ruolo = %s"
        self._cursor.execute(query, (role,))
        return self._cursor.fetchall()
    #endregion