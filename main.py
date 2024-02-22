import sys,os
sys.path.insert(0, os.getcwd())
from gui.login_window import LoginWindow
from database.connection import create_db_connection

# La funzione main che avvia l'applicazione
def main():
    db_connection = create_db_connection()
    app = LoginWindow(db_connection)
    app.mainloop()

if __name__ == '__main__':
    main()