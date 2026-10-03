from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
patch=r'''<script id="crvtDonneurPatch">
(function(){
  const donors=['BUMP','CAP\'BORNE','FRESHMILE','50FIVE','TIME2PLUG'];
  function getAudit(){return typeof audit!=='undefined'?audit:null;}
  function addDonor(){
    const a=getAudit(); const general=document.getElementById('general');
    if(!a||!general||document.getElementById('crvtDonneurSelect')) return;
    const grid=general.querySelector('.grid'); if(!grid) return;
    const wrap=document.createElement('div'); wrap.className='full';
    wrap.innerHTML='<label for="crvtDonneurSelect">Donneur d\'ordre</label><select id="crvtDonneurSelect"><option value="">Sélectionner…</option>'+donors.map(x=>'<option value="'+x.replace(/'/g,"&#039;")+'">'+x+'</option>').join('')+'</select>';
    grid.insertBefore(wrap,grid.children[2]||null);
    const sel=wrap.querySelector('select'); sel.value=a.donneur||'BUMP';
    a.donneur=sel.value;
    sel.addEventListener('change',()=>{a.donneur=sel.value;if(typeof save==='function')save();});
  }
  function injectDonorIntoReport(){
    const overlay=document.getElementById('crvtReportFix'); if(!overlay) return;
    const frame=overlay.querySelector('iframe'); const a=getAudit(); if(!frame||!a) return;
    const apply=()=>{try{const doc=frame.contentDocument;if(!doc||!doc.body)return;if(doc.getElementById('crvtDonorReport'))return;const meta=doc.querySelector('.meta');if(!meta)return;const d=doc.createElement('div');d.id='crvtDonorReport';d.style.cssText='font-weight:800;color:#075777;margin-top:4px';d.textContent=a.donneur||'';meta.appendChild(d);}catch(e){}}
    frame.addEventListener('load',apply,{once:true}); setTimeout(apply,200);
  }
  function watch(){
    addDonor();setTimeout(addDonor,100);setTimeout(addDonor,500);
    const mo=new MutationObserver(()=>{addDonor();injectDonorIntoReport();});
    mo.observe(document.body,{childList:true,subtree:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch);else watch();
})();
</script>'''
if 'crvtDonneurPatch' in s: raise SystemExit(0)
if '</body>' not in s: raise SystemExit('body end not found')
s=s.replace('</body>',patch+'</body>',1)
p.write_text(s,encoding='utf-8')
