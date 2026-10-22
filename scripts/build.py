from pathlib import Path
import json, re
import yaml

ROOT = Path(__file__).resolve().parents[1]
items = []
errors = []

for file in sorted((ROOT / 'works').glob('*/info.md')):
    text = file.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.S)
    if not match:
        raise ValueError(f'Missing YAML frontmatter: {file}')
    data = yaml.safe_load(match.group(1)) or {}
    for required in ('title', 'year'):
        if not data.get(required):
            raise ValueError(f'{file}: missing {required}')
    folder = file.parent.relative_to(ROOT).as_posix()

    def image_path(path):
        if not path:
            return ''
        if path.startswith('http'):
            return path
        # Paths starting images/ use the site's pre-existing image folder.
        return path if path.startswith('images/') else f'{folder}/{path}'

    data['cover'] = image_path(data.get('cover', ''))
    data['images'] = [dict(im, file=image_path(im.get('file', ''))) for im in data.get('images', [])]
    for block in data.get('layout', []):
        if block.get('file'):
            block['file'] = image_path(block['file'])
        if block.get('files'):
            block['files'] = [image_path(f) for f in block['files']]

    # Check local image references; never alter existing artwork content.
    references = [('cover', data['cover'])]
    references += [(f'images[{i}].file', im.get('file', ''))
                   for i, im in enumerate(data['images'])]
    for i, block in enumerate(data.get('layout', [])):
        if block.get('file'):
            references.append((f'layout[{i}].file', block['file']))
        references += [(f'layout[{i}].files[{j}]', name)
                       for j, name in enumerate(block.get('files', []))]

    for field, image in references:
        if not image or image.startswith(('http://', 'https://')):
            continue
        target = ROOT / image
        if target.is_file():
            continue
        suggestion = ''
        if target.parent.is_dir():
            matches = [candidate.name for candidate in target.parent.iterdir()
                       if candidate.is_file() and candidate.name.casefold() == target.name.casefold()]
            if matches:
                suggestion = f' (case mismatch: {matches[0]})'
        errors.append(f'{file.relative_to(ROOT)} → {field}: {image}{suggestion}')

    data['description'] = match.group(2).strip()
    data['slug'] = file.parent.name
    items.append(data)

if errors:
    raise ValueError('Missing artwork image files:\n- ' + '\n- '.join(dict.fromkeys(errors))
                     + '\nworks.json was not overwritten.')

items.sort(key=lambda x: (-int(x['year']), x['slug']))
(ROOT / 'works.json').write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Built {len(items)} artworks; all referenced local image files exist')
