from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Put cable characteristics directly in Informations techniques.
old = '["environnement","Environnement Borne","select:Extérieur|Intérieur|Autre"],["position","Positionnement de Borne","select:Sur mur|Sur pied|Autre"]'
new = '["environnement","Environnement Borne","select:Extérieur|Intérieur|Autre"],["position","Positionnement de Borne","select:Sur mur|Sur pied|Autre"],["longueurCable","Mesure du cheminement (m)","number"],["typeCable","Type de câble","select:3G10|5G10"],["cableCommunication","Câble de communication","select:Oui|Non"]'
if old not in s:
    raise SystemExit('common target not found')
s = s.replace(old, new, 1)

# 2) Include the new fields in the PDF technical information table.
old = 'position:"Positionnement de la borne"\n};'
new = 'position:"Positionnement de la borne",\nlongueurCable:"Mesure du cheminement (m)",\ntypeCable:"Type de câble",\ncableCommunication:"Câble de communication"\n};'
if old not in s:
    raise SystemExit('techLabels target not found')
s = s.replace(old, new, 1)

# 3) Make the Informations tab status aware of the new fields.
old = 'if(key==="infos") return audit.data.commentaire||audit.data.place||audit.data.puissance||audit.data.compteur||audit.data.borne||audit.data.environnement||audit.data.position?"ok":"warn";'
new = 'if(key==="infos") return audit.data.commentaire||audit.data.place||audit.data.puissance||audit.data.compteur||audit.data.borne||audit.data.environnement||audit.data.position||audit.data.longueurCable||audit.data.typeCable||audit.data.cableCommunication?"ok":"warn";'
if old not in s:
    raise SystemExit('quicknav target not found')
s = s.replace(old, new, 1)

# 4) Remove the obsolete cable-fields patch that was incorrectly embedded in the generated PDF iframe.
start = s.find('<!-- CRVT V7+ cable fields patch -->')
if start != -1:
    end = s.find('</body></html>`;', start)
    if end == -1:
        raise SystemExit('obsolete patch end not found')
    s = s[:start] + s[end:]

# 5) Remove the obsolete "Place disponible dans le tableau ?" question.
old = 'tableau:[\n["place","Place disponible dans le tableau ?","select:Oui|Non"]\n],'
if old in s:
    s = s.replace(old, 'tableau:[],', 1)

# 6) Put annotation tools on two rows on mobile while keeping all tools clickable.
old = '.crvtAnnotTools{flex:0 0 auto;display:flex;gap:8px;align-items:center;overflow-x:auto;overflow-y:hidden;padding:9px;background:#fff;border-bottom:1px solid #dbe5ec;box-shadow:0 3px 12px #0002;-webkit-overflow-scrolling:touch}'
new = '.crvtAnnotTools{flex:0 0 auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;align-items:stretch;padding:9px;background:#fff;border-bottom:1px solid #dbe5ec;box-shadow:0 3px 12px #0002}.crvtAnnotTools .crvtAT,.crvtAnnotTools .crvtASelect{width:100%;min-width:0}'
if old not in s:
    raise SystemExit('annotation toolbar target not found')
s = s.replace(old, new, 1)

# 7) Make every annotation button the same compact size on phones.
old = '@media(max-width:620px){.crvtAnnotHead>div{font-size:16px}.crvtAnnotFoot{align-items:stretch}.crvtAnnotFoot span{display:none}.crvtAnnotFoot>div{width:100%;display:flex}.crvtCancel,.crvtSave{flex:1}.crvtAT,.crvtASelect{font-size:13px;padding:8px 10px}}'
new = '@media(max-width:620px){.crvtAnnotHead>div{font-size:16px}.crvtAnnotTools{grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;padding:7px}.crvtAT,.crvtASelect{font-size:12px;padding:8px 4px;min-height:42px;border-radius:10px}.crvtAnnotFoot{align-items:stretch}.crvtAnnotFoot span{display:none}.crvtAnnotFoot>div{width:100%;display:flex}.crvtCancel,.crvtSave{flex:1}}'
if old not in s:
    raise SystemExit('mobile annotation CSS target not found')
s = s.replace(old, new, 1)

# 8) Remove ONLY the obsolete "Prévoir un tableau supplémentaire" block.
# Keep the existing photo/annotation system and every other working tableau control unchanged.
old = '}else if(audit.data.place==="Non"){\nt.innerHTML=`<div class="item"><b>⚠️ Prévoir un tableau supplémentaire</b><p>Ajouter une photo du tableau existant et l’annoter.</p>${photos("tableau")}</div>`;\n}else t.innerHTML="";'
new = '}else t.innerHTML="";'
if old in s:
    s = s.replace(old, new, 1)

# 9) Remove the old PLACE DISPONIBLE / TABLEAU SUPPLÉMENTAIRE answer from the PDF.
# Do not remove the actual tableau photo/annotation blocks.
old = '''    ${first?`<div class="bigAnswer"><span>PLACE DISPONIBLE DANS LE TABLEAU</span><b>${esc(place||"Non renseigné")}</b>
    ${place==="Non"?`<div class="recommendation"><b>TABLEAU SUPPLÉMENTAIRE À PRÉVOIR</b>${photos.length?`<br>La photo ci-dessous permet de localiser la situation constatée.`:""}</div>`:""}`:""}
    ${block.html}'''
new = '''    ${block.html}'''
if old in s:
    s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('CRVT patch applied:', len(s), 'bytes')
