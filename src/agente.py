import json, sys, subprocess, pathlib, pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
RAIZ = pathlib.Path(__file__).parent.parent

def correr_suite(ruta_tests: str) -> str:
    r = subprocess.run(
        ["pytest", ruta_tests, "-v", "--tb=short"],
        capture_output=True, text=True, cwd=RAIZ, encoding="utf-8", errors="replace",
    )
    return r.stdout + r.stderr

def diagnosticar(log: str, codigo: str) -> list:
    prompt = (RAIZ / "prompts" / "diagnosticar.md").read_text(encoding="utf-8")
    r = Anthropic().messages.create(
        model="claude-sonnet-5",
        max_tokens=8000,
        system=prompt,
        messages=[{"role": "user", "content": f"SALIDA DE PYTEST:\n{log}\n\nCODIGO DE LOS TESTS:\n{codigo}"}],
    )
    texto = "".join(b.text for b in r.content if b.type == "text")
    return json.loads(texto.strip().removeprefix("```json").removesuffix("```").strip())

def main(archivo_test: str):
    ruta = f"tests/{archivo_test}"
    print(f"[1/3] Ejecutando {ruta}...")
    log = correr_suite(ruta)

    resumen = [l for l in log.splitlines() if "passed" in l or "failed" in l]
    print(f"[2/3] {resumen[-1].strip() if resumen else 'sin resumen'}")

    if " failed" not in log:
        print("[3/3] Sin fallos. Nada que diagnosticar.")
        return

    codigo = (RAIZ / "tests" / archivo_test).read_text(encoding="utf-8")
    print("[3/3] Diagnosticando fallos...")
    hallazgos = diagnosticar(log, codigo)

    salida = RAIZ / "outputs" / "diagnostico.csv"
    pd.DataFrame(hallazgos).to_csv(salida, index=False, encoding="utf-8-sig")

    for h in hallazgos:
        print(f"  {h['clasificacion']:8} | {h['caso']} | {h['diagnostico']}")
    print(f"\nDiagnóstico -> {salida}")

if __name__ == "__main__":
    main(sys.argv[1])