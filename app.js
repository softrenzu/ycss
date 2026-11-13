(function(){
"use strict";
var matchesUrl="./data/matches.json",postsUrl="./data/posts.json";
var league="https://www.fleague.jp/club/yokohama/schedule.html";
var ticket="https://more.tiget.net/events/10287";
function el(id){return document.getElementById(id);}
function safe(value){return String(value==null?"":value).replace(/[&<>"']/g,function(ch){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch];});}
function dateToday(){var d=new Intl.DateTimeFormat("sv-SE",{timeZone:"Asia/Tokyo",year:"numeric",month:"2-digit",day:"2-digit"});return d.format(new Date());}
var toggle=el("menu-button"),mobile=el("mobile-menu");
if(toggle&&mobile){toggle.addEventListener("click",function(){var open=toggle.getAttribute("aria-expanded")==="true";toggle.setAttribute("aria-expanded",String(!open));toggle.setAttribute("aria-label",open?"メニューを開く":"メニューを閉じる");mobile.hidden=open;});mobile.querySelectorAll("a").forEach(function(a){a.addEventListener("click",function(){mobile.hidden=true;toggle.setAttribute("aria-expanded","false");});});}
function matchCard(m){
var isHome=m.location==="HOME",link=isHome&&m.ticketUrl?m.ticketUrl:league;
var main=isHome&&m.ticketUrl?"チケットを確認 ↗":"公式日程を確認 ↗";
return '<article class="game'+(isHome?' highlight':'')+'"><div class="game-date"><small>'+safe(m.year)+' / '+safe(m.month)+'</small><strong>'+safe(m.day)+'</strong><span>'+safe(m.weekday)+'　'+safe(m.time)+'</span></div><div class="game-info"><span class="game-label '+(isHome?"home":"")+'">'+(isHome?"● HOME GAME":"● AWAY GAME")+' / '+safe(m.round)+'</span><h3>Y.S.C.C.横浜 <span style="color:#8b9fb0;font-size:.7em">vs</span> '+safe(m.opponent)+'</h3><p>会場：'+safe(m.venue)+'</p><p>開催地：'+safe(m.city)+'</p></div><div class="game-action"><a href="'+safe(link)+'" target="_blank" rel="noopener noreferrer">'+main+'</a><a class="secondary" href="'+league+'" target="_blank" rel="noopener noreferrer">全日程 ↗</a></div></article>';
}
fetch(matchesUrl,{cache:"no-cache"}).then(function(r){if(!r.ok)throw Error("matches");return r.json();}).then(function(data){var matches=(data.matches||[]).filter(function(m){return m.date>=dateToday();}).sort(function(a,b){return a.date.localeCompare(b.date);});el("match-list").innerHTML=matches.length?matches.slice(0,5).map(matchCard).join(""):'<div class="empty-msg">掲載中の今後の試合がありません。<a href="'+league+'" target="_blank" rel="noopener noreferrer">Fリーグ公式日程で最新情報をご確認ください ↗</a></div>';}).catch(function(){el("match-list").innerHTML='<div class="empty-msg">日程の読み込みができませんでした。<a href="'+league+'" target="_blank" rel="noopener noreferrer">Fリーグ公式日程でご確認ください ↗</a></div>';});
var allPosts=[],filter="all",limit=6;
function drawPosts(){var list=allPosts.filter(function(p){return filter==="all"||p.category===filter;});var html=list.slice(0,limit).map(function(p,i){var theme=p.visual==="PLAY"?" orange":p.visual==="CITY"?" midnight":"";return '<article class="article"><div class="article-visual'+theme+'"><small>'+safe(p.category)+' / '+safe(p.date)+'</small><strong>'+safe(p.visual||"FUTSAL")+'</strong></div><div class="article-body"><span class="article-meta">'+safe(p.date)+' · '+safe(p.category)+'</span><h3>'+safe(p.title)+'</h3><p>'+safe(p.summary)+'</p><a href="./'+encodeURI(p.url||"blog/"+p.id+".html")+'">記事を読む ↗</a></div></article>';}).join("");el("article-list").innerHTML=html||'<p class="empty-msg">このカテゴリーの記事はまだありません。</p>';var more=el("show-more");more.hidden=list.length<=limit;}
fetch(postsUrl,{cache:"no-cache"}).then(function(r){if(!r.ok)throw Error("posts");return r.json();}).then(function(data){allPosts=(data.posts||[]).sort(function(a,b){return b.date.localeCompare(a.date)||String(b.id).localeCompare(String(a.id));});drawPosts();}).catch(function(){el("article-list").innerHTML='<p class="empty-msg">記事を読み込めませんでした。時間をおいて再度お試しください。</p>';});
document.querySelectorAll(".filter").forEach(function(b){b.addEventListener("click",function(){filter=b.getAttribute("data-cat");limit=6;document.querySelectorAll(".filter").forEach(function(x){var on=x===b;x.classList.toggle("current",on);x.setAttribute("aria-pressed",String(on));});drawPosts();});});
el("show-more").addEventListener("click",function(){limit+=6;drawPosts();});
})();