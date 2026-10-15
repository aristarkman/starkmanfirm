#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build one post (EN + ES) into the starkmanfirm.com codebase.

Usage:
    python3 build_post.py            # needs ./site/ (a clone of the repo) -> writes pages,
                                     # index cards and sitemap entries
    python3 build_post.py --dropin   # no repo needed -> writes standalone drop-in HTML

All per-post copy lives in a sibling copy.py. Since 2026-09-15 that module also supplies the
byline, the index-card date, the "More reading" links and the citation list, so this script is
fully generic and does not need editing between cycles.
"""
import io, json, os, re, sys
import importlib.util

SITE = "https://www.starkmanfirm.com/"
ROOT = os.path.dirname(os.path.abspath(__file__))


def _site_dir():
    """Where the site checkout lives.

    Three ways, in priority order, so the same script works in both places it runs:
      1. --site PATH          (explicit)
      2. $SITE_DIR            (explicit, for CI)
      3. ./site next to this script, then the repo root two levels up.

    The sandbox flow clones the repo into ./site beside the script. GitHub Actions
    checks the repo out so that the site IS the repo root, i.e. ../.. from here.
    """
    argv = sys.argv
    if "--site" in argv:
        return os.path.abspath(argv[argv.index("--site") + 1])
    if os.environ.get("SITE_DIR"):
        return os.path.abspath(os.environ["SITE_DIR"])
    beside = os.path.join(ROOT, "site")
    if os.path.isdir(beside):
        return beside
    repo_root = os.path.abspath(os.path.join(ROOT, os.pardir, os.pardir))
    if os.path.isfile(os.path.join(repo_root, "sitemap.xml")):
        return repo_root
    return beside


S = _site_dir()
OUT = os.path.join(ROOT, "dropin")

_spec = importlib.util.spec_from_file_location("postcopy", os.path.join(ROOT, "copy.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

EN_DIR = f"resources/{C.EN_SLUG}/"
ES_DIR = f"es/recursos/{C.ES_SLUG}/"

EN_SKEL = "resources/workers-comp-claim-denied-nj/index.html"
ES_SKEL = "es/recursos/reclamo-negado/index.html"

CITATIONS = getattr(C, "CITATIONS", [])

# --- Back-compatibility shims (added 2026-09-15) -----------------------------
# copy modules written before 2026-09-15 (e.g. copy_2026-09-01.py) predate the generic
# generator and carry no byline / card-date / "More reading" fields. The playbook tells a
# future run to rebuild a lost post from its saved copy_<date>.py, and without these
# fallbacks that instruction dies with AttributeError. Byline and card date are derivable
# from DATE; "More reading" degrades to an empty rail card.
_ES_MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
              "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
_ES_ABBR = ["ene", "feb", "mar", "abr", "may", "jun",
            "jul", "ago", "sep", "oct", "nov", "dic"]


def _date_parts():
    import datetime
    d = datetime.date(*(int(x) for x in C.DATE.split("-")))
    return d


def _default(name):
    d = _date_parts()
    return {
        "EN_BYLINE": f"Published {d.strftime('%B')} {d.day}, {d.year} · Morris Starkman",
        "ES_BYLINE": f"Publicado el {d.day} de {_ES_MONTHS[d.month - 1]} de {d.year} · Morris Starkman",
        "EN_CARD_DATE": f"{d.strftime('%b')} {d.day}, {d.year}",
        "ES_CARD_DATE": f"{d.day} {_ES_ABBR[d.month - 1]} {d.year}",
        "EN_MORE": [],
        "ES_MORE": [],
    }[name]


def cp(name):
    """Per-post copy field, falling back to a derived default for older copy modules."""
    return getattr(C, name, None) or _default(name)

FALLBACK_FIRM = [{
    "@type": "LegalService", "@id": SITE + "#firm", "name": "Starkman Firm",
    "url": SITE, "areaServed": "New Jersey",
}]


def read(p):
    with io.open(os.path.join(S, p), encoding="utf-8") as f:
        return f.read()


def write(path, s, base=None):
    full = os.path.join(base or S, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, "w", encoding="utf-8") as f:
        f.write(s)


def firm_graph(skel):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', skel, re.S)
    graph = json.loads(m.group(1))["@graph"]
    return [n for n in graph if n.get("@type") in {"LegalService", "Attorney", "Person"}]


def head_block(lang, title, desc, out_dir, alt_dir, graph):
    canonical = SITE + out_dir
    en_url = SITE + (out_dir if lang == "en" else alt_dir)
    es_url = SITE + (alt_dir if lang == "en" else out_dir)
    alt = (f'<link rel="alternate" hreflang="en-us" href="{en_url}">'
           f'<link rel="alternate" hreflang="es-us" href="{es_url}">'
           f'<link rel="alternate" hreflang="x-default" href="{en_url}">')
    full_title = f"{title} | Starkman Firm"
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, separators=(",", ":"))
    u = "../../" if lang == "en" else "../../../"
    locale = "en_US" if lang == "en" else "es_US"
    og_alt = "The attorneys of Starkman Firm" if lang == "en" else "Los abogados de Starkman Firm"
    return (
        f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<title>{full_title}</title><meta name="description" content="{desc}">'
        f'<link rel="canonical" href="{canonical}">{alt}\n'
        f'<meta property="og:type" content="article"><meta property="og:title" content="{full_title}">'
        f'<meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}">'
        f'<meta property="og:locale" content="{locale}">\n'
        f'<meta name="geo.region" content="US-NJ"><meta name="geo.placename" content="Cherry Hill, New Jersey">\n'
        f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
        f'<link rel="stylesheet" href="{u}assets/site.css">\n'
        f'<script type="application/ld+json">{ld}</script>\n'
        f'<link rel="icon" href="{u}assets/logo-mark.png"><link rel="apple-touch-icon" href="{u}assets/logo-mark.png">'
        f'<meta name="theme-color" content="#E91A20">'
        f'<meta property="og:image" content="https://www.starkmanfirm.com/assets/og-cover.jpg">'
        f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        f'<meta property="og:image:alt" content="{og_alt}"><meta property="og:site_name" content="Starkman Firm">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{full_title}">'
        f'<meta name="twitter:description" content="{desc}">'
        f'<meta name="twitter:image" content="https://www.starkmanfirm.com/assets/og-cover.jpg">'
        f'<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">\n'
        f'<script async src="https://www.googletagmanager.com/gtag/js?id=G-NG99FGY5L4"></script>\n'
        f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}'
        f"gtag('js',new Date());gtag('config','G-NG99FGY5L4');</script>\n"
    )


def make_graph(firm, lang, title, desc, out_dir, crumb_home, crumb_res, faq):
    canonical = SITE + out_dir
    graph = list(firm)
    graph.append({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": crumb_home,
         "item": SITE + ("" if lang == "en" else "es/")},
        {"@type": "ListItem", "position": 2, "name": crumb_res,
         "item": SITE + ("resources/" if lang == "en" else "es/recursos/")},
        {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
    ]})
    post = {"@type": "BlogPosting", "headline": title, "datePublished": C.DATE,
            "dateModified": C.DATE, "description": desc, "inLanguage": lang,
            "author": {"@id": SITE + "attorneys/#morris"},
            "publisher": {"@id": SITE + "#firm"},
            "mainEntityOfPage": canonical}
    if CITATIONS:
        post["citation"] = CITATIONS
    graph.append(post)
    graph.append({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    return graph


def body_blocks(lang, title, lead, body, faq, disclaimer, crumb_home, crumb_res,
                crumb_res_href, faq_heading, byline, rail_head, rail_lead, rail_call,
                rail_more, more_links):
    u = "../../" if lang == "en" else "../../../"
    home_href = u + ("index.html" if lang == "en" else "es/index.html")
    review_href = u + ("free-case-review/index.html" if lang == "en" else "es/consulta-gratis/index.html")
    hero = (
        f'\n<div class="pagehero"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb">'
        f'<a href="{home_href}">{crumb_home}</a> <span style="opacity:.5">/</span> '
        f'<a href="{crumb_res_href}">{crumb_res}</a> <span style="opacity:.5">/</span> '
        f'<span>{title}</span></nav></div>'
        f'<div class="wrap" style="display:flex;flex-direction:column;gap:20px;padding-top:26px">\n'
        f'<h1>{title}</h1><p>{lead}</p></div></div>\n'
    )
    more = "".join(f'<a href="{href}" style="font-size:16px">{label}</a>' for label, href in more_links)
    article = (
        f'<section><div class="wrap twocol"><article class="prose">'
        f'<p class="fine" style="margin-bottom:6px">{byline}</p>{body}\n'
        f'<p class="fine" style="margin-top:20px">{disclaimer}</p></article>\n'
        f'<aside class="rail"><div class="railcard dark"><h3>{rail_head}</h3>'
        f'<p style="margin:0;font-size:16px;color:#D5D0CA">{rail_lead}</p>'
        f'<a class="btn btn-brick" href="tel:+18564247277">856-424-7277</a>'
        f'<a class="btn btn-out-w" href="{review_href}">{rail_call}</a></div>\n'
        f'<div class="railcard"><h3>{rail_more}</h3>{more}</div></aside></div></section>\n'
    )
    faq_html = (
        f'<section class="faq"><div class="wrap" style="max-width:880px"><div class="sechead">'
        f'<h2 class="sec">{faq_heading}</h2></div><div style="margin-top:26px">'
        + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
        + '</div></div></section>\n'
    )
    return hero, article, faq_html


LANGS = {
    "en": dict(
        skel=EN_SKEL, out_dir=EN_DIR, alt_dir=ES_DIR,
        title=C.EN_TITLE, desc=C.EN_DESC, lead=C.EN_LEAD, body=C.EN_BODY,
        faq=C.EN_FAQ, disclaimer=C.EN_DISCLAIMER,
        crumb_home="Home", crumb_res="Resources", crumb_res_href="../index.html",
        faq_heading="Questions we get", byline=cp("EN_BYLINE"),
        rail_head="Free consultation",
        rail_lead="Questions about your own case? Twenty minutes, no cost.",
        rail_call="Request a review", rail_more="More reading",
        more_links=cp("EN_MORE"), card_date=cp("EN_CARD_DATE")),
    "es": dict(
        skel=ES_SKEL, out_dir=ES_DIR, alt_dir=EN_DIR,
        title=C.ES_TITLE, desc=C.ES_DESC, lead=C.ES_LEAD, body=C.ES_BODY,
        faq=C.ES_FAQ, disclaimer=C.ES_DISCLAIMER,
        crumb_home="Inicio", crumb_res="Recursos", crumb_res_href="../index.html",
        faq_heading="Preguntas frecuentes", byline=cp("ES_BYLINE"),
        rail_head="Consulta gratis",
        rail_lead="¿Preguntas sobre su caso? Veinte minutos, sin costo.",
        rail_call="Solicitar revisión", rail_more="Más lecturas",
        more_links=cp("ES_MORE"), card_date=cp("ES_CARD_DATE")),
}


def build(lang, dropin=False):
    cfg = LANGS[lang]
    if dropin:
        firm = FALLBACK_FIRM
        chrome_top = chrome_bottom = ""
    else:
        skel = read(cfg["skel"])
        firm = firm_graph(skel)
        chrome = skel[skel.index("</head><body>"):]
        main_start = chrome.index("<main>") + len("<main>")
        cta_start = chrome.index('<section class="cta">')
        chrome_top, chrome_bottom = chrome[:main_start], chrome[cta_start:]

    graph = make_graph(firm, lang, cfg["title"], cfg["desc"], cfg["out_dir"],
                       cfg["crumb_home"], cfg["crumb_res"], cfg["faq"])
    head = head_block(lang, cfg["title"], cfg["desc"], cfg["out_dir"], cfg["alt_dir"], graph)
    hero, article, faq_html = body_blocks(
        lang, cfg["title"], cfg["lead"], cfg["body"], cfg["faq"], cfg["disclaimer"],
        cfg["crumb_home"], cfg["crumb_res"], cfg["crumb_res_href"], cfg["faq_heading"],
        cfg["byline"], cfg["rail_head"], cfg["rail_lead"], cfg["rail_call"],
        cfg["rail_more"], cfg["more_links"])

    if dropin:
        note = (f"<!-- DROP-IN for {cfg['out_dir']} — no repo was reachable when this was built.\n"
                f"     Paste the HEAD block into a copy of {cfg['skel']}'s <head>, and the\n"
                f"     BODY block between <main> and <section class=\"cta\">. -->\n")
        write(f"{lang}-dropin.html",
              note + "<!-- ===== HEAD BLOCK ===== -->\n" + head +
              "\n<!-- ===== BODY BLOCK ===== -->\n" + hero + article + faq_html,
              base=OUT)
    else:
        write(cfg["out_dir"] + "index.html", head + chrome_top + hero + article + faq_html + chrome_bottom)


def add_index_card(lang):
    cfg = LANGS[lang]
    path = "resources/index.html" if lang == "en" else "es/recursos/index.html"
    html = read(path)
    href = f'{C.EN_SLUG if lang == "en" else C.ES_SLUG}/index.html'
    if href in html:
        print(f"  card already present in {path}")
        return
    m = re.search(r'<div class="postlist">\s*(<a\b.*?</a>)', html, re.S)
    if not m:
        raise SystemExit(f"could not find an existing card in {path}")
    template = m.group(1)
    card = template
    card = re.sub(r'href="[^"]*"', f'href="{href}"', card, count=1)
    dates = re.findall(r'>([A-Z][a-z]{2} \d{1,2}, \d{4}|\d{1,2} [a-z]{3} \d{4})<', template)
    if dates:
        card = card.replace(f'>{dates[0]}<', f'>{cfg["card_date"]}<', 1)
    hm = re.search(r'<h3[^>]*>(.*?)</h3>', template, re.S)
    if hm:
        card = card.replace(hm.group(1), cfg["title"], 1)
    pm = re.search(r'<p[^>]*>(.*?)</p>', template, re.S)
    if pm:
        card = card.replace(pm.group(1), cfg["desc"], 1)
    html = html.replace(template, card + template, 1)
    write(path, html)
    print(f"  card added to {path}")


def add_sitemap():
    path = "sitemap.xml"
    xml = read(path)
    if C.EN_SLUG in xml:
        print("  sitemap already has the new URLs")
        return
    en, es = SITE + EN_DIR, SITE + ES_DIR
    block = (
        f'<url><loc>{en}</loc><lastmod>{C.DATE}</lastmod>'
        f'<xhtml:link rel="alternate" hreflang="en-us" href="{en}"/>'
        f'<xhtml:link rel="alternate" hreflang="es-us" href="{es}"/>'
        f'<xhtml:link rel="alternate" hreflang="x-default" href="{en}"/></url>\n'
        f'<url><loc>{es}</loc><lastmod>{C.DATE}</lastmod>'
        f'<xhtml:link rel="alternate" hreflang="en-us" href="{en}"/>'
        f'<xhtml:link rel="alternate" hreflang="es-us" href="{es}"/>'
        f'<xhtml:link rel="alternate" hreflang="x-default" href="{en}"/></url>\n'
    )
    xml = xml.replace("</urlset>", block + "</urlset>", 1)
    write(path, xml)
    print("  sitemap.xml updated")


if __name__ == "__main__":
    dropin = "--dropin" in sys.argv
    if not dropin and not os.path.isdir(S):
        raise SystemExit(
            f"no site checkout found at {S} — pass --site PATH, set SITE_DIR, "
            f"clone the repo into ./site beside this script, or run with --dropin")
    if not dropin:
        print(f"building into {S}")
    for lang in ("en", "es"):
        build(lang, dropin=dropin)
    if not dropin:
        add_index_card("en")
        add_index_card("es")
        add_sitemap()
    print(f"drop-in files written to {OUT}" if dropin else f"pages written into {S}")
