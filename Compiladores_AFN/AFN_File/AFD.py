import csv

class AFD:
    def __init__(self, numero_estados):
        """
        Constructor que inicializa la tabla de transiciones y el número de estados.
        :param numero_estados: Número de estados en el AFD.
        """
        self.alfabeto = []  # Alfabeto (lista de caracteres)
        self.num_estados = numero_estados
        self.tablaAFD = [[-1 for _ in range(258)] for _ in range(numero_estados)]  # Tabla de transiciones
        self.id = 0  # ID autoincremental

    def guardar_AFD_archivo(self, nombre_archivo):
        """
        Guarda el AFD en un archivo.
        :param nombre_archivo: Nombre del archivo donde se guardará el AFD.
        """
        with open(nombre_archivo, 'w', newline='') as archivo:
            writer = csv.writer(archivo)
            # Guardar el número de estados
            writer.writerow([self.num_estados])
            # Guardar cada fila de la tabla AFD
            for fila in self.tablaAFD:
                fila_str = ','.join(map(str, fila))
                writer.writerow([fila_str])

    def leer_AFD_archivo(self, nombre_archivo):
        """
        Lee el AFD desde un archivo.
        :param nombre_archivo: Nombre del archivo desde donde se leerá el AFD.
        """
        with open(nombre_archivo, 'r') as archivo:
            reader = csv.reader(archivo)
            # Leer el número de estados
            self.num_estados = int(next(reader)[0])
            # Leer la tabla de transiciones
            self.tablaAFD = []
            for row in reader:
                # Convertir la cadena de una fila en una lista de enteros
                fila = list(map(int, row[0].split(',')))
                self.tablaAFD.append(fila)
