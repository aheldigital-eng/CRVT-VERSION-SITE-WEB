import re
from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove the obsolete tableau availability question, without touching photo controls.
s,nq=re.subn(r'tableau:\[\s*\["place","Place disponible dans le tableau \?","select:Oui\|Non"\]\s*\],','tableau:[],',s,count=1)

# Replace only the conditional wrapper around the existing tableau photo block.
pat=re.compile(r'if\(audit\.data\.place===("\')Oui\1\)\{\s*'
              r't\.innerHTML=`<div class="item"><b>📷 Photo du tableau</b><p>Prendre une photo puis l’annoter\.</p>\$\{photos\("tableau"\)\}</div>`;\s*'
              r'\}else if\(audit\.data\.place===("\')Non\2\)\{\s*'
              r't\.innerHTML=`<div class="item"><b>⚠️ Prévoir un tableau supplémentaire</b><p>Ajouter une photo du tableau existant et l’annoter\.</p>\$\{photos\("tableau"\)\}</div>`;\s*'
              r'\}else t\.innerHTML="";')
replacement='t.innerHTML=`<div class="item"><b>📷 Photo du tableau</b><p>Prendre une photo puis l’annoter.</p>${photos("tableau")}</div>`;'
s,nui=pat.subn(replacement,s,count=1)

# Remove the obsolete PDF answer tied to the deleted question.
pdf_pat=re.compile(r'\n\s*\$\{first\?`<div class="bigAnswer"><span>PLACE DISPONIBLE DANS LE TABLEAU</span><b>\$\{esc\(place\|\|"Non renseigné"\)\}</b></div>\s*\$\{place==="Non"\?`<div class="recommendation"><b>TABLEAU SUPPLÉMENTAIRE À PRÉVOIR</b>.*?`:\"\"\}`:\"\"\}\n\s*\$\{block\.html\}',re.S)
s,npdf=pdf_pat.subn('\n    ${block.html}',s,count=1)

# Remove the old empty-table fallback page which existed only for the deleted question.
fallback=re.compile(r'\n\s*if\(!blocks\.length\)\{\s*pages\.push\(`[^`]*?PLACE DISPONIBLE DANS LE TABLEAU.*?`\);\s*\}',re.S)
s,nfb=fallback.subn('',s,count=1)

# Safety: never publish if the photo system was removed or the obsolete block remains.
if 'Place disponible dans le tableau ?' in s or 'Prévoir un tableau supplémentaire' in s or 'PLACE DISPONIBLE DANS LE TABLEAU' in s:
    raise SystemExit('SAFETY STOP: obsolete tableau text remains')
if 'photos("tableau")' not in s:
    raise SystemExit('SAFETY STOP: tableau photo system disappeared')
if nui != 1:
    raise SystemExit(f'SAFETY STOP: tableau photo block replacement count={nui}')

p.write_text(s,encoding='utf-8')
print(f'OK nq={nq} ui={nui} pdf={npdf} fallback={nfb} bytes={len(s)}')
