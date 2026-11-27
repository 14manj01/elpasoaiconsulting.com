"""Build elpasoaiconsulting.com into docs/, which GitHub Pages serves.

Usage:  python build.py

Each page is a file in src/: a JSON header inside the first <!-- --> comment,
followed by the page body. The header keys are read in render() below.
CSS, JS and images live in docs/assets and are not generated.
"""
import hashlib
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
INDEXNOW_KEY = "84bffaa91e8b3f7d5d0d0872bd2ec92d"  # proves site ownership to IndexNow (Bing and others)
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
            ("Training", "/ai-training-el-paso.html"),
            ("Invoices", "/invoice-automation-el-paso.html"),
            ("Phones", "/ai-chatbot-receptionist-el-paso.html"),
            ("Your website", "/build-a-website-with-ai.html"),
            ("Tech help", "/ai-for-it-help.html"),
            ("AI agents", "/ai-agent-setup-el-paso.html"),
            ("Restaurants", "/ai-for-restaurants-el-paso.html"),
            ("Español", "/es/"),
        ],
        "points": [
            ("AI for invoices", "/invoice-automation-el-paso.html"),
            ("AI for phones", "/ai-chatbot-receptionist-el-paso.html"),
            ("AI for your website", "/build-a-website-with-ai.html"),
            ("AI for IT help", "/ai-for-it-help.html"),
        ],
        "hero_more": ("See 65 things AI can do", "/what-can-ai-automate.html"),
        "demo": {
            "label": "Examples of messages from an AI agent to a business owner",
            "name": "Your AI agent",
            "scenes": [
                {
                    "tab": "Restaurant",
                    "time": "Example · 7:02 AM",
                    "caption": "Example: an AI agent such as Claude Duet or a ChatGPT dot working a restaurant's back office.",
                    "msgs": [
                        ("", "Good morning. Two things need you today."),
                        ("", "Two supplier invoices came in overnight. Both are in QuickBooks. Produce is up 12% this month."),
                        ("", "Catering invoice #1042 is 14 days late. I drafted a reminder."),
                        ("me", "Send it."),
                        ("", "Sent. Reminders stop the moment they pay."),
                    ],
                },
                {
                    "tab": "Contractor",
                    "time": "Example · 5:40 PM",
                    "caption": "Example: an AI receptionist for the calls you cannot take, with an AI agent handling follow-up.",
                    "msgs": [
                        ("", "You were on a roof all afternoon. Four calls came in and all four got an answer."),
                        ("", "Two estimates are booked: Thursday 9 AM and Friday 2 PM."),
                        ("", "The Mesa Street quote has had no reply in five days. Follow-up drafted."),
                        ("me", "Send it."),
                        ("", "Sent. I also asked yesterday's customer for a review."),
                    ],
                },
                {
                    "tab": "Clinic",
                    "time": "Example · 8:15 AM",
                    "caption": "Example: appointment reminders and review replies, with a person approving anything public.",
                    "msgs": [
                        ("", "Tomorrow has three unconfirmed appointments. Reminders went out in English and Spanish."),
                        ("", "Two patients rescheduled by text. The calendar is updated."),
                        ("", "A two-star review came in last night. I drafted a reply for you to read."),
                        ("me", "Show me."),
                        ("", "Here it is. Nothing is posted until you approve it."),
                    ],
                },
                {
                    "tab": "Office",
                    "time": "Example · Friday 4:00 PM",
                    "caption": "Example: an AI agent moving information between your inbox, job list and accounting.",
                    "msgs": [
                        ("", "Your Friday report is ready: sales, bookings and expenses on one page."),
                        ("", "I sorted 86 emails. Four need you today, and the replies are drafted."),
                        ("", "Three new orders came in by email. Each is now a work order and a draft invoice."),
                        ("me", "Anything late?"),
                        ("", "One invoice is 30 days overdue. Want the reminder?"),
                    ],
                },
            ],
        },
        "ticker": [
            "Chase overdue invoices", "Answer the calls you miss", "Text back missed callers", "Reply to every new lead",
            "Follow up on quiet quotes", "Send appointment reminders", "Ask for reviews", "Draft review replies",
            "Enter supplier bills", "Flag price increases", "Sort the inbox", "Draft the replies",
            "Turn job notes into estimates", "Move orders into your books", "Build the Friday report", "Track food costs",
            "Write training manuals", "Post in English and Spanish", "Keep Google hours current", "Update your website",
            "Troubleshoot the Wi-Fi", "Set up backups", "Lock down accounts", "Decode error messages",
        ],
        "book": "Book a free consultation",
        "book_short": "Book a free consult",
        "all_services": ("All training", "/#services"),
        "learn": "Learn more",
        "faq_title": "Questions, answered.",
        "cta_title": "Start with a free consultation.",
        "cta_text": "Tell me what is eating your time. I will tell you whether AI can fix it, and teach you how.",
        "foot_services": "Training",
        "foot_more": "More training",
        "foot_company": "Company",
        "foot_company_links": [
            ("About James Mann, Ph.D.", "/about.html"),
            ("What AI can automate", "/what-can-ai-automate.html"),
            ("AI for restaurants", "/ai-for-restaurants-el-paso.html"),
            ("Examples and use cases", "/ai-use-cases-el-paso.html"),
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
        "points": [
            ("IA para facturas", "/invoice-automation-el-paso.html"),
            ("IA para llamadas", "/ai-chatbot-receptionist-el-paso.html"),
            ("IA para tu sitio web", "/build-a-website-with-ai.html"),
            ("IA para soporte técnico", "/ai-for-it-help.html"),
        ],
        "hero_more": ("Ver servicios", "/es/#servicios"),
        "demo": {
            "label": "Ejemplos de mensajes de un agente de IA al dueño de un negocio",
            "name": "Tu agente de IA",
            "scenes": [
                {
                    "tab": "Restaurante",
                    "time": "Ejemplo · 7:02 a. m.",
                    "caption": "Ejemplo: un agente de IA como Claude Duet o un dot de ChatGPT en la administración de un restaurante.",
                    "msgs": [
                        ("", "Buenos días. Hoy hay dos cosas que necesitan tu atención."),
                        ("", "Anoche llegaron dos facturas de proveedores. Ya están en QuickBooks. Las verduras subieron 12% este mes."),
                        ("", "La factura de banquetes n.º 1042 tiene 14 días de atraso. Preparé un recordatorio."),
                        ("me", "Envíalo."),
                        ("", "Enviado. Los recordatorios se detienen en cuanto pagan."),
                    ],
                },
                {
                    "tab": "Contratista",
                    "time": "Ejemplo · 5:40 p. m.",
                    "caption": "Ejemplo: una recepcionista de IA para las llamadas que no puedes tomar y un agente que da seguimiento.",
                    "msgs": [
                        ("", "Estuviste en un techo toda la tarde. Entraron cuatro llamadas y las cuatro recibieron respuesta."),
                        ("", "Hay dos presupuestos agendados: jueves 9 a. m. y viernes 2 p. m."),
                        ("", "La cotización de la calle Mesa lleva cinco días sin respuesta. Preparé un seguimiento."),
                        ("me", "Envíalo."),
                        ("", "Enviado. También le pedí una reseña al cliente de ayer."),
                    ],
                },
                {
                    "tab": "Consultorio",
                    "time": "Ejemplo · 8:15 a. m.",
                    "caption": "Ejemplo: recordatorios de citas y respuestas a reseñas; una persona aprueba todo lo que se publica.",
                    "msgs": [
                        ("", "Mañana hay tres citas sin confirmar. Ya salieron los recordatorios en inglés y español."),
                        ("", "Dos pacientes cambiaron su cita por mensaje. El calendario está actualizado."),
                        ("", "Anoche llegó una reseña de dos estrellas. Preparé una respuesta para que la leas."),
                        ("me", "Muéstramela."),
                        ("", "Aquí está. No se publica nada hasta que la apruebes."),
                    ],
                },
                {
                    "tab": "Oficina",
                    "time": "Ejemplo · viernes 4:00 p. m.",
                    "caption": "Ejemplo: un agente de IA que pasa la información entre tu correo, tu lista de trabajos y tu contabilidad.",
                    "msgs": [
                        ("", "Tu reporte del viernes está listo: ventas, reservas y gastos en una página."),
                        ("", "Ordené 86 correos. Cuatro te necesitan hoy y las respuestas están en borrador."),
                        ("", "Llegaron tres pedidos por correo. Cada uno ya es una orden de trabajo y una factura en borrador."),
                        ("me", "¿Hay algo atrasado?"),
                        ("", "Una factura tiene 30 días de atraso. ¿Envío el recordatorio?"),
                    ],
                },
            ],
        },
        "ticker": [
            "Cobrar facturas atrasadas", "Contestar las llamadas perdidas", "Responder a cada cliente nuevo",
            "Dar seguimiento a cotizaciones", "Enviar recordatorios de citas", "Pedir reseñas",
            "Capturar facturas de proveedores", "Detectar aumentos de precio", "Ordenar el correo",
            "Convertir notas en presupuestos", "Hacer el reporte del viernes", "Vigilar el costo de alimentos",
            "Publicar en inglés y español", "Actualizar horarios en Google", "Actualizar tu sitio web",
            "Diagnosticar el Wi-Fi", "Configurar respaldos", "Proteger las cuentas",
        ],
        "book": "Reserva una consulta gratis",
        "book_short": "Consulta gratis",
        "all_services": ("Ver servicios", "/es/#servicios"),
        "learn": "Más información",
        "faq_title": "Preguntas frecuentes.",
        "cta_title": "Empieza con una consulta gratis.",
        "cta_text": "Cuéntame qué te quita tiempo. Te diré si la inteligencia artificial puede resolverlo, y te enseñaré cómo.",
        "foot_services": "Capacitación",
        "foot_more": "Más capacitación",
        "foot_company": "Empresa",
        "foot_company_links": [
            ("Sobre James Mann, Ph.D. (en inglés)", "/about.html"),
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
    "agent": '<rect x="5" y="8" width="14" height="10" rx="3"/><path d="M12 8V4.5M9.5 13h.01M14.5 13h.01M3 13h2M19 13h2"/><circle cx="12" cy="3.5" r="1"/>',
    "dots": '<circle cx="5.5" cy="12" r="2.2"/><circle cx="12" cy="12" r="2.2"/><circle cx="18.5" cy="12" r="2.2"/>',
    "duet": '<circle cx="9" cy="12" r="5.5"/><circle cx="15" cy="12" r="5.5"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "window": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 9.5h18M6.5 7.3h.01M9 7.3h.01"/>',
    "wrench": '<path d="M20 7.5a4.5 4.5 0 0 1-6.2 4.2L7 18.5A1.8 1.8 0 0 1 4.5 16l6.8-6.8A4.5 4.5 0 0 1 17 3.5L14.5 6l1 2.5 2.5 1z"/>',
}

RIDGE = """<svg class="ridge" viewBox="0 0 1200 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
<path fill="#2a1242" fill-opacity=".75" d="M0 300V170l90-46 80 40 110-92 90 70 120-58 100 84 130-96 110 78 100-52 120 70 150-40v172z"/>
<path fill="#05060f" d="M0 300v-90l70-30 60 22 90-70 55 34 85-96 60 48 70-28 80 74 75-52 95 60 70-88 62 46 88-20 80 62 60-30 100 58v100z"/>
</svg>"""


def asset(name):
    """Asset URL with a content hash, so browsers never pair new pages with a cached old stylesheet."""
    digest = hashlib.sha1((OUT / "assets" / name).read_bytes()).hexdigest()[:8]
    return f"/assets/{name}?v={digest}"


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


def demo(text):
    """Phone mock for the home hero: example conversations, each playing in about five seconds."""
    scenes = text["scenes"]
    first = scenes[0]
    messages = "".join(f'<p class="msg{" me" if who else ""}">{line}</p>' for who, line in first["msgs"])
    tabs = "".join(
        f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}">{scene["tab"]}</button>'
        for i, scene in enumerate(scenes)
    )
    data = json.dumps(
        [{"time": s["time"], "caption": s["caption"], "msgs": [list(m) for m in s["msgs"]]} for s in scenes],
        ensure_ascii=False, separators=(",", ":"),
    ).replace("</", "<\\/")
    return (
        f'<figure class="demo" aria-label="{text["label"]}">\n<div class="panel">\n<div class="phone">\n'
        f'<div class="phone-top"><span class="avatar">{icon("spark")}</span>'
        f'<p><b>{text["name"]}</b><small>{first["time"]}</small></p></div>\n'
        f'<div class="chat">{messages}</div>\n</div>\n{RIDGE}\n</div>\n'
        f'<div class="demo-tabs" role="tablist">{tabs}</div>\n'
        f'<figcaption>{first["caption"]}</figcaption>\n'
        f'<script type="application/json" id="demo-scenes">{data}</script>\n</figure>'
    )


def ticker(items):
    """Looping strip of tasks; the second copy exists only to make the loop seamless."""
    first = "".join(f"<li>{item}</li>" for item in items)
    second = "".join(f'<li aria-hidden="true">{item}</li>' for item in items)
    return f'<div class="ticker"><ul>{first}{second}</ul></div>'


def row_sizes(count):
    """Lay tiles out in rows of two wide or three regular tiles, never leaving one alone."""
    sizes = []
    while count:
        size = min((2, 3, 3)[len(sizes) % 3], count)
        if count - size == 1:
            size = 3 if size == 2 else 2
        sizes.append(size)
        count -= size
    return sizes


def services_grid(services, lang):
    wide, start = set(), 0
    for size in row_sizes(len(services)):
        if size < 3:
            wide.update(range(start, start + size))
        start += size
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
        "description": "Hands-on AI training and guided setup for businesses in El Paso, Texas. Clients learn to use AI for invoices, phone answering, automation and more, and run it themselves.",
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
            "name": "AI training",
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
        "jobTitle": "AI Trainer and Consultant",
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

    second_label, second_href = t["all_services"]
    actions = "" if is_404 else (
        f'<div class="actions"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">{t["book"]}</a>'
        f'<a class="more" href="{second_href}">{second_label}</a></div>'
    )

    if page["kind"] in ("home", "es"):
        points = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in t["points"])
        more_label, more_href = t["hero_more"]
        home_actions = (
            f'<div class="actions"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">{t["book"]}</a>'
            f'<a class="more" href="{more_href}">{more_label}</a></div>'
        )
        hero = (
            '<section class="hero hero-split">\n<div class="wrap">\n<div class="hero-grid">\n<div class="hero-copy">\n'
            f'<h1><span class="eyebrow grad">{page["eyebrow"]}</span>{page["h1"]}</h1>\n'
            f'<p class="lede">{page["lede"]}</p>\n{home_actions}\n<ul class="points">{points}</ul>\n</div>\n'
            f'{demo(t["demo"])}\n</div>\n{ticker(t["ticker"])}\n</div>\n</section>'
        )
    else:
        crumbs = "" if is_404 else f'<ol class="crumbs"><li><a href="/">Home</a></li><li>{page["crumb"]}</li></ol>'
        hero = (
            f'<section class="hero">\n<div class="wrap">\n{crumbs}\n<p class="eyebrow grad">{page["eyebrow"]}</p>\n'
            f'<h1>{page["h1"]}</h1>\n<p class="lede">{page["lede"]}</p>\n{actions}\n</div>\n</section>'
        )
    sticky = "" if is_404 else f'<a class="sticky-cta" href="{BOOK}" target="_blank" rel="noopener">{t["book"]}</a>'

    body = (
        page["body"]
        .replace("{{services}}", services_grid(services, lang))
        .replace("{{areas}}", chips())
        .replace("{{book}}", BOOK)
    )
    body = re.sub(r"\{\{icon:(\w+)\}\}", lambda match: icon(match.group(1)), body)

    # Generated sections continue the light/grey alternation of the page body.
    body_sections = re.findall(r'<section class="section( alt)?"', body)
    next_alt = bool(body_sections) and body_sections[-1] == ""

    examples = ""
    if page.get("examples"):
        cards = "".join(f'<article class="card"><h3>{title}</h3><p>{text}</p></article>' for title, text in page["examples"])
        examples = (
            f'<section class="section{" alt" if next_alt else ""}" id="examples"><div class="wrap">'
            '<div class="section-head reveal"><h2>Examples.</h2>'
            '<p>Illustrative setups that show what is possible. They are not client results.</p></div>'
            f'<div class="cards reveal">{cards}</div></div></section>'
        )
        next_alt = not next_alt

    faq = ""
    if page.get("faq"):
        items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in page["faq"])
        anchor = "preguntas" if lang == "es" else "faq"
        faq = (
            f'<section class="section{" alt" if next_alt else ""}" id="{anchor}"><div class="wrap">'
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
<meta property="og:image:alt" content="{BRAND}: hands-on AI training for businesses in El Paso, Texas">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="{asset("style.css")}">
<script type="application/ld+json">{structured_data(page, services)}</script>
<script src="{asset("main.js")}" defer></script>
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
{hero}
{body}
{examples}
{faq}
{cta}
</main>
{sticky}
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
    (OUT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    print(f"Built {len(pages)} pages into {OUT}")


if __name__ == "__main__":
    main()
