import random

# Definición del APND
alfabeto = {'0', '1'}
alfabeto_pila = {'Z', 'a'}
estados = {'q1', 'q2', 'q3', 'qf'}
estado_inicial = 'q1'
simbolo_pila_inicial = 'Z'
estados_aceptacion = {'qf'}
transiciones = {
    ('q1', '0'): [('q2', 'a', '')],
    ('q2', '1'): [('q3', 'a', ''), ('qf', 'a', '')],
    ('q3', '0'): [('q3', 'a', '')],
    ('q3', '1'): [('q1', '', 'a')],
}

def procesar(cadena, alfabeto, alfabeto_pila, estados, estado_inicial, 
             simbolo_pila_inicial, estados_aceptacion, transiciones):
    # Inicializar la pila y el estado actual
    pila = [simbolo_pila_inicial]
    estado_actual = estado_inicial

    # Procesar cada símbolo de la cadena
    for simbolo in cadena:
        if simbolo not in alfabeto:
            return False  # Símbolo no válido en la cadena

        # Verificar si existe una transición para (estado_actual, simbolo)
        if (estado_actual, simbolo) not in transiciones:
            return False

        opciones = transiciones[(estado_actual, simbolo)]
        transicion_encontrada = False  # Inicializar al inicio de cada iteración
        (nuevo_estado, push, pop) = random.choice(opciones) # Elegir una transición aleatoria
        
        if pop:
            if pila and pila[-1] == pop:
                pila.pop()
            else:
                return False  # La opción elegida no es válida
        
        if push:
            pila.append(push)
        
        estado_actual = nuevo_estado
        transicion_encontrada = True

        if not transicion_encontrada:
            return False

    # La cadena es aceptada si se termina en un estado de aceptación
    return estado_actual in estados_aceptacion

# Probar  cadenas
cadenas_prueba = ['01', '01', '01', '01101', '01101', '01101', '001', '100']

for cadena in cadenas_prueba:
    resultado = procesar(cadena, alfabeto, alfabeto_pila, estados, estado_inicial, simbolo_pila_inicial, estados_aceptacion, transiciones)
    print(f"Cadena: {cadena} - {'Aceptada' if resultado else 'No aceptada'}")