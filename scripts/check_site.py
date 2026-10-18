"""公開前の参照・画像同一性・静的本文・ページ選択を確認する。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json

root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=[];self.images=[];self.options=[]
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if 'id' in data:self.ids.append(data['id'])
        if tag=='img':self.images.append(data)
        if tag=='option':self.options.append(data.get('value'))
        for k in ('href','src'):
            if k in data:self.refs.append(data[k])
def read(path):
    page=Page();page.feed(path.read_text(encoding='utf-8'));return page
for filename in ['index.html','episodes/01/index.html']:
    path=root/filename;page=read(path)
    for ref in page.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc:continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        if target.is_dir():target=target/'index.html'
        assert target.is_relative_to(root) and target.is_file(),ref
        if url.fragment and target.suffix=='.html':assert url.fragment in read(target).ids,ref
episode=read(root/'episodes/01/index.html')
assert episode.options==[str(n) for n in range(1,17)]
assert [i for i in episode.ids if i.startswith('p')]==[f'p{n}' for n in range(1,17)]
assert len(episode.images)==16
assert episode.images[0]['fetchpriority']=='high'
assert all(p.get('loading')=='lazy' for p in episode.images[1:])
manifest=json.loads((root/'pages.json').read_text(encoding='utf-8'))
for p in manifest['pages']:
    assert hashlib.sha256((root/p['file']).read_bytes()).hexdigest()==p['sha256']
print('OK: 目次・縦読み16ページ・全参照・画像同一性・遅延読み込み・ページ選択')
