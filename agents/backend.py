"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa el cambio aprobado con alcance controlado.

Debes:
- preservar contratos y criterios de aceptación;
- hacer cambios pequeños y coherentes;
- ejecutar pruebas relevantes y reportar evidencia real;
- mantener fuera del cambio los hallazgos secundarios no aprobados;
- registrar riesgos residuales cuando aplique.

No debes:
- ampliar el alcance por deuda no aprobada;
- desactivar tests o gates para forzar resultados;
- inventar resultados de pruebas;
- cambiar contratos sin aprobación.
"""
agent = Agent(role='Desarrollador backend', goal="Implementar cambios backend aprobados con trazabilidad y calidad.",
              backstory="Eres un desarrollador backend de ReqFlow que implementa cambios aprobados de forma auditable y con disciplina de alcance.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    title = str(feature.get("title", ""))
    description = str(feature.get("description", ""))
    acceptance_criteria = str(feature.get("acceptance_criteria", []))
    task_description = (
        INSTRUCTIONS
        + "\nContexto del cambio aprobado:"
        + "\nTítulo: " + title
        + "\nDescripción: " + description
        + "\nCriterios de aceptación: " + acceptance_criteria
        + "\n\nTareas obligatorias:"
        + "\n1) Implementa únicamente backend para cumplir los criterios de aceptación."
        + "\n2) Mantén consistencia con el stack y convenciones del proyecto."
        + "\n3) Si detectas bloqueos o riesgos, documéntalos explícitamente."
        + "\n4) No inventes pruebas ni resultados; declara lo no verificado."
    )
    return Task(
        description=task_description,
        expected_output=(
            "Código en bloques markdown; primera línea con // Nombre.java y "
            "package pe.bcp.login.service. Incluye una sección final breve "
            "de evidencia con: criterios cubiertos, riesgos residuales y "
            "pendientes de validación."
        ),
        agent=agent
    )
