import networkx as nx

# Crear un grafo dirigido que represente los componentes de un CRM
G = nx.DiGraph()

# Definir nodos y relaciones (aristas) entre los componentes del CRM
nodos = [
    ("CRM", "Gestión de Clientes"),
    ("CRM", "Automatización de Marketing"),
    ("CRM", "Análisis de Ventas"),
    ("Gestión de Clientes", "Clientes Actuales"),
    ("Gestión de Clientes", "Clientes Potenciales"),
    ("Automatización de Marketing", "Campañas"),
    ("Automatización de Marketing", "Segmentación"),
    ("Análisis de Ventas", "Previsión de Ventas"),
    ("Análisis de Ventas", "Informes de Desempeño"),
    ("Análisis de Ventas", "Análisis de Tendencias"),
    ("Clientes Actuales", "Soporte al Cliente"),
    ("Clientes Actuales", "Fidelización"),
    ("Clientes Potenciales", "Generación de Leads"),
    ("Clientes Potenciales", "Calificación de Leads"),
    ("Campañas", "Campañas de Email"),
    ("Campañas", "Campañas en Redes Sociales"),
    ("Segmentación", "Segmentación Demográfica"),
    ("Segmentación", "Segmentación por Comportamiento"),
    ("Email Marketing", "Plantillas de Email"),
    ("Email Marketing", "Automatización de Emails"),
]

G.add_edges_from(nodos)

def responder_pregunta(pregunta):
    pregunta = pregunta.lower()

    # Caso 1: Pregunta del tipo "¿Qué es <concepto>?"
    for nodo in G.nodes:
        if f"qué es {nodo.lower()}" in pregunta:
            subtemas = list(G.successors(nodo))
            if subtemas:
                return f"{nodo} es un componente del CRM que abarca aspectos como: {', '.join(subtemas)}."
            else:
                return f"{nodo} es un elemento del CRM sin subcategorías definidas en este modelo."

    # Caso 2: Pregunta sobre la relación entre dos conceptos
    conceptos = [nodo for nodo in G.nodes if nodo.lower() in pregunta]
    if len(conceptos) == 2:
        nodo1, nodo2 = conceptos
        if G.has_edge(nodo1, nodo2):
            return f"{nodo2} forma parte de {nodo1} en la estructura del CRM."
        elif G.has_edge(nodo2, nodo1):
            return f"{nodo1} forma parte de {nodo2} en la estructura del CRM."
        else:
            return f"{nodo1} y {nodo2} están relacionados en el CRM, pero no existe una conexión directa en este modelo."

    return "Lo siento, no tengo información sobre esa consulta en el contexto del CRM."