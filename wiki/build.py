#!/usr/bin/env python3
"""Genera el centro de ayuda estático (wiki/site/) desde wiki/docs/ayuda/*.md. Solo stdlib.

Uso:  python3 wiki/build.py            -> wiki/site/  (raíz de https://wiki.mesifly.com)
      WIKI_PREFIX=/ayuda python3 wiki/build.py -> wiki/site/ayuda/ (si algún día va bajo una ruta)
"""
import html, json, os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs" / "ayuda"
IMG = ROOT.parent / "one" / "img"
APP = "https://app.mesifly.com"      # la aplicación (botones «Abrir Mesifly», rutas ruta_app)
SITE = "https://wiki.mesifly.com"     # esta wiki, en la raíz de su subdominio
PREFIX = os.environ.get("WIKI_PREFIX", "")
OUT = ROOT / "site" / PREFIX.strip("/")
# Datos de _variables.md (si cambian allá, cámbialos aquí)
PRICE, TRIAL = "5", "14"

CATS = {
    "primeros-pasos": ("Primeros pasos", "🚀", "Crea tu cuenta, entra y deja listo tu restaurante."),
    "menu": ("Tu menú", "🍽️", "Sube fotos, arma categorías y platillos, y comparte tu enlace."),
    "pedidos": ("Pedidos", "🛎️", "Recibe y atiende pedidos, conecta Telegram y fija tu horario."),
    "mi-restaurante": ("Tu restaurante", "🏪", "Datos, logo, colores y varias sucursales."),
    "equipo": ("Tu equipo", "👥", "Crea empleados y define qué pueden hacer."),
    "consultar-informacion": ("Consultar información", "📊", "Ventas y productos más pedidos."),
    "cuenta-y-plan": ("Cuenta y plan", "⚙️", "Perfil, contraseña, plan y baja de la cuenta."),
    "para-tus-clientes": ("Para tus clientes", "🧾", "Cómo pide un comensal y qué hacer si no ve tu menú."),
}
AUD = {"dueno": "Para dueños", "empleado": "Para empleados", "cliente": "Para clientes", "todos": "Para todos"}
QUICK = ["crear-cuenta", "subir-fotos-del-menu", "ver-y-compartir-el-menu", "conectar-telegram",
         "recibir-y-atender-pedidos", "prueba-gratis-y-suscripcion"]
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()
SPECIAL = {"preguntas-frecuentes": "preguntas-frecuentes", "glosario": "glosario", "CHANGELOG": "cambios"}

def die(msg):
    sys.exit(f"build.py: {msg}")

# ---------- front matter y markdown ----------
def parse_doc(path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            v = re.sub(r"\s+#\s.*$", "", v.strip())
            if v.startswith("["):
                v = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
            else:
                v = v.strip('"')
            meta[k.strip()] = v
        text = text[m.end():]
    return meta, text

def esc(s):
    return html.escape(s, quote=True)

def inline(s):
    codes = []
    def stash(m):
        codes.append(f"<code>{html.escape(m.group(1), quote=False)}</code>")
        return f"\x00{len(codes) - 1}\x00"
    s = esc(re.sub(r"`([^`]+)`", stash, s))
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)

def plain(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

def slug(s):
    s = re.sub(r"[^\w\s-]", "", plain(s).lower())
    return re.sub(r"[\s_]+", "-", s).strip("-")

LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)")

def render_list(items, i, indent):
    """items: [(indent, ordered, text)]; devuelve (html, siguiente_i, textos_de_primer_nivel)."""
    tag = "ol" if items[i][1] else "ul"
    out, tops = [f"<{tag}>"], []
    while i < len(items) and items[i][0] >= indent:
        ind, _, text = items[i]
        if ind > indent:  # sublista sin padre directo
            sub, i, _ = render_list(items, i, ind)
            out.append(sub)
            continue
        i += 1
        li = inline(text)
        tops.append(plain(li))
        if i < len(items) and items[i][0] > indent:
            sub, i, _ = render_list(items, i, items[i][0])
            li += sub
        out.append(f"<li>{li}</li>")
    out.append(f"</{tag}>")
    return "".join(out), i, tops

def render_md(md, faq=False):
    lines = md.splitlines()
    out, toc, steps, problems, qa = [], [], [], [], []
    h1, h2, para, i = "", "", [], 0

    def flush():
        if not para:
            return
        t = " ".join(para)
        para.clear()
        m = faq and re.match(r"^\*\*(¿.+?\?)\*\*\s*(.*)$", t)
        if m:
            out.append(f"<h3>{inline(m.group(1))}</h3><p>{inline(m.group(2))}</p>")
            qa.append((plain(inline(m.group(1))), plain(inline(m.group(2)))))
        else:
            out.append(f"<p>{inline(t)}</p>")

    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            flush(); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)", ln)
        if m:
            flush()
            n, text = len(m.group(1)), m.group(2).strip()
            if n == 1 and not h1:
                h1 = text
            else:
                sid = slug(text)
                if n == 2:
                    h2 = text
                    toc.append((sid, plain(inline(text))))
                out.append(f'<h{n} id="{sid}">{inline(text)} <a class="anchor" href="#{sid}" aria-label="Enlace a esta sección">#</a></h{n}>')
            i += 1; continue
        if re.match(r"^-{3,}$", ln.strip()):
            flush(); out.append("<hr>"); i += 1; continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush()
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], rows[2:]
            if h2.startswith("Problemas"):
                problems += [r for r in body if len(r) >= 3]
            cap = f"<caption>{esc(h2 or h1)}</caption>" if (h2 or h1) else ""
            th = "".join(f'<th scope="col">{inline(c)}</th>' for c in head)
            tr = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f'<div class="tbl"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>')
            continue
        if LIST_RE.match(ln):
            flush()
            items = []
            while i < len(lines):
                m = LIST_RE.match(lines[i])
                if m:
                    items.append((len(m.group(1).expandtabs(4)), m.group(2)[0].isdigit(), m.group(3)))
                elif lines[i].strip() and lines[i].startswith("  ") and items:  # continuación
                    ind, o, t = items[-1]
                    items[-1] = (ind, o, t + " " + lines[i].strip())
                elif not lines[i].strip() and i + 1 < len(lines) and LIST_RE.match(lines[i + 1]):
                    pass
                else:
                    break
                i += 1
            base = min(x[0] for x in items)
            norm = [(x[0] - base, x[1], x[2]) for x in items]
            html_l, _, tops = render_list(norm, 0, 0)
            if norm[0][1] and h2.startswith("Pasos"):
                steps.append((h2, tops))
            out.append(html_l)
            continue
        if ln.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i].lstrip("> ")); i += 1
            out.append(f"<blockquote><p>{inline(' '.join(q))}</p></blockquote>")
            continue
        para.append(ln.strip()); i += 1
    flush()
    return dict(html="\n".join(out), h1=h1, toc=toc, steps=steps, problems=problems, qa=qa)

# ---------- corpus ----------
def load():
    docs = []
    files = sorted(DOCS.glob("*/*.md")) + [DOCS / "preguntas-frecuentes.md", DOCS / "glosario.md", DOCS / "CHANGELOG.md"]
    for p in files:
        if p.parent.name == "_plantillas":
            continue
        meta, body = parse_doc(p)
        rel = p.relative_to(DOCS).as_posix()
        if p.parent != DOCS:
            cat = re.sub(r"^\d+-", "", p.parent.name)
            if cat not in CATS or "id" not in meta:
                die(f"{rel}: categoría o id desconocido")
            url = f"/{cat}/{meta['id']}/"
        else:
            cat, url = "consulta-rapida", f"/{SPECIAL[p.stem]}/"
            meta.setdefault("titulo", "Historial de cambios de la ayuda")
            meta.setdefault("resumen", "Registro de cambios de esta ayuda cuando cambia la aplicación.")
            meta.setdefault("actualizado", "2026-10-27")
            meta.setdefault("audiencia", "todos")
            meta.setdefault("palabras_clave", ["cambios", "novedades"])
            meta.setdefault("ruta_app", "n/a")
            meta.setdefault("id", "cambios")
        for k in ("titulo", "resumen", "actualizado"):
            if not meta.get(k):
                die(f"{rel}: falta {k}")
        docs.append(dict(meta=meta, body=body, rel=rel, cat=cat, url=url, path=p))
    return docs

def fix_links(md, doc, by_rel, absolute):
    def sub(m):
        target = (doc["path"].parent / m.group(1)).resolve()
        try:
            rel = target.relative_to(DOCS).as_posix()
        except ValueError:
            die(f"{doc['rel']}: enlace fuera de docs: {m.group(1)}")
        if rel not in by_rel:
            die(f"{doc['rel']}: enlace roto: {m.group(1)}")
        return f"]({(SITE if absolute else '')}{PREFIX}{by_rel[rel]['url']}{m.group(2) or ''})"
    return re.sub(r"\]\(([^)#\s]+\.md)(#[^)\s]*)?\)", sub, md)

def fecha(s):
    y, m, d = map(int, s.split("-"))
    return f"{d} de {MESES[m - 1]} de {y}"

def ld(objs):
    return "".join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace("</", "<\\/") + "</script>" for o in objs)

ORG = {"@type": "Organization", "name": "Mesifly", "url": APP + "/", "logo": f"{SITE}{PREFIX}/assets/icono.png"}

# ---------- plantillas ----------
def shell(title, desc, url, body, graph, kind="article"):
    canon = f"{SITE}{PREFIX}{url}"
    full_title = title if url == "/" else f"{title} | Ayuda Mesifly"
    return f"""<!doctype html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#e8590c">
<link rel="icon" href="{PREFIX}/assets/icono.png" type="image/png">
<meta property="og:type" content="{kind}"><meta property="og:locale" content="es_MX"><meta property="og:site_name" content="Ayuda Mesifly">
<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}{PREFIX}/assets/logo.png"><meta name="twitter:card" content="summary">
<link rel="alternate" type="text/plain" href="{SITE}{PREFIX}/llms.txt" title="llms.txt">
<link rel="stylesheet" href="{PREFIX}/assets/wiki.css">
<script>document.documentElement.className="js"</script>
{ld(graph)}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site"><div class="wrap bar">
<a class="logo" href="{PREFIX}/" aria-label="Centro de ayuda de Mesifly, inicio"><img src="{PREFIX}/assets/logo.png" width="351" height="96" alt="Mesifly"><span>Ayuda</span></a>
<form class="search" role="search" action="{PREFIX}/" onsubmit="return false"><label class="sr" for="q">Buscar en la ayuda</label>
<input id="q" type="search" placeholder="Busca: crear cuenta, Telegram, QR…" autocomplete="off" aria-controls="res" aria-expanded="false"><ul id="res" role="listbox" hidden></ul></form>
<nav aria-label="Principal"><a href="{PREFIX}/preguntas-frecuentes/">Preguntas</a><a class="btn" href="{APP}/">Abrir Mesifly</a></nav>
</div></header>
{body}
<footer class="site"><div class="wrap">
<nav aria-label="Pie"><a href="{PREFIX}/preguntas-frecuentes/">Preguntas frecuentes</a><a href="{PREFIX}/glosario/">Glosario</a><a href="{PREFIX}/cambios/">Cambios de la ayuda</a><a href="{PREFIX}/llms.txt">llms.txt</a><a href="{APP}/">app.mesifly.com</a></nav>
<p>© Mesifly · Menú digital y pedidos directos para restaurantes, sin comisión por pedido.</p></div></footer>
<script src="{PREFIX}/assets/wiki.js" defer></script>
</body></html>"""

def breadcrumbs(crumbs):
    """crumbs: [(nombre, url)] sin el inicio; devuelve (html, jsonld)."""
    allc = [("Ayuda", "/")] + crumbs
    last = len(allc) - 1
    items = "".join(
        "<li>" + (f'<span aria-current="page">{esc(n)}</span>' if k == last else f'<a href="{PREFIX}{u}">{esc(n)}</a>') + "</li>"
        for k, (n, u) in enumerate(allc))
    j = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, "item": f"{SITE}{PREFIX}{u}"} for k, (n, u) in enumerate(allc)]}
    return f'<nav class="crumbs" aria-label="Migas de pan"><ol>{items}</ol></nav>', j

def sidebar(docs, current):
    parts = []
    for c, (name, ico, _) in CATS.items():
        li = "".join(
            f'<li><a href="{PREFIX}{d["url"]}"' + (' aria-current="page"' if d["url"] == current else "") + f'>{esc(d["meta"]["titulo"])}</a></li>'
            for d in docs if d["cat"] == c)
        parts.append(f'<section><h2><a href="{PREFIX}/{c}/">{ico} {esc(name)}</a></h2><ul>{li}</ul></section>')
    return f'<aside class="side" aria-label="Temas de la ayuda">{"".join(parts)}</aside>'

def howto(doc, r):
    if not r["steps"]:
        return []
    mk = lambda tops: [{"@type": "HowToStep", "position": k + 1, "text": t} for k, t in enumerate(tops)]
    if len(r["steps"]) == 1:
        steps = mk(r["steps"][0][1])
    else:
        steps = [{"@type": "HowToSection", "name": n, "itemListElement": mk(t)} for n, t in r["steps"]]
    return [{"@type": "HowTo", "name": doc["meta"]["titulo"], "description": doc["meta"]["resumen"], "inLanguage": "es", "step": steps}]

def faq_ld(pairs):
    if not pairs:
        return []
    return [{"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}]

# ---------- generación ----------
def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def main():
    docs = load()
    by_rel = {d["rel"]: d for d in docs}
    by_id = {d["meta"]["id"]: d for d in docs}
    for q in QUICK:
        if q not in by_id:
            die(f"QUICK: id inexistente {q}")
    if OUT.exists():
        shutil.rmtree(OUT)
    search, urls = [], []

    for d in docs:
        m = d["meta"]
        d["r"] = render_md(fix_links(d["body"], d, by_rel, False), faq=d["url"] == "/preguntas-frecuentes/")
        for rel_id in m.get("relacionados", []):
            if rel_id not in by_id:
                die(f"{d['rel']}: relacionado inexistente {rel_id}")
        search.append({"t": m["titulo"], "u": PREFIX + d["url"], "r": m["resumen"],
                       "k": " ".join(m.get("palabras_clave", [])), "x": plain(d["r"]["html"])})

    # páginas de artículo
    for d in docs:
        m, r = d["meta"], d["r"]
        cat_name = CATS[d["cat"]][0] if d["cat"] in CATS else "Consulta rápida"
        crumbs = ([(cat_name, f"/{d['cat']}/")] if d["cat"] in CATS else []) + [(m["titulo"], d["url"])]
        bc_html, bc_ld = breadcrumbs(crumbs)
        canon = f"{SITE}{PREFIX}{d['url']}"
        art = {"@type": "TechArticle", "headline": m["titulo"], "description": m["resumen"], "inLanguage": "es",
               "dateModified": m["actualizado"], "datePublished": m["actualizado"], "url": canon,
               "mainEntityOfPage": canon, "keywords": ", ".join(m.get("palabras_clave", [])),
               "author": ORG, "publisher": ORG,
               "audience": {"@type": "Audience", "audienceType": AUD.get(m.get("audiencia"), "Todos")}}
        faq_pairs = r["qa"] or [(f"¿Qué hago si veo {plain(inline(c[0]))}?", f"{plain(inline(c[1]))}. {plain(inline(c[2]))}") for c in r["problems"]]
        graph = [{"@context": "https://schema.org", **g} for g in [art, bc_ld] + howto(d, r) + faq_ld(faq_pairs)]
        ruta = m.get("ruta_app", "n/a")
        app_btn = ""
        if ruta not in ("n/a", ""):
            if ":" in ruta:
                app_btn = f'<p class="route">Dirección en la app: <code>app.mesifly.com{esc(ruta.replace(":slug", "tu-negocio"))}</code></p>'
            else:
                app_btn = f'<p><a class="btn" href="{APP}{esc(ruta)}">Abrir en la app</a></p>'
        toc = ""
        if len(r["toc"]) > 1:
            toc = '<aside class="toc" aria-label="En esta página"><h2>En esta página</h2><ul>' + "".join(
                f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in r["toc"]) + "</ul></aside>"
        rel_html = ""
        rels = [by_id[i] for i in m.get("relacionados", [])]
        if rels and d["cat"] in CATS:
            rel_html = '<nav class="related" aria-label="Artículos relacionados"><h2>También te puede servir</h2><ul>' + "".join(
                f'<li><a href="{PREFIX}{x["url"]}"><strong>{esc(x["meta"]["titulo"])}</strong><span>{esc(x["meta"]["resumen"])}</span></a></li>' for x in rels) + "</ul></nav>"
        pn = ""
        if d["cat"] in CATS:
            sib = [x for x in docs if x["cat"] == d["cat"]]
            k = sib.index(d)
            prev = f'<a rel="prev" href="{PREFIX}{sib[k - 1]["url"]}"><small>Anterior</small>{esc(sib[k - 1]["meta"]["titulo"])}</a>' if k else "<span></span>"
            nxt = f'<a rel="next" href="{PREFIX}{sib[k + 1]["url"]}"><small>Siguiente</small>{esc(sib[k + 1]["meta"]["titulo"])}</a>' if k + 1 < len(sib) else "<span></span>"
            pn = f'<nav class="pn" aria-label="Anterior y siguiente">{prev}{nxt}</nav>'
        h1 = r["h1"] or m["titulo"]
        aud = f'<span class="badge">{AUD[m["audiencia"]]}</span>' if m.get("audiencia") in AUD and d["cat"] in CATS else ""
        body = f"""<div class="wrap layout">{sidebar(docs, d["url"])}
<main id="main"><article>{bc_html}
<header class="art"><p class="meta">{aud}<span>Actualizado <time datetime="{m["actualizado"]}">{fecha(m["actualizado"])}</time></span></p>
<h1>{esc(h1)}</h1><p class="lead">{esc(m["resumen"])}</p>{app_btn}</header>
<div class="prose">{r["html"]}</div></article>{rel_html}{pn}</main>{toc}</div>"""
        write(d["url"].strip("/") + "/index.html", shell(m["titulo"], m["resumen"], d["url"], body, graph))
        urls.append((d["url"], m["actualizado"]))

    # páginas de categoría
    for c, (name, ico, desc) in CATS.items():
        arts = [d for d in docs if d["cat"] == c]
        bc_html, bc_ld = breadcrumbs([(name, f"/{c}/")])
        cards = "".join(f'<li><a href="{PREFIX}{d["url"]}"><strong>{esc(d["meta"]["titulo"])}</strong><span>{esc(d["meta"]["resumen"])}</span></a></li>' for d in arts)
        item_list = {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": k + 1, "url": f"{SITE}{PREFIX}{d['url']}", "name": d["meta"]["titulo"]} for k, d in enumerate(arts)]}
        graph = [{"@context": "https://schema.org", **g} for g in
                 [{"@type": "CollectionPage", "name": name, "description": desc, "inLanguage": "es"}, bc_ld, item_list]]
        body = f"""<div class="wrap layout">{sidebar(docs, "")}<main id="main">{bc_html}
<header class="art"><h1>{ico} {esc(name)}</h1><p class="lead">{esc(desc)}</p></header>
<ul class="cards one">{cards}</ul></main></div>"""
        write(f"{c}/index.html", shell(name, desc, f"/{c}/", body, graph, kind="website"))
        urls.append((f"/{c}/", max(d["meta"]["actualizado"] for d in arts)))

    # inicio
    cards = ""
    for c, (name, ico, desc) in CATS.items():
        li = "".join(f'<li><a href="{PREFIX}{d["url"]}">{esc(d["meta"]["titulo"])}</a></li>' for d in docs if d["cat"] == c)
        cards += f'<li class="cat"><h3><a href="{PREFIX}/{c}/"><span aria-hidden="true">{ico}</span> {esc(name)}</a></h3><p>{esc(desc)}</p><ul>{li}</ul></li>'
    chips = "".join(f'<li><a href="{PREFIX}{by_id[q]["url"]}">{esc(by_id[q]["meta"]["titulo"])}</a></li>' for q in QUICK)
    facts = [("Precio", f"${PRICE} USD al mes por restaurante (sucursal)."), ("Prueba gratis", f"{TRIAL} días en la primera alta."),
             ("Comisión por pedido", "Ninguna. Solo pagas la suscripción."), ("Tu cliente", "No se registra ni descarga nada: abre tu enlace y pide.")]
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in facts)
    desc = "Centro de ayuda de Mesifly: guías paso a paso para crear tu cuenta, armar tu menú digital, recibir pedidos por Telegram y administrar tu restaurante."
    body = f"""<main id="main">
<section class="hero"><div class="wrap"><span class="eyebrow">Centro de ayuda</span>
<h1>¿En qué te podemos ayudar?</h1><p class="lead">Guías paso a paso para armar tu menú digital y recibir pedidos directos, sin tecnicismos.</p>
<h2 class="sr">Lo más consultado</h2><ul class="chips">{chips}</ul></div></section>
<section class="wrap" id="temas" aria-labelledby="t"><h2 id="t">Todos los temas</h2><ul class="cards">{cards}</ul></section>
<section class="band"><div class="wrap"><h2>Respuestas rápidas</h2><dl class="facts">{dl}</dl>
<p><a class="btn" href="{PREFIX}/preguntas-frecuentes/">Ver todas las preguntas frecuentes</a></p></div></section></main>"""
    graph = [{"@context": "https://schema.org", "@type": "WebSite", "name": "Ayuda Mesifly", "url": f"{SITE}{PREFIX}/", "inLanguage": "es",
              "publisher": ORG, "potentialAction": {"@type": "SearchAction", "target": f"{SITE}{PREFIX}/?q={{search_term_string}}", "query-input": "required name=search_term_string"}},
             {"@context": "https://schema.org", **ORG, "description": "Menú digital y pedidos directos para restaurantes, sin comisión por pedido."},
             {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Mesifly", "url": APP + "/", "applicationCategory": "BusinessApplication",
              "operatingSystem": "Web, PWA", "inLanguage": ["es", "en"],
              "offers": {"@type": "Offer", "price": PRICE, "priceCurrency": "USD", "description": f"Por restaurante (sucursal) al mes, {TRIAL} días de prueba gratis."}}]
    write("index.html", shell("Centro de ayuda de Mesifly", desc, "/", body, graph, kind="website"))
    urls.append(("/", max(d["meta"]["actualizado"] for d in docs)))

    write("404.html", shell("Página no encontrada", "La página que buscas no existe en el centro de ayuda.", "/404.html",
          f'<main id="main" class="wrap nf"><h1>No encontramos esa página</h1><p class="lead">Prueba con el buscador o vuelve al <a href="{PREFIX}/">inicio de la ayuda</a>.</p></main>', []))

    # búsqueda, sitemap, robots, llms
    write("assets/search.json", json.dumps(search, ensure_ascii=False, separators=(",", ":")))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{SITE}{PREFIX}{u}</loc><lastmod>{lm}</lastmod></url>\n" for u, lm in urls) + "</urlset>\n")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot"]
    write("robots.txt", "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {SITE}{PREFIX}/sitemap.xml\n")

    L = ["# Mesifly: centro de ayuda",
         f"> Guías paso a paso de Mesifly, menú digital propio y pedidos directos para restaurantes, sin comisión por pedido. ${PRICE} USD al mes por restaurante (sucursal), {TRIAL} días de prueba gratis. Los pedidos llegan por Telegram; el comensal no se registra ni descarga nada; el pago se arregla directo con el restaurante.", ""]
    for c, (name, _, _) in CATS.items():
        L.append(f"## {name}")
        L += [f"- [{d['meta']['titulo']}]({SITE}{PREFIX}{d['url']}): {d['meta']['resumen']}" for d in docs if d["cat"] == c]
        L.append("")
    L.append("## Consulta rápida")
    L += [f"- [{d['meta']['titulo']}]({SITE}{PREFIX}{d['url']}): {d['meta']['resumen']}" for d in docs if d["cat"] == "consulta-rapida"]
    write("llms.txt", "\n".join(L) + "\n")
    full = ["# Mesifly: centro de ayuda (texto completo)\n"]
    for d in docs:
        body = re.sub(r"^# .*\n", "", fix_links(d["body"], d, by_rel, True).strip() + "\n", count=1)
        full.append(f"\n---\n\n# {d['meta']['titulo']}\nURL: {SITE}{PREFIX}{d['url']}\nActualizado: {d['meta']['actualizado']}\nResumen: {d['meta']['resumen']}\n{body}")
    write("llms-full.txt", "".join(full))

    # assets
    for f in ("logo.png", "icono.png"):
        shutil.copy(IMG / f, OUT / "assets" / f)
    for f in ("wiki.css", "wiki.js"):
        shutil.copy(ROOT / "assets" / f, OUT / "assets" / f)

    # nada fuera de app.mesifly.com (salvo schema.org / sitemaps.org)
    bad = set()
    for f in OUT.rglob("*.html"):
        for u in re.findall(r"https?://[^\s\"'<)]+", f.read_text(encoding="utf-8")):
            if not re.match(r"https?://(app\.mesifly\.com|wiki\.mesifly\.com|schema\.org|www\.sitemaps\.org)\b", u):
                bad.add(u)
    if bad:
        die(f"URLs fuera de {APP} y {SITE}: {sorted(bad)}")
    print(f"OK: {len(docs)} artículos, {len(urls)} páginas -> {OUT}")

if __name__ == "__main__":
    main()
