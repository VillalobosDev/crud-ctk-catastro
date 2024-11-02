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
input_frame.pack(fill="x", padx=10, pady=10)

def open_save_popup():
    """Open a popup window to input data for a new register."""
    popup = ctk.CTkToplevel(window)
    popup.title("Add New Register")
    popup.geometry("400x400")

    # Create entry fields in the popup window
    cedula_popup = ctk.CTkEntry(popup, placeholder_text="Cedula", font=placeholder_poppins, width=300)
    cedula_popup.pack(padx=5, pady=5)

    contribuyente_popup = ctk.CTkEntry(popup, placeholder_text="Contribuyente", font=placeholder_poppins)
    contribuyente_popup.pack(padx=5, pady=5)

    nombreinmueble_popup = ctk.CTkEntry(popup, placeholder_text="Nombre Inmueble", font=placeholder_poppins)
    nombreinmueble_popup.pack(padx=5, pady=5)

    rif_popup = ctk.CTkEntry(popup, placeholder_text="RIF", font=placeholder_poppins)
    rif_popup.pack(padx=5, pady=5)

    sector_popup = ctk.CTkEntry(popup, placeholder_text="Sector", font=placeholder_poppins)
    sector_popup.pack(padx=5, pady=5)

    uso_popup = ctk.CTkEntry(popup, placeholder_text="Uso", font=placeholder_poppins)
    uso_popup.pack(padx=5, pady=5)

    codcatastral_popup = ctk.CTkEntry(popup, placeholder_text="Cod Catastral", font=placeholder_poppins)
    codcatastral_popup.pack(padx=5, pady=5)

    fechaliquidacion_popup = ctk.CTkEntry(popup, placeholder_text="Fecha Liquidación", font=placeholder_poppins)
    fechaliquidacion_popup.pack(padx=5, pady=5)

    # Array of popup entries to pass to save function
    popup_placeholder_array = [
        cedula_popup, contribuyente_popup, nombreinmueble_popup, rif_popup, sector_popup, uso_popup, codcatastral_popup, fechaliquidacion_popup
    ]

    # Save button within popup
    def save_popup_data():
        save(cedula_popup, contribuyente_popup, nombreinmueble_popup, rif_popup, sector_popup, uso_popup, codcatastral_popup, fechaliquidacion_popup, popup_placeholder_array, my_tree)
        popup.destroy()  # Close popup after saving

    save_button = ctk.CTkButton(popup, text="Save", command=save_popup_data, font=button_poppins)
    save_button.pack(pady=10)

# Create a frame to hold the Treeview
frame_tree = ctk.CTkFrame(window, fg_color='white', width=580, height=360)
frame_tree.pack(pady=10, padx=10, expand=True, fill="both")  # Adjusted padding

# Define buttons with text and appropriate commands
# Define buttons with text and appropriate commands
buttons = [
    ("Agregar", open_save_popup),  # Change this to open the popup
    ("Actualizar", lambda: update(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry, placeholderArray)),
    ("Eliminar", lambda: delete(my_tree)),
    ("Seleccionar", lambda: select(my_tree, placeholderArray)),
    ("Buscar", lambda: find(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry)),
    ("Limpiar", lambda: clear(placeholderArray)),
    ("Exportar a Excel", lambda: exportExcel())
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

my_tree.bind('<ButtonRelease-1>', lambda event: select(my_tree, placeholderArray))  # Bind selection event

some_function(my_tree, placeholderArray)

# Draw a rounded rectangle on the frame_tree
canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
canvas.place(x=0, y=0)  # Position the canvas at the top-left of the frame
create_rounded_rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')

# Refresh the table
refreshTable(my_tree)

window.mainloop()


