from fastapi import FastAPI
from pydantic import BaseModel
import networkx as nx
from fastapi.middleware.cors import CORSMiddleware
import random


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (en producción, restringe esto)
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

G = nx.DiGraph()
nodos = [
    ("CRM", "Gestión de Clientes"),
    ("CRM", "Automatización de Marketing"),
    ("CRM", "Análisis de Ventas"),
    ("CRM", "Atención al Cliente"),
    ("Gestión de Clientes", "Segmentación de Clientes"),
    ("Gestión de Clientes", "Customer Journey"),
    ("Gestión de Clientes", "Personalización"),
    ("Segmentación de Clientes", "Segmentación Demográfica"),
    ("Segmentación de Clientes", "Segmentación por Comportamiento"),
    ("Automatización de Marketing", "Automatización de Emails"),
    ("Automatización de Marketing", "Lead Scoring"),
    ("Automatización de Marketing", "Automatización de Flujos de Trabajo"),
    ("Lead Scoring", "Cualificación de Leads"),
    ("Análisis de Ventas", "Análisis Predictivo"),
    ("Análisis de Ventas", "Dashboard de Ventas"),
    ("Atención al Cliente", "Chatbots"),
    ("Atención al Cliente", "Soporte Omnicanal"),
    ("Atención al Cliente", "Bases de Conocimiento"),
    ("Publicidad Digital", "Google Ads"),
    ("Publicidad Digital", "Facebook Ads"),
]
G.add_edges_from(nodos)

def generar_descripcion(nodo):
    """Genera una descripción más natural para un concepto basado en sus relaciones."""
    descripciones = [
        f"{nodo} es una estrategia clave en CRM utilizada para mejorar la gestión y relación con los clientes.",
        f"{nodo} optimiza procesos de negocio y facilita la toma de decisiones estratégicas dentro del CRM.",
        f"{nodo} permite automatizar tareas, segmentar clientes y mejorar la personalización en estrategias de marketing."
    ]
    descripcion = random.choice(descripciones) + " "
    
    padres = list(G.predecessors(nodo))
    hijos = list(G.successors(nodo))
    
    if padres:
        descripcion += f"Está vinculado con {', '.join(padres)}, lo que potencia su funcionalidad en la gestión empresarial. "
    
    if hijos:
        descripcion += f"Dentro de sus aplicaciones se incluyen {', '.join(hijos)}, que optimizan la experiencia del cliente y la eficiencia operativa. "
    
    return descripcion

def responder_pregunta(pregunta):
    pregunta = pregunta.lower()
    conceptos_encontrados = [nodo for nodo in G.nodes if nodo.lower() in pregunta]
    
    if not conceptos_encontrados:
        return "No tengo información exacta sobre eso, pero puedo explicarte cómo funciona en CRM si me das más contexto."
    
    if "qué es" in pregunta:
        return generar_descripcion(conceptos_encontrados[0])
    
    if "para qué sirve" in pregunta:
        nodo = conceptos_encontrados[0]
        return f"{nodo} ayuda a las empresas a mejorar su eficiencia operativa, reducir costos y optimizar estrategias en CRM. Por ejemplo, se usa en {', '.join(G.successors(nodo))} para personalizar la comunicación y segmentar clientes."
    
    if "beneficios de" in pregunta:
        nodo = conceptos_encontrados[0]
        return f"Los beneficios de {nodo} incluyen mayor productividad, mejor segmentación y toma de decisiones basada en datos. Su uso en {', '.join(G.successors(nodo))} mejora la fidelización y conversión de clientes."
    
    if "cómo se aplica" in pregunta:
        nodo = conceptos_encontrados[0]
        return f"{nodo} se implementa en CRM a través de herramientas digitales y estrategias de automatización. Por ejemplo, se puede integrar con software de CRM para mejorar la segmentación y personalización."
    
    if "cómo se relaciona" in pregunta and len(conceptos_encontrados) == 2:
        nodo1, nodo2 = conceptos_encontrados[:2]
        if G.has_edge(nodo1, nodo2):
            return f"{nodo2} es un componente clave dentro de {nodo1}, ayudando a optimizar procesos y mejorar la toma de decisiones en CRM."
        elif G.has_edge(nodo2, nodo1):
            return f"{nodo1} y {nodo2} están directamente relacionados en CRM, combinando automatización y análisis de datos para mejorar la eficiencia."
        else:
            caminos = list(nx.all_simple_paths(G, source=nodo1, target=nodo2))
            if caminos:
                camino_texto = " → ".join(caminos[0])
                return f"{nodo1} y {nodo2} están conectados en CRM a través de esta relación: {camino_texto}."
            return f"Aunque {nodo1} y {nodo2} no tienen una conexión directa, pueden complementarse en estrategias como la automatización de marketing y la segmentación de clientes."
    
    if "diferencia entre" in pregunta and len(conceptos_encontrados) == 2:
        nodo1, nodo2 = conceptos_encontrados[:2]
        return f"{nodo1} y {nodo2} tienen enfoques distintos en CRM. Mientras que {nodo1} se centra en {random.choice(G.successors(nodo1) or ['su aplicación específica'])}, {nodo2} es más utilizado para {random.choice(G.successors(nodo2) or ['su optimización estratégica'])}."
    
    return "Buena pregunta. Si puedes darme más detalles, podré darte una mejor respuesta."

# Modelo Pydantic para la solicitud
class PreguntaRequest(BaseModel):
    pregunta: str

# Ruta para responder preguntas
@app.post("/pregunta")
async def pregunta(pregunta_request: PreguntaRequest):
    pregunta = pregunta_request.pregunta
    respuesta = responder_pregunta(pregunta)
    return {"respuesta": respuesta}

# Ruta de prueba
@app.get("/")
async def root():
    return {"message": "Bienvenido al Asistente Virtual de CRM"}
