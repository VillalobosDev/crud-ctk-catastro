import customtkinter as ctk
from tkinter import ttk
import ctypes
from app_functions import *

def rectangle(canvas, x0, y0, x1, y1, r, **kwargs):
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

# Creando la ventana
window = ctk.CTk()
window.title("CRUD Catastro")
window.geometry("1080x720")
#window.resizable(width=False, height=False)

myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary st
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# Creado el frame donde iran los botones
frame = ctk.CTkFrame(window)
frame.pack(fill="x", padx=10, pady=10)
frame.grid_columnconfigure(6, weight=1)

# Estilo 
button_poppins = ("poppins", 16, "bold") 
placeholder_poppins = ("poppins", 12, "normal") 

input_frame = ctk.CTkFrame(window)

# Creando inputs despues de los botones, para las ventanas modales
cedulaEntry = ctk.CTkEntry(frame, placeholder_text="Introduce la cedula", font=placeholder_poppins, width=200)
cedulaEntry.grid(row=0, column=7, padx=7, pady=5, sticky="e")

contribuyenteEntry = ctk.CTkEntry(input_frame, placeholder_text="Contribuyente", font=placeholder_poppins)

nombreinmuebleEntry = ctk.CTkEntry(input_frame, placeholder_text="Nombre Inmueble", font=placeholder_poppins)

rifEntry = ctk.CTkEntry(input_frame, placeholder_text="RIF", font=placeholder_poppins)

sectorEntry = ctk.CTkEntry(input_frame, placeholder_text="Sector", font=placeholder_poppins)

usoEntry = ctk.CTkEntry(input_frame, placeholder_text="Uso", font=placeholder_poppins)

codcatastralEntry = ctk.CTkEntry(input_frame, placeholder_text="Cod Catastral", font=placeholder_poppins)

fechaliquidacionEntry = ctk.CTkEntry(input_frame, placeholder_text="Fecha Liquidación", font=placeholder_poppins)

placeholderArray = [cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry]

# Frame para el treeview (Vista de los registros)
frame_tree = ctk.CTkFrame(window, fg_color='white', width=580, height=360)
frame_tree.pack(pady=10, padx=10, expand=True, fill="both")  

# Definiendo botones con sus comandos
buttons = [
    ("Agregar", lambda: open_save_popup(my_tree)),
    ("Actualizar", lambda: open_update_modal(my_tree, placeholderArray)),
    ("Eliminar", lambda: delete(my_tree)),
    ("Exportar a Excel", lambda: exportExcel())
]

# Creamos los botones con un blucle for
for i, (text, command) in enumerate(buttons):
    ctk.CTkButton(frame, text=text, command=command, font=button_poppins).grid(row=0, column=i, padx=5, pady=5, sticky="w")

# Creamos a parte el boton de busqueda para adjuntar disntintas propiedades
ctk.CTkButton(frame, text="Buscar", command= lambda: find(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry), font=button_poppins).grid(row=0, column=6, padx=5, pady=5, sticky="e")

# Creando estilo para el treeview
style = ttk.Style()
style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 


# Creando el treeview para mostrar los registros
my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
my_tree.pack(pady=10, padx=10, fill="both", expand=True)

# Definiendo las columnas 
my_tree['columns'] = ('register_id', 'cedula', 'contribuyente', 'nombreinmueble', 'rif', 'sector', 'uso', 'codcatastral', 'fechaliquidacion')

# Formateando columnas
for col in my_tree['columns']:
    my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
    my_tree.column(col, anchor='center')


# Llamamos la funcion para crear un canvas alrededor del treeview y darle un aspecto redondeado
# Nativamente desde tkinter o customtkinter no se encuentran opciones similares
# Y esta fue nuestra forma de darle el efecto border radius que da un toque de clase al treeview

canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
canvas.place(x=0, y=0)  # Posicionamos el canvas
rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')

# Llamamos los registros de la base de datos
with connection() as conn:
    cursor = conn.cursor()
    sql = '''
    SELECT * FROM reg ORDER BY fechaliquidacion DESC   
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    refreshTable(my_tree, results)

window.mainloop()


