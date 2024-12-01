import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from threading import Thread
from time import sleep
from visualization import calculate_coordinates, azimuth_elevation_to_steps, plot_globe
from modbus_handler import ModbusHandler
from config import SERIAL_PORT, BAUDRATE, TIMEOUT, HOME_AZIMUTH, HOME_ELEVATION

class AntennaControllerApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Antenna Controller")

        # Modbus kezelő inicializálás
        self.modbus_handler = ModbusHandler(SERIAL_PORT, BAUDRATE, TIMEOUT)

        # Alapértelmezett pozíciók
        self.azimuth = 0
        self.elevation = 0
        self.target_azimuth = HOME_AZIMUTH
        self.target_elevation = HOME_ELEVATION

        # GUI Elemei
        tkinter.Label(root, text="Azimuth (0° - 360°):").grid(row=0, column=0, padx=5, pady=5)
        self.azimuth_entry = tkinter.Entry(root)
        self.azimuth_entry.grid(row=0, column=1, padx=5, pady=5)
        tkinter.Label(root, text="Elevation (-90° - 90°):").grid(row=1, column=0, padx=5, pady=5)
        self.elevation_entry = tkinter.Entry(root)
        self.elevation_entry.grid(row=1, column=1, padx=5, pady=5)
        tkinter.Button(root, text="Send position", command=self.set_target_position).grid(row=2, column=0, columnspan=2,pady=10)
        tkinter.Button(root, text="Return to Home", command=self.return_to_home).grid(row=3, column=0, columnspan=2, pady=10)
        self.status_label = tkinter.Label(root, text="Status: Enter azimuth and elevation.")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)
        self.coordinates_label = tkinter.Label(root, text="Coordinates: x=0, y=0, z=0")
        self.coordinates_label.grid(row=5, column=0, columnspan=2, pady=5)

        # "Földgömb" vizualizáció
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111, projection='3d')
        plot_globe(self.ax)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tkinter_widget().grid(row=6, column=0, columnspan=2)
        self.start_real_time_movement()

    def set_target_position(self):

        try:
            azimuth = float(self.azimuth_entry.get())
            elevation = float(self.elevation_entry.get())

            # Lépésszámok kiszámítása
            azimuth_steps, elevation_steps = azimuth_elevation_to_steps(azimuth, elevation)

            # Lépésszámok regiszterekbe írása
            self.modbus_handler.write_register(1, 0x0100, azimuth_steps)  # Azimut regiszter
            self.modbus_handler.write_register(1, 0x0101, elevation_steps)  # Eleváció regiszter

            # Koordináták számítása és frissítése a GUI-ban
            x, y, z = calculate_coordinates(azimuth, elevation)
            self.coordinates_label.config(text=f"Coordinates: x={x:.2f}, y={y:.2f}, z={z:.2f}")

            self.status_label.config(text="Status: Position sent.")
        except ValueError:
            self.status_label.config(text="Error: Invalid input.")

    def read_current_position(self):

        try:
            azimuth_steps = self.modbus_handler.read_register(1, 0x0200)  # Azimut aktuális pozíció
            elevation_steps = self.modbus_handler.read_register(1, 0x0201)  # Eleváció aktuális pozíció

            # Lépésszámokat visszaalakítjuk azimut és eleváció értékre
            azimuth = azimuth_steps / 10.0
            elevation = elevation_steps / 10.0

            self.status_label.config(text=f"Current Position: Azimuth={azimuth}°, Elevation={elevation}°")
        except Exception as e:
            self.status_label.config(text=f"Error reading position: {str(e)}")

    def return_to_home(self):

        try:
            # Kezdőpozíció lépésszámainak kiszámítása
            azimuth_steps, elevation_steps = azimuth_elevation_to_steps(
                self.home_azimuth, self.home_elevation
            )

            # Lépésszámok írása regiszterekbe
            self.modbus_handler.write_register(1, 0x0100, azimuth_steps)  # Azimut regiszter
            self.modbus_handler.write_register(1, 0x0101, elevation_steps)  # Eleváció regiszter

            self.status_label.config(text="Status: Returning to home position.")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def start_real_time_movement(self):

        def task():
            while True:
                self.read_current_position()
                sleep(1)

        Thread(target=task, daemon=True).start()

    def close(self):

        self.modbus_handler.close()