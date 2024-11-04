import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont  
import pymysql
import csv
from datetime import datetime
import ctypes
from app_functions import *

def create_rounded_rectangle(canvas, x0, y0, x1, y1, r, **kwargs):
    """Draw a rounded rectangle on the specified canvas."""
    points = [
        x0 + r, y0,   # Top-left corner
        x1 - r, y0,   # Top-right corner
        x1, y0 + r,   # Top-right corner round
        x1, y1 - r,   # Bottom-right corner round
        x1 - r, y1,   # Bottom-right corner
        x0 + r, y1,   # Bottom-left corner
        x0, y1 - r,   # Bottom-left corner round
        x0, y0 + r,   # Top-left corner round
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Create the main window using customtkinter
window = ctk.CTk()
window.title("CRUD Catastro")
window.geometry("1330x600")
#window.resizable(width=False,height=False)

myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
window.iconbitmap(r'C:\Github\crud-ctk-catastro\crud-ctk-catastro\img\img.ico')

# Create a frame for input fields and buttons
frame = ctk.CTkFrame(window)
frame.pack(fill="x", padx=10, pady=10)

# Buttons style
button_poppins = ("poppins", 16, "bold") 
placeholder_poppins = ("poppins", 12, "normal") 

input_frame = ctk.CTkFrame(window)

# Create input fields with placeholders after the buttons
cedulaEntry = ctk.CTkEntry(frame, placeholder_text="Introduce la cedula", font=placeholder_poppins, width=200)
cedulaEntry.grid(row=0, column=6, padx=5, pady=5, sticky="ew")

contribuyenteEntry = ctk.CTkEntry(input_frame, placeholder_text="Contribuyente", font=placeholder_poppins)

nombreinmuebleEntry = ctk.CTkEntry(input_frame, placeholder_text="Nombre Inmueble", font=placeholder_poppins)

rifEntry = ctk.CTkEntry(input_frame, placeholder_text="RIF", font=placeholder_poppins)

sectorEntry = ctk.CTkEntry(input_frame, placeholder_text="Sector", font=placeholder_poppins)

usoEntry = ctk.CTkEntry(input_frame, placeholder_text="Uso", font=placeholder_poppins)

codcatastralEntry = ctk.CTkEntry(input_frame, placeholder_text="Cod Catastral", font=placeholder_poppins)

fechaliquidacionEntry = ctk.CTkEntry(input_frame, placeholder_text="Fecha Liquidación", font=placeholder_poppins)

placeholderArray = [cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry]

# Create a frame to hold the Treeview
frame_tree = ctk.CTkFrame(window, fg_color='white', width=580, height=360)
frame_tree.pack(pady=10, padx=10, expand=True, fill="both")  # Adjusted padding

# Define buttons with text and appropriate commands
buttons = [
    ("Agregar", open_save_popup),
    ("Actualizar", lambda: open_update_modal(my_tree, placeholderArray)),
    ("Eliminar", lambda: delete(my_tree)),
    ("Limpiar", lambda: clear(placeholderArray)),
    ("Exportar a Excel", lambda: exportExcel()),
    ("Buscar", lambda: find(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry))
]

# Create the buttons in a loop
for i, (text, command) in enumerate(buttons):
    ctk.CTkButton(frame, text=text, command=command, font=button_poppins).grid(row=0, column=i, padx=5, pady=5, sticky="w")

# Create a style for the Treeview
style = ttk.Style()
style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  # Set the desired font and size for the treeview
style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))  # Set header font size and style


# Create Treeview for displaying records with the custom style
my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
my_tree.pack(pady=10, padx=10, fill="both", expand=True)

# Define columns
my_tree['columns'] = ('register_id', 'cedula', 'contribuyente', 'nombreinmueble', 'rif', 'sector', 'uso', 'codcatastral', 'fechaliquidacion')

# Format columns
for col in my_tree['columns']:
    my_tree.heading(col, text=col.capitalize(), anchor='center')  # Ensure anchor alignment
    my_tree.column(col, anchor='center')

some_function(my_tree, placeholderArray)

# Draw a rounded rectangle on the frame_tree
canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
canvas.place(x=0, y=0)  # Position the canvas at the top-left of the frame
create_rounded_rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')

# Refresh the table to show db results
with connection() as conn:
    cursor = conn.cursor()
    sql = '''
    SELECT * FROM reg ORDER BY fechaliquidacion DESC   
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    refreshTable(my_tree, results)

window.mainloop()


