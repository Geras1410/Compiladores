from .Estado import Estado
from .ConjIj import ConjIj
from .AFD import AFD
import string  # Para obtener todos los símbolos ASCII

class AFN:
    contId = 0  # Variable estática para el conteo de estados

    def __init__(self):
        """
        Constructor de un AFN.
        :param id_afn: Identificador único del AFN.
        :param estado_inicial: Estado inicial del AFN.
        :param estado_final: Estado final del AFN.
        """
        self.id_afn = AFN.contId  # ID único del AFN hacerlo auto incremental
        AFN.contId += 1
        self.edo_inicial = None  # Estado inicial
        self.edos_afn = set()  # Conjunto de estados
        self.alfabeto = set()  # Alfabeto del AFN
        self.edos_acept = set()  # Conjunto de estados de aceptación

    def agregar_estado(self, estado):
        """
        Agrega un estado al conjunto de estados del AFN.
        :param estado: Estado a agregar.
        """
        self.edos_afn.add(estado)

    @staticmethod
    def afn_basico(simbolo, token=None):
        """
        Crea un AFN básico que reconoce un solo símbolo o un rango de símbolos.
        :param simbolo: El símbolo o rango de símbolos reconocido por el AFN.
        :param token: Token asociado al estado de aceptación (si es necesario).
        :return: Un AFN básico.
        """
        afn = AFN()  # Crea un nuevo AFN

        # Crear estado inicial y estado de aceptación
        estado_inicial = Estado()
        estado_aceptacion = Estado(es_aceptacion=True, token=token)

        # Crear la transición desde el estado inicial al de aceptación
        if isinstance(simbolo, list) and len(simbolo) == 2:
            # Si es un rango de símbolos, crear una transición para cada símbolo del rango
            for c in range(ord(simbolo[0]), ord(simbolo[1]) + 1):
                estado_inicial.agregar_transicion(chr(c), estado_aceptacion)
                afn.alfabeto.add(chr(c))  # Agregar al alfabeto
        else:
            # Si es un solo símbolo
            estado_inicial.agregar_transicion(simbolo, estado_aceptacion)
            afn.alfabeto.add(simbolo)

        # Asignar el estado inicial y el conjunto de estados de aceptación
        afn.edo_inicial = estado_inicial
        afn.edos_acept.add(estado_aceptacion)

        # Agregar los estados al conjunto de estados del AFN
        afn.agregar_estado(estado_inicial)
        afn.agregar_estado(estado_aceptacion)

        return afn

    def concatenar(self, afn2):
        """
        Concatenación de dos AFNs.
        :param afn2: Otro AFN a concatenar.
        :return: El AFN modificado tras la operación.
        """
        for transicion in afn2.edo_inicial.transiciones:
            for e in self.edos_acept:
                e.agregar_transicion(transicion.simbolo, transicion.estado_destino)
                e.es_aceptacion = False

        # Unir los conjuntos de estados
        self.edos_afn.update(afn2.edos_afn)
        self.edos_afn.remove(afn2.edo_inicial)

        # Actualizar el conjunto de estados de aceptación
        self.edos_acept.clear()
        self.edos_acept.update(afn2.edos_acept)
        self.alfabeto.update(afn2.alfabeto)

        return self

    def unir(self, afn2):
        """
        Unión de dos AFNs (OR).
        :param afn2: Otro AFN con el cual se realizará la unión.
        :return: El AFN modificado tras la operación.
        """
        #Crear nuevos estados e1 y e2
        e1 = Estado() #Nuevo edo inicial
        e2 = Estado(es_aceptacion=True) # Nuevo edo de aceptacion

        #Crear transiciones vacias desde e1 a los estados iniciales de ambos afn's
        e1.agregar_transicion('ε', self.edo_inicial)
        e1.agregar_transicion('ε', afn2.edo_inicial)

        #Reasignar transiciones desde los estados de aceptacion a ambos AFN's hacia el nuevo estado e2
        for e in self.edos_acept:
            e.agregar_transicion('ε', e2)
            e.es_aceptacion = False
        for e in afn2.edos_acept:
            e.agregar_transicion('ε', e2)
            e.es_aceptacion = False

        #Actualizar estado inicial y conjunto de esatdos de aceptacion
        self.edo_inicial = e1
        self.edos_acept.clear()
        self.edos_acept.add(e2)

        # Unir los conjuntos de estados y alfabeto
        self.edos_afn.update(afn2.edos_afn)
        self.edos_afn.add(e1)
        self.edos_afn.add(e2)
        self.alfabeto.update(afn2.alfabeto)

        return self

    def cerradura(self):
        """
        Aplicación de la cerradura (cierre de Kleene).
        :return: El AFN modificado tras la operación.
        """
        e1 = Estado()  # Nuevo estado inicial
        e2 = Estado(es_aceptacion=True)  # Nuevo estado de aceptación

        # Agregar transiciones desde e1 hacia el estado inicial actual y el nuevo estado de aceptación
        e1.agregar_transicion('ε', self.edo_inicial)
        e1.agregar_transicion('ε', e2)

        # Agregar transiciones desde los estados de aceptación actuales hacia el nuevo estado de aceptación y el inicial
        for e in self.edos_acept:
            e.agregar_transicion('ε', e2)
            e.agregar_transicion('ε', self.edo_inicial)
            e.es_aceptacion = False

        # Actualizar el estado inicial y el conjunto de estados de aceptación
        self.edo_inicial = e1
        self.edos_acept.clear()
        self.edos_acept.add(e2)

        # Agregar los nuevos estados al conjunto de estados
        self.edos_afn.add(e1)
        self.edos_afn.add(e2)

        return self

    def cierre_kleene(self, nuevo_id):
        """
        Cerradura de Kleene aplicada al AFN.
        :return: El AFN modificado tras la operación.
        """
        self.cerradura()  # Aplicar la cerradura regular
        self.edo_inicial.agregar_transicion('ε', next(iter(self.edos_acept)))  # Agregar transición de la inicial al estado de aceptación
        return self

    def opcional(self):
        """
        Aplicación de la operación opcional (a|ε).
        :return: El AFN modificado tras la operación.
        """
        e1 = Estado()  # Nuevo estado inicial
        e2 = Estado(es_aceptacion=True)  # Nuevo estado de aceptación

        # Agregar transiciones desde e1 al estado inicial actual y al nuevo estado de aceptación
        e1.agregar_transicion('ε', self.edo_inicial)
        e1.agregar_transicion('ε', e2)

        # Agregar transiciones vacías desde los estados de aceptación actuales al nuevo estado de aceptación
        for e in self.edos_acept:
            e.agregar_transicion('ε', e2)
            e.es_aceptacion = False

        # Actualizar estado inicial y conjunto de estados de aceptación
        self.edo_inicial = e1
        self.edos_acept.clear()
        self.edos_acept.add(e2)

        # Agregar nuevos estados al conjunto de estados
        self.edos_afn.add(e1)
        self.edos_afn.add(e2)

        return self

    def go_to(self, conjunto_estados, simbolo):
        """
        Obtiene el conjunto de estados alcanzables desde un conjunto de estados dado con un símbolo específico.
        :param conjunto_estados: El conjunto de estados desde los que se desea mover.
        :param simbolo: El símbolo por el cual se hará la transición.
        :return: Un conjunto de estados alcanzables.
        """
        resultado = set()

        # Para cada estado en el conjunto de entrada
        for estado in conjunto_estados:
            # Revisar cada transición del estado
            for transicion in estado.transiciones:
                # Verificar si el símbolo está dentro del conjunto de símbolos de la transición
                if simbolo in transicion.simbolo:
                    resultado.add(transicion.estado_destino)

        return resultado

    def cerradura_epsilon(self, conjunto_estados):
        """
        Calcula el conjunto de estados alcanzables desde un conjunto de estados utilizando transiciones ε.
        :param conjunto_estados: El conjunto de estados desde los cuales se calculará la cerradura-ε.
        :return: El conjunto de estados alcanzables mediante transiciones ε.
        """
        # Inicializar el resultado con los estados de entrada
        resultado = set(conjunto_estados)

        # Pila para procesar los estados (inicialmente con los estados dados)
        pila = list(conjunto_estados)

        # Mientras haya estados en la pila
        while pila:
            # Tomar un estado de la pila
            estado_actual = pila.pop()

            # Revisar las transiciones desde el estado actual
            for transicion in estado_actual.transiciones:
                # Si la transición es por ε
                if transicion.simbolo == 'ε' and transicion.estado_destino not in resultado:
                    # Agregar el estado destino al resultado
                    resultado.add(transicion.estado_destino)
                    # Agregar el estado destino a la pila para seguir procesando
                    pila.append(transicion.estado_destino)

        return resultado

    def mover(self, conjunto_estados, simbolo):
        """
        Calcula el conjunto de estados alcanzables desde un conjunto de estados dado mediante una transición con el símbolo proporcionado.
        :param conjunto_estados: El conjunto de estados desde los cuales se desea mover.
        :param simbolo: El símbolo de la transición.
        :return: Un conjunto de estados alcanzables mediante el símbolo.
        """
        resultado = set()

        # Para cada estado en el conjunto de entrada
        for estado in conjunto_estados:
            # Revisar cada transición del estado
            for transicion in estado.transiciones:
                # Si la transición tiene el símbolo dado, agregar el estado destino al resultado
                if transicion.simbolo == simbolo:
                    resultado.add(transicion.estado_destino)

        return resultado

    def convertir_a_afd(self):
        """
        Convierte un AFN a un AFD usando el método de subconjuntos.
        :return: El AFD generado.
        """
        # Paso 1: Crear el AFD con el número máximo de estados posibles (inicialmente desconocido)
        afd = AFD(0)

        # Paso 2: Inicializamos la lista de subconjuntos, partiendo de la cerradura epsilon del estado inicial
        S0 = self.cerradura_epsilon({self.edo_inicial})
        subconjuntos = [S0]  # Lista que almacena los subconjuntos
        conjIj_list = [ConjIj()]  # Lista de subconjuntos procesados
        conjIj_list[0].ConjI = S0  # Asignar el primer subconjunto a ConjIj

        # Mapeo del subconjunto al ID del AFD
        subconjunto_a_id = {frozenset(S0): 0}

        # La tabla AFD comenzará a llenarse con transiciones para cada símbolo ASCII
        afd.tablaAFD = []

        # Procesar cada subconjunto (inicialmente solo tenemos S0)
        for i, subconjunto in enumerate(subconjuntos):
            conjIj = conjIj_list[i]  # Obtener el conjunto ConjIj correspondiente
            conjIj.TransicionesAFD[0] = i  # ID del estado en la primera columna

            # Verificar si este subconjunto contiene algún estado de aceptación
            es_aceptacion = any(estado in self.edos_acept for estado in subconjunto)
            conjIj.TransicionesAFD[-1] = 1 if es_aceptacion else -1  # -1 para no aceptación

            # Ahora recorremos todos los símbolos ASCII
            for simbolo_ascii in range(255):
                simbolo = chr(simbolo_ascii)

                # Aplicar la función go_to para este subconjunto con el símbolo actual
                nuevo_conjunto = self.go_to(subconjunto, simbolo)
                nuevo_conjunto = self.cerradura_epsilon(nuevo_conjunto)

                if nuevo_conjunto:  # Si hay algún estado alcanzable
                    # Si este nuevo conjunto no está en los subconjuntos procesados, lo agregamos
                    if frozenset(nuevo_conjunto) not in subconjunto_a_id:
                        subconjunto_a_id[frozenset(nuevo_conjunto)] = len(subconjuntos)
                        subconjuntos.append(nuevo_conjunto)
                        conjIj_list.append(ConjIj())  # Agregar un nuevo conjunto ConjIj

                    # Obtener el ID del nuevo conjunto y guardar la transición
                    id_nuevo_conjunto = subconjunto_a_id[frozenset(nuevo_conjunto)]
                    conjIj.TransicionesAFD[simbolo_ascii + 1] = id_nuevo_conjunto

        # Una vez completados todos los subconjuntos y transiciones, actualizar la tablaAFD
        afd.num_estados = len(subconjuntos)
        afd.tablaAFD = [conj.TransicionesAFD for conj in conjIj_list]

        return afd

    def mostrar_afn(self):
        """
        Muestra los estados, transiciones y símbolos del AFN.
        """
        print(f"AFN ID: {self.id_afn}")
        print("Estados del AFN:")

        for estado in self.edos_afn:
            # Indicar si el estado es de aceptación y mostrar el token
            aceptacion_str = "Sí" if estado.es_aceptacion else "No"
            token_str = f"Token: {estado.token}" if estado.token else "No Token"

            print(f"Estado {estado.id_estado}: Aceptación: {aceptacion_str}, {token_str}")

            # Mostrar todas las transiciones del estado
            for transicion in estado.transiciones:
                print(
                    f"  - Transición con símbolo '{transicion.simbolo}' hacia Estado {transicion.estado_destino.id_estado}")

        print("\nAlfabeto:", self.alfabeto)
        print("Estados de aceptación:", [estado.id_estado for estado in self.edos_acept])
        print("Estado inicial:", self.edo_inicial.id_estado)
        print("----------\n")
