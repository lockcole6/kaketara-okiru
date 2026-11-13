"""番号付き原稿をグレースケールWebPへ変換。原稿は変更しません。"""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image, ImageChops, ImageStat

parser=argparse.ArgumentParser()
parser.add_argument('source',type=Path,help='page-001.png〜page-016.png のあるフォルダ')
parser.add_argument('--quality',type=int,default=90)
parser.add_argument('--episode',type=int,choices=(1,2),default=1)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
target=root/'images' if args.episode==1 else root/'images/episode-02'
target.mkdir(parents=True,exist_ok=True)
pages=[]
for n in range(1,17):
    source=args.source/f'page-{n:03d}.png'
    output=target/f'page-{n:03d}.webp'
    with Image.open(source) as raw:
        gray=raw.convert('L')
        gray.save(output,format='WEBP',quality=args.quality,method=6,exact=True)
    with Image.open(output) as decoded:
        assert decoded.size==gray.size
        decoded.load()
        error=ImageStat.Stat(ImageChops.difference(gray,decoded.convert('L'))).mean[0]
    pages.append({'page':n,'file':output.relative_to(root).as_posix(),
                  'width':gray.width,'height':gray.height,
                  'bytes':output.stat().st_size,'originalBytes':source.stat().st_size,
                  'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
                  'meanAbsoluteLumaError':round(error,3)})
before=sum(p['originalBytes'] for p in pages)
after=sum(p['bytes'] for p in pages)
manifest={'title':'賭けたら起きる。','episode':'第1話 退屈な男' if args.episode==1 else '第2話 眠らない男',
          'encoding':{'format':'WebP','grayscale':True,'quality':args.quality,'resized':False},
          'originalBytes':before,'totalBytes':after,'savedPercent':round((1-after/before)*100,1),
          'pages':pages}
manifest_path=root/'pages.json' if args.episode==1 else root/'episodes/02/pages.json'
manifest_path.parent.mkdir(parents=True,exist_ok=True)
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'pages':16,'originalBytes':before,'totalBytes':after,'savedPercent':manifest['savedPercent'],'minPageBytes':min(p['bytes'] for p in pages),'maxPageBytes':max(p['bytes'] for p in pages)},ensure_ascii=False))
