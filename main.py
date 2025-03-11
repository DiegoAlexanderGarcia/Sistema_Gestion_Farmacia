import json
import os
from datetime import datetime
import msvcrt

def esperar_tecla():
    print("\nPresione cualquier tecla para continuar...")
    msvcrt.getch()

class SistemaFarmacia:
    def __init__(self):
        self.archivo_medicamentos = 'medicamentos.json'
        self.archivo_ventas = 'ventas.json'
        self.archivo_compras = 'compras.json'
        self.medicamentos = self.cargar_datos(self.archivo_medicamentos)
        self.ventas = self.cargar_datos(self.archivo_ventas)
        self.compras = self.cargar_datos(self.archivo_compras)

    def cargar_datos(self, archivo):
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def guardar_datos(self, datos, archivo):
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def buscar_medicamento_por_id(self, id_medicamento):
        for med in self.medicamentos:
            if med['id'] == id_medicamento:
                return med
        return None

    def registrar_venta(self):
        os.system('cls')
        print("\n=== Registrar Venta ===")
        
        # Mostrar medicamentos disponibles
        print("\nMedicamentos disponibles:")
        print("ID  | Nombre           | Stock | Precio")
        print("-" * 50)
        for med in self.medicamentos:
            print(f"{med['id']:<4} | {med['nombre']:<16} | {med['stock']:<6} | ${med['precio']:.2f}")

        while True:
            try:
                id_med = int(input("\nID del medicamento: ").strip())
                medicamento = self.buscar_medicamento_por_id(id_med)
                if medicamento is None:
                    print("Medicamento no encontrado.")
                    continue
                break
            except ValueError:
                print("Por favor ingrese un número válido.")

        while True:
            try:
                cantidad = int(input("Cantidad a vender: ").strip())
                if cantidad <= 0:
                    print("La cantidad debe ser mayor que 0.")
                    continue
                if cantidad > medicamento['stock']:
                    print(f"Stock insuficiente. Stock actual: {medicamento['stock']}")
                    continue
                break
            except ValueError:
                print("Por favor ingrese un número válido.")

        total = medicamento['precio'] * cantidad

        # Registrar la venta
        venta = {
            "id": len(self.ventas) + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "medicamento_id": medicamento['id'],
            "medicamento_nombre": medicamento['nombre'],
            "cantidad": cantidad,
            "precio_unitario": medicamento['precio'],
            "total": total
        }

        # Actualizar stock
        medicamento['stock'] -= cantidad
        
        # Guardar cambios
        self.ventas.append(venta)
        self.guardar_datos(self.ventas, self.archivo_ventas)
        self.guardar_datos(self.medicamentos, self.archivo_medicamentos)

        # Mostrar resumen
        print("\n=== Resumen de la Venta ===")
        print(f"Medicamento: {medicamento['nombre']}")
        print(f"Cantidad: {cantidad}")
        print(f"Precio unitario: ${medicamento['precio']:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Stock restante: {medicamento['stock']}")
        esperar_tecla()

    def registrar_compra(self):
        os.system('cls')
        print("\n=== Registrar Compra ===")
        
        # Mostrar medicamentos existentes
        print("\nMedicamentos en el sistema:")
        print("ID  | Nombre           | Stock actual")
        print("-" * 50)
        for med in self.medicamentos:
            print(f"{med['id']:<4} | {med['nombre']:<16} | {med['stock']:<6}")

        while True:
            try:
                id_med = int(input("\nID del medicamento (0 para nuevo): ").strip())
                if id_med == 0:
                    return self.agregar_medicamento()
                medicamento = self.buscar_medicamento_por_id(id_med)
                if medicamento is None:
                    print("Medicamento no encontrado.")
                    continue
                break
            except ValueError:
                print("Por favor ingrese un número válido.")

        while True:
            try:
                cantidad = int(input("Cantidad comprada: ").strip())
                if cantidad <= 0:
                    print("La cantidad debe ser mayor que 0.")
                    continue
                break
            except ValueError:
                print("Por favor ingrese un número válido.")

        while True:
            try:
                precio_compra = float(input("Precio de compra unitario: ").strip())
                if precio_compra <= 0:
                    print("El precio debe ser mayor que 0.")
                    continue
                break
            except ValueError:
                print("Por favor ingrese un número válido.")

        total = precio_compra * cantidad

        # Registrar la compra
        compra = {
            "id": len(self.compras) + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "medicamento_id": medicamento['id'],
            "medicamento_nombre": medicamento['nombre'],
            "cantidad": cantidad,
            "precio_unitario": precio_compra,
            "total": total
        }

        # Actualizar stock
        medicamento['stock'] += cantidad
        
        # Guardar cambios
        self.compras.append(compra)
        self.guardar_datos(self.compras, self.archivo_compras)
        self.guardar_datos(self.medicamentos, self.archivo_medicamentos)

        # Mostrar resumen
        print("\n=== Resumen de la Compra ===")
        print(f"Medicamento: {medicamento['nombre']}")
        print(f"Cantidad: {cantidad}")
        print(f"Precio unitario: ${precio_compra:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Nuevo stock: {medicamento['stock']}")
        esperar_tecla()

    def ver_historial_ventas(self):
        os.system('cls')
        if not self.ventas:
            print("\nNo hay ventas registradas.")
            esperar_tecla()
            return

        print("\n=== Historial de Ventas ===")
        print("ID  | Fecha                | Medicamento      | Cant | P.Unit  | Total")
        print("-" * 75)
        for venta in self.ventas:
            print(f"{venta['id']:<4} | {venta['fecha']} | {venta['medicamento_nombre']:<15} | {venta['cantidad']:<5} | ${venta['precio_unitario']:<7.2f} | ${venta['total']:.2f}")
        esperar_tecla()

    def ver_historial_compras(self):
        os.system('cls')
        if not self.compras:
            print("\nNo hay compras registradas.")
            esperar_tecla()
            return

        print("\n=== Historial de Compras ===")
        print("ID  | Fecha                | Medicamento      | Cant | P.Unit  | Total")
        print("-" * 75)
        for compra in self.compras:
            print(f"{compra['id']:<4} | {compra['fecha']} | {compra['medicamento_nombre']:<15} | {compra['cantidad']:<5} | ${compra['precio_unitario']:<7.2f} | ${compra['total']:.2f}")
        esperar_tecla()

    def agregar_medicamento(self):
        os.system('cls')
        print("\n=== Agregar Nuevo Medicamento ===")
        
        while True:
            nombre = input("Nombre del medicamento: ").strip()
            if nombre:
                break
            print("El nombre no puede estar vacío.")

        descripcion = input("Descripción: ").strip()

        while True:
            try:
                precio_str = input("Precio de venta: ").strip()
                if not precio_str:
                    continue
                precio = float(precio_str)
                if precio > 0:
                    break
                print("El precio debe ser mayor que 0")
            except ValueError:
                print("Por favor ingrese un número válido")

        while True:
            try:
                stock_str = input("Stock inicial: ").strip()
                if not stock_str:
                    continue
                stock = int(stock_str)
                if stock >= 0:
                    break
                print("El stock no puede ser negativo")
            except ValueError:
                print("Por favor ingrese un número entero")

        proveedor = input("Proveedor: ").strip()

        while True:
            try:
                fecha = input("Fecha de vencimiento (YYYY-MM-DD): ").strip()
                if not fecha:
                    continue
                datetime.strptime(fecha, "%Y-%m-%d")
                break
            except ValueError:
                print("Formato de fecha inválido. Use YYYY-MM-DD")

        medicamento = {
            "id": len(self.medicamentos) + 1,
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "stock": stock,
            "proveedor": proveedor,
            "fecha_vencimiento": fecha
        }

        self.medicamentos.append(medicamento)
        self.guardar_datos(self.medicamentos, self.archivo_medicamentos)

        os.system('cls')
        print("\n¡Medicamento agregado exitosamente!")
        print("\nDetalles del medicamento:")
        print(f"ID: {medicamento['id']}")
        print(f"Nombre: {medicamento['nombre']}")
        print(f"Precio: ${medicamento['precio']:.2f}")
        print(f"Stock: {medicamento['stock']}")
        print(f"Proveedor: {medicamento['proveedor']}")
        print(f"Fecha de vencimiento: {medicamento['fecha_vencimiento']}")
        esperar_tecla()

    def mostrar_medicamentos(self):
        os.system('cls')
        if not self.medicamentos:
            print("\nNo hay medicamentos registrados.")
            esperar_tecla()
            return

        print("\n=== Inventario de Medicamentos ===")
        print("ID  | Nombre           | Stock | Precio  | Vencimiento")
        print("-" * 60)
        for med in self.medicamentos:
            print(f"{med['id']:<4} | {med['nombre']:<16} | {med['stock']:<6} | ${med['precio']:<7.2f} | {med['fecha_vencimiento']}")
        esperar_tecla()

def main():
    sistema = SistemaFarmacia()
    
    while True:
        os.system('cls')
        print("=== SISTEMA DE GESTIÓN DE FARMACIA ===")
        print("1. Agregar medicamento")
        print("2. Ver inventario")
        print("3. Registrar venta")
        print("4. Registrar compra")
        print("5. Ver historial de ventas")
        print("6. Ver historial de compras")
        print("0. Salir")
        
        try:
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                sistema.agregar_medicamento()
            elif opcion == "2":
                sistema.mostrar_medicamentos()
            elif opcion == "3":
                sistema.registrar_venta()
            elif opcion == "4":
                sistema.registrar_compra()
            elif opcion == "5":
                sistema.ver_historial_ventas()
            elif opcion == "6":
                sistema.ver_historial_compras()
            elif opcion == "0":
                print("\n¡Gracias por usar el sistema!")
                esperar_tecla()
                break
            else:
                print("\nOpción no válida.")
                esperar_tecla()
        except Exception as e:
            print(f"\nError: {str(e)}")
            esperar_tecla()

if __name__ == "__main__":
    main()
