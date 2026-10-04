from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '/* CRVT CROP PREVIEW V3 */'
if marker in s:
    print('Crop preview V3 already present')
    raise SystemExit(0)

# Replace the previous small preview with a large, mobile-friendly live preview.
new_css = '''
<style id="crvt-crop-preview-v3">
.crvtCropPreview{position:fixed;left:8px;right:8px;bottom:78px;width:auto;height:min(42vh,360px);background:#fff;border:2px solid #14a7b8;border-radius:14px;box-shadow:0 14px 45px #0008;z-index:2147483000;display:none;overflow:hidden}
.crvtCropPreview.open{display:flex;flex-direction:column}
.crvtCropPreviewTitle{flex:none;height:38px;background:#075d78;color:#fff;font:800 13px Arial,sans-serif;display:flex;align-items:center;justify-content:center;letter-spacing:.3px}
.crvtCropPreview canvas{display:block;flex:1;width:100%;height:calc(100% - 38px);object-fit:contain;background:#111;min-height:0}
@media(min-width:621px){.crvtCropPreview{left:50%;right:auto;transform:translateX(-50%);width:min(720px,calc(100vw - 24px));height:min(46vh,430px);bottom:86px}}
</style>
'''

# If V2 is present, replace only its style block. Otherwise inject V3.
pattern_v2 = re.compile(r'<style id="crvt-crop-preview-v2">.*?</style>', re.S)
if pattern_v2.search(s):
    s = pattern_v2.sub(new_css.strip(), s, count=1)
else:
    if '</head>' not in s:
        raise SystemExit('head introuvable')
    s = s.replace('</head>', new_css + '\n</head>', 1)

# Add a visible marker so this patch is never applied twice.
if '</script>\n</body>' in s:
    s = s.replace('</script>\n</body>', marker + '\n</script>\n</body>', 1)
else:
    raise SystemExit('fin du document introuvable')

p.write_text(s, encoding='utf-8')
print('OK: large live crop preview applied')
