# BLUE COURT | Y.S.C.C.横浜 JFLサッカー応援メディア

目的は、Y.S.C.C.横浜の **サッカートップチーム（JFL）** のホームゲーム観客増加と、公式のクラブ情報・スポーツ参加への導線づくりです。横浜エクセレンス向けサイトの「試合 → 観戦ガイド → チケット → 毎日ブログ」という情報設計を参考にしています。

公開サイト: https://blue-court-yscc.onrender.com/

GitHub: https://github.com/softrenzu/ycss

公式情報:

- JFL日程・結果: https://www.jfl.or.jp/jfl-pc/view/s.php?a=2591&f=2026A001_spc.html
- Y.S.C.C.横浜: https://www.yscc1986.net/
- Y.S.C.C.公式チケット: https://ticket.yscc1986.net/
- YS-BASE: https://ys-base.yscc1986.net/

## 毎日のブログ投稿

`.github/workflows/publish.yml` は毎日 **10:10 JST頃** にGitHub Actionsを起動し、`scripts/daily_blog.py` でその日の観戦記事を１本作成、`data/posts.json` と `blog/*.html` と `sitemap.xml` をGitHubへコミットします。既存記事が同じ日にある場合は重複投稿しません。GitHub Actionsのスケジュール実行は混雑時に遅延する可能性があります。

Renderはmainへの変更で自動デプロイする設定です。毎日公開できているかどうかは、GitHub Actionsの実行履歴とRenderのデプロイ履歴の両方で確認してください。

記事内容は、サッカー観戦の魅力・チケットの買い方・スタジアムへの行き方・JFLの見どころ・クラブへの関心を高めるテーマを24本でローテーション。架空の試合結果、観客数、チケット残席、選手のコメントや募集状況は作りません。ニュース記事の自動要約や無断転載も行いません。

## サイト構成

- `index.html`: トップ・試合日程・チケット・初観戦ガイド・クラブ・FAQ。
- `styles.css`, `football.css`: モバイル対応の青・オレンジデザイン。
- `app.js`: 日程・記事の表示、最新ホーム戦の案内、記事カテゴリー切替。
- `data/matches.json`: 2026年11月13日に公式情報から確認したJFL日程（手動更新）。
- `data/posts.json`: ブログの記事・出典・日付。
- `blog/*.html`: SEOと共有に対応した独立記事ページ。
- `scripts/daily_blog.py`: 毎日記事生成・ページ再構築・sitemap更新。
- `.github/workflows/site-smoke-test.yml`: 公開先へのHTTPアクセス検証。

## 重要な運用上の注意

クラブ公式運営を装う表現は使わず、独立ファンメディアとして制作しています。公式ロゴ、写真、動画は権利確認まで転載しません。スクールの募集枠や参加条件、広告・アクセス解析連携は未設定です。

**日程は自動更新されません。** `data/matches.json` は試合の延期・中止・新日程発表に合わせて公式サイトを確認して更新してください。次のホーム戦バナーは掲載日程の範囲で自動切替し、掲載済みの最後の試合が過ぎたら非表示にして古い試合を「次回」と表示しないようにしています。

クラブの広報担当から提供される写真・募集情報・イベント告知を反映するには、提供データと使用許諾の確認が必要です。アクセス解析（GA4）や観客数実績の測定は別途設計します。

## 開発時の動作確認

```bash
python3 scripts/daily_blog.py
python3 -m http.server 8000
```

起動後に `http://localhost:8000/` を開きます。
