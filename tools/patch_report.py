from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
if 'crvtReportFix' in s:
    raise SystemExit(0)
patch = r'''<script>
(function(){
  function getAudit(){return typeof audit!=='undefined' ? audit : null;}
  function escR(v){return String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));}
  function reportHTML(){
    const a=getAudit(), d=(a&&a.data)||{};
    const rows=[
      ['Client',a&&a.client],['Auditeur',a&&a.auditeur],['Date',a&&typeof fr==='function'?fr(a.date):''],
      ['Type de visite',a&&a.typeVisite],['Puissance souscrite',d.puissance],['Type de compteur',d.compteur],
      ['Tableau divisionnaire',d.divisionnaire],['Type de borne',d.typeborne],['Environnement',d.environnement],['Positionnement',d.position],
      ['Longueur cheminement',d.longueur?d.longueur+' m':''],['Hauteur / profondeur',d.hauteur?d.hauteur+' m':''],
      ['Type de câble',d.typeCable],['Câble de communication',d.cableCommunication]
    ];
    const photos=[];
    if(a&&a.photos) Object.entries(a.photos).forEach(([sec,arr])=>(arr||[]).forEach(p=>{if(p&&p.data)photos.push({sec,data:p.data,note:p.note||''})}));
    return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CRVT - Compte rendu de visite technique</title><style>body{font-family:Arial,sans-serif;margin:0;color:#172433;background:#fff}main{max-width:900px;margin:auto;padding:28px}h1{color:#075777;margin:0 0 4px;font-size:25px}h2{color:#075777;border-bottom:2px solid #d8e7ed;padding-bottom:7px;margin-top:25px}.meta{color:#64748b;margin-bottom:20px}.grid{display:grid;grid-template-columns:1fr 1fr;border:1px solid #d9e3e8}.cell{padding:9px;border-bottom:1px solid #e6edf0}.cell:nth-child(odd){font-weight:700;background:#f7fafb}.photos{display:grid;grid-template-columns:1fr 1fr;gap:12px}.photo{border:1px solid #d9e3e8;padding:8px;border-radius:8px}.photo img{width:100%;max-height:330px;object-fit:contain}.note{font-size:12px;color:#64748b}@media(max-width:650px){main{padding:16px}.grid,.photos{grid-template-columns:1fr}}</style></head><body><main><h1>CRVT</h1><div class="meta">Compte rendu de visite technique</div><h2>Informations techniques</h2><div class="grid">${rows.filter(r=>r[1]!==undefined&&r[1]!=='').map(r=>`<div class="cell">${escR(r[0])}</div><div class="cell">${escR(r[1])}</div>`).join('')}</div>${a&&a.commentaire?`<h2>Commentaire</h2><p>${escR(a.commentaire).replace(/\n/g,'<br>')}</p>`:''}${d.observations?`<h2>Observations</h2><p>${escR(d.observations).replace(/\n/g,'<br>')}</p>`:''}${photos.length?`<h2>Photos</h2><div class="photos">${photos.map(p=>`<div class="photo"><img src="${p.data}"><div class="note">${escR(p.sec)}${p.note?' — '+escR(p.note):''}</div></div>`).join('')}</div>`:''}<h2>Validation</h2><p>Compte rendu généré depuis CRVT.</p></main></body></html>`;
  }
  function showReport(){
    const old=document.getElementById('crvtReportFix'); if(old)old.remove();
    const overlay=document.createElement('div'); overlay.id='crvtReportFix'; overlay.className='reportOverlay';
    overlay.innerHTML='<div class="reportBar"><b style="margin-right:auto">Aperçu du compte rendu</b><button type="button" id="crvtPrint">🖨️ PDF / Imprimer</button><button type="button" id="crvtClose">✕ Fermer</button></div><iframe class="reportFrame" title="Aperçu PDF"></iframe>';
    document.body.appendChild(overlay);
    const frame=overlay.querySelector('iframe'); const html=reportHTML(); frame.srcdoc=html;
    overlay.querySelector('#crvtClose').onclick=()=>overlay.remove();
    overlay.querySelector('#crvtPrint').onclick=()=>{try{frame.contentWindow.focus();frame.contentWindow.print();}catch(e){const w=window.open();if(w){w.document.write(html);w.document.close();w.focus();w.print();}}};
  }
  const install=()=>{const b=document.getElementById('reportBtn');if(b)b.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();showReport();},true);};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>'''
if '</body>' not in s:
    raise SystemExit('body end not found')
s = s.replace('</body>', patch + '</body>', 1)
p.write_text(s, encoding='utf-8')
