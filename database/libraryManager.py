from database.queries import _DipendentiDB, _LibraryDB, _PrestitiDB, _UtentiDB, _CategoriaDB

class LibraryManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self._users_db = _UtentiDB(self.db_connection)
        self._books_db = _LibraryDB(self.db_connection)
        self._loans_db = _PrestitiDB(self.db_connection)
        self._employees_db = _DipendentiDB(self.db_connection)
        self._category_db = _CategoriaDB(self.db_connection)

    #region Operazioni sui libri
    def get_books_columns(self):
        return self._books_db._get_books_columns()
    
    def add_book(self, titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria):
        return self._books_db._add_book(titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria)

    def update_book(self, titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria, vecchio_isbn):
        return self._books_db._update_book(titolo, autore, isbn, anno, quantita_tot, quantita_disp, categoria, vecchio_isbn)

    def delete_book(self, isbn_libro):
        return self._books_db._delete_book(isbn_libro)
    
    def get_books_titles(self):
        return self._books_db._get_books_titles()
    
    def get_book_by_title(self, title):
        return self._books_db._get_book_by_title(title)

    def search_book_by_title(self, title):
        return self._books_db._search_book_by_title(title)

    def search_books_by_author(self, author):
        return self._books_db._search_books_by_author(author)

    def search_books_by_isbn(self, isbn):
        return self._books_db._search_books_by_isbn(isbn)
    
    def get_all_books(self):
        return self._books_db._get_all_books()
    #endregion
    
    #region Operazioni sulle categorie
    def get_categories_columns(self):
        return self._category_db._get_categories_columns()
    
    def add_category(self, nome, descrizione):
        self._category_db._add_category(nome, descrizione)

    def get_category(self, id_categoria):
        return self._category_db._get_category(id_categoria)

    def update_category(self, nome, descrizione, vecchio_nome):
        self._category_db._update_category(nome, descrizione, vecchio_nome)

    def delete_category(self, nome):
        self._category_db._delete_category(nome)
        
    def get_categories_by_name(self, nome):
        return self._category_db._get_categories_by_name(nome)
    
    def search_categories_by_description(self, descrizione):
        return self._category_db._search_categories_by_description(descrizione)
    
    def search_categories_by_book(self, id_libro):
        return self._category_db._search_categories_by_book(id_libro)
    
    def get_category(self, id_categoria):
        return self._category_db._get_category(id_categoria)
    
    def get_all_categories(self):
        return self._category_db._get_all_categories()
    
    def get_all_categories_names(self):
        return self._category_db._get_all_categories_names()
    #endregion

    #region Operazioni sugli utenti
    def get_users_columns(self):
        return self._users_db._get_users_columns()
    
    def add_user(self, nome, cognome, email):
        return self._users_db._add_user(nome, cognome, email)

    def update_user(self, nome, cognome, email, data_reg, vecchia_email):
        return self._users_db._update_user(nome, cognome, email, data_reg, vecchia_email)

    def delete_user(self, email):
        return self._users_db._delete_user(email)
    
    def get_users_names(self):
        return self._users_db._get_users_names()
    
    def get_user_id(self, nome, cognome):
        return self._users_db._get_user_id(nome, cognome)

    def search_user_by_name(self, name):
        return self._users_db._search_user_by_name(name)

    def search_users_by_email(self, email):
        return self._users_db._search_users_by_email(email)
    
    def search_users_by_id(self, user_id):
        return self._users_db._search_users_by_id(user_id)
    
    def search_users_by_surname(self, surname):
        return self._users_db._search_users_by_surname(surname)
    
    def search_users_by_name_and_surname(self, name, surname):
        return self._users_db._search_users_by_name_and_surname(name, surname)
    
    def search_users_by_loan(self, loan_id):
        return self._users_db._search_users_by_loan(loan_id)
    
    def search_users_by_loan_history(self, id_libro):
        return self._users_db._search_users_by_loan_history(id_libro)
    
    def get_all_users(self):
        return self._users_db._get_all_users()
    #endregion
    
    #region Operazioni sui prestiti
    def get_loans_columns(self):
        return self._loans_db._get_loans_columns()
    
    def add_loan(self, nome, cognome, book_titolo, data_inizio, data_fine, stato):
        return self._loans_db._add_loan(nome, cognome, book_titolo, data_inizio, data_fine, stato)

    def update_loan(self, id_prestito, data_inizio, data_fine, stato):
        return self._loans_db._update_loan(id_prestito, data_inizio, data_fine, stato)
    
    def delete_loan(self, identificativo):
        return self._loans_db._delete_loan(identificativo)

    def search_active_loans(self):
        return self._loans_db._search_active_loans()

    def search_user_loans_history(self, user_id):
        return self._loans_db._search_user_loans_history(user_id)

    def search_overdue_loans(self, today_date):
        return self._loans_db._search_overdue_loans(today_date)
    
    def get_all_loans(self):
        return self._loans_db._get_all_loans()
    #endregion

    #region Operazioni sui dipendenti
    def get_employees_columns(self):
        return self._employees_db._get_employees_columns()
    
    def hash_password(self, password):
        return self._employees_db._hash_password(password)
    
    def check_employee(self, username, hashed_password):
        return self._employees_db._check_employee(username, hashed_password)
    
    def add_employee(self, user_role, nome, cognome, email, username, password, ruolo):
        hash_password = self.hash_password(password)
        return self._employees_db._add_employee(user_role, nome, cognome, email, username, hash_password, ruolo)
    
    def update_employee(self, user_role, nome, cognome, email, username, ruolo, vecchio_username):
        #hash_password = self.hash_password(password)
        return self._employees_db._update_employee(user_role, nome, cognome, email, username, ruolo, vecchio_username)

    def delete_employee(self, user_role, email, username):
        return self._employees_db._delete_employee_if_admin(user_role,  email, username)

    def promote_employee(self, user_role,  nome, cognome, new_role):
        return self._employees_db._promote_employee(user_role,  nome, cognome, new_role)
    
    def search_employees_by_name(self, name):
        return self._employees_db._search_employees_by_name(name)
    
    def search_employees_by_email(self, email):
        return self._employees_db._search_employees_by_email(email)
    
    def search_employees_by_role(self, role):
        return self._employees_db._search_employees_by_role(role)
    
    def get_all_employees(self, user_role):
        return self._employees_db._get_all_employees(user_role)
    
    def update_password(self, user_role, username, nuova_password):
        return self._employees_db._update_password(user_role, username, nuova_password)
    
    #endregion