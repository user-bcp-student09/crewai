"""Define la arquitectura y el contrato verificable del Issue para el equipo."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """
Analiza el mismo Issue, sus criterios de aceptación y las interfaces y el código
del producto proporcionados en el contexto. Recibes el título, la descripción
del Issue y los criterios de aceptación; usa las referencias disponibles como
evidencia, sin afirmar que inspeccionaste código al que no tienes acceso.
Revisa también el código y las interfaces adjuntos a la tarea. Si no se adjuntan,
comprueba si la descripción del Issue contiene esa evidencia. Una ruta o URL por
sí sola no equivale a código inspeccionado. Si la evidencia sigue faltando,
solicítala al responsable del producto y marca como BLOQUEADO el análisis de
compatibilidad y las decisiones que dependan de ella; no cierres el contrato
como listo para implementación.

Define componentes, responsabilidades y límites del cambio. Distingue lo que
existe de lo propuesto, reutiliza las interfaces existentes y explica el recorrido
de una petición desde Frontend hasta Backend y persistencia, si corresponde.
Decide la distribución de responsabilidades y el contrato compartido, sin
implementar código ni diseñar migraciones que corresponden a otros agentes.
Respeta las restricciones tecnológicas del producto y del contexto del flujo.

Especifica para cada operación de API el método HTTP, ruta, autorización,
entradas de ruta, consulta y cuerpo, tipos, campos obligatorios y validaciones.
Define respuestas y errores con sus códigos HTTP, estructura y condiciones.
Incluye ejemplos coherentes de petición, respuesta válida y error; utiliza
datos ficticios, nunca secretos ni datos personales. Si no se necesita una API,
justifícalo y describe la interfaz afectada sin inventar endpoints.

Relaciona cada criterio de aceptación con el componente que lo resuelve, la
operación o interfaz afectada y una comprobación con entrada, acción y resultado
esperado. Conserva el texto original de cada criterio y asígnale un identificador.
Incluye casos válidos, inválidos y de límite cuando correspondan.

Declara supuestos, preguntas pendientes, riesgos y dependencias. Si faltan
criterios, código o interfaces, indícalo explícitamente: identifica la información
necesaria, el responsable de confirmarla y qué decisión queda bloqueada.
No presentes supuestos como contratos existentes o decisiones aprobadas.
Todo cambio de contrato de API, compatible o incompatible, debe quedar documentado
y pendiente de aprobación humana y coordinación entre Arquitectura, Backend y
Frontend antes de implementarse. Como Arquitecto, centraliza esa decisión y
registra el impacto en consumidores; para cambios incompatibles, define además
la estrategia de compatibilidad o migración.

Entrega únicamente el contenido Markdown de user_story.md, con componentes,
contrato de API y criterios verificables. Indica las decisiones que necesitan
Backend, Frontend, Testing, Security y Chapter, y Datos si participa; si no hay
agente de Datos, deriva la persistencia necesaria a Backend.
No inventes pruebas, resultados ni aprobaciones: separa la evidencia disponible
de las comprobaciones propuestas y marca estas últimas como NO EJECUTADO.
En un reintento, incorpora el feedback humano, explica las correcciones y conserva
los contratos no afectados. La entrega sigue sujeta a aprobación humana.
"""
agent = Agent(role='Arquitecto de solución y contratos de API',
              goal="Definir una solución acotada y un contrato de API coherente "
                   "con el Issue, las interfaces existentes y cada criterio de aceptación.",
              backstory="Eres responsable de la arquitectura compartida del equipo. "
                        "Conviertes el requisito y la evidencia del producto en "
                        "componentes, límites y contratos verificables para los "
                        "agentes posteriores. Explicas decisiones y alternativas, "
                        "haces visibles los bloqueos y no sustituyes la aprobación humana.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    """Acepta product_code y product_interfaces opcionales con evidencia del producto."""
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\nDescripción del Issue y contexto del producto:\n"
                + str(feature.get("description", ""))
                + "\nCriterios de aceptación originales:\n"
                + str(feature.get("acceptance_criteria", []))
                + "\nCódigo del producto adjunto (product_code):\n"
                + str(feature.get("product_code") or
                      "NO ADJUNTO: comprobar la descripción del Issue y solicitar evidencia si falta.")
                + "\nInterfaces del producto adjuntas (product_interfaces):\n"
                + str(feature.get("product_interfaces") or
                      "NO ADJUNTAS: comprobar la descripción del Issue y solicitar evidencia si falta."),
                expected_output="""Contenido Markdown de user_story.md con estas secciones:
1. Issue y alcance: objetivo, código e interfaces realmente revisados con sus
   referencias, evidencia faltante, cambio incluido y excluido.
2. Componentes y responsabilidades: existentes y propuestos, límites, dependencias
   y recorrido de una petición.
3. Contrato de API: operaciones, autorización, entradas tipadas y validaciones,
   respuestas, errores y ejemplos de petición, éxito y error; o justificación
   verificable si no aplica. Explicita compatibilidad y cambios pendientes de aprobación.
4. Criterios verificables: tabla con ID, criterio original, componente, operación
   o interfaz, entrada, acción, resultado esperado y evidencia o estado NO EJECUTADO.
5. Decisiones y coordinación: entregables para los siguientes roles y responsables
   de confirmar cualquier cambio de contrato, con estado de coordinación entre
   Arquitectura, Backend y Frontend y aprobación humana pendiente o respaldada por evidencia.
6. Supuestos y pendientes: preguntas, riesgos, bloqueos y evidencia necesaria;
   marca BLOQUEADO lo que dependa del código o interfaces ausentes e identifica
   al responsable de aportarlos; correcciones del feedback humano cuando corresponda.
No incluyas implementaciones ni afirmes resultados de pruebas no ejecutadas.""",
                agent=agent)
