# qa-agent

Agente que convierte un requerimiento en casos de prueba formales, los automatiza con Playwright, los ejecuta y diagnostica los fallos.

Nace de un problema real: en QA institucional, disenar casos y documentar defectos consume mas tiempo que probar. Y el entregable no es un CSV cualquiera, es un formato con estructura definida.

## Flujo

    requerimiento.md
          |  [IA] diseno de casos
    casos.csv  (clasificados por flujo: basico / alterno / integridad / otras)
          |  [IA] generacion de codigo
    test_*.py  (pytest + Playwright)
          |  ejecucion real
    log de pytest
          |  [IA] diagnostico
    diagnostico.csv  (clasificacion del fallo + ticket redactado)
          |  consolidacion
    DA-F05.xlsx  (entregable formal, con resultados ya llenados)

Los primeros dos pasos son generacion. El cuarto es donde el sistema deja de ser un script: lee el resultado de su propio trabajo y decide que significa.

## El entregable

La salida no es un CSV generico: es el formato DA-F05 de Casos de Prueba de Integracion y Negocio, con la estructura que se usa en QA institucional.

- Clasificacion por flujos basicos, alternos o de excepcion, integridad de datos y otras pruebas
- Numeracion de CP que reinicia dentro de cada flujo
- Precondiciones generales, objetivo y componentes involucrados
- Columnas de ejecucion (Estatus, Resultado del CP, Hallazgos) que se llenan solas con la salida del diagnostico
- Bloque de estadisticas al cierre

Ese ultimo punto es el que mas tiempo ahorra: el agente ejecuta, clasifica el fallo y el documento formal sale lleno.

## Resultados

Partiendo de un requerimiento de login de 6 lineas:

| Metrica | Valor |
|---|---|
| Casos de prueba disenados | 15 |
| Tests automatizados ejecutables | 13 |
| Casos marcados como no automatizables | 10 |
| Tiempo de ejecucion de la suite | 20 s |
| Tiempo total del pipeline completo | ~3 min |
| Equivalente manual estimado | PENDIENTE |

El prompt prohibe inventar casos para rellenar flujos que no aplican al alcance. Menos casos, mejor clasificados.

## Diagnostico de fallos

El agente clasifica cada fallo en BUG, TEST, ENTORNO o FLAKY, y redacta el ticket solo cuando es un defecto real.

Ejemplo de una corrida con un fallo inducido a proposito:

> **TEST | CP-001** - El test usa la contrasena password_malo en lugar de la credencial valida secret_sauce, por lo que el login falla como es esperado dado el dato incorrecto; no es un fallo de la aplicacion, ya que CP-005 con la contrasena correcta paso exitosamente.

Clasifico correctamente como defecto del test y no de la aplicacion, cruzando el fallo contra otro test que si paso. Ese cruce no esta en el prompt: se deduce del contexto de la corrida.

Criterio de registro: un fallo clasificado como TEST, ENTORNO o FLAKY no se marca como "Paso" en el documento. Queda como "Reejecutar". Un test mal escrito no es evidencia de que el sistema funcione.

## Stack

Python - Claude API - Playwright - pytest - pandas - openpyxl

## Uso

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    playwright install chromium

Crea un archivo .env con tu llave:

    ANTHROPIC_API_KEY=tu_key

Luego:

    python src/generar_casos.py login.md               # requerimiento -> casos
    python src/exportar_da_f05.py login_casos.csv      # casos -> DA-F05
    python src/generar_specs.py login_casos.csv        # casos -> tests
    python src/agente.py test_login.py                 # ejecuta + diagnostica
    python src/exportar_da_f05.py login_casos.csv      # DA-F05 con resultados

## Estructura

    requerimientos/   entrada: requerimientos en markdown
    prompts/          instrucciones de cada etapa del pipeline
    src/              los cuatro ejecutables
    tests/            specs generados
    outputs/          casos, diagnosticos y DA-F05 (ignorados por git)

Los prompts estan separados del codigo a proposito. Cuando el agente se equivoca, el arreglo casi siempre va en el prompt, no en Python.

## Limitaciones conocidas

- Los casos que dependen de estado previo (bloqueo tras N intentos, usuario inactivo) se marcan como no automatizables. Requieren control de base de datos que el sitio de prueba no expone.
- Los selectores se declaran en el prompt. Un cambio de UI obliga a actualizarlos a mano.
- Probado contra SauceDemo. Apuntar a otra aplicacion exige reescribir el bloque de selectores.
- Los metadatos del DA-F05 (proyecto, sistema, modulo) se editan en el script, no se infieren del requerimiento.

## Que sigue

- [ ] Integracion con Mantis via API para abrir el defecto automaticamente
- [ ] Reintento automatico de fallos clasificados como FLAKY
- [ ] Inferir los metadatos del DA-F05 desde el requerimiento
- [ ] Reporte Allure
