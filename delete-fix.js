(function(){
  async function crvtDeleteAudit(id){
    if(!window.confirm('Supprimer définitivement cet audit enregistré ?')) return;
    try{
      const db=await new Promise((resolve,reject)=>{
        const req=indexedDB.open('auditTerrainV26DB');
        req.onsuccess=()=>resolve(req.result);
        req.onerror=()=>reject(req.error||new Error('IndexedDB indisponible'));
      });
      await new Promise((resolve,reject)=>{
        const tx=db.transaction('audits','readwrite');
        tx.objectStore('audits').delete(Number(id));
        tx.oncomplete=resolve;
        tx.onerror=()=>reject(tx.error||new Error('Suppression impossible'));
        tx.onabort=()=>reject(tx.error||new Error('Suppression annulée'));
      });
      db.close();
      if(typeof window.idbAll==='function' && typeof window.historyCache!=='undefined'){
        try{ window.historyCache=await window.idbAll(); }catch(e){}
      }
      if(typeof window.history==='function') window.history();
      if(typeof window.render==='function') window.render();
      if(typeof window.toast==='function') window.toast('Audit supprimé');
    }catch(err){
      console.error('CRVT deleteAudit',err);
      if(typeof window.toast==='function') window.toast('Impossible de supprimer cet audit.');
    }
  }
  window.deleteAudit=crvtDeleteAudit;
})();
