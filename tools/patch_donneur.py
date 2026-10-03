from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'crvtDonneurPatch' in s:
    raise SystemExit(0)
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
  function watch(){addDonor();setTimeout(addDonor,100);setTimeout(addDonor,500);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch);else watch();
})();
</script>'''
if '</body>' not in s: raise SystemExit('body end not found')
s=s.replace('</body>',patch+'</body>',1)
p.write_text(s,encoding='utf-8')
