import tkinter as tk
from tkinter import ttk
import json

# Función para crear la ventana y los campos de entrada
def create_window(json_data):
    # Crear la ventana principal
    window = tk.Tk()
    window.title("Dynamic Inputs")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    # position_x = screen_width // 2
    # position_y = screen_height // 2
    position_x = 0
    position_y = 0
    window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    # Establecer un tamaño fijo para la ventana
    # window.geometry("800x400")  # Ajusta el tamaño según sea necesario

    # Crear un contenedor de canvas y scrollbar
    canvas = tk.Canvas(window)
    v_scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Función para actualizar el frame dentro del canvas
    def update_scroll_region():
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    # Crear el frame que será el contenido del canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: update_scroll_region()
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=v_scrollbar.set)
    
    # Función para el scroll del ratón
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Asociar el evento de scroll del ratón
    window.bind_all("<MouseWheel>", on_mouse_wheel)
    # Número de columnas
    num_columns = 3

    # Crear campos de entrada basados en el JSON
    row = 0
    col = 0
    entries = {}
    for key, value in json_data.items():
        # Crear una etiqueta para cada campo
        label = ttk.Label(scrollable_frame, text=key)
        label.grid(row=row, column=col*2, sticky=tk.W, padx=3, pady=(3,0))

        # Crear un campo de entrada
        entry = ttk.Entry(scrollable_frame, width=15)  # Ajustar el tamaño del campo de entrada
        entry.grid(row=row+1, column=col*2, sticky=tk.W, padx=3, pady=(3,0))
        entries[key] = entry

        # Mover a la siguiente columna
        col += 1
        if col >= num_columns:
            col = 0
            row += 2

    # Botón para cerrar la ventana
    close_button = ttk.Button(scrollable_frame, text="Close", command=window.destroy)
    close_button.grid(row=row+1, column=0, columnspan=num_columns*2, pady=10)

    # Ejecutar la aplicación
    window.mainloop()

# Función para cargar JSON desde un archivo
def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Ruta al archivo JSON
file_path = 'search_data.json'

# Cargar los datos desde el archivo y crear la ventana
json_data = load_json_from_file(file_path)
create_window(json_data)
