from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* CRVT CROP V1 */'
if marker in s:
    print('Crop patch already present')
    raise SystemExit(0)

crop_css = '''\n<style id="crvt-crop-v1">\n.crvt-crop-overlay{pointer-events:none}\n</style>\n'''
s = s.replace('</head>', crop_css + '</head>', 1)

old_btn = '<button type="button" class="crvt-tool" id="text">T<span>Texte</span></button>'
new_btn = old_btn + '<button type="button" class="crvt-tool" id="crop">✂️<span>Rogner</span></button>'
if old_btn not in s:
    raise SystemExit('Bouton texte introuvable')
s = s.replace(old_btn, new_btn, 1)

old_vars = 'let tool="select",color="#e11d48",strokeStyle="solid",drawing=null,drawingBefore=null,selected=-1,drag=null;'
if old_vars not in s:
    raise SystemExit('Variables annotate introuvables')
s = s.replace(old_vars, old_vars + ' let cropStart=null,cropRect=null;', 1)

old_draw = '  function draw(){\n    if(!c.width||!c.height)return;\n    ctx.clearRect(0,0,c.width,c.height);ctx.drawImage(img,0,0,c.width,c.height);'
new_draw = old_draw + '''\n    if(cropRect){\n      const x=Math.min(cropRect.x,cropRect.x2),y=Math.min(cropRect.y,cropRect.y2),w=Math.abs(cropRect.x2-cropRect.x),h=Math.abs(cropRect.y2-cropRect.y);\n      ctx.save();\n      ctx.fillStyle="rgba(0,0,0,.38)";ctx.fillRect(0,0,c.width,c.height);\n      ctx.clearRect(x,y,w,h);ctx.drawImage(img,0,0,c.width,c.height,x,y,w,h);\n      ctx.strokeStyle="#14a7b8";ctx.lineWidth=3;ctx.setLineDash([10,7]);ctx.strokeRect(x,y,w,h);ctx.setLineDash([]);\n      ctx.fillStyle="#14a7b8";ctx.font="bold 14px Arial";ctx.fillText("Zone conservée",Math.max(6,x+6),Math.max(18,y+18));\n      ctx.restore();\n    }'''
if old_draw not in s:
    raise SystemExit('Début draw introuvable')
s = s.replace(old_draw, new_draw, 1)

old_set = 'function setTool(t){tool=t;drawing=null;drag=null;selected=-1;'
if old_set not in s:
    raise SystemExit('setTool introuvable')
s = s.replace(old_set, 'function setTool(t){tool=t;drawing=null;drag=null;selected=-1;cropStart=null;cropRect=null;', 1)

old_tools = '["select","pen","arrow","line","circle","rect","text"]'
if old_tools not in s:
    raise SystemExit('Liste outils introuvable')
s = s.replace(old_tools, '["select","pen","arrow","line","circle","rect","text","crop"]', 1)

old_down = 'c.onpointerdown=e=>{\n    e.preventDefault();c.setPointerCapture?.(e.pointerId);const p=pt(e);\n    if(tool==="select"){'
new_down = '''c.onpointerdown=e=>{\n    e.preventDefault();c.setPointerCapture?.(e.pointerId);const p=pt(e);\n    if(tool==="crop"){cropStart={x:p.x,y:p.y};cropRect={x:p.x,y:p.y,x2:p.x,y2:p.y};draw();return;}\n    if(tool==="select"){'''
if old_down not in s:
    raise SystemExit('pointerdown introuvable')
s = s.replace(old_down, new_down, 1)

old_move = 'c.onpointermove=e=>{e.preventDefault();const p=pt(e);if(tool==="select"&&drag&&selected>=0){'
new_move = '''c.onpointermove=e=>{e.preventDefault();const p=pt(e);\n    if(tool==="crop"&&cropStart){cropRect={x:cropStart.x,y:cropStart.y,x2:p.x,y2:p.y};draw();return;}\n    if(tool==="select"&&drag&&selected>=0){'''
if old_move not in s:
    raise SystemExit('pointermove introuvable')
s = s.replace(old_move, new_move, 1)

old_up = 'c.onpointerup=e=>{e.preventDefault();if(drawing&&drawingBefore){commit(drawingBefore)}'
new_up = '''c.onpointerup=e=>{\n    e.preventDefault();\n    if(tool==="crop"&&cropRect){\n      const x=Math.min(cropRect.x,cropRect.x2),y=Math.min(cropRect.y,cropRect.y2),w=Math.abs(cropRect.x2-cropRect.x),h=Math.abs(cropRect.y2-cropRect.y);\n      if(w<30||h<30){cropRect=null;cropStart=null;draw();toast("Zone de rognage trop petite");return;}\n      const iw=img.naturalWidth||img.width||c.width,ih=img.naturalHeight||img.height||c.height;\n      const sx=iw/c.width,sy=ih/c.height;\n      const sx0=Math.max(0,Math.round(x*sx)),sy0=Math.max(0,Math.round(y*sy));\n      const sw=Math.min(iw-sx0,Math.round(w*sx)),sh=Math.min(ih-sy0,Math.round(h*sy));\n      if(sw<30||sh<30){cropRect=null;cropStart=null;draw();toast("Zone de rognage trop petite");return;}\n      if((objects||[]).length&&!confirm("Cette photo contient des annotations. Le rognage va les retirer pour éviter qu’elles soient décalées. Continuer ?")){cropRect=null;cropStart=null;draw();return;}\n      const out=document.createElement("canvas");out.width=sw;out.height=sh;out.getContext("2d").drawImage(img,sx0,sy0,sw,sh,0,0,sw,sh);\n      const data=out.toDataURL("image/jpeg",.92);\n      photo.baseData=data;photo.data=data;photo.annotations=[];photo.rotation=0;\n      if(audit.status==="Terminé")audit.status="Brouillon";\n      cropRect=null;cropStart=null;\n      close(false);save();render();toast("Photo rognée");return;\n    }\n    if(drawing&&drawingBefore){commit(drawingBefore)}'''
if old_up not in s:
    raise SystemExit('pointerup introuvable')
s = s.replace(old_up, new_up, 1)

s = s.replace('</script>\n</body>', marker + '\n</script>\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('OK: crop patch applied')
