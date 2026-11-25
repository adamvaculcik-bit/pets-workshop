"""Obsah podstránek služeb. Každá služba má vlastní URL /sluzby/<slug>.

Texty jsou psané v první osobě (za Adama). Při úpravě služby stačí změnit text tady –
šablona `templates/service.html`, mapa webu i odkazy na úvodní stránce se upraví samy.
"""

SERVICES = [
    {
        "slug": "digitalizace-vykresu",
        "card": "Digitalizace",
        "card_text": "Převod starších papírových výkresů do digitální podoby (DWG, PDF).",
        "title": "Digitalizace starých výkresů do DWG a PDF",
        "meta_title": "Digitalizace starých výkresů do DWG | Adam Vaculčík",
        "description": "Převedu papírové a naskenované stavební výkresy do digitální podoby v AutoCADu nebo Archicadu. Výstup DWG a PDF, připravený pro další projektování. Zlínský kraj i celá ČR.",
        "lead": "Máte staré papírové výkresy domu, které potřebujete upravit, doplnit nebo použít pro nový projekt? Překreslím je do přesné digitální podoby, se kterou se dá dál pracovat.",
        "image": "img/hero.webp",
        "image_alt": "Digitální výkres vzniklý z původní dokumentace",
        "includes": [
            "Překreslení půdorysů, řezů a pohledů z papírových výkresů nebo skenů",
            "Sjednocení měřítka, kót a popisů do přehledné podoby",
            "Výkresy rozdělené do hladin, připravené pro další úpravy",
            "Kontrola návazností mezi jednotlivými výkresy",
        ],
        "inputs": [
            "Sken nebo kvalitní fotografie původních výkresů (ideálně ve vyšším rozlišení)",
            "Informace, k čemu budou výkresy sloužit (přestavba, prodej, stavební úřad…)",
            "Případné ruční poznámky nebo změny oproti původnímu stavu",
        ],
        "outputs": "DWG (AutoCAD), PDF; případně model v Archicadu podle domluvy.",
        "steps": [
            ("Pošlete podklady", "Stačí e-mailem – skeny, fotky, případně popis zakázky."),
            ("Domluvíme rozsah", "Upřesníme, které výkresy a v jakém formátu potřebujete."),
            ("Zpracování", "Výkresy přesně překreslím a zkontroluji návaznosti."),
            ("Předání", "Dostanete hotové soubory, drobné úpravy po kontrole jsou samozřejmostí."),
        ],
        "faq": [
            ("Stačí mi fotografie výkresů z mobilu?",
             "Často ano, pokud jsou ostré, celé a fotografované kolmo. U nečitelných míst se domluvíme, "
             "jak chybějící údaje doplnit – například z kontrolního zaměření."),
            ("Co když se skutečný stav liší od starých výkresů?",
             "Výkresy mohu upravit podle dodaného zaměření nebo vašich poznámek. Navazující službou je "
             "zakreslení skutečného stavu."),
            ("Kolik digitalizace stojí?",
             "Cena záleží na počtu a složitosti výkresů. Pošlete podklady a připravím nabídku na míru."),
        ],
    },
    {
        "slug": "zakresleni-skutecneho-stavu",
        "card": "Skutečný stav",
        "card_text": "Zakreslení skutečného stavu stavby podle zaměření a podkladů.",
        "title": "Zakreslení skutečného stavu stavby",
        "meta_title": "Zakreslení skutečného stavu stavby | Adam Vaculčík",
        "description": "Výkresy skutečného stavu (pasport) stávajících budov podle dodaného zaměření, náčrtů a fotografií. Podklad pro rekonstrukci, prodej nebo stavební úřad.",
        "lead": "U starších staveb často dokumentace chybí nebo neodpovídá skutečnosti. Podle zaměření a podkladů připravím přehledné výkresy, jak stavba vypadá dnes.",
        "image": "img/mostarna-lidecko.webp",
        "image_alt": "Stávající objekt – podklad pro zakreslení skutečného stavu",
        "includes": [
            "Půdorysy všech podlaží, řezy a pohledy podle skutečnosti",
            "Kótování, výšky, popisy místností a ploch",
            "Vyznačení nosných konstrukcí, otvorů a schodišť",
            "Podklad pro projektanta, stavební úřad, banku nebo prodej nemovitosti",
        ],
        "inputs": [
            "Zaměření stavby (míry jednotlivých místností, výšky, tloušťky zdí)",
            "Ruční náčrty a fotografie interiéru i exteriéru",
            "Původní výkresy, pokud existují – i neúplné",
        ],
        "outputs": "DWG, PDF; na přání i 3D model stavby.",
        "steps": [
            ("Pošlete podklady", "Zaměření, náčrty, fotografie a případné staré výkresy."),
            ("Kontrola podkladů", "Projdu, zda je vše potřebné, a případně upozorním na chybějící míry."),
            ("Zakreslení", "Připravím půdorysy, řezy a pohledy podle skutečnosti."),
            ("Předání", "Výkresy dostanete v PDF i DWG pro další práci projektanta."),
        ],
        "faq": [
            ("Provádíte i zaměření přímo na místě?",
             "Ozvěte se a popište zakázku – domluvíme, jak se zaměřením postupovat."),
            ("K čemu výkresy skutečného stavu potřebuji?",
             "Typicky jako podklad pro rekonstrukci, přístavbu, změnu užívání, prodej nemovitosti "
             "nebo pro jednání se stavebním úřadem."),
        ],
    },
    {
        "slug": "3d-model-stavby",
        "card": "3D modely",
        "card_text": "3D modely staveb pro vizualizaci, kontrolu návazností a prezentaci.",
        "title": "3D model stavby z výkresů",
        "meta_title": "3D model domu a stavby z výkresů | Adam Vaculčík",
        "description": "3D modely rodinných domů, bytových domů i hospodářských staveb v Archicadu podle výkresové dokumentace. Pro vizualizaci, kontrolu návazností a prezentaci klientovi.",
        "lead": "Z 2D výkresů vytvořím 3D model stavby. Pomůže klientovi lépe si stavbu představit a projektantovi odhalit kolize ještě před realizací.",
        "image": "img/bytovy-dum-lichy.webp",
        "image_alt": "3D model bytového domu",
        "includes": [
            "3D model stavby podle dodané výkresové dokumentace",
            "Konstrukce, otvory, střecha a základní materiály",
            "Pohledy a perspektivy pro prezentaci",
            "Kontrola návazností konstrukcí mezi podlažími",
        ],
        "inputs": [
            "Výkresová dokumentace (půdorysy, řezy, pohledy) v PDF nebo DWG",
            "Představa o materiálech, barvách a úrovni detailu",
            "Účel modelu – prezentace, kontrola, podklad pro vizualizaci",
        ],
        "outputs": "Model v Archicadu (PLN), export IFC, obrázky pohledů; další formáty podle domluvy.",
        "steps": [
            ("Pošlete výkresy", "A popište, k čemu model potřebujete."),
            ("Úroveň detailu", "Domluvíme, jak podrobný model má být."),
            ("Modelování", "Model vytvořím a průběžně zkontroluji proti výkresům."),
            ("Předání", "Model a pohledy dostanete v dohodnutých formátech."),
        ],
        "faq": [
            ("Děláte i fotorealistické vizualizace?",
             "Primárně připravuji přesný 3D model. Rozsah prezentačních výstupů domluvíme podle zakázky."),
            ("Jaké stavby modelujete?",
             "Rodinné domy, bytové domy i menší hospodářské a provozní stavby – podívejte se na portfolio."),
        ],
    },
    {
        "slug": "vykresova-dokumentace",
        "card": "2D výkresy",
        "card_text": "Půdorysy, řezy, pohledy, kótování a rozkreslování dokumentace.",
        "title": "Stavební výkresy a úpravy projektové dokumentace",
        "meta_title": "Kreslení stavebních výkresů – půdorysy, řezy, pohledy | Adam Vaculčík",
        "description": "Kreslení a úpravy stavebních výkresů v Archicadu a AutoCADu: půdorysy, řezy, pohledy, kótování a rozkreslování projektové dokumentace podle zadání projektanta.",
        "lead": "Zpracuji výkresovou část dokumentace podle vašich podkladů a zadání – přesně, přehledně a v jednotném stylu.",
        "image": "img/rd-zubni-ordinace.webp",
        "image_alt": "Rodinný dům se zubní ordinací – výkresová dokumentace",
        "includes": [
            "Půdorysy, řezy a pohledy",
            "Kótování, popisy, legendy místností a materiálů",
            "Úpravy a rozkreslování rozpracované dokumentace",
            "Sjednocení výkresů do jednotného grafického stylu a razítka",
        ],
        "inputs": [
            "Zadání a skici projektanta nebo architekta",
            "Rozpracované výkresy v DWG / PLN / PDF",
            "Požadovaný styl výkresů, razítko a měřítka",
        ],
        "outputs": "DWG, PLN (Archicad), PDF.",
        "steps": [
            ("Zadání", "Pošlete podklady a popište, co potřebujete zpracovat."),
            ("Nabídka", "Domluvíme rozsah, formát a termín."),
            ("Zpracování", "Výkresy připravím podle zadání a vašich zvyklostí."),
            ("Revize a předání", "Zapracuji připomínky a předám finální soubory."),
        ],
        "faq": [
            ("Pracujete v našem šablonovém souboru a razítku?",
             "Ano, rád se přizpůsobím vašim šablonám, hladinám a grafickým zvyklostem."),
            ("Zpracujete jen část dokumentace?",
             "Ano – například jen řezy a pohledy nebo úpravy po připomínkách. Stačí popsat rozsah."),
        ],
    },
    {
        "slug": "vypocet-ploch-a-kubatur",
        "card": "Výpočty",
        "card_text": "Výpočty ploch a kubatur a další technické podklady.",
        "title": "Výpočty ploch a kubatur",
        "meta_title": "Výpočet ploch a obestavěného prostoru (kubatur) | Adam Vaculčík",
        "description": "Výpočty podlahových ploch, obestavěného prostoru a kubatur podle výkresové dokumentace. Přehledné tabulky jako technický podklad pro projekt, rozpočet nebo úřad.",
        "lead": "Z výkresů nebo 3D modelu připravím přehledné výpočty ploch a kubatur, které můžete rovnou přiložit k dokumentaci.",
        "image": "img/ruzdka-stodola.webp",
        "image_alt": "Hospodářská stavba – podklad pro výpočet kubatur",
        "includes": [
            "Výpočet podlahových ploch po místnostech a podlažích",
            "Výpočet obestavěného prostoru a kubatur",
            "Přehledné tabulky a vyznačení ploch ve výkresech",
            "Další technické podklady podle potřeby projektu",
        ],
        "inputs": [
            "Výkresy stavby (PDF, DWG nebo PLN)",
            "Účel výpočtu a požadovaná struktura tabulek",
        ],
        "outputs": "Tabulky (PDF, XLSX) a výkresy s vyznačenými plochami.",
        "steps": [
            ("Pošlete výkresy", "A napište, k čemu výpočty potřebujete."),
            ("Výpočet", "Plochy a objemy spočítám z výkresů nebo z modelu."),
            ("Předání", "Dostanete tabulky a výkresy s vyznačením ploch."),
        ],
        "faq": [
            ("Spočítáte plochy i ze starých papírových výkresů?",
             "Ano, výkresy nejprve digitalizuji a výpočet pak provedu z digitální podoby."),
        ],
    },
    {
        "slug": "externi-kreslic-cad",
        "card": "Spolupráce na IČO",
        "card_text": "Externí výpomoc pro projektanty: jednorázově i dlouhodobě.",
        "title": "Externí kreslič CAD na IČO pro projektanty a architekty",
        "meta_title": "Externí kreslič CAD na IČO – Archicad, AutoCAD | Adam Vaculčík",
        "description": "Externí technická výpomoc pro projekční kanceláře, architekty a stavební firmy. Kreslení v Archicadu a AutoCADu na IČO – jednorázově, krátkodobě i dlouhodobě.",
        "lead": "Máte víc práce, než stíháte? Pomohu jako externí kreslič na IČO – bez náboru, bez závazků, přesně v rozsahu, který potřebujete.",
        "image": "img/adam.webp",
        "image_alt": "Adam Vaculčík – externí kreslič CAD",
        "includes": [
            "Jednorázové zpracování konkrétní části projektu",
            "Krátkodobá výpomoc ve špičce",
            "Dlouhodobá spolupráce na pravidelných zakázkách",
            "Práce v Archicadu i AutoCADu, přizpůsobení vašim šablonám",
        ],
        "inputs": [
            "Popis zakázky a požadovaný rozsah práce",
            "Podklady a šablony vaší kanceláře",
            "Termíny a způsob předávání (e-mail, sdílené úložiště)",
        ],
        "outputs": "Podle zvyklostí vaší kanceláře – DWG, PLN, PDF.",
        "steps": [
            ("Seznámení", "Krátce probereme, na čem pracujete a s čím potřebujete pomoci."),
            ("Zkušební zakázka", "Menší úkol, na kterém si ověříte kvalitu a styl práce."),
            ("Spolupráce", "Pracuji na zakázkách podle vašeho zadání a termínů."),
            ("Fakturace", "Fakturuji jako OSVČ na IČO – žádné starosti s pracovní smlouvou."),
        ],
        "faq": [
            ("Jak probíhá předávání podkladů?",
             "Obvykle e-mailem nebo přes sdílené úložiště. Přizpůsobím se tomu, co používáte."),
            ("Pracujete jen ve Zlínském kraji?",
             "Sídlím v Kateřinicích u Vsetína, ale výkresovou práci lze zpracovávat na dálku – "
             "spolupráce je tedy možná po celé ČR."),
        ],
    },
]

SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES}
