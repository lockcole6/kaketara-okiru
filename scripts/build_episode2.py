"""第1話の既存UIを保ち、第2話と前後話リンクを生成する。build_site.pyから呼ぶ。"""
from pathlib import Path
import json, re
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'episodes/02/pages.json').read_text(encoding='utf-8'))
pages=data['pages']
assert [p['page'] for p in pages]==list(range(1,17))
first=root/'episodes/01/index.html'
base=first.read_text(encoding='utf-8')
second=base.replace('第1話','第2話').replace('退屈な男','眠らない男')
figures=[]
for p in pages:
    n=p['page']; loading='fetchpriority="high"' if n==1 else 'loading="lazy"'
    figures.append(f'<figure id="p{n}"><img src="../../{p["file"]}?v={p["sha256"][:12]}" width="{p["width"]}" height="{p["height"]}" alt="賭けたら起きる。 第2話 {n}ページ" {loading} decoding="async"><figcaption>{n} / 16</figcaption></figure>')
second=re.sub(r'<main class="pages">.*?</main>','<main class="pages">'+'\n'.join(figures)+'</main>',second,flags=re.S)
second=second.replace('<div class="links">','<div class="links"><a href="../01/">‹ 前の話へ</a>')
second=second.replace('<p>第2話 了</p>','<p>第2話 了</p><a class="btn" href="../01/">‹ 第1話へ</a>')
(root/'episodes/02/index.html').write_text(second,encoding='utf-8',newline='\n')
base=base.replace('<div class="links">','<div class="links"><a href="../02/">次の話へ ›</a>')
base=base.replace('<p>第1話 了</p>','<p>第1話 了</p><a class="btn primary" href="../02/">第2話を読む ›</a>')
first.write_text(base,encoding='utf-8',newline='\n')
index=(root/'index.html').read_text(encoding='utf-8')
index=index.replace('全1話 ／ 全16ページ','全2話 ／ 全32ページ')
index=index.replace('第1話『退屈な男』。全16ページ。','全2話・32ページ。第2話『眠らない男』公開中。')
index=index.replace('href="episodes/01/">最新話を読む','href="episodes/02/">最新話を読む')
cover=pages[0]
row=f'<a class="row" href="episodes/02/"><img width="{cover["width"]}" height="{cover["height"]}" class="thumb" src="{cover["file"]}?v={cover["sha256"][:12]}" alt="" loading="lazy" decoding="async"><div><small>第2話</small><h3>眠らない男</h3><p>脱・会社員計画、始動。調べるほど、夜が短くなる。</p></div><span class="arrow" aria-hidden="true">›</span></a>'
index=index.replace('</main>',row+'</main>')
(root/'index.html').write_text(index,encoding='utf-8',newline='\n')
print('第2話16ページ・全2話の目次・前後話リンクを追加しました')
