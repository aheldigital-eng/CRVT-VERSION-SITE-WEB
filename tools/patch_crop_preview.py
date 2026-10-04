from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* CRVT CROP PREVIEW V2 */'
if marker in s:
    print('Crop preview already present')
    raise SystemExit(0)

# Add a live enlarged preview of the exact crop area.
css = '''\n<style id="crvt-crop-preview-v2">\n.crvtCropPreview{position:fixed;right:12px;top:72px;width:min(190px,44vw);height:190px;background:#fff;border:2px solid #14a7b8;border-radius:12px;box-shadow:0 10px 30px #0006;z-index:1200;display:none;overflow:hidden}\n.crvtCropPreview.open{display:block}\n.crvtCropPreviewTitle{height:28px;background:#075d78;color:#fff;font:800 11px Arial,sans-serif;display:flex;align-items:center;justify-content:center}\n.crvtCropPreview canvas{display:block;width:100%;height:calc(100% - 28px);object-fit:contain;background:#111}\n@media(max-width:620px){.crvtCropPreview{width:170px;height:170px;top:66px;right:8px}}\n</style>\n'''
if '</head>' not in s:
    raise SystemExit('head introuvable')
s = s.replace('</head>', css + '</head>', 1)

old_vars = 'let cropStart=null,cropRect=null;'
new_vars = '''let cropStart=null,cropRect=null;\n    let cropPreviewBox=null,cropPreviewCanvas=null;\n    function ensureCropPreview(){\n      if(cropPreviewBox) return;\n      cropPreviewBox=document.createElement("div");\n      cropPreviewBox.className="crvtCropPreview";\n      cropPreviewBox.innerHTML='<div class="crvtCropPreviewTitle">APERÇU DU ROGNAGE</div><canvas></canvas>';\n      document.body.appendChild(cropPreviewBox);\n      cropPreviewCanvas=cropPreviewBox.querySelector("canvas");\n    }\n    function updateCropPreview(){\n      if(tool!=="crop"||!cropRect||!img||!img.complete) return;\n      ensureCropPreview();\n      cropPreviewBox.classList.add("open");\n      const x=Math.min(cropRect.x,cropRect.x2),y=Math.min(cropRect.y,cropRect.y2),w=Math.abs(cropRect.x2-cropRect.x),h=Math.abs(cropRect.y2-cropRect.y);\n      if(w<4||h<4) return;\n      const iw=img.naturalWidth||img.width||c.width,ih=img.naturalHeight||img.height||c.height;\n      const sx=iw/c.width,sy=ih/c.height;\n      const sx0=Math.max(0,Math.round(x*sx)),sy0=Math.max(0,Math.round(y*sy));\n      const sw=Math.max(1,Math.min(iw-sx0,Math.round(w*sx))),sh=Math.max(1,Math.min(ih-sy0,Math.round(h*sy)));\n      const maxW=420,maxH=420,scale=Math.min(maxW/sw,maxH/sh);\n      cropPreviewCanvas.width=Math.max(1,Math.round(sw*scale));\n      cropPreviewCanvas.height=Math.max(1,Math.round(sh*scale));\n      const pc=cropPreviewCanvas.getContext("2d");\n      pc.clearRect(0,0,cropPreviewCanvas.width,cropPreviewCanvas.height);\n      pc.drawImage(img,sx0,sy0,sw,sh,0,0,cropPreviewCanvas.width,cropPreviewCanvas.height);\n    }\n    function removeCropPreview(){\n      if(cropPreviewBox){cropPreviewBox.remove();cropPreviewBox=null;cropPreviewCanvas=null;}\n    }'''
if old_vars not in s:
    raise SystemExit('variables crop introuvables')
s = s.replace(old_vars, new_vars, 1)

old_set = 'function setTool(t){tool=t;drawing=null;drag=null;selected=-1;cropStart=null;cropRect=null;'
new_set = 'function setTool(t){tool=t;drawing=null;drag=null;selected=-1;cropStart=null;cropRect=null;if(t!=="crop")removeCropPreview();else ensureCropPreview();'
if old_set not in s:
    raise SystemExit('setTool crop introuvable')
s = s.replace(old_set, new_set, 1)

old_move = 'if(tool==="crop"&&cropStart){cropRect={x:cropStart.x,y:cropStart.y,x2:p.x,y2:p.y};draw();return;}'
new_move = 'if(tool==="crop"&&cropStart){cropRect={x:cropStart.x,y:cropStart.y,x2:p.x,y2:p.y};draw();updateCropPreview();return;}'
if old_move not in s:
    raise SystemExit('pointermove crop introuvable')
s = s.replace(old_move, new_move, 1)

old_down = 'if(tool==="crop"){cropStart={x:p.x,y:p.y};cropRect={x:p.x,y:p.y,x2:p.x,y2:p.y};draw();return;}'
new_down = 'if(tool==="crop"){ensureCropPreview();cropPreviewBox.classList.add("open");cropStart={x:p.x,y:p.y};cropRect={x:p.x,y:p.y,x2:p.x,y2:p.y};draw();updateCropPreview();return;}'
if old_down not in s:
    raise SystemExit('pointerdown crop introuvable')
s = s.replace(old_down, new_down, 1)

old_up_start = 'if(tool==="crop"&&cropRect){'
if old_up_start not in s:
    raise SystemExit('pointerup crop introuvable')
# Remove preview on every crop completion/cancel by placing it immediately before the existing close.
s = s.replace('close(false);save();render();toast("Photo rognée");return;', 'removeCropPreview();close(false);save();render();toast("Photo rognée");return;', 1)
s = s.replace('cropRect=null;cropStart=null;draw();toast("Zone de rognage trop petite");return;', 'cropRect=null;cropStart=null;draw();removeCropPreview();toast("Zone de rognage trop petite");return;', 1)
s = s.replace('cropRect=null;cropStart=null;draw();return;}\n      const iw=', 'cropRect=null;cropStart=null;draw();removeCropPreview();return;}\n      const iw=', 1)

s = s.replace('</script>\n</body>', marker + '\n</script>\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('OK: live crop preview applied')
