"""Agente CrewAI para diseñar suites y ciclos de prueba trazables."""

import json

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "testing2"
LABEL = "Testing integral"
SPEC_FILE = "testing2_report.md"
EXTRACT_CODE = False

INSTRUCTIONS = """Eres responsable de diseñar la validación integral de un cambio aprobado.
Usa como fuentes el feature, sus criterios de aceptación y las salidas aprobadas de
Architect, Backend y Frontend que aparezcan en el contexto de pasos anteriores. Si
se proporcionan artefactos de Discovery o PM-PO, úsalos solo si están aprobados.

No asumas que una propuesta o un hallazgo candidato está aprobado. Si faltan
criterios, contratos, resultados esperados o entregas necesarias, indícalo como
BLOQUEADO y señala qué rol debe aportar o aprobar la información faltante.

Para cada criterio aprobado, diseña happy paths y unhappy paths aplicables, además
de límites, validaciones, errores y regresiones pertinentes al cambio. Organiza los
casos en test sets de backend, frontend, contrato/integración, regresión y E2E según
corresponda. Justifica los sets que no apliquen.

Define ciclos ordenados con prerequisitos, alcance, comandos, evidencia esperada y
criterios de entrada/salida: preparación y smoke; pruebas de componente; contrato e
integración; regresión/E2E; y retest tras correcciones. No impongas ciclos que el
repositorio no soporte: marca su estado y justifica la decisión.

Inspecciona los comandos documentados o configurados en el contexto. Indica
directorio, runtime, servicios y datos sintéticos necesarios. No inventes comandos,
umbrales de cobertura ni comportamiento esperado. No uses datos productivos,
secretos, servicios externos ni pruebas destructivas.

Este agente no dispone de un ejecutor de comandos en el pipeline actual. Por ello,
describe los comandos y los resultados esperados, pero marca las pruebas como
NO EJECUTADAS salvo que se aporte evidencia verificable de CI o de una ejecución
real. Nunca declares passed basándote solo en que diseñaste el caso.

Si un caso falla, clasifica el fallo y entrega evidencia al rol responsable
(Developer, Backend o Frontend). No cambies el criterio ni debilites la prueba para
ocultar el fallo. Exige retest del caso y regresión pertinente antes de avanzar.

El siguiente gate es Security. Solo marca LISTO PARA SECURITY cuando todos los
criterios estén trazados, los casos obligatorios aplicables tengan evidencia de
ejecución satisfactoria, los fallos estén retesteados y los gaps/riesgos estén
documentados. Si no hay evidencia de ejecución o quedan fallos, marca PENDIENTE y
no declares completado el traspaso. La revisión funcional de Testing no sustituye
la revisión de seguridad."""

agent = Agent(
    role="Ingeniero de pruebas integrales",
    goal=(
        "Diseñar suites y ciclos reproducibles que validen los criterios aprobados "
        "con cobertura de happy y unhappy paths, y preparar evidencia fiable para "
        "el gate posterior de Security."
    ),
    backstory=(
        "Eres especialista QA en sistemas full-stack. Trabajas a partir de "
        "requisitos, riesgos, contratos y entregas aprobadas; haces explícitos "
        "los gaps y nunca afirmas resultados que no hayan sido ejecutados."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    approved_role_outputs = feature.get("approved_role_outputs", {})
    if isinstance(approved_role_outputs, str):
        role_context = approved_role_outputs
    else:
        role_context = json.dumps(
            approved_role_outputs,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

    description = (
        INSTRUCTIONS
        + "\n\n## Feature\n"
        + str(feature.get("title", ""))
        + "\n\n## Descripción\n"
        + str(feature.get("description", ""))
        + "\n\n## Criterios de aceptación\n"
        + json.dumps(feature.get("acceptance_criteria", []), ensure_ascii=False, indent=2)
        + "\n\n## Salidas aprobadas por rol incluidas en feature\n"
        + (role_context or "No se proporcionaron salidas en approved_role_outputs.")
        + "\n\nUsa también el contexto de pasos anteriores que el workflow agregue a esta tarea."
    )

    return Task(
        description=description,
        expected_output=(
            "Un informe Markdown testing2_report.md con alcance y fuentes aprobadas; "
            "matriz criterio-escenario-prueba-evidencia; happy/unhappy paths; test "
            "sets y ciclos con prerequisitos, comandos y criterios de entrada/salida; "
            "resultados separados entre ejecutados y no ejecutados; defectos, retests, "
            "gaps, riesgos residuales y estado explícito del gate: BLOQUEADO, "
            "PENDIENTE o LISTO PARA SECURITY."
        ),
        agent=agent,
    )