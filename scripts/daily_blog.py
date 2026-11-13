#!/usr/bin/env python3
"""BLUE COURT daily original evergreen futsal tips and static post pages.

No unverified news, scores, attendance, availability or match results.
Standard library only. Safe to rerun, one additional tip per JST calendar day.
"""
from __future__ import annotations
import html
import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT
POSTS = SITE / "data" / "posts.json"
ARTICLES = SITE / "blog"
BASE = "https://softrenzu.github.io/ycss/"
OFFICIAL = "https://ysccfutsal.jp/"
TICKET = "https://more.tiget.net/events/10287"

# Editorial calendar: evergreen tips only, not fabricated match reports.
TIPS = [
    ("観戦ガイド", "試合の会場名を最初に確認しよう", "同じクラブの試合でも、会場が違うことがあります。", "試合の日付と開始時刻に加えて、アリーナ名までメモしておきましょう。交通機関は開催地で変わります。"),
    ("観戦ガイド", "初めての観戦は、余裕を持った到着を", "試合前の移動時間も大事な準備。", "公式発表の開場時刻と開始時刻を確認しましょう。チケットの表示方法や持ち物も早めにチェック。"),
    ("観戦ガイド", "５人制ならではのスピード感", "フットサルは攻守の切り替えに注目。", "一度ボールを奪うとあっという間にゴール前へ。得点直前のパスにも注目すると面白さが増します。"),
    ("プレーする", "選手と蹴れるYS個サルをチェック", "初めての個サルでも、公式の参加案内から確認できます。", "YS個サルの開催日・費用・予約方法は公式と開催施設の最新ページを必ず確認してください。"),
    ("観戦ガイド", "ボールを持っていない選手にも注目", "パスコースを作る動きに、戦術のヒントがある。", "ボールを追うだけでなく、スペースへ走る選手や味方のために動く選手を見てみましょう。"),
    ("観戦ガイド", "観戦で一番盛り上がる瞬間を探そう", "シュートの瞬間だけでなく、ボール奪取も見どころ。", "攻守の切り替わり、キーパーの判断、パスの連続など、自分の好きな場面を見つけると次の観戦が楽しみになります。"),
    ("観戦ガイド", "子どもと観戦するときの事前確認", "家族観戦はチケット条件と会場ルールの確認から。", "子どもの料金区分、座席の条件、持ち込み品や入場時間などは公式販売案内で確認してください。"),
    ("プレーする", "フットサルの育成カテゴリーを調べてみよう", "U-18・U-22など、競技を続けたい人の選択肢。", "体験や入団の条件は時期により変わります。クラブ公式のアカデミー案内から問い合わせましょう。"),
    ("観戦ガイド", "試合前に知っておきたいパスの見どころ", "小さなスペースを生かす連携に注目。", "選手が相手の背後に動く瞬間や、細かなパス交換から生まれるチャンスを探してみてください。"),
    ("観戦ガイド", "ホームとアウェーを見分ける", "Y.S.C.C.横浜の試合でも県外開催があります。", "日程表のHOME・AWAYと開催地を見て、行きたい試合の場所を確認しましょう。"),
    ("観戦ガイド", "観戦後に次の試合を探す", "初めての１試合を次の週末の楽しみに。", "興味が深まったら、Fリーグの公式日程を見て次の対戦相手や開催会場を確認してみましょう。"),
    ("観戦ガイド", "初観戦の持ち物をチェック", "スマートフォン、チケット、交通手段を前日に確認。", "電子チケットは表示できるようにしておき、会場ごとの手荷物ルールや場内案内も事前に確認しましょう。")
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
        links = ['<a href="' + OFFICIAL + '" target="_blank" rel="noopener noreferrer">Y.S.C.C.横浜フットサル公式 ↗</a>',
                 '<a href="https://www.fleague.jp/club/yokohama/schedule.html" target="_blank" rel="noopener noreferrer">Fリーグ公式日程 ↗</a>']
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{summary}"><meta property="og:title" content="{title} | BLUE COURT"><meta property="og:description" content="{summary}">
<link rel="canonical" href="{escape(url)}"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../styles.css">
<title>{title} | BLUE COURT</title>
<style>.post-hero{{background:#081b36;color:#fff;padding:85px 0 76px}}.post-hero a{{color:#ff9e77;font-weight:800;font-size:12px}}.post-hero h1{{font-size:clamp(29px,5vw,53px);line-height:1.4;letter-spacing:-.06em;max-width:850px}}.post-meta{{font-weight:800;font-size:12px;letter-spacing:.07em;color:#b7d0e7}}.post-content{{max-width:800px;margin:auto;padding:60px 24px 100px}}.post-content p{{font-size:16px;line-height:2.2;margin:0 0 30px}}.post-sources{{border-top:1px solid #d9e2ee;margin-top:50px;padding-top:25px}}.post-sources a{{display:inline-block;padding:10px 14px;background:#f2f6fb;color:#105bab;margin:5px;font-weight:800;font-size:12px}}.post-back{{display:inline-block;margin-top:45px;font-size:13px;font-weight:800;color:#105bab}}</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BlogPosting","headline":{json.dumps(post["title"], ensure_ascii=False)},"datePublished":{json.dumps(post["date"])},"description":{json.dumps(post["summary"], ensure_ascii=False)},"mainEntityOfPage":{json.dumps(url)}}}</script>
</head><body><header class="header"><div class="wrap header-inner"><a class="brand" href="../"><span class="brand-symbol"><span class="brand-ball"></span></span><span class="brand-name"><b>BLUE<span>COURT</span><i>.</i></b><small>YOKOHAMA FUTSAL FAN GUIDE</small></span></a><a class="header-cta" href="../#journal">記事一覧へ ↗</a></div></header>
<main><section class="post-hero"><div class="wrap"><a href="../#journal">← BLUE COURT JOURNAL</a><p class="post-meta">{published} ／ {escape(post["category"])}</p><h1>{title}</h1><p>{summary}</p></div></section><article class="post-content">{body}<div class="post-sources"><h2>関連する公式情報</h2>{''.join(links)}<p style="font-size:12px;color:#607388">※ BLUE COURTは非公式ファンメディアです。試合日程・料金・募集内容は公式サイトで最新情報をご確認ください。</p></div><a class="post-back" href="../#journal">← 記事一覧へ戻る</a></article></main>
<footer class="footer"><div class="wrap"><a class="footer-brand" href="../">BLUE COURT<span>.</span></a><p>Y.S.C.C.横浜フットサル独立観戦ガイド。クラブ公式サイトではありません。</p></div></footer></body></html>'''

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
                "id": today + "-daily-futsal",
                "date": today,
                "category": category,
                "visual": "DAILY",
                "title": today.replace("-", "年", 1).replace("-", "月", 1) + "日の観戦ノート｜" + title,
                "summary": summary,
                "body": [summary, tip, "公式日程・会場・参加条件は必ずクラブ・リーグ公式サイトで確認してください。"],
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
    urls = [(BASE, today)] + [(BASE + "blog/" + p["id"] + ".html", p["date"]) for p in posts]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, changed in urls:
        xml += "<url><loc>" + escape(url) + "</loc><lastmod>" + changed + "</lastmod></url>\n"
    xml += "</urlset>\n"
    (SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("BLUE COURT: " + str(len(posts)) + " articles built; latest " + today)

if __name__ == "__main__":
    generate()
