"""Render public profile data to static Korean and English homepages."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / '_data/profile.json').read_text(encoding='utf-8'))
E = html.escape

def a(url, label, cls='text-link'):
    return f'<a class="{cls}" href="{E(url, quote=True)}">{label}<span aria-hidden="true">↗</span></a>'

def render(lang):
    ko = lang == 'ko'
    t = lambda kr, en: kr if ko else en
    key = lambda item, field: E(item[field + '_' + lang])
    b = P['book']
    works = []
    for w in P['works'][:3]:
        date = w['released'][:7].replace('-', '.')
        works.append(f'''<article class="work work-{w['id']}">
          <a class="work-image" href="{E(w['url'])}" aria-label="{E(w['title'])} — Steam"><img src="{E(w['image'])}" alt="{E(w['title'])}" width="616" height="353" loading="lazy"></a>
          <div class="work-body"><div class="work-meta"><span>{key(w,'status')}</span><span>{date}</span></div>
          <h3>{E(w['title'])}</h3><p class="role">{key(w,'role')}</p><p>{key(w,'summary')}</p>
          {a(w['url'],t('Steam에서 보기','View on Steam'))}</div>
        </article>''')
    careers = ''.join(f'''<li><time>{c['start'].replace('-','.')} — {(c['end'] or t('현재','Present')).replace('-','.')}</time><div><h3>{key(c,'company')}<span>{key(c,'role')}</span></h3><p>{key(c,'work')}</p></div></li>''' for c in P['careers'])
    education=''.join(f'<li><span>{c["start"][:4]}–{c["end"][:4]}</span><div><strong>{key(c,"school")}</strong><p>{key(c,"degree")}</p></div></li>' for c in P['education'])
    certificates=''.join(f'<li><span>{c["date"].replace("-",".")}</span><div><strong>{E(c["name"] if ko else c["name_en"])}</strong><p>{E(c["issuer"] if ko else c["issuer_en"])}{(" · "+t("2019년 응시 기록","Test taken in 2019")) if c.get("note") else ""}</p></div></li>' for c in P['certifications'])
    awards=''.join(f'<li><span>{c["date"].replace("-",".")}</span><div><strong>{E(c["name"] if ko else c["name_en"])} · {E(c["award"] if ko else c["award_en"])}</strong><p>{E(c["issuer"] if ko else c["issuer_en"])}</p></div></li>' for c in P['awards'])
    projects=''
    web_work=''
    for c in P['additional_projects']:
        gallery=''
        if c.get('image'):
            gallery=f'<figure class="project-screens"><a href="{E(c["url"])}"><img src="{E(c["image"])}" alt="{E(c["title"])} {t("PC 상품 탐색 화면","desktop product search")}" loading="lazy"></a>'
            if c.get('mobile_image'):
                gallery+=f'<a class="mobile-screen" href="{E(c["url"])}"><img src="{E(c["mobile_image"])}" alt="{E(c["title"])} {t("모바일 상품 탐색 화면","mobile product search")}" loading="lazy"></a>'
            gallery+=f'<figcaption>{E(c["title"])} · {t("프론트엔드 · UI/UX","Frontend & UI/UX")}</figcaption></figure>'
        item_id=f' id="project-{E(c["id"])}"' if c.get('id') else ''
        if c.get('id')=='booth-now':
            web_work=f'<section class="section wrap web-work" id="project-booth-now"><div class="section-heading"><div><p class="eyebrow">WEB / FRONTEND &amp; UI/UX</p><h2>BOOTH NOW</h2></div>{a(c["url"],t("서비스 보기","Visit the service"))}</div><p class="web-description">{key(c,"summary")}</p>{gallery}</section>'
        else:
            projects+=f'<li{item_id}><h3>{E(c["title"])}</h3><p>{key(c,"summary")}</p>{a(c["url"],t("프로젝트 보기","View project"))}{gallery}</li>'
    languages=''.join(f'<li><strong>{key(c,"name")}</strong><span>{key(c,"level")}</span></li>' for c in P['languages'])
    skill_groups=''.join(f'<div><dt>{key(g,"name")}</dt><dd>{" · ".join(E(s) for s in g["items"])}</dd></div>' for g in P['skill_groups'])
    ai_intro=f'<div class="ai-experience"><h3>{key(P["ai_development"],"title")}</h3><p>{key(P["ai_development"],"summary")}</p></div>'
    albums=''.join(f'''<article class="album"><a class="album-art" href="{E(r['url'])}"><img src="{E(r['image'])}" alt="{E(r['title'])} {t('앨범 표지','album cover')}" width="1200" height="1200" loading="lazy"></a><div class="album-meta"><span>{r['year']}</span><span>Illustration: {E(r['illustration'])}</span></div><h3>{E(r['title'])}</h3><p>{key(r,'role')}</p>{a(r['url'],t('앨범 듣기','Listen to the album'))}</article>''' for r in P['music']['releases'])
    music_activities=''.join(f'<li><span>{E(c["date"])}</span><div><strong>{E(c["title"])}</strong><p>{key(c,"role")}</p></div></li>' for c in P['music']['activities'])
    title = t('박태준 | 게임 개발자 · 저자 · MoEater 대표', 'Taejoon Park | Game Developer & Author')
    desc = t('한빛미디어 게임 프로그래밍 책 제1저자(공저), 전 컴투스·컴투버스 개발자. EULA, EGG RAIDERS와 개발 작업을 소개합니다.', 'Game developer leading MoEater, former Com2us and Com2Verse developer, and first-listed co-author of a game programming book published by Hanbit Media.')
    canonical = 'https://rekorn.com/' + ('' if ko else 'en/')
    jsonld = {'@context':'https://schema.org','@type':'Person','name':'박태준','alternateName':['Taejoon Park','Rekorn'],'url':'https://rekorn.com/','jobTitle':'Game Developer','sameAs':[P['links']['github'],P['links']['linkedin'],P['links']['studio']], 'alumniOf':{'@type':'CollegeOrUniversity','name':'University of Tsukuba'}}
    return f'''<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="ko" href="https://rekorn.com/"><link rel="alternate" hreflang="en" href="https://rekorn.com/en/"><link rel="alternate" hreflang="x-default" href="https://rekorn.com/">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://rekorn.com/assets/portfolio/taejoon-park.png"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#f4f1e9">
<link rel="icon" href="/assets/portfolio/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/portfolio/site.css?v={E(P['revision'])}">
<script type="application/ld+json">{json.dumps(jsonld,ensure_ascii=False)}</script>
</head><body>
<a class="skip" href="#main">{t('본문 바로가기','Skip to content')}</a>
<header class="site-header wrap"><a class="wordmark" href="{t('/','/en/')}">REKORN<span class="dot">.</span></a><nav aria-label="{t('주 메뉴','Main navigation')}"><a href="#work">{t('작품','Work')}</a><a href="#about">{t('이력','About')}</a><a href="#contact">{t('개발 문의','Contact')}</a><a class="lang" href="{t('/en/','/')}" lang="{t('en','ko')}">{t('EN','한국어')}</a></nav></header>
<main id="main">
<section class="hero wrap" aria-labelledby="name"><div class="hero-copy"><p class="eyebrow">GAME DEVELOPER · AUTHOR · MOEATER</p><h1 id="name">{t('박태준','Taejoon<br>Park')}<span>Rekorn</span></h1><p class="hero-lead">{t('게임을 개발하고,<br>게임 개발에 관한 책을 썼습니다.','I develop games.<br>I also wrote a book about making them.')}</p><p class="hero-detail">{t('『한 권으로 배우는 게임 프로그래밍』 제1저자(공저).<br>컴투스·컴투버스를 거쳐, 지금은 MoEater를 이끌고 있습니다.','First-listed co-author of a game programming book from Hanbit Media.<br>Formerly at Com2us and Com2Verse. Now leading MoEater.')}</p><p class="hero-detail">{t("게임·앱·웹서비스 제작 · 업무 자동화 · AI 개발 환경 구축", "Games, apps and web development · Workflow automation · AI development environments")}</p><div class="hero-actions"><a class="button" href="#contact">{t('개발 의뢰하기','Discuss a project')}<span aria-hidden="true">↗</span></a><a class="quiet-link" href="#work">{t('만든 것들 보기','Explore my work')}<span aria-hidden="true">↓</span></a></div></div>
<figure class="portrait"><img src="/assets/portfolio/taejoon-park.png" alt="{t('박태준','Taejoon Park')}" width="1071" height="1145" fetchpriority="high"><figcaption><span>TAEJOON PARK</span><span>SOUTH KOREA</span></figcaption></figure></section>
<div class="credentials wrap"><span>{t('전 컴투스 · 컴투버스','Former Com2us · Com2Verse')}</span><span>{t('쓰쿠바대학 공학 학사','University of Tsukuba')}</span><span>{t('일본 전기학회 IEEJ 논문 공저','IEEJ 2020 paper co-author')}</span></div>
<nav class="section-nav wrap" aria-label="{t('포트폴리오 목차','Portfolio contents')}"><a href="#book">{t('저서','Book')}</a><a href="#work">{t('게임','Games')}</a><a href="#project-booth-now">{t('웹서비스','Web service')}</a><a href="#research">{t('연구 · 오픈소스','Research & code')}</a><a href="#about">{t('경력','Experience')}</a><a href="#technology">{t('기술','Technology')}</a><a href="#music">{t('음악','Music')}</a></nav>
<section class="book-section wrap" id="book"><a class="book-display" href="{b['url']}" aria-label="{t('저서 상세 보기','View the book')}"><span class="book-label">HANBIT MEDIA / 2024</span><img src="{b['image']}" alt="{E(b['title'])} 책 표지" width="300" height="390" loading="lazy"></a><div class="book-copy"><p class="eyebrow">PUBLISHED AUTHOR</p><h2>{t('한 권으로 배우는<br>게임 프로그래밍','A book about<br>game programming')}</h2><p class="book-byline">{t('제1저자(공저) · 박태준, 박효재, 윤하연','First-listed co-author · Taejoon Park, Hyojae Park & Hayeon Yoon')}</p><p>{t('수학과 물리, 자료구조와 알고리즘, 디자인 패턴.<br>게임을 만드는 데 필요한 기초 지식을 한 권에 담았습니다.','Math, physics, data structures, algorithms and design patterns.<br>A practical foundation for building games, published in Korean.')}</p><dl class="book-data"><div><dt>{t('출판사','Publisher')}</dt><dd>{t('한빛미디어','Hanbit Media')}</dd></div><div><dt>{t('출간일','Published')}</dt><dd>2024.10.28</dd></div><div><dt>ISBN</dt><dd>9791169213035</dd></div></dl>{a(b['url'],t('서점에서 책 보기','View the book'))}</div></section>
<section class="section wrap" id="work"><div class="section-heading"><div><p class="eyebrow">SELECTED WORK</p><h2>{t('출시한 게임','Released games')}</h2></div><p>{t('작품과 그 안에서 맡은 일.','The games, and my part in making them.')}</p></div><div class="work-grid">{''.join(works)}</div>
<div class="work-notes"><article><span class="index">IN DEVELOPMENT</span><h3>GynoFactory</h3><p>{key(P['works'][3],'summary')}</p>{a(P['links']['studio'],t('MoEater 팀 소개','Meet MoEater'))}</article><article><span class="index">UNITY EDITOR TOOL</span><h3>RekornTools.Avatar</h3><p>{key(P['works'][4],'summary')}</p>{a(P['works'][4]['url'],t('BOOTH 판매 페이지','View on BOOTH'))}</article></div></section>
{web_work}<section class="evidence-section" id="research"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">RESEARCH & OPEN SOURCE</p><h2>{t('연구와 오픈소스 기여','Research & open source')}</h2></div></div><div class="evidence-grid"><article><span class="index">IEEJ NATIONAL CONVENTION / 2020</span><h3>{t('HoloLens를 활용한<br>콘크리트 균열 검사','Concrete crack inspection<br>with HoloLens')}</h3><p>{t('쓰쿠바대학에서 MR HMD를 활용한 검사 시스템을 연구했습니다. 일본 전기학회(IEEJ) 2020 전국대회 논문에 공동 저자로 참여했습니다.','Researched an interactive inspection system using a mixed reality headset at the University of Tsukuba. Co-authored a paper for the IEEJ National Convention in 2020.')}</p><details><summary>{t('논문 제목과 공개 코드','Paper title and code')}</summary><p lang="ja">{E(P['research']['title'])}</p><p>3-040 · IEEJ 2020</p>{a('https://github.com/urun4m0r1/CrackManager','CrackManager / C#')}</details>{a(P['research']['url'],t('학회 발표 기록','Conference record'))}</article><article class="code-contribution"><span class="index">MERGED / APR 13, 2026</span><h3>Friflo.Engine.ECS</h3><p>{key(P['open_source'],'summary')}</p><div class="code-result"><span>IRelation</span><span aria-hidden="true">→</span><span>{t('역직렬화 수정','Deserialization fix')}</span><small>3 {t('회귀 테스트','regression tests')}</small></div>{a(P['open_source']['url'],t('병합된 PR #126','Merged PR #126'))}</article></div><div class="project-index"><h3>{t('더 만든 것들','More projects')}</h3><ul>{projects}</ul></div></div></section>
<section class="section wrap about" id="about"><div class="about-intro"><p class="eyebrow">ABOUT</p><h2>{t('개발 이력','Experience')}</h2><p>{t('2022년 첫 입사 이후 회사 재직과 독립 게임 개발을 이어왔습니다. 현재는 3인 팀 MoEater의 대표로 게임을 만들고 있습니다.','I have worked in development since 2022, through studio roles and independent projects. Today I lead MoEater, a three-person game development team.')}</p>{a(P['links']['linkedin'],'LinkedIn')}{a(P['links']['github'],'GitHub')}{a('/assets/portfolio/Taejoon-Park-Portfolio-KO.pdf',t('작품집 PDF · 6쪽','Portfolio PDF · Korean'))}</div><ol class="timeline">{careers}</ol></section>
<section class="technology-section wrap" id="technology"><div><p class="eyebrow">TECHNOLOGY</p><h2>{t('기술과 도구','Technology & tools')}</h2>{ai_intro}</div><dl class="technology-list">{skill_groups}</dl></section>
<section class="background-section wrap"><div class="background-title"><p class="eyebrow">BACKGROUND</p><h2>{t('학력과 활동','Education & credentials')}</h2></div><div class="background-content"><div class="education-list"><h3>{t('학력','Education')}</h3><ul class="detail-list">{education}</ul><p class="scholarship">{t('한일공동이공계학부장학생 선발 · 일본어 연수 2015–2016','Japan–Korea Joint Government Scholarship program · Japanese language training, 2015–2016')}</p></div><details open><summary>{t('수상','Awards')}<span>04</span></summary><ul class="detail-list">{awards}</ul></details><details><summary>{t('자격 · 어학 시험','Qualifications & language tests')}<span>08</span></summary><ul class="detail-list">{certificates}</ul></details><details><summary>{t('언어','Languages')}<span>03</span></summary><ul class="language-list">{languages}</ul></details></div></section>
<section class="music-section wrap" id="music"><div class="music-heading"><div><p class="eyebrow">MUSIC / REKORN</p><h2>{t('음반과 무대','Records & live events')}</h2></div><div><p>{t('Neodymium Pudding과 東方パラダイス에서 음반을 프로듀싱하고,<br>한국과 일본의 클럽·동인 행사에서 DJ와 VJ로 활동했습니다.','I produced records with Neodymium Pudding and Touhou Paradise,<br>and performed as a DJ and VJ at clubs and independent music events in Korea and Japan.')}</p>{a('/legacy/',t('이전 사이트와 활동 기록','The original site & activity archive'))}</div></div><div class="discography">{albums}</div><details class="music-events"><summary>{t('공연 · 행사 기획 이력','Performances & event production')}</summary><ul class="detail-list">{music_activities}</ul>{a(P['music']['activity_source'],t('전체 활동 기록','Full activity record'))}</details></section>
<section class="contact-section" id="contact"><div class="wrap contact"><div><p class="eyebrow">LET’S WORK TOGETHER</p><h2>{t('어떤 것을<br>만들고 계신가요?','What are<br>you building?')}</h2></div><div class="contact-copy"><p>{t('게임·앱·웹서비스를 새로 만들고 확장하는 일을 맡습니다.<br>개발 도구, 업무 자동화 프로그램과 AI 개발 환경도 구축합니다.','I build games, apps and web applications.<br>I also develop production tools, workflow automation and AI development environments.')}</p><p class="muted">{t('만들고 싶은 제품이나 개선하려는 업무를 알려주세요.<br>아이디어와 현재 상황을 바탕으로 개발 범위와 견적을 안내드립니다.','Tell me about the product you want to build or the workflow you want to improve.<br>We can define the scope, deliverables and budget from there.')}</p><div class="contact-links">{a(P['links']['wishket'],t('위시켓에서 문의','Contact on Wishket'),'button light')}{a(P['links']['linkedin'],'LinkedIn','button outline')}</div><a class="email" href="mailto:urun4m0r1@gmail.com">urun4m0r1@gmail.com ↗</a></div></div></section>
</main><footer class="wrap footer"><span>© 2026 Taejoon Park · Rekorn</span><div>{a('/legacy/',t('이전 사이트 · 음악 아카이브','Legacy · music archive'))}{a(P['links']['studio'],'MoEater')}{a(P['links']['github'],'GitHub')}</div></footer>
</body></html>
'''

for language, path in [('ko', ROOT/'index.html'),('en', ROOT/'en/index.html')]:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(render(language),encoding='utf-8',newline='\n')
print('Rendered Korean and English portfolio from revision',P['revision'])
paths=['/','/en/','/legacy/','/legacy/works/','/legacy/neodymium-pudding/','/legacy/blog/','/legacy/blog/dj-intro-01/','/legacy/blog/dj-intro-02/','/legacy/blog/dj-intro-03/']
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://rekorn.com{p}</loc></url>\n' for p in paths)+'</urlset>\n'
(ROOT/'sitemap.xml').write_text(sitemap,encoding='utf-8',newline='\n')
