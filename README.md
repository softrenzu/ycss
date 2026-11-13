# BLUE COURT

Y.S.C.C.横浜フットサルの観戦者増加・新規ファン獲得・個サルや育成カテゴリーへの誘導を目的とした独立ファンガイドです。横浜エクセレンス向け「GREEN SIDE」の設計思想を参考に、YSCC向けに独立した新規コードで制作しました。

- 公開サイト: https://blue-court-yscc.onrender.com/
- Repository: https://github.com/softrenzu/ycss
- GitHub Pages URL: https://softrenzu.github.io/ycss/
- Club official: https://ysccfutsal.jp/
- F.League fixture list: https://www.fleague.jp/club/yokohama/schedule.html
- Official home ticket sales: https://more.tiget.net/events/10287
- YS個サル: https://ysccfutsal.jp/yskosal/
- Academy: https://ysccfutsal.jp/academy/

## 公開状況

Render静的サイトとして公開済み（GitHub mainブランチ更新時に自動デプロイ）。GitHub Pagesは別途有効化する場合のミラーとして下記参照。

## GitHub Pages初回公開

リポジトリはpublicです。GitHub Pagesが未有効の場合、Webの公開にはGitHubのUIで次の設定が1回だけ必要です。

1. [Settings > Pages](https://github.com/softrenzu/ycss/settings/pages)を開く。
2. Build and deployment > Source を GitHub Actions に切り替える。
3. [Actions > Publish BLUE COURT and daily journal](https://github.com/softrenzu/ycss/actions/workflows/publish.yml) から Run workflow を実行する。
4. ワークフローの緑色の成功表示を確認し、公開URLを開いてください。

注: GitHub Pagesはコードをpushしただけでは必ずしも自動で有効になりません。GitHub標準トークンだけで新しいPages設定を作成できないため、手動の初回有効化が必要な場合があります。

## 構成

- index.html: ホームページ、リンクとFAQ。
- styles.css: レスポンシブのブルー／オレンジデザイン。
- app.js: JSONの日程・記事表示、記事フィルター、スマホメニュー。
- data/matches.json: 手動で確認した2026-27試合日程（更新情報は必ず公式照合）。
- data/posts.json: 記事本文とメタデータ。
- blog/*.html: scripts/daily_blog.pyが生成するSEO対応記事ページ。
- scripts/daily_blog.py: JST日付で最大1記事/日の独自の観戦ヒントを生成し、個別HTMLとサイトマップを書き出す。既存記事と重複しない。
- .github/workflows/publish.yml: push時と毎日10:00 JST頃に記事生成・GitHub Pages公開。
- sitemap.xml: 記事別URLを自動登録。

## 運用と注意

観客導線は「検索 / 記事 → 観戦日程 → 公式チケット」、参加導線は「記事 → YS個サル / アカデミー公式ページ」です。

日程とチケットの掲載データは2026年11月13日の公式情報に基づきます。自動ブログは時事ニュースではなく一般的な観戦のヒントであり、架空の結果・スコア・選手コメント・空席状況などを生成しません。試合日程は自動収集しません。最新のFリーグ公式情報に照合して、data/matches.jsonを更新してください。

実際の来場数や申込み数の成果測定にはクラブ側との連携が必要です。GA4や広告タグは設定していません。クラブ公式・スポンサー公認サイトを示唆する表現は使わず、掲載写真・ロゴの権利確認が済むまで流用しません。

## ローカル確認

python -m http.server 8000 で起動して http://localhost:8000 を開きます。記事生成は python scripts/daily_blog.py。
