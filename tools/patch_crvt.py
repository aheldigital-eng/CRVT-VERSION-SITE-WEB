import re
from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Keep the existing technical information fields.
old = '["environnement","Environnement Borne","select:Extérieur|Intérieur|Autre"],["position","Positionnement de Borne","select:Sur mur|Sur pied|Autre"]'
new = '["environnement","Environnement Borne","select:Extérieur|Intérieur|Autre"],["position","Positionnement de Borne","select:Sur mur|Sur pied|Autre"],["longueurCable","Mesure du cheminement (m)","number"],["typeCable","Type de câble","select:3G10|5G10"],["cableCommunication","Câble de communication","select:Oui|Non"]'
if old in s:
    s = s.replace(old, new, 1)

# 2) Keep the technical information labels used by the PDF.
old = 'position:"Positionnement de la borne"\n};'
new = 'position:"Positionnement de la borne",\nlongueurCable:"Mesure du cheminement (m)",\ntypeCable:"Type de câble",\ncableCommunication:"Câble de communication"\n};'
if old in s:
    s = s.replace(old, new, 1)

# 3) Keep the Informations tab aware of the existing fields.
old = 'if(key==="infos") return audit.data.commentaire||audit.data.place||audit.data.puissance||audit.data.compteur||audit.data.borne||audit.data.environnement||audit.data.position?"ok":"warn";'
new = 'if(key==="infos") return audit.data.commentaire||audit.data.place||audit.data.puissance||audit.data.compteur||audit.data.borne||audit.data.environnement||audit.data.position||audit.data.longueurCable||audit.data.typeCable||audit.data.cableCommunication?"ok":"warn";'
if old in s:
    s = s.replace(old, new, 1)

# 4) Remove the old embedded cable-fields patch if it is still present.
start = s.find('<!-- CRVT V7+ cable fields patch -->')
if start != -1:
    end = s.find('</body></html>`;', start)
    if end == -1:
        raise SystemExit('obsolete embedded patch found but its end was not found')
    s = s[:start] + s[end:]

# 5) Remove ONLY the obsolete "Place disponible dans le tableau ?" field.
s = re.sub(
    r'tableau:\[\s*\["place","Place disponible dans le tableau \?","select:Oui\|Non"\]\s*\],',
    'tableau:[],',
    s,
    count=1,
)

# 6) Keep the annotation toolbar on two compact rows on phones.
old = '.crvtAnnotTools{flex:0 0 auto;display:flex;gap:8px;align-items:center;overflow-x:auto;overflow-y:hidden;padding:9px;background:#fff;border-bottom:1px solid #dbe5ec;box-shadow:0 3px 12px #0002;-webkit-overflow-scrolling:touch}'
new = '.crvtAnnotTools{flex:0 0 auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;align-items:stretch;padding:9px;background:#fff;border-bottom:1px solid #dbe5ec;box-shadow:0 3px 12px #0002}.crvtAnnotTools .crvtAT,.crvtAnnotTools .crvtASelect{width:100%;min-width:0}'
if old in s:
    s = s.replace(old, new, 1)

# 7) Compact annotation buttons on phones without changing their handlers.
old = '@media(max-width:620px){.crvtAnnotHead>div{font-size:16px}.crvtAnnotFoot{align-items:stretch}.crvtAnnotFoot span{display:none}.crvtAnnotFoot>div{width:100%;display:flex}.crvtCancel,.crvtSave{flex:1}.crvtAT,.crvtASelect{font-size:13px;padding:8px 10px}}'
new = '@media(max-width:620px){.crvtAnnotHead>div{font-size:16px}.crvtAnnotTools{grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;padding:7px}.crvtAT,.crvtASelect{font-size:12px;padding:8px 4px;min-height:42px;border-radius:10px}.crvtAnnotFoot{align-items:stretch}.crvtAnnotFoot span{display:none}.crvtAnnotFoot>div{width:100%;display:flex}.crvtCancel,.crvtSave{flex:1}}'
if old in s:
    s = s.replace(old, new, 1)

# 8) CRITICAL: remove only the warning text/block, but ALWAYS keep the existing
# tableau photo + annotation controls. This fixes the regression where photos vanished.
pattern = re.compile(
    r'if\(audit\.data\.place===\\"Oui\\"\)\{\s*'
    r't\.innerHTML=`<div class=\\"item\\"><b>📷 Photo du tableau</b><p>Prendre une photo puis l’annoter\.</p>\$\{photos\(\\"tableau\\"\)\}</div>`;\s*'
    r'\}else if\(audit\.data\.place===\\"Non\\"\)\{\s*'
    r't\.innerHTML=`<div class=\\"item\\"><b>⚠️ Prévoir un tableau supplémentaire</b><p>Ajouter une photo du tableau existant et l’annoter\.</p>\$\{photos\(\\"tableau\\"\)\}</div>`;\s*'
    r'\}else t\.innerHTML=\\"\\";'
)
replacement = 't.innerHTML=`<div class="item"><b>📷 Photo du tableau</b><p>Prendre une photo puis l’annoter.</p>${photos("tableau")}</div>`;'
s2, n = pattern.subn(replacement, s, count=1)
if n == 1:
    s = s2
else:
    # Same source logic without escaped quotes, used by the current V7 source.
    pattern2 = re.compile(
        r'if\(audit\.data\.place===\"Oui\"\)\{\s*'
        r't\.innerHTML=`<div class="item"><b>📷 Photo du tableau</b><p>Prendre une photo puis l’annoter\.</p>\$\{photos\("tableau"\)\}</div>`;\s*'
        r'\}else if\(audit\.data\.place===\"Non\"\)\{\s*'
        r't\.innerHTML=`<div class="item"><b>⚠️ Prévoir un tableau supplémentaire</b><p>Ajouter une photo du tableau existant et l’annoter\.</p>\$\{photos\("tableau"\)\}</div>`;\s*'
        r'\}else t\.innerHTML="";'
    )
    s2, n = pattern2.subn(replacement, s, count=1)
    if n == 1:
        s = s2
    else:
        raise SystemExit('tableau UI block not found; refusing to publish a risky change')

# 9) Remove the obsolete PLACE DISPONIBLE / TABLEAU SUPPLÉMENTAIRE block from the PDF,
# while leaving the real tableau photo/annotation content untouched.
answer_pattern = re.compile(
    r'\n\s*\$\{first\?`<div class="bigAnswer"><span>PLACE DISPONIBLE DANS LE TABLEAU</span><b>\$\{esc\(place\|\|"Non renseigné"\)\}</b></div>\s*'
    r'\$\{place==="Non"\?`<div class="recommendation"><b>TABLEAU SUPPLÉMENTAIRE À PRÉVOIR</b>.*?`\:\"\"\}`\:\"\"\}\n\s*\$\{block\.html\}',
    re.S,
)
s, removed_answer = answer_pattern.subn('\n    ${block.html}', s, count=1)

# Fallback page that existed only to display the deleted place question.
fallback_pattern = re.compile(
    r'\n\s*if\(!blocks\.length\)\{\s*'
    r'pages\.push\(`[^`]*?PLACE DISPONIBLE DANS LE TABLEAU.*?`\);\s*\}',
    re.S,
)
s, removed_fallback = fallback_pattern.subn('', s, count=1)

# 10) Safety checks: do not publish if the working photo system was accidentally removed.
if 'photos("tableau")' not in s:
    raise SystemExit('SAFETY STOP: tableau photo system disappeared')
if 'Prévoir un tableau supplémentaire' in s:
    raise SystemExit('SAFETY STOP: obsolete warning block remains')
if 'Place disponible dans le tableau ?' in s:
    raise SystemExit('SAFETY STOP: obsolete place question remains')
if 'PLACE DISPONIBLE DANS LE TABLEAU' in s:
    raise SystemExit('SAFETY STOP: obsolete PDF place answer remains')

p.write_text(s, encoding='utf-8')
print('CRVT patch applied safely:', len(s), 'bytes; pdf answer removed=', removed_answer, 'fallback removed=', removed_fallback)
