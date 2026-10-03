import re
from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Remove ONLY the obsolete "Place disponible dans le tableau ?" field.
s, nq = re.subn(
    r'tableau:\[\s*\["place","Place disponible dans le tableau \?","select:Oui\|Non"\]\s*\],',
    'tableau:[],',
    s,
    count=1,
)

# 2) Remove ONLY the obsolete warning card. Do NOT touch the working tableau photo card.
warning_pat = re.compile(
    r'<div class="item"><b>⚠️ Prévoir un tableau supplémentaire</b>'
    r'<p>Ajouter une photo du tableau existant et l’annoter\.</p>'
    r'\$\{photos\("tableau"\)\}</div>',
    re.S,
)
s, nw = warning_pat.subn('', s, count=1)

# If the warning card is wrapped in the old place===Non conditional, remove only that
# conditional branch while preserving the preceding working photo branch.
branch_pat = re.compile(
    r'else if\(audit\.data\.place===(["\'])Non\1\)\{\s*'
    r't\.innerHTML=`<div class="item"><b>⚠️ Prévoir un tableau supplémentaire</b>'
    r'<p>Ajouter une photo du tableau existant et l’annoter\.</p>'
    r'\$\{photos\("tableau"\)\}</div>`;\s*\}',
    re.S,
)
s, nb = branch_pat.subn('', s, count=1)

# Remove a leftover empty else attached to the deleted availability question only.
s = re.sub(r'else\s*t\.innerHTML="";', '', s, count=1)

# 3) Remove the obsolete PDF answer/recommendation for the deleted question.
pdf_pat = re.compile(
    r'\$\{first\?`<div class="bigAnswer"><span>PLACE DISPONIBLE DANS LE TABLEAU</span>'
    r'<b>\$\{esc\(place\|\|"Non renseigné"\)\}</b></div>\s*'
    r'\$\{place==="Non"\?`<div class="recommendation"><b>TABLEAU SUPPLÉMENTAIRE À PRÉVOIR</b>.*?`:\"\"\}`:\"\"\}',
    re.S,
)
s, npdf = pdf_pat.subn('', s, count=1)

# Fallback page that existed only for the deleted question: remove the whole push block.
fallback_pat = re.compile(
    r'\n\s*if\(!blocks\.length\)\{\s*pages\.push\(`[^`]*?PLACE DISPONIBLE DANS LE TABLEAU.*?`\);\s*\}',
    re.S,
)
s, nfb = fallback_pat.subn('', s, count=1)

# 4) Safety checks. The working photo system MUST remain.
if 'photos("tableau")' not in s:
    raise SystemExit('SAFETY STOP: tableau photo system disappeared')
if 'Place disponible dans le tableau ?' in s:
    raise SystemExit('SAFETY STOP: obsolete place question remains')
if 'Prévoir un tableau supplémentaire' in s:
    raise SystemExit('SAFETY STOP: obsolete warning remains')
if 'PLACE DISPONIBLE DANS LE TABLEAU' in s:
    raise SystemExit('SAFETY STOP: obsolete PDF block remains')

# The photo card itself must still exist after cleanup.
if 'Photo du tableau' not in s:
    raise SystemExit('SAFETY STOP: tableau photo card disappeared')

p.write_text(s, encoding='utf-8')
print(f'OK nq={nq} warning={nw} branch={nb} pdf={npdf} fallback={nfb} bytes={len(s)}')
