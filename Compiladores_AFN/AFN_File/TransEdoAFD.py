class TransEdoAFD:
    def __init__(self, id_edo, num_simbolos=258):
        """
        Constructor para la clase TransEdoAFD.
        :param id_edo: Identificador del estado.
        :param num_simbolos: Número de símbolos para las transiciones (258 en este caso).
        """
        self.id_edo = id_edo  # ID del estado
        self.transAFD = [-1] * num_simbolos  # Inicializar transiciones con -1 (sin transición)

    def set_transicion(self, simbolo, id_edo_destino):
        """
        Establece una transición desde este estado hacia otro estado dado un símbolo.
        :param simbolo: El símbolo de la transición (usualmente el valor ASCII).
        :param id_edo_destino: El estado destino para esta transición.
        """
        self.transAFD[ord(simbolo)] = id_edo_destino

    def get_transicion(self, simbolo):
        """
        Obtiene el estado destino de la transición dado un símbolo.
        :param simbolo: El símbolo para el cual se busca la transición.
        :return: El estado destino si existe la transición, de lo contrario -1.
        """
        return self.transAFD[ord(simbolo)]

    def __repr__(self):
        """
        Representación en texto del estado y sus transiciones.
        """
        transiciones = [(chr(i), t) for i, t in enumerate(self.transAFD) if t != -1]
        return f"Estado {self.id_edo}, Transiciones: {transiciones}"
