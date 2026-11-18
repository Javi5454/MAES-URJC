"""Motor común de los mapas conceptuales de la SA: disposición, comprobaciones y salida en CXL (CmapTools) y TikZ.

Coordenadas en centímetros, con el centro de cada concepto; y crece hacia abajo. Los tamaños de caja imitan los de
CmapTools (Verdana 12) y `comprobar` exige que ninguna caja ni palabra de enlace se solape y que ninguna línea
atraviese un concepto.
"""
from xml.sax.saxutils import quoteattr

COLOR = {
    "marco": ((250, 214, 214), "Marco: situación, contexto, reto, ODS y producto"),
    "curr":  ((210, 226, 250), "Currículo: saberes, competencias, criterios y descriptores"),
    "acc":   ((214, 238, 214), "Actividades, metodología y recursos"),
    "eval":  ((255, 234, 196), "Evaluación: instrumentos y evidencias"),
}
PX = 42  # píxeles de CmapTools por centímetro
TIKZ = {"center": "", "left": ".west", "right": ".east", "top": ".north", "bottom": ".south"}


def W(lab):
    return 0.157 * max(len(l) for l in lab.split("\n")) + 0.6


def H(lab):
    return 0.4 * (lab.count("\n") + 1) + 0.3


def WF(lab):  # palabra de enlace
    return 0.145 * len(lab) + 0.3


def corta(p, q, caja):
    """¿El segmento p-q atraviesa el interior de la caja (x, y, w, h)? (Liang-Barsky)"""
    x, y, w, h = caja
    x0, x1, y0, y1 = x - w / 2 + 0.05, x + w / 2 - 0.05, y - h / 2 + 0.05, y + h / 2 - 0.05
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return False
        else:
            r = qq / pp
            if pp < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
    return t0 < t1


class Mapa:
    """C: {id: (etiqueta, familia, genérico)}. P: [(origen, enlace, [destinos], cruzado, ajuste)].

    Ajuste de la palabra de enlace: None (punto medio), ("t", f) (fracción del recorrido), ("p", x, y[, ancla_origen, ancla_destino])
    (posición fija), ("lista", dy) (lista en columna) o ("cruce", ancla_origen, ancla_destino[, f]).
    """

    def __init__(self, C, titulo, pregunta, nombre, max_palabras=4):
        self.C, self.titulo, self.pregunta, self.nombre = C, titulo, pregunta, nombre
        self.max_palabras = max_palabras
        self.POS, self.LADO, self.P, self.GLOSAS = {}, {}, [], []
        self.XC, self.YL, self.MX, self.MY = 0.0, 0.0, 1.8, 3.4
        self.notas_leyenda = ""
        self.leyenda_extra = ""  # texto suelto bajo la leyenda, en las dos salidas
        self.libres = []  # conceptos sin enlaces: (id, etiqueta, x, y)

    # ---------- disposición ----------
    def pon(self, cid, x, y):
        self.POS[cid] = (x, y)

    def columna(self, ids, borde, lado, y0, paso):
        """Lista en columna. 'R': conceptos a la derecha de la línea de la lista, flechas por su borde izquierdo."""
        for k, cid in enumerate(ids):
            w = W(self.C[cid][0])
            self.pon(cid, borde + w / 2 if lado == "R" else borde - w / 2, y0 + k * paso)
            self.LADO[cid] = "left" if lado == "R" else "right"

    def pila(self, ids, borde, lado, y_arriba, sep=0.35, ys=None):
        """Como `columna`, pero con conceptos de distinta altura; o en las alturas `ys` dadas."""
        y = y_arriba
        for k, cid in enumerate(ids):
            h = H(self.C[cid][0])
            yc = ys[k] if ys else y + h / 2
            self.columna([cid], borde, lado, yc, 0)
            y = yc + h / 2 + sep
        return y

    def ancla(self, cid, a):
        x, y = self.POS[cid]
        w, h = W(self.C[cid][0]), H(self.C[cid][0])
        return {"center": (x, y), "left": (x - w / 2, y), "right": (x + w / 2, y),
                "top": (x, y - h / 2), "bottom": (x, y + h / 2)}[a]

    def frase(self, o, ds, aj):
        xo, yo = self.POS[o]
        if aj and aj[0] == "lista":
            return xo, yo + (aj[1] if len(aj) > 1 else 1.0)
        if aj and aj[0] == "p":
            return aj[1], aj[2]
        if aj and aj[0] == "cruce":
            (x1, y1), (x2, y2) = self.ancla(o, aj[1]), self.ancla(ds[0], aj[2])
            f = aj[3] if len(aj) > 3 else 0.5
            return x1 + f * (x2 - x1), y1 + f * (y2 - y1)
        xd, yd = self.POS[ds[0]]
        f = aj[1] if aj and aj[0] == "t" else 0.5
        return xo + f * (xd - xo), yo + f * (yd - yo)

    def anclas(self, o, d, aj):
        if aj and aj[0] == "cruce":
            return aj[1], aj[2]
        if aj and aj[0] == "lista":
            return "center", self.LADO[d]
        if aj and aj[0] == "p" and len(aj) > 3:
            return aj[3], aj[4]
        return "center", "center"

    # ---------- comprobaciones ----------
    def comprobar(self):
        C, P, POS = self.C, self.P, self.POS
        assert len(C) == len({v[0] for v in C.values()}), "concepto repetido"
        assert set(POS) == set(C), set(C) ^ set(POS)
        assert not [c for c in C if c.startswith("enl")], "identificador reservado"
        for o, _, ds, _, _ in P:
            assert o in C and all(d in C for d in ds), (o, ds)
        assert {o for o, *_ in P} | {d for _, _, ds, _, _ in P for d in ds} == set(C), "concepto suelto"
        for lab, *_ in C.values():
            assert len(lab.replace("\n", " ").split()) <= self.max_palabras or lab.startswith("¿"), lab
        for _, lab, *_ in P:
            assert lab == lab.lower() and lab.split()[0] not in ("es", "tiene", "con", "de"), lab
        cajas = [(cid, *POS[cid], W(C[cid][0]), H(C[cid][0])) for cid in C]
        cajas += [(cid, x, y, W(lab), H(lab)) for cid, lab, x, y in self.libres]
        assert not {cid for cid, *_ in self.libres} & set(C), "concepto libre repetido"
        cajas += [(f"«{lab}» ({o})", *self.frase(o, ds, aj), WF(lab), 0.42) for o, lab, ds, _, aj in P]
        cajas += [(f"glosa «{g[:20]}»", x, y, 0.13 * max(len(l) for l in g.split("\n")) + 0.3, 0.38 * (g.count("\n") + 1))
                  for g, x, y in self.GLOSAS]
        solapes = [f"{a} / {b}" for i, (a, xa, ya, wa, ha) in enumerate(cajas) for b, xb, yb, wb, hb in cajas[i + 1:]
                   if abs(xa - xb) < (wa + wb) / 2 + 0.1 and abs(ya - yb) < (ha + hb) / 2 + 0.05]
        cruces = []
        for o, lab, ds, _, aj in P:
            f = self.frase(o, ds, aj)
            for d in ds:
                a_o, a_d = self.anclas(o, d, aj)
                for p, q, ext in ((self.ancla(o, a_o), f, {o}), (f, self.ancla(d, a_d), {d})):
                    for cid in C:
                        if cid not in ext and corta(p, q, (*POS[cid], W(C[cid][0]), H(C[cid][0]))):
                            cruces.append(f"«{lab}» ({o}→{d}) atraviesa {cid}")
        errores = [f"solape: {s}" for s in solapes] + [f"cruce: {c}" for c in cruces]
        assert not errores, "\n  ".join(["problemas de disposición:"] + errores)

    # ---------- CXL ----------
    def px(self, x, y):
        return round((x + self.MX) * PX), round((y + self.MY) * PX)

    def cxl(self):
        C, P, POS = self.C, self.P, self.POS
        con, lp, cn, ca, la, na = [], [], [], [], [], []
        for cid, (lab, fam, gen) in C.items():
            rgb = COLOR[fam][0]
            X, Y = self.px(*POS[cid])
            con.append(f'<concept id="{cid}" label={quoteattr(lab)}/>')
            ca.append(f'<concept-appearance id="{cid}" x="{X}" y="{Y}" width="{round(W(lab) * PX)}" '
                      f'height="{round(H(lab) * PX)}" background-color="{rgb[0]},{rgb[1]},{rgb[2]},255"'
                      + (' font-style="bold"' if gen else "") + "/>")
        for cid, lab, x, y in self.libres:
            X, Y = self.px(x, y)
            con.append(f'<concept id="{cid}" label={quoteattr(lab)}/>')
            ca.append(f'<concept-appearance id="{cid}" x="{X}" y="{Y}" width="{round(W(lab) * PX)}" '
                      f'height="{round(H(lab) * PX)}" background-color="255,255,255,255"/>')
        # Encabezado: título de la SA y, debajo, la pregunta de enfoque (conceptos sueltos, sin borde)
        X, Y = self.px(self.XC, -2.5)
        con.append(f'<concept id="titulo" label={quoteattr(self.titulo)}/>')
        ca.append(f'<concept-appearance id="titulo" x="{X}" y="{Y}" width="{round((0.2 * len(self.titulo) + 0.6) * PX)}" '
                  f'height="34" background-color="255,255,255,255" border-color="0,0,0,0" font-style="bold" font-size="16"/>')
        X, Y = self.px(self.XC, -1.6)
        texto = "Pregunta de enfoque: " + self.pregunta
        con.append(f'<concept id="foco" label={quoteattr(texto)}/>')
        ca.append(f'<concept-appearance id="foco" x="{X}" y="{Y}" width="{round(W(texto) * PX)}" height="28" '
                  f'background-color="255,255,255,255" border-color="0,0,0,0" font-style="italic"/>')
        x = 0.0
        for fam, (rgb, texto) in COLOR.items():
            w = 0.13 * len(texto) + 0.6
            X, Y = self.px(x + w / 2, self.YL)
            con.append(f'<concept id="ley_{fam}" label={quoteattr(texto)}/>')
            ca.append(f'<concept-appearance id="ley_{fam}" x="{X}" y="{Y}" width="{round(w * PX)}" height="26" '
                      f'background-color="{rgb[0]},{rgb[1]},{rgb[2]},255" font-size="10"/>')
            x += w + 0.8
        if self.leyenda_extra:
            lineas = self.leyenda_extra.split("\n")
            w = 0.12 * max(len(l) for l in lineas) + 0.6
            X, Y = self.px(w / 2, self.YL + 0.6 + 0.3 * len(lineas))
            con.append(f'<concept id="ley_extra" label={quoteattr(self.leyenda_extra)}/>')
            ca.append(f'<concept-appearance id="ley_extra" x="{X}" y="{Y}" width="{round(w * PX)}" height="{12 + 14 * len(lineas)}" '
                      f'background-color="255,255,255,255" border-color="0,0,0,0" font-size="10"/>')
        k = 0
        for i, (o, lab, ds, cruz, aj) in enumerate(P, 1):
            lid = f"lp{i}"
            X, Y = self.px(*self.frase(o, ds, aj))
            lp.append(f'<linking-phrase id="{lid}" label={quoteattr(lab)}/>')
            la.append(f'<linking-phrase-appearance id="{lid}" x="{X}" y="{Y}" width="{round(WF(lab) * PX)}" height="18"/>')
            estilo = ' style="dashed"' if cruz else ""
            for d_i, d in enumerate(ds):
                a_o, a_d = self.anclas(o, d, aj)
                if d_i == 0:
                    k += 1
                    cn.append(f'<connection id="cx{k}" from-id="{o}" to-id="{lid}"/>')
                    na.append(f'<connection-appearance id="cx{k}" from-pos="{a_o}" to-pos="center" arrowhead="no"{estilo}/>')
                k += 1
                cn.append(f'<connection id="cx{k}" from-id="{lid}" to-id="{d}"/>')
                na.append(f'<connection-appearance id="cx{k}" from-pos="center" to-pos="{a_d}" arrowhead="yes"{estilo}/>')
        xmax = max([x + W(C[c][0]) / 2 for c, (x, _) in POS.items()] + [x + W(l) / 2 for _, l, x, _ in self.libres])
        Wm, Hm = self.px(xmax + 1.0, self.YL + 1.0 + 0.6 * (self.leyenda_extra.count("\n") + 1 if self.leyenda_extra else 0))
        j = "\n      ".join
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<cmap xmlns:dcterms="http://purl.org/dc/terms/" xmlns="http://cmap.ihmc.us/xml/cmap/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <res-meta>
    <dc:title>{self.nombre}</dc:title>
    <dc:description>{self.titulo}</dc:description>
    <dc:creator><vcard:FN>Javier Gómez López</vcard:FN></dc:creator>
    <dc:language>es</dc:language>
  </res-meta>
  <map width="{Wm}" height="{Hm}">
    <concept-list>
      {j(con)}
    </concept-list>
    <linking-phrase-list>
      {j(lp)}
    </linking-phrase-list>
    <connection-list>
      {j(cn)}
    </connection-list>
    <concept-appearance-list>
      {j(ca)}
    </concept-appearance-list>
    <linking-phrase-appearance-list>
      {j(la)}
    </linking-phrase-appearance-list>
    <connection-appearance-list>
      {j(na)}
    </connection-appearance-list>
  </map>
</cmap>
'''

    # ---------- TikZ ----------
    def tex(self):
        C, P, POS = self.C, self.P, self.POS

        def t(s):
            return s.replace("\n", r"\\")
        L = [r"""\documentclass[border=8mm]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[scaled=0.92]{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,shadows}
\definecolor{urjc}{RGB}{200,16,46}"""]
        for fam, (rgb, _) in COLOR.items():
            L.append(r"\definecolor{%s}{RGB}{%d,%d,%d}" % (fam, *rgb))
        L.append(r"""\begin{document}
\begin{tikzpicture}[y=-1cm, font=\small,
  c/.style={draw=black!70, rounded corners=3pt, align=center, inner sep=2pt, fill=#1,
    drop shadow={opacity=0.15, shadow xshift=0.6pt, shadow yshift=-0.6pt}},
  lp/.style={fill=white, inner sep=1pt, font=\footnotesize\itshape, text=black!75},
  glosa/.style={font=\footnotesize\itshape, text=urjc!85!black, align=center},
  a/.style={-{Stealth[length=2mm]}, black!65, thick},
  l/.style={black!65, thick},
  cz/.style={dashed}]""")
        L.append(r"\node[font=\Large\bfseries] at (%.2f,-2.5) {%s};" % (self.XC, self.titulo))
        L.append(r"\node[font=\itshape] at (%.2f,-1.6) {\textbf{Pregunta de enfoque:} %s};" % (self.XC, self.pregunta))
        for cid, (lab, fam, gen) in C.items():
            x, y = POS[cid]
            f = r"\bfseries" if gen else ""
            L.append(r"\node[c=%s, font=\small%s, minimum width=%.2fcm, minimum height=%.2fcm] (%s) at (%.2f,%.2f) {%s};"
                     % (fam, f, W(lab) - 0.2, H(lab) - 0.15, cid, x, y, t(lab)))
        for cid, lab, x, y in self.libres:
            L.append(r"\node[c=white, font=\small, minimum width=%.2fcm, minimum height=%.2fcm] (%s) at (%.2f,%.2f) {%s};"
                     % (W(lab) - 0.2, H(lab) - 0.15, cid, x, y, t(lab)))
        for i, (o, lab, ds, cruz, aj) in enumerate(P, 1):
            x, y = self.frase(o, ds, aj)
            e = ",cz" if cruz else ""
            L.append(r"\coordinate (enl%d) at (%.2f,%.2f);" % (i, x, y))
            for d_i, d in enumerate(ds):
                a_o, a_d = self.anclas(o, d, aj)
                if d_i == 0:
                    L.append(r"\draw[l%s] (%s%s) -- (enl%d);" % (e, o, TIKZ[a_o], i))
                L.append(r"\draw[a%s] (enl%d) -- (%s%s);" % (e, i, d, TIKZ[a_d]))
            L.append(r"\node[lp] at (enl%d) {%s};" % (i, lab))
        for texto, x, y in self.GLOSAS:
            L.append(r"\node[glosa] at (%.2f,%.2f) {%s};" % (x, y, t(texto)))
        x = 0.0
        for fam, (_, texto) in COLOR.items():
            L.append(r"\node[c=%s, font=\footnotesize, anchor=west] at (%.2f,%.2f) {%s};" % (fam, x, self.YL, texto))
            x += 0.13 * len(texto) + 1.4
        L.append(r"\draw[l,cz] (%.2f,%.2f) -- ++(1.6,0) node[right, font=\footnotesize, text=black] {enlace cruzado entre ramas};" % (x, self.YL))
        L.append(r"\node[font=\footnotesize, anchor=west] at (%.2f,%.2f) {\textbf{Negrita}: concepto genérico, que baja a un elemento propio de la situación de aprendizaje \quad \textcolor{urjc!85!black}{\itshape Cursiva roja}: por qué el diseño está alineado%s};" % (x + 6.2, self.YL, self.notas_leyenda))
        if self.leyenda_extra:
            L.append(r"\node[font=\footnotesize, anchor=north west, align=left] at (0,%.2f) {%s};"
                     % (self.YL + 0.5, self.leyenda_extra.replace("\n", r"\\")))
        L.append(r"\end{tikzpicture}" "\n" r"\end{document}")
        return "\n".join(L) + "\n"

    def escribir(self, carpeta, cxl, tex):
        self.comprobar()
        (carpeta / cxl).write_text(self.cxl(), encoding="utf-8")
        (carpeta / tex).write_text(self.tex(), encoding="utf-8")
        ancho = max(x + W(self.C[c][0]) / 2 for c, (x, _) in self.POS.items())
        print(f"{tex}: {len(self.C)} conceptos, {len(self.P)} proposiciones, "
              f"{sum(1 for p in self.P if p[3])} enlaces cruzados; ancho {ancho:.0f} cm, sin solapes ni cruces")
