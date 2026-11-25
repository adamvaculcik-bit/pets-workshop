"""Web Adama Vaculčíka s AI asistentem (Flask + Claude API)."""

import json
import os
import threading
import time
from collections import defaultdict, deque

import anthropic
from flask import Flask, Response, abort, jsonify, render_template, request, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from services import SERVICES, SERVICES_BY_SLUG

app = Flask(__name__)
# Hosting (Render) běží za proxy – díky tomu Flask zná skutečné https:// a doménu.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Hlavní adresa webu pro vyhledávače (např. https://vaculcik.com). Když není nastavená,
# použije se adresa, na kterou návštěvník přišel.
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")


def base_url() -> str:
    return SITE_URL or request.url_root.rstrip("/")


@app.context_processor
def inject_globals():
    return {"site_url": base_url(), "services": SERVICES}

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

# Jednoduchá ochrana proti zahlcení: max. RATE_LIMIT dotazů na IP za RATE_WINDOW sekund.
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", 20))
RATE_WINDOW = 10 * 60
_hits: dict[str, deque] = defaultdict(deque)
_hits_lock = threading.Lock()


def rate_limited(ip: str) -> bool:
    now = time.monotonic()
    with _hits_lock:
        hits = _hits[ip]
        while hits and now - hits[0] > RATE_WINDOW:
            hits.popleft()
        if len(hits) >= RATE_LIMIT:
            return True
        hits.append(now)
        return False


def client_ip() -> str:
    # Za proxy hostingu (Render apod.) je skutečná IP první v X-Forwarded-For.
    forwarded = request.headers.get("X-Forwarded-For", "")
    return forwarded.split(",")[0].strip() or request.remote_addr or "?"


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


@app.route("/sluzby/<slug>")
def service(slug):
    s = SERVICES_BY_SLUG.get(slug)
    if s is None:
        abort(404)
    base = base_url()
    page = base + url_for("service", slug=slug)
    structured_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "name": s["title"],
                "description": s["description"],
                "url": page,
                "serviceType": s["card"],
                "provider": {"@id": base + "/#firma"},
                "areaServed": [{"@type": "AdministrativeArea", "name": "Zlínský kraj"},
                               {"@type": "Country", "name": "Česká republika"}],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in s["faq"]],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Úvod", "item": base + "/"},
                    {"@type": "ListItem", "position": 2, "name": s["card"], "item": page},
                ],
            },
        ],
    }
    return render_template("service.html", s=s, structured_data=structured_data)


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


@app.route("/robots.txt")
def robots():
    body = f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {base_url()}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    base = base_url()
    urls = [base + "/"] + [base + url_for("service", slug=s["slug"]) for s in SERVICES]
    items = "".join(f"  <url><loc>{u}</loc><changefreq>monthly</changefreq></url>\n" for u in urls)
    body = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{items}</urlset>\n")
    return Response(body, mimetype="application/xml")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    messages = clean_history(payload.get("messages"))
    if not messages:
        return jsonify({"error": "Prázdná zpráva."}), 400
    if rate_limited(client_ip()):
        return jsonify({"error": "Příliš mnoho dotazů. Zkuste to prosím za pár minut, "
                                 "nebo napište Adamovi na adam.vaculcik@gmail.com."}), 429

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
