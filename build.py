import json, os, html, zipfile, shutil, re
E = html.escape
OUT = '/mnt/user-data/outputs/auto-sites'
DATE = '23.11.2026'
PH = {'nvc-proekt': '20390960/2a0000019eb563d62c4126c1cc7a27554864',
      'beltdaservis': '5102477/2a000001824b931a213c7f3f48aef70f98ce',
      'pyataya-peredacha': '16771051/2a00000197ea31e304a952220ec839e37152',
      'avtoservis-kalinina': '11403733/2a0000018e29f04cf745acfe771a6a4a6942',
      'avtoklimat': '11492238/2a0000018e85606a7c9decafd3f383621342'}
MESH = {'nvc-proekt': ('#ff6a00', '#fff2a8'), 'beltdaservis': ('#7aa7ff', '#a6f0ff'), 'pyataya-peredacha': ('#ff3b30', '#7a0b0b'),
        'avtoservis-kalinina': ('#7fb08a', '#e6c98a'), 'avtoklimat': ('#2a7bff', '#7af0ff')}
LOGO = {'nvc-proekt': '2384894/2a00000174dd710dbedc088dfc10bb71cbc4', 'avtoklimat': '3767262/2a000001755822de823682666b1c3791a945'}
def purl(slug, size): return f'https://avatars.mds.yandex.net/get-altay/{PH[slug]}/{size}'

BASE = '''*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{font-family:var(--body);background:var(--bg);color:var(--fg);line-height:1.65;font-weight:300}a{color:inherit;text-decoration:none}.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:var(--nav);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}.nav .wrap{display:flex;justify-content:space-between;align-items:center;height:64px}.logo{font-family:var(--head);font-weight:700;font-size:1.2rem}.nav .t{color:var(--acc);font-weight:600}
section{padding:72px 0}h1,h2,h3{font-family:var(--head);line-height:1.1}h1{font-size:clamp(2.1rem,5.5vw,4rem)}h2{font-size:clamp(1.8rem,4vw,2.6rem);margin-bottom:28px}
.kicker{color:var(--acc);letter-spacing:.2em;text-transform:uppercase;font-size:.8rem;margin-bottom:14px}.sub{margin:18px 0 28px;max-width:560px;color:var(--mut);font-size:1.1rem}
.hero{position:relative;overflow:hidden;padding:96px 0 84px}.hero-in{display:grid;gap:36px;grid-template-columns:1.4fr 1fr;align-items:center;position:relative;z-index:1}@media(max-width:820px){.hero-in{grid-template-columns:1fr}}
.cta{display:flex;flex-wrap:wrap;gap:12px}.btn{display:inline-block;padding:14px 26px;border-radius:var(--r);font-weight:600;transition:transform .25s,box-shadow .25s,background .25s}.btn:hover{transform:translateY(-3px)}.btn.p{background:var(--acc);color:var(--onacc)}.btn.g{border:1px solid var(--line)}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r)}.rate{padding:28px;text-align:center}.rate b{display:block;font-family:var(--head);font-size:4.5rem;color:var(--acc);line-height:1}.rate span{display:block;margin-top:6px}.rate small{color:var(--mut)}
.svcs{display:grid;gap:16px}.svc{padding:22px}.svc .n{color:var(--acc);font-family:var(--head);font-weight:700}.svc h3{font-size:1.2rem;margin:4px 0}.svc p{color:var(--mut);font-size:.95rem}
.chips{display:flex;flex-wrap:wrap;gap:10px}.chip{padding:8px 16px;border:1px solid var(--line);border-radius:99px;font-size:.9rem}
.revs{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}.rev{padding:24px;transition:transform .3s}.rev:hover{transform:translateY(-4px)}.rev p{margin-bottom:14px}.rev cite{color:var(--acc);font-style:normal;font-size:.9rem}.note{color:var(--mut);font-size:.85rem;margin-top:14px}
.contact{display:grid;gap:28px;grid-template-columns:1fr 1fr}@media(max-width:700px){.contact{grid-template-columns:1fr}}.contact .ph{font-family:var(--head);font-size:clamp(1.8rem,5vw,2.6rem);color:var(--acc);display:block;margin:8px 0 18px}.contact .lbl{color:var(--mut);font-size:.8rem;text-transform:uppercase;letter-spacing:.15em}.links{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}.links a{border-bottom:1px solid var(--acc)}
footer{padding:28px 0 40px;border-top:1px solid var(--line);color:var(--mut);font-size:.8rem}
.reveal{opacity:0;transform:translateY(26px);transition:opacity .7s,transform .7s}.reveal.in{opacity:1;transform:none}
'''

PREM = '''
.demo{background:var(--acc);color:var(--onacc);text-align:center;font-size:.76rem;font-weight:600;letter-spacing:.06em;padding:8px 14px;text-transform:uppercase}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:50;opacity:.05;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E")}
.hero-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.32;filter:saturate(.85) contrast(1.05)}.hero-fade{position:absolute;inset:0;background:linear-gradient(180deg,var(--bg) 0,transparent 30%,transparent 55%,var(--bg) 100%)}
.hero{min-height:84vh;display:flex;align-items:center;text-align:left}.hero-in{width:100%}.kicker::before{content:"";display:inline-block;width:36px;height:1px;background:var(--acc);vertical-align:middle;margin-right:12px}
h2::after{content:"";display:block;width:56px;height:3px;background:var(--acc);margin-top:14px}.btn.p::after{content:" \\2192"}
.strip{display:grid;grid-template-columns:repeat(3,1fr);border-block:1px solid var(--line)}.strip div{padding:28px 12px;text-align:center;border-right:1px solid var(--line)}.strip div:last-child{border:0}.strip b{display:block;font-family:var(--head);font-size:clamp(1.8rem,5vw,3rem);color:var(--acc);line-height:1.1}.strip span{color:var(--mut);font-size:.8rem;text-transform:uppercase;letter-spacing:.12em}
.shot{margin:0;border-radius:var(--r);overflow:hidden;position:relative;border:1px solid var(--line)}.shot img{display:block;width:100%;max-height:520px;object-fit:cover;transition:transform 1.2s}.shot:hover img{transform:scale(1.04)}.shot figcaption{position:absolute;left:0;right:0;bottom:0;padding:40px 18px 14px;font-size:.78rem;color:#fff;background:linear-gradient(transparent,rgba(0,0,0,.72))}
.svc:hover,.rev:hover{box-shadow:0 18px 50px -18px color-mix(in srgb,var(--acc) 55%,transparent)}.btn.p:hover{box-shadow:0 10px 36px -8px color-mix(in srgb,var(--acc) 70%,transparent)}
'''
BASE += PREM
JS = '''var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add("in");io.unobserve(x.target)}})},{threshold:.12});document.querySelectorAll(".reveal").forEach(function(el){io.observe(el)});
var io2=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){io2.unobserve(x.target);var el=x.target,n=+el.dataset.n,t=performance.now();(function f(c){var p=Math.min(1,(c-t)/1400);el.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)})(t)}})});document.querySelectorAll(".cnt").forEach(function(el){io2.observe(el)});'''
GLASS = '''
:root{--gl:light-dark(rgba(255,255,255,.55),rgba(255,255,255,.06));--gl2:light-dark(rgba(255,255,255,.9),rgba(255,255,255,.22));--glsh:light-dark(rgba(20,30,60,.2),rgba(0,0,0,.6))}
.prog{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--acc),var(--m2));z-index:99;box-shadow:0 0 12px var(--acc)}
.bgph{position:fixed;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;opacity:.2;filter:saturate(1.1)}
.mesh{position:fixed;inset:-10%;z-index:-1;pointer-events:none;background:radial-gradient(38% 32% at 12% 16%,color-mix(in srgb,var(--acc) 40%,transparent),transparent 72%),radial-gradient(34% 30% at 90% 26%,color-mix(in srgb,var(--m2) 36%,transparent),transparent 72%),radial-gradient(42% 36% at 68% 92%,color-mix(in srgb,var(--m3) 30%,transparent),transparent 72%),radial-gradient(30% 28% at 8% 80%,color-mix(in srgb,var(--m2) 24%,transparent),transparent 72%);filter:blur(24px);animation:drift 24s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate3d(3%,-3%,0) scale(1.08) rotate(2deg)}}
.hero-fade{background:linear-gradient(180deg,transparent 60%,color-mix(in srgb,var(--bg) 75%,transparent))}
.rate,.svc,.rev,.badge,.sb,.shot figcaption{position:relative;overflow:hidden;background:linear-gradient(145deg,var(--gl2),var(--gl) 45%);-webkit-backdrop-filter:blur(16px) saturate(170%);backdrop-filter:blur(16px) saturate(170%);box-shadow:inset 0 0 0 1px var(--gl2),inset 0 -10px 24px -14px rgba(255,255,255,.1),0 20px 44px -22px var(--glsh)}
.rate,.rev{border-color:transparent}
.rate{-webkit-backdrop-filter:blur(14px) saturate(190%);backdrop-filter:blur(14px) saturate(190%) url(#lq);transform:perspective(900px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .25s}
.rate::before,.svc::before,.rev::before,.badge::before,.sb::before,.shot figcaption::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:radial-gradient(240px circle at var(--mx,30%) var(--my,0%),rgba(255,255,255,.3),transparent 62%);opacity:.45;transition:opacity .35s}
.rate:hover::before,.svc:hover::before,.rev:hover::before,.badge:hover::before,.sb:hover::before,.shot:hover figcaption::before{opacity:1}
.shot figcaption{position:absolute;left:16px;right:auto;bottom:16px;max-width:min(440px,calc(100% - 32px));padding:16px 20px;border-radius:20px;color:var(--fg);background:linear-gradient(145deg,color-mix(in srgb,var(--bg) 58%,transparent),color-mix(in srgb,var(--bg) 28%,transparent));-webkit-backdrop-filter:blur(14px) saturate(190%);backdrop-filter:blur(14px) saturate(190%) url(#lq)}
.shot figcaption b{display:block;font-family:var(--head);font-size:1.2rem}.shot figcaption span{display:block;font-size:.85rem}.shot figcaption small{display:block;color:var(--mut);font-size:.72rem;margin-top:6px}
.svc,.rev,.sb{transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,background .35s}
.svc .n{display:inline-block;transition:.35s}.svc:hover .n{transform:scale(1.18);transform-origin:left;text-shadow:0 0 18px var(--acc)}
.svc h3::after{content:"\\2192";display:inline-block;margin-left:8px;opacity:0;transform:translateX(-10px);transition:.35s;color:var(--acc)}.svc:hover h3::after{opacity:1;transform:none}
.rev::after{content:"\\201C";position:absolute;right:16px;top:-6px;font-size:5rem;font-family:serif;color:var(--acc);opacity:.18;transition:.4s}.rev:hover::after{opacity:.5;transform:translateY(4px)}
.badge{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:99px;font-size:.82rem;font-weight:500;letter-spacing:.02em;transition:transform .3s,box-shadow .3s;cursor:default}
.badge .dot{width:8px;height:8px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 25%,transparent),0 0 10px var(--acc);animation:pulse 2.4s infinite}
@keyframes pulse{50%{box-shadow:0 0 0 6px color-mix(in srgb,var(--acc) 5%,transparent),0 0 14px var(--acc)}}
.badge::after{content:"";position:absolute;top:0;left:-120%;width:60%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.4),transparent);transform:skewX(-20deg);transition:left .7s}.badge:hover::after{left:140%}.badge:hover{transform:translateY(-3px);box-shadow:inset 0 0 0 1px var(--acc),0 10px 26px -10px var(--acc)}
.badge.sm{padding:2px 9px;font-size:.6rem;text-transform:uppercase;letter-spacing:.12em;margin-left:6px;vertical-align:middle;background:var(--acc);color:var(--onacc);box-shadow:none}
.lgo{height:30px;width:30px;border-radius:8px;object-fit:cover;margin-right:10px;vertical-align:middle;background:#fff}
.mosaic{display:grid;gap:14px;grid-template-columns:2fr 1fr;grid-template-rows:240px 240px}.mosaic .big{grid-row:span 2}.mosaic img{width:100%;height:100%;max-height:none;object-fit:cover}
.mosaic .crop{scale:1.9}.mosaic .c1{transform-origin:18% 30%}.mosaic .c2{transform-origin:86% 72%}
@media(max-width:700px){.mosaic{grid-template-columns:1fr 1fr;grid-template-rows:260px 150px}.mosaic .big{grid-row:auto;grid-column:span 2}}
.hb{display:flex;flex-wrap:wrap;gap:8px;margin:-8px 0 26px}
.stats{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin-top:14px}.sb{padding:18px 20px;border-radius:var(--r)}.sb:hover{transform:translateY(-5px)}.sb b{font-family:var(--head);font-size:2rem;color:var(--acc);line-height:1}.sb span{display:block;margin-top:4px}.sb small{color:var(--mut)}
.bar{height:5px;border-radius:9px;background:var(--line);margin-top:12px;overflow:hidden}.bar u{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,var(--acc),color-mix(in srgb,var(--acc) 40%,white));transform-origin:left;transform:scaleX(0);transition:transform 1.3s cubic-bezier(.2,.7,.2,1) .3s}.stats.in .bar u{transform:scaleX(1)}
.links a{border-bottom:0;background:linear-gradient(var(--acc),var(--acc)) 0 100%/0 2px no-repeat;transition:background-size .35s,color .3s}.links a:hover{background-size:100% 2px;color:var(--acc)}
.nav .t{position:relative}.nav .t::after{content:"";position:absolute;left:0;bottom:-4px;height:2px;width:0;background:var(--acc);transition:width .3s}.nav .t:hover::after{width:100%}
.btn{position:relative;overflow:hidden;translate:var(--tx,0) var(--ty,0)}.btn:active{scale:.96}.btn.g{-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);background:var(--gl)}.btn.g:hover{border-color:var(--acc)}
.btn.p::before{content:"";position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.5) 50%,transparent 70%);transform:translateX(-120%);transition:transform .7s}.btn.p:hover::before{transform:translateX(120%)}
.btn.p::after{display:inline-block;transition:transform .3s}.btn.p:hover::after{transform:translateX(5px)}
.rip{position:absolute;width:10px;height:10px;margin:-5px;border-radius:50%;background:rgba(255,255,255,.55);animation:rip .65s ease-out forwards;pointer-events:none}@keyframes rip{to{transform:scale(30);opacity:0}}
.reveal.in{animation:rise .8s cubic-bezier(.2,.7,.2,1) backwards;animation-delay:var(--d,0s)}@keyframes rise{from{opacity:0;transform:translateY(26px)}}
:focus-visible{outline:2px solid var(--acc);outline-offset:3px;border-radius:6px}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.reveal{opacity:1!important;transform:none!important}}
'''
JS2 = '''var P=document.querySelector(".prog"),HB=document.querySelector(".hero-bg");
function sc(){var h=document.documentElement,y=window.scrollY,m=h.scrollHeight-innerHeight;P.style.width=(m>0?y/m*100:0)+"%";if(HB)HB.style.transform="translateY("+(y*.22)+"px) scale(1.1)"}
addEventListener("scroll",sc,{passive:true});sc();
document.querySelectorAll(".svcs,.revs,.chips,.stats").forEach(function(g){Array.prototype.forEach.call(g.children,function(c,i){c.style.setProperty("--d",(i*70)+"ms")})});
document.querySelectorAll(".svc,.rev,.rate,.badge,.sb,.shot").forEach(function(el){el.addEventListener("pointermove",function(e){var r=el.getBoundingClientRect();el.style.setProperty("--mx",(e.clientX-r.left)+"px");el.style.setProperty("--my",(e.clientY-r.top)+"px")})});
document.querySelectorAll(".rate").forEach(function(el){el.addEventListener("pointermove",function(e){var r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;el.style.setProperty("--rx",(-y*10)+"deg");el.style.setProperty("--ry",(x*12)+"deg")});el.addEventListener("pointerleave",function(){el.style.setProperty("--rx","0deg");el.style.setProperty("--ry","0deg")})});
document.querySelectorAll(".btn").forEach(function(b){b.addEventListener("pointermove",function(e){var r=b.getBoundingClientRect();b.style.setProperty("--tx",((e.clientX-r.left-r.width/2)*.18)+"px");b.style.setProperty("--ty",((e.clientY-r.top-r.height/2)*.25)+"px")});b.addEventListener("pointerleave",function(){b.style.setProperty("--tx","0px");b.style.setProperty("--ty","0px")});b.addEventListener("click",function(e){var r=b.getBoundingClientRect(),s=document.createElement("span");s.className="rip";s.style.left=(e.clientX-r.left)+"px";s.style.top=(e.clientY-r.top)+"px";b.appendChild(s);setTimeout(function(){s.remove()},650)})});'''
IMG_ERR = "if(!this.dataset.f){this.dataset.f=1;this.src=this.dataset.s}else{%s}"
DARK_LIGHT = '@media(prefers-color-scheme:dark){:root{color-scheme:dark;--bg:%s;--fg:%s;--mut:%s;--card:%s;--line:%s;--nav:%s}}'

D = [
dict(slug='nvc-proekt', name='НВЦ-Проект', city='Новополоцк', phone='+375 29 208-85-85', tel='+375292088585',
 addr='Новополоцк, Измерительский пр., 5', rating='4,3', rated=190, reviews=82, map='https://yandex.by/maps/-/CXcFbB4N',
 h1='СТО, автомойка и шиномонтаж в Новополоцке', sub='Диагностика, кузовной ремонт, автостёкла, тормоза и электрика на Измерительском проезде, 5.',
 svc=[('Автомойка','Для легкового и грузового транспорта. Запись заранее по телефону.'),('Мойка высокого давления','Чистота автомобиля после мойки под давлением.'),('Лёгкий кузовной ремонт','Крылья, пороги, двери, капот, бампер, крыша: удаление дефектов.'),('Установка автостёкол','Подбор стекла под модель и год выпуска, монтаж.'),('Шиномонтаж','Установка и замена шин на колёсах.'),('Компьютерная диагностика','Определение и анализ неисправностей автомобиля.'),('Ремонт лобовых стёкол','Восстановление стекла после механических повреждений.'),('Замена автостёкол','Демонтаж старого, подготовка поверхности, установка и проверка герметичности.'),('Автоэлектрик','Ремонт, диагностика и обслуживание электрики и электроники.'),('Ремонт тормозной системы','Работы по восстановлению работоспособности тормозов.')],
 facts=['Оплата картой','Базовое сервисное обслуживание','Замена масла','Ремонт ходовой части','Ремонт рулевых реек','Ремонт форсунок','Замена ГРМ','Тонировка стёкол','Заправка и ремонт автокондиционера'],
 revs=[('Алина М.','На диагностике проверили всё от двигателя до электроники, мелкие проблемы устранили сразу. В зоне ожидания комфортно.'),('Emomali D.','На диагностике тормозов честно сказали, что ремонт не нужен, и не стали предлагать лишних услуг.'),('Даша С.','Всё вовремя и быстро, запчасти можно заказать на месте, машину возвращают чистой.')],
 links=[('WhatsApp','https://wa.me/+375292088585'),('Telegram','https://t.me/+375292088585'),('Viber','https://viber.click/+375292088585')],
 font='Oswald:wght@500;700&family=Roboto:wght@300;400;700', deco='',
 css='''html{color-scheme:dark}:root{--bg:#111;--fg:#f2f2f2;--mut:#a3a3a3;--acc:#FFC400;--onacc:#111;--card:#1b1b1b;--line:#2c2c2c;--nav:rgba(17,17,17,.9);--r:2px;--head:'Oswald',sans-serif;--body:'Roboto',sans-serif}
h1,h2,h3,.logo{text-transform:uppercase}h1{font-weight:700}.hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:22px;background:repeating-linear-gradient(-45deg,#FFC400 0 16px,#111 16px 32px)}
.svcs{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}.svc{background:var(--card);border-left:4px solid var(--acc);transition:.3s}.svc:hover{transform:translateX(6px);background:#222}.svc .n{font-size:2rem}'''),
dict(slug='beltdaservis', name='БелТДАсервис', city='Полоцк', phone='+375 44 704-45-09', tel='+375447044509',
 addr='Полоцк, ул. Янки Купалы, 16А', rating='4,8', rated=100, reviews=40, map='https://yandex.by/maps/-/CXcFbVpb',
 h1='Автосервис в Полоцке с рейтингом 4,8', sub='ул. Янки Купалы, 16А. Диагностика, консультации и чистка форсунок.',
 svc=[('Чистка форсунок','Указана в карточке организации как вид работ.'),('Диагностика и консультация','Клиенты в отзывах благодарят за консультацию и диагностику.'),('Ремонт автомобилей','Клиенты советуют сервис для ремонта дизельных автомобилей.')],
 facts=['Персонал: 75% положительных отзывов (24)','Ремонт: 70% положительных отзывов (11)','Чистка форсунок'],
 revs=[('Вадим В.','Провели консультацию и диагностику, объяснили, что переживать не стоит. За помощь денег не взяли.'),('Дмитрий','Работники рассказывают, как улучшить авто, цены для города не заоблачные. Советует для ремонта дизельного авто.')],
 links=[], font='IBM+Plex+Sans:wght@300;400;600&family=IBM+Plex+Mono:wght@500', deco='',
 css='''html{color-scheme:light}:root{--bg:#f4f7fb;--fg:#0b1f3a;--mut:#51627c;--acc:#1f6bff;--onacc:#fff;--card:#fff;--line:#d9e2f0;--nav:rgba(244,247,251,.9);--r:14px;--head:'IBM Plex Sans',sans-serif;--body:'IBM Plex Sans',sans-serif}
h1,h2,h3{font-weight:600}.hero{text-align:center;background:radial-gradient(60% 60% at 50% 0,#dbe7ff,transparent)}.hero-in{grid-template-columns:1fr}.hero .sub{margin-inline:auto}.cta,.hb{justify-content:center}.rate{max-width:260px;margin:0 auto;box-shadow:0 20px 50px rgba(31,107,255,.15)}
.svcs{gap:0}.svc{display:grid;grid-template-columns:60px 1fr;column-gap:10px;border-bottom:1px solid var(--line);padding:22px 8px;transition:.3s}.svc:hover{background:var(--card);padding-left:20px}.svc .n{grid-row:span 2;font-family:'IBM Plex Mono',monospace}
'''+DARK_LIGHT%('#0b1424','#e8eefc','#9fb0cc','#122038','#22344f','rgba(11,20,36,.9)')),
dict(slug='pyataya-peredacha', name='Пятая Передача', city='Полоцк', phone='+375 29 711-09-09', tel='+375297110909', phone_note='дополнительный телефон',
 addr='Полоцк, ул. Шенягина, 44А', rating='4,1', rated=96, reviews=35, map='https://yandex.by/maps/-/CXcFbGk7',
 h1='Автосервис, АКПП и автозапчасти в Полоцке', sub='ул. Шенягина, 44А. Шиномонтаж, развал-схождение, ремонт АКПП и магазин запчастей.',
 svc=[('Автосервис','Рубрика «Автосервис, автотехцентр» на Яндекс Картах.'),('Ремонт АКПП','Отдельная рубрика организации.'),('Шиномонтаж','Клиенты отмечают быструю работу с колёсами.'),('Развал-схождение','Указано среди особенностей организации.'),('Магазин автозапчастей и автотоваров','Клиенты отмечают, что запчасти можно подобрать на месте.')],
 facts=['Автосервис','Ремонт АКПП','Шиномонтаж','Развал-схождение','Магазин автозапчастей'],
 revs=[('Misha R.','ГРМ заменили в день обращения, в автомагазине всё подобрали на месте, цена приятная.'),('Н.','Приехал с пробитым колесом, дождался очереди, всё сделали быстро и чётко.')],
 links=[], font='Bebas+Neue&family=Barlow:wght@300;400;600', deco='<div class="big5" aria-hidden="true">5</div>',
 css='''html{color-scheme:dark}:root{--bg:#0c0c0e;--fg:#fff;--mut:#b3b3b8;--acc:#E10600;--onacc:#fff;--card:#16161a;--line:#2a2a30;--nav:rgba(12,12,14,.9);--r:0;--head:'Bebas Neue',sans-serif;--body:'Barlow',sans-serif}
h1,h2{font-style:italic;text-transform:uppercase;font-weight:400}h1{font-size:clamp(3rem,9vw,6rem)}h2{font-size:clamp(2.4rem,5vw,3.6rem)}.btn{transform:skew(-8deg)}.btn:hover{transform:skew(-8deg) translateY(-3px)}
.big5{position:absolute;right:-2%;top:-6%;font-family:'Bebas Neue',sans-serif;font-size:min(60vw,540px);line-height:1;color:transparent;-webkit-text-stroke:2px var(--acc);opacity:.5}
.svcs{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}.svc{background:var(--card);border-top:3px solid var(--acc);clip-path:polygon(0 0,100% 0,100% calc(100% - 18px),calc(100% - 18px) 100%,0 100%);transition:.3s}.svc:hover{background:var(--acc)}.svc:hover p,.svc:hover .n{color:#fff}'''),
dict(slug='avtoservis-kalinina', name='Автосервис', city='Новополоцк', phone='+375 29 360-99-10', tel='+375293609910',
 addr='Новополоцк, ул. Калинина, 19А, корп. 815', rating='4,9', rated=104, reviews=30, map='https://yandex.by/maps/-/CXcFbOIc',
 h1='Ходовая, двигатель и развал-схождение в Новополоцке', sub='ул. Калинина, 19А, корп. 815. Тормоза, сцепление, ГРМ, замена масла.',
 svc=[('Ремонт тормозной системы',None),('Ремонт двигателя',None),('Замена масла',None),('Ремонт ходовой части','Клиенты отмечают хорошую диагностику ходовой.'),('Ремонт сцепления',None),('Замена ГРМ',None),('Развал-схождение','По отзыву клиента, 3D-развал делают на месте.'),('Базовое сервисное обслуживание',None)],
 facts=['Оплата картой','Сход-развал: 92% положительных отзывов (12)','Ремонт: 92% положительных отзывов (12)','Персонал: 83% положительных отзывов (13)'],
 revs=[('Александр К.','Ответственные и обязательные, 3D-развал на месте, находят все стуки и советуют, что делать в первую очередь. Запчасти могут заказать сами.'),('protopopov861','Развал-схождение делают отлично, можно присутствовать при работе.'),('Лихой Ли','Работа выполняется профессионально, теперь всегда заезжает сюда.')],
 links=[], font='Fraunces:wght@600&family=Inter:wght@300;400;600', deco='',
 css='''html{color-scheme:light}:root{--bg:#f3efe6;--fg:#1c2a22;--mut:#5b6a60;--acc:#1f5c3a;--onacc:#f3efe6;--card:#faf7f0;--line:#cfc8b8;--nav:rgba(243,239,230,.92);--r:0;--head:'Fraunces',serif;--body:'Inter',sans-serif}
h1,h2{font-weight:600;letter-spacing:-.02em}.hero{border-bottom:1px solid var(--line)}.hero .kicker{border-top:2px solid var(--acc);padding-top:12px;display:inline-block}.rate{border:2px solid var(--acc);background:transparent}
.svcs{gap:0;border-top:2px solid var(--fg)}.svc{display:grid;grid-template-columns:70px 1fr 1.2fr;gap:16px;align-items:baseline;border-bottom:1px solid var(--line);padding:18px 4px;transition:.3s}.svc:hover{background:var(--card);padding-left:16px}.svc h3{margin:0}@media(max-width:700px){.svc{grid-template-columns:50px 1fr}.svc p{grid-column:2}}
'''+DARK_LIGHT%('#101a14','#eef3ee','#a3b3a8','#16241b','#2a3d31','rgba(16,26,20,.9)')),
dict(slug='avtoklimat', name='Автоклимат', city='Витебская область', phone='+375 29 649-05-60', tel='+375296490560',
 addr='Витебская обл., Полоцкий р-н, Экиманский сельсовет, д. Тросно', rating='4,9', rated=83, reviews=27, map='https://yandex.by/maps/-/CXcFb29b',
 h1='Автокондиционеры и вебасто в Витебской области', sub='д. Тросно, Полоцкий район. Заправка и ремонт кондиционеров, установка и ремонт вебасто.',
 svc=[('Диагностика и ремонт автокондиционера','Определение утечек и проблем в работе, ремонт системы.'),('Заправка автокондиционера','Своевременная заправка для комфорта и безопасности.'),('Ремонт компрессора автокондиционера',None),('Ремонт радиатора автокондиционера',None),('Установка вебасто','Автономный воздушный отопитель для тёплого салона зимой.'),('Ремонт вебасто','Ремонт воздушного отопителя.'),('Промывка системы охлаждения','Перед заменой антифриза.'),('Ремонт медных, алюминиевых, латунных деталей',None),('Ремонт рефрижераторов и холодильных установок',None)],
 facts=['Оплата картой','Базовое сервисное обслуживание','Компьютерная диагностика','Ремонт автоэлектрики','Персонал: 100% положительных отзывов (14)','Ремонт кондиционера: 79% положительных (15)'],
 revs=[('Евгений К.','Диагностика, разбор вариантов, объяснение ценообразования и согласование. После ремонта кондиционер холодит лучше.'),('Игорь П.','Люди знают своё дело: делают, если берутся, и дают гарантию.'),('Юрий Ж.','Опрессовка, осмотр на утечки, заправка. Предложили добавить краситель для поиска течи. Цены демократичные.')],
 links=[('Instagram','https://www.instagram.com/autoclimate.by/')], font='Sora:wght@600;700&family=Inter:wght@300;400;600',
 deco='<svg class="flake" viewBox="-50 -50 100 100" fill="none" stroke="#38d6ff" stroke-width="1.2" stroke-linecap="round" aria-hidden="true"><path d="M0-46V46M-40-23L40 23M-40 23L40-23M0-32l-8-8M0-32l8-8M0 32l-8 8M0 32l8 8M-28-16l-11 0M-28-16l-3-11M28 16l11 0M28 16l3 11M-28 16l-11 0M-28 16l-3 11M28-16l11 0M28-16l3-11"/></svg>',
 css='''html{color-scheme:dark}:root{--bg:#06121f;--fg:#e6f6ff;--mut:#8fb2c9;--acc:#38d6ff;--onacc:#06121f;--card:rgba(255,255,255,.06);--line:rgba(160,220,255,.18);--nav:rgba(6,18,31,.7);--r:22px;--head:'Sora',sans-serif;--body:'Inter',sans-serif}
body{background:radial-gradient(70% 50% at 80% 0,#0b3a5e,transparent),radial-gradient(50% 40% at 0 40%,#0a2a4a,transparent),var(--bg);background-attachment:fixed}
.card,.svc{backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);box-shadow:inset 0 1px 0 rgba(255,255,255,.15)}.svcs{grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}.svc{background:var(--card);border:1px solid var(--line);border-radius:var(--r);transition:.35s}.svc:hover{transform:translateY(-6px);box-shadow:0 0 36px rgba(56,214,255,.35);border-color:var(--acc)}
.flake{position:absolute;right:4%;top:10%;width:min(46vw,380px);opacity:.25;animation:spin 60s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}'''),
]

def plural(n, a, b, c):
    n10, n100 = n % 10, n % 100
    return a if n10 == 1 and n100 != 11 else b if 2 <= n10 <= 4 and not 12 <= n100 <= 14 else c

def page(d):
    svc = ''.join(f'<article class="svc reveal"><span class="n">{i+1:02d}</span><h3>{E(t)}</h3>{f"<p>{E(x)}</p>" if x else "<p></p>"}</article>' for i, (t, x) in enumerate(d['svc']))
    mm = [re.match(r'^(.+?): (\d+)% положительных(?: отзывов)? \((\d+)\)$', f) for f in d['facts']]
    chips = ''.join(f'<span class="badge"><i class="dot"></i>{E(f)}</span>' for f, m in zip(d['facts'], mm) if not m)
    st = [m.groups() for m in mm if m]
    stats_html = ''
    revs = ''.join(f'<blockquote class="rev card reveal"><p>{E(t)}</p><cite>{E(a)}</cite></blockquote>' for a, t in d['revs'])
    links = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{E(n)}</a>' for n, u in d['links'])
    pn = f' <small style="font-size:.8rem;color:var(--mut)">({d["phone_note"]})</small>' if d.get('phone_note') else ''
    title = f'{d["name"]} — {d["city"]}'
    hs = purl(d['slug'], 'XXL'); ls = purl(d['slug'], 'L_height')
    m2, m3 = MESH[d['slug']]
    lg = f'<img class="lgo" src="{purl(d["slug"], "S_height").replace(PH[d["slug"]], LOGO[d["slug"]])}" alt="" referrerpolicy="no-referrer" onerror="this.remove()">' if d['slug'] in LOGO else ''
    hb = f'<span class="badge"><i class="dot"></i>★ {d["rating"]} на Яндекс Картах</span><span class="badge">{E(d["city"])}</span><span class="badge">{d["reviews"]} {plural(d["reviews"],"отзыв","отзыва","отзывов")}</span>'
    he = IMG_ERR % 'this.remove()'; se = IMG_ERR % "this.closest('section').remove()" 
    return f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(d["sub"])}">
<link href="https://fonts.googleapis.com/css2?family={d["font"]}&display=swap" rel="stylesheet">
<style>{BASE}{d["css"]}{GLASS}</style></head><body>
<div class="prog" style="--m2:{m2}"></div><svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="lq"><feTurbulence type="fractalNoise" baseFrequency=".008 .012" numOctaves="2" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="12"/></filter></svg>
<img class="bgph" src="{hs}" data-s="{ls}" alt="" referrerpolicy="no-referrer" onerror="{he}"><div class="mesh" style="--m2:{m2};--m3:{m3}"></div>
<div class="demo">Демо-версия · прототип сайта будет удалён по первой просьбе владельца</div>
<header class="nav"><div class="wrap"><span class="logo">{lg}{E(d["name"])}<span class="badge sm">демо</span></span><a class="t" href="tel:{d["tel"]}">{d["phone"]}</a></div></header>
<section class="hero"><img class="hero-bg" src="{hs}" data-s="{ls}" alt="" referrerpolicy="no-referrer" onerror="{he}"><div class="hero-fade"></div>{d["deco"]}<div class="wrap hero-in"><div><p class="kicker">{E(d["city"])}</p><h1>{E(d["h1"])}</h1><p class="sub">{E(d["sub"])}</p><div class="hb">{hb}</div>
<div class="cta"><a class="btn p" href="tel:{d["tel"]}">Позвонить</a><a class="btn g" href="{d["map"]}" target="_blank" rel="noopener">Маршрут на карте</a></div></div>
<aside class="rate card"><b>{d["rating"]}</b><span>рейтинг · {d["rated"]} {plural(d["rated"],"оценка","оценки","оценок")}</span><small>{d["reviews"]} {plural(d["reviews"],"отзыв","отзыва","отзывов")} на Яндекс Картах</small></aside></div></section>
<div class="wrap"><div class="strip"><div><b>{d["rating"]}</b><span>рейтинг</span></div><div><b class="cnt" data-n="{d["rated"]}">0</b><span>оценок</span></div><div><b class="cnt" data-n="{d["reviews"]}">0</b><span>отзывов</span></div></div></div>
<section><div class="wrap"><h2 class="reveal">Услуги</h2><div class="svcs">{svc}</div><p class="note">Стоимость уточняйте по телефону.</p></div></section>
<section><div class="wrap"><h2 class="reveal">Фото</h2><div class="mosaic reveal"><figure class="shot big"><img src="{hs}" data-s="{ls}" alt="{E(d["name"])}" loading="lazy" referrerpolicy="no-referrer" onerror="{se}"><figcaption><b>{E(d["name"])}</b><span>{E(d["addr"])}</span><small>Фото из карточки на Яндекс Картах · демо-версия</small></figcaption></figure><figure class="shot"><img class="crop c1" src="{hs}" data-s="{ls}" alt="{E(d["name"])}" loading="lazy" referrerpolicy="no-referrer" onerror="{se}"></figure><figure class="shot"><img class="crop c2" src="{hs}" data-s="{ls}" alt="{E(d["name"])}" loading="lazy" referrerpolicy="no-referrer" onerror="{se}"></figure></div><p class="note">Фото и его фрагменты из карточки организации на Яндекс Картах.</p></div></section>
<section><div class="wrap"><h2 class="reveal">Особенности</h2><div class="chips reveal">{chips}</div>{stats_html}</div></section>
<section><div class="wrap"><h2 class="reveal">Что пишут клиенты</h2><div class="revs">{revs}</div><p class="note">Краткий пересказ отзывов с Яндекс Карт.</p></div></section>
<section><div class="wrap contact reveal"><div><p class="lbl">Телефон</p><a class="ph" href="tel:{d["tel"]}">{d["phone"]}</a>{pn}<p class="lbl">Адрес</p><p>{E(d["addr"])}</p></div>
<div><p class="lbl">Как добраться</p><p>Откройте карточку организации на Яндекс Картах, чтобы построить маршрут.</p><div class="cta" style="margin-top:16px"><a class="btn p" href="{d["map"]}" target="_blank" rel="noopener">Открыть на карте</a></div><div class="links">{links}</div></div></div></section>
<footer><div class="wrap">Демо-версия: это не официальный сайт организации, он будет удалён по первой просьбе владельца. Данные и фото взяты из публичной карточки на Яндекс Картах (на {DATE}), права на них принадлежат владельцам.</div></footer>
<script>{JS}{JS2}</script>
</body></html>'''

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(f'{OUT}/data/raw')
cards = ''
for d in D:
    os.makedirs(f'{OUT}/{d["slug"]}')
    open(f'{OUT}/{d["slug"]}/index.html', 'w', encoding='utf-8').write(page(d))
    raw = {k: v for k, v in d.items() if k not in ('css', 'font', 'deco')}
    json.dump(raw, open(f'{OUT}/data/raw/{d["slug"]}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    cards += f'<a class="c" href="{d["slug"]}/"><b>{E(d["name"])}</b><span>{E(d["city"])}</span><i>★ {d["rating"]} · {d["rated"]} оценок</i></a>'
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(f'''<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Автосервисы — сайты</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#0E0E10;color:#eee;font-family:system-ui,sans-serif;padding:48px 20px}}h1{{max-width:900px;margin:0 auto 28px;font-size:2rem}}.g{{max-width:900px;margin:0 auto;display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}}.c{{display:block;padding:22px;border:1px solid #2a2a30;border-radius:16px;text-decoration:none;color:inherit;transition:.3s}}.c:hover{{border-color:#FF5A1F;transform:translateY(-4px)}}.c b{{display:block;font-size:1.2rem}}.c span{{color:#999}}.c i{{display:block;margin-top:10px;color:#FF5A1F;font-style:normal}}</style></head><body><h1>Пять сайтов для автосервисов</h1><p style="max-width:900px;margin:0 auto 24px;color:#999">Демо-версии. Будут удалены по первой просьбе владельцев.</p><div class="g">{cards}</div></body></html>''')
open(f'{OUT}/.nojekyll', 'w').close()
open(f'{OUT}/README.md', 'w', encoding='utf-8').write('''# Сайты автосервисов

> **Демо-версия.** Прототипы будут удалены по первой просьбе владельцев организаций. Фото подгружаются из карточек Яндекс Карт (hotlink), права принадлежат владельцам.\n\nПять статичных сайтов (чистые HTML/CSS/JS, без сборки), у каждого свой стиль.

| Папка | Организация |
|---|---|
| `nvc-proekt/` | НВЦ-Проект, Новополоцк |
| `beltdaservis/` | БелТДАсервис, Полоцк |
| `pyataya-peredacha/` | Пятая Передача, Полоцк |
| `avtoservis-kalinina/` | Автосервис, Новополоцк |
| `avtoklimat/` | Автоклимат, Витебская обл. |

`data/raw/*.json` — факты из карточек Яндекс Карт (на 23.11.2026). `tools/build.py` пересобирает сайты.

## Публикация на GitHub Pages
1. Создайте репозиторий и загрузите содержимое папки.
2. Settings → Pages → Deploy from a branch → `main` / `(root)`.
3. Сайты откроются по адресам `https://<user>.github.io/<repo>/<папка>/`.
''')
os.makedirs(f'{OUT}/tools'); shutil.copy(__file__, f'{OUT}/tools/build.py')
z = '/mnt/user-data/outputs/auto-sites.zip'
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for r, _, fs in os.walk(OUT):
        for f in fs:
            p = os.path.join(r, f); zf.write(p, os.path.relpath(p, '/mnt/user-data/outputs'))
print('ok')
