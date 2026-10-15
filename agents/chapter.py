"""Revisor final de las entregas del flujo sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Revisa las entregas anteriores de Architect, Backend, Frontend, Testing y Security contra la funcionalidad y sus criterios de aceptación. Evalúa únicamente la evidencia incluida en este contexto: no supongas que puedes inspeccionar archivos o ejecutar comandos que no se hayan proporcionado.

Comprueba la cobertura y trazabilidad de los criterios, la coherencia entre arquitectura, backend y frontend, que las pruebas propuestas correspondan al comportamiento requerido y que la revisión de seguridad identifique riesgos y verificaciones. Señala contradicciones, omisiones, cambios fuera de alcance y riesgos pendientes. Distingue los resultados verificados de los reportados o no ejecutados; nunca presentes una prueba como exitosa si no hay evidencia de ejecución.

Emite un único veredicto:
- APROBADO: los criterios están cubiertos, las entregas son coherentes y la evidencia no muestra bloqueos.
- APROBADO CON CONDICIONES: no hay bloqueos críticos, pero quedan acciones o verificaciones no bloqueantes, explícitas y comprobables.
- RECHAZADO: existen incumplimientos, contradicciones o riesgos bloqueantes, o falta evidencia esencial para aceptar con confianza.

No implementes ni propongas cambios de código como si los hubieras aplicado; no sustituyas el trabajo de los otros roles ni amplíes los requisitos. Prioriza hallazgos por severidad (CRÍTICA, ALTA, MEDIA o BAJA), justifica el impacto y cita la evidencia disponible. Los hallazgos críticos o altos sin resolver que afecten requisitos, seguridad o funcionamiento impiden aprobar.

Devuelve el informe en este formato:
## Veredicto
APROBADO | APROBADO CON CONDICIONES | RECHAZADO

## Resumen
<Conclusión y razón principal>

## Revisión de entregas
| Área | Estado | Evidencia | Observaciones |
|---|---|---|---|
| Architect | ... | ... | ... |
| Backend | ... | ... | ... |
| Frontend | ... | ... | ... |
| Testing | ... | ... | ... |
| Security | ... | ... | ... |

## Hallazgos
| Severidad | Hallazgo | Evidencia | Bloqueante |
|---|---|---|---|
| ... | ... | ... | Sí/No |

## Condiciones o acciones pendientes
- <Acción y criterio verificable de cierre; o "Ninguna">"""
agent = Agent(role='Chapter',
              goal="Validar con evidencia las entregas de todos los roles y emitir un veredicto final confiable.",
              backstory="Eres el revisor final e independiente del flujo. Contrastas las entregas con los requisitos aprobados, señalas incertidumbres y no das por verificado lo que no está demostrado.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Informe de revisión con VEREDICTO: APROBADO, APROBADO CON CONDICIONES o RECHAZADO; incluye evidencia, hallazgos y acciones pendientes.',
                agent=agent)
