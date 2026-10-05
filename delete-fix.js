(function(){
  async function openCrvtDb(){
    return await new Promise(function(resolve,reject){
      var req=indexedDB.open('auditTerrainV26DB');
      req.onsuccess=function(){resolve(req.result)};
      req.onerror=function(){reject(req.error||new Error('IndexedDB indisponible'))};
    });
  }
  async function crvtDeleteAudit(id){
    if(!window.confirm('Supprimer définitivement cet audit enregistré ?')) return;
    var db=null;
    try{
      db=await openCrvtDb();
      await new Promise(function(resolve,reject){
        var tx=db.transaction('audits','readwrite');
        var store=tx.objectStore('audits');
        var key=id;
        var getReq=store.get(id);
        getReq.onsuccess=function(){
          if(getReq.result==null){
            var n=Number(id);
            if(!Number.isNaN(n)){
              var getNum=store.get(n);
              getNum.onsuccess=function(){
                if(getNum.result!=null) key=n;
                store.delete(key);
              };
              getNum.onerror=function(){store.delete(key)};
            }else store.delete(key);
          }else store.delete(key);
        };
        getReq.onerror=function(){store.delete(key)};
        tx.oncomplete=function(){resolve()};
        tx.onerror=function(){reject(tx.error||new Error('Suppression impossible'))};
        tx.onabort=function(){reject(tx.error||new Error('Suppression annulée'))};
      });
      if(db) db.close();
      if(typeof window.idbAll==='function'){
        try{window.historyCache=await window.idbAll()}catch(e){}
      }
      if(typeof window.history==='function') window.history();
      if(typeof window.render==='function') window.render();
      if(typeof window.toast==='function') window.toast('Audit supprimé');
    }catch(err){
      try{if(db) db.close()}catch(e){}
      console.error('CRVT deleteAudit',err);
      if(typeof window.toast==='function') window.toast('Impossible de supprimer cet audit.');
      else window.alert('Impossible de supprimer cet audit.');
    }
  }
  window.deleteAudit=crvtDeleteAudit;
})();
