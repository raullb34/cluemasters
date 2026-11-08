"""Genera la clave y el mensaje en cifrado Pigpen (símbolos 'alienígenas') como SVG."""
import sys
from pathlib import Path

S = 40  # tamaño de cada símbolo
STROKE = 'stroke="#111" stroke-width="3" stroke-linecap="round" fill="none"'


def glyph(ch, x, y):
    """Devuelve el SVG de un símbolo pigpen con la esquina superior izquierda en (x, y)."""
    i = ord(ch) - ord("A")
    p = []
    if i < 18:  # rejillas de 3x3 (A-I sin punto, J-R con punto)
        dot, k = i >= 9, i % 9
        r, c = divmod(k, 3)
        x0, y0, x1, y1 = x + 4, y + 4, x + S - 4, y + S - 4
        if c > 0: p.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" {STROKE}/>')
        if c < 2: p.append(f'<line x1="{x1}" y1="{y0}" x2="{x1}" y2="{y1}" {STROKE}/>')
        if r > 0: p.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" {STROKE}/>')
        if r < 2: p.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" {STROKE}/>')
    else:  # aspas en X (S-V sin punto, W-Z con punto)
        dot, k = i >= 22, (i - 18) % 4
        cx, cy = x + S / 2, y + S / 2
        a, b = 4, S - 4
        pts = [  # arriba, izquierda, derecha, abajo
            ((x + a, y + a), (x + b, y + a)),
            ((x + a, y + a), (x + a, y + b)),
            ((x + b, y + a), (x + b, y + b)),
            ((x + a, y + b), (x + b, y + b)),
        ][k]
        (ax, ay), (bx, by) = pts
        p.append(f'<polyline points="{ax},{ay} {cx},{cy} {bx},{by}" {STROKE}/>')
    if dot:
        p.append(f'<circle cx="{x + S / 2}" cy="{y + S / 2}" r="4" fill="#111"/>')
    return "".join(p)


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>\n')


def key():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cols, cw, rh = 7, 70, 84
    body = []
    for n, ch in enumerate(letters):
        r, c = divmod(n, cols)
        x, y = 15 + c * cw, 15 + r * rh
        body.append(glyph(ch, x + 7, y))
        body.append(f'<text x="{x + 27}" y="{y + S + 26}" font-family="Arial" font-size="20" '
                    f'font-weight="bold" text-anchor="middle" fill="#111">{ch}</text>')
    rows = -(-len(letters) // cols)
    return svg(30 + cols * cw, 15 + rows * rh, "".join(body))


def message(text, per_line=12):
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) > per_line and cur:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    lines.append(cur)
    step, gap, lh = S + 8, 22, S + 26
    width = max(len(l) for l in lines) * step + 30
    body = []
    for r, line in enumerate(lines):
        x = 15
        for ch in line:
            if ch == " ":
                x += gap
                continue
            body.append(glyph(ch, x, 15 + r * lh))
            x += step
    return svg(width, 30 + len(lines) * lh - 26 + 4, "".join(body))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    (out / "clave-simbolos-alienigenas.svg").write_text(key(), encoding="utf-8")
    (out / "mensaje-alienigena.svg").write_text(
        message("LA LLAVE ESTA EN EL LIBRO DE CODIGOS"), encoding="utf-8")
    print("ok")
