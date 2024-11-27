import customtkinter as ctk
import pymysql
from tkinter import messagebox
from tkinter import ttk
import csv 
import sqlite3


placeholder_texts = ["Cedula", "Contribuyente", "Nombre Inmueble", "RIF", "Sector", "Cod Catastral", "Fecha Liquidación", "Pago", "Monto"]
button_poppins = ("poppins", 16, "bold") 
placeholder_poppins = ("poppins", 12, "normal") 

# Funcion para establecer la conexion con la db

def connection():
    return sqlite3.connect('./regdb.db')

def read():
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """SELECT register_id, cedula, contribuyente, nombreinmueble, rif, sector, 
                     uso, codcatastral, fechaliquidacion, pago, monto FROM reg ORDER BY fechaliquidacion DESC"""
            cursor.execute(sql)
            results = cursor.fetchall()

            # Check if results are empty
            if not results:
                print("No records found.")
            else:
                for row in results:
                    print(row)  # Print each record for debugging

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
        print(f'Results type: {type(results)}')
        for i, array in enumerate(results):
            tag = "evenrow" if i % 2 == 0 else "oddrow" # Altenar los colores establecidos en my_tree.tag_configure
            my_tree.insert(parent='', index='end', text="", values=array, tag=tag)

    # Configuracion para las filas de registros
    my_tree.tag_configure('evenrow', background="#EEEEEE")
    my_tree.tag_configure('oddrow', background="#FFFFFF") 

# Funcion para guardar los datos en la db

def save(cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry, pago, montoEntry, my_tree):

    # Obtenemos los datos de los placeholder/entry's

    cedula = cedulaEntry.get().strip()
    contribuyente = contribuyenteEntry.get().strip()
    nombreinmueble = nombreinmuebleEntry.get().strip()
    rif = rifEntry.get().strip()
    sector = sectorEntry.get().strip()
    uso = usoEntry.get().strip()
    codcatastral = codcatastralEntry.get().strip()
    fechaliquidacion = fechaliquidacionEntry.get().strip()
    pago = pago.strip()  # Ensure this is a string
    monto = montoEntry.get().strip()

    # Verificamos si todos los campos estan llenos

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
                     uso, codcatastral, fechaliquidacion, pago, monto) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion, pago, monto))
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
                sql = """SELECT register_id, cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion 
                         FROM reg ORDER BY fechaliquidacion DESC"""
                cursor.execute(sql)
                results = cursor.fetchall()
                refreshTable(my_tree, results)
                return

            # Si se provee una cedula devuelve unicamene que los registros asociados con esa cedula
            sql = """SELECT register_id, cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion, pago, monto 
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

def open_save_popup(my_tree):
    """Open a popup window to input data for a new register."""
    window = ctk.CTk()
    popup = ctk.CTkToplevel(window)
    popup.title("Nuevo Registro")
    popup.geometry("400x500")
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

    pago_frame = ctk.CTkFrame(popup)  # Create a frame to hold the dropdown
    pago_frame.pack(padx=5, pady=5, fill="x")  # Pack the frame with a fill option if needed

    pago_options = ["Yes", "No"]  # You can add other options here if needed
    pago_dropdown = ctk.CTkOptionMenu(pago_frame, values=pago_options, font=placeholder_poppins)
    pago_dropdown.pack(padx=5, pady=5, side="left")

    monto_popup = ctk.CTkEntry(popup, placeholder_text="Monto", font=placeholder_poppins, width=380)
    monto_popup.pack(padx=5, pady=5)


    # Save button within popup
    def save_popup_data():
        save(cedula_popup, contribuyente_popup, nombreinmueble_popup, rif_popup, sector_popup, uso_popup, codcatastral_popup, fechaliquidacion_popup, pago_dropdown.get(), monto_popup, my_tree)
        #1messagebox.showinfo(title="Ventana Guardado", message="El registro se guardo existosamente")  
        popup.destroy()  # Close popup after saving

    save_button = ctk.CTkButton(popup, text="Save", command=save_popup_data, font=button_poppins, width=380)
    save_button.pack(pady=10)

###########################################################################################################################################
######################################### Pop-up update window / Modal###########################################################
######################################### Ventana modal para actualizar###########################################################
###########################################################################################################################################

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
            cedula = ?,
            contribuyente = ?,
            nombreinmueble = ?,
            rif = ?,
            sector = ?,
            uso = ?,
            codcatastral = ?,
            fechaliquidacion = ?
            pago = ?
            monto = ?
            WHERE register_id = ?
            '''
            cursor.execute(sql,(*updated_values, my_tree.item(item_id)['values'][0]))
            conn.commit()
        results = read()
        refreshTable(my_tree, results)
        messagebox.showinfo(title="Actualización de registro",message="Registro actualizado exitosamente")
        modal.destroy()

    update_button = ctk.CTkButton(modal, text="Actualizar", command=update_record)
    update_button.pack(pady=10)

