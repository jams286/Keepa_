import tkinter as tk
from tkinter import messagebox, ttk, font, filedialog
import openpyxl
import keepaUtils as kp


columns_excel = [
    "ASIN", "Locale", "Image", "Title", "Sales Rank: Drops last 30 days", "Sales Rank: Drops last 90 days",
    "Bought in past month", "Buy Box: 180 days avg.", "Buy Box: 90 days avg.", "Buy Box: 30 days avg.",
    "Buy Box: Current", "New: 180 days avg.", "New: 90 days avg.", "New: 30 days avg.", "New: Current",
    "Amazon: Current", "Amazon out of stock percentage: 90 days OOS %", "Amazon: 90 days avg.",
    "Amazon: 180 days avg.", "FBA Fees:", "Buy Box: % Amazon 90 days", "URL: Amazon", "Package: Weight (g)",
    "Referral Fee %", "Hazardous Materials", "New Offer Count: Current", "Buy Box Seller",
    "Lowest FBA Seller", "Brand"
]

def run_process():
    def import_excel()->openpyxl.Workbook:        
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if filename:
            try:
                # Cargar el archivo Excel
                wb = openpyxl.load_workbook(filename)       
            except Exception as e:
                print(f"Error al cargar el archivo Excel: {e}")              
            else:
                return wb
    workbook = import_excel()
    sheet = workbook.active
    asins_list = []
    for row in sheet.iter_rows(min_row=2, values_only=True, max_row=3):  # Empezar desde la segunda fila (después de los encabezados)        
        asins_list.append(row[0])  

    if len(asins_list) <= 100:
        filas = kp.RequestProducts(asins_list)
        for k,v in filas.items():
            print(f'Clave:{k}, Valor:{v}')
        


root = tk.Tk()
root.title("Keepa")
# configurando tamaño
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 8
window_height = screen_height // 8
position_x = screen_width // 2
position_y = screen_height // 4
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
# Header
header = tk.Frame(root,bg="#0F0F0F")
header.columnconfigure(0, weight=10)
header.rowconfigure(0,weight=10)

# content1 = tk.Frame(root,bg='#949E9B')
# content1.columnconfigure(0, weight=10)
# content1.rowconfigure(0, weight=10)

content2 = tk.Frame(root,bg='#232D3F')
content2.columnconfigure(0, weight=10)
content2.rowconfigure(0, weight=10)

footer = tk.Frame(root,bg='#0F0F0F')
# configuracion columna
root.columnconfigure(0, weight=10)
# configuracion filas
root.rowconfigure(0, weight=1) #10%
root.rowconfigure(1, weight=8) #80%
root.rowconfigure(2, weight=1) #10%
# agregar header, content y footer
header.grid(row=0, sticky=tk.NSEW)
# content1.grid(row=1, column=0, sticky=tk.NSEW)
content2.grid(row=1, sticky=tk.NSEW, columnspan=2)
footer.grid(row=2, sticky=tk.NSEW)

button = tk.Button(content2, text="Importar Excel", command=run_process, justify="center", highlightthickness=2, bg="#008170", activebackground='#005B41', width=20, height=2)
button.grid(column=0, row=0)

root.mainloop()

if __name__ == '__main__':
    pass