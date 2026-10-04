from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'CRVT CROP PREVIEW V3'
if marker in s:
    print('V3 already applied')
    raise SystemExit(0)

css = r'''<style id="crvt-crop-preview-v3">
/* CRVT CROP PREVIEW V3 */
.crvt-crop-active .canvaswrap{
  display:grid!important;
  grid-template-columns:1fr!important;
  grid-template-rows:minmax(0,1fr) minmax(0,1fr)!important;
  align-items:stretch!important;
  justify-items:stretch!important;
  gap:8px!important;
  padding:8px!important;
  background:#f8fafc!important;
}
.crvt-crop-active .canvaswrap canvas#crvtCropSource{
  grid-row:1!important;
  width:100%!important;
  height:100%!important;
  max-width:100%!important;
  max-height:100%!important;
  object-fit:contain!important;
  min-height:0!important;
}
.crvt-crop-active .canvaswrap .crvt-crop-preview-wrap{
  grid-row:2!important;
  display:flex!important;
  width:100%!important;
  height:100%!important;
  min-height:0!important;
  flex:initial!important;
  flex-direction:column!important;
  align-items:center!important;
  justify-content:center!important;
  gap:5px!important;
  padding:5px!important;
  border:1px solid #cbd5e1!important;
  border-radius:10px!important;
  background:#fff!important;
  overflow:hidden!important;
}
.crvt-crop-active .crvt-crop-preview-label{
  flex:none!important;
  display:block!important;
  font:800 11px Arial,sans-serif!important;
  color:#0b6e9e!important;
  letter-spacing:.7px!important;
  text-transform:uppercase!important;
}
.crvt-crop-active .canvaswrap canvas.crvt-crop-preview{
  display:block!important;
  width:100%!important;
  height:calc(100% - 22px)!important;
  max-width:100%!important;
  max-height:calc(100% - 22px)!important;
  min-height:0!important;
  object-fit:contain!important;
  background:#111!important;
  border:2px solid #14a7b8!important;
  border-radius:7px!important;
}
@media(max-width:620px){
  .crvt-crop-active .canvaswrap{grid-template-rows:minmax(0,1fr) minmax(0,1fr)!important;padding:5px!important;gap:5px!important}
  .crvt-crop-active .canvaswrap .crvt-crop-preview-wrap{padding:4px!important}
}
</style>'''

if '</head>' not in s:
    raise SystemExit('head introuvable')
s = s.replace('</head>', css + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
print('OK: V3 split-screen crop preview CSS added')
