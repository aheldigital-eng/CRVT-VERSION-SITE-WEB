from pathlib import Path

# The tableau photo system is already validated. Do not rewrite or remove
# its fields from the published CRVT page during PWA publication.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
p.write_text(s, encoding='utf-8')
print(f'OK tableau module preserved; bytes={len(s)}')
