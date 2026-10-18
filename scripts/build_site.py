"""ページ目録から目次と縦読みHTMLを生成する。"""
from pathlib import Path
import json,hashlib,html

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'pages.json').read_text(encoding='utf-8'))
pages=manifest['pages']
assert [p['page'] for p in pages]==list(range(1,17))
title=html.escape(manifest['title'])
subtitle='第1話「退屈な男」'
version=lambda file:hashlib.sha256((root/file).read_bytes()).hexdigest()[:12]
css_version=version('styles.css')
reader_version=version('reader.js')
landing_version=version('landing.js')
cover=pages[0]
common_footer='創作漫画です。人物・出来事は架空です。AIを用いて制作しています。'
index=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#1c201f"><meta name="description" content="漫画『賭けたら起きる。』第1話『退屈な男』。全16ページ。"><title>{title}｜漫画</title><link rel="stylesheet" href="styles.css?v={css_version}"><script src="landing.js?v={landing_version}" defer></script></head>
<body><header class="head wrap"><a class="brand" href="https://lockcole6.github.io/">LOCKCOLE WORKS</a><a href="https://lockcole6.github.io/#manga">作品一覧へ ↗</a></header>
<main class="wrap"><section class="intro"><small>全1話 ／ 全16ページ</small><h1>{title}</h1><p>退屈な毎日を送る男が、賭けをきっかけに目を覚ます。</p><div class="actions"><a class="btn primary" href="episodes/01/">第1話から読む</a><a class="btn" href="episodes/01/">最新話を読む</a></div></section>
<h2 class="heading">エピソード</h2><a class="row" href="episodes/01/"><img width="{cover['width']}" height="{cover['height']}" class="thumb" src="{cover['file']}?v={cover['sha256'][:12]}" alt="" loading="lazy" decoding="async"><div><small>第1話</small><h3>退屈な男</h3><p>眠たい毎日。缶ジュース一本で、世界が変わる。</p></div><span class="arrow" aria-hidden="true">›</span></a></main>
<footer class="wrap">{common_footer}<br>© LOCKCOLE WORKS</footer></body></html>
'''
options=''.join(f'<option value="{p["page"]}">{p["page"]} / {len(pages)}</option>' for p in pages)
figures=[]
for p in pages:
    n=p['page'];loading='fetchpriority="high"' if n==1 else 'loading="lazy"'
    ending='、1話完' if n==16 else ''
    figures.append(f'<figure id="p{n}"><img src="../../{p["file"]}?v={p["sha256"][:12]}" width="{p["width"]}" height="{p["height"]}" alt="{title} 第1話 {n}ページ{ending}" {loading} decoding="async"><figcaption>{n} / {len(pages)}</figcaption></figure>')
body='\n'.join(figures)
episode=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#1c201f"><title>{subtitle}｜{title}</title><link rel="stylesheet" href="../../styles.css?v={css_version}"></head>
<body class="reader"><a class="skip" href="#p1">本文へ</a><header class="reader-head wrap"><a href="../../index.html">‹ 目次</a><h1>{subtitle}</h1><span class="muted">{title}</span></header>
<nav class="wrap readerbar" aria-label="話とページ"><label>ページ <select id="jump" aria-label="表示ページ">{options}</select></label><div class="links"><a href="../../index.html">目次へ</a></div></nav>
<main class="pages">{body}</main>
<section class="reader-end"><p>第1話 了</p><a class="btn" href="../../index.html">目次へ戻る</a><a class="btn" href="#p1">この話の最初へ</a></section>
<footer class="wrap">{common_footer}</footer><script src="../../reader.js?v={reader_version}"></script></body></html>
'''
(root/'index.html').write_text(index,encoding='utf-8',newline='\n')
folder=root/'episodes/01';folder.mkdir(parents=True,exist_ok=True)
(folder/'index.html').write_text(episode,encoding='utf-8',newline='\n')
print('目次・第1話の縦読みHTMLを生成しました（16ページ）')
