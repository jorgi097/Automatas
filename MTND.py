class MTND:
    def __init__(self, estados, alfabeto, alfabeto_cinta, transiciones, estado_inicial, blanco, estados_aceptacion):
        """
        Inicializa la Máquina de Turing No Determinista (MTND)
        
        :param estados: Conjunto de estados (list/set)
        :param alfabeto: Alfabeto de entrada (list/set)
        :param alfabeto_cinta: Alfabeto de la cinta (list/set)
        :param transiciones: Diccionario de transiciones 
                            formato: {(estado_actual, simbolo_cinta): [(nuevo_estado, simbolo_escribir, movimiento), ...]}
                            movimiento puede ser 'L' (izquierda), 'R' (derecha) o 'S' (permanecer)
        :param estado_inicial: Estado inicial (str)
        :param blanco: Símbolo blanco de la cinta (str)
        :param estados_aceptacion: Conjunto de estados de aceptación (list/set)
        """
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.alfabeto_cinta = set(alfabeto_cinta)
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.blanco = blanco
        self.estados_aceptacion = set(estados_aceptacion)
        
    def acepta(self, cadena):
        """
        Determina si la MTND acepta la cadena dada
        
        :param cadena: Cadena de entrada a verificar
        :return: True si la cadena es aceptada, False en caso contrario
        """
        # Configuración inicial: estado actual, cinta y posición de la cabeza
        configuracion_inicial = (self.estado_inicial, list(cadena), 0)
        configuraciones = {configuracion_inicial}
        
        while configuraciones:
            nuevas_configuraciones = set()
            
            for (estado_actual, cinta, posicion) in configuraciones:
                # Verificar si estamos en un estado de aceptación
                if estado_actual in self.estados_aceptacion:
                    return True
                
                # Obtener el símbolo actual de la cinta (blanco si está fuera de los límites)
                simbolo_actual = cinta[posicion] if 0 <= posicion < len(cinta) else self.blanco
                
                # Verificar si hay transiciones definidas para el estado actual y símbolo
                if (estado_actual, simbolo_actual) in self.transiciones:
                    for (nuevo_estado, simbolo_escribir, movimiento) in self.transiciones[(estado_actual, simbolo_actual)]:
                        # Crear una copia de la cinta para cada transición posible
                        nueva_cinta = list(cinta)
                        
                        # Asegurarse de que la posición actual existe en la cinta
                        if 0 <= posicion < len(nueva_cinta):
                            nueva_cinta[posicion] = simbolo_escribir
                        else:
                            # Si estamos fuera de los límites, expandir la cinta
                            if posicion < 0:
                                nueva_cinta.insert(0, simbolo_escribir)
                                posicion = 0  # Ajustar posición después de insertar al inicio
                            else:
                                nueva_cinta.append(simbolo_escribir)
                        
                        # Calcular nueva posición según el movimiento
                        if movimiento == 'L':
                            nueva_posicion = posicion - 1
                        elif movimiento == 'R':
                            nueva_posicion = posicion + 1
                        else:  # 'S' para permanecer
                            nueva_posicion = posicion
                        
                        # Agregar la nueva configuración al conjunto
                        nuevas_configuraciones.add((nuevo_estado, nueva_cinta, nueva_posicion))
            
            configuraciones = nuevas_configuraciones
        
        return False


# Ejemplo de uso: MTND que acepta el lenguaje {ww | w ∈ {0,1}*}

# Definición de la MTND
estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q_accept'}
alfabeto = {'0', '1'}
alfabeto_cinta = {'0', '1', 'X', 'Y', '_'}
transiciones = {
    # Fase 1: Marcar el primer símbolo
    ('q0', '0'): [('q1', 'X', 'R')],
    ('q0', '1'): [('q1', 'Y', 'R')],
    ('q0', 'X'): [('q_accept', 'X', 'S')],  # Cadena vacía
    ('q0', 'Y'): [('q_accept', 'Y', 'S')],  # Cadena vacía
    
    # Fase 2: Moverse al final de la cadena
    ('q1', '0'): [('q1', '0', 'R')],
    ('q1', '1'): [('q1', '1', 'R')],
    ('q1', 'X'): [('q1', 'X', 'R')],
    ('q1', 'Y'): [('q1', 'Y', 'R')],
    ('q1', '_'): [('q2', '_', 'L')],
    
    # Fase 3: Marcar el último símbolo (debe coincidir con el primero)
    ('q2', '0'): [('q3', 'X', 'L')],
    ('q2', '1'): [('q3', 'Y', 'L')],
    
    # Fase 4: Volver al inicio
    ('q3', '0'): [('q3', '0', 'L')],
    ('q3', '1'): [('q3', '1', 'L')],
    ('q3', 'X'): [('q0', 'X', 'R')],
    ('q3', 'Y'): [('q0', 'Y', 'R')],
    
    # Estado de aceptación (por si acaso)
    ('q_accept', '_'): [('q_accept', '_', 'S')]
}
estado_inicial = 'q0'
blanco = '_'
estados_aceptacion = {'q_accept'}

# Crear la MTND
mtnd = MTND(estados, alfabeto, alfabeto_cinta, transiciones, estado_inicial, blanco, estados_aceptacion)

# Probar algunas cadenas
cadenas_prueba = ['', '00', '11', '0101', '0110', '0011', '0000', '01', '001']
for cadena in cadenas_prueba:
    resultado = "acepta" if mtnd.acepta(cadena) else "rechaza"
    print(f"La MTND {resultado} la cadena '{cadena}'")