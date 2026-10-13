# qa-agent

Agente que convierte un requerimiento en casos de prueba, los automatiza con Playwright, los ejecuta y diagnostica los fallos.

Nace de un problema real: en QA institucional, disenar casos y levantar defectos consume mas tiempo que probar.

## Flujo

    requerimiento.md
          |  [IA] diseno de casos
    casos.csv  (id, modulo, precondiciones, pasos, datos, resultado esperado, tipo, prioridad)
          |  [IA] generacion de codigo
    test_*.py  (pytest + Playwright)
          |  ejecucion real
    log de pytest
          |  [IA] diagnostico
    diagnostico.csv  (clasificacion + ticket redactado)

Los primeros dos pasos son generacion. El ultimo es donde el sistema deja de ser un script: lee el resultado de su propio trabajo y decide que significa.

## Resultados

Partiendo de un requerimiento de login de 6 lineas:

| Metrica | Valor |
|---|---|
| Casos de prueba generados | 23 |
| Tests automatizados ejecutables | 13 |
| Casos marcados como no automatizables | 10 |
| Tiempo de ejecucion de la suite | 20 s |
| Tiempo total del pipeline completo | ~3 min |
| Equivalente manual estimado | PENDIENTE |

## Diagnostico de fallos

El agente clasifica cada fallo en BUG, TEST, ENTORNO o FLAKY, y redacta el ticket solo cuando es un defecto real.

Ejemplo de una corrida con un fallo inducido a proposito:

> **TEST | CP-001** - El test usa la contrasena password_malo en lugar de la credencial valida secret_sauce, por lo que el login falla como es esperado dado el dato incorrecto; no es un fallo de la aplicacion, ya que CP-005 con la contrasena correcta paso exitosamente.

Clasifico correctamente como defecto del test y no de la aplicacion, cruzando el fallo contra otro test que si paso. Ese cruce no esta en el prompt: se deduce del contexto de la corrida.

## Stack

Python - Claude API - Playwright - pytest - pandas

## Uso

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    playwright install chromium

Crea un archivo .env con tu llave:

    ANTHROPIC_API_KEY=tu_key

Luego:

    python src/generar_casos.py login.md
    python src/generar_specs.py login_casos.csv
    python src/agente.py test_login.py

## Estructura

    requerimientos/   entrada: requerimientos en markdown
    prompts/          instrucciones de cada etapa
    src/              los tres ejecutables del pipeline
    tests/            specs generados
    outputs/          casos y diagnosticos (ignorados por git)

## Limitaciones conocidas

- Los casos que dependen de estado previo (bloqueo tras N intentos, usuario inactivo) se marcan como no automatizables. Requieren control de base de datos que el sitio de prueba no expone.
- Los selectores se declaran en el prompt. Un cambio de UI obliga a actualizarlos a mano.
- Probado contra SauceDemo. Apuntar a otra aplicacion exige reescribir el bloque de selectores.

## Que sigue

- [ ] Integracion con Mantis via API para abrir el defecto automaticamente
- [ ] Reintento automatico de fallos clasificados como FLAKY
- [ ] Reporte Allure
