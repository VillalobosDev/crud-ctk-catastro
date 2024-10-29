
import pymysql
from tkinter import messagebox
import csv
from customtkinter import CTkEntry
from tkinter import ttk

def some_function(my_tree, placeholderArray):
    # Now placeholderArray is defined here and can be used.
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
        sql = """SELECT cedula, contribuyente, nombreinmueble, rif, sector, 
                 uso, codcatastral, fechaliquidacion FROM reg ORDER BY fechaliquidacion DESC"""
        cursor.execute(sql)
        results = cursor.fetchall()
    return results

def refreshTable(my_tree, results=None):
    # Clear existing items in the tree
    for data in my_tree.get_children():
        my_tree.delete(data)

    # If results are provided, insert them into the tree
    if results:
        for array in results:
            my_tree.insert(parent='', index='end', text="", values=array, tag="orow")

    my_tree.tag_configure('orow', background="#EEEEEE")

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

def update(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry, placeholderArray):
    if not my_tree.selection():
        messagebox.showwarning("", "Por favor selecciona un elemento para actualizar.")
        return

    selectedItem = my_tree.selection()[0]
    item_values = my_tree.item(selectedItem)['values']

    if not item_values or len(item_values) < 8:
        messagebox.showwarning("", "El elemento seleccionado no tiene valores completos.")
        return

    selectedItemId = str(item_values[0])

    cedula = cedulaEntry.get().strip()
    contribuyente = contribuyenteEntry.get().strip()
    nombreinmueble = nombreinmuebleEntry.get().strip()
    rif = rifEntry.get().strip()
    sector = sectorEntry.get().strip()
    uso = usoEntry.get().strip()
    codcatastral = codcatastralEntry.get().strip()
    fechaliquidacion = fechaliquidacionEntry.get().strip()

    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """UPDATE reg 
                     SET cedula = %s, contribuyente = %s, nombreinmueble = %s, 
                         rif = %s, sector = %s, uso = %s, codcatastral = %s, 
                         fechaliquidacion = %s 
                     WHERE cedula = %s"""

            cursor.execute(sql, (cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion, selectedItemId))
            conn.commit()

        for num in range(len(placeholderArray)):
            setph('', num, placeholderArray)
        refreshTable(my_tree)

    except Exception as err:
        messagebox.showwarning("", "Un error se produjo: " + str(err))

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

def select(my_tree, placeholderArray):
    try:
        selectedItem = my_tree.selection()[0]
        cedula = str(my_tree.item(selectedItem)['values'][0])
        contribuyente = str(my_tree.item(selectedItem)['values'][1])
        nombreinmueble = str(my_tree.item(selectedItem)['values'][2])
        rif = str(my_tree.item(selectedItem)['values'][3])
        sector = str(my_tree.item(selectedItem)['values'][4])
        uso = str(my_tree.item(selectedItem)['values'][5])
        codcatastral = str(my_tree.item(selectedItem)['values'][6])
        fechaliquidacion = str(my_tree.item(selectedItem)['values'][7])

        setph(cedula, 0, placeholderArray)
        setph(contribuyente, 1, placeholderArray)
        setph(nombreinmueble, 2, placeholderArray)
        setph(rif, 3, placeholderArray)
        setph(sector, 4, placeholderArray)
        setph(uso, 5, placeholderArray)
        setph(codcatastral, 6, placeholderArray)
        setph(fechaliquidacion, 7, placeholderArray)
    except:
        messagebox.showwarning("", "Por favor selecciona una columna")

def find(my_tree, cedulaEntry, contribuyenteEntry, nombreinmuebleEntry, rifEntry, sectorEntry, usoEntry, codcatastralEntry, fechaliquidacionEntry):
    try:
        with connection() as conn:
            cursor = conn.cursor()

            # Retrieve values from entry fields
            cedula = cedulaEntry.get().strip()
            contribuyente = contribuyenteEntry.get().strip()
            nombreinmueble = nombreinmuebleEntry.get().strip()
            rif = rifEntry.get().strip()
            sector = sectorEntry.get().strip()
            uso = usoEntry.get().strip()
            codcatastral = codcatastralEntry.get().strip()
            fechaliquidacion = fechaliquidacionEntry.get().strip()

            # If no entry fields are filled, get all records ordered by fechaliquidacion
            if not any([cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion]):
                sql = """SELECT cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion 
                         FROM reg ORDER BY fechaliquidacion DESC"""
                cursor.execute(sql)
                results = cursor.fetchall()
                refreshTable(my_tree, results)
                return

            # If a cedula is present, retrieve all records associated with that cedula
            if cedula:
                sql = """SELECT cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion 
                         FROM reg WHERE cedula = %s ORDER BY fechaliquidacion DESC"""
                cursor.execute(sql, (cedula,))
                results = cursor.fetchall()
                refreshTable(my_tree, results)
                if not results:  # If no results were found
                    messagebox.showwarning("", "No se encontraron registros para la cédula proporcionada.")
                return
            
            # This section allows flexible, partial searches based 
            # on any combination of fields the user fills, enabling a custom query without hard-coding each possible combination.

            # # If specific fields are filled, construct the query
            # fields = {
            #     'cedula': cedula,
            #     'contribuyente': contribuyente,
            #     'nombreinmueble': nombreinmueble,
            #     'rif': rif,
            #     'sector': sector,
            #     'uso': uso,
            #     'codcatastral': codcatastral,
            #     'fechaliquidacion': fechaliquidacion
            # }

            # query_conditions = []
            # query_values = []

            # for field, value in fields.items():
            #     if value:  # Only include non-empty fields in the query
            #         query_conditions.append(f"{field} LIKE %s")
            #         query_values.append(f'%{value}%')

            # if query_conditions:  # Only run this if there are conditions
            #     query = "SELECT cedula, contribuyente, nombreinmueble, rif, sector, uso, codcatastral, fechaliquidacion FROM reg WHERE " + " AND ".join(query_conditions) + " ORDER BY fechaliquidacion DESC"
            #     cursor.execute(query, query_values)
            #     results = cursor.fetchall()
                
            #     # Clear the treeview and insert new items
            #     refreshTable(my_tree, results)

            #     if not results:  # If no results were found
            #         messagebox.showwarning("", "No se encontraron registros.")
            # else:
            #     messagebox.showwarning("", "Por favor proporciona al menos un criterio de búsqueda.")

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