# 賭けたら起きる。

第1話「退屈な男」全16ページの漫画閲覧サイト。

**[漫画を読む](https://lockcole6.github.io/kaketara-okiru/)**

- コマは右から左へ読みます。
- 「次のページ」または左矢印キーで進み、右矢印キーで戻ります。
- ページ番号から直接移動できます。URLの `#p15` などでページを指定できます。
- 「全ページを縦に読む」で連続表示へ切り替えられます。
- ページ番号と末尾「1話完」を含む2026年9月22日の修正版です。

## 軽量化

番号付きPNGを、グレーの階調を保った白黒WebP（品質90）に変換しています。画像は元の1024×1584pxを維持。1ページ表示では現在のページと次の1枚を読み込み、縦読みでは表示位置に合わせて読み込みます。圧縮率・各ファイルの容量は `pages.json` に記録しています。

原寸PNG・PDF・制作設定・過去版はローカルの制作プロジェクトで保管。このリポジトリには公開用画像、閲覧コード、再変換スクリプトを収録しています。

## 画像を更新する

PythonとPillowを用意し、番号付き原稿フォルダを指定します。

```sh
python -m pip install Pillow
python scripts/build_images.py /path/to/numbered-png
```

ローカルで確認する場合:

```sh
python -m http.server 8000
```

`http://localhost:8000/` を開きます。GitHub Pagesは `main` ブランチのルートから公開します。更新をpushすると反映されます。

## 制作

原案と人物設定をもとに、[MangaAgentsStudio-A](https://github.com/potechitakusan/MangaAgentsStudio-A) の制作手順を参考に制作。作画と指定箇所の画像修正には内蔵imagegenを使用しています。
