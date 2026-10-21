#!/usr/bin/env python3
"""One-time conservative patch: read artwork sizes, alignment, captions from info.md.

Place this file at scripts/enable_info_layout.py in the website repository.
Run locally from the repo with: python scripts/enable_info_layout.py
Existing artwork content, index navigation, styling and default layouts are retained.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'index.html'
if not path.is_file():
    raise SystemExit('ERROR: scripts/enable_info_layout.py must be inside the website repository.')
html = path.read_text(encoding='utf-8')
MARKER = '/* INFO_MD_ARTWORK_LAYOUT_V2 */'
if MARKER in html:
    print('Already installed; no changes made.')
    raise SystemExit(0)
start_key = 'let vid=videoId(work.video);let hero='
end_key = "\nlet images='',queue=[];"
start = html.find(start_key)
end = html.find(end_key, start)
if start == -1 or end == -1 or html.count(start_key) != 1 or html.count(end_key) != 1:
    raise SystemExit('ERROR: Unrecognized index.html; no changes made.')
old_block = html[start:end]
assert 'const photoFigure=' in old_block and '2018-elegy' in old_block
image_line = "editorial+=photoFigure(im,im.type==='installation'?'work-image--installation':'work-image--detail-single');"
pair_line = "(block.files||[]).map(f=>photoFigure(photoMap.get(f)||{file:f},'work-image--detail'))"
if html.count(image_line) != 1 or html.count(pair_line) != 1:
    raise SystemExit('ERROR: Unexpected layout format; no changes made.')
replacement = r'''/* INFO_MD_ARTWORK_LAYOUT_V2 */
// Frontmatter options: cover_width: 72%, cover_caption: "...";
// images: - file: ...; width: 75%; align: center; caption: "..."
// layout: - type: image; file: ...; width: 75%; align: left
function artworkWidth(v) {
  if(v===undefined||v===null||String(v).trim()==='')return '';
  let s=String(v).trim();
  if(/^\d+(?:\.\d+)?$/.test(s))s+='%';
  if(!/^\d+(?:\.\d+)?%$/.test(s))return '';
  const n=parseFloat(s);
  return n>=10&&n<=200?`${n}%`:'';
}
function artworkAlign(v) {
  let s=String(v||'center').toLowerCase();
  return ['left','center','right'].includes(s)?s:'center';
}
function imageStyle(im,cls) {
  // Keep old sizing for every image without an explicit info.md width.
  let w=artworkWidth(im.width);
  if(!w&&work.slug==='2024-painting'&&String(im.file||'').endsWith('/detail-02.jpg'))w='100%';
  let css='';
  if(w)css+=`width:${w};`+(parseFloat(w)<=100?'max-width:100%;':'max-width:none;');
  // Do not override site CSS alignment unless explicitly requested in info.md.
  if(im.align){let a=artworkAlign(im.align);css+=a==='left'?'margin-left:0;margin-right:auto;':a==='right'?'margin-left:auto;margin-right:0;':'margin-left:auto;margin-right:auto;';}
  return css;
}
let vid=videoId(work.video);
let coverMeta=(work.images||[]).find(im=>im.file===work.cover)||{};
let legacyCoverCaption=work.slug==='2018-gwangju-biennale'?'〈섬웨어 오버 더 레인보우〉 설치전경 광주비엔날레(2018)':work.slug==='2018-elegy'?'〈잔해를 위한 애가: 녹나무숲〉 큐슈예문관 설치전경(2018)':'';
let coverCaption=work.cover_caption??coverMeta.caption??legacyCoverCaption;
let coverWidth=artworkWidth(work.cover_width??coverMeta.width);
let coverAlign=work.cover_align||coverMeta.align;
let coverCss=coverWidth?`width:${coverWidth};${parseFloat(coverWidth)<=100?'max-width:100%;':'max-width:none;'}`:'';
if(coverAlign){let a=artworkAlign(coverAlign);coverCss+=a==='left'?'margin-left:0;margin-right:auto;':a==='right'?'margin-left:auto;margin-right:0;':'margin-left:auto;margin-right:auto;';}
let hero=(!vid&&work.cover)?`<figure class="hero-frame"${coverCss?` style="${coverCss}"`:''}><a href="${esc(work.cover)}" target="_blank" rel="noopener" aria-label="대표사진 확대"><img class="hero" src="${esc(work.cover)}" alt="${esc(work.title)}"></a>${coverCaption?`<figcaption>${esc(coverCaption)}</figcaption>`:''}</figure>`:'';
const photoFigure=(im,cls)=>{
  let css=imageStyle(im,cls);
  return `<figure class="work-image ${cls}"${css?` style="${css}"`:''}><a href="${esc(im.file)}" target="_blank" rel="noopener" aria-label="사진 확대"><img loading="lazy" src="${esc(im.file)}" alt="${esc(im.caption||work.title)}"></a>${im.caption?`<figcaption>${esc(im.caption)}</figcaption>`:''}</figure>`;
};'''
updated = html[:start] + replacement + html[end:]
updated = updated.replace(image_line, "editorial+=photoFigure({...im,width:block.width??im.width,align:block.align??im.align,caption:block.caption??im.caption},im.type==='installation'?'work-image--installation':'work-image--detail-single');", 1)
updated = updated.replace(pair_line, "(block.files||[]).map(f=>photoFigure({...((photoMap.get(f))||{file:f}),width:block.width??((photoMap.get(f)||{}).width),align:block.align??((photoMap.get(f)||{}).align)},'work-image--detail'))", 1)
backup = path.with_name('index.before-info-layout.html.bak')
if backup.exists():
    raise SystemExit('ERROR: Backup already exists; no changes made. Check manually.')
shutil.copy2(path,backup)
path.write_text(updated,encoding='utf-8')
print('Success: updated index.html; backup saved as index.before-info-layout.html.bak')
print('No info.md, images, works.json, or other site files modified.')
