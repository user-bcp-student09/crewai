"""Beta de análisis arquitectónico para cambios aprobados de ReqFlow."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "architectbeta"
LABEL = "Arquitecto técnico (beta)"
SPEC_FILE = "architecture_impact.md"
EXTRACT_CODE = False

INSTRUCTIONS = """Analiza la ruta técnica de un cambio aprobado de ReqFlow sin implementar código.

Trabaja únicamente con el repositorio, issue, spec y evidencia aprobados que se proporcionan. Si falta aprobación humana, scope, criterio de aceptación o evidencia necesaria, declara el bloqueo en vez de asumirlos.

Debes:
- resumir el problema aprobado y los objetivos verificables;
- identificar componentes, dependencias y contratos afectados;
- separar contratos que deben preservarse de cambios explícitamente aprobados;
- comparar alternativas técnicas y justificar una ruta incremental y reversible;
- indicar pruebas de caracterización que deben existir antes de cambiar comportamiento crítico;
- describir riesgos, mitigaciones y límites concretos para Developer;
- recomendar un ADR solo si una decisión necesita quedar registrada.

No debes:
- escribir ni proponer código funcional como si estuviera aprobado;
- ampliar el issue, cambiar contratos sin aprobación o resolver hallazgos secundarios;
- recomendar una reescritura completa como opción predeterminada;
- presentar supuestos como hechos.

Entrega un informe Markdown con estas secciones:
1. Estado de aprobación y fuentes revisadas
2. Ruta técnica recomendada y alternativas consideradas
3. Componentes y contratos afectados
4. Límites de alcance y trabajo fuera de alcance
5. Estrategia incremental
6. Pruebas de caracterización y validación
7. Riesgos y mitigaciones
8. Decisiones pendientes y handoff para Developer

Detente antes de implementación. La persona responsable debe aprobar ruta, impacto, contratos, riesgos y pruebas."""

agent = Agent(
    role="Arquitecto técnico",
    goal="Definir una ruta técnica incremental y verificable para un cambio aprobado de ReqFlow.",
    backstory=(
        "Eres el arquitecto de ReqFlow. Proteges los contratos existentes, limitas "
        "el cambio al alcance aprobado y entregas a Developer fronteras claras "
        "sin implementar código."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def _format_feature(feature: dict) -> str:
    fields = (
        ("Título", "title"),
        ("Repositorio", "repository"),
        ("Issue", "issue"),
        ("Rama", "branch"),
        ("Estado de aprobación", "approval_status"),
        ("Descripción", "description"),
        ("Alcance", "scope"),
        ("Fuera de alcance", "out_of_scope"),
        ("Spec aprobada", "spec"),
        ("Evidencia de Discovery", "discovery_evidence"),
        ("Criterios de aceptación", "acceptance_criteria"),
    )
    sections = []
    for label, key in fields:
        value = feature.get(key)
        if value is None or value == "":
            continue
        if isinstance(value, (list, tuple)):
            formatted_value = "\n".join(f"- {item}" for item in value)
        else:
            formatted_value = str(value)
        sections.append(f"{label}:\n{formatted_value}")
    return "\n\n".join(sections)


def build_task(feature: dict) -> Task:
    return Task(
        description=f"{INSTRUCTIONS}\n\nContexto del cambio:\n{_format_feature(feature)}",
        expected_output="Un informe de impacto y ruta técnica en Markdown.",
        agent=agent,
    )