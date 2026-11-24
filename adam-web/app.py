"""Web Adama Vaculčíka s AI asistentem (Flask + Claude API)."""

import json
import os

import anthropic
from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

MODEL = "claude-opus-5-5"
MAX_HISTORY = 20  # max. počet zpráv z historie, které posíláme do API
MAX_MESSAGE_CHARS = 2000

SYSTEM_PROMPT = """Jsi AI asistent na webu Adama Vaculčíka. Odpovídáš návštěvníkům webu \
(typicky projektantům, architektům, stavebním firmám a soukromým stavebníkům) česky, \
stručně, věcně a přátelsky. Vykáš.

O Adamovi:
- Věnuje se technickému zpracování stavební dokumentace, tvorbě 2D výkresů a 3D modelů \
v oblasti pozemního stavitelství.
- Zpracovává půdorysy, řezy, pohledy, kótování, úpravy a rozkreslování projektové \
dokumentace, digitalizaci starších výkresů a zakreslování skutečného stavu.
- Podle potřeby připravuje 3D modely staveb, výpočty ploch a kubatur a další technické podklady.
- Pracuje v Archicadu a AutoCADu. Zakládá si na přesném a přehledném zpracování podle \
dodaných podkladů a zadání.
- Absolvent SPŠ stavební, obor pozemní stavitelství. Má praktické zkušenosti ze \
stavebnictví a zednických prací.
- Spolupracuje jako externí technická výpomoc na IČO: jednorázové zpracování části \
projektu, krátkodobá výpomoc i dlouhodobá spolupráce.
- Portfolio: Bytový dům LICHÝ, Moštárna Lidečko, RD se zubní ordinací, Růžďka STODOLA.

Kontakt: telefon +420 603 888 122, e-mail adam.vaculcik@gmail.com, \
adresa Kateřinice 76, 756 21. Pracovní doba Po–Pá 9:00–18:00.

Pravidla:
- Neuváděj konkrétní ceny ani termíny. Ty se domlouvají individuálně – odkaž na kontakt.
- Nevymýšlej si služby, reference ani údaje, které výše nejsou. Když něco nevíš, řekni to \
a doporuč kontaktovat Adama.
- Když návštěvník popisuje svou zakázku, pomoz mu ujasnit, jaké podklady má připravit \
(např. stávající výkresy, zaměření, fotografie, formát výstupu, měřítko), a na požádání \
mu sestav krátký text poptávky, který může poslat e-mailem.
- Na otázky mimo stavební dokumentaci a Adamovy služby odpověz krátce a vrať se k tématu.
- Odpovídej obvykle v 1–4 krátkých odstavcích, bez nadpisů."""

_client = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def clean_history(raw) -> list[dict]:
    """Ponechá jen platné zprávy user/assistant a ořízne délku."""
    if not isinstance(raw, list):
        return []
    messages = []
    for item in raw[-MAX_HISTORY:]:
        if not isinstance(item, dict):
            continue
        role, content = item.get("role"), item.get("content")
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content[:MAX_MESSAGE_CHARS]})
    # API vyžaduje, aby konverzace začínala zprávou uživatele a končila jí.
    while messages and messages[0]["role"] != "user":
        messages.pop(0)
    if not messages or messages[-1]["role"] != "user":
        return []
    return messages


def sse(event: dict) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    messages = clean_history(payload.get("messages"))
    if not messages:
        return jsonify({"error": "Prázdná zpráva."}), 400

    def generate():
        try:
            with get_client().beta.messages.stream(
                model=MODEL,
                max_tokens=4000,
                system=SYSTEM_PROMPT,
                messages=messages,
                output_config={"effort": "low"},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                for text in stream.text_stream:
                    yield sse({"text": text})
                final = stream.get_final_message()
            if final.stop_reason == "refusal":
                yield sse({"text": "Omlouvám se, na tohle neodpovím. "
                                   "Napište prosím Adamovi přímo na adam.vaculcik@gmail.com."})
        except (anthropic.AuthenticationError, TypeError):
            # TypeError vyhodí SDK, když není nastavený žádný klíč (ANTHROPIC_API_KEY).
            app.logger.exception("Chybí nebo je neplatný API klíč")
            yield sse({"error": "AI asistent teď není nastavený. Kontaktujte prosím Adama "
                                "na +420 603 888 122 nebo adam.vaculcik@gmail.com."})
        except anthropic.RateLimitError:
            yield sse({"error": "Asistent je teď přetížený, zkuste to prosím za chvíli."})
        except (anthropic.APIStatusError, anthropic.APIConnectionError):
            app.logger.exception("Chyba Claude API")
            yield sse({"error": "Asistent je dočasně nedostupný, zkuste to prosím později."})
        yield sse({"done": True})

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5100)))
