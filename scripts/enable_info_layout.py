#!/usr/bin/env python3
"""One-time, idempotent modification of the existing site's index.html.
Only artwork rendering rules are changed. No artwork content or other sections are rewritten.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "index.html"
html = path.read_text(encoding="utf-8")

MARKER = "/* info.md controls artwork image size, position, and captions */"
if MARKER in html:
    print("index.html already supports info.md artwork layouts")
    raise SystemExit(0)

start_key = "let vid=videoId(work.video);let hero="
end_key = "\nlet images='',queue=[];"
start = html.find(start_key)
end = html.find(end_key, start)
if start < 0 or end < 0:
    raise RuntimeError("Unknown index.html renderer; stopped without changing any file.")

replacement = r"""/* info.md controls artwork image size, position, and captions */
function layoutWidth(value) {
  let s=String(value??'').trim();
  if(!s)return '';
  if(/^\d+(?:\.\d+)?$/.test(s))s+='%';
  if(!/^\d+(?:\.\d+)?%$/.test(s))return '';
  let n=parseFloat(s);
  return (n>=10&&n<=100)?n+'%':'';
}
function imageStyle(im) {
  let width=layoutWidth(im.width);
  let align=String(im.align||'center').toLowerCase();
  if(!['left','right','center'].includes(align))align='center';
  let css=width?`width:${width};max-width:100%;`:'';
  if(align==='left')css+='margin-left:0;margin-right:auto;';
  else if(align==='right')css+='margin-left:auto;margin-right:0;';
  else css+='margin-left:auto;margin-right:auto;';
  return css;
}
let vid=videoId(work.video);
let coverMeta=(work.images||[]).find(im=>im.file===work.cover)||{};
let coverCaption=work.cover_caption||coverMeta.caption||'';
let heroWidth=layoutWidth(work.cover_width||coverMeta.width)||'100%';
let hero=(!vid&&work.cover)?
  `<figure class="hero-frame" style="width:${heroWidth};max-width:100%"><a href="${esc(work.cover)}" target="_blank" rel="noopener" aria-label="대표사진 확대"><img class="hero" src="${esc(work.cover)}" alt="${esc(work.title)}"></a>${coverCaption?`<figcaption>${esc(coverCaption)}</figcaption>`:''}</figure>`:'';
const photoFigure=(im,cls)=>{
  let css=imageStyle(im);
  return `<figure class="work-image ${cls}" style="${css}"><a href="${esc(im.file)}" target="_blank" rel="noopener" aria-label="사진 확대"><img loading="lazy" src="${esc(im.file)}" alt="${esc(im.caption||work.title)}"></a>${im.caption?`<figcaption>${esc(im.caption)}</figcaption>`:''}</figure>`;
};"""
html = html[:start] + replacement + html[end:]

# The layout blocks, not the image-list order, determine the placement and width.
old = "editorial+=photoFigure(im,im.type==='installation'?'work-image--installation':'work-image--detail-single');"
new = "editorial+=photoFigure({...im,width:block.width||im.width,align:block.align||im.align},im.type==='installation'?'work-image--installation':'work-image--detail-single');"
if html.count(old) != 1:
    raise RuntimeError("Unexpected image block implementation; stopped.")
html=html.replace(old,new,1)

old_pair = "(block.files||[]).map(f=>photoFigure(photoMap.get(f)||{file:f},'work-image--detail'))"
new_pair = "(block.files||[]).map(f=>photoFigure({...((photoMap.get(f))||{file:f}),width:block.width||((photoMap.get(f)||{}).width),align:block.align||((photoMap.get(f)||{}).align)},'work-image--detail'))"
if html.count(old_pair) != 1:
    raise RuntimeError("Unexpected paired image implementation; stopped.")
html=html.replace(old_pair,new_pair,1)

# Remove the single artwork-specific rule: width now belongs in info.md.
html=html.replace('#work-content[data-work="2018-elegy"] .hero-frame{width:72%;max-width:100%}', '')

# Keep the original HTML, CSS, navigation, CV and text archive otherwise untouched.
path.write_text(html,encoding="utf-8")
print("Patched index.html to use info.md for artwork captions, widths and alignment.")
