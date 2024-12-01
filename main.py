from tkinter import Tk
from gui import AntennaControllerApp
from config import WINDOW_TITLE
from error_handler import log_error, show_error_gui

# GUI inicializálás, Exceptio-ok kezelése
def main():

    try:
        # Tkinter ablak inicializálása
        root = Tk()
        root.title(WINDOW_TITLE)

        # GUI betöltése
        app = AntennaControllerApp(root)

        root.protocol("WM_DELETE_WINDOW", app.close)  # Modbus kapcsolat lezárása ablak bezárásakor
        root.mainloop()
    except Exception as e:
        # Hiba naplózása és megjelenítése
        error_message = f"Unexpected error: {str(e)}"
        log_error(error_message)
        show_error_gui(error_message)

if __name__ == "__main__":
    main()
