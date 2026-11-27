"""Build elpasoaiconsulting.com into docs/, which GitHub Pages serves.

Usage:  python build.py

Each page is a file in src/: a JSON header inside the first <!-- --> comment,
followed by the page body. The header keys are read in render() below.
CSS, JS and images live in docs/assets and are not generated.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

DOMAIN = "elpasoaiconsulting.com"
SITE = f"https://{DOMAIN}"
BRAND = "El Paso AI Consulting"
OWNER = "James Mann"
BOOK = "https://cal.com/james-mann-kzawdp"
TODAY = date.today().isoformat()

AREAS = [
    "El Paso", "West El Paso", "East El Paso", "Northeast El Paso", "Lower Valley",
    "Fort Bliss", "Horizon City", "Socorro", "San Elizario", "Canutillo", "Anthony",
    "Sunland Park", "Santa Teresa", "Las Cruces",
]

TEXT = {
    "en": {
        "home": "/",
        "skip": "Skip to content",
        "menu": "Menu",
        "nav": [
            ("Services", "/#services"),
            ("Consulting", "/ai-consulting-el-paso.html"),
            ("Automation", "/ai-automation-el-paso.html"),
            ("Chatbots", "/ai-chatbot-receptionist-el-paso.html"),
            ("Training", "/ai-training-el-paso.html"),
            ("About", "/about.html"),
            ("Español", "/es/"),
        ],
        "book": "Book a free consultation",
        "book_short": "Book a free consult",
        "all_services": ("All services", "/#services"),
        "learn": "Learn more",
        "faq_title": "Questions, answered.",
        "cta_title": "Start with a free consultation.",
        "cta_text": "Tell me what is eating your time. I will tell you whether AI can fix it, and how.",
        "foot_services": "Services",
        "foot_more": "More services",
        "foot_company": "Company",
        "foot_company_links": [
            ("About James Mann, Ph.D.", "/about.html"),
            ("Book a consultation", "/contact.html"),
            ("En español", "/es/"),
        ],
        "foot_area": "Service area",
        "foot_area_text": "Based in El Paso, Texas. On site across El Paso County and southern New Mexico, and remote anywhere in the United States.",
        "legal": "Independent consultant. Not affiliated with or endorsed by OpenAI, Anthropic, Google, Meta, Microsoft or Palantir. Product names are trademarks of their owners.",
    },
    "es": {
        "home": "/es/",
        "skip": "Saltar al contenido",
        "menu": "Menú",
        "nav": [
            ("Servicios", "/es/#servicios"),
            ("Cómo funciona", "/es/#proceso"),
            ("Preguntas", "/es/#preguntas"),
            ("Sobre mí", "/about.html"),
            ("English", "/"),
        ],
        "book": "Reserva una consulta gratis",
        "book_short": "Consulta gratis",
        "all_services": ("Ver servicios", "/es/#servicios"),
        "learn": "Más información",
        "faq_title": "Preguntas frecuentes.",
        "cta_title": "Empieza con una consulta gratis.",
        "cta_text": "Cuéntame qué te quita tiempo. Te diré si la inteligencia artificial puede resolverlo, y cómo.",
        "foot_services": "Servicios",
        "foot_more": "Más servicios",
        "foot_company": "Empresa",
        "foot_company_links": [
            ("Sobre James Mann, Ph.D.", "/about.html"),
            ("Reservar una consulta", BOOK),
            ("In English", "/"),
        ],
        "foot_area": "Zona de servicio",
        "foot_area_text": "Con base en El Paso, Texas. En persona en el condado de El Paso y el sur de Nuevo México, y a distancia en todo Estados Unidos.",
        "legal": "Consultor independiente. Sin afiliación ni respaldo de OpenAI, Anthropic, Google, Meta, Microsoft o Palantir. Los nombres de productos son marcas de sus propietarios.",
    },
}

ICONS = {
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "flow": '<circle cx="4" cy="6" r="1.5"/><path d="M5.5 6H10a4 4 0 0 1 4 4v4a4 4 0 0 0 4 4h2"/><path d="m17.5 15 3 3-3 3"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.2 2.7 2.5 6 2.5s6-1.3 6-2.5v-4.5"/><path d="M22 9v5"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "dna": '<path d="M7 3c0 6 10 6 10 12 0 2-1 4-1 6M17 3c0 6-10 6-10 12 0 2 1 4 1 6"/><path d="M8.5 6h7M9.5 9.5h5M9.5 14.5h5M8.5 18h7"/>',
    "chart": '<path d="M4 4v16h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "spark": '<path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="m18.5 16 .6 1.9 1.9.6-1.9.6-.6 1.9-.6-1.9-1.9-.6 1.9-.6z"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
}

SKYLINE = """<div class="skyline reveal" role="img" aria-label="{label}">
<p>El Paso, Texas</p>
<svg viewBox="0 0 1200 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
<defs><radialGradient id="glow"><stop offset="0" stop-color="#fff3c4" stop-opacity=".9"/><stop offset="1" stop-color="#fff3c4" stop-opacity="0"/></radialGradient></defs>
<path fill="#2a1242" fill-opacity=".75" d="M0 300V170l90-46 80 40 110-92 90 70 120-58 100 84 130-96 110 78 100-52 120 70 150-40v172z"/>
<path fill="#05060f" d="M0 300v-90l70-30 60 22 90-70 55 34 85-96 60 48 70-28 80 74 75-52 95 60 70-88 62 46 88-20 80 62 60-30 100 58v100z"/>
<circle cx="372" cy="128" r="26" fill="url(#glow)"/>
<path fill="#fff7d6" d="m372 118 2.35 6.76 7.16.15-5.71 4.33 2.08 6.85-5.88-4.09-5.88 4.09 2.08-6.85-5.71-4.33 7.16-.15z"/>
</svg>
</div>"""


def esc(text):
    return html.escape(text, quote=True)


def plain(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def load_pages():
    pages = []
    for path in sorted(SRC.glob("*.html")):
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"\s*<!--(.*?)-->\s*", raw, re.S)
        if not match:
            raise SystemExit(f"{path.name}: missing JSON header comment")
        try:
            meta = json.loads(match.group(1))
        except json.JSONDecodeError as err:
            raise SystemExit(f"{path.name}: bad JSON header: {err}")
        meta.setdefault("lang", "en")
        meta.setdefault("kind", "page")
        meta["body"] = raw[match.end():]
        meta["url"] = "/" + re.sub(r"(^|/)index\.html$", r"\1", meta["out"])
        pages.append(meta)
    return pages


def icon(name):
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


def services_grid(services, lang):
    wide = {0, 1, len(services) - 2, len(services) - 1}
    tiles = []
    for i, page in enumerate(services):
        card = page["card_es"] if lang == "es" else page["card"]
        cls = "tile wide reveal" if i in wide else "tile reveal"
        tiles.append(
            f'<a class="{cls}" href="{page["url"]}">{icon(page["icon"])}'
            f'<h3>{card["title"]}</h3><p>{card["text"]}</p>'
            f'<span class="more">{TEXT[lang]["learn"]}</span></a>'
        )
    return '<div class="bento">\n' + "\n".join(tiles) + "\n</div>"


def chips():
    return '<ul class="chips reveal">' + "".join(f"<li>{a}</li>" for a in AREAS) + "</ul>"


def structured_data(page, services):
    url = SITE + page["url"]
    business = {
        "@type": "ProfessionalService",
        "@id": f"{SITE}/#business",
        "name": BRAND,
        "url": f"{SITE}/",
        "image": f"{SITE}/assets/og.png",
        "logo": f"{SITE}/assets/apple-touch-icon.png",
        "description": "Independent AI consulting, automation, chatbots, training and private AI for businesses in El Paso, Texas.",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "El Paso",
            "addressRegion": "TX",
            "addressCountry": "US",
        },
        "areaServed": [{"@type": "City", "name": "El Paso, TX"}, {"@type": "City", "name": "Las Cruces, NM"},
                       {"@type": "AdministrativeArea", "name": "El Paso County, TX"}],
        "founder": {"@id": f"{SITE}/#james"},
        "knowsLanguage": ["en"],
        "potentialAction": {"@type": "ReserveAction", "name": "Book a free consultation", "target": BOOK},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "AI services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["card"]["title"], "url": SITE + s["url"]}}
                for s in services
            ],
        },
    }
    person = {
        "@type": "Person",
        "@id": f"{SITE}/#james",
        "name": OWNER,
        "honorificSuffix": "Ph.D.",
        "jobTitle": "AI Consultant",
        "url": f"{SITE}/about.html",
        "worksFor": {"@id": f"{SITE}/#business"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Baylor University"},
        "knowsAbout": ["Artificial intelligence", "Large language models", "Workflow automation",
                       "Model Context Protocol", "Bioinformatics", "CRISPR diagnostics"],
        "sameAs": ["https://github.com/14manj01", "https://github.com/JamesGerardMann",
                   "https://doi.org/10.1186/s12859-022-04968-5"],
    }
    webpage = {
        "@type": "AboutPage" if page["out"] == "about.html" else "ContactPage" if page["out"] == "contact.html" else "WebPage",
        "@id": url + "#page",
        "url": url,
        "name": page["title"],
        "description": page["description"],
        "inLanguage": page["lang"],
        "isPartOf": {"@id": f"{SITE}/#site"},
        "about": {"@id": f"{SITE}/#business"},
        "dateModified": TODAY,
    }
    site = {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": BRAND,
            "publisher": {"@id": f"{SITE}/#business"}, "inLanguage": ["en", "es"]}
    graph = [site, business, person, webpage]
    if page["kind"] not in ("home", "es"):
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": url},
            ],
        })
    if page["kind"] == "service":
        graph.append({
            "@type": "Service",
            "@id": url + "#service",
            "name": page["card"]["title"],
            "serviceType": page["service_type"],
            "description": page["description"],
            "url": url,
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": business["areaServed"],
        })
    if page.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "@id": url + "#faq",
            "inLanguage": page["lang"],
            "mainEntity": [
                {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                for q, a in page["faq"]
            ],
        })
    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render(page, services):
    lang = page["lang"]
    t = TEXT[lang]
    url = SITE + page["url"]
    is_404 = page["kind"] == "404"

    nav = "".join(
        f'<li><a href="{href}"{" aria-current=page" if href == page["url"] else ""}>{label}</a></li>'
        for label, href in t["nav"]
    )
    half = (len(services) + 1) // 2

    def service_links(items):
        key = "card_es" if lang == "es" else "card"
        return "".join(f'<li><a href="{s["url"]}">{s[key]["title"]}</a></li>' for s in items)

    def link(label, href):
        external = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        return f'<li><a href="{href}"{external}>{label}</a></li>'

    alternates = ""
    if page["kind"] in ("home", "es"):
        alternates = (
            f'<link rel="alternate" hreflang="en" href="{SITE}/">\n'
            f'<link rel="alternate" hreflang="es" href="{SITE}/es/">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n'
        )

    crumbs = ""
    if page["kind"] not in ("home", "es", "404"):
        crumbs = f'<ol class="crumbs"><li><a href="/">Home</a></li><li>{page["crumb"]}</li></ol>'

    second_label, second_href = t["all_services"]
    hero_extra = SKYLINE.format(label="Sunset over the Franklin Mountains with the Star on the Mountain") if page["kind"] in ("home", "es") else ""
    actions = "" if is_404 else (
        f'<div class="actions"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">{t["book"]}</a>'
        f'<a class="more" href="{second_href}">{second_label}</a></div>'
    )

    body = (
        page["body"]
        .replace("{{services}}", services_grid(services, lang))
        .replace("{{areas}}", chips())
        .replace("{{book}}", BOOK)
    )

    faq = ""
    if page.get("faq"):
        items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in page["faq"])
        anchor = "preguntas" if lang == "es" else "faq"
        faq = (
            f'<section class="section" id="{anchor}"><div class="wrap">'
            f'<div class="section-head reveal"><h2>{t["faq_title"]}</h2></div>'
            f'<div class="faq reveal">{items}</div></div></section>'
        )

    cta = "" if is_404 else (
        f'<section class="cta-band"><div class="wrap"><div class="cta reveal"><h2>{t["cta_title"]}</h2>'
        f'<p>{t["cta_text"]}</p><a class="btn" href="{BOOK}" target="_blank" rel="noopener">{t["book"]}</a></div></div></section>'
    )

    robots = "noindex" if is_404 else "index, follow, max-image-preview:large"
    canonical = "" if is_404 else f'<link rel="canonical" href="{url}">\n'

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page["title"])}</title>
<meta name="description" content="{esc(page["description"])}">
{canonical}{alternates}<meta name="robots" content="{robots}">
<meta name="author" content="{OWNER}, Ph.D.">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="El Paso">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="{"es_US" if lang == "es" else "en_US"}">
<meta property="og:title" content="{esc(page["title"])}">
<meta property="og:description" content="{esc(page["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: AI consulting, automation and training in El Paso, Texas">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{structured_data(page, services)}</script>
<script src="/assets/main.js" defer></script>
</head>
<body>
<a class="skip" href="#main">{t["skip"]}</a>
<header class="nav">
<div class="wrap nav-in">
<a class="brand" href="{t["home"]}">El Paso <b>AI</b> Consulting</a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="{t["menu"]}"><span></span><span></span></button>
<nav class="menu" id="menu" aria-label="Main"><ul>{nav}</ul></nav>
<a class="btn btn-sm" href="{BOOK}" target="_blank" rel="noopener">{t["book_short"]}</a>
</div>
</header>
<main id="main">
<section class="hero">
<div class="wrap">
{crumbs}
<p class="eyebrow grad">{page["eyebrow"]}</p>
<h1>{page["h1"]}</h1>
<p class="lede">{page["lede"]}</p>
{actions}
{hero_extra}
</div>
</section>
{body}
{faq}
{cta}
</main>
<footer class="footer">
<div class="wrap">
<div class="footer-cols">
<div><h2>{t["foot_services"]}</h2><ul>{service_links(services[:half])}</ul></div>
<div><h2>{t["foot_more"]}</h2><ul>{service_links(services[half:])}</ul></div>
<div><h2>{t["foot_company"]}</h2><ul>{"".join(link(label, href) for label, href in t["foot_company_links"])}</ul></div>
<div><h2>{t["foot_area"]}</h2><p>{t["foot_area_text"]}</p></div>
</div>
<div class="legal">
<p>{t["legal"]}</p>
<p>&copy; {TODAY[:4]} {BRAND} &middot; {OWNER}, Ph.D. &middot; El Paso, Texas</p>
</div>
</div>
</footer>
</body>
</html>
"""


def main():
    pages = load_pages()
    services = sorted((p for p in pages if p["kind"] == "service"), key=lambda p: p["order"])
    for page in pages:
        target = OUT / page["out"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(page, services), encoding="utf-8", newline="\n")

    indexed = sorted((p for p in pages if p["kind"] != "404"), key=lambda p: (p["url"] != "/", p["url"]))
    urls = "".join(f"  <url>\n    <loc>{SITE}{p['url']}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n" for p in indexed)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        encoding="utf-8", newline="\n",
    )
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8", newline="\n")
    (OUT / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8", newline="\n")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(pages)} pages into {OUT}")


if __name__ == "__main__":
    main()
