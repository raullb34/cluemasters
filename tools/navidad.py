"""Imprimibles del escape room navideño «¿Quién se ha comido las galletas de Papá Noel?»."""
import random
import sys
from pathlib import Path

INK = "#1b1b1b"
RED = "#c0392b"
FONT = 'font-family="Arial, Helvetica, sans-serif"'


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>\n')


def text(x, y, s, size=20, weight="normal", fill=INK, anchor="middle", extra=""):
    return (f'<text x="{x}" y="{y}" {FONT} font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


def number_message(msg):
    """Mensaje en código A=1 ... Z=26: un número por letra y una raya para escribirla."""
    words, box, gap = msg.split(), 52, 26
    lines, cur = [], []
    for w in words:  # máximo ~11 casillas por línea
        if sum(len(x) for x in cur) + len(cur) + len(w) > 11 and cur:
            lines.append(cur)
            cur = []
        cur.append(w)
    lines.append(cur)
    width = 30 + max(sum(len(x) for x in l) * box + (len(l) - 1) * gap for l in lines)
    body = [text(width / 2, 38, "MENSAJE SECRETO DE LOS ELFOS", 24, "bold", RED)]
    y = 70
    for line in lines:
        x = 15
        for w in line:
            for ch in w:
                n = ord(ch) - 64
                body.append(f'<rect x="{x + 3}" y="{y}" width="{box - 6}" height="40" rx="6" '
                            f'fill="#fdf2f0" stroke="{RED}" stroke-width="2"/>')
                body.append(text(x + box / 2, y + 28, n, 22, "bold"))
                body.append(f'<line x1="{x + 8}" y1="{y + 80}" x2="{x + box - 8}" y2="{y + 80}" '
                            f'stroke="{INK}" stroke-width="2"/>')
                x += box
            x += gap
        y += 110
    key_y = y + 10
    body.append(text(width / 2, key_y, "CLAVE:  A=1  B=2  C=3 ... Z=26", 18, "bold"))
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cell = (width - 30) / 13
    for i, ch in enumerate(letters):
        r, c = divmod(i, 13)
        cx, cy = 15 + c * cell + cell / 2, key_y + 30 + r * 46
        body.append(text(cx, cy, ch, 16, "bold"))
        body.append(text(cx, cy + 18, i + 1, 14))
    return svg(width, key_y + 30 + 2 * 46, "".join(body))


def maze(cols=11, rows=11, cell=40, seed=24):
    """Laberinto perfecto (un solo camino) de las galletas al árbol."""
    random.seed(seed)
    walls = {(c, r): {"N", "S", "E", "W"} for c in range(cols) for r in range(rows)}
    moves = {"N": (0, -1, "S"), "S": (0, 1, "N"), "E": (1, 0, "W"), "W": (-1, 0, "E")}
    stack, seen = [(0, 0)], {(0, 0)}
    while stack:
        c, r = stack[-1]
        opts = [(d, c + dx, r + dy, back) for d, (dx, dy, back) in moves.items()
                if (c + dx, r + dy) in walls and (c + dx, r + dy) not in seen]
        if not opts:
            stack.pop()
            continue
        d, nc, nr, back = random.choice(opts)
        walls[(c, r)].discard(d)
        walls[(nc, nr)].discard(back)
        seen.add((nc, nr))
        stack.append((nc, nr))
    walls[(0, 0)].discard("W")
    walls[(cols - 1, rows - 1)].discard("E")
    ox, oy = 110, 70
    body = [text(ox + cols * cell / 2, 40, "¿POR DÓNDE ESCAPÓ EL LADRÓN DE GALLETAS?", 20, "bold", RED)]
    st = f'stroke="{INK}" stroke-width="4" stroke-linecap="round"'
    for (c, r), ws in walls.items():
        x, y = ox + c * cell, oy + r * cell
        if "N" in ws: body.append(f'<line x1="{x}" y1="{y}" x2="{x + cell}" y2="{y}" {st}/>')
        if "S" in ws: body.append(f'<line x1="{x}" y1="{y + cell}" x2="{x + cell}" y2="{y + cell}" {st}/>')
        if "W" in ws: body.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + cell}" {st}/>')
        if "E" in ws: body.append(f'<line x1="{x + cell}" y1="{y}" x2="{x + cell}" y2="{y + cell}" {st}/>')
    body.append(text(ox - 55, oy + 18, "GALLETAS", 14, "bold", RED))
    body.append(text(ox - 55, oy + 34, "→", 18, "bold", RED))
    ex = ox + cols * cell
    ey = oy + (rows - 1) * cell
    body.append(f'<polygon points="{ex + 55},{ey - 20} {ex + 35},{ey + 22} {ex + 75},{ey + 22}" fill="#2e7d32"/>')
    body.append(f'<rect x="{ex + 50}" y="{ey + 22}" width="10" height="10" fill="#6d4c41"/>')
    body.append(text(ex + 55, ey + 52, "?", 18, "bold", RED))
    return svg(ox * 2 + cols * cell, oy + rows * cell + 70, "".join(body))


def mirror(msg_lines):
    """Mensaje escrito al revés: se lee poniéndolo delante de un espejo."""
    w, lh = 760, 64
    h = 90 + lh * len(msg_lines)
    body = [text(w / 2, 40, "Este mensaje solo se puede leer con… ¿un espejo?", 18, "bold", RED)]
    inner = "".join(text(w / 2, 100 + i * lh, line, 38, "bold") for i, line in enumerate(msg_lines))
    body.append(f'<g transform="translate({w},0) scale(-1,1)">{inner}</g>')
    return svg(w, h, "".join(body))


def notebook(suspects):
    w, row = 760, 70
    h = 150 + row * len(suspects) + 120
    body = [text(w / 2, 46, "CUADERNO DE DETECTIVE", 30, "bold", RED),
            text(w / 2, 80, "Tacha a cada sospechoso cuando una pista demuestre que es inocente.", 16)]
    for i, (name, desc) in enumerate(suspects):
        y = 110 + i * row
        body.append(f'<rect x="40" y="{y}" width="{w - 80}" height="{row - 12}" rx="10" fill="#fff8e7" '
                    f'stroke="{INK}" stroke-width="2"/>')
        body.append(f'<rect x="58" y="{y + 15}" width="28" height="28" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        body.append(text(106, y + 28, name, 22, "bold", anchor="start"))
        body.append(text(106, y + 50, desc, 15, anchor="start"))
    y = 110 + row * len(suspects) + 30
    body.append(text(w / 2, y, "CÓDIGO DE LA CAJA FUERTE", 20, "bold", RED))
    for k in range(3):
        x = w / 2 - 105 + k * 75
        body.append(f'<rect x="{x}" y="{y + 15}" width="60" height="64" rx="8" fill="#fff" '
                    f'stroke="{RED}" stroke-width="3"/>')
    return svg(w, h, "".join(body))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "1-mensaje-elfos.svg": number_message("BUSCAD EN EL CALCETIN"),
        "2-laberinto.svg": maze(),
        "3-mensaje-espejo.svg": mirror(["LUCIA LLEVABA", "ZAPATILLAS DE CASA", "EL NUMERO SECRETO ES 1"]),
        "0-cuaderno-detective.svg": notebook([
            ("Bigotes, el gato", "Le encanta subirse a la mesa de la cocina."),
            ("Toby, el perro", "Nunca dice que no a una galleta."),
            ("El abuelo Paco", "Dice que las galletas de jengibre son sus favoritas."),
            ("La prima Lucía", "Se quedó despierta hasta muy tarde."),
            ("Papá Noel", "¿Habrá pasado ya por casa?"),
        ]),
    }
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
    print("ok", len(files))
