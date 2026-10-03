from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace("const d=(window.audit&&audit.data)||{};", "const a=(typeof audit!=='undefined')?audit:null, d=(a&&a.data)||{};")
s=s.replace("['Client',window.audit&&audit.client],['Auditeur',window.audit&&audit.auditeur],['Date',window.audit&&typeof fr==='function'?fr(audit.date):'']", "['Client',a&&a.client],['Auditeur',a&&a.auditeur],['Date',a&&typeof fr==='function'?fr(a.date):'']")
s=s.replace("['Type de visite',window.audit&&audit.typeVisite]", "['Type de visite',a&&a.typeVisite]")
s=s.replace("if(window.audit&&audit.photos)", "if(a&&a.photos)")
s=s.replace("${window.audit&&audit.commentaire?", "${a&&a.commentaire?")
p.write_text(s,encoding='utf-8')
