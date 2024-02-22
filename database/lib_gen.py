from faker import Faker
from connection import create_db_connection
import random

fake = Faker()

def insert_sample_books(cursor, num_books=100):
    # Seleziona tutte le possibili categorie
    cursor.execute("SELECT ID_Categoria FROM Categorie")
    categories = [row[0] for row in cursor.fetchall()]
    insert_query = """
    INSERT INTO Libri (Titolo, Autore, ISBN, Anno_Pubblicazione, Quantita_Totale, Quantita_Disponibile, ID_Categoria)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """ 
    for _ in range(num_books):
        title = fake.text(max_nb_chars=20)  # Genera un titolo falso
        author = fake.name()  # Genera un nome falso per l'autore
        isbn = fake.isbn13()  # Genera un falso ISBN
        year = fake.year()  # Genera un anno falso
        quantity = fake.random_int(min=1, max=20)  # Genera una quantità falsa di libri
        category_id = random.choice(categories)  # Sceglie un ID di categoria a caso

        # Esegui la query con i dati generati
        cursor.execute(insert_query, (title, author, isbn, year, quantity, quantity, category_id))  
    # Esegue il commit delle transazioni sul database
    db.commit()

def insert_random_categories(cursor, num_categories=20):
    insert_query = "INSERT INTO Categorie (Nome) VALUES (%s);"
    for _ in range(num_categories):
        category_name = fake.word().capitalize()  # Genera un nome di categoria casuale
        cursor.execute(insert_query, (category_name,))
    db.commit()
    
def insert_random_users(cursor, num_users=20):
    # Prendi alcuni ID libri esistenti
    cursor.execute("SELECT ID_Libro FROM Libri ORDER BY RAND() LIMIT %s;", (num_users,))
    book_ids = [row[0] for row in cursor.fetchall()]
    
    # Prendi alcuni ID categorie esistenti
    cursor.execute("SELECT ID_Categoria FROM Categorie ORDER BY RAND() LIMIT %s;", (num_users,))
    category_ids = [row[0] for row in cursor.fetchall()]

    insert_query = """
    INSERT INTO Utenti (Nome, Cognome, Email, ID_Libro, ID_Categoria)
    VALUES (%s, %s, %s, %s, %s);
    """

    for i in range(num_users):
        name = fake.first_name()
        surname = fake.last_name()
        email = fake.email()
        # Assicurati che ci siano abbastanza ID libri e categorie per gli utenti
        book_id = book_ids[i % len(book_ids)]
        category_id = category_ids[i % len(category_ids)]
        cursor.execute(insert_query, (name, surname, email, book_id, category_id))

    db.commit()

def insert_random_employees(cursor, num_employees=20):
    insert_query = "INSERT INTO Dipendenti (Nome, Cognome, Email, Ruolo) VALUES (%s, %s, %s, %s);"
    roles = ['Amministratore', 'Bibliotecario', 'Assistente']

    for _ in range(num_employees):
        name = fake.first_name()
        surname = fake.last_name()
        email = fake.email()
        role = random.choice(roles)
        cursor.execute(insert_query, (name, surname, email, role))

    db.commit()

db = create_db_connection("localhost", "root", "", "librarymanager")    
cursor = db.cursor()
# insert_random_users(cursor)
# insert_random_employees(cursor)
# insert_sample_books(cursor, num_books=100)
insert_random_categories(cursor, num_categories=20)