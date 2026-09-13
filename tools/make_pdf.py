#!/usr/bin/env python3
"""Arma el resumen completo de la materia en HTML listo para imprimir (A4).

Reutiliza el contenido de page.html (los resúmenes de cada unidad, la sección
de recursos y el glosario) y los diagramas de assets/, para que el PDF y la
página de estudio nunca se desincronicen.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/fonts/fonts.css"

page = open(os.path.join(ROOT, "page.html")).read()


def grab(name):
    m = re.search(r"var %s\s*=\s*`(.*?)`;" % name, page, re.S) or \
        re.search(r"%s\s*=\s*`(.*?)`;" % name, page, re.S)
    if not m:
        raise SystemExit("no encontré " + name)
    return m.group(1)


UNITS = [
    ("u0", "0", "El genoma humano por dentro", "Actividad previa", "#a8560c"),
    ("u1", "1", "Ómicas, regulación y validación", "Clase 1", "#d31c6b"),
    ("u2", "2", "Proyecto Genoma Humano y NGS", "Clase 2", "#7333e0"),
    ("u3", "3", "Variación, poblaciones y bases de datos", "Clase 3", "#0c7d73"),
    ("u4", "4", "TP 1 · Del FASTQ a la variante", "Trabajo práctico 1", "#0a6dbb"),
    ("u5", "5", "TP 2 · Anotar, filtrar y clasificar", "Trabajo práctico 2", "#4b46cf"),
    ("u6", "6", "cfDNA prenatal: la genómica en la clínica", "Actividad previa", "#b01345"),
]

sums = {u[0]: grab("SUM\\." + u[0]) for u in UNITS}
recursos = grab("RECURSOS")
gloss_raw = re.search(r"var GLOSS=\[(.*?)\n\];", page, re.S).group(1)
GLOSS = re.findall(r'\["(.*?)","(.*?)","(u\d)"\]', gloss_raw)

FIG = re.compile(r'<figure class="figwrap">.*?</figure>', re.S)


def split_figure(html):
    """Saca la figura del cuerpo de la unidad: va en su propia página apaisada."""
    m = FIG.search(html)
    if not m:
        return html, ""
    return html.replace(m.group(0), ""), m.group(0)


def section(recursos_html, title):
    """Extrae un bloque <div class="card"> de RECURSOS por su título."""
    for block in re.findall(r'<div class="card">.*?</div>\s*(?=<div class="card">|$)', recursos_html, re.S):
        if title in block:
            return block
    return ""


mapa = open(os.path.join(ROOT, "assets", "mapa-mental.svg")).read()

CSS = """
@page { size: A4 portrait; margin: 16mm 15mm 18mm; }
@page apaisada { size: A4 landscape; margin: 9mm; }
@page portada { margin: 0; }

:root{
  --ink:#2c1522; --ink2:#4f3341; --ink3:#8a6878;
  --line:#eccfde; --line2:#dfb0ca; --pink:#c2185b; --pinkd:#9c1049; --pinks:#fdeaf2;
  --panel:#fffafc; --red:#b31b3a; --reds:#fdeaee;
}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;color:var(--ink);background:#fff;
  font-family:"Source Sans 3",system-ui,sans-serif;font-size:9.6pt;line-height:1.42}
h1,h2,h3,h4{font-family:"Bricolage Grotesque","Source Sans 3",sans-serif;margin:0;line-height:1.15}
p{margin:0 0 .5em}
code,.mono{font-family:"JetBrains Mono",monospace;font-size:.88em}
code{background:var(--pinks);border:.5pt solid var(--line);border-radius:2pt;padding:0 2pt}
a{color:var(--pinkd);text-decoration:none}

/* ---------- portada ---------- */
.cover{page:portada;height:297mm;position:relative;overflow:hidden;
  background:linear-gradient(160deg,#fff4f9 0%,#ffe8f2 55%,#ffdcec 100%);
  padding:34mm 22mm 0;page-break-after:always}
.cover .kicker{font-size:10pt;letter-spacing:.24em;text-transform:uppercase;color:var(--pinkd);font-weight:700}
.cover h1{font-size:44pt;font-weight:800;letter-spacing:-.02em;margin:6mm 0 3mm;color:var(--ink)}
.cover h1 em{font-style:normal;color:var(--pink)}
.cover .sub{font-size:13pt;color:var(--ink2);max-width:120mm}
.cover .toc{margin-top:16mm;border-top:1.5pt solid var(--pink);padding-top:6mm;max-width:135mm}
.cover .toc div{display:flex;gap:6mm;align-items:baseline;padding:1.6mm 0;border-bottom:.5pt solid var(--line2);
  font-size:10.5pt}
.cover .toc b{font-family:"JetBrains Mono",monospace;color:var(--pink);min-width:9mm}
.cover .toc span{color:var(--ink2);margin-left:auto;font-size:8.6pt;text-transform:uppercase;letter-spacing:.1em}
.cover .foot{position:absolute;bottom:18mm;left:22mm;right:22mm;font-size:8.6pt;color:var(--ink3);
  border-top:.5pt solid var(--line2);padding-top:3mm}
.cover .helix{position:absolute;right:-38mm;top:4mm;width:128mm;opacity:.11}

/* ---------- unidades ---------- */
.unit{page-break-before:always}
.unit-head{border-bottom:2.5pt solid var(--c);padding-bottom:2.5mm;margin-bottom:5mm;
  display:flex;align-items:baseline;gap:4mm}
.unit-head .n{font-family:"JetBrains Mono",monospace;font-size:9pt;font-weight:700;color:var(--c);
  letter-spacing:.12em;white-space:nowrap}
.unit-head h2{font-size:19pt;font-weight:800;flex:1}
.unit-head .src{font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);font-weight:700}

.block{margin-bottom:4.5mm;page-break-inside:avoid}
.block h4{font-size:11.5pt;font-weight:800;color:var(--c);margin-bottom:1.4mm}
ul.tight{margin:.2em 0 .6em;padding-left:4.4mm}
ul.tight li{margin:.2em 0}
ol.tight{margin:.2em 0 .6em;padding-left:5mm}
ol.tight li{margin:.2em 0}
.kv{display:grid;grid-template-columns:auto 1fr;gap:1mm 4mm;margin-bottom:.5em}
.kv dt{font-weight:700;color:var(--c)}
.kv dd{margin:0;color:var(--ink2)}
.note{border-left:2.5pt solid var(--pink);background:var(--pinks);padding:2.2mm 3mm;border-radius:0 2mm 2mm 0;
  margin:2mm 0;page-break-inside:avoid}
.note.warn{border-left-color:var(--red);background:var(--reds)}
.note.exam{border-left-color:#7333e0;background:#f4eefe}
.note h4{font-size:10pt;margin-bottom:.8mm;color:var(--ink)}
.note p{margin:0}
.flow{display:flex;flex-wrap:wrap;gap:1.2mm;align-items:center;font-family:"JetBrains Mono",monospace;
  font-size:7.6pt;margin:1.5mm 0}
.flow span{background:var(--pinks);border:.5pt solid var(--line);padding:.8mm 1.6mm;border-radius:1.6mm}
.flow i{color:var(--pink);font-style:normal;font-weight:700}
.deck2{display:grid;grid-template-columns:1fr 1fr;gap:2.5mm;margin:2mm 0}
.mini{border:.6pt solid var(--line);border-radius:2mm;padding:2.2mm 2.6mm;background:var(--panel);
  page-break-inside:avoid}
.mini b{display:block;font-family:"Bricolage Grotesque",sans-serif;font-size:10pt;margin-bottom:.6mm}
.mini p{margin:0;font-size:9pt;color:var(--ink2)}
.tablewrap{margin:2mm 0;page-break-inside:avoid}
table{border-collapse:collapse;width:100%;font-size:8.8pt}
th,td{text-align:left;padding:1.4mm 2mm;border-bottom:.5pt solid var(--line);vertical-align:top}
th{font-size:7.4pt;text-transform:uppercase;letter-spacing:.08em;color:var(--ink3);background:var(--pinks);
  font-weight:700}
.muted{color:var(--ink3);font-size:8.6pt}
.eyebrow,.lead{display:none}
.search,#gcount,.gloss{display:none}
.figwrap{page:apaisada;page-break-before:always;margin:0;text-align:center}
.figwrap svg{display:block;margin:0 auto;width:240mm;height:auto}
.figwrap figcaption{font-size:8.4pt;color:var(--ink3);margin-top:2mm;text-align:left}
.mapa{page-break-before:always;text-align:center}
.mapa svg{display:block;margin:0 auto;width:172mm;height:auto}
.mapa p{font-size:8.4pt;color:var(--ink3);text-align:left;margin-top:2mm}

/* ---------- anexos ---------- */
.anexo{page-break-before:always}
.anexo h2{font-size:19pt;font-weight:800;border-bottom:2.5pt solid var(--pink);padding-bottom:2.5mm;
  margin-bottom:5mm}
.card{margin-bottom:5mm;page-break-inside:avoid}
.card h4{font-size:11.5pt;font-weight:800;color:var(--pinkd);margin-bottom:1.6mm}
.gl{column-count:2;column-gap:7mm;font-size:8.8pt}
.gl div{break-inside:avoid;margin-bottom:1.8mm}
.gl b{color:var(--ink);font-family:"Bricolage Grotesque",sans-serif}
.gl span{color:var(--ink2)}
.hr{height:.5pt;background:var(--line);margin:4mm 0}
"""


def build():
    parts = []
    parts.append("<!doctype html><html lang='es'><head><meta charset='utf-8'>")
    parts.append("<title>Genómica · resumen completo</title>")
    parts.append("<style>" + open(FONTS).read() + "</style>")
    parts.append("<style>" + CSS + "</style></head><body>")

    # ---------- portada ----------
    toc = "".join(
        "<div><b>%s</b>%s<span>%s</span></div>" % (n, t, src) for _, n, t, src, _ in UNITS
    ) + "<div><b>A</b>Anexos: tablas, criterios ACMG y glosario<span>Recursos</span></div>"
    parts.append("""
<section class="cover">
  <svg class="helix" viewBox="0 0 200 320" fill="none" stroke="#c2185b" stroke-width="3">
    <path d="M60 0 C 150 40, 60 80, 60 80 S 150 160, 60 200 S 150 280, 60 320"/>
    <path d="M140 0 C 50 40, 140 80, 140 80 S 50 160, 140 200 S 50 280, 140 320"/>
    <g stroke-width="2">%s</g>
  </svg>
  <p class="kicker">Genómica y Proteómica · primer parcial</p>
  <h1>Resumen completo de <em>genómica</em></h1>
  <p class="sub">Actividad previa, clases 1 a 3 y los dos trabajos prácticos, ordenados para estudiar de principio a fin.</p>
  <div class="toc">%s</div>
  <div class="foot">Armado a partir de tus resúmenes de la materia. La parte de transcriptómica y proteómica
  no está incluida: no entra en el primer parcial y no forma parte de este material.</div>
</section>""" % ("".join('<line x1="70" y1="%d" x2="130" y2="%d"/>' % (y, y) for y in range(14, 320, 26)), toc))

    # ---------- mapa mental ----------
    parts.append('<section class="mapa"><h2 style="font-size:19pt;font-weight:800;text-align:left;'
                 'border-bottom:2.5pt solid var(--pink);padding-bottom:2.5mm;margin-bottom:5mm">'
                 'Mapa mental de la materia</h2>' + mapa +
                 '<p>Las ocho ramas que entran en el parcial. Lo resaltado es lo que más aparece en los exámenes.</p></section>')

    # ---------- unidades ----------
    for uid, n, title, src, color in UNITS:
        body, fig = split_figure(sums[uid])
        parts.append('<section class="unit" style="--c:%s">' % color)
        parts.append('<div class="unit-head"><span class="n">UNIDAD %s</span><h2>%s</h2>'
                     '<span class="src">%s</span></div>' % (n, title, src))
        parts.append(body)
        parts.append("</section>")
        if fig:
            parts.append(fig)

    # ---------- anexos ----------
    parts.append('<section class="anexo"><h2>Anexo · tablas y chuletas</h2>')
    for t in ["1 · El camino de los archivos", "2 · Cada herramienta y la pregunta que responde",
              "3 · Tecnologías de secuenciación", "4 · Los patrones de herencia en el VCF",
              "5 · Cómo responder las preguntas", "6 · Los 10 errores que anulan una respuesta",
              "7 · Qué aparece en los modelos viejos"]:
        parts.append(section(recursos, t))
    parts.append("</section>")

    # ---------- glosario ----------
    gl = "".join('<div><b>%s.</b> <span>%s</span></div>' % (g[0], g[1])
                 for g in sorted(GLOSS, key=lambda x: x[0].lower()))
    parts.append('<section class="anexo"><h2>Anexo · glosario</h2><div class="gl">%s</div>'
                 '<div class="hr"></div><p class="muted">%d términos. Versión interactiva, flashcards, '
                 'banco de preguntas y simulacros en la página de estudio del repositorio.</p></section>'
                 % (gl, len(GLOSS)))

    parts.append("</body></html>")
    html = "\n".join(parts)
    out = os.path.join(ROOT, "assets", "resumen-print.html")
    open(out, "w").write(html)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
