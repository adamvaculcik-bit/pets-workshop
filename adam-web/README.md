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
- **Obrázky:** `static/img/` (WebP). Nový obrázek nahrajte sem a odkažte na něj v `index.html`.

## Nasazení na Render

Konfigurace je v `render.yaml` v kořeni repozitáře.

1. Přihlaste se na https://render.com přes GitHub.
2. **New → Blueprint**, vyberte repozitář `pets-workshop` a větev, na které je web.
3. Render se zeptá na `ANTHROPIC_API_KEY` – vložte klíč z console.anthropic.com.
4. Klikněte **Deploy**. Web poběží na adrese typu `https://adam-vaculcik-web.onrender.com`.

Vlastní doménu nastavíte v Render → Settings → Custom Domains. Pak v Render →
Environment nastavte `SITE_URL` na hlavní adresu (např. `https://vaculcik.com`), aby
Google i náhledy při sdílení používaly vždy tuto doménu.

## Vyhledávače a sdílení

- Strukturovaná data pro Google (firma, adresa, služby, pracovní doba) jsou v `<head>`
  v `templates/index.html` – při změně kontaktů je upravte i tam.
- `/robots.txt` a `/sitemap.xml` generuje `app.py`.
- Obrázek pro sdílení: `static/og-image.jpg` (1200×630). Kontrola náhledu:
  https://www.opengraph.xyz nebo LinkedIn Post Inspector.
- Po spuštění domény přidejte web do Google Search Console a odešlete `sitemap.xml`.
Na bezplatném tarifu web po 15 minutách nečinnosti usne a první načtení pak trvá
asi minutu.

Chat má limit 20 dotazů na IP za 10 minut (proměnná `RATE_LIMIT`). V console.anthropic.com
si navíc nastavte měsíční limit útraty. Klíč nikdy nedávejte do kódu ani do Gitu.
