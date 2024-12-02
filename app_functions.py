import customtkinter as ctk
import pymysql
from tkinter import messagebox
from tkinter import ttk
from tkinter import Toplevel
import csv 
import sqlite3
from tkcalendar import Calendar


placeholder_texts = ["Cedula", "Contribuyente", "Nombre Inmueble", "RIF", "Sector", "Cod Catastral", "Fecha Liquidación", "Pago", "Monto"]
button_poppins = ("poppins", 16, "bold") 
placeholder_poppins = ("poppins", 12, "normal") 

# Funcion para establecer la conexion con la db

def connection():
    return sqlite3.connect('regdb.db')

def read():
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """SELECT * FROM reg ORDER BY fechaliquidacion DESC"""
            cursor.execute(sql)
            results = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        results = []

    return results
# Funcion para mostrar los registros de la base de datos

def refreshTable(my_tree, results=None):
    
    # Limpiamos los elementos existentes en el tree
    my_tree.delete(*my_tree.get_children())


    # Si se añadio un valor para results en el llamado de la funcion se insertan en el tree
    # Donde results usualmente en un read() de la db
    
    if results:
#        print(f'Results type: {type(results)}')
        for i, array in enumerate(results):
            tag = "evenrow" if i % 2 == 0 else "oddrow" # Altenar los colores establecidos en my_tree.tag_configure
            my_tree.insert(parent='', index='end', text="", values=array, tag=tag)

    else:
        print("Something went wrong in refreshtable function")


    # Configuracion para las filas de registros
    my_tree.tag_configure('evenrow', background="#EEEEEE")
    my_tree.tag_configure('oddrow', background="#FFFFFF") 

# Funcion para guardar los datos en la db

def save(cedulaEntry, cedulaValue, contribuyenteEntry, nombreinmuebleEntry, rif_indicator, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry, pagoEntry, montoEntry, montoEntry2, my_tree):

    cedula = cedulaValue.get() + cedulaEntry.get()

    contribuyente_popup = contribuyenteEntry.get()
    
    nombreinmueble_popup = nombreinmuebleEntry.get() 

    rif_popup = rif_indicator.get() + rifEntry.get()

    sector_popup = sectorEntry.get() 

    uso_popup = usoEntry.get()

    codcatastral_popup = codcatastralEntry.get()

    selected_date = fechaliquidacionEntry

    pago = pagoEntry.get()

    monto1 = montoEntry.get() 
    monto2 = montoEntry2.get()
    montototal = float(monto1) + float(monto2)
 

    

    # Comentado ya que algunos registros no llevan todos los campos y aún no tenemos respuesta de cuales
    # Son imprecindibles

    #if not all([cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion]):
       # messagebox.showwarning("", "Llena todos los formularios")
        #return

    # Si los campos estan llenos guardamos los datos en la db como un nuevo registro

    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """INSERT INTO reg (cedula, contribuyente, nombreinmueble, rif, sector, 
                     uso, codcatastral, fechaliquidacion, pago, monto, monto2, monto_total) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (cedula, contribuyente_popup, nombreinmueble_popup, rif_popup, sector_popup, uso_popup, codcatastral_popup, selected_date, pago, monto1, monto2,montototal))
            conn.commit()

        results = read() # Llamamos los registros de la bd para mostrarlos en el tree.
        refreshTable(my_tree, results)
        messagebox.showinfo(title="Registro Guardado", message="Registro guardado exitosamente") # Pop-up para confirmar que se guardo el registro

    except Exception as e:
        messagebox.showwarning("", "Se produjo un error: " + str(e)) # Pop-up para mostrar error

# Funcion para eliminar registro seleccionado del tree

def delete(my_tree):

    if not my_tree.selection():
        messagebox.showwarning("", "Por favor selecciona una fila") # Si no hay un registro seleccionado mostramos un pop-up y detenemos la funcion
        return

    decision = messagebox.askquestion("", "Seguro de eliminar los datos seleccionados?") # Verificamos si el usuario esta seguro de eliminar el registro
    if decision != 'yes':
        return

    selectedItem = my_tree.selection()[0] # Guardamos la seleccion del registro en una variable, para acceder a sus valores
    # Seleccionamos los valores para ejecutar el codigo
    cedula = str(my_tree.item(selectedItem)['values'][1]) # Cedula
    name = str(my_tree.item(selectedItem)['values'][2]) # Nombre
    register_id = str(my_tree.item(selectedItem)['values'][0]) # Id registro
    # print(f"{cedula} {name}")    
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM reg WHERE register_id = ?" # Eliminaremos el registro donde coincida el id registro seleccionado con el de la db
            cursor.execute(sql, (register_id,))
            conn.commit()
            messagebox.showinfo(title="Registro eliminado", message=f"Se elimino el registro de '{name}'-'{cedula}' correctamente") # Pop-up mostrando de quien fue el registro eliminado
            results = read()
            refreshTable(my_tree, results)
    except Exception as err:
        messagebox.showwarning("", f"Un error se produjo: {err}")

# Funcion para buscar filtrando por cedula
# Variables no utilizadas se pretender orientar en un futuro para realizar filtros de busqueda

def find(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry):
    try:
        with connection() as conn:
            cursor = conn.cursor()

            # Obtenemos la cedula de la barra de busqueda
            cedula = cedulaEntry.get().strip()
            

            # Si no se provee la cedula, devuelve todos los registro de la db
            if not cedula:
                sql = """SELECT register_id,
                                     cedula,
                              contribuyente,
                             nombreinmueble,
                                        rif,
                                     sector, 
                                        uso, 
                               codcatastral, 
                           fechaliquidacion,
                                       pago,
                                       monto 
                         FROM reg ORDER BY fechaliquidacion DESC"""
                cursor.execute(sql)
                results = cursor.fetchall()
                refreshTable(my_tree, results)
                return

            # Si se provee una cedula devuelve unicamene que los registros asociados con esa cedula
            sql = """SELECT register_id,
                                 cedula,
                          contribuyente,
                         nombreinmueble,
                                    rif,
                                 sector, 
                                    uso, 
                           codcatastral, 
                       fechaliquidacion,
                                   pago,
                                   monto 
                     FROM reg WHERE cedula = ? ORDER BY fechaliquidacion DESC"""
            cursor.execute(sql, (cedula,))

            results = cursor.fetchall()
            refreshTable(my_tree, results)
            if not results:  # Si no hay resultados
                messagebox.showwarning("", "No se encontraron registros para la cédula proporcionada.")
                results = read()
                refreshTable(my_tree, results)
            return

    except Exception as e:
        messagebox.showwarning("", f"An error occurred: {e}")
        print(e)

# Funcion para exportar a excel

def exportExcel():
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM reg"
            cursor.execute(sql)
            data = cursor.fetchall()

            with open('registros.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Cedula', 'Contribuyente', 'Nombre Inmueble', 'RIF', 'Sector', 'Uso', 'Cod Catastral', 'Fecha Liquidacion'])
                writer.writerows(data)

            messagebox.showinfo("Exportación Completa", "Los registros han sido exportados a 'registros.csv'")
    except Exception as e:
        messagebox.showwarning("", f"Error al exportar: {str(e)}")

###########################################################################################################################################
######################################### Pop-up save window / Modal###########################################################
######################################### Ventana modal para guardar###########################################################
###########################################################################################################################################

def open_calendar_popup(entry_widget):
    """Open a calendar popup to select a date."""
    calendar_popup = Toplevel()
    calendar_popup.title("Seleccionar Fecha")
    calendar_popup.geometry("300x300")
    calendar_popup.resizable(width=False, height=False)

    # Add Calendar widget
    calendar = Calendar(calendar_popup, date_pattern="dd-mm-yyyy")  # Use desired format
    calendar.pack(padx=10, pady=10)

    # Function to handle date selection
    def select_date():
        selected_date = calendar.get_date()
        entry_widget.delete(0, "end")  # Clear existing value in the entry
        entry_widget.insert(0, selected_date)  # Insert selected date
        calendar_popup.destroy()  # Close the calendar popup

    # Add button to confirm date selection
    select_button = ctk.CTkButton(calendar_popup, text="Seleccionar", command=select_date)
    select_button.pack(pady=10)

def open_save_popup(my_tree):
    """Open a popup window to input data for a new register."""
    window = ctk.CTk()
    popup = ctk.CTkToplevel(window)
    popup.title("Nuevo Registro")
    popup.geometry("400x600")
    #popup.resizable(width=False, height=False)
    popup.resizable()

    # Create frame for entry fields
    
    contribuyente_frame = ctk.CTkFrame(popup)
    contribuyente_frame.pack(padx=10, pady=5, fill="x")
    
    cedula_frame = ctk.CTkFrame(popup)
    cedula_frame.pack(padx=10, pady=5, fill="x")
    
    inmueble_frame = ctk.CTkFrame(popup)
    inmueble_frame.pack(padx=10, fill="x")
    
    # entry_frame = ctk.CTkFrame(popup)
    # entry_frame.pack(padx=10, pady=5, fill="x")
    
    rif_frame = ctk.CTkFrame(popup)
    rif_frame.pack(padx=10, pady=5,fill="x")
    
    sector_frame = ctk.CTkFrame(popup)
    sector_frame.pack(padx=10, pady=5,fill="x")

    uso_frame = ctk.CTkFrame(popup)
    uso_frame.pack(padx=10, pady=5,fill="x")

    codcastastral_frame = ctk.CTkFrame(popup)
    codcastastral_frame.pack(padx=10, pady=5,fill="x")

    # Create entry fields in the frame

    contribuyente_popup = ctk.CTkEntry(contribuyente_frame, placeholder_text="Contribuyente", font=placeholder_poppins, width=380)
    # contribuyente_popup.grid(row=0, column=0, pady=5)
    contribuyente_popup.pack(pady=5, padx=5)

    contribuyente_values = ["V","E"]    
    contribuyente_indicator = ctk.CTkOptionMenu(cedula_frame, values=contribuyente_values, width=56, font=placeholder_poppins)
    contribuyente_indicator.pack(padx=5, pady=5, side="left")

    cedula_popup = ctk.CTkEntry(cedula_frame, placeholder_text="Cedula", font=placeholder_poppins, width=380)
    # cedula_popup.grid(row=1, column=0, pady=5)
    cedula_popup.pack(pady=5, padx=5)

    nombreinmueble_popup = ctk.CTkEntry(inmueble_frame, placeholder_text="Nombre Inmueble", font=placeholder_poppins, width=380)
    nombreinmueble_popup.grid(pady=5)
    nombreinmueble_popup.pack(pady=5, padx=5)

    rif_values = ["J","C","G"]    
    rif_indicator = ctk.CTkOptionMenu(rif_frame, values=rif_values, width=56, font=placeholder_poppins)
    rif_indicator.pack(padx=5, pady=5, side="left")

    rif_popup = ctk.CTkEntry(rif_frame, placeholder_text="RIF", font=placeholder_poppins, width=380)
    # rif_popup.grid(pady=5)
    rif_popup.pack(pady=5, padx=5)

    sector_popup = ctk.CTkEntry(sector_frame, placeholder_text="Sector", font=placeholder_poppins, width=380)
    sector_popup.grid(pady=5)
    sector_popup.pack(pady=5, padx=5)

    uso_options = ["Comercial", "Residencial"]

    uso_label = ctk.CTkLabel(uso_frame, text="TIPO DE USO", font=button_poppins)
    uso_label.pack(side="left", padx=10, pady=5)

    uso_popup = ctk.CTkOptionMenu(uso_frame, values=uso_options, font=placeholder_poppins )
    # uso_popup.grid(pady=5)
    uso_popup.pack(padx=5, pady=5, fill="x", expand=True, side="right")

    codcatastral_popup = ctk.CTkEntry(codcastastral_frame, placeholder_text="Cod Catastral", font=placeholder_poppins, width=380)
    codcatastral_popup.grid(row=6, column=0, pady=5)
    codcatastral_popup.pack(pady=5, padx=5)

    

    # Create frame for calendar button
    calendar_frame = ctk.CTkFrame(popup)
    calendar_frame.pack(pady=5, padx=10, fill="x")

    fechaliquidacion_entry = ctk.CTkEntry(calendar_frame, placeholder_text="Fecha Liquidación", font=placeholder_poppins, width=300)
    fechaliquidacion_entry.pack(padx=5, pady=5, side='left')

    calendar_button = ctk.CTkButton(calendar_frame, text="📅",width=50, command=lambda: open_calendar_popup(fechaliquidacion_entry))
    calendar_button.pack(pady=5, padx=5, fill="x")

    

    # Create frame for payment dropdown
    pago_frame = ctk.CTkFrame(popup)
    pago_frame.pack(pady=5, padx=10, fill="x")

    # Create the label
    pagonopago = ctk.CTkLabel(pago_frame, text="PAGO O NO PAGO", font=button_poppins)
    pagonopago.pack(side="left", padx=10, pady=5)

    # Create the dropdown menu
    pago_options = ["Si", "No"]
    pago_dropdown = ctk.CTkOptionMenu(pago_frame, values=pago_options, font=placeholder_poppins)
    pago_dropdown.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    monto_frame = ctk.CTkFrame(popup)
    monto_frame.pack(pady=5, padx=10, fill="x")

    monto_popup = ctk.CTkEntry(monto_frame, placeholder_text="Monto", font=placeholder_poppins, width=190)
    monto_popup.pack(side="left", padx=5, pady=5, fill="x")
    monto_popup2 = ctk.CTkEntry(monto_frame, placeholder_text="Monto 2", font=placeholder_poppins, width=190)
    monto_popup2.pack(side="right", padx=5, pady=5, fill="x")

    # Save button within popup




    


    def save_popup_data():
        
        selected_date = fechaliquidacion_entry.get()

        save(cedula_popup, contribuyente_indicator, contribuyente_popup, nombreinmueble_popup, rif_indicator, rif_popup, sector_popup, uso_popup, codcatastral_popup, selected_date, pago_dropdown, monto_popup, monto_popup2, my_tree)
        popup.destroy()  # Close popup after saving

    save_button = ctk.CTkButton(popup, text="Save", command=save_popup_data, font=button_poppins, width=380)
    save_button.pack(pady=5)


###########################################################################################################################################
######################################### Pop-up update window / Modal###########################################################
######################################### Ventana modal para actualizar###########################################################
###########################################################################################################################################

# def open_update_modal(my_tree, placeholderArray):
#     if not my_tree.selection():
#         messagebox.showwarning("", "Por favor selecciona fila")
#         return

#     selectedItem = my_tree.selection()[0]
#     item_id = selectedItem
#     values = my_tree.item(selectedItem)['values']

#     # Create modal window for updating
#     modal = ctk.CTkToplevel()
#     modal.title("Actualizar registro")
#     modal.geometry("400x500")


#     # Create input fields with existing data
#     entries = []
#     for i, placeholder in enumerate(placeholderArray):
#             entry = ctk.CTkEntry(modal, placeholder_text=placeholder.get())
#             entry.insert(0, values[i + 1])  # +1 to skip register_id
#             entry.pack(pady=5)
#             entries.append(entry)

#     # Update button within modal
#     def update_record():
#         updated_values = [entry.get() for entry in entries]
#         # Update the Treeview item with new values, except register_id
#         my_tree.item(item_id, values=(my_tree.item(item_id)['values'][0], *updated_values))
#         with connection() as conn:
#             cursor = conn.cursor()
#             sql = '''
#             UPDATE reg
#             SET 
#             cedula = ?,
#             contribuyente = ?,
#             nombreinmueble = ?,
#             rif = ?,
#             sector = ?,
#             uso = ?,
#             codcatastral = ?,
#             fechaliquidacion = ?,
#             pago = ?,
#             monto = ?
#             WHERE register_id = ?
#             '''
#             cursor.execute(sql,(*updated_values, my_tree.item(item_id)['values'][0]))
#             conn.commit()
#         results = read()
#         refreshTable(my_tree, results)
#         messagebox.showinfo(title="Actualización de registro",message="Registro actualizado exitosamente")
#         modal.destroy()

#     update_button = ctk.CTkButton(modal, text="Actualizar", command=update_record)
#     update_button.pack(pady=10)

def open_update_modal(my_tree, placeholderArray):
    if not my_tree.selection():
        messagebox.showwarning("", "Por favor selecciona fila")
        return

    selectedItem = my_tree.selection()[0]
    item_id = selectedItem
    values = my_tree.item(selectedItem)['values']

    # Create modal window for updating
    modal = ctk.CTkToplevel()
    modal.title("Actualizar registro")
    modal.geometry("400x600")

    # Create frames and fields
    contribuyente_frame = ctk.CTkFrame(modal)
    contribuyente_frame.pack(padx=10, pady=5, fill="x")

    cedula_frame = ctk.CTkFrame(modal)
    cedula_frame.pack(padx=10, pady=5, fill="x")

    inmueble_frame = ctk.CTkFrame(modal)
    inmueble_frame.pack(padx=10, pady=5, fill="x")

    rif_frame = ctk.CTkFrame(modal)
    rif_frame.pack(padx=10, pady=5, fill="x")

    sector_frame = ctk.CTkFrame(modal)
    sector_frame.pack(padx=10, pady=5, fill="x")

    uso_frame = ctk.CTkFrame(modal)
    uso_frame.pack(padx=10, pady=5, fill="x")

    codcatastral_frame = ctk.CTkFrame(modal)
    codcatastral_frame.pack(padx=10, pady=5, fill="x")

    calendar_frame = ctk.CTkFrame(modal)
    calendar_frame.pack(pady=5, padx=10, fill="x")

    pago_frame = ctk.CTkFrame(modal)
    pago_frame.pack(pady=5, padx=10, fill="x")

    monto_frame = ctk.CTkFrame(modal)
    monto_frame.pack(pady=5, padx=10, fill="x")

    # Populate fields with existing data
    contribuyente_values = ["1", "2", "3"]
    contribuyente_indicator = ctk.CTkOptionMenu(contribuyente_frame, values=contribuyente_values)
    # contribuyente_indicator.set(values[1])  # Set existing value
    contribuyente_indicator.pack(padx=5, pady=5, side="left")

    contribuyente_popup = ctk.CTkEntry(contribuyente_frame, placeholder_text="Contribuyente")
    contribuyente_popup.insert(0, values[2])
    contribuyente_popup.pack(padx=5, pady=5, fill="x")

    cedula_popup = ctk.CTkEntry(cedula_frame, placeholder_text="Cedula")
    cedula_popup.insert(0, values[1])
    cedula_popup.pack(padx=5, pady=5, fill="x")

    nombreinmueble_popup = ctk.CTkEntry(inmueble_frame, placeholder_text="Nombre Inmueble")
    nombreinmueble_popup.insert(0, values[3])
    nombreinmueble_popup.pack(padx=5, pady=5, fill="x")

    rif_values = ["V", "E", "J", "C", "G"]
    rif_indicator = ctk.CTkOptionMenu(rif_frame, values=rif_values)
    rif = values[4][0]
    rif_indicator.set(rif)
    rif_indicator.pack(padx=5, pady=5, side="left")

    rif_popup = ctk.CTkEntry(rif_frame, placeholder_text="RIF")
    rif_popup.insert(0, values[4])
    rif_popup.pack(padx=5, pady=5, fill="x")

    sector_popup = ctk.CTkEntry(sector_frame, placeholder_text="Sector")
    sector_popup.insert(0, values[5])
    sector_popup.pack(padx=5, pady=5, fill="x")

    uso_options = ["Comercial", "Residencial"]
    uso_label = ctk.CTkLabel(uso_frame, text="TIPO DE USO", font=button_poppins)
    uso_label.pack(side="left", padx=10)
    uso_popup = ctk.CTkOptionMenu(uso_frame, values=uso_options)
    uso_popup.set(values[6])
    uso_popup.pack(side="right", padx=5, fill="x", expand=True)

    codcatastral_popup = ctk.CTkEntry(codcatastral_frame, placeholder_text="Cod Catastral")
    codcatastral_popup.insert(0, values[7])
    codcatastral_popup.pack(padx=5, pady=5, fill="x")

    fechaliquidacion_entry = ctk.CTkEntry(calendar_frame, placeholder_text="Fecha Liquidación", width=300)
    fechaliquidacion_entry.insert(0, values[8])
    fechaliquidacion_entry.pack(pady=5, padx=5, side="left")

    calendar_button = ctk.CTkButton(calendar_frame, text="📅", width=50, command=lambda: open_calendar_popup(fechaliquidacion_entry))
    calendar_button.pack( padx=5, pady=5, fill="x")

    pago_options = ["Si", "No"]
    pago_label = ctk.CTkLabel(pago_frame, text="PAGO O NO PAGO", font=button_poppins)
    pago_label.pack(padx=10, fill="x", side="left")
    pago_dropdown = ctk.CTkOptionMenu(pago_frame, values=pago_options)
    # pago_dropdown.set(values[11])
    pago_dropdown.pack(side="right", padx=5, fill="x", expand=True)

    monto_popup = ctk.CTkEntry(monto_frame, placeholder_text="Monto", width=180)
    # monto_popup.insert(0, values[12])
    monto_popup.pack(side="left", padx=5)

    monto_popup2 = ctk.CTkEntry(monto_frame, placeholder_text="Monto 2", width=180)
    # monto_popup2.insert(0, values[13])
    monto_popup2.pack(side="right", padx=5)

    # Update button
    def update_record():
        updated_values = [
            cedula_popup.get(),
            contribuyente_popup.get(),
            nombreinmueble_popup.get(),
            rif_popup.get(),
            sector_popup.get(),
            uso_popup.get(),
            codcatastral_popup.get(),
            fechaliquidacion_entry.get(),
            pago_dropdown.get(),
            monto_popup.get(),
            monto_popup2.get(),
        ]
        my_tree.item(item_id, values=(values[0], *updated_values))
        with connection() as conn:
            cursor = conn.cursor()
            sql = '''
            UPDATE reg
            SET cedula = ?, contribuyente = ?, nombreinmueble = ?, rif = ?, sector = ?, uso = ?, 
            codcatastral = ?, fechaliquidacion = ?, pago = ?, monto = ?
            WHERE register_id = ?'''
            cursor.execute(sql, (*updated_values, values[0]))
            conn.commit()
        refreshTable(my_tree, read())
        messagebox.showinfo("Actualización", "Registro actualizado")
        modal.destroy()

    update_button = ctk.CTkButton(modal, text="Actualizar", command=update_record)
    update_button.pack(pady=10)
