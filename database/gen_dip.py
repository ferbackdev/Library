import random
import bcrypt

# Funzione per generare una password casuale
def generate_random_password(length=10):
    # Genera una password casuale alfanumerica
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = ''.join(random.choice(alphabet) for i in range(length))
    return password.encode('utf-8')

# Funzione per criptare una password
def hash_password(password):
    # Genera un sale e cripta la password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode('utf-8')

# Lista per contenere i dipendenti
dipendenti = []

# Generare e criptare 5 password per 5 dipendenti
for i in range(1, 12):
    random_password = generate_random_password()
    hashed_password = hash_password(random_password)
    print(f'Nome{i}', f'Cognome{i}', f'email{i}@example.com', random_password, 'Dipendente')
    dipendenti.append((f'Nome{i}', f'Cognome{i}', f'email{i}@example.com', hashed_password, 'Dipendente'))

for i in range(1, 2):
    random_password = generate_random_password()
    hashed_password = hash_password(random_password)
    print(f'Nome{i}', f'Cognome{i}', f'email{i}@example.com', random_password, 'Admin')
    dipendenti.append((f'Nome{i}', f'Cognome{i}', f'email{i}@example.com', hashed_password, 'Admin'))

# Stampa le query SQL per ciascun dipendente
for nome, cognome, email, password, ruolo in dipendenti:
    print(f"INSERT INTO Dipendenti (Nome, Cognome, Email, Password, Ruolo) VALUES ('{nome}', '{cognome}', '{email}', '{password}', '{ruolo}');")
