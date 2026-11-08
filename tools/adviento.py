"""Tarjetas imprimibles del calendario de Adviento casero «24 retos de detective».

Genera dos hojas (días 1-12 y 13-24) con 12 tarjetas cada una, listas para recortar.
"""
import sys
from pathlib import Path

INK, RED, GREEN = "#1b1b1b", "#c0392b", "#2e7d32"
FONT = 'font-family="Arial, Helvetica, sans-serif"'

# (texto del reto en líneas cortas, texto en espejo opcional)
RETOS = [
    (["Adivinanza:", "Tengo dientes", "pero no muerdo.", "¿Qué soy?"], None),
    (["Encuentra 5 cosas", "ROJAS en casa", "en menos de", "2 minutos."], None),
    (["Descifra el código", "(A=1, B=2...):", "14-1-22-9-4-1-4"], None),
    (["Dibuja un muñeco", "de nieve con los", "ojos cerrados."], None),
    (["Adivinanza:", "Subo y bajo", "sin moverme.", "¿Qué soy?"], None),
    (["Lee este mensaje", "con un espejo:"], "DAME UN ABRAZO"),
    (["Cuenta las bolas", "del árbol de", "Navidad. ¡Sin", "equivocarte!"], None),
    (["Aprende a decir", "«Feliz Navidad»", "en 3 idiomas."], None),
    (["Adivinanza:", "Tengo agujas pero", "no sé coser. ¿Qué", "soy?"], None),
    (["Un adulto esconde", "un calcetín.", "Encuéntralo con", "«frío o caliente»."], None),
    (["Haz una tarjeta", "de Navidad para", "alguien de tu", "familia."], None),
    (["Papá Noel tiene", "9 renos y 3 se", "van a dormir.", "¿Cuántos tiran?"], None),
    (["Con los ojos tapados,", "llega del sofá", "al árbol solo con", "las indicaciones."], None),
    (["Lee al revés:", "S O L A G E R"], None),
    (["Mira 10 objetos", "30 segundos. Un", "adulto quita uno.", "¿Cuál falta?"], None),
    (["Toma tus huellas", "con lápiz y celo.", "¿Son iguales", "que las de papá?"], None),
    (["Canta un", "villancico entero", "sin equivocarte."], None),
    (["Adivinanza:", "Vuelo sin alas,", "lloro sin ojos.", "¿Qué soy?"], None),
    (["Revela el mensaje", "invisible con", "ayuda de un adulto", "(¡zumo de limón!)."], None),
    (["Ordena las letras", "y descubre el", "animal navideño:", "R O N E"], None),
    (["Adivina el personaje", "navideño que piensa", "un adulto con", "preguntas de sí/no."], None),
    (["Haz una cadena", "de papel para", "decorar tu", "habitación."], None),
    (["Junta todas tus", "letras secretas en", "orden. ¿Qué", "mensaje forman?"], None),
    (["¡NOCHEBUENA!", "Última pista:", "busca debajo", "del árbol."], None),
]


def card(day, lines, mirror, x, y, w, h):
    p = [f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" rx="14" fill="#fffaf2" '
         f'stroke="{RED}" stroke-width="3" stroke-dasharray="10 6"/>']
    p.append(f'<circle cx="{x + w / 2}" cy="{y + 52}" r="32" fill="{RED}"/>')
    p.append(f'<text x="{x + w / 2}" y="{y + 64}" {FONT} font-size="34" font-weight="bold" '
             f'fill="#fff" text-anchor="middle">{day}</text>')
    ty = y + 112
    for i, line in enumerate(lines):
        weight = "bold" if i == 0 and line.endswith(":") else "normal"
        p.append(f'<text x="{x + w / 2}" y="{ty}" {FONT} font-size="17" font-weight="{weight}" '
                 f'fill="{INK}" text-anchor="middle">{line}</text>')
        ty += 23
    if mirror:
        cx = x + w / 2
        p.append(f'<g transform="translate({2 * cx},0) scale(-1,1)"><text x="{cx}" y="{ty + 8}" {FONT} '
                 f'font-size="20" font-weight="bold" fill="{GREEN}" text-anchor="middle">{mirror}</text></g>')
    if day <= 22:
        p.append(f'<text x="{x + w / 2}" y="{y + h - 26}" {FONT} font-size="15" fill="{GREEN}" '
                 f'font-weight="bold" text-anchor="middle">Letra secreta: ____</text>')
    return "".join(p)


def sheet(first):
    cols, rows, w, h = 3, 4, 260, 270
    W, H = cols * w + 20, rows * h + 70
    body = [f'<text x="{W / 2}" y="40" {FONT} font-size="24" font-weight="bold" fill="{RED}" '
            f'text-anchor="middle">CALENDARIO DE ADVIENTO DEL DETECTIVE · DÍAS {first}-{first + 11}</text>']
    for k in range(12):
        r, c = divmod(k, cols)
        day = first + k
        lines, mirror = RETOS[day - 1]
        body.append(card(day, lines, mirror, 10 + c * w, 55 + r * h, w, h))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="#fff"/>{"".join(body)}</svg>\n')


if __name__ == "__main__":
    assert len(RETOS) == 24
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "retos-dias-1-12.svg").write_text(sheet(1), encoding="utf-8")
    (out / "retos-dias-13-24.svg").write_text(sheet(13), encoding="utf-8")
    print("ok")
