from pathlib import Path
import json, re
import yaml
ROOT = Path(__file__).resolve().parents[1]
items=[]
for file in sorted((ROOT/'works').glob('*/info.md')):
    text=file.read_text(encoding='utf-8')
    match=re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$',text,re.S)
    if not match:
        raise ValueError(f'Missing YAML frontmatter: {file}')
    data=yaml.safe_load(match.group(1)) or {}
    for required in ('title','year'):
        if not data.get(required): raise ValueError(f'{file}: missing {required}')
    folder=file.parent.relative_to(ROOT).as_posix()
    def image_path(path):
        if not path: return ''
        if path.startswith('http'): return path
        # Paths starting images/ use the site's pre-existing image folder.
        return path if path.startswith('images/') else f'{folder}/{path}'
    data['cover']=image_path(data.get('cover',''))
    data['images']=[dict(im,file=image_path(im.get('file',''))) for im in data.get('images',[])]
    data['description']=match.group(2).strip()
    data['slug']=file.parent.name
    items.append(data)
items.sort(key=lambda x:(-int(x['year']),x['slug']))
(ROOT/'works.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Built {len(items)} artworks')
