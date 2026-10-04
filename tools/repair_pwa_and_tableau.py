import re
from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Repair malformed style nesting without changing validated UI sections.
s = s.replace('</style>\n</style>\n<style>\n/* V20 — outils pro terrain */', '</style>\n<style>\n/* V20 — outils pro terrain */', 1)
s = s.replace('</style>\r\n</style>\r\n<style>\r\n/* V20 — outils pro terrain */', '</style>\r\n<style>\r\n/* V20 — outils pro terrain */', 1)
s = re.sub(r'</style>\s*</style>\s*</head>', '</style>\n</head>', s, count=1)

# Normalize the Informations fields exactly once.
common = '''const common=[
["puissance","Puissance souscrite","select:3 kVA|6 kVA|9 kVA|12 kVA|15 kVA|18 kVA|24 kVA|36 kVA|Autre"],["compteur","Type de Compteur","select:Monophasé|Triphasé|Autre"],
["divisionnaire","Installation d’un tableau divisionnaire","select:Oui|Non"],["typeborne","Type de borne","select:Monophasé|Triphasé|Autre"],
["environnement","Environnement Borne","select:Extérieur|Intérieur|Autre"],["position","Positionnement de Borne","select:Sur mur|Sur pied|Autre"],
["distance","Distance (m)","text"],["typeCable","Type de câble","select:3G10|5G10"],["cablecom","Câble de communication","select:Oui|Non"]
];'''
s, n = re.subn(r'const common=\[.*?\];', common, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Impossible de normaliser const common')

p.write_text(s, encoding='utf-8')
print(f'OK normalized common fields and repaired styles; bytes={len(s)}')
