import customtkinter as ctk
import pymysql
from tkinter import messagebox
import csv
from customtkinter import CTkEntry
from tkinter import ttk

placeholder_texts = ["Cedula", "Contribuyente", "Nombre Inmueble", "RIF", "Sector", "Cod Catastral", "Fecha Liquidación"]
button_poppins = ("poppins", 16, "bold") 
placeholder_poppins = ("poppins", 12, "normal") 

def some_function(my_tree, placeholderArray):
    # Now placeholderArray is defined here and can be used
    pass

# Function to connect to the database
def connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='regdb'
    )

def read():
    with connection() as conn:  # Use context manager to handle connection
        cursor = conn.cursor()
        sql = """SELECT register_id, cedula, contribuyente, nombreinmueble, rif, sector, 
                 uso, codcatastral, fechaliquidacion FROM reg ORDER BY fechaliquidacion DESC"""
        cursor.execute(sql)
        results = cursor.fetchall()
    return results

def refreshTable(my_tree, results=None):
    # Clear existing items in the tree
    my_tree.delete(*my_tree.get_children())

    # If results are provided, insert them into the tree
    if results:
        for i, array in enumerate(results):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            my_tree.insert(parent='', index='end', text="", values=array, tag=tag)

    # Configure row colors
    my_tree.tag_configure('evenrow', background="#EEEEEE")
    my_tree.tag_configure('oddrow', background="#FFFFFF") 

def setph(word, num, placeholderArray):
    if num < len(placeholderArray):
        entry = placeholderArray[num]
        entry.delete(0, 'end')  # Clear the current text
        entry.insert(0, word)

def save(cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry, placeholderArray, my_tree):
    cedula = cedulaEntry.get().strip()
    contribuyente = contribuyenteEntry.get().strip()
    nombreinmueble = nombreinmuebleEntry.get().strip()
    rif = rifEntry.get().strip()
    sector = sectorEntry.get().strip()
    uso = usoEntry.get().strip()
    codcatastral = codcatastralEntry.get().strip()
    fechaliquidacion = fechaliquidacionEntry.get().strip()

    if not all([cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion]):
        messagebox.showwarning("", "Llena todos los formularios")
        return

    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """INSERT INTO reg (cedula, contribuyente, nombreinmueble, rif, sector, 
                     uso, codcatastral, fechaliquidacion) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion))
            conn.commit()

        for num in range(len(placeholderArray)):
            setph('', num, placeholderArray)
        refreshTable(my_tree)

    except Exception as e:
        messagebox.showwarning("", "Se produjo un error: " + str(e))

# def update(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry, placeholderArray):
#     if not my_tree.selection():
#         messagebox.showwarning("", "Por favor selecciona un elemento para actualizar.")
#         return

#     selectedItem = my_tree.selection()[0]
#     item_values = my_tree.item(selectedItem)['values']

#     if not item_values or len(item_values) < 8:
#         messagebox.showwarning("", "El elemento seleccionado no tiene valores completos.")
#         return

#     selectedItemId = str(item_values[0])

#     cedula = cedulaEntry.get().strip()
#     contribuyente = contribuyenteEntry.get().strip()
#     nombreinmueble = nombreinmuebleEntry.get().strip()
#     rif = rifEntry.get().strip()
#     sector = sectorEntry.get().strip()
#     uso = usoEntry.get().strip()
#     codcatastral = codcatastralEntry.get().strip()
#     fechaliquidacion = fechaliquidacionEntry.get().strip()

#     try:
#         with connection() as conn:
#             cursor = conn.cursor()
#             sql = """UPDATE reg 
#                      SET cedula = %s, contribuyente = %s, nombreinmueble = %s, 
#                          rif = %s, sector = %s, uso = %s, codcatastral = %s, 
#                          fechaliquidacion = %s 
#                      WHERE register_id = %s"""

#             cursor.execute(sql, (cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion, selectedItemId))
#             conn.commit()

#         for num in range(min(len(placeholderArray), len(placeholder_texts))):
#             setph(placeholder_texts[num], num, placeholderArray)
#         results = read()
#         refreshTable(my_tree, results)

#     except Exception as err:
#         messagebox.showwarning("", "Un error se produjo: " + str(err))

def delete(my_tree):
    if not my_tree.selection():
        messagebox.showwarning("", "Por favor selecciona fila")
        return

    decision = messagebox.askquestion("", "Seguro de eliminar los datos seleccionados?")
    if decision != 'yes':
        return

    selectedItem = my_tree.selection()[0]
    cedula = str(my_tree.item(selectedItem)['values'][0])

    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM reg WHERE cedula = %s"
            cursor.execute(sql, (cedula,))
            conn.commit()
            messagebox.showinfo("", "Se elimino el registro correctamente")
            refreshTable(my_tree)
    except Exception as err:
        messagebox.showwarning("", f"Un error se produjo: {err}")

# def select(my_tree, placeholderArray):
#     try:
#         selected_items = my_tree.selection()
#         if len(selected_items) != 1:
#             messagebox.showwarning("Selection Error", "Please select only one row for updating.")
#             return


#         selectedItem = my_tree.selection()[0]
#         cedula = str(my_tree.item(selectedItem)['values'][1])
#         contribuyente = str(my_tree.item(selectedItem)['values'][2])
#         nombreinmueble = str(my_tree.item(selectedItem)['values'][3])
#         rif = str(my_tree.item(selectedItem)['values'][4])
#         sector = str(my_tree.item(selectedItem)['values'][5])
#         uso = str(my_tree.item(selectedItem)['values'][6])
#         codcatastral = str(my_tree.item(selectedItem)['values'][7])
#         fechaliquidacion = str(my_tree.item(selectedItem)['values'][8])

#         setph(cedula, 0, placeholderArray)
#         setph(contribuyente, 1, placeholderArray)
#         setph(nombreinmueble, 2, placeholderArray)
#         setph(rif, 3, placeholderArray)
#         setph(sector, 4, placeholderArray)
#         setph(uso, 5, placeholderArray)
#         setph(codcatastral, 6, placeholderArray)
#         setph(fechaliquidacion, 7, placeholderArray)

#         open_update_modal(my_tree, placeholderArray, selectedItem)
#     except Exception as e:
#         messagebox.showwarning(f"{e}", "Por favor selecciona una columna")
#         print(e)

def find(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry):
    try:
        with connection() as conn:
            cursor = conn.cursor()

            # Retrieve values from entry fields
            cedula = cedulaEntry.get().strip()
            

            # If no entry fields are filled, get all records ordered by fechaliquidacion
            if not cedula:
                sql = """SELECT register_id, cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion 
                         FROM reg ORDER BY fechaliquidacion DESC"""
                cursor.execute(sql)
                results = cursor.fetchall()
                refreshTable(my_tree, results)
                return

            # If a cedula is present, retrieve all records associated with that cedula
            sql = """SELECT register_id, cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion 
                     FROM reg WHERE cedula = %s ORDER BY fechaliquidacion DESC"""
            cursor.execute(sql, (cedula,))
            results = cursor.fetchall()
            refreshTable(my_tree, results)
            if not results:  # If no results were found
                messagebox.showwarning("", "No se encontraron registros para la cédula proporcionada.")
            return

    except Exception as e:
        messagebox.showwarning("", f"An error occurred: {e}")
        print(e)

def clear(placeholderArray):
    for num in range(len(placeholderArray)):
        setph('', num, placeholderArray)

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
###########################################################################################################################################

def open_save_popup():
    """Open a popup window to input data for a new register."""
    window = ctk.CTk()
    popup = ctk.CTkToplevel(window)
    popup.title("Nuevo Registro")
    popup.geometry("400x400")
    popup.resizable(width=False,height=False)

    # Create entry fields in the popup window
    cedula_popup = ctk.CTkEntry(popup, placeholder_text="Cedula", font=placeholder_poppins, width=380)
    cedula_popup.pack(padx=5, pady=5)

    contribuyente_popup = ctk.CTkEntry(popup, placeholder_text="Contribuyente", font=placeholder_poppins, width=380)
    contribuyente_popup.pack(padx=5, pady=5)

    nombreinmueble_popup = ctk.CTkEntry(popup, placeholder_text="Nombre Inmueble", font=placeholder_poppins, width=380)
    nombreinmueble_popup.pack(padx=5, pady=5)

    rif_popup = ctk.CTkEntry(popup, placeholder_text="RIF", font=placeholder_poppins, width=380)
    rif_popup.pack(padx=5, pady=5)

    sector_popup = ctk.CTkEntry(popup, placeholder_text="Sector", font=placeholder_poppins, width=380)
    sector_popup.pack(padx=5, pady=5)

    uso_popup = ctk.CTkEntry(popup, placeholder_text="Uso", font=placeholder_poppins, width=380)
    uso_popup.pack(padx=5, pady=5)

    codcatastral_popup = ctk.CTkEntry(popup, placeholder_text="Cod Catastral", font=placeholder_poppins, width=380)
    codcatastral_popup.pack(padx=5, pady=5)

    fechaliquidacion_popup = ctk.CTkEntry(popup, placeholder_text="Fecha Liquidación", font=placeholder_poppins, width=380)
    fechaliquidacion_popup.pack(padx=5, pady=5)

    # Array of popup entries to pass to save function
    popup_placeholder_array = [
        cedula_popup, contribuyente_popup, nombreinmueble_popup, rif_popup, sector_popup, uso_popup, codcatastral_popup, fechaliquidacion_popup
    ]

    # Save button within popup
    def save_popup_data(my_tree):
        save(cedula_popup, contribuyente_popup, nombreinmueble_popup, rif_popup, sector_popup, uso_popup, codcatastral_popup, fechaliquidacion_popup, popup_placeholder_array, my_tree)
        popup.destroy()  # Close popup after saving

    save_button = ctk.CTkButton(popup, text="Save", command=save_popup_data, font=button_poppins, width=380)
    save_button.pack(pady=10)

###########################################################################################################################################
######################################### Pop-up update window / Modal###########################################################
###########################################################################################################################################

def open_update_modal(my_tree, placeholderArray):
    selectedItem = my_tree.selection()[0]
    item_id = selectedItem
    values = my_tree.item(selectedItem)['values']

    # Create modal window for updating
    modal = ctk.CTkToplevel()
    modal.title("Actualizar registro")
    modal.geometry("400x400")


    # Create input fields with existing data
    entries = []
    for i, placeholder in enumerate(placeholderArray):
        entry = ctk.CTkEntry(modal, placeholder_text=placeholder.get())
        entry.insert(0, values[i + 1])  # +1 to skip register_id
        entry.pack(pady=5)
        entries.append(entry)

    # Update button within modal
    def update_record():
        updated_values = [entry.get() for entry in entries]
        # Update the Treeview item with new values, except register_id
        my_tree.item(item_id, values=(my_tree.item(item_id)['values'][0], *updated_values))
        with connection() as conn:
            cursor = conn.cursor()
            sql = '''
            UPDATE reg
            SET 
            cedula = %s,
            contribuyente = %s,
            nombreinmueble = %s,
            rif = %s,
            sector = %s,
            uso = %s,
            codcatastral = %s,
            fechaliquidacion = %s
            WHERE register_id = %s
            '''
            cursor.execute(sql,(*updated_values, my_tree.item(item_id)['values'][0]))
            conn.commit()
        modal.destroy()

    update_button = ctk.CTkButton(modal, text="Actualizar", command=update_record)
    update_button.pack(pady=10)

