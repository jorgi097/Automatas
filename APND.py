class APND:
    # Constructor del APND
    def __init__(self, estados, alfabeto, alfabeto_pila, transiciones, estado_inicial, simbolo_pila_inicial, estados_aceptacion):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.alfabeto_pila = set(alfabeto_pila)
        self.transiciones = transiciones # {(estado_actual, simbolo_entrada, simbolo_pila): [(nuevo_estado, cadena_reemplazo_pila), ...]}
        self.estado_inicial = estado_inicial
        self.simbolo_pila_inicial = simbolo_pila_inicial
        self.estados_aceptacion = set(estados_aceptacion)
        
    # Determina si el APND acepta la cadena dada
    def acepta(self, cadena):

        # Configuración inicial: estado actual, posición en cadena, y pila
        configuraciones = {(self.estado_inicial, 0, (self.simbolo_pila_inicial,))}
        
        while configuraciones:
            nuevas_configuraciones = set()
            
            for (estado_actual, pos, pila) in configuraciones:
                # Verificar si estamos en un estado de aceptación (por estado final o pila vacía)
                if (estado_actual in self.estados_aceptacion) or (not pila and self.aceptacion_por_pila_vacia()):
                    return True
                
                # Obtener el próximo símbolo de entrada (o ε si hemos terminado la cadena)
                simbolo_entrada = cadena[pos] if pos < len(cadena) else None
                
                # Obtener el símbolo en el tope de la pila (o ε si la pila está vacía)
                tope_pila = pila[-1] if pila else None
                
                # Procesar transiciones con el símbolo de entrada actual (incluyendo ε)
                for entrada in [simbolo_entrada, None]:
                    if (estado_actual, entrada, tope_pila) in self.transiciones:
                        for (nuevo_estado, reemplazo_pila) in self.transiciones[(estado_actual, entrada, tope_pila)]:
                            # Manejar la pila
                            nueva_pila = list(pila[:-1])  # Eliminar el tope
                            nueva_pila.extend(reemplazo_pila[::-1])  # Agregar los nuevos símbolos en orden correcto
                            
                            # Calcular nueva posición (avanzar solo si no fue transición ε)
                            nueva_pos = pos + (1 if entrada is not None else 0)
                            
                            nuevas_configuraciones.add((nuevo_estado, nueva_pos, tuple(nueva_pila)))
            
            configuraciones = nuevas_configuraciones
        
        return False
    
    # Determina si el APND acepta por pila vacía (En este ejemplo simple, asumimos que acepta por estado final)
    def aceptacion_por_pila_vacia(self):
        return False


# Ejemplo de uso: APND para el lenguaje {0^n 1^n | n >= 1}

# Definición del APND
estados = {'q0', 'q1', 'q2', 'q3'}
alfabeto = {'0', '1'}
alfabeto_pila = {'Z', '0'}
transiciones = {
    # Transiciones para 0s: apilar 0s
    ('q0', '0', 'Z'): [('q0', '0Z')],
    ('q0', '0', '0'): [('q0', '00')],
    
    # Transición para el primer 1: cambiar a q1
    ('q0', '1', '0'): [('q1', '')],
    
    # Transiciones para 1s: desapilar 0s
    ('q1', '1', '0'): [('q1', '')],
    
    # Transición ε al final: si Z está en el tope, ir a estado de aceptación
    ('q1', None, 'Z'): [('q2', '')]
}
estado_inicial = 'q0'
simbolo_pila_inicial = 'Z'
estados_aceptacion = {'q2'}

# Crear el APND
apnd = APND(estados, alfabeto, alfabeto_pila, transiciones, estado_inicial, simbolo_pila_inicial, estados_aceptacion)

# Probar algunas cadenas
cadenas_prueba = ['01', '0011', '000111', '001', '0101', '']
for cadena in cadenas_prueba:
    resultado = "acepta" if apnd.acepta(cadena) else "rechaza"
    print(f"El APND {resultado} la cadena '{cadena}'")