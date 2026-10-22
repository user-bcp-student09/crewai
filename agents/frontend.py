INSTRUCTIONS = """
Implementa la interacción frontend de la feature usando como fuentes de verdad
sus criterios de aceptación y los contratos aprobados de Arquitectura y Backend
incluidos en el contexto. No inventes endpoints, campos, formatos, códigos de
error ni reglas de navegación. Si falta un dato o los contratos se contradicen,
márcalo como PENDIENTE DE CONFIRMAR y evita ocultar esa limitación.

Entrega primero el contenido de frontend_spec.md con:
- Recorrido del usuario, acciones disponibles y resultado de cada acción.
- Campos: etiqueta visible, tipo de control, obligatoriedad, validación,
  mensaje de error y regla del contrato que la justifica.
- Endpoint y método aprobados, modelo de petición y respuesta, errores
  documentados y navegación posterior al éxito. Marca lo no definido.
- Estados de carga, inicial/vacío, éxito y error; acciones permitidas en cada
  estado y mensajes visibles. Para una feature sin listado, define el estado
  inicial sin inventar resultados vacíos.
- Comprobaciones reproducibles para éxito, validación, errores de API y red,
  reintento y envío duplicado. Incluye npm run build y npm start, y marca
  NO EJECUTADO cualquier comprobación que no hayas ejecutado.

Implementa el recorrido en Angular 17, coherente con el scaffolding existente.
Usa Reactive Forms para formularios, HttpClient para consumir la API y los
modelos del contrato aprobado. La validación del cliente mejora la experiencia,
pero no sustituye la validación del servidor. Evita solicitudes duplicadas:
bloquea reenvíos mientras haya una petición en curso y restablece el estado
también cuando falle.

Incluye carga accesible, mensajes de error accionables y reintento cuando
corresponda. Conserva etiquetas asociadas a controles, errores vinculados con
aria-describedby, anuncios de estado apropiados, navegación por teclado y foco
visible. No dependas solo del color para comunicar estados.

Después de la especificación, entrega todos los archivos necesarios para el
recorrido como bloques de código independientes. La primera línea de cada
bloque debe identificar el archivo con un comentario válido para su tipo:
TypeScript: // nombre.ts
HTML: <!-- nombre.html -->
CSS: /* nombre.css */
Usa nombres de archivo que el extractor reconozca y no mezcles archivos en un
mismo bloque. No afirmes que compilaste o ejecutaste pruebas si no lo hiciste.
"""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

agent = Agent(
    role='Desarrollador frontend',
    goal="Completar la tarea asignada.",
    backstory="Eres un integrante del equipo.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'Contenido de frontend_spec.md y código Angular 17 en bloques separados; '
                    'cada bloque empieza con un comentario de nombre de archivo válido para '
                    'su tipo y compatible con el extractor.'
                ),
                agent=agent)