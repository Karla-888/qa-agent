import sys, pathlib, pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
RAIZ = pathlib.Path(__file__).parent.parent

def generar(archivo_csv: str):
    casos = pd.read_csv(RAIZ / "outputs" / archivo_csv).to_json(orient="records", force_ascii=False)
    prompt = (RAIZ / "prompts" / "generar_specs.md").read_text(encoding="utf-8")

    r = Anthropic().messages.create(
        model="claude-sonnet-5",
        max_tokens=16000,
        system=prompt,
        messages=[{"role": "user", "content": f"Casos de prueba:\n\n{casos}"}],
    )
    texto = "".join(b.text for b in r.content if b.type == "text")
    codigo = texto.strip().removeprefix("```python").removesuffix("```").strip()

    salida = RAIZ / "tests" / f"test_{pathlib.Path(archivo_csv).stem.replace('_casos','')}.py"
    salida.write_text(codigo, encoding="utf-8")
    print(f"Specs -> {salida}")

if __name__ == "__main__":
    generar(sys.argv[1])