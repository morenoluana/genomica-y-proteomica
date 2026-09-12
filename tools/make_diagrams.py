#!/usr/bin/env python3
"""Genera los diagramas de flujo de trabajo del TP1 y el TP2 (SVG)."""
import html
import os

W = 1680

INK = "#2c1522"
INK2 = "#6d4a5c"
INK3 = "#9b7787"
PANEL = "#fff6fa"
CARD = "#ffffff"
LINE = "#f0cfe0"
LINE2 = "#e3b4cd"
PINK = "#d31c6b"
PINK_D = "#a3134f"
PINK_S = "#ffe3ef"
BLUE = "#0a6dbb"
BLUE_S = "#e2f0fc"
INDIGO = "#4b46cf"
INDIGO_S = "#e8e7fd"
GREEN = "#0f7a52"
GREEN_S = "#dcf5e9"
RED = "#c02040"
RED_S = "#ffe3e9"

FONT = "'Bricolage Grotesque','Trebuchet MS',system-ui,sans-serif"
BODY = "'Source Sans 3','Segoe UI',system-ui,sans-serif"
MONO = "'JetBrains Mono','DejaVu Sans Mono',monospace"


def e(s):
    return html.escape(str(s), quote=True)


def txt(x, y, s, size=15, fill=INK2, weight="400", anchor="start", font=None, ls=None):
    f = font or BODY
    extra = ' letter-spacing="%s"' % ls if ls else ""
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" font-weight="%s" '
            'fill="%s" text-anchor="%s"%s>%s</text>' % (x, y, f, size, weight, fill, anchor, extra, e(s)))


def lines(x, y, arr, size=14, fill=INK2, lh=19, weight="400", font=None):
    return "".join(txt(x, y + i * lh, s, size, fill, weight, font=font) for i, s in enumerate(arr))


def rrect(x, y, w, h, r=14, fill=CARD, stroke=LINE, sw=1.6, extra=""):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" '
            'stroke-width="%g"%s/>' % (x, y, w, h, r, fill, stroke, sw, (" " + extra) if extra else ""))


def chip(x, y, label, fill=PINK_S, stroke=PINK, ink=PINK_D, size=13, font=None, pad=11, h=26):
    w = len(label) * (size * 0.60) + pad * 2
    s = rrect(x, y, w, h, h / 2, fill, stroke, 1.2)
    s += txt(x + w / 2, y + h * 0.68, label, size, ink, "700", "middle", font or BODY)
    return s, w


def arrow_h(x1, x2, y, color=PINK, sw=3):
    m = "ahb" if color == BLUE else "ah"
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g" '
            'stroke-linecap="round" marker-end="url(#%s)"/>' % (x1, y, x2 - 9, y, color, sw, m))


def arrow_v(y1, y2, x, color=PINK, sw=3):
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g" '
            'stroke-linecap="round" marker-end="url(#ah)"/>' % (x, y1, x, y2 - 9, color, sw))


# ----------------------------------------------------------------- iconos ---
def ic_fastq(x, y, c=PINK):
    s = ""
    for i, (dx, w) in enumerate([(0, 40), (6, 32), (2, 36)]):
        s += rrect(x + dx, y + 2 + i * 12, w, 7, 3.5, c if i == 0 else PINK_S, c, 1.2)
    for i in range(8):
        s += '<rect x="%g" y="%g" width="3" height="%g" fill="%s" opacity=".55"/>' % (
            x + i * 5.6, y + 40, max(3, 12 - i * 1.3), c)
    return s


def ic_qc(x, y, c=PINK):
    s = '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6"/>' % (x, y + 44, x + 46, y + 44, c)
    for i, h in enumerate([34, 30, 27, 20, 12, 7]):
        s += '<rect x="%g" y="%g" width="5.5" height="%g" rx="2" fill="%s" opacity="%g"/>' % (
            x + 2 + i * 7.4, y + 44 - h, h, c, 1 - i * 0.11)
    return s


def ic_ref(x, y, c=PINK):
    s = '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % (
        x, y + 30, x + 46, y + 30, c)
    for i in range(6):
        s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2"/>' % (
            x + 3 + i * 8, y + 30, x + 3 + i * 8, y + 38, c)
    s += '<circle cx="%g" cy="%g" r="9" fill="none" stroke="%s" stroke-width="2.6"/>' % (x + 14, y + 14, c)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % (
        x + 20, y + 20, x + 27, y + 26, c)
    return s


def ic_align(x, y, c=PINK):
    s = '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        x, y + 8, x + 46, y + 8, INK3)
    for i, (dx, w) in enumerate([(0, 26), (12, 26), (6, 30), (20, 24)]):
        s += rrect(x + dx, y + 16 + i * 8, w, 5.5, 2.8, c, c, 0)
    return s


def ic_bam(x, y, c=PINK):
    s = rrect(x + 4, y + 2, 38, 44, 6, PINK_S, c, 1.6)
    s += txt(x + 23, y + 21, "0 1 0", 9, c, "700", "middle", MONO)
    s += txt(x + 23, y + 33, "1 0 1", 9, c, "700", "middle", MONO)
    return s


def ic_dedup(x, y, c=PINK):
    s = ""
    for i in range(3):
        s += rrect(x + 2, y + 4 + i * 12, 30, 7, 3.5, PINK_S if i else c, c, 1.2)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        x + 34, y + 18, x + 46, y + 30, RED)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        x + 46, y + 18, x + 34, y + 30, RED)
    return s


def ic_call(x, y, c=PINK):
    s = '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        x, y + 10, x + 46, y + 10, INK3)
    s += txt(x + 20, y + 6, "G", 12, INK3, "700", "middle", MONO)
    for i in range(3):
        s += rrect(x + 2 + i * 4, y + 18 + i * 10, 32, 6, 3, PINK_S, c, 1.2)
    s += rrect(x + 16, y + 18, 12, 26, 3, "none", RED, 1.8)
    s += txt(x + 22, y + 34, "A", 12, RED, "700", "middle", MONO)
    return s


def ic_norm(x, y, c=PINK):
    s = rrect(x + 2, y + 4, 42, 14, 4, PINK_S, c, 1.2)
    s += txt(x + 23, y + 15, "AT--GC", 10, c, "700", "middle", MONO)
    s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2.4" '
          'marker-end="url(#ah)"/>' % (x + 23, y + 22, x + 23, y + 30, c))
    s += rrect(x + 2, y + 30, 42, 14, 4, c, c, 0)
    s += txt(x + 23, y + 41, "--ATGC", 10, "#ffffff", "700", "middle", MONO)
    return s


def ic_tag(x, y, c=PINK):
    s = ('<path d="M%g %g L%g %g A6 6 0 0 1 %g %g L%g %g Z" fill="%s" stroke="%s" stroke-width="1.6"/>'
         % (x + 4, y + 24, x + 22, y + 6, x + 30, y + 6, x + 44, y + 20, PINK_S, c))
    s += ('<path d="M%g %g L%g %g A6 6 0 0 0 %g %g L%g %g Z" fill="none" stroke="%s" stroke-width="1.6"/>'
          % (x + 4, y + 24, x + 22, y + 42, x + 30, y + 42, x + 44, y + 28, c))
    s += '<circle cx="%g" cy="%g" r="3.4" fill="%s"/>' % (x + 33, y + 24, c)
    return s


def ic_db(x, y, c=PINK):
    s = ""
    for i in range(3):
        s += ('<ellipse cx="%g" cy="%g" rx="17" ry="6" fill="%s" stroke="%s" stroke-width="1.6"/>'
              % (x + 20, y + 10 + i * 12, PINK_S, c))
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6"/>' % (x + 3, y + 10, x + 3, y + 34, c)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6"/>' % (x + 37, y + 10, x + 37, y + 34, c)
    s += '<path d="M%g %g h6 v-6 h6 v6 h6 v6 h-6 v6 h-6 v-6 h-6 z" fill="%s"/>' % (x + 26, y + 36, RED)
    return s


def ic_funnel(x, y, c=PINK):
    s = ('<path d="M%g %g L%g %g L%g %g L%g %g L%g %g L%g %g Z" fill="%s" stroke="%s" stroke-width="1.8"/>'
         % (x + 1, y + 4, x + 45, y + 4, x + 28, y + 24, x + 28, y + 44, x + 18, y + 38, x + 18, y + 24, PINK_S, c))
    for i in range(3):
        s += '<circle cx="%g" cy="%g" r="2.6" fill="%s"/>' % (x + 12 + i * 11, y + 11, c)
    return s


def ic_scale(x, y, c=PINK):
    s = '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        x + 23, y + 6, x + 23, y + 44, c)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        x + 5, y + 12, x + 41, y + 12, c)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        x + 12, y + 44, x + 34, y + 44, c)
    s += ('<path d="M%g %g L%g %g L%g %g Z" fill="%s"/>' % (x + 1, y + 26, x + 15, y + 26, x + 8, y + 13, PINK_S))
    s += ('<path d="M%g %g L%g %g L%g %g Z" fill="%s"/>' % (x + 31, y + 26, x + 45, y + 26, x + 38, y + 13, c))
    return s


def ic_dna(x, y, c=PINK):
    s = ('<path d="M%g %g C %g %g, %g %g, %g %g S %g %g, %g %g" fill="none" stroke="%s" stroke-width="2.8"/>'
         % (x + 8, y + 2, x + 40, y + 12, x + 8, y + 24, x + 8 + 16, y + 24 + 0,
            x + 40, y + 36, x + 8, y + 46, c))
    s += ('<path d="M%g %g C %g %g, %g %g, %g %g S %g %g, %g %g" fill="none" stroke="%s" stroke-width="2.8" opacity=".55"/>'
          % (x + 38, y + 2, x + 6, y + 12, x + 38, y + 24, x + 38 - 16, y + 24,
             x + 6, y + 36, x + 38, y + 46, c))
    for i in range(4):
        s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2"/>' % (
            x + 12, y + 8 + i * 10, x + 34, y + 8 + i * 10, c)
    return s


def ic_vcf(x, y, c=PINK):
    s = rrect(x + 3, y + 2, 40, 44, 5, "#ffffff", c, 1.6)
    for i in range(4):
        s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.2" opacity=".5"/>' % (
            x + 3, y + 13 + i * 8, x + 43, y + 13 + i * 8, c)
    s += rrect(x + 3, y + 2, 40, 11, 5, c, c, 0)
    s += txt(x + 23, y + 10.5, "VCF", 8, "#ffffff", "700", "middle", MONO)
    s += txt(x + 8, y + 22, "0/1", 8, INK2, "700", "start", MONO)
    s += txt(x + 8, y + 30, "0/1", 8, INK2, "700", "start", MONO)
    s += txt(x + 8, y + 38, "1/1", 8, PINK_D, "700", "start", MONO)
    return s


def ic_family(x, y, c=PINK):
    s = rrect(x + 1, y + 6, 15, 15, 2, "#ffffff", c, 2)
    s += '<circle cx="%g" cy="%g" r="8" fill="#ffffff" stroke="%s" stroke-width="2"/>' % (x + 37, y + 13, c)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6"/>' % (x + 16, y + 11, x + 29, y + 11, c)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6"/>' % (x + 16, y + 15, x + 29, y + 15, c)
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6"/>' % (x + 23, y + 15, x + 23, y + 30, c)
    s += rrect(x + 15, y + 30, 15, 15, 2, c, c, 0)
    return s


ICONS = {"fastq": ic_fastq, "qc": ic_qc, "ref": ic_ref, "align": ic_align, "bam": ic_bam,
         "dedup": ic_dedup, "call": ic_call, "norm": ic_norm, "tag": ic_tag, "db": ic_db,
         "funnel": ic_funnel, "scale": ic_scale, "dna": ic_dna, "vcf": ic_vcf, "family": ic_family}


def step_card(x, y, w, h, num, title, tool, out, ql, icon, accent=PINK):
    s = rrect(x, y, w, h, 16, CARD, LINE, 1.8)
    s += '<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (x + 18, y, w - 36, accent)
    s += '<circle cx="%g" cy="%g" r="17" fill="%s"/>' % (x + 34, y + 38, accent)
    s += txt(x + 34, y + 45, str(num), 19, "#ffffff", "800", "middle", FONT)
    s += ICONS[icon](x + w - 62, y + 16, accent)
    s += lines(x + 18, y + 88, title, 20, INK, 24, "800", FONT)
    yy = y + 88 + len(title) * 24 + 6
    s += txt(x + 18, yy, tool, 13.5, accent, "700", font=MONO)
    s += lines(x + 18, yy + 24, ql, 14, INK2, 18.5)
    ch, cw = chip(x + 18, y + h - 40, out, "#fbf1f6", LINE2, INK2, 12.5, MONO)
    s += ch
    return s


def head_band(title, subtitle, accent, right_box):
    s = txt(60, 74, title, 40, INK, "800", font=FONT)
    s += txt(60, 108, subtitle, 19, INK2)
    s += '<rect x="60" y="122" width="120" height="6" rx="3" fill="%s"/>' % accent
    s += right_box
    return s


def svg_open(h, extra_defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" width="%g" height="%g" '
            'role="img" style="max-width:100%%;height:auto;display:block">'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
            'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>'
            '<marker id="ahb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
            'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>%s</defs>'
            '<rect x="0" y="0" width="%g" height="%g" rx="0" fill="%s"/>'
            % (W, h, W, h, PINK, BLUE, extra_defs, W, h, PANEL))


# =============================================================== TP 1 ========
def tp1():
    H = 1215
    s = svg_open(H)

    # --- caso ---
    bx, by, bw, bh = 1046, 26, 574, 126
    box = rrect(bx, by, bw, bh, 16, "#ffffff", LINE2, 1.8)
    box += ic_family(bx + 22, by + 34, PINK)
    box += txt(bx + 96, by + 32, "EL CASO", 12.5, INK3, "700", font=BODY, ls="2.6")
    box += lines(bx + 96, by + 58, [
        "Trío familiar: padre + madre + hijo afectado (proband).",
        "Osteopetrosis · padres consanguíneos y asintomáticos.",
        "Hipótesis: herencia autosómica recesiva.",
    ], 15, INK2, 22)
    s += head_band("TP 1 · Del FASTQ a la variante",
                   "Análisis de datos de secuenciación de exomas para el diagnóstico de una enfermedad genética",
                   BLUE, box)

    steps = [
        (1, ["Datos crudos"], "descarga · Illumina paired-end", "FASTQ  R1 + R2  (.fq.gz)", "fastq",
         ["Dos archivos por persona:", "cada fragmento se lee de", "los dos extremos. Todavía", "no sé dónde va cada read."]),
        (2, ["Control de calidad"], "FastQC + MultiQC", "reportes .html", "qc",
         ["¿Mis lecturas son confiables?", "Calidad por base, GC content", "(ojo: es exoma, no genoma)", "y duplicación."]),
        (3, ["Genoma de", "referencia"], "hg19 · cromosoma 8 · BWA index", "FASTA + índices", "ref",
         ["El andamiaje contra el cual", "comparar. Indexar no cambia", "la secuencia: crea archivos", "para buscar rápido."]),
        (4, ["Alineamiento"], "BWA MEM  (+ read groups)", "SAM", "align",
         ["¿Dónde va cada read?", "Los read groups (ID, SM, PL)", "mantienen separados a", "padre ≠ madre ≠ hijo."]),
        (5, ["Compresión", "y orden"], "samtools view · sort · index", "BAM + BAI", "bam",
         ["Lo mismo en binario,", "ordenado por posición e", "indexado para acceder", "rápido a una región."]),
        (6, ["Posprocesamiento"], "filtrado de pares + dedup.", "BAM limpio", "dedup",
         ["Se sacan los duplicados de", "PCR: si no, una molécula", "amplificada muchas veces", "infla la evidencia."]),
        (7, ["Llamado", "de variantes"], "FreeBayes · joint calling", "VCF", "call",
         ["¿Qué difiere de la", "referencia? SNPs, indels,", "MNPs. QUAL = confianza del", "llamado, NO patogenicidad."]),
        (8, ["Normalización"], "bcftools norm", "VCF normalizado", "norm",
         ["Separa multialélicas y", "alinea indels a la izquierda:", "representación consistente", "para cruzar con bases."]),
        (9, ["Anotación", "funcional"], "SnpEff", "VCF + efecto e IMPACT", "tag",
         ["¿Qué significa? Gen, efecto", "(missense, stop_gained,", "frameshift), IMPACT y", "nomenclatura c. / p."]),
        (10, ["Anotación clínica", "y poblacional"], "SnpSift · ClinVar · 1000G", "VCF anotado", "db",
         ["¿Ya se conoce clínicamente?", "¿Qué tan frecuente es?", "AF global y por población", "(EUR, AFR, AMR, EAS, SAS)."]),
    ]

    cw, gap, x0 = 291, 26, 60
    rows = [(steps[:5], 196), (steps[5:], 546)]
    ch = 300
    for row, ry in rows:
        for i, (num, title, tool, out, icon, ql) in enumerate(row):
            x = x0 + i * (cw + gap)
            accent = BLUE if ry == 196 else PINK
            s += step_card(x, ry, cw, ch, num, title, tool, out, ql, icon, accent)
            if i < 4:
                s += arrow_h(x + cw + 4, x + cw + gap - 4, ry + ch / 2, accent, 3.2)
    # conector de fila 1 a fila 2
    s += ('<path d="M %g %g C %g %g, %g %g, %g %g" fill="none" stroke="%s" stroke-width="3.2" '
          'stroke-dasharray="9 7" marker-end="url(#ah)"/>'
          % (x0 + 4 * (cw + gap) + cw / 2, 196 + ch + 6, x0 + 4 * (cw + gap) + cw / 2, 520,
             x0 + cw / 2, 470, x0 + cw / 2, 540, PINK))
    lbl = "las lecturas ya están alineadas y limpias"
    lw = len(lbl) * 7.6 + 28
    s += rrect(W / 2 + 40 - lw / 2, 496, lw, 28, 14, PANEL, PANEL, 0)
    s += txt(W / 2 + 40, 515, lbl, 14, INK3, "600", "middle")

    # --- banda final ---
    fy = 900
    s += rrect(60, fy, 1560, 250, 18, "#ffffff", LINE2, 1.8)
    s += '<rect x="60" y="%g" width="1560" height="6" rx="3" fill="%s"/>' % (fy, GREEN)

    s += ic_funnel(96, fy + 34, PINK)
    s += txt(154, fy + 52, "11 · FILTRO FINAL", 19, INK, "800", font=FONT)
    s += txt(154, fy + 74, "SnpSift filter", 13.5, PINK, "700", font=MONO)
    crit = ["proband 1/1 · padre 0/1 · madre 0/1", "IMPACT = HIGH o MODERATE",
            "frecuencia < 1%", "evidencia en ClinVar"]
    for i, c in enumerate(crit):
        cch, ccw = chip(96, fy + 96 + i * 34, c, PINK_S, PINK, PINK_D, 13.5)
        s += cch
    s += txt(96, fy + 240, "de miles de variantes a unas pocas candidatas", 13.5, INK3, "600")

    s += arrow_h(520, 566, fy + 125, PINK, 3.2)

    s += rrect(580, fy + 40, 470, 170, 14, BLUE_S, BLUE, 1.6)
    s += txt(602, fy + 70, "12 · LA VARIANTE CANDIDATA", 17, INK, "800", font=FONT)
    s += txt(602, fy + 104, "CA2   c.290G>A   p.Trp97*", 22, BLUE, "700", font=MONO)
    s += lines(602, fy + 132, [
        "stop_gained → codón de parada prematuro,",
        "proteína truncada (IMPACT HIGH).",
        "Deficiencia de anhidrasa carbónica II:",
        "osteopetrosis con acidosis tubular renal.",
    ], 14, INK2, 19)

    s += arrow_h(1064, 1110, fy + 125, PINK, 3.2)

    s += rrect(1124, fy + 40, 470, 170, 14, GREEN_S, GREEN, 1.6)
    s += ic_scale(1520, fy + 56, GREEN)
    s += txt(1146, fy + 70, "13 · INTERPRETACIÓN ACMG/AMP", 17, INK, "800", font=FONT)
    ev = [("PVS1", "muy fuerte · pérdida de función"), ("PM2", "moderado · ausente en 1000G"),
          ("PP1", "apoyo · cosegrega en la familia"), ("PP4", "apoyo · el fenotipo coincide")]
    for i, (k, v) in enumerate(ev):
        s += txt(1146, fy + 100 + i * 21, k, 14, GREEN, "700", font=MONO)
        s += txt(1200, fy + 100 + i * 21, v, 13.5, INK2)
    cch, ccw = chip(1146, fy + 176, "= PATOGÉNICA", GREEN, GREEN, "#ffffff", 15)
    s += cch

    # --- pie ---
    s += rrect(60, 1166, 1560, 34, 10, RED_S, RED, 1.2)
    s += txt(W / 2, 1188, "QUAL ≠ impacto biológico    ·    IMPACT ≠ patogenicidad    ·    AF = 0 no demuestra que la variante no exista",
             14.5, RED, "700", "middle")
    return s + "</svg>"


# =============================================================== TP 2 ========
def tp2():
    H = 1215
    s = svg_open(H)

    bx, by, bw, bh = 1046, 26, 574, 126
    box = rrect(bx, by, bw, bh, 16, "#ffffff", LINE2, 1.8)
    box += ic_vcf(bx + 22, by + 36, INDIGO)
    box += txt(bx + 96, by + 32, "LOS DATOS", 12.5, INK3, "700", font=BODY, ls="2.6")
    box += lines(bx + 96, by + 58, [
        "Familia real sana CEPH/Utah 1463: NA12891 (padre),",
        "NA12892 (madre), NA12878 (hija). Los docentes agregaron",
        "una variante patogénica real y publicada (spike-in).",
    ], 14.5, INK2, 21)
    s += head_band("TP 2 · Anotar, filtrar y clasificar",
                   "Del VCF de un trío familiar a una variante candidata clasificada con criterios ACMG/AMP",
                   INDIGO, box)

    # --- 1. entrada + pedigrí ---
    px, py, pw, ph = 60, 196, 610, 500
    s += rrect(px, py, pw, ph, 18, CARD, LINE, 1.8)
    s += '<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (px + 18, py, pw - 36, INDIGO)
    s += '<circle cx="%g" cy="%g" r="17" fill="%s"/>' % (px + 34, py + 38, INDIGO)
    s += txt(px + 34, py + 45, "1", 19, "#ffffff", "800", "middle", FONT)
    s += ic_family(px + pw - 62, py + 16, INDIGO)
    s += txt(px + 18, py + 92, "El pedigrí decide qué busco", 22, INK, "800", font=FONT)
    s += txt(px + 18, py + 116, "VCF + archivo .tfam", 13.5, INDIGO, "700", font=MONO)
    s += lines(px + 18, py + 140, [
        "El .tfam trae familia, individuo, padre, madre, sexo y fenotipo.",
        "Fenotipo: 1 = no afectado, 2 = afectado.   Sexo: 1 = macho, 2 = hembra.",
    ], 14, INK2, 19)

    ty = py + 186
    heads = ["patrón de herencia", "hija", "padre", "madre"]
    cols = [px + 22, px + 340, px + 430, px + 520]
    for i, h in enumerate(heads):
        s += txt(cols[i] + (0 if i == 0 else 32), ty, h, 12, INK3, "700", "start" if i == 0 else "middle", BODY, "1.4")
    pats = [
        ("Autosómico recesivo", "1/1", "0/1", "0/1", True),
        ("Dominante del padre", "0/1", "0/1", "0/0", False),
        ("Dominante de la madre", "0/1", "0/0", "0/1", False),
        ("Dominante de novo", "0/1", "0/0", "0/0", False),
        ("No heredada (hija sana)", "0/0", "0/1", "0/1", False),
    ]
    for i, (name, a, b, c, hi) in enumerate(pats):
        yy = ty + 22 + i * 44
        if hi:
            s += rrect(px + 14, yy, pw - 28, 38, 10, INDIGO_S, INDIGO, 1.6)
        s += txt(px + 22, yy + 25, name, 15, INK if hi else INK2, "700" if hi else "600")
        for j, g in enumerate([a, b, c]):
            gx = cols[j + 1] + 4
            fill = INDIGO if (hi and g == "1/1") else ("#ffffff" if not hi else "#ffffff")
            ink = "#ffffff" if (hi and g == "1/1") else INK2
            s += rrect(gx, yy + 7, 56, 24, 12, fill, INDIGO if hi else LINE2, 1.4)
            s += txt(gx + 28, yy + 24, g, 14, ink, "700", "middle", MONO)
    s += txt(px + 22, py + ph - 26,
             "0 = alelo de referencia   ·   1 = alelo alternativo   ·   0|1 phased se normaliza a 0/1",
             13, INK3, "600")

    # --- 2. anotar: capas ---
    ax, ay, aw, ah = 700, 196, 920, 250
    s += rrect(ax, ay, aw, ah, 18, CARD, LINE, 1.8)
    s += '<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (ax + 18, ay, aw - 36, PINK)
    s += '<circle cx="%g" cy="%g" r="17" fill="%s"/>' % (ax + 34, ay + 38, PINK)
    s += txt(ax + 34, ay + 45, "2", 19, "#ffffff", "800", "middle", FONT)
    s += txt(ax + 62, ay + 45, "Anotar: capas de información sobre el mismo VCF", 22, INK, "800", font=FONT)

    layers = [
        ("bcftools norm", "separa multialélicas · alinea indels a la izquierda", "#fbe9f2"),
        ("SnpEff", "gen · efecto · IMPACT (HIGH…MODIFIER) · HGVSp p.Trp97*", "#f7e2ee"),
        ("ClinVar", "¿ya fue reportada? clasificación + review status (estrellas)", "#f3daea"),
        ("1000 Genomes", "AF global y por población (EUR, AFR, AMR, EAS, SAS)", "#efd2e5"),
    ]
    for i, (name, desc, fill) in enumerate(layers):
        ly = ay + 72 + i * 36
        s += rrect(ax + 24 + i * 10, ly, aw - 60 - i * 20, 30, 8, fill, PINK, 1.3)
        s += txt(ax + 38 + i * 10, ly + 20, name, 14.5, PINK_D, "700", font=MONO)
        s += txt(ax + 200, ly + 20, desc, 14, INK2)
    s += txt(ax + 24, ay + ah - 16, "El VCF es siempre el mismo archivo: cada herramienta le agrega columnas de información.",
             13, INK3, "600")

    # --- 3. filtrar: embudo ---
    fx, fy2, fw, fh = 700, 466, 920, 230
    s += rrect(fx, fy2, fw, fh, 18, CARD, LINE, 1.8)
    s += '<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (fx + 18, fy2, fw - 36, PINK)
    s += '<circle cx="%g" cy="%g" r="17" fill="%s"/>' % (fx + 34, fy2 + 38, PINK)
    s += txt(fx + 34, fy2 + 45, "3", 19, "#ffffff", "800", "middle", FONT)
    s += txt(fx + 62, fy2 + 45, "Filtrar: recién acá se descartan variantes", 22, INK, "800", font=FONT)
    s += ic_funnel(fx + fw - 62, fy2 + 16, PINK)

    steps_f = [
        ("miles de variantes", "una persona sana difiere mucho de la referencia", 460),
        ("patrón de herencia", "hija 1/1 · padre 0/1 · madre 0/1", 390),
        ("IMPACT HIGH o MODERATE", "priorizo lo que puede alterar la proteína", 330),
        ("frecuencia < 5%", "una enfermedad rara no viene de una variante común", 260),
        ("unas pocas candidatas", "ahora sí miro variante por variante", 200),
    ]
    for i, (name, desc, wbar) in enumerate(steps_f):
        yy = fy2 + 72 + i * 30
        cx = fx + 30
        s += rrect(cx, yy, wbar, 25, 8, PINK if i == 4 else PINK_S, PINK, 1.3)
        s += txt(cx + 12, yy + 17, name, 14, "#ffffff" if i == 4 else PINK_D, "700")
        s += txt(cx + wbar + 16, yy + 17, desc, 13.5, INK3)

    # --- 4. ACMG ---
    gx, gy, gw, gh = 60, 716, 1560, 340
    s += rrect(gx, gy, gw, gh, 18, CARD, LINE, 1.8)
    s += '<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (gx + 18, gy, gw - 36, GREEN)
    s += '<circle cx="%g" cy="%g" r="17" fill="%s"/>' % (gx + 34, gy + 38, GREEN)
    s += txt(gx + 34, gy + 45, "4", 19, "#ffffff", "800", "middle", FONT)
    s += txt(gx + 62, gy + 45, "Interpretar: combinar la evidencia con los criterios ACMG/AMP", 22, INK, "800", font=FONT)
    s += ic_scale(gx + gw - 62, gy + 16, GREEN)

    crit = [
        ("PVS1", "muy fuerte", "pérdida de función (nonsense, frameshift, splicing) en un gen donde la LoF causa la enfermedad", "SnpEff · IMPACT HIGH", GREEN),
        ("PS1 / PM5", "fuerte / moderado", "la misma variante ya fue reportada patogénica / otra patogénica afecta el mismo codón", "ClinVar", GREEN),
        ("PM2", "moderado", "ausente o extremadamente rara en poblaciones de referencia", "1000 Genomes · gnomAD", GREEN),
        ("PP1", "de apoyo", "cosegrega con la enfermedad dentro de la familia", "pedigrí .tfam", GREEN),
        ("PP4", "de apoyo", "el fenotipo del paciente coincide con la enfermedad del gen", "clínica · OMIM · UniProt", GREEN),
        ("BA1 / BS1", "en contra", "demasiado frecuente para una enfermedad rara → evidencia de que NO es patogénica", "1000 Genomes · gnomAD", RED),
    ]
    for i, (k, w8, desc, src, col) in enumerate(crit):
        yy = gy + 84 + i * 32
        s += rrect(gx + 24, yy, 110, 26, 8, GREEN_S if col == GREEN else RED_S, col, 1.3)
        s += txt(gx + 79, yy + 18, k, 14, col, "700", "middle", MONO)
        s += txt(gx + 148, yy + 18, w8, 13.5, col, "700")
        s += txt(gx + 302, yy + 18, desc, 14, INK2)
        s += txt(gx + gw - 30, yy + 18, src, 13, INK3, "600", "end", MONO)

    # escala de clasificación
    sy = gy + 322
    labels = [("BENIGNA", "#e6f0ec"), ("PROB. BENIGNA", "#eaf3ef"), ("VUS", "#f3eef1"),
              ("PROB. PATOGÉNICA", "#ffdde9"), ("PATOGÉNICA", PINK)]
    swid = (gw - 48) / 5
    for i, (lab, fill) in enumerate(labels):
        x = gx + 24 + i * swid
        s += rrect(x, sy - 30, swid - 6, 26, 8, fill, PINK if i == 4 else LINE2, 1.3)
        s += txt(x + (swid - 6) / 2, sy - 12, lab, 13, "#ffffff" if i == 4 else INK2, "700", "middle")

    # --- pie ---
    s += rrect(60, 1080, 1560, 112, 14, RED_S, RED, 1.4)
    s += txt(88, 1108, "LO QUE MÁS SE PIERDE PUNTOS", 12.5, RED, "700", font=BODY, ls="2.4")
    notes = [
        "Todo tiene que estar en la MISMA versión del genoma: VCF, FASTA, SnpEff, ClinVar y 1000 Genomes (acá, GRCh38). Las coordenadas cambian entre GRCh37 y GRCh38.",
        "Antes de anotar con 1000 Genomes se sacan los campos AF/AC/AN propios del VCF: si no, confundís la frecuencia de tu trío con la frecuencia poblacional.",
        "IMPACT ≠ patogenicidad   ·   raro ≠ patogénico   ·   la mayoría de las variantes son LOW/MODIFIER y no están en ClinVar: es lo esperable.",
    ]
    s += lines(88, 1132, notes, 14, INK2, 21)
    return s + "</svg>"


# ========================================================== MAPA MENTAL =====
BRANCHES = [
    ("1", "El genoma humano", "Actividad previa", "#a8560c", "dna", [
        ("3,2 × 10⁹ pb · 22 pares de autosomas + sexuales.", 0),
        ("Sólo 2–3% codifica proteínas (~23.000 genes);", 1),
        ("los exones son ~1% del genoma.", 2),
        ("Fenotipo = genotipo + ambiente + historia de vida", 0),
        ("+ epigenética. El genoma condiciona, no determina.", 2),
        ("No codificante: promotores, enhancers, silencers,", 0),
        ("ARNt, ARNr, miARN, siARN, lncRNA.", 2),
        ("Repetitivas: LINE 21% · SINE/Alu 13% · mini y", 0),
        ("microsatélites · telómeros · pseudogenes.", 2),
        ("Transposones ~45%: clase I (vía ARN, transcriptasa", 0),
        ("reversa) vs clase II (transposasa, cortar y pegar).", 2),
        ("Un gen → muchas proteínas: splicing alternativo (95%),", 1),
        ("promotores alternativos, edición de ARN.", 2),
        ("Organización: nucleoide y plásmidos vs nucleosoma →", 0),
        ("cromatina → cromosoma. Endosimbiosis.", 2),
        ("Identificar genes: ORF en 6 marcos, TATA, GT–AG,", 0),
        ("ESTs, homología y conservación.", 2),
    ]),
    ("2", "Ómicas y validación", "Clase 1", "#d31c6b", "dna", [
        ("Genética (genes sueltos) vs genómica (genoma completo)", 0),
        ("vs genómica funcional: cómo el genoma se hace función.", 2),
        ("Transcriptoma · proteoma · metaboloma · epigenoma ·", 0),
        ("metagenómica · microbioma. Todos dinámicos.", 2),
        ("Qué estudio en cada molécula: ADN = secuencia;", 1),
        ("ARN = abundancia; proteína = abundancia (MS, ELISA).", 2),
        ("Hypothesis-driven vs discovery-driven: las ómicas", 0),
        ("generan hipótesis a partir de datos masivos.", 2),
        ("Validación técnica (¿la medición es real? Sanger, qPCR),", 1),
        ("biológica (otra cohorte) y funcional (KO, CRISPR).", 1),
        ("Casos: Pääbo (ADNmt → genoma nuclear; 1–4% neandertal)", 0),
        ("y C4 en esquizofrenia (poda sináptica, ratones KO).", 2),
        ("Somos >99,9% iguales: variantes de susceptibilidad ≠", 0),
        ("mutación causal (esquizofrenia vs fibrosis quística).", 2),
    ]),
    ("3", "Proyecto Genoma Humano", "Clase 2", "#7333e0", "ref", [
        ("HGP 1990–2003: público, internacional, secuencias", 0),
        ("liberadas en 24 h. 20 voluntarios, ~70% de uno solo.", 2),
        ("Collins: hierarchical shotgun (BAC → mapa físico →", 1),
        ("secuenciar). Venter: whole-genome shotgun.", 1),
        ("Los dos usaron Sanger: cambia la estrategia, no la", 1),
        ("química. Celera además usó los datos públicos.", 2),
        ("2001 borradores · 2004 eucromatina 99%, 341 gaps,", 0),
        ("20.000–25.000 genes.", 2),
        ("2022 T2T (CHM13: autosomas + X, es 46,XX) ·", 0),
        ("2023 cromosoma Y (HG002), con PacBio HiFi + Nanopore.", 2),
        ("El problema de la heterocromatina era el ensamblaje", 1),
        ("de secuencias repetitivas, no la química.", 1),
        ("Secuenciar ≠ anotar. GENCODE, Ensembl, RefSeq y CHESS", 1),
        ("dan números de genes distintos.", 2),
    ]),
    ("4", "NGS y tecnologías", "Clase 2", "#0a6dbb", "align", [
        ("2ª generación: secuenciación por síntesis, masiva en", 0),
        ("paralelo, microfluídica, amplificación previa.", 2),
        ("454 → PPi y luz · Ion Torrent → H⁺ y potencial ·", 1),
        ("Illumina → fluoróforos + terminadores reversibles.", 1),
        ("Homopolímeros: problema de 454 e Ion Torrent; Illumina", 1),
        ("los resuelve (una base por ciclo).", 2),
        ("3ª generación: molécula única y long reads. PacBio", 1),
        ("(ZMW, por síntesis) · Nanopore (corriente iónica, NO).", 1),
        ("FASTQ = reads + calidad (cae al final por", 0),
        ("desincronización) vs FASTA = sólo secuencia.", 2),
        ("Profundidad 30X · paired-end · multiplexado y barcodes", 0),
        ("(más muestras = menos profundidad).", 2),
        ("De novo vs contra referencia → mapeo → variant calling", 0),
        ("→ VCF (CHROM, POS, REF, ALT, QUAL).", 2),
        ("WGS · WES · targeted (captura por sondas o PCR).", 0),
        ("SNP array = genotipificación de posiciones conocidas,", 1),
        ("no secuenciación: LD, GWAS, servicios tipo 23andMe.", 1),
    ]),
    ("5", "Variación y poblaciones", "Clase 3", "#0c7d73", "family", [
        ("Somos diploides: homocigota (A/A) vs heterocigota (A/G).", 0),
        ("Tipos: SNV/SNP, indels, estructurales (deleciones,", 0),
        ("duplicaciones, inversiones, translocaciones), CNV.", 2),
        ("Germinales (heredables, en todas las células) vs", 1),
        ("somáticas (aparecen en un linaje durante la vida).", 1),
        ("Primeros diploides: HuRef (Levy 2007) y Watson", 0),
        ("(Wheeler 2008): 7,4X, <1 M USD, ~3,3 M de SNPs.", 2),
        ("Duplicaciones segmentarias: >5 kb y >90% identidad.", 0),
        ("CNVs detectadas por CGH y SNP arrays.", 2),
        ("Mayor diversidad genética en África; fuera de África", 1),
        ("hay menos por efecto fundador.", 1),
        ("Cuello de botella (la población se reduce) vs efecto", 0),
        ("fundador (un grupo se separa) · admixture.", 2),
        ("Earth BioGenome y Darwin Tree of Life: sólo el 1% de", 0),
        ("los eucariotas; long reads, ensamblado y anotación.", 2),
    ]),
    ("6", "Bases de datos y GWAS", "Clase 3", "#b01345", "db", [
        ("dbSNP: identificadores (rsID), inclusiva y NO curada.", 0),
        ("1000 Genomes: variabilidad poblacional, frecuencias,", 0),
        ("haplotipos y LD (3202 muestras, 26 poblaciones).", 2),
        ("gnomAD: frecuencias alélicas por población; es la que", 1),
        ("se usa hoy para filtrar. Ensembl: consecuencias.", 1),
        ("ENCODE: elementos funcionales (ChIP-seq, ATAC-seq,", 0),
        ("DNase-seq). Crítica: estado molecular ≠ función causal.", 2),
        ("ChIP-seq: anticuerpo + beads → ADN unido → secuenciar", 0),
        ("→ dónde estaba unida la proteína.", 2),
        ("ClinVar: interpretación clínica, review status", 1),
        ("(estrellas) y conflictos → VUS. ClinGen: gen-enfermedad", 1),
        ("y dosage. PharmGKB: alelos estrella (haplotipos).", 1),
        ("GWAS: casos vs controles → genotipificación → QC →", 0),
        ("PLINK → Manhattan plot → follow-up.", 2),
        ("Asociación ≠ causalidad. Cosegregación familiar.", 1),
        ("El PRS usa los resultados de los GWAS como pesos.", 0),
    ]),
    ("7", "TP 1 · del FASTQ a la variante", "Trabajo práctico 1", "#4b46cf", "fastq", [
        ("Trío con osteopetrosis, padres consanguíneos y sanos", 0),
        ("→ hipótesis de herencia autosómica recesiva.", 2),
        ("¿Por qué exoma? ~1% del genoma pero concentra las", 0),
        ("variantes de enfermedad; más barato que WGS.", 2),
        ("FASTQ → FastQC/MultiQC → BWA MEM (SAM, read groups)", 1),
        ("→ samtools (BAM + BAI) → dedup → FreeBayes (VCF).", 1),
        ("La deduplicación evita que una molécula amplificada", 0),
        ("infle la evidencia de una variante.", 2),
        ("QUAL = confianza del llamado, NO patogenicidad.", 1),
        ("SnpEff: efecto, IMPACT (HIGH…MODIFIER) y HGVS", 0),
        ("(c.290G>A / p.Trp97*).", 2),
        ("Filtro: 1/1 + 0/1 + 0/1 · HIGH o MODERATE · AF <1%", 1),
        ("· ClinVar → candidata CA2 p.Trp97*.", 1),
        ("ACMG: PVS1 + PM2 + PP1 + PP4 = PATOGÉNICA.", 1),
    ]),
    ("8", "TP 2 · anotar, filtrar y clasificar", "Trabajo práctico 2", "#c2185b", "vcf", [
        ("Arranca en VCF + .tfam: familia CEPH/Utah 1463 (sana)", 0),
        ("con una variante patogénica real agregada (spike-in).", 2),
        ("El pedigrí define el patrón: recesivo (1/1, 0/1, 0/1),", 1),
        ("dominante heredado, de novo (0/1, 0/0, 0/0).", 1),
        ("Todo en GRCh38: VCF, FASTA, SnpEff, ClinVar y 1000G.", 1),
        ("Las coordenadas cambian entre versiones.", 2),
        ("bcftools norm: multialélicas e indels (left alignment).", 0),
        ("Phased 0|1 se normaliza a 0/1.", 2),
        ("Capas: SnpEff → ClinVar → 1000 Genomes (antes se sacan", 0),
        ("los AF/AC/AN propios del VCF).", 2),
        ("La mayoría de las variantes son LOW/MODIFIER y no están", 0),
        ("en ClinVar: es lo esperable en una persona sana.", 2),
        ("Orden: herencia → impacto → frecuencia → evidencia", 1),
        ("clínica → relación gen-fenotipo → ACMG/AMP.", 1),
        ("ACMG: PVS1, PS1/PM5, PM2, PP1, PP4 y BA1/BS1 →", 1),
        ("patogénica … VUS … benigna.", 1),
    ]),
]


def branch_card(x, y, w, num, title, src, color, icon, bullets):
    lh = 20.5
    h = 86 + len(bullets) * lh + 16
    s = rrect(x, y, w, h, 16, CARD, LINE, 1.8)
    s += '<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (x + 18, y, w - 36, color)
    s += '<circle cx="%g" cy="%g" r="16" fill="%s"/>' % (x + 32, y + 38, color)
    s += txt(x + 32, y + 45, num, 18, "#ffffff", "800", "middle", FONT)
    s += txt(x + 58, y + 36, title, 21, INK, "800", font=FONT)
    s += txt(x + 58, y + 58, src.upper(), 11.5, INK3, "700", font=BODY, ls="2.2")
    s += ICONS[icon](x + w - 58, y + 14, color)
    s += '<rect x="%g" y="%g" width="3" height="%g" rx="1.5" fill="%s" opacity=".35"/>' % (
        x + 24, y + 76, len(bullets) * lh + 2, color)
    for i, (t, kind) in enumerate(bullets):
        yy = y + 92 + i * lh
        if kind != 2:
            s += '<circle cx="%g" cy="%g" r="3" fill="%s"/>' % (x + 25.5, yy - 4.5, color)
        s += txt(x + 38, yy, t, 14, color if kind == 1 else INK2, "700" if kind == 1 else "400")
    return s, h


def card_h(b):
    return 86 + len(b[5]) * 20.5 + 16


def mapa():
    gap = 18
    top = 168
    colL = sum(card_h(b) for b in BRANCHES[:4]) + 3 * gap
    colR = sum(card_h(b) for b in BRANCHES[4:]) + 3 * gap
    H = top + max(colL, colR) + 130
    s = svg_open(H)
    s += txt(60, 74, "Mapa mental · lo que entra en el primer parcial", 40, INK, "800", font=FONT)
    s += txt(60, 108, "Genómica: actividad previa, clases 1 a 3 y los dos trabajos prácticos", 19, INK2)
    s += '<rect x="60" y="122" width="120" height="6" rx="3" fill="%s"/>' % PINK

    lw, rw = 540, 540
    lx, rx = 60, 1080
    left_pos, right_pos = [], []
    yy = top
    for i in range(4):
        left_pos.append(yy)
        yy += card_h(BRANCHES[i]) + gap
    yy = top
    for i in range(4, 8):
        right_pos.append(yy)
        yy += card_h(BRANCHES[i]) + gap

    # hub
    hw, hh = 280, 292
    hx = 700
    hy = top + max(colL, colR) / 2 - hh / 2
    for i, b in enumerate(BRANCHES):
        color = b[3]
        if i < 4:
            y0 = left_pos[i]
            hgt = card_h(b)
            s += ('<path d="M %g %g C %g %g, %g %g, %g %g" fill="none" stroke="%s" '
                  'stroke-width="4" stroke-linecap="round" opacity=".85"/>'
                  % (hx + 4, hy + hh / 2, hx - 50, hy + hh / 2, lx + lw + 70, y0 + hgt / 2,
                     lx + lw + 6, y0 + hgt / 2, color))
            s += '<circle cx="%g" cy="%g" r="6" fill="%s"/>' % (lx + lw + 6, y0 + hgt / 2, color)
        else:
            y0 = right_pos[i - 4]
            hgt = card_h(b)
            s += ('<path d="M %g %g C %g %g, %g %g, %g %g" fill="none" stroke="%s" '
                  'stroke-width="4" stroke-linecap="round" opacity=".85"/>'
                  % (hx + hw - 4, hy + hh / 2, hx + hw + 50, hy + hh / 2, rx - 70, y0 + hgt / 2,
                     rx - 6, y0 + hgt / 2, color))
            s += '<circle cx="%g" cy="%g" r="6" fill="%s"/>' % (rx - 6, y0 + hgt / 2, color)

    for i, (num, title, src, color, icon, bullets) in enumerate(BRANCHES):
        if i < 4:
            c, _ = branch_card(lx, left_pos[i], lw, num, title, src, color, icon, bullets)
        else:
            c, _ = branch_card(rx, right_pos[i - 4], rw, num, title, src, color, icon, bullets)
        s += c

    # nodo central
    s += rrect(hx, hy, hw, hh, 24, "#ffffff", PINK, 3)
    s += txt(hx + hw / 2, hy + 58, "GENÓMICA", 40, PINK, "800", "middle", FONT)
    s += txt(hx + hw / 2, hy + 86, "primer parcial", 19, INK2, "600", "middle")
    s += '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6"/>' % (
        hx + 40, hy + 104, hx + hw - 40, hy + 104, LINE2)
    s += txt(hx + hw / 2, hy + 130, "Del genoma a la función:", 14.5, INK2, "700", "middle")
    s += lines(hx + 26, hy + 154, [
        "qué hay en el genoma, cómo se",
        "lee, cómo varía entre personas",
        "y cómo se interpreta una variante.",
    ], 14, INK2, 20)
    chips = ["Act. previa", "Clase 1", "Clase 2", "Clase 3", "TP 1", "TP 2"]
    cxp, cyp = hx + 22, hy + 228
    for c in chips:
        _, cwid = chip(cxp, cyp, c, PINK_S, PINK, PINK_D, 11.5, BODY, 8, 22)
        if cxp + cwid > hx + hw - 18:
            cxp, cyp = hx + 22, cyp + 28
        ch, cwid = chip(cxp, cyp, c, PINK_S, PINK, PINK_D, 11.5, BODY, 8, 22)
        s += ch
        cxp += cwid + 6

    # pie: los pares que no se confunden
    fy = top + max(colL, colR) + 10
    s += rrect(60, fy, 1560, 88, 14, RED_S, RED, 1.4)
    s += txt(88, fy + 30, "LOS PARES QUE NO SE PUEDEN CONFUNDIR", 12.5, RED, "700", font=BODY, ls="2.4")
    s += lines(88, fy + 56, [
        "secuenciar ≠ anotar    ·    llamado de variantes ≠ anotación de variantes    ·    QUAL ≠ impacto biológico    ·    IMPACT ≠ patogenicidad",
        "asociación (GWAS) ≠ causalidad    ·    raro ≠ patogénico    ·    exoma ≠ expresión    ·    SNP array ≠ secuenciación    ·    AF = 0 ≠ inexistente",
    ], 15, INK2, 22)
    return s + "</svg>"


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "assets")
    os.makedirs(out, exist_ok=True)
    for name, fn in (("tp1-flujo", tp1), ("tp2-flujo", tp2), ("mapa-mental", mapa)):
        p = os.path.join(out, name + ".svg")
        with open(p, "w") as f:
            f.write(fn())
        print(p, os.path.getsize(p), "bytes")


if __name__ == "__main__":
    main()
