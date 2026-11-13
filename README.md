# 賭けたら起きる。

第1話「退屈な男」と第2話「眠らない男」、全2話・32ページの漫画閲覧サイト。

**[目次](https://lockcole6.github.io/kaketara-okiru/)** · **[第1話を読む](https://lockcole6.github.io/kaketara-okiru/episodes/01/)** · **[第2話を読む](https://lockcole6.github.io/kaketara-okiru/episodes/02/)**

## UI

[退屈のオッズ](https://lockcole6.github.io/taikutsu-no-odds/) と同じ配色、800px幅、目次・エピソード行、縦読み、上部の固定ページ選択メニューを採用。画像はスクロールに合わせて遅延読み込みします。本文はJavaScript無効でも読めます。

- ページは上から下へ、コマは右から左へ読みます。
- ページ選択メニュー、または左右の矢印キーで移動できます。
- `episodes/01/#p15` で途中のページを直接開けます。
- 従来の `/#p15` も同じページへ転送します。
- ページ番号と末尾「1話完」を含む修正版を使用しています。

## 軽量化の比較

全16ページ・1024×1584pxの同じ原稿で比較しました。

|形式|合計容量|
|---|---:|
|元のRGB PNG|36.6MB|
|階調を保った白黒PNG|13.5MB|
|掲載中の白黒WebP・品質90|5.0MB|
|16階調に減らしたPNG・比較用|4.6MB|

白黒PNGは元画像より63.2％削減できますが、掲載中のWebPより大きくなります。16階調PNGはさらに軽くなるものの、階調が減るため掲載用には採用していません。サイトでは元の解像度と階調の見え方を維持したWebPを使用します。画像ごとの容量は `pages.json` を参照。

元のPNG、階調を保った軽量PNG、PDF、設定、過去版はローカル制作プロジェクトで保管しています。

第2話は全16ページ・1024×1536px。元PNGの48,746,388バイトから、同じ白黒WebP・品質90で6,768,954バイトへ86.1％削減しました。1ページ331,620〜496,546バイト。解像度は変更せず、元PNGは保管しています。WebPは非可逆圧縮です。詳細は `episodes/02/pages.json`。第1話の画像は変更していません。

## 更新・確認

PythonとPillowを用意して実行します。

```sh
python -m pip install Pillow
python scripts/build_images.py /path/to/numbered-png
python scripts/build_images.py /path/to/episode-02/png --episode 2
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 8000
```

`http://localhost:8000/` を開きます。画像は `pages.json` からHTMLに展開し、CSS・JavaScriptはそのまま配信する静的サイトです。GitHub Pagesは `main` ブランチのルートから公開します。

## 制作

原案と人物設定をもとに、[MangaAgentsStudio-A](https://github.com/potechitakusan/MangaAgentsStudio-A) の制作手順を参考に制作。作画と指定箇所の画像修正には内蔵imagegenを使用しています。UI参照: [lockcole6/taikutsu-no-odds](https://github.com/lockcole6/taikutsu-no-odds)。
