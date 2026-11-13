(function(){
"use strict";
var matchesUrl="./data/matches.json",postsUrl="./data/posts.json";
var league="https://www.jfl.or.jp/jfl-pc/view/s.php?a=2591&f=2026A001_spc.html";
var ticket="https://ticket.yscc1986.net/";
function el(id){return document.getElementById(id);}
function safe(value){return String(value==null?"":value).replace(/[&<>"']/g,function(ch){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch];});}
function dateToday(){var d=new Intl.DateTimeFormat("sv-SE",{timeZone:"Asia/Tokyo",year:"numeric",month:"2-digit",day:"2-digit"});return d.format(new Date());}
var toggle=el("menu-button"),mobile=el("mobile-menu");
if(toggle&&mobile){toggle.addEventListener("click",function(){var open=toggle.getAttribute("aria-expanded")==="true";toggle.setAttribute("aria-expanded",String(!open));toggle.setAttribute("aria-label",open?"メニューを開く":"メニューを閉じる");mobile.hidden=open;});mobile.querySelectorAll("a").forEach(function(a){a.addEventListener("click",function(){mobile.hidden=true;toggle.setAttribute("aria-expanded","false");});});}
function matchCard(m){
var link=isHome?(m.ticketUrl||ticket):league;
var main=isHome?(m.ticketUrl?"公式チケットへ ↗":"チケット情報を確認 ↗"):"JFL公式日程へ ↗";
return '<article class="game'+(isHome?' highlight':'')+'"><div class="game-date"><small>'+safe(m.year)+' / '+safe(m.month)+'</small><strong>'+safe(m.day)+'</strong><span>'+safe(m.weekday)+'　'+safe(m.time)+'</span></div><div class="game-info"><span class="game-label '+(isHome?"home":"")+'">'+(isHome?"● HOME GAME":"● AWAY GAME")+' / '+safe(m.round)+'</span><h3>Y.S.C.C.横浜 <span style="color:#8b9fb0;font-size:.7em">vs</span> '+safe(m.opponent)+'</h3><p>会場：'+safe(m.venue)+'</p><p>開催地：'+safe(m.city)+'</p>'+(m.ticketStatus?'<p>チケット：'+safe(m.ticketStatus)+'（クラブ公式で要確認）</p>':'')+'</div><div class="game-action"><a href="'+safe(link)+'" target="_blank" rel="noopener noreferrer">'+main+'</a><a class="secondary" href="'+league+'" target="_blank" rel="noopener noreferrer">全日程 ↗</a></div></article>';
}
if(dateToday()>"2026-11-15"){el("ticket-promo").hidden=true;el("next-home-banner").hidden=true;}
function updateNextHome(matches){
  var home=matches.find(function(m){return m.location==="HOME";});
  var banner=el("next-home-banner");
  if(!home){banner.hidden=true;return;}
  banner.hidden=false;
  var url=home.ticketUrl||ticket,month=String(Number(home.month)),day=String(Number(home.day));
  el("next-home-content").innerHTML='<div><span class="live-tag">NEXT HOME GAME</span><strong>'+safe(month)+'.'+safe(day)+' <span>'+safe(home.weekday)+' / '+safe(home.time)+' KICK OFF</span></strong><p>Y.S.C.C.横浜 <b>VS</b> '+safe(home.opponent)+'<br><small>'+safe(home.venue)+' · '+safe(home.round)+'</small></p></div><a class="btn btn-orange" target="_blank" rel="noopener noreferrer" href="'+safe(url)+'">公式チケット情報 ↗</a>';
}
fetch(matchesUrl,{cache:"no-cache"}).then(function(r){if(!r.ok)throw Error("matches");return r.json();}).then(function(data){var matches=(data.matches||[]).filter(function(m){return m.date>=dateToday();}).sort(function(a,b){return a.date.localeCompare(b.date);});el("match-list").innerHTML=matches.length?matches.slice(0,5).map(matchCard).join(""):'<div class="empty-msg">掲載中の今後の試合がありません。<a href="'+league+'" target="_blank" rel="noopener noreferrer">JFL公式日程で最新情報をご確認ください ↗</a></div>';updateNextHome(matches);}).catch(function(){el("match-list").innerHTML='<div class="empty-msg">日程の読み込みができませんでした。<a href="'+league+'" target="_blank" rel="noopener noreferrer">JFL公式日程でご確認ください ↗</a></div>';});
var allPosts=[],filter="all",limit=6;
function drawPosts(){var list=allPosts.filter(function(p){return filter==="all"||p.category===filter;});var html=list.slice(0,limit).map(function(p,i){var theme=p.visual==="PLAY"?" orange":p.visual==="CITY"?" midnight":"";return '<article class="article"><div class="article-visual'+theme+'"><small>'+safe(p.category)+' / '+safe(p.date)+'</small><strong>'+safe(p.visual||"FOOTBALL")+'</strong></div><div class="article-body"><span class="article-meta">'+safe(p.date)+' · '+safe(p.category)+'</span><h3>'+safe(p.title)+'</h3><p>'+safe(p.summary)+'</p><a href="./'+encodeURI(p.url||"blog/"+p.id+".html")+'">記事を読む ↗</a></div></article>';}).join("");el("article-list").innerHTML=html||'<p class="empty-msg">このカテゴリーの記事はまだありません。</p>';var more=el("show-more");more.hidden=list.length<=limit;}
fetch(postsUrl,{cache:"no-cache"}).then(function(r){if(!r.ok)throw Error("posts");return r.json();}).then(function(data){allPosts=(data.posts||[]).sort(function(a,b){return b.date.localeCompare(a.date)||String(b.id).localeCompare(String(a.id));});drawPosts();}).catch(function(){el("article-list").innerHTML='<p class="empty-msg">記事を読み込めませんでした。時間をおいて再度お試しください。</p>';});
document.querySelectorAll(".filter").forEach(function(b){b.addEventListener("click",function(){filter=b.getAttribute("data-cat");limit=6;document.querySelectorAll(".filter").forEach(function(x){var on=x===b;x.classList.toggle("current",on);x.setAttribute("aria-pressed",String(on));});drawPosts();});});
el("show-more").addEventListener("click",function(){limit+=6;drawPosts();});
})();
