"""Imprimibles del escape room «El robo del diamante azul» (8-10 años).

Genera: mensaje en cifrado César, sopa de letras con mensaje oculto, sudoku 4x4 y fichas
de sospechosos. Código final del candado: 7-3-5.
"""
import itertools
import random
import sys
from pathlib import Path

INK, BLUE, GOLD = "#1b1b1b", "#1e4f9c", "#e0a800"
FONT = 'font-family="Arial, Helvetica, sans-serif"'


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>\n')


def t(x, y, s, size=20, weight="normal", fill=INK, anchor="middle"):
    return f'<text x="{x}" y="{y}" {FONT} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def cesar(msg, shift=3):
    enc = "".join(ABC[(ABC.index(c) + shift) % 26] if c in ABC else c for c in msg)
    W = 800
    body = [t(W / 2, 46, "MENSAJE INTERCEPTADO AL LADRÓN", 28, "bold", BLUE)]
    words, lines, cur = enc.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 14 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    y = 100
    for line in lines:
        x = W / 2 - len(line) * 26
        for ch in line:
            if ch != " ":
                body.append(f'<rect x="{x}" y="{y}" width="46" height="50" rx="6" fill="#eef3fb" stroke="{BLUE}" stroke-width="2"/>')
                body.append(t(x + 23, y + 36, ch, 30, "bold"))
                body.append(f'<line x1="{x + 6}" y1="{y + 92}" x2="{x + 40}" y2="{y + 92}" stroke="{INK}" stroke-width="2"/>')
            x += 52
        y += 120
    body.append(t(W / 2, y + 10, "PISTA: cada letra se ha movido 3 puestos hacia delante (A → D).", 19, "bold"))
    body.append(t(W / 2, y + 36, "Para descifrar, muévela 3 puestos hacia atrás.", 19))
    cell = (W - 40) / 26
    for i, ch in enumerate(ABC):
        x = 20 + i * cell + cell / 2
        body.append(t(x, y + 80, ch, 18, "bold"))
    return svg(W, int(y + 100), "".join(body)), enc


def sopa(words, message, n=8, seed=7):
    rnd = random.Random(seed)
    dirs = [(0, 1), (1, 0), (1, 1)]
    while True:
        grid = [[None] * n for _ in range(n)]
        ok = True
        for w in sorted(words, key=len, reverse=True):
            placed = False
            for _ in range(400):
                dr, dc = rnd.choice(dirs)
                r = rnd.randrange(n - dr * (len(w) - 1))
                c = rnd.randrange(n - dc * (len(w) - 1))
                cells = [(r + dr * k, c + dc * k) for k in range(len(w))]
                if all(grid[a][b] in (None, w[k]) for k, (a, b) in enumerate(cells)):
                    for k, (a, b) in enumerate(cells):
                        grid[a][b] = w[k]
                    placed = True
                    break
            if not placed:
                ok = False
                break
        free = [(a, b) for a in range(n) for b in range(n) if grid[a][b] is None]
        if ok and len(free) == len(message):
            break
    for (a, b), ch in zip(free, message):
        grid[a][b] = ch
    for a, b in free[len(message):]:
        grid[a][b] = "★"
    S = 62
    W = n * S + 300
    H = n * S + 140
    body = [t(W / 2, 44, "SOPA DE LETRAS DEL MUSEO", 28, "bold", BLUE)]
    for a in range(n):
        for b in range(n):
            x, y = 30 + b * S, 70 + a * S
            body.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="#fff" stroke="#9fb3d1" stroke-width="1.5"/>')
            body.append(t(x + S / 2, y + 42, grid[a][b], 30, "bold", GOLD if grid[a][b] == "★" else INK))
    lx = 30 + n * S + 30
    body.append(t(lx, 100, "BUSCA:", 22, "bold", BLUE, "start"))
    for i, w in enumerate(words):
        body.append(t(lx, 140 + i * 36, f"□ {w}", 22, "normal", INK, "start"))
    body.append(t(W / 2, 70 + n * S + 40, "Después, lee en orden las letras que sobran: esconden un mensaje.", 19, "bold"))
    return svg(W, H, "".join(body)), len(free)


def sudoku():
    sol = [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]
    given = {(0, 0), (0, 3), (1, 1), (1, 2), (2, 0), (2, 1), (3, 2), (3, 3)}
    target = (2, 3)  # casilla marcada: su número es el segundo del candado (3)

    def valid(g):
        for i in range(4):
            if sorted(g[i]) != [1, 2, 3, 4] or sorted(g[r][i] for r in range(4)) != [1, 2, 3, 4]:
                return False
        for br, bc in itertools.product((0, 2), (0, 2)):
            if sorted(g[br + a][bc + b] for a in (0, 1) for b in (0, 1)) != [1, 2, 3, 4]:
                return False
        return True

    empties = [(r, c) for r in range(4) for c in range(4) if (r, c) not in given]
    count = 0
    for perm in itertools.product(range(1, 5), repeat=len(empties)):
        g = [[sol[r][c] if (r, c) in given else 0 for c in range(4)] for r in range(4)]
        for (r, c), v in zip(empties, perm):
            g[r][c] = v
        if valid(g):
            count += 1
    assert count == 1, f"el sudoku tiene {count} soluciones"
    S = 110
    W, H = 4 * S + 80, 4 * S + 190
    body = [t(W / 2, 44, "SUDOKU DE LA CAJA FUERTE", 26, "bold", BLUE),
            t(W / 2, 74, "Cada fila, columna y cuadrado: 1, 2, 3 y 4", 17)]
    ox, oy = 40, 100
    for r in range(4):
        for c in range(4):
            x, y = ox + c * S, oy + r * S
            fill = "#fff6d6" if (r, c) == target else "#fff"
            body.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{fill}" stroke="#9fb3d1" stroke-width="2"/>')
            if (r, c) in given:
                body.append(t(x + S / 2, y + 72, sol[r][c], 56, "bold"))
            if (r, c) == target:
                body.append(t(x + S - 16, y + 26, "★", 24, "bold", GOLD))
    for k in (0, 2, 4):
        body.append(f'<line x1="{ox}" y1="{oy + k * S}" x2="{ox + 4 * S}" y2="{oy + k * S}" stroke="{INK}" stroke-width="5"/>')
        body.append(f'<line x1="{ox + k * S}" y1="{oy}" x2="{ox + k * S}" y2="{oy + 4 * S}" stroke="{INK}" stroke-width="5"/>')
    body.append(t(W / 2, oy + 4 * S + 50, "El número de la casilla ★ es el", 20, "bold"))
    body.append(t(W / 2, oy + 4 * S + 76, "SEGUNDO número del candado.", 20, "bold"))
    return svg(W, H, "".join(body))


def sospechosos():
    people = [
        ("1", "Sr. Gómez", ["Lleva gafas", "Lleva sombrero", "Es alto"]),
        ("4", "Sra. Ruiz", ["No lleva gafas", "Lleva gorra", "Es alta"]),
        ("5", "Sr. Pardo", ["No lleva gafas", "Lleva gorra", "Es bajito"]),
        ("8", "Srta. Vela", ["Lleva gafas", "Lleva gorra", "Es bajita"]),
    ]
    W, cw, ch = 820, 380, 230
    body = [t(W / 2, 46, "FICHAS DE LOS SOSPECHOSOS", 28, "bold", BLUE)]
    for i, (num, name, traits) in enumerate(people):
        r, c = divmod(i, 2)
        x, y = 20 + c * (cw + 20), 70 + r * (ch + 20)
        body.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="#f7f9fc" stroke="{BLUE}" stroke-width="3"/>')
        body.append(f'<circle cx="{x + 52}" cy="{y + 52}" r="34" fill="{GOLD}"/>')
        body.append(t(x + 52, y + 64, num, 34, "bold"))
        body.append(t(x + 104, y + 62, name, 30, "bold", INK, "start"))
        for k, tr in enumerate(traits):
            body.append(t(x + 40, y + 125 + k * 34, "• " + tr, 22, "normal", INK, "start"))
    y = 70 + 2 * (ch + 20) + 20
    body.append(t(W / 2, y, "LO QUE VIO EL VIGILANTE:", 22, "bold", BLUE))
    for k, s in enumerate(["El ladrón NO llevaba gafas.", "Llevaba GORRA.", "Era más BAJITO que el vigilante (que mide poco)."]):
        body.append(t(W / 2, y + 36 + k * 30, s, 21, "normal"))
    body.append(t(W / 2, y + 140, "El número del culpable es el TERCER número del candado.", 20, "bold"))
    return svg(W, int(y + 170), "".join(body))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    c, enc = cesar("MIRAD DEBAJO DEL SOFA")
    (out / "1-mensaje-cesar.svg").write_text(c, encoding="utf-8")
    message = "ELPRIMERNUMERODELCANDADOESSIETE"
    s, free = sopa(["MUSEO", "DIAMANTE", "LADRON", "PISTA", "LUPA", "AGENTE"], message)
    (out / "2-sopa-de-letras.svg").write_text(s, encoding="utf-8")
    (out / "3-sudoku.svg").write_text(sudoku(), encoding="utf-8")
    (out / "4-sospechosos.svg").write_text(sospechosos(), encoding="utf-8")
    print("ok; cifrado:", enc, "| casillas libres en la sopa:", free, "para", len(message), "letras")
