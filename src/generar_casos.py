import json, sys, pathlib, pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
RAIZ = pathlib.Path(__file__).parent.parent

def generar(archivo_req: str):
    req = (RAIZ / "requerimientos" / archivo_req).read_text(encoding="utf-8")
    prompt = (RAIZ / "prompts" / "casos_de_prueba.md").read_text(encoding="utf-8")

    r = Anthropic().messages.create(
        model="claude-sonnet-5",
        max_tokens=8000,
        system=prompt,
        messages=[{"role": "user", "content": f"Requerimiento:\n\n{req}"}],
    )
    texto = "".join(b.text for b in r.content if b.type == "text")
    texto = texto.strip().removeprefix("```json").removesuffix("```").strip()
    casos = json.loads(texto)

    salida = RAIZ / "outputs" / f"{pathlib.Path(archivo_req).stem}_casos.csv"
    pd.DataFrame(casos).to_csv(salida, index=False, encoding="utf-8-sig")
    print(f"{len(casos)} casos -> {salida}")

if __name__ == "__main__":
    generar(sys.argv[1])