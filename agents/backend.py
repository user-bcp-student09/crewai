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
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
