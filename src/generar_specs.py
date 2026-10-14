import json, sys, pathlib, re, pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
RAIZ = pathlib.Path(__file__).parent.parent


def bloque_sitio(cfg: dict) -> str:
    s = cfg["selectores"]
    c = cfg["credenciales"]
    lineas = [
        f"Sitio bajo prueba: {cfg['nombre']} - {cfg['url']}",
        "",
        "Selectores:",
        f"- usuario: {s['usuario']}",
        f"- contrasena: {s['contrasena']}",
        f"- boton login: {s['boton_login']}",
        f"- mensaje de error: {s['mensaje_error']}",
        f"- elemento post-login: {s['elemento_post_login']} (texto \"{s['texto_post_login']}\")",
        "",
        "Credenciales reales del sitio:",
        f"- validas: {c['validas']['usuario']} / {c['validas']['contrasena']}",
    ]
    if c.get("bloqueado"):
        lineas.append(f"- usuario bloqueado: {c['bloqueado']['usuario']} / {c['bloqueado']['contrasena']}")
    else:
        lineas.append("- este sitio no tiene usuario bloqueado: marca con skip los casos que lo requieran")
    lineas += [
        "",
        f"Notas del sitio: {cfg['notas']}",
        "",
        "Para casos de login exitoso usa SIEMPRE las credenciales reales de arriba, ignorando los datos genericos del caso.",
    ]
    return "\n".join(lineas)


def generar(archivo_csv: str, sitio: str):
    cfg = json.loads((RAIZ / "sitios" / f"{sitio}.json").read_text(encoding="utf-8"))
    casos = pd.read_csv(RAIZ / "outputs" / archivo_csv).to_json(orient="records", force_ascii=False)
    prompt = (RAIZ / "prompts" / "generar_specs.md").read_text(encoding="utf-8")
    prompt = prompt.replace("{{CONFIG_SITIO}}", bloque_sitio(cfg))

    r = Anthropic().messages.create(
        model="claude-sonnet-5",
        max_tokens=16000,
        system=prompt,
        messages=[{"role": "user", "content": f"Casos de prueba:\n\n{casos}"}],
    )
    texto = "".join(b.text for b in r.content if b.type == "text")
    codigo = texto.strip().removeprefix("```python").removesuffix("```").strip()

    base = pathlib.Path(archivo_csv).stem.replace("_casos", "")
    slug = re.sub(r"[^a-z0-9]+", "_", sitio.lower())
    salida = RAIZ / "tests" / f"test_{base}_{slug}.py"
    salida.write_text(codigo, encoding="utf-8")
    print(f"Specs ({cfg['nombre']}) -> {salida}")


if __name__ == "__main__":
    generar(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "saucedemo")
