#!/usr/bin/env python3
"""BLUE COURT daily original JFL football attendance guides and static pages.

No unverified news, scores, attendance, availability or match results.
Standard library only. Safe to rerun, one additional tip per JST calendar day.
"""
from __future__ import annotations
import html
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT
POSTS = SITE / "data" / "posts.json"
ARTICLES = SITE / "blog"
BASE = "https://blue-court-yscc.onrender.com/"
OFFICIAL = "https://www.yscc1986.net/"
TICKET = "https://ticket.yscc1986.net/"
JFL = "https://www.jfl.or.jp/jfl-pc/view/s.php?a=2591&f=2026A001_spc.html"

# Rotating reader-first editorial calendar. Never invent scores, lineup, prices or breaking news.
TIPS = [
    ("観戦ガイド", "最初に会場名をチェックしよう", "横浜開催でもスタジアムは一つではありません。", "Y.S.C.C.横浜のホームゲームには保土ケ谷公園サッカー場やニッパツ三ツ沢球技場の開催があります。日程表の対戦相手だけではなく、会場名と所在地まで確認して、移動先を間違えないようにしましょう。"),
    ("観戦ガイド", "キックオフより少し前に到着する理由", "スタジアムでの時間を楽しむ準備も観戦の一部。", "初めての場所では、駅からの移動や入場の列に予想以上の時間がかかることがあります。開場時間は試合ごとに公式発表を確認し、座席を探す時間や飲み物を準備する時間も含めて予定を立てましょう。"),
    ("観戦ガイド", "スマホのQRチケットを準備する", "入場直前に慌てないための小さな習慣。", "Y.S.C.C.公式チケットサイトで購入した電子チケットはQRコードを画面に出して入場する方式です。スクリーンショットでの入場は利用規約上できないため、通信環境とバッテリーを確認し、公式案内どおりに表示しましょう。"),
    ("観戦ガイド", "親子で初めてのサッカー観戦", "子どもと行くならチケット条件の確認から。", "小中高生の料金区分や未就学児の扱いは試合の公式販売ページで確認しましょう。天気や気温に合わせた服装、飲み物、移動経路を準備しておけば、試合前の時間も家族で楽しみやすくなります。"),
    ("観戦ガイド", "ホームとアウェーを見分けよう", "試合日が同じでも観戦できる場所は異なります。", "HOMEはY.S.C.C.横浜が主催する試合、AWAYは相手クラブのホームで行う試合です。旅先でのアウェー観戦も楽しいですが、初めてなら横浜開催のホームゲームからチェックするのがおすすめです。"),
    ("観戦ガイド", "ゴール前の攻防を見てみよう", "サッカーの見どころは得点の瞬間だけではありません。", "シュートに至る直前の動き、味方へのパス、相手のブロック、ゴールキーパーの判断。ほんの数秒に多くのプレーが詰まっています。初観戦ではボールのある場所だけ追っても十分楽しめます。"),
    ("観戦ガイド", "ボールのない場所にも注目", "ピッチ全体を見るとチャンスが生まれる理由が見える。", "サッカーは11人制。ボールを持つ選手以外も、走り込んでパスの道をつくったり、守備の位置を調整したりしています。少し余裕が出てきたら、ボールから離れた選手の動きを追ってみましょう。"),
    ("観戦ガイド", "守備が攻撃に変わる瞬間", "ボールを奪った直後は一気に動きます。", "守備で粘り強くボールを奪ってから、前方の味方へパスを送る数秒間は見どころのひとつです。スタジアムではピッチ全体が見えるので、ボールを奪う前の選手の立ち位置にも目を向けてみてください。"),
    ("観戦ガイド", "初観戦の服装と持ち物", "屋外スタジアムだからこそ準備しておきたいこと。", "天気予報、体感温度、座席の位置を考えて服装を選びましょう。スマートフォン、チケット、モバイルバッテリー、飲み物などを出発前にチェック。持ち込みや応援ルールは必ず開催試合の公式案内を優先してください。"),
    ("観戦ガイド", "一人観戦にもチャレンジしてみる", "サッカーは一人でも自分のペースで楽しめます。", "気になった試合を決め、行き方とチケットを確認してスタジアムへ。周囲に合わせて無理に大きな声を出す必要はありません。プレーに集中して拍手を送るだけでも、地元クラブの応援の一歩になります。"),
    ("観戦ガイド", "友人を誘うための３つの情報", "サッカーに詳しくない友人も誘いやすく。", "試合の日付と開始時刻、会場までの行き方、チケットの購入先。この３つをメッセージに書くだけで、誘われた相手も予定を判断しやすくなります。集合場所は駅なのか会場入口なのかを決めておくと安心です。"),
    ("観戦ガイド", "週末の予定にサッカーを入れる", "遠くの旅行でなくても非日常は近所にあります。", "横浜市内で開催されるホームゲームなら、午前中に街で過ごしてからスタジアムへ向かう計画も立てられます。キックオフ時刻と最寄りの交通機関を先に確認して、無理のない一日にしましょう。"),
    ("横浜の街", "保土ケ谷のサッカー場を知ろう", "11月にホームゲームがある保土ケ谷公園。", "県立保土ケ谷公園サッカー場は横浜市保土ケ谷区花見台にあります。スタジアムは屋外の天然芝。バス停から公園内を移動する時間も考え、アクセス方法は保土ケ谷公園公式の最新情報を確認しておきましょう。"),
    ("横浜の街", "三ツ沢でサッカーを観る一日", "横浜駅から行きやすいニッパツ三ツ沢球技場。", "ニッパツ三ツ沢球技場は横浜市神奈川区三ツ沢西町にある球技場です。横浜駅方面からのバス、三ツ沢上町駅からの徒歩などのアクセスがあります。試合前にスタジアム名と交通ルートをチェックしておきましょう。"),
    ("観戦ガイド", "試合前に知りたいJFLのこと", "Y.S.C.C.横浜は日本フットボールリーグで戦っています。", "JFLは全国のクラブが参加する11人制サッカーのリーグです。チームごとにホームタウンと特色があり、地域を背負った対戦が続きます。試合日程や順位・結果の確認は日本フットボールリーグ公式サイトから。"),
    ("クラブを知る", "横浜のクラブを応援する楽しさ", "身近な街に、応援できるサッカーチームがある。", "Y.S.C.C.横浜は横浜に根ざすサッカークラブ。名前やエンブレムだけでなく、選手の取り組み、地域活動に少しずつ目を向けてみましょう。クラブの最新情報や活動の詳細は公式サイトで知ることができます。"),
    ("クラブを知る", "1986年から続くY.S.C.C.の歩み", "クラブの歴史を知ると応援が少し深まります。", "Y.S.C.C.は1986年に始まった横浜のスポーツクラブです。サッカーのトップチームはJFLで戦いながら、横浜のスポーツ文化とつながっています。過去の歩みや現在の選手たちについて、クラブ公式の紹介を読んでみませんか。"),
    ("クラブを知る", "YS-BASEというもう一つの入口", "自分でボールを蹴る楽しさにも出会える。", "Y.S.C.C.が運営するYS-BASEは、横浜市瀬谷区の天然芝サッカー施設です。試合を観る楽しさと、実際にサッカーを楽しむ時間はつながっています。利用条件や空き状況はYS-BASE公式の予約ページで確かめてください。"),
    ("観戦ガイド", "注目したいサイドからの攻撃", "タッチライン沿いの動きにもチャンスがある。", "サイドの選手が前へ運び、味方にパスを通すことでゴール前にチャンスが生まれることがあります。スタジアムでピッチ全体を見渡しながら、ボールがどこからゴールに近づいていくか追ってみましょう。"),
    ("観戦ガイド", "セットプレーの楽しみ方", "コーナーキックやフリーキックにも注目。", "プレーが一度止まり、選手たちが立ち位置を工夫するセットプレー。キッカーが助走を始める前に、ゴール前で選手がどう動いているか観察してみると、違った面白さが見えてきます。"),
    ("観戦ガイド", "観戦後は次の試合を探そう", "１試合の経験が次の週末を楽しみにしてくれます。", "初めて観戦したら、次に行けそうなホームゲームを公式日程で探してみましょう。同じ相手との対戦でも、試合の展開は毎回違います。友人や家族を誘ってみるのもひとつの楽しみ方です。"),
    ("観戦ガイド", "選手名を知らなくても大丈夫", "好きなプレーから選手を覚えてみましょう。", "最初から全選手を覚えていなくても問題ありません。ゴールキーパーのセーブ、パスの出し手、守備で粘る選手など、心に残ったプレーから気になる選手を見つけ、公式の選手紹介で名前を確認してみてください。"),
    ("観戦ガイド", "写真を撮る前に確認したいこと", "思い出を残すときも周りへの配慮を。", "観戦中の撮影は、主催者が発表する撮影ルールに従う必要があります。隣の席の人の視界を遮ったり、通路をふさいだりしないようにしましょう。選手や周りの観客のプライバシーにも配慮して楽しみたいですね。"),
    ("横浜の街", "横浜の近場でスポーツ観戦", "身近な場所で新しい週末の楽しみを探そう。", "サッカー観戦は、特別な旅行をしなくても楽しめる週末のイベントです。日程とアクセスを調べ、前後の食事や街歩きも含めて予定を立ててみてください。ホームゲームの正式な会場は日程ごとに異なるため公式情報を確認しましょう。")
]

def escape(value: object) -> str:
    return html.escape(str(value), quote=True)

def now_jst() -> str:
    override = os.environ.get("BLOG_DATE")
    if override:
        return datetime.strptime(override, "%Y-%m-%d").date().isoformat()
    return datetime.now(ZoneInfo("Asia/Tokyo")).date().isoformat()

def page(post: dict) -> str:
    title = escape(post["title"])
    summary = escape(post["summary"])
    published = escape(post["date"])
    url = BASE + quote("blog/" + post["id"] + ".html")
    body = "\n".join("<p>" + escape(p) + "</p>" for p in post.get("body", []))
    links = []
    for source in post.get("sources", []):
        source_url = str(source.get("url", ""))
        if source_url.startswith("https://"):
            links.append('<a href="' + escape(source_url) + '" target="_blank" rel="noopener noreferrer">' + escape(source.get("label", "公式情報")) + " ↗</a>")
    if not links:
        links = ['<a href="' + OFFICIAL + '" target="_blank" rel="noopener noreferrer">Y.S.C.C.横浜サッカー公式 ↗</a>',
                 '<a href="' + JFL + '" target="_blank" rel="noopener noreferrer">JFL公式日程 ↗</a>',
                 '<a href="' + TICKET + '" target="_blank" rel="noopener noreferrer">Y.S.C.C.公式チケット ↗</a>']
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{summary}"><meta property="og:title" content="{title} | BLUE COURT"><meta property="og:description" content="{summary}">
<link rel="canonical" href="{escape(url)}"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../styles.css">
<title>{title} | BLUE COURT</title>
<style>.post-hero{{background:#081b36;color:#fff;padding:85px 0 76px}}.post-hero a{{color:#ff9e77;font-weight:800;font-size:12px}}.post-hero h1{{font-size:clamp(29px,5vw,53px);line-height:1.4;letter-spacing:-.06em;max-width:850px}}.post-meta{{font-weight:800;font-size:12px;letter-spacing:.07em;color:#b7d0e7}}.post-content{{max-width:800px;margin:auto;padding:60px 24px 100px}}.post-content p{{font-size:16px;line-height:2.2;margin:0 0 30px}}.post-sources{{border-top:1px solid #d9e2ee;margin-top:50px;padding-top:25px}}.post-sources a{{display:inline-block;padding:10px 14px;background:#f2f6fb;color:#105bab;margin:5px;font-weight:800;font-size:12px}}.post-back{{display:inline-block;margin-top:45px;font-size:13px;font-weight:800;color:#105bab}}</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BlogPosting","headline":{json.dumps(post["title"], ensure_ascii=False)},"datePublished":{json.dumps(post["date"])},"description":{json.dumps(post["summary"], ensure_ascii=False)},"mainEntityOfPage":{json.dumps(url)}}}</script>
</head><body><header class="header"><div class="wrap header-inner"><a class="brand" href="../"><span class="brand-symbol"><span class="brand-ball"></span></span><span class="brand-name"><b>BLUE<span>COURT</span><i>.</i></b><small>Y.S.C.C. YOKOHAMA FOOTBALL FAN MEDIA</small></span></a><a class="header-cta" href="../#journal">記事一覧へ ↗</a></div></header>
<main><section class="post-hero"><div class="wrap"><a href="../#journal">← BLUE COURT JOURNAL</a><p class="post-meta">{published} ／ {escape(post["category"])}</p><h1>{title}</h1><p>{summary}</p></div></section><article class="post-content">{body}<div class="post-sources"><h2>関連する公式情報</h2>{''.join(links)}<p style="font-size:12px;color:#607388">※ BLUE COURTは非公式ファンメディアです。試合日程・料金・募集内容は公式サイトで最新情報をご確認ください。</p></div><a class="post-back" href="../#journal">← 記事一覧へ戻る</a></article></main>
<footer class="footer"><div class="wrap"><a class="footer-brand" href="../">BLUE COURT<span>.</span></a><p>JFL・Y.S.C.C.横浜サッカー独立観戦メディア。クラブ公式サイトではありません。</p></div></footer></body></html>'''

def generate() -> None:
    data = json.loads(POSTS.read_text(encoding="utf-8"))
    posts = data.get("posts", [])
    today = now_jst()
    if not any(p.get("date") == today and p.get("autoGenerated") for p in posts):
        # No new automatic post on days already covered by manually curated content.
        if not any(p.get("date") == today for p in posts):
            base = datetime.strptime(today, "%Y-%m-%d").date().toordinal()
            category, title, summary, tip = TIPS[base % len(TIPS)]
            posts.insert(0, {
                "id": today + "-daily-football",
                "date": today,
                "category": category,
                "visual": "DAILY",
                "title": datetime.strptime(today, "%Y-%m-%d").strftime("%Y年%m月%d日") + "のYSCC観戦ノート｜" + title,
                "summary": summary,
                "body": [summary, tip, "次の週末に行ける試合がないか、JFL公式日程とY.S.C.C.公式チケットサイトをチェックしてみましょう。開催情報や販売条件は公式の最新情報が優先です。"],
                "sources": [
                    {"label": "JFL公式 試合日程", "url": JFL},
                    {"label": "Y.S.C.C.公式チケット", "url": TICKET}
                ],
                "autoGenerated": True
            })
    ids = set()
    ARTICLES.mkdir(exist_ok=True)
    posts = sorted(posts, key=lambda x: (x["date"], x["id"]), reverse=True)
    for post in posts:
        name = post["id"]
        if not all(ch.isascii() and (ch.isalnum() or ch in "-_") for ch in name):
            raise ValueError("invalid article id: " + name)
        if name in ids:
            raise ValueError("duplicate id: " + name)
        ids.add(name)
        post["url"] = "blog/" + name + ".html"
        (ARTICLES / (name + ".html")).write_text(page(post), encoding="utf-8")
    POSTS.write_text(json.dumps({"posts": posts}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Render's existing build command copies a fixed legacy asset list. Stage the
    # football-specific stylesheet in its publish directory before that copy.
    publish_dir = SITE / "public"
    publish_dir.mkdir(exist_ok=True)
    shutil.copyfile(SITE / "football.css", publish_dir / "football.css")
    urls = [(BASE, today)] + [(BASE + "blog/" + p["id"] + ".html", p["date"]) for p in posts]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, changed in urls:
        xml += "<url><loc>" + escape(url) + "</loc><lastmod>" + changed + "</lastmod></url>\n"
    xml += "</urlset>\n"
    (SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("BLUE COURT: " + str(len(posts)) + " articles built; latest " + today)

if __name__ == "__main__":
    generate()
