(function(){
'use strict';
const css=document.createElement('style');
css.textContent=`
.crvtNewAnnotOverlay{position:fixed!important;inset:0!important;width:100vw!important;height:100dvh!important;background:rgba(9,25,38,.97)!important;z-index:2147483647!important;display:flex!important;flex-direction:column!important;overflow:hidden!important;padding:0!important;margin:0!important;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important}
html.crvtAnnotLock,body.crvtAnnotLock{overflow:hidden!important;height:100%!important;overscroll-behavior:none!important}
body.crvtAnnotLock>header,body.crvtAnnotLock>#quickNav{display:none!important;visibility:hidden!important;pointer-events:none!important}
.crvtAnnotHead{flex:0 0 auto;background:linear-gradient(135deg,#081b2c,#0b496b 55%,#13a9b8);color:#fff;padding:10px 12px;display:flex;align-items:center;justify-content:space-between;gap:10px;box-shadow:0 3px 15px #0005;z-index:5}
.crvtAnnotHead b{font-size:16px}.crvtAnnotHead span{font-size:11px;opacity:.82;display:block;margin-top:2px}.crvtAnnotClose{border:0;background:#fff;color:#173247;border-radius:12px;width:42px;height:42px;font-size:24px;font-weight:900;cursor:pointer;touch-action:manipulation}
.crvtAnnotTools{flex:0 0 auto;background:#f7fafc;border-bottom:1px solid #cbd5e1;padding:8px;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:7px;max-height:34dvh;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;z-index:4}
.crvtAnnotBtn,.crvtAnnotSelect{min-width:0;min-height:46px;border:1px solid #cbd5e1;border-radius:12px;background:#fff;color:#294052;font-weight:850;font-size:13px;padding:7px 6px;cursor:pointer;touch-action:manipulation;user-select:none;-webkit-tap-highlight-color:transparent}
.crvtAnnotBtn.active{background:#e4f8fb;border-color:#14a7b8;box-shadow:0 0 0 2px #14a7b833;color:#075a82}.crvtAnnotBtn.danger{background:#fff1f2;border-color:#fecdd3;color:#b91c1c}.crvtAnnotBtn.primary{background:linear-gradient(135deg,#0b6e9e,#13a7b8);border-color:transparent;color:#fff}.crvtAnnotSelect{appearance:auto;padding-left:8px}
.crvtAnnotCanvasArea{flex:1 1 auto;min-height:0;position:relative;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#101820;padding:8px}.crvtAnnotCanvasBox{position:relative;max-width:100%;max-height:100%;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 35px #0008;background:#fff;touch-action:none}#crvtAnnotCanvas{display:block;max-width:100%;max-height:100%;width:auto;height:auto;touch-action:none;cursor:crosshair;background:#fff}
.crvtAnnotHelp{flex:0 0 auto;background:#081b2c;color:#d8e8ef;padding:7px 10px;font-size:11px;line-height:1.35;text-align:center}.crvtAnnotActions{flex:0 0 auto;background:#f7fafc;padding:7px 8px;display:grid;grid-template-columns:1fr 1fr 1.2fr;gap:7px;border-top:1px solid #cbd5e1;z-index:5}
@media(max-width:700px){.crvtAnnotTools{grid-template-columns:repeat(3,minmax(0,1fr));max-height:38dvh}.crvtAnnotBtn,.crvtAnnotSelect{min-height:48px;font-size:12px}.crvtAnnotHead{padding:8px 10px}.crvtAnnotHead b{font-size:14px}.crvtAnnotCanvasArea{padding:5px}.crvtAnnotActions{grid-template-columns:1fr 1fr 1.35fr}.crvtAnnotHelp{font-size:10px}}
`;
document.head.appendChild(css);
const clone=a=>JSON.parse(JSON.stringify(a||[]));
const loadImage=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=src});
function getAudit(){try{return eval('audit')}catch(e){return null}}
window.annotate=async function(sec,i){
 try{
  const audit=getAudit(),photo=audit?.photos?.[sec]?.[i];
  if(!photo){toast('Photo introuvable');return}
  const src=photo.baseData||photo.data;if(!src){toast('Image introuvable');return}
  if(!photo.baseData)photo.baseData=src;if(!Array.isArray(photo.annotations))photo.annotations=[];
  const im=await loadImage(src),max=1800,scale=Math.min(1,max/im.naturalWidth,max/im.naturalHeight),W=Math.max(1,Math.round(im.naturalWidth*scale)),H=Math.max(1,Math.round(im.naturalHeight*scale));
  const ov=document.createElement('div');ov.className='crvtNewAnnotOverlay';ov.innerHTML=`
  <div class="crvtAnnotHead"><div><b>✏️ Annoter la photo</b><span>Photo ${i+1} • annotations visibles dans le rapport</span></div><button class="crvtAnnotClose" id="caClose">×</button></div>
  <div class="crvtAnnotTools">
   <button class="crvtAnnotBtn active" data-tool="select">↖️ Sélection</button><button class="crvtAnnotBtn" data-tool="draw">✏️ Dessin</button><button class="crvtAnnotBtn" data-tool="arrow">↗️ Flèche</button><button class="crvtAnnotBtn" data-tool="line">╱ Ligne</button><button class="crvtAnnotBtn" data-tool="circle">⭕ Cercle</button><button class="crvtAnnotBtn" data-tool="rect">▭ Rectangle</button><button class="crvtAnnotBtn" data-tool="text">T Texte</button><button class="crvtAnnotBtn active" data-style="solid">━ Plein</button><button class="crvtAnnotBtn" data-style="dashed">╌ Pointillé</button>
   <select class="crvtAnnotSelect" id="caColor"><option value="#ef3340">🔴 Rouge</option><option value="#1479a6">🔵 Bleu</option><option value="#16a34a">🟢 Vert</option><option value="#f59e0b">🟠 Orange</option><option value="#111827">⚫ Noir</option><option value="#ffffff">⚪ Blanc</option></select>
   <button class="crvtAnnotBtn" id="caUndo">↶ Annuler</button><button class="crvtAnnotBtn" id="caRedo">↷ Rétablir</button><button class="crvtAnnotBtn" id="caDelete">🗑️ Supprimer</button><button class="crvtAnnotBtn" id="caSmall">➖ Réduire</button><button class="crvtAnnotBtn" id="caLarge">➕ Agrandir</button><button class="crvtAnnotBtn danger" id="caClear">🧹 Tout effacer</button>
  </div>
  <div class="crvtAnnotCanvasArea"><div class="crvtAnnotCanvasBox"><canvas id="crvtAnnotCanvas" width="${W}" height="${H}"></canvas></div></div>
  <div class="crvtAnnotHelp">Sélection : touchez une annotation pour la déplacer. Tracez avec le doigt. Texte : touchez l'image puis saisissez le texte.</div>
  <div class="crvtAnnotActions"><button class="crvtAnnotBtn" id="caCancel">✕ Annuler</button><button class="crvtAnnotBtn" id="caReset">↺ Réinitialiser</button><button class="crvtAnnotBtn primary" id="caSave">💾 Enregistrer</button></div>`;
  document.body.appendChild(ov);document.documentElement.classList.add('crvtAnnotLock');document.body.classList.add('crvtAnnotLock');
  const c=ov.querySelector('#crvtAnnotCanvas'),ctx=c.getContext('2d');let anns=clone(photo.annotations),history=[clone(anns)],hp=0,tool='select',style='solid',color='#ef3340',selected=-1,drawing=null,drag=null;
  const snapshot=()=>{history=history.slice(0,hp+1);history.push(clone(anns));if(history.length>50)history.shift();hp=history.length-1};
  const bbox=a=>({x:Math.min(a.x1,a.x2),y:Math.min(a.y1,a.y2),w:Math.abs(a.x2-a.x1),h:Math.abs(a.y2-a.y1)});
  function stroke(g,a){g.strokeStyle=a.color||'#ef3340';g.lineWidth=a.size||Math.max(4,W/350);g.lineCap='round';g.lineJoin='round';g.setLineDash(a.style==='dashed'?[14,10]:[])}
  function arrow(g,a){const ang=Math.atan2(a.y2-a.y1,a.x2-a.x1),len=Math.max(12,Math.min(34,Math.hypot(a.x2-a.x1,a.y2-a.y1)*.18));g.beginPath();g.moveTo(a.x2,a.y2);g.lineTo(a.x2-len*Math.cos(ang-.48),a.y2-len*Math.sin(ang-.48));g.moveTo(a.x2,a.y2);g.lineTo(a.x2-len*Math.cos(ang+.48),a.y2-len*Math.sin(ang+.48));g.stroke()}
  function drawOne(g,a,idx){stroke(g,a);if(idx===selected){g.save();g.strokeStyle='#14a7b8';g.lineWidth=Math.max(3,(a.size||4)+5);g.setLineDash([8,7]);const n=a.type==='text'?{x:a.x,y:a.y,w:(a.text||'').length*(a.size||32)*.65,h:(a.size||32)*1.3}:{...bbox(a)};g.strokeRect(n.x-8,n.y-8,Math.max(16,n.w+16),Math.max(16,n.h+16));g.restore();stroke(g,a)}
   if(a.type==='draw'){g.beginPath();(a.points||[]).forEach((p,j)=>j?g.lineTo(p.x,p.y):g.moveTo(p.x,p.y));g.stroke()}
   else if(a.type==='line'||a.type==='arrow'){g.beginPath();g.moveTo(a.x1,a.y1);g.lineTo(a.x2,a.y2);g.stroke();if(a.type==='arrow')arrow(g,a)}
   else if(a.type==='circle'){const n=bbox(a);g.beginPath();g.ellipse(n.x+n.w/2,n.y+n.h/2,Math.max(1,n.w/2),Math.max(1,n.h/2),0,0,Math.PI*2);g.stroke()}
   else if(a.type==='rect'){const n=bbox(a);g.strokeRect(n.x,n.y,n.w,n.h)}
   else if(a.type==='text'){g.save();g.fillStyle=a.color||'#ef3340';g.font=`900 ${a.size||32}px Arial`;g.textBaseline='top';String(a.text||'').split('\n').forEach((t,j)=>g.fillText(t,a.x,a.y+j*(a.size||32)*1.15));g.restore()}
   g.setLineDash([])
  }
  function redraw(){ctx.clearRect(0,0,W,H);ctx.drawImage(im,0,0,W,H);anns.forEach((a,k)=>drawOne(ctx,a,k));if(drawing){const a={type:tool,points:drawing.points,x1:drawing.start.x,y1:drawing.start.y,x2:drawing.last.x,y2:drawing.last.y,color,style,size:Math.max(4,W/350)};if(tool==='draw')drawOne(ctx,{...a,type:'draw'},-1);else drawOne(ctx,a,-1)}}
  const point=e=>{const r=c.getBoundingClientRect();return{x:(e.clientX-r.left)*W/r.width,y:(e.clientY-r.top)*H/r.height}};
  const seg=(p,a,b)=>{const dx=b.x-a.x,dy=b.y-a.y,l=dx*dx+dy*dy;if(!l)return Math.hypot(p.x-a.x,p.y-a.y);let t=((p.x-a.x)*dx+(p.y-a.y)*dy)/l;t=Math.max(0,Math.min(1,t));return Math.hypot(p.x-(a.x+t*dx),p.y-(a.y+t*dy))};
  function hit(a,p){const pad=Math.max(20,a.size||5);if(a.type==='draw')return (a.points||[]).some((q,j)=>j>0&&seg(p,a.points[j-1],q)<pad);if(a.type==='text'){const w=(a.text||'').length*(a.size||32)*.65;return p.x>=a.x-pad&&p.x<=a.x+w+pad&&p.y>=a.y-pad&&p.y<=a.y+(a.size||32)*1.5+pad}const n=bbox(a);if(a.type==='line'||a.type==='arrow')return seg(p,{x:a.x1,y:a.y1},{x:a.x2,y:a.y2})<pad;if(a.type==='circle'){const cx=n.x+n.w/2,cy=n.y+n.h/2,rx=Math.max(1,n.w/2),ry=Math.max(1,n.h/2),v=((p.x-cx)/rx)**2+((p.y-cy)/ry)**2;return Math.abs(v-1)<.25||v<1&&p.x>=n.x-pad&&p.x<=n.x+n.w+pad&&p.y>=n.y-pad&&p.y<=n.y+n.h+pad}return p.x>=n.x-pad&&p.x<=n.x+n.w+pad&&p.y>=n.y-pad&&p.y<=n.y+n.h+pad}
  function setTool(t){tool=t;ov.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));c.style.cursor=t==='select'?'grab':t==='text'?'text':'crosshair'}
  ov.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));ov.querySelectorAll('[data-style]').forEach(b=>b.onclick=()=>{style=b.dataset.style;ov.querySelectorAll('[data-style]').forEach(x=>x.classList.toggle('active',x.dataset.style===style))});ov.querySelector('#caColor').onchange=e=>color=e.target.value;
  ov.querySelector('#caUndo').onclick=()=>{if(hp>0){hp--;anns=clone(history[hp]);selected=-1;redraw()}};ov.querySelector('#caRedo').onclick=()=>{if(hp<history.length-1){hp++;anns=clone(history[hp]);selected=-1;redraw()}};
  ov.querySelector('#caDelete').onclick=()=>{if(selected>=0){anns.splice(selected,1);selected=-1;snapshot();redraw()}};function resize(f){if(selected<0)return;anns[selected].size=Math.max(2,Math.min(120,(anns[selected].size||5)*f));snapshot();redraw()}ov.querySelector('#caSmall').onclick=()=>resize(.8);ov.querySelector('#caLarge').onclick=()=>resize(1.25);
  ov.querySelector('#caClear').onclick=()=>{if(!anns.length||confirm('Supprimer toutes les annotations de cette photo ?')){anns=[];selected=-1;snapshot();redraw()}};
  function addText(p){const t=prompt('Texte à placer sur la photo :','');if(!t||!t.trim())return;anns.push({type:'text',x:p.x,y:p.y,text:t.trim(),color,size:Math.max(24,W/35),style:'solid'});selected=anns.length-1;snapshot();redraw()}
  c.onpointerdown=e=>{e.preventDefault();c.setPointerCapture?.(e.pointerId);const p=point(e);if(tool==='text'){addText(p);return}if(tool==='select'){selected=-1;for(let k=anns.length-1;k>=0;k--)if(hit(anns[k],p)){selected=k;break}if(selected>=0)drag={start:p,orig:clone(anns[selected])};redraw();return}drawing={start:p,last:p,points:[p]};redraw()};
  c.onpointermove=e=>{const p=point(e);if(drag){const a=anns[selected],o=drag.orig,dx=p.x-drag.start.x,dy=p.y-drag.start.y;if(o.x1!==undefined){a.x1=o.x1+dx;a.y1=o.y1+dy;a.x2=o.x2+dx;a.y2=o.y2+dy}if(o.x!==undefined){a.x=o.x+dx;a.y=o.y+dy}if(o.points)a.points=o.points.map(q=>({x:q.x+dx,y:q.y+dy}));redraw();return}if(drawing){drawing.last=p;drawing.points.push(p);redraw()}};
  c.onpointerup=e=>{if(drag){drag=null;snapshot();redraw();return}if(!drawing)return;const d=drawing;drawing=null;if(tool==='draw'){if(d.points.length>1)anns.push({type:'draw',points:d.points,color,style,size:Math.max(4,W/350)})}else{const end=d.last;if(Math.hypot(end.x-d.start.x,end.y-d.start.y)>4)anns.push({type:tool,x1:d.start.x,y1:d.start.y,x2:end.x,y2:end.y,color,style,size:Math.max(4,W/350)})}selected=anns.length-1;snapshot();redraw()};
  const close=()=>{ov.remove();document.documentElement.classList.remove('crvtAnnotLock');document.body.classList.remove('crvtAnnotLock')};ov.querySelector('#caClose').onclick=close;ov.querySelector('#caCancel').onclick=close;ov.querySelector('#caReset').onclick=()=>{anns=clone(photo.annotations);history=[clone(anns)];hp=0;selected=-1;redraw()};
  ov.querySelector('#caSave').onclick=()=>{const out=document.createElement('canvas');out.width=W;out.height=H;const g=out.getContext('2d');g.drawImage(im,0,0,W,H);anns.forEach(a=>drawOne(g,a,-1));photo.data=out.toDataURL('image/jpeg',.9);photo.baseData=photo.baseData||src;photo.annotations=clone(anns);if(audit.status==='Terminé')audit.status='Brouillon';save();close();render();updateQuickNav();toast(anns.length?`${anns.length} annotation(s) enregistrée(s)`:'Photo enregistrée')};
  redraw();
 }catch(e){console.error(e);toast('Erreur annotation : '+(e.message||e))}
};
console.log('CRVT annotation editor v3 actif');
})();