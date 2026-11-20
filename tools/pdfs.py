"""Genera los PDF descargables de los juegos del blog (uno por juego) con Edge sin ventana.

Uso: python tools/pdfs.py   (desde la raíz del repo) -> static/pdf/*.pdf
Cada PDF: portada con instrucciones, una hoja A4 por imprimible, tarjetas/cartas,
soluciones para el adulto y una última página con más juegos y los libros.
"""
import html
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "static" / "images"
OUT = ROOT / "static" / "pdf"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 14mm; }
* { box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; color: #1b1b1b; margin: 0; }
.page { page-break-after: always; min-height: 262mm; position: relative; }
.page:last-child { page-break-after: auto; }
h1 { color: #c62828; font-size: 30pt; margin: 0 0 6mm; text-align: center; }
h2 { color: #c62828; font-size: 18pt; margin: 0 0 4mm; }
p, li { font-size: 12.5pt; line-height: 1.45; }
.sub { text-align: center; font-size: 14pt; margin-bottom: 8mm; }
.box { border: 2px solid #c62828; border-radius: 4mm; padding: 5mm 7mm; margin: 5mm 0; }
.sheet { display: flex; align-items: center; justify-content: center; min-height: 250mm; }
.sheet img { width: 100%; height: auto; max-height: 250mm; object-fit: contain; }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.card { border: 2.5px dashed #c62828; border-radius: 4mm; padding: 6mm; font-size: 14pt; min-height: 55mm; }
.card b { color: #c62828; }
.letter { border: 3px double #c62828; border-radius: 4mm; padding: 10mm 12mm; font-size: 15pt; line-height: 1.6; margin-top: 8mm; }
table { border-collapse: collapse; width: 100%; font-size: 11.5pt; }
td, th { border: 1px solid #bbb; padding: 2.2mm 3mm; text-align: left; vertical-align: top; }
th { background: #fbe9e7; }
.foot { position: absolute; bottom: 0; left: 0; right: 0; text-align: center; font-size: 9.5pt; color: #777; }
.web { color: #c62828; font-weight: bold; }
"""

FOOT = '<div class="foot">Gratis para uso personal y en el aula · Más juegos en <span class="web">cluemasters.es</span></div>'


def page(inner, foot=True):
    return f'<div class="page">{inner}{FOOT if foot else ""}</div>'


def sheet(rel):
    return page(f'<div class="sheet"><img src="{(IMG / rel).as_uri()}"></div>')


def cover(title, sub, ficha, pasos):
    rows = "".join(f"<li>{p}</li>" for p in pasos)
    f = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in ficha)
    return page(f'<h1>{title}</h1><div class="sub">{sub}</div><table>{f}</table>'
                f'<div class="box"><h2>Cómo prepararlo</h2><ol>{rows}</ol></div>'
                '<p>Imprime solo las páginas que necesites. Las soluciones están al final: ¡que no las vean los jugadores!</p>')


def solutions(rows, extra=""):
    r = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return page(f'<h2>Soluciones (solo para adultos)</h2><table><tr><th>Prueba</th><th>Solución</th></tr>{r}</table>{extra}')


def more(kids=True):
    books = ("<li><b>El Laboratorio de Navidad</b>: calendario de Adviento con 24 experimentos de ciencia fáciles, "
             "misiones secretas con QR y dibujos para colorear (6–10 años).</li>"
             "<li><b>Navidad</b> e <b>Invierno Mágico</b>: libros para colorear con 30 dibujos navideños (4–8 años).</li>")
    games = ("<li>Escape room de Navidad para niños (6–10 años)</li>"
             "<li>Escape room para niños de 8 a 10 años: el robo del diamante azul</li>"
             "<li>Calendario de Adviento casero con 24 retos de detective</li>"
             "<li>Escape room en casa por menos de 20 € (adolescentes y adultos)</li>")
    return page('<h2>¿Os ha gustado?</h2>'
                '<p>Tienes más juegos gratis para imprimir en <span class="web">cluemasters.es</span>:</p>'
                f'<ul>{games}</ul>'
                + ('<h2 style="margin-top:10mm">Libros de Little Crayon Studio</h2>'
                   '<p>Búscalos en Amazon por su título o desde <span class="web">cluemasters.es/enlaces</span>:</p>'
                   f'<ul>{books}</ul>' if kids else "")
                + '<div class="box" style="margin-top:12mm"><b>¿Cuántos minutos habéis tardado?</b> '
                  'Cuéntanoslo en Instagram: <span class="web">@cluemasters.es</span></div>')


def navidad():
    cards = (
        '<div class="card"><b>PISTA DEL CALCETÍN</b><br>Junto a la chimenea hay huellas de <b>BOTAS</b>. '
        'El ladrón llevaba botas.<br><br>Número secreto: <b>2</b><br><br>Ahora resolved el laberinto.</div>'
        '<div class="card"><b>PISTA DEL ÁRBOL</b><br>El abuelo Paco se fue a dormir a las diez y '
        '<b>roncó toda la noche</b>. ¡Lo oyó toda la casa!<br><br>Número secreto: <b>4</b><br><br>Leed la hoja con un espejo.</div>')
    letter = ('<div class="letter">🎅 <b>Queridos detectives:</b><br><br>¡Me habéis pillado! Fui yo quien se comió las '
              'galletas. Estaban riquísimas, y Rudolph se llevó la zanahoria para el camino.<br><br>Gracias por cuidar tan '
              'bien de la Navidad. Sois los mejores detectives del Polo Norte… y de fuera de él.<br><br>'
              '<i>Con cariño, Papá Noel</i></div>')
    return "escape-room-navidad-ninos", [
        cover("¿Quién se ha comido las galletas de Papá Noel?", "Escape room de Navidad para niños de 6 a 10 años",
              [("Jugadores", "1 a 5 niños + un adulto"), ("Duración", "30–45 minutos"), ("Código final", "en las soluciones")],
              ["Imprime el cuaderno de detective (uno por niño), el mensaje de los elfos, el laberinto y el mensaje en espejo.",
               "Recorta las dos tarjetas de pistas. Mete la del calcetín y el laberinto en un calcetín navideño.",
               "Deja la tarjeta del árbol y el mensaje en espejo debajo del árbol de Navidad.",
               "Mete la carta de Papá Noel y unas chocolatinas en una caja con candado de 3 cifras (código 2-4-1).",
               "Dales el cuaderno y el mensaje de los elfos, y lee: «Alguien se ha comido las galletas de Papá Noel…»"]),
        sheet("escape-navidad/0-cuaderno-detective.svg"),
        sheet("escape-navidad/1-mensaje-elfos.svg"),
        sheet("escape-navidad/2-laberinto.svg"),
        sheet("escape-navidad/3-mensaje-espejo.svg"),
        page(f'<h2>Tarjetas de pistas (recortar)</h2><div class="cards">{cards}</div>{letter}'),
        solutions([("1. Mensaje de los elfos", "BUSCAD EN EL CALCETÍN"),
                   ("2. Calcetín", "Fuera Bigotes y Toby (no llevan botas). Número 2"),
                   ("3. Árbol", "Fuera el abuelo Paco. Número 4"),
                   ("4. Espejo", "LUCÍA LLEVABA ZAPATILLAS DE CASA. EL NÚMERO SECRETO ES 1 → fuera Lucía"),
                   ("Culpable y código", "Papá Noel · candado 2-4-1")]),
        more(),
    ]


def museo():
    diploma = ('<div class="letter" style="text-align:center"><b style="font-size:24pt;color:#1e4f9c">DIPLOMA</b><br>'
               'de <b>Agente Especial del Museo</b><br><br>Concedido a ______________________<br><br>'
               'por recuperar el diamante azul en ____ minutos.<br><br><i>Dirección del Museo de Historia</i></div>')
    return "escape-room-ninos-8-10-anos", [
        cover("El robo del diamante azul", "Escape room para niños de 8 a 10 años",
              [("Jugadores", "2 a 6 niños"), ("Duración", "40–60 minutos"), ("Código final", "en las soluciones")],
              ["Imprime las cuatro hojas: mensaje César, sopa de letras, sudoku y sospechosos.",
               "Mete la sopa, el sudoku y los sospechosos en un sobre y escóndelo debajo del sofá.",
               "En una caja con candado de 3 cifras (código 7-3-5) mete el «diamante» y el premio.",
               "Dales el mensaje César y lee la historia del robo del diamante."]),
        sheet("escape-museo/1-mensaje-cesar.svg"),
        sheet("escape-museo/2-sopa-de-letras.svg"),
        sheet("escape-museo/3-sudoku.svg"),
        sheet("escape-museo/4-sospechosos.svg"),
        solutions([("1. Cifrado César", "MIRAD DEBAJO DEL SOFÁ"),
                   ("2. Sopa de letras", "EL PRIMER NÚMERO DEL CANDADO ES SIETE → 7"),
                   ("3. Sudoku", "Fila 3: 2 1 4 3 → la estrella es 3"),
                   ("4. Sospechosos", "Sin gafas y con gorra: Ruiz y Pardo. Bajito: Sr. Pardo → 5"),
                   ("Código final", "7-3-5")], diploma),
        more(),
    ]


def adviento():
    letters = "FELIZNAVIDADDETECTIVES"
    sol = ["El peine", "—", "NAVIDAD", "—", "La escalera", "DAME UN ABRAZO", "Lo comprobáis juntos",
           "Merry Christmas, Joyeux Noël…", "El reloj", "—", "—", "6", "—", "REGALOS", "—",
           "Ninguna huella es igual", "—", "La nube", "El mensaje que escribas", "RENO", "—", "—"]
    rows = [(f"Día {i + 1}", f"{sol[i]} · letra <b>{letters[i]}</b>") for i in range(22)]
    rows += [("Día 23", "FELIZ NAVIDAD DETECTIVES"), ("Día 24", "Sorpresa debajo del árbol")]
    return "calendario-adviento-retos-detective", [
        cover("Calendario de Adviento del detective", "24 retos para niños de 6 a 10 años",
              [("Duración", "5–15 minutos al día"), ("Necesitas", "24 sobres, bolsitas o rollos de cartón")],
              ["Imprime las dos hojas de tarjetas y recórtalas por la línea de puntos.",
               "Mete cada tarjeta en su sobre o casilla, del 1 al 24.",
               "Cuando el niño complete el reto del día, dale su letra secreta (lista al final).",
               "Día 19: la noche antes, escribe un mensaje con zumo de limón; un adulto lo revela con calor.",
               "Día 24: deja una sorpresa o una carta debajo del árbol."]),
        sheet("adviento/retos-dias-1-12.svg"),
        sheet("adviento/retos-dias-13-24.svg"),
        solutions(rows),
        more(),
    ]


def adultos():
    informe = ('<h2>INFORME DEL MINISTERIO INTERGALÁCTICO · TOP SECRET</h2><table>'
               '<tr><th>Sistema</th><th>Frecuencia</th><th>Estado</th></tr>'
               '<tr><td>Núcleo de energía</td><td>2 pulsos/s</td><td>Estable</td></tr>'
               '<tr><td>Antena principal</td><td>7 pulsos/s</td><td>Emitiendo</td></tr>'
               '<tr><td>Refrigeración</td><td>4 pulsos/s</td><td>Estable</td></tr>'
               '<tr><td>Escudo térmico</td><td>9 pulsos/s</td><td>Estable</td></tr>'
               '<tr><td>Fusible de respaldo</td><td>7 pulsos/s</td><td>⚠ Revisar</td></tr></table>'
               '<p><i>Dos sistemas nunca comparten frecuencia. Si ocurre, el problema está en el <b>FUSIBLE DEFECTUOSO</b>.</i></p>')
    victoria = ('<div class="letter">📡 <b>TRANSMISIÓN CANCELADA</b><br><br>¡Enhorabuena, agentes de Clue Street 13!<br><br>'
                'Habéis evitado que la señal alienígena llegue a su destino. La humanidad os debe una.<br><br>'
                '<i>Firmado: Centro de Control de Invasiones Domésticas</i></div>')
    circuito = ('<div class="box"><h2>Prueba 3: el circuito (dibújalo tú)</h2><p>En un folio, dibuja un <b>Núcleo</b> a la '
                'izquierda y una <b>Antena</b> a la derecha unidos por 4–5 cables de colores que se cruzan. Solo el '
                '<b>verde</b> llega a la antena. Leyenda: rojo = 2, azul = 8, amarillo = 1, <b>verde = 5</b>. '
                'Mételo en un sobre con la etiqueta «Fusible de respaldo».</p></div>')
    return "escape-room-invasion-clue-street-13", [
        cover("Invasión en Clue Street 13", "Escape room en casa para adolescentes y adultos",
              [("Jugadores", "2 a 5"), ("Duración", "45–60 minutos"), ("Código final", "en las soluciones")],
              ["Imprime el mensaje alienígena y la clave de símbolos. Esconde la clave en el salón.",
               "Pon un libro con la etiqueta «Libro de códigos»: dentro, una llave USB con un 3 y el informe.",
               "Dibuja el circuito (instrucciones abajo) y mételo en el sobre «Fusible de respaldo».",
               "Cierra una caja con candado de 3 cifras (código 3-7-5) con el «transmisor» y la carta de victoria."]),
        sheet("escape-20/mensaje-alienigena.svg"),
        sheet("escape-20/clave-simbolos-alienigenas.svg"),
        page(informe + circuito + victoria),
        solutions([("1. Mensaje alienígena", "LA LLAVE ESTÁ EN EL LIBRO DE CÓDIGOS → USB con el 3"),
                   ("2. Informe", "El 7 se repite → FUSIBLE DEFECTUOSO → 7"),
                   ("3. Circuito", "Llega el cable verde → 5"),
                   ("Código final", "3-7-5")]),
        more(kids=False),
    ]


def build(name, pages):
    OUT.mkdir(parents=True, exist_ok=True)
    doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / f"{name}.html"
        src.write_text(doc, encoding="utf-8")
        out = OUT / f"{name}.pdf"
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", src.as_uri()], check=True, capture_output=True, timeout=120)
    print("ok", out.name, out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    for fn in (navidad, museo, adviento, adultos):
        build(*fn())
