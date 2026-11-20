"""Sugerencias de autocompletado de Google (España) para ideas de búsquedas.

Uso: python -I tools/sugerencias.py "semilla 1" "semilla 2" ...
"""
import json, sys, time, urllib.parse, urllib.request

for seed in sys.argv[1:]:
    found = []
    for suffix in ["", " para", " de", " gratis", " niños"]:
        q = seed + suffix
        url = "https://suggestqueries.google.com/complete/search?client=firefox&hl=es&gl=es&q=" + urllib.parse.quote(q)
        try:
            data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode("latin-1"))
            found += [t for t in data[1] if t not in found]
        except Exception as e:
            print("ERR", q, e, file=sys.stderr)
        time.sleep(0.3)
    print(f"## {seed}: " + " | ".join(found))
