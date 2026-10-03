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

# 5) Keep the validated annotation tools intact and make the toolbar scrollable on small phones.
old = '.tools{display:flex;gap:6px;flex-wrap:wrap}.tools .btn{flex:none}'
new = '.tools{display:flex;gap:6px;flex-wrap:wrap;max-height:34vh;overflow-y:auto;padding-right:2px;align-content:flex-start}.tools .btn{flex:none}.tools select{flex:none;min-height:44px}.tools::-webkit-scrollbar{width:6px}.tools::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:99px}'
if old not in s:
    raise SystemExit('tools css target not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('CRVT patch applied:', len(s), 'bytes')
