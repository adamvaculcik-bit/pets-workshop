# Web Adama Vaculčíka s AI asistentem

Jednostránkový web (Úvod, Služby, O mně, Portfolio, AI asistent, Kontakt) podle
původního webu na Webnode. Navíc obsahuje AI asistenta, který odpovídá návštěvníkům
na dotazy ke službám a pomáhá sepsat poptávku. Asistent běží na Claude API (Anthropic).

## Spuštění

```bash
cd adam-web
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # klíč z https://console.anthropic.com
python app.py                          # http://localhost:5100
```

Bez API klíče web funguje, jen asistent místo odpovědi ukáže kontakt.

## Úpravy

- **Texty webu:** `templates/index.html`
- **Barvy a vzhled:** `static/style.css` (proměnné nahoře, např. `--accent`)
- **Co asistent ví a jak odpovídá:** `SYSTEM_PROMPT` v `app.py`
- **Obrázky:** zatím se načítají z Webnode. Pro trvalé řešení je stáhněte do `static/`
  a změňte cesty v `index.html`.

## Nasazení

Na hostingu s Pythonem (např. Render, Railway, Azure App Service) spusťte
`gunicorn app:app` a nastavte proměnnou prostředí `ANTHROPIC_API_KEY`.
Klíč nikdy nedávejte do kódu ani do Gitu.
