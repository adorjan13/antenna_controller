import logging
from tkinter import messagebox

# Logging konfiguráció
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(message):

    logging.error(message)

def show_error_gui(message, root=None):

    if root:
        messagebox.showerror("Error", message, parent=root)
    else:
        messagebox.showerror("Error", message)
