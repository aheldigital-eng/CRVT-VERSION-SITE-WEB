import re
from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
original = s

# Repair the malformed style nesting from the previous header/PWA patch.
s, n1 = re.subn(
    r'(</style>\s*\n\s*)<style id="crvt-v19-max-design">',
    r'\1</style>\n<style id="crvt-v19-max-design">',
    s,
    count=1,
)
s, n2 = re.subn(r'</style>\s*</style>\s*</head>', '</style>\n</head>', s, count=1)

# Keep the tableau photo system but remove references to the deleted
# "Place disponible dans le tableau ?" question.
s = s.replace(
    'audit.data.commentaire||audit.data.place||audit.data.puissance||audit.data.compteur||audit.data.borne||audit.data.environnement||audit.data.position||audit.data.longueurCable||audit.data.typeCable||audit.data.cableCommunication',
    'audit.data.commentaire||audit.data.puissance||audit.data.compteur||audit.data.borne||audit.data.environnement||audit.data.position||audit.data.longueurCable||audit.data.typeCable||audit.data.cableCommunication',
)
s = s.replace(
    'if(key==="tableau") return !audit.sections.tableau?"warn":(audit.data.place && photoCount("tableau")?"ok":"warn");',
    'if(key==="tableau") return !audit.sections.tableau?"warn":(photoCount("tableau")?"ok":"warn");',
)
s = s.replace(
    'if(["place","passage","protection"].includes(e.dataset.field)) renderFollowups();',
    'if(["passage","protection"].includes(e.dataset.field)) renderFollowups();',
)

# Remove obsolete validation warnings/targets for the deleted question.
s = re.sub(
    r'\n\s*if\(audit\.sections\.tableau\)\{\s*if\(audit\.data\.place\) add\("warning","Tableau électrique : décision manquante".*?\n\s*\}',
    '', s, count=1, flags=re.S,
)
s = re.sub(
    r'\n\s*if\(t\.includes\(\'tableau électrique : décision\'\)\) return \{selector:\'\[data-field="place"\]\};',
    '', s, count=1,
)
s = re.sub(
    r'\n\s*if\(t\.includes\(\'tableau électrique : aucune photo\'\)\) return \{selector:\'#tableauFollow\'\};',
    '', s, count=1,
)
s = s.replace(' let place=audit.data.place||"";\n', '')

# Safety checks: never publish if the working tableau photo system disappeared.
if 'photos("tableau")' not in s:
    raise SystemExit('SAFETY STOP: tableau photo system disappeared')
if 'Photo du tableau' not in s:
    raise SystemExit('SAFETY STOP: tableau photo card disappeared')
if 'Place disponible dans le tableau ?' in s:
    raise SystemExit('SAFETY STOP: obsolete place question remains')
if 'Prévoir un tableau supplémentaire' in s:
    raise SystemExit('SAFETY STOP: obsolete warning remains')
if 'PLACE DISPONIBLE DANS LE TABLEAU' in s:
    raise SystemExit('SAFETY STOP: obsolete PDF block remains')

if s == original:
    print('NO CHANGES NEEDED')
else:
    p.write_text(s, encoding='utf-8')
    print(f'OK style_open={n1} extra_style={n2} bytes={len(s)}')
