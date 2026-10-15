"""Assemble the OC Vibe dashboard from the BI Pulse template's CSS/logo and the content module."""
import os as _os
BASE = _os.path.dirname(_os.path.abspath(__file__))  # pipeline folder
import json, re, base64, os
import content as C

css = open(BASE + '/assets/css.txt').read()
logo_line = open(BASE + '/assets/logo.txt').read().strip()
logo_img = re.search(r'<img [^>]+>', logo_line).group(0)

PREP = "Oct. 13, 2026"
import ocv_content as OCVC
import schedule as SC   # Oct. 14, 2026: quarterly update schedule and planned sources
DATA = dict(main=C.DATA_EXTRA['main'], tags=C.DATA_EXTRA['tags'], sections=C.SECTIONS, stories=C.STORIES, takeaways=C.TAKEAWAYS, sources=C.SOURCES, prepared=PREP, register=OCVC.REGISTER, schedule=SC.SCHEDULE, ask=C.DATA_EXTRA['ask'], lib=C.DATA_EXTRA['lib'])

EXTRA_CSS = r"""


/* Value tooltips and highlight on hover/focus */
#vtip{position:fixed;z-index:9999;pointer-events:none;max-width:280px;padding:7px 10px;border-radius:var(--r-sm);background:#231F20;color:#FFFFFF;font-size:13px;font-weight:700;line-height:1.35;box-shadow:none}
#vtip[hidden]{display:none}
[data-tip]{cursor:default}
[data-tip]:focus-visible{outline:2px solid #125C60;outline-offset:2px}
.hbars .t.is-hot .f,.vcol.is-hot .b,.ann-bar.is-hot .f{outline:2px solid #125C60;outline-offset:1px}
.hovering .hbars .t:not(.is-hot) .f,.hovering .vcol:not(.is-hot) .b,.ann-bars.hovering .ann-bar:not(.is-hot) .f{opacity:.45}
.vcol.is-hot .bv,.hbars .t.is-hot + .v{color:#125C60;font-weight:800}
svg.vz circle.hit{fill:transparent;stroke:none}
svg.vz circle.hit.is-hot{fill:#43A3A3;fill-opacity:.18;stroke:#125C60;stroke-width:2}
svg.vz rect.is-hot,svg.vz line.is-hot{stroke:#231F20;stroke-width:2}
.hovering svg.vz rect[data-tip]:not(.is-hot){opacity:.55}
table.heat td.is-hot{outline:3px solid #231F20;outline-offset:-3px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) #vtip{background:#F9F9F2;color:#231F20}}
:root[data-theme="dark"] #vtip{background:#F9F9F2;color:#231F20}
@media print{#vtip{display:none}}

/* Calculation breakdowns */
.calc-line{display:block;font-size:12.5px;line-height:1.4;margin-top:4px;padding:4px 8px;border-radius:var(--r-sm);background:var(--zebra);color:var(--ink,inherit);font-weight:500}
.calc-line b{color:var(--heading);font-weight:750}
.calc-steps{margin:16px 0 0;border:1px solid var(--border);border-radius:var(--r-md);background:var(--surface-card);padding:14px 16px}
.calc-steps h3{margin:0 0 10px;font-size:17px;color:var(--heading)}
.calc-steps table{width:100%}.calc-steps td,.calc-steps th{font-size:13.5px;line-height:1.4;vertical-align:top}
.calc-steps tr.hi th,.calc-steps tr.hi td{background:var(--surface-fill)}
.calc-steps .n{text-align:right;white-space:nowrap}
/* Featured BI charts */
.feat{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:18px 0 0}
.feat.one{grid-template-columns:minmax(0,1fr)}
.feat>div:last-child:nth-child(odd){grid-column:1/-1}
@media (max-width:900px){.feat{grid-template-columns:minmax(0,1fr)}}
.feat .chartf{height:100%;margin:0}
svg.vz{width:100%;height:auto;display:block;margin:6px 0 2px;overflow:visible}
svg.vz .gl{stroke:#231F20;stroke-opacity:.15;stroke-width:1}
svg.vz .ax{font-size:11px;fill:#231F20;font-family:inherit}svg.vz .ax.b{font-weight:700}
svg.vz .dl{font-size:12px;font-weight:700;fill:#231F20;font-family:inherit}svg.vz .dl.f{fill:#125C60;font-size:13px}
svg.vz .ln{fill:none;stroke-linejoin:round;stroke-linecap:round}svg.vz .ln.f{stroke:#43A3A3;stroke-width:3}svg.vz .ln.o{stroke:#77C7C9;stroke-width:2}
svg.vz .ar{fill:#B4D9E3;fill-opacity:.35;stroke:none}
svg.vz .pt.f{fill:#43A3A3}svg.vz .pt.o{fill:#77C7C9}
svg.vz .wf1{fill:#43A3A3}svg.vz .wf2{fill:#77C7C9}svg.vz .wft{fill:#125C60}svg.vz .wfc{stroke:#231F20;stroke-opacity:.4;stroke-dasharray:3 3}
svg.vz .rb{fill:#B4D9E3}svg.vz .rmb{stroke:#125C60;stroke-width:3}svg.vz .rmm{stroke:#43A3A3;stroke-width:2}svg.vz .rme{stroke:#231F20;stroke-opacity:.5;stroke-width:1.5;stroke-dasharray:4 3}
.legend i.lf{background:#43A3A3}.legend i.lo{background:#77C7C9}
table.heat{width:100%}table.heat td{text-align:center;font-weight:700;font-size:13.5px;color:#231F20}table.heat td.hx{text-align:left;font-weight:500;font-size:12.5px;background:transparent}
table.heat td.hx{color:var(--ink)}
.upnext .kv,.upnext b{color:#FFFFFF!important;background:none!important}
.bd-route{color:#231F20!important}
.heat .h1,.heat-lg .h1{background:#F9F9F2}.heat .h2,.heat-lg .h2{background:#B4D9E3}.heat .h3,.heat-lg .h3{background:#77C7C9}.heat .h4,.heat-lg .h4{background:#43A3A3}.heat .h5,.heat-lg .h5{background:#125C60;color:#FFFFFF}
.heat-lg i{border:1px solid #B4D9E3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) svg.vz .ax,:root:not([data-theme="light"]) svg.vz .dl{fill:#F9F9F2}:root:not([data-theme="light"]) svg.vz .dl.f{fill:#77C7C9}:root:not([data-theme="light"]) svg.vz .gl{stroke:#F9F9F2}:root:not([data-theme="light"]) svg.vz .wft{fill:#F9F9F2}:root:not([data-theme="light"]) svg.vz .rmb{stroke:#F9F9F2}}
:root[data-theme="dark"] svg.vz .ax,:root[data-theme="dark"] svg.vz .dl{fill:#F9F9F2}:root[data-theme="dark"] svg.vz .dl.f{fill:#77C7C9}:root[data-theme="dark"] svg.vz .gl{stroke:#F9F9F2}:root[data-theme="dark"] svg.vz .wft{fill:#F9F9F2}:root[data-theme="dark"] svg.vz .rmb{stroke:#F9F9F2}
/* KPI data cards (VA Branded KpiCard: one value, label, change, source; teal top rule) */
.art-side{padding:0;border:0;background:none}
.art-side h3{margin:0 0 10px}
.art-stat{border:1px solid var(--border);border-top:3px solid #43A3A3;border-radius:var(--r-md);background:var(--surface-card);padding:12px 14px!important;margin:0 0 10px}
.art-stat:first-of-type{padding-top:12px!important;border-top:3px solid #43A3A3}
.as-v{font-size:32px!important;font-weight:750!important;font-style:normal!important;letter-spacing:-.01em}
/* Entrance motion: fade and 12px rise, 400ms, once (VA Branded allows entrance only) */
@media (prefers-reduced-motion:no-preference){.js-anim .reveal{opacity:0;transform:translateY(12px);transition:opacity .4s ease-out,transform .4s ease-out}.js-anim .reveal.in{opacity:1;transform:none}}
@media print{.reveal{opacity:1!important;transform:none!important}}

/* Article view for every section (overview stays the main announcement) */
.art-h{border-bottom:1px solid var(--border);padding:4px 0 14px;margin:0 0 16px;max-width:980px}
.art-kick{display:inline-block;font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--heading);border-bottom:3px solid #43A3A3;padding-bottom:2px;margin-bottom:8px}
.art-head{margin:0 0 6px;font-size:clamp(24px,3.2vw,34px);line-height:1.12;font-weight:900;font-style:italic;color:var(--heading);letter-spacing:-.005em}
.art-dek{margin:0 0 8px;font-size:17px;line-height:1.4;font-weight:600}
.art-q{margin:0 0 6px;font-size:14px;line-height:1.4;color:var(--muted)}
.art-by .badge{white-space:normal;max-width:100%;overflow-wrap:anywhere}
.art-by{margin:0;font-size:12.5px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.art-grid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:22px;align-items:start}
@media (max-width:1000px){.art-grid{grid-template-columns:minmax(0,1fr)}}
.art-lede{margin:0}
.art-w5h{margin:16px 0 0;max-width:820px}
.art-w5h h3,.art-side h3,.ocv-whole h3{margin:0 0 10px;font-size:17px;color:var(--heading)}
.w5h-p{margin:0 0 9px;font-size:15px;line-height:1.55}
.w5h-p .w5h-k{color:var(--heading);font-weight:800;margin-right:2px}
.art-side{border:1px solid var(--border);border-radius:var(--r-md);background:var(--surface-card);padding:14px 16px}
.art-stat{display:flex;flex-direction:column;gap:2px;padding:10px 0;border-top:1px solid var(--border-subtle)}
.art-stat:first-of-type{border-top:0;padding-top:0}
.as-k{font-size:10.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--heading)}
.as-v{font-size:26px;line-height:1.1;font-weight:900;font-style:italic;color:var(--heading)}
.as-l{font-size:13px;font-weight:700}.as-p{font-size:13px;line-height:1.4}
.art-fig{margin:18px 0 0}
.ocv-whole{margin:18px 0 0;border:1px solid var(--border);border-top:4px solid #125C60;border-radius:var(--r-md);background:var(--surface-card);padding:14px 18px}
.ow-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
@media (max-width:760px){.ow-grid{grid-template-columns:minmax(0,1fr)}}
.ow-col h4{margin:0 0 8px;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--heading)}
.ow-col ul{margin:0;padding-left:0;list-style:none}.ow-col li{margin:0 0 12px;font-size:14.5px;line-height:1.5}
.otag{display:inline-block;font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:1px 7px;border-radius:var(--pill);border:1px solid #43A3A3;background:transparent;color:var(--heading);margin-right:4px;vertical-align:1px;line-height:1.5}
.cc-t2{width:100%}.cc-t2 td,.cc-t2 th{vertical-align:top;font-size:14px;line-height:1.45}
.cc-t2 tbody th{white-space:nowrap;border-left:5px solid #43A3A3}
.cc-t2 tr.cc-growth th{border-left-color:#125C60}.cc-t2 tr.cc-quick-win th{border-left-color:#77C7C9}.cc-t2 tr.cc-early-hurdle th{border-left-color:#231F20}.cc-t2 tr.cc-pitfall th{border-left-color:#A10009}.cc-t2 tr.cc-explanation th{border-left-color:#B4D9E3}
.cc-t2 .src-cell{font-size:12px;color:var(--muted);min-width:180px}
.muted{color:var(--muted)}
.cc-box .scroll{overflow-x:auto}
@media (max-width:640px){.art-fig .scroll,.sec-more .scroll{overflow-x:auto}.art-fig .scroll table,.sec-more .scroll table{min-width:560px}}
@media (max-width:640px){.cc-t2,.cc-t2 tbody,.cc-t2 tr,.cc-t2 th,.cc-t2 td{display:block;width:auto}.cc-t2 thead{display:none}.cc-t2 tr{border-left:5px solid #43A3A3;margin:0 0 10px;padding:4px 0}.cc-t2 tbody th{border-left:0!important;white-space:normal}.cc-t2 .src-cell{min-width:0}
.cc-t2 tr.cc-growth{border-left-color:#125C60}.cc-t2 tr.cc-quick-win{border-left-color:#77C7C9}.cc-t2 tr.cc-early-hurdle{border-left-color:#231F20}.cc-t2 tr.cc-pitfall{border-left-color:#A10009}.cc-t2 tr.cc-explanation{border-left-color:#B4D9E3}}
.more-d{margin:18px 0 0;border:1px solid var(--border);border-radius:var(--r-md);background:var(--surface-card)}
.more-d>summary{cursor:pointer;padding:12px 18px;font-weight:800;color:var(--heading);font-size:15px}
.more-d[open]>summary{border-bottom:1px solid var(--border-subtle)}
.more-d .sec-more,.more-d .notes-box{margin:14px 18px}
.more-d .notes-box{border:0;padding:0;background:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .ocv-whole{border-top-color:#43A3A3}:root:not([data-theme="light"]) .cc-t2 tr.cc-early-hurdle th{border-left-color:#F9F9F2}}
:root[data-theme="dark"] .ocv-whole{border-top-color:#43A3A3}:root[data-theme="dark"] .cc-t2 tr.cc-early-hurdle th{border-left-color:#F9F9F2}
@media print{.more-d>summary{display:none}}

/* John's logic: essentials (5W+H), compare and contrast, inline sources */
.w5h-box,.cc-box{margin:14px 0 0;border:1px solid var(--border);border-radius:var(--r-md);background:var(--surface-card);padding:14px 18px}
.w5h-box h3,.cc-box h3{margin:0 0 10px;font-size:17px;color:var(--heading)}
.w5h-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.cc-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
@media (max-width:1100px){.cc-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.w5h-grid,.cc-grid{grid-template-columns:minmax(0,1fr)}}
.w5h-c{border-top:3px solid #43A3A3;padding:8px 2px 2px}
.w5h-k{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--heading);margin-bottom:4px}
.w5h-c p,.cc-c p{margin:0;font-size:14px;line-height:1.45}
.cc-c{border:1px solid var(--border-subtle);border-left:6px solid #43A3A3;border-radius:var(--r-sm);padding:10px 12px;display:flex;flex-direction:column;gap:6px;background:var(--surface-page)}
.cc-t{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--heading)}
.cc-growth{border-left-color:#125C60}.cc-opportunity{border-left-color:#43A3A3}.cc-quick-win{border-left-color:#77C7C9}
.cc-early-hurdle{border-left-color:#231F20}.cc-pitfall{border-left-color:#A10009}
.cc-pitfall .cc-t{color:#A10009}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .cc-early-hurdle{border-left-color:#F9F9F2}:root:not([data-theme="light"]) .cc-pitfall .cc-t{color:#F9F9F2}}
:root[data-theme="dark"] .cc-early-hurdle{border-left-color:#F9F9F2}:root[data-theme="dark"] .cc-pitfall .cc-t{color:#F9F9F2}
.cc-sol{background:var(--zebra);border-radius:var(--r-sm);padding:6px 8px}
.src-inline{display:block;font-size:11.5px;line-height:1.35;color:var(--muted);opacity:.85;margin-top:3px;font-weight:400}
#recList table th[scope="row"]{min-width:220px}

/* Key metrics: bold + teal; marker underline inside the short answer; key-number callout */
b.kv{font-weight:750;color:var(--heading);white-space:nowrap}
.answer b.kv,.ann b.kv,.ann-paper b.kv{color:inherit;font-weight:800;background:linear-gradient(transparent 62%,rgba(67,163,163,.38) 62%);padding:0 1px}
.answer{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px 22px;align-items:center}
.answer-key{display:flex;flex-direction:column;align-items:flex-end;text-align:right;border-left:3px solid #43A3A3;padding:4px 0 4px 18px;max-width:240px}
.ak-v{font-size:34px;line-height:1.05;font-weight:900;font-style:italic;letter-spacing:-.01em;color:var(--on-fill)}
.ak-l{font-size:12px;line-height:1.3;font-weight:600;margin-top:4px;color:var(--on-fill)}
@media (max-width:640px){.answer{grid-template-columns:minmax(0,1fr)}.answer-key{align-items:flex-start;text-align:left;border-left:0;border-top:3px solid #43A3A3;padding:10px 0 0;max-width:none}.ak-v{font-size:28px}}
.ocv-box li b.kv,.takeaways b.kv{color:var(--heading)}
.sc-p b.kv{color:inherit;font-weight:750}

.page-h .badge{white-space:normal;max-width:100%;overflow-wrap:anywhere}

/* OC Vibe staff calculator */
.calc-box{margin:14px 0 0;border:2px solid var(--heading);border-radius:var(--r-lg);background:var(--surface-card);padding:18px 20px}
.calc-box h3{margin:0 0 4px;color:var(--heading);font-size:19px}
.calc-sub{margin:0 0 14px;font-size:14px;line-height:1.45}
.calc-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:20px}
@media (max-width:900px){.calc-grid{grid-template-columns:minmax(0,1fr)}}
.calc-in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px 14px;align-content:start}
@media (max-width:640px){.calc-in{grid-template-columns:minmax(0,1fr)}}
.calc-f{display:flex;flex-direction:column;gap:4px;font-size:13px;font-weight:600}
.calc-w{display:flex;align-items:center;gap:6px;border:1px solid var(--border);border-radius:var(--r-sm);padding:0 10px;background:var(--surface-page)}
.calc-w i{font-style:normal;font-weight:600;color:var(--heading)}
.calc-f input{font:inherit;font-size:15px;font-weight:500;border:0;background:transparent;color:var(--ink);padding:8px 0;width:100%;min-width:0}
.calc-note{grid-column:1/-1}.calc-note input{border:1px solid var(--border);border-radius:var(--r-sm);padding:8px 10px;background:var(--surface-page)}
.calc-f input:focus-visible,.calc-w:focus-within{outline:2px solid var(--focus);outline-offset:1px}
.calc-acts{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px}
.calc-status{grid-column:1/-1;font-size:13px;margin:0}
.calc-out h4{margin:12px 0 6px;font-size:14px;color:var(--heading)}
.calc-hl{margin:0;padding-left:18px;font-size:13px;display:grid;gap:4px}

/* What this means for OC Vibe */
.ocv-box{margin:14px 0 0;border:1px solid var(--border);border-left:6px solid #43A3A3;border-radius:var(--r-md);background:var(--surface-card);padding:14px 18px}
.ocv-box h3{margin:0 0 8px;font-size:17px;color:var(--heading)}
.ocv-box ul{margin:0;padding-left:20px;display:grid;gap:6px}
.ocv-box li{font-size:15px;line-height:1.45}

/* Export chooser */
.exp-dlg{border:1px solid var(--border);border-radius:var(--r-lg);background:var(--surface-card);color:var(--ink);padding:22px 24px;width:min(460px,calc(100vw - 32px));max-height:calc(100vh - 48px);overflow:auto;font-family:var(--font-sans)}
.exp-dlg::backdrop{background:rgba(35,31,32,.55)}
.exp-dlg h3{margin:0 0 4px;color:var(--heading);font-size:20px}
.exp-sub{margin:0 0 14px;font-size:14px}
.exp-dlg fieldset{border:0;padding:0;margin:0 0 14px}
.exp-dlg legend{font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--heading);margin-bottom:8px}
.exp-fmt label{display:flex;gap:8px;align-items:center;font-size:15px;padding:4px 0}
.exp-quick{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}
.exp-list{display:grid;gap:2px;border:1px solid var(--border-subtle);border-radius:var(--r-md);padding:6px}
.exp-item{display:flex;gap:10px;align-items:center;padding:7px 8px;border-radius:var(--r-sm);font-size:15px;cursor:pointer}
.exp-item:hover{background:var(--zebra)}
.exp-dlg input[type=checkbox],.exp-dlg input[type=radio]{width:18px;height:18px;accent-color:#125C60;flex:none}
.exp-count{font-size:13px;margin:8px 0 0}
.exp-acts{display:flex;justify-content:flex-end;gap:10px}
.exp-acts .ctl:disabled{opacity:.5;cursor:not-allowed}

/* Selected tab: filled pill so the active section is obvious */
.tabs{gap:4px!important;padding:6px 0}
.tab{padding:8px 14px!important;border-radius:var(--pill);border-bottom:0!important}
.tab:hover{background:var(--surface-fill);color:var(--on-fill)}
.tab[aria-current="true"]{background:var(--cta-bg);color:var(--cta-ink)!important;font-weight:750}
.tab:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tab[aria-current="true"]{background:#43A3A3;color:#231F20!important}}
:root[data-theme="dark"] .tab[aria-current="true"]{background:#43A3A3;color:#231F20!important}

/* ---- OC Vibe additions (VA Branded tokens only) ---- */
.ann-bar{grid-template-columns:minmax(96px,150px) minmax(0,1fr) 64px}
.ann-bar .l{white-space:normal;overflow:visible;line-height:1.2}
.sec-more{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:24px;align-items:start}
.sec-more > *{min-width:0}
.sec-more .wide{grid-column:1 / -1}
@media (max-width:1000px){.sec-more{grid-template-columns:minmax(0,1fr)}}
.chartf{background:var(--surface-card);border:1px solid var(--border-subtle);border-radius:var(--r-md);padding:16px 18px;margin:0}
.chartf h3{margin:0 0 4px;font-size:17px;line-height:1.25;font-weight:700;color:var(--heading);text-wrap:balance}
.chartf .csub2{margin:0 0 14px;font-size:13px;font-weight:350;line-height:1.35}
.chartf .src{margin-top:10px}
.hbars{display:grid;grid-template-columns:minmax(90px,max-content) minmax(60px,1fr) max-content;gap:8px 12px;align-items:center}
.hbars .l{font-size:13px;font-weight:600;line-height:1.2;max-width:22ch}
.hbars .t{height:16px;position:relative}
.hbars .f{position:absolute;left:0;top:0;bottom:0;background:var(--ESC4);border:1px solid var(--ESC3);border-radius:2px}
.hbars .hi .f,.hbars .f.hi{background:var(--ESC1);border-color:var(--ESC1)}
.hbars .v{font-size:13px;font-weight:750;font-variant-numeric:tabular-nums;text-align:right}
.vcols{display:flex;align-items:flex-end;gap:6px;height:210px;padding-top:6px;border-bottom:1px solid color-mix(in srgb,var(--grid) 35%,transparent)}
.vcol{flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:4px}
.vcol .bv{font-size:11.5px;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.vcol .b{width:78%;background:var(--ESC1);border:1px solid var(--ESC1);border-radius:2px 2px 0 0}
.vcol.fc .b{background:var(--ESC4);border:1.5px dashed var(--ESC3)}
.vcol.hi .b{background:var(--ESC3);border-color:var(--ESC3)}
.vlabs{display:flex;gap:6px;margin-top:6px}
.vlabs span{flex:1 1 0;min-width:0;text-align:center;font-size:11.5px;font-weight:600}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin:10px 0 0;font-size:12px;font-weight:600}
.legend i{display:inline-block;width:14px;height:10px;margin-right:6px;vertical-align:-1px;border-radius:2px}
.legend .a{background:var(--ESC1)} .legend .h{background:var(--ESC3)} .legend .f{background:var(--ESC4);border:1.5px dashed var(--ESC3)}
.notes-box{background:var(--surface-card);border:1px solid var(--border-subtle);border-radius:var(--r-md);padding:16px 18px;margin-top:24px}
.notes-box h3{margin:0 0 8px;font-size:15px;font-weight:700;color:var(--heading)}
.notes-box ul{margin:0;padding-left:18px;display:grid;gap:6px}
.notes-box li{font-size:14px;font-weight:350;line-height:1.45}
.sec-warn{border:1.5px solid var(--P3);border-radius:var(--r-md);padding:10px 14px;margin:16px 0 0;font-size:14px;line-height:1.4;background:var(--surface-card)}
.sec-warn b{color:var(--unfav)}
tr.hirow td,tr.hirow th{background:var(--surface-fill)!important;color:var(--on-fill);font-weight:700}
.src-list{display:grid;gap:12px;margin:0;padding:0;list-style:none}
.src-item{border:1px solid var(--border-subtle);border-radius:var(--r-md);padding:12px 14px;background:var(--surface-card)}
.src-item h4{margin:0 0 4px;font-size:15px;font-weight:700;color:var(--heading)}
.src-item p{margin:0 0 8px;font-size:13.5px;font-weight:350;line-height:1.4}
.src-acts{display:flex;flex-wrap:wrap;gap:8px}
.src-acts a{font-size:13px;font-weight:700;color:var(--heading);text-underline-offset:3px}
.src-acts .dl{font:inherit;font-size:13px;font-weight:700;color:var(--cta-ink);background:var(--cta-bg);border:1.5px solid var(--cta-bg);border-radius:var(--r-sm);padding:6px 10px;cursor:pointer}
.src-acts .dl:focus-visible,.src-acts a:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.src-acts .pend{font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--P3);color:var(--unfav);border-radius:var(--r-sm);padding:4px 8px}
.dq{margin:0;padding-left:18px;display:grid;gap:6px}
.dq li{font-size:14px;font-weight:350;line-height:1.45}
.qa-row.warnrow .qa-q::after{content:" · partial";font-weight:600;font-size:12px;color:var(--unfav)}

/* Newsroom structure (Oct. 13, 2026): news report, details cards, analysis band, up next */
.page,.page [id]{scroll-margin-top:var(--navh,120px)}
.kind{display:inline-block;font-weight:800;color:#FFFFFF;background:#125C60;border-radius:3px;padding:1px 7px;margin-right:2px;letter-spacing:.1em}
.art-lede .dline{font-weight:800;color:var(--heading);letter-spacing:.02em}
.nut{margin:14px 0 0;padding:12px 16px;border:1px solid var(--border);border-top:3px solid var(--heading);background:var(--surface-card);border-radius:var(--r-md)}
.nut-l{display:block;font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--heading);margin-bottom:4px}
.nut p{margin:0;font-size:16px;line-height:1.55}
.art-w5h{max-width:none;margin:20px 0 0}
.d-sub{margin:-4px 0 12px;font-size:13.5px;color:var(--muted)}
.dgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
@media (max-width:1000px){.dgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.dgrid{grid-template-columns:minmax(0,1fr)}}
.dcard{display:flex;flex-direction:column;gap:4px;background:var(--surface-card);border:1px solid var(--border);border-top:4px solid #43A3A3;border-radius:var(--r-md);padding:14px 16px;min-width:0}
.dcard .dk{font-size:11.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--heading)}
.dcard .dfig{font-size:clamp(24px,2.6vw,32px);line-height:1.08;font-weight:900;font-style:italic;color:var(--heading);overflow-wrap:anywhere}
.dcard .dfl{font-size:13.5px;font-weight:700;line-height:1.35}
.dcard p{margin:6px 0 2px;font-size:14px;line-height:1.5;border-top:1px solid var(--border-subtle);padding-top:8px}
.dcard .src-inline{margin-top:auto}
.an-band{margin:28px 0 4px;padding:14px 0 10px;border-top:3px double var(--heading);border-bottom:1px solid var(--border)}
.an-band .kind{font-size:11.5px;text-transform:uppercase}
.an-band h3{margin:8px 0 4px;font-size:22px;font-weight:900;font-style:italic;color:var(--heading)}
.an-band p{margin:0;font-size:14.5px;color:var(--muted)}
.upnext{margin:26px 0 6px;padding:16px 18px;border:1px solid var(--border);border-top:4px solid #43A3A3;border-radius:var(--r-md);background:var(--surface-card);display:grid;grid-template-columns:auto 1fr;gap:4px 14px;align-items:center}
.upnext .un-k{font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.upnext .un-b{justify-self:start;font:inherit;font-size:19px;font-weight:900;font-style:italic;color:var(--heading);background:none;border:0;padding:0;cursor:pointer;text-align:left}
.upnext .un-b:hover,.upnext .un-b:focus-visible{text-decoration:underline}
.upnext p{grid-column:1/-1;margin:2px 0 0;font-size:14.5px;line-height:1.5}
@media print{.upnext{display:none}}
@media (max-width:640px){.calc-steps .scroll{overflow-x:auto}.calc-steps table{min-width:540px}}
.art-body .calc-steps{margin-top:14px}

/* Layout v18 (Oct. 13, 2026): full-width headlines, stacked full-width reading, horizontal stat strips, no side columns */
.art-h{max-width:none}
.art-head{font-size:clamp(24px,2.85vw,44px);line-height:1.08;text-wrap:pretty;max-width:none}
.art-dek{font-size:clamp(16px,1.35vw,19px);max-width:none}
.art-lede-wrap{display:grid;gap:22px}
.qs-q{font-size:clamp(18px,1.6vw,22px)!important;font-weight:750;color:var(--heading);line-height:1.3!important;margin:2px 0 14px!important}
.qs-al{display:block;margin-top:2px}
.art-nums{margin-top:26px}
.data-jump{margin-top:18px}
.seg-h{margin-top:56px!important}
.art-lede-wrap .answer,.art-lede-wrap .nut{margin:0}
.art-lede .answer-t p{font-size:clamp(15.5px,1.2vw,17.5px);line-height:1.55}
.nut p{font-size:clamp(15px,1.15vw,17px)}
.art-nums{margin:18px 0 0}
.art-nums h3{margin:0 0 10px;font-size:17px;color:var(--heading)}
.art-nums .nums{display:flex;flex-wrap:wrap;gap:12px;align-items:stretch}.art-nums .nums>*{flex:1 1 210px;min-width:0}
.art-nums .art-stat,.art-nums .art-stat:first-of-type{display:flex;flex-direction:column;gap:3px;margin:0;border:1px solid var(--border);border-top:3px solid #43A3A3;border-radius:var(--r-md);background:var(--surface-card);padding:12px 14px!important}
.art-nums .art-stat .src-inline{margin-top:auto}
.calc-steps{margin-top:18px}
.ann-h{max-width:none!important;font-size:clamp(26px,2.85vw,46px);text-wrap:pretty!important}
.ann-dek{max-width:none!important;font-size:clamp(16px,1.4vw,20px)}
.ann-nums{margin:4px 0 16px;border-top:1px solid var(--ESC4);padding-top:12px}
.ann-nums h3{margin:0 0 8px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--DARK)!important}
.ann-strip{display:flex;flex-wrap:wrap;gap:10px}.ann-strip>*{flex:1 1 180px;min-width:0}
.ann-strip .ann-stat,.ann-strip .ann-stat:last-child{border:1px solid var(--ESC4);border-top:3px solid var(--ESC3);border-radius:var(--r-sm);padding:10px 12px}
.ann-cols{columns:3 300px;column-gap:30px;column-rule:1px solid var(--ESC4);border-top:1px solid var(--ESC4);padding-top:14px}
.ann-wide{margin:8px 0 0}
.ann-wide .ann-bars{grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));column-gap:32px;row-gap:8px}
.ann-wide .ann-bar{grid-template-columns:minmax(120px,210px) minmax(0,1fr) 64px}
@media (max-width:640px){.ann-paper{padding:16px 14px}.ann-strip>*,.art-nums .nums>*{flex-basis:140px}.ann-strip .ann-stat b{font-size:22px}.art-nums .art-stat .as-v{font-size:22px}}


/* Data infographics (Oct. 13, 2026): "At a glance" block in each news report */
.ig-wrap{margin:18px 0 0;display:grid;gap:14px}
.ig-wrap.two{grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr))}
.ig-wrap .ig-k{grid-column:1/-1;margin:0;font-size:17px;color:var(--heading)}
.ig{margin:0;background:var(--surface-card);border:1px solid var(--border);border-top:4px solid var(--ESC3);border-radius:var(--r-md);padding:16px 18px 12px;min-width:0}
.ig-h h4{margin:0;font-size:clamp(17px,1.4vw,21px);font-weight:900;font-style:italic;color:var(--heading);line-height:1.2}
.ig-h p{margin:3px 0 12px;font-size:13px;color:var(--muted)}
.ig-src{margin:10px 0 0;font-size:11.5px;color:var(--muted)}
.ig-calc{margin:6px 0 0;font-size:12.5px}
.ig .grow{display:block;height:100%;background:var(--ESC1);border-radius:3px;transform-origin:left center}
.ig .grow-y{display:block;width:100%;background:var(--ESC4);border-radius:4px 4px 0 0;transform-origin:center bottom;align-self:flex-end}
@media (prefers-reduced-motion:no-preference){
  .ig .grow,.ig .grow-y{transition:transform .9s cubic-bezier(.2,.7,.2,1) calc(var(--i,0)*110ms)}
  .js-anim .ig:not(.in) .grow{transform:scaleX(0)}
  .js-anim .ig:not(.in) .grow-y{transform:scaleY(0)}
  .ig .wf-grid span.on{transition:background-color .25s ease calc(var(--i,0)*9ms)}
  .js-anim .ig:not(.in) .wf-grid span.on{background:var(--border)}
  .ig .ch-step,.ig .ch-link,.ig .rc-ln,.ig .bd-r,.ig .fn-s,.ig .vs-r,.ig .pp{transition:opacity .45s ease calc(var(--i,0)*140ms),transform .45s ease calc(var(--i,0)*140ms)}
  .js-anim .ig:not(.in) :is(.ch-step,.ch-link,.rc-ln,.bd-r,.fn-s,.vs-r){opacity:0;transform:translateY(8px)}
}
/* chain */
.ig-chain{list-style:none;margin:0;padding:0;display:flex;align-items:stretch;gap:0}
.ch-step{flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:4px;background:var(--surface-page);border:1px solid var(--border);border-radius:var(--r-md);padding:12px}
.ch-v{font-size:clamp(22px,2.2vw,32px);font-weight:900;font-style:italic;color:var(--heading);line-height:1.05;font-variant-numeric:tabular-nums}
.ch-l{font-size:13.5px;font-weight:700;line-height:1.3}
.ch-link{flex:0 0 118px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:0 6px;text-align:center}
.ch-arrow{display:block;width:100%;height:3px;background:var(--ESC1);position:relative}
.ch-arrow::after{content:"";position:absolute;right:-1px;top:-5px;border:6.5px solid transparent;border-left:9px solid var(--ESC1);border-right:0}
.ch-t{font-size:11.5px;line-height:1.3;font-weight:600}
@media (max-width:1100px){.ig-chain{flex-direction:column}.ch-link{flex:none;flex-direction:row;padding:6px 0 6px 18px;text-align:left;gap:10px}.ch-arrow{width:3px;height:26px;flex:none}.ch-arrow::after{right:-5px;top:auto;bottom:-1px;border:6.5px solid transparent;border-top:9px solid var(--ESC1);border-bottom:0}}
/* waffle */
.ig-waffles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px}
.wf{margin:0;display:flex;flex-direction:column;gap:8px}
.wf-grid{display:grid;grid-template-columns:repeat(10,1fr);gap:3px;max-width:240px}
.wf-grid span{aspect-ratio:1;border-radius:2px;background:var(--border)}
.wf-grid span.on{background:var(--ESC1)}
.wf figcaption{font-size:14px;line-height:1.35}
.wf figcaption b{font-size:24px;font-weight:900;font-style:italic;color:var(--heading);display:block}
.wf small{display:block;font-size:11.5px;color:var(--muted);margin-top:3px}
@media (max-width:640px){.ig-waffles{grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.wf-grid{gap:2px}.wf figcaption{font-size:12px}.wf figcaption b{font-size:18px}.wf small{font-size:10.5px}}
/* receipt */
.ig-receipt{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:22px;align-items:start}
@media (max-width:900px){.ig-receipt{grid-template-columns:minmax(0,1fr)}}
.rc-paper{background:#FFFFFF;color:#231F20;border:1px solid var(--border);border-radius:4px;padding:14px 18px;box-shadow:0 1px 0 var(--border);background-image:radial-gradient(circle at 8px -2px,var(--surface-card) 6px,transparent 6.5px);background-size:16px 10px;background-repeat:repeat-x;background-position:0 100%}
.rc-h{margin:0 0 10px;font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px dashed #231F20;padding-bottom:8px}
.rc-ln{display:grid;grid-template-columns:auto 1fr auto;gap:2px 8px;align-items:baseline;padding:6px 0;border-bottom:1px dashed #C9C6B8}
.rc-l{font-size:14.5px;font-weight:700}
.rc-dots{border-bottom:2px dotted #C9C6B8;transform:translateY(-4px)}
.rc-ln b{font-size:17px;font-weight:900;font-variant-numeric:tabular-nums;color:#125C60}
.rc-bar{grid-column:1/-1;height:6px;background:#F9F9F2;border-radius:3px;overflow:hidden}
.rc-ln small{grid-column:1/-1;font-size:11.5px}
.rc-tot{display:grid;grid-template-columns:1fr auto;gap:2px 8px;padding-top:10px;margin-top:4px;border-top:3px double #231F20}
.rc-tot span{font-size:15px;font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.rc-tot b{font-size:24px;font-weight:900;font-style:italic;color:#125C60}
.rc-tot small{grid-column:1/-1;font-size:11.5px}
/* every $1 mix */
.rc-mh{margin:0 0 8px;font-size:15px;font-weight:800;color:var(--heading)}
.rc-stack{display:flex;height:34px;border-radius:5px;overflow:hidden;border:1px solid var(--border)}
.rc-seg{display:block;height:100%;transform-origin:left center}
.s0{background:#125C60}.s1{background:#43A3A3}.s2{background:#77C7C9}.s3{background:#B4D9E3}.s4{background:#C9C6B8}
.rc-leg{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:6px}
.rc-leg li{display:flex;align-items:baseline;gap:8px;font-size:14px}
.rc-leg b{font-size:18px;font-weight:900;font-style:italic;color:var(--heading);min-width:3ch}
.rc-leg small{color:var(--muted)}
.sw{width:12px;height:12px;border-radius:2px;flex:none;align-self:center}
@media (prefers-reduced-motion:no-preference){.rc-seg{transition:transform .7s ease calc(var(--i,0)*140ms)}.js-anim .ig:not(.in) .rc-seg{transform:scaleX(0)}}
/* people */
.ig-people{display:flex;flex-wrap:wrap;align-items:center;gap:14px 24px}
.pp-row{display:flex;gap:6px}
.pp{width:clamp(22px,3vw,34px);display:block}
.pp svg{width:100%;height:auto;display:block;fill:var(--border)}
.pp{position:relative}
.pp::after{content:"";position:absolute;inset:0;background:var(--ESC1);clip-path:inset(0 calc((1 - var(--f))*100%) 0 0);-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 48'%3E%3Ccircle cx='12' cy='7' r='6'/%3E%3Cpath d='M3 18a9 9 0 0 1 18 0v14h-4v15h-10V32H3z'/%3E%3C/svg%3E") center/100% 100% no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 48'%3E%3Ccircle cx='12' cy='7' r='6'/%3E%3Cpath d='M3 18a9 9 0 0 1 18 0v14h-4v15h-10V32H3z'/%3E%3C/svg%3E") center/100% 100% no-repeat}
@media (prefers-reduced-motion:no-preference){.pp::after{transition:clip-path .5s ease calc(var(--i,0)*90ms)}.js-anim .ig:not(.in) .pp::after{clip-path:inset(0 100% 0 0)}}
.pp-cap{margin:0;font-size:15px;line-height:1.4;flex:1 1 260px}
.pp-cap b{font-size:clamp(26px,2.6vw,36px);font-weight:900;font-style:italic;color:var(--heading);display:block}
/* towers */
.ig-towers{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px;align-items:end}
.tw{display:flex;flex-direction:column;align-items:center;gap:4px;outline-offset:2px}
.tw-b{height:150px;width:100%;max-width:64px;display:flex;align-items:flex-end;background:repeating-linear-gradient(to bottom,var(--surface-page) 0 8px,transparent 8px 10px);border:1px solid var(--border);border-radius:5px 5px 0 0;overflow:hidden}
.tw.hi .grow-y{background:var(--ESC1)}
.tw b{font-size:14px;font-weight:800;font-variant-numeric:tabular-nums}
.tw span{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
/* share */
.sh-bar{height:28px;background:var(--ESC4);border-radius:5px;overflow:hidden;border:1px solid var(--border)}
.sh-bar .grow{background:var(--ESC3);border-radius:0}
.sh-leg{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 18px;margin-top:8px;font-size:14px}
.sh-leg b{font-size:20px;font-weight:900;font-style:italic;color:var(--heading)}
/* departure board */
.ig-board{background:#125C60;color:#FFFFFF;border-radius:var(--r-md);padding:10px 14px;font-variant-numeric:tabular-nums}
.ig-board *{color:#FFFFFF}
.bd-h,.bd-r{display:grid;grid-template-columns:62px minmax(0,1fr) minmax(130px,34%);gap:10px;align-items:center;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.25)}
.bd-h{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;opacity:.85}
.bd-route{font-size:17px;font-weight:900;background:#43A3A3;border-radius:4px;text-align:center;padding:2px 0}
.bd-d{font-size:14px;font-weight:600}
.bd-n{display:flex;align-items:center;gap:8px}
.bd-bar{flex:1;height:8px;background:rgba(255,255,255,.18);border-radius:4px;overflow:hidden}
.bd-bar .grow{background:#B4D9E3}
.bd-n b{font-size:18px;font-weight:900;min-width:3ch;text-align:right}
.bd-t{border-bottom:0}.bd-t .bd-route{background:#FFFFFF;color:#125C60!important}
.ig-extra{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-top:10px}
.ig-extra div{border:1px solid var(--border);border-radius:var(--r-sm);padding:8px 10px;display:flex;flex-direction:column}
.ig-extra b{font-size:20px;font-weight:900;font-style:italic;color:var(--heading)}
.ig-extra span{font-size:12.5px;line-height:1.3}
/* funnel */
.ig-funnel{display:grid;gap:8px}
.fn-s{width:var(--w);min-width:min(100%,250px);margin:0 auto;background:var(--ESC4);color:#231F20;clip-path:polygon(0 0,100% 0,96% 100%,4% 100%);padding:12px 8%;text-align:center;display:flex;flex-direction:column}
.fn-s+.fn-s{background:var(--ESC1)}
.fn-s *{color:#231F20}
.fn-s b{font-size:clamp(22px,2.4vw,32px);font-weight:900;font-style:italic}
.fn-s span{font-size:13px;font-weight:700}
.fn-rates{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:4px}
.fn-rates div{border:1px solid var(--border);border-top:3px solid var(--ESC3);border-radius:var(--r-sm);padding:8px 10px;display:flex;flex-direction:column}
.fn-rates b{font-size:24px;font-weight:900;font-style:italic;color:var(--heading)}
.fn-rates span{font-size:13px;font-weight:700}.fn-rates small{font-size:11.5px}
/* versus */
.ig-vs{display:grid;gap:12px}
.vs-r{display:grid;grid-template-columns:minmax(150px,26%) minmax(0,1fr);gap:12px;align-items:center}
.vs-l{font-size:14px;font-weight:700}
.vs-bars{display:grid;gap:4px}
.vs-b{position:relative;height:26px;background:#F9F9F2;border:1px solid var(--border);border-radius:4px;overflow:hidden}
.vs-b .grow{height:100%}
.vs-b.b .grow{background:var(--ESC4)}
.vs-b em{position:absolute;left:8px;top:50%;transform:translateY(-50%);font-style:normal;font-size:12.5px;font-weight:600;color:#231F20;white-space:nowrap}
.vs-b em b{font-weight:900}
@media (max-width:640px){.vs-r{grid-template-columns:minmax(0,1fr)}.ig-towers{gap:4px}.tw-b{height:110px}.tw span{font-size:10.5px}.tw b{font-size:12px}.bd-h,.bd-r{grid-template-columns:48px minmax(0,1fr) 90px}.bd-d{font-size:12.5px}.ig{padding:14px 12px 10px}}
@media print{.ig .grow,.ig .grow-y{transform:none!important}.ig :is(.ch-step,.ch-link,.rc-ln,.bd-r,.fn-s,.vs-r){opacity:1!important;transform:none!important}}

/* Maps (Oct. 13, 2026) */
.mp-wrapall{display:grid;gap:14px;margin:16px 0 0}
.mp{margin:0;background:var(--surface-card);border:1px solid var(--border);border-top:4px solid var(--ESC3);border-radius:var(--r-md);padding:16px 18px 12px;min-width:0}
.mp-grid{display:grid;grid-template-columns:minmax(0,2.4fr) minmax(220px,1fr);gap:18px;align-items:start}
@media (max-width:900px){.mp-grid{grid-template-columns:minmax(0,1fr)}}
.mp-canvas{background:var(--surface-page);border-radius:var(--r-sm);padding:6px}
.mp-svg{display:block;width:100%;height:auto}
.mp-svg [data-tip]{cursor:pointer;outline:none}.mp-svg .mp-b:focus,.mp-svg .mp-st:focus{stroke:#231F20;stroke-width:2.5}
:root[data-theme="dark"] :is(.mp-canvas,.mp-key),:root:not([data-theme="light"]) :is(.mp-canvas,.mp-key){--mp-land:#3a4a4b;--mp-line:#1d2324;--mp-ink:#F9F9F2;--mp-halo:#1d2324;--mp-val:#B4D9E3;--mp-b0:#B4D9E3;--mp-b1:#43A3A3;--mp-b2:#2E6E72}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) :is(.mp-canvas,.mp-key){--mp-land:#E9EBE4;--mp-line:#FFFFFF;--mp-ink:#231F20;--mp-halo:#FFFFFF;--mp-val:#125C60;--mp-b0:#125C60;--mp-b1:#43A3A3;--mp-b2:#B4D9E3}}
:root[data-theme="light"] :is(.mp-canvas,.mp-key){--mp-land:#E9EBE4;--mp-line:#FFFFFF;--mp-ink:#231F20;--mp-halo:#FFFFFF;--mp-val:#125C60;--mp-b0:#125C60;--mp-b1:#43A3A3;--mp-b2:#B4D9E3}
.mp-key{font-size:13.5px}
.mp-kh{margin:0 0 6px;font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--heading)}
.mp-bins{list-style:none;margin:0 0 12px;padding:0;display:grid;gap:4px}.mp-bins li{display:flex;gap:8px;align-items:center}
.mp-bins .sw{width:14px;height:14px;border-radius:3px;flex:none}.sw.b0{background:var(--mp-b0,#125C60)}.sw.b1{background:var(--mp-b1,#43A3A3)}.sw.b2{background:var(--mp-b2,#B4D9E3)}.sw.land{background:#E9EBE4;border:1px solid var(--border)}
.mp-top{margin:0 0 10px;padding-left:20px;display:grid;gap:4px}.mp-top b{font-weight:900;color:var(--heading)}
.mp-note{margin:0;font-size:12px;display:flex;gap:6px;align-items:center}.mp-hk{width:10px;height:10px;background:#A10009;transform:rotate(45deg);display:inline-block}
@media (prefers-reduced-motion:no-preference){.mp-b{transform-box:fill-box;transform-origin:center;transition:transform .7s cubic-bezier(.2,.7,.2,1) calc(var(--i,0)*70ms)}.js-anim .mp:not(.in) .mp-b{transform:scale(0)}
  .mp-st{transition:opacity .6s ease}.js-anim .mp:not(.in) .mp-st{opacity:.15}}
@media print{.mp-b{transform:none!important}.mp-st{opacity:1!important}}
/* Key takeaways (overview) */
.kts{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 22px}.kts>.kt{flex:1 1 240px;min-width:0}
.kt{display:flex;flex-direction:column;gap:3px;text-align:left;font:inherit;color:inherit;background:var(--surface-card);border:1px solid var(--border);border-top:4px solid var(--ESC1);border-radius:var(--r-md);padding:14px 16px;cursor:pointer}
.kt:hover,.kt:focus-visible{border-color:var(--heading);box-shadow:0 2px 10px rgba(18,92,96,.15)}
.kt-k{font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--heading)}
.kt-v{font-size:clamp(28px,2.6vw,38px);font-weight:900;font-style:italic;color:var(--heading);line-height:1.05}
.kt-l{font-size:13.5px;font-weight:800}
.kt-h{font-size:14.5px;line-height:1.4;margin-top:4px}
.kt-s{font-size:11.5px;color:var(--muted);margin-top:2px}
.kt-go{margin-top:auto;padding-top:8px;font-size:13px;font-weight:800;color:var(--heading)}
.kv{font-weight:850!important}
/* More data and notes: called out so readers do not skip it */
.more-d{border:2px solid var(--heading)!important;background:var(--surface-card)}
.more-d>summary{list-style:none;display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:center;padding:14px 18px!important;background:linear-gradient(90deg,rgba(67,163,163,.16),rgba(180,217,227,.12))}
.more-d>summary::-webkit-details-marker{display:none}
.md-ic{width:34px;height:34px;border-radius:50%;background:var(--ESC3);color:#FFFFFF;display:grid;place-items:center;font-size:22px;font-weight:800;line-height:1}
.more-d[open] .md-ic{transform:rotate(45deg)}
.md-t{display:flex;flex-direction:column;gap:2px}.md-t b{font-size:17px;color:var(--heading)}.md-s{font-size:13.5px;font-weight:500;color:var(--ink)}
.md-btn{font-size:13px;font-weight:800;color:#FFFFFF;background:var(--ESC3);border-radius:999px;padding:7px 16px}
.more-d .md-close{display:none}.more-d[open] .md-close{display:inline}.more-d[open] .md-open{display:none}
@media (prefers-reduced-motion:no-preference){.more-d:not([open]) .md-ic{animation:mdpulse 2.4s ease-in-out 2}}
@keyframes mdpulse{0%,100%{box-shadow:0 0 0 0 rgba(67,163,163,.55)}50%{box-shadow:0 0 0 9px rgba(67,163,163,0)}}
@media (max-width:640px){.more-d>summary{grid-template-columns:auto minmax(0,1fr)}.md-btn{grid-column:1/-1;justify-self:start}}
/* Up next: stands out */
.upnext{background:var(--ESC3)!important;border:0!important;color:#FFFFFF;padding:22px 24px!important;grid-template-columns:minmax(0,1fr) auto!important;gap:6px 20px!important;box-shadow:0 6px 20px rgba(18,92,96,.25)}
.upnext *{color:#FFFFFF}
.upnext .un-k{grid-column:1/-1;opacity:.9;color:#B4D9E3!important}
.upnext .un-b{grid-column:2;grid-row:2;align-self:center;background:#FFFFFF;color:#125C60!important;border-radius:999px;padding:12px 22px!important;font-size:18px!important;font-style:normal!important;box-shadow:0 2px 0 rgba(0,0,0,.15)}
.upnext .un-b *{color:#125C60!important}
.upnext .un-b:hover,.upnext .un-b:focus-visible{text-decoration:none!important;outline:3px solid #B4D9E3;outline-offset:2px}
.upnext p{grid-column:1;grid-row:2;font-size:15.5px!important;margin:0!important}
@media (max-width:640px){.upnext{grid-template-columns:minmax(0,1fr)!important}.upnext .un-b{grid-column:1;grid-row:auto;justify-self:start}}
footer a{color:inherit;font-weight:800}
.exp-link{margin:10px 0 0}.exp-link label{display:block;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px}.exp-link input{width:100%;font:inherit;font-size:14px;padding:8px 10px;border:1.5px solid var(--ctl);border-radius:var(--r-sm);background:var(--surface-card);color:var(--ink)}
/* Update schedule (Oct. 14, 2026) */
.upd-bar{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:center;width:100%;margin:14px 0 4px;padding:14px 18px;text-align:left;font:inherit;color:inherit;cursor:pointer;background:var(--surface-card);border:2px solid var(--heading);border-left-width:8px;border-radius:var(--r-md)}
.upd-bar:hover{background:linear-gradient(90deg,rgba(67,163,163,.14),rgba(180,217,227,.08))}
.upd-bar:focus-visible{outline:3px solid var(--heading);outline-offset:2px}
.upd-ic{width:38px;height:38px;border-radius:50%;background:var(--heading);color:var(--surface-card);display:grid;place-items:center;font-size:22px;font-weight:900}
.upd-t{display:grid;gap:3px;font-size:14px}.upd-t>b{font-size:17px;font-weight:900;color:var(--heading)}.upd-t span b{font-weight:800;color:var(--heading)}
.upd-go{font-weight:800;color:var(--heading);white-space:nowrap;font-size:14px}
@media (max-width:640px){.upd-bar{grid-template-columns:auto minmax(0,1fr)}.upd-go{grid-column:2}}
.upd-lede{font-size:16px;margin:0 0 14px;max-width:none}
.upd-box .dgrid{margin:0 0 16px}
.upd-box .tbl-cap{margin-top:14px}
"""

EXTRA_CSS += r"""
/* D3 visuals (Oct. 14, 2026): colors by class for light and dark */
.d3f svg{width:100%;height:auto;display:block;margin-top:8px}
.d3s{position:relative}
.x6s{overflow-x:auto;overflow-y:hidden}
@media (max-width:760px){.ig-antv .igc{min-width:720px}}
@media (max-width:760px){.d3s{overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:6px}.d3s>svg{min-width:720px}.d3s::before{content:'Swipe sideways to see the full chart \2192';display:block;font-size:12px;font-weight:700;color:var(--muted, #6b6560);margin:4px 0 2px;position:sticky;left:0}}
.d3vz text{font-family:var(--font-sans);fill:var(--ink)}
.d3vz .lbl{font-size:13px;font-weight:700}
.d3vz .m{font-size:15px;font-weight:800;fill:var(--heading)}
.d3vz .mu{font-size:12px}
.d3vz .axl{stroke:var(--border);stroke-width:2}
.d3vz .tk{stroke:var(--border);stroke-width:1.5}
.d3vz .tkl{font-size:11px;opacity:.85}
.d3vz .val{font-size:12.5px;font-weight:700}
.d3vz .val.hi{font-weight:900;fill:var(--heading)}
.d3vz .rowbg{fill:transparent}
.d3vz .d3-row{cursor:pointer;outline:none}
.d3vz .d3-row:hover .rowbg,.d3vz .d3-row:focus-visible .rowbg{fill:rgba(67,163,163,.12);stroke:#43A3A3;stroke-width:1.5}
.d3vz .dot{stroke:var(--surface-card);stroke-width:2}
.d3vz .g-anaheim{fill:#125C60}.d3vz .g-gardengrove{fill:#43A3A3}.d3vz .g-orangecounty{fill:#77C7C9}.d3vz .g-california{fill:var(--surface-card);stroke:var(--ink);stroke-width:2.5}.d3vz .g-us{fill:#231F20}
.d3vz .tmh{font-size:15px;font-weight:800;fill:var(--heading)}
.d3vz .tm.c0{fill:#125C60}.d3vz .tm.c1{fill:#43A3A3}.d3vz .tm.c2{fill:#77C7C9}.d3vz .tm.c3{fill:#B4D9E3}.d3vz .tm.c4{fill:#8A8580}
.d3vz .tml{font-size:14px;font-weight:800}.d3vz .tmv{font-size:13px;font-weight:700}
.d3vz text.c0{fill:#FFFFFF}.d3vz text.c1,.d3vz text.c2,.d3vz text.c3,.d3vz text.c4{fill:#231F20}
.d3vz rect.tm.is-hot,.d3vz circle.dot.is-hot{stroke:var(--ink);stroke-width:3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .d3vz .g-anaheim{fill:#B4D9E3}:root:not([data-theme="light"]) .d3vz .g-us{fill:#F9F9F2}
 :root:not([data-theme="light"]) .d3vz .tm.c0{fill:#B4D9E3}:root:not([data-theme="light"]) .d3vz text.c0{fill:#231F20}:root:not([data-theme="light"]) .d3vz .tm.c2{fill:#3E6E70}:root:not([data-theme="light"]) .d3vz .tm.c3{fill:#2E4F50}:root:not([data-theme="light"]) .d3vz .tm.c4{fill:#6B6560}
 :root:not([data-theme="light"]) .d3vz text.c2,:root:not([data-theme="light"]) .d3vz text.c3,:root:not([data-theme="light"]) .d3vz text.c4{fill:#F9F9F2}}
:root[data-theme="dark"] .d3vz .g-anaheim{fill:#B4D9E3}:root[data-theme="dark"] .d3vz .g-us{fill:#F9F9F2}:root[data-theme="dark"] .d3vz .tm.c0{fill:#B4D9E3}:root[data-theme="dark"] .d3vz text.c0{fill:#231F20}:root[data-theme="dark"] .d3vz .tm.c2{fill:#3E6E70}:root[data-theme="dark"] .d3vz .tm.c3{fill:#2E4F50}:root[data-theme="dark"] .d3vz .tm.c4{fill:#6B6560}:root[data-theme="dark"] .d3vz text.c2,:root[data-theme="dark"] .d3vz text.c3,:root[data-theme="dark"] .d3vz text.c4{fill:#F9F9F2}

/* AntV layer (Oct. 14, 2026) */
.g2c{position:relative;width:100%;min-height:var(--g2h,260px)}
.g2c.g2-on{height:var(--g2h,260px)}
.g2c.g2-on > *{max-width:100%}
.g2-tooltip{font-family:"Sharp Sans Disp No2","Proxima Nova",system-ui,sans-serif!important;font-size:13px!important;border-radius:6px!important}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .g2-tooltip{background:#231F20!important;color:#F9F9F2!important;box-shadow:0 4px 16px rgba(0,0,0,.5)!important}}
:root[data-theme="dark"] .g2-tooltip{background:#231F20!important;color:#F9F9F2!important}
.t8-on{display:block}
.t8-on p,.t8-on div{margin:0!important;font-family:inherit!important}
.answer-t .t8-on{display:inline}
.answer-t .t8-on p{display:inline}
.ig-antv .igc,.ig-x6 .x6c{width:100%;border-radius:8px}
.ig-antv .igc svg{width:100%;height:100%}
.ig-x6 .x6-geo{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 8px}
.ig-x6 .x6c{border:1px solid var(--border-subtle);background:var(--surface-page);overflow:hidden;position:relative}
.ig-antv,.ig-x6{margin-top:18px}
.ig-fb{font-size:14px}

/* More data visible and Up next that draws the eye (Oct. 14, 2026) */
.more-prev{margin-top:26px}
.more-prev .mp-h{margin:0 0 4px;font-size:13px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;color:var(--heading);padding-top:10px;border-top:1px solid var(--border)}
.more-prev .mp-c{margin-left:8px;font-size:12px;letter-spacing:.04em;text-transform:none;font-weight:800;color:#FFFFFF;background:#125C60;border-radius:var(--pill);padding:2px 9px}
.more-prev .sec-more{margin-top:12px;grid-template-columns:repeat(2,minmax(0,1fr))}
@media (max-width:900px){.more-prev .sec-more{grid-template-columns:minmax(0,1fr)}}
details.fold.strong{border:2px solid #125C60;border-left:8px solid #125C60;margin-top:18px}
details.fold.strong>summary{background:linear-gradient(90deg,rgba(67,163,163,.22),rgba(180,217,227,.12))}
details.fold.strong .fd-t b{font-size:18px}
details.fold.strong .fd-btn{background:#125C60;color:#FFFFFF;border-color:#125C60;padding:6px 16px}
details.fold.strong .fd-btn *{color:#FFFFFF}
@media (prefers-reduced-motion:no-preference){details.fold.strong:not([open]) .fd-ic{animation:mdpulse 2.4s ease-in-out 2}}
.seg-chip.hot{border-color:#125C60;background:#125C60;color:#FFFFFF}.seg-chip.hot span{color:#FFFFFF}.seg-chip em{font-style:normal;font-weight:600;opacity:.9}
.data-jump{margin:14px 0 0;font-size:14px!important;padding:8px 14px!important;border:2px solid #125C60!important;color:var(--heading)}
.upnext2{position:relative;margin:48px 0 8px;padding:26px 28px 24px;border-radius:var(--r-md);background:#125C60;color:#FFFFFF;box-shadow:0 10px 28px rgba(18,92,96,.32);display:grid;gap:8px}
.upnext2 *{color:#FFFFFF}
.un2-prog{height:6px;border-radius:3px;background:rgba(255,255,255,.22);overflow:hidden;margin-bottom:6px}.un2-prog span{display:block;height:100%;background:#B4D9E3}
.un2-k{font-size:12px;font-weight:900;letter-spacing:.18em;text-transform:uppercase;color:#B4D9E3!important}
.un2-h{margin:0;font-size:clamp(22px,2.4vw,30px);line-height:1.15;font-weight:900;font-style:italic}
.un2-p{margin:0;font-size:16px;line-height:1.5;max-width:70ch}
.upnext2 .kv,.upnext2 b{color:#FFFFFF!important;background:none!important}
.un2-b{justify-self:start;margin-top:8px;font:inherit;font-size:19px;font-weight:900;background:#FFFFFF;color:#125C60!important;border:0;border-radius:999px;padding:14px 26px;cursor:pointer;box-shadow:0 3px 0 rgba(0,0,0,.18)}
.un2-b *{color:#125C60!important}
.un2-b:hover,.un2-b:focus-visible{outline:3px solid #B4D9E3;outline-offset:3px}
@media (prefers-reduced-motion:no-preference){.un2-b span{display:inline-block;animation:un2nudge 1.6s ease-in-out 3}}
@keyframes un2nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
.next-pill{position:fixed;right:22px;bottom:22px;z-index:60;font:inherit;font-size:15px;font-weight:900;background:#125C60;color:#FFFFFF;border:2px solid #FFFFFF;border-radius:999px;padding:12px 20px;box-shadow:0 8px 24px rgba(0,0,0,.28);cursor:pointer}
.next-pill[hidden]{display:none}
.next-pill:hover,.next-pill:focus-visible{outline:3px solid #B4D9E3;outline-offset:2px}
@media (max-width:640px){.next-pill{right:12px;bottom:12px;font-size:14px;padding:10px 16px}}
@media print{.next-pill,.data-jump{display:none!important}}

/* Newspaper-style segment breaks and folds (Oct. 14, 2026): clean section flags, generous space, supporting detail folded */
.seg-h{display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px;align-items:start;margin:44px 0 18px;padding-top:12px;border-top:3px solid var(--heading);position:relative}
.seg-h::before{content:"";position:absolute;left:0;right:0;top:3px;border-top:1px solid var(--heading)}
.seg-h .seg-n{font-size:12px;font-weight:900;letter-spacing:.08em;color:#FFFFFF;background:var(--ESC3);border-radius:2px;padding:3px 7px;margin-top:3px}
.seg-h h3{margin:0;font-size:13px;font-weight:900;letter-spacing:.18em;text-transform:uppercase;color:var(--heading)}
.seg-h p{margin:4px 0 0;font-size:15px;line-height:1.45;max-width:none}
.art .seg-h:first-of-type{margin-top:28px}
.seg-nav{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0 0;padding-top:12px;border-top:1px solid var(--border-subtle)}
.seg-chip{font:inherit;font-size:12.5px;font-weight:700;padding:5px 10px;border:1px solid var(--border);border-radius:var(--pill);background:var(--surface-card);color:var(--ink);cursor:pointer}
.seg-chip span{display:inline-block;min-width:16px;font-weight:900;color:var(--heading)}
.seg-chip:hover,.seg-chip:focus-visible{border-color:var(--ESC1)}
details.fold{margin:12px 0 0;border:1px solid var(--border);border-left:4px solid var(--ESC1);border-radius:var(--r-sm);background:var(--surface-card)}
details.fold>summary{list-style:none;display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;align-items:center;padding:12px 16px;cursor:pointer}
details.fold>summary::-webkit-details-marker{display:none}
details.fold .fd-ic{font-size:20px;font-weight:800;color:var(--heading);line-height:1;transition:transform .2s}
details.fold[open] .fd-ic{transform:rotate(45deg)}
details.fold .fd-t b{display:block;font-size:16px;color:var(--heading)}
details.fold .fd-t span{display:block;font-size:13.5px;line-height:1.4;margin-top:2px}
details.fold .fd-btn{font-size:13px;font-weight:800;color:var(--heading);border:1.5px solid var(--ESC1);border-radius:var(--pill);padding:4px 12px}
details.fold .fd-close{display:none}details.fold[open] .fd-close{display:inline}details.fold[open] .fd-open{display:none}
details.fold[open]>summary{border-bottom:1px solid var(--border-subtle)}
details.fold .fd-body{padding:6px 16px 16px}
details.fold .fd-body>.calc-steps,details.fold .fd-body>.cc-box{margin-top:8px;border:0;padding:0;background:none}
@media (max-width:640px){details.fold>summary{grid-template-columns:auto minmax(0,1fr)}details.fold .fd-btn{display:none}.seg-h{margin-top:34px}}
@media print{details.fold>summary{display:none}.seg-nav{display:none}}
.find-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0 0 6px}
@media (max-width:900px){.find-row{grid-template-columns:1fr}}
.find-link{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 10px;text-align:left;font:inherit;color:inherit;background:var(--surface-card);border:1px solid var(--border);border-radius:var(--r-sm);padding:10px 14px;cursor:pointer}
.find-link b{font-size:15px;color:var(--heading)}.find-link span{grid-column:1;font-size:13px;line-height:1.35}.find-link .go{grid-column:2;grid-row:1/3;align-self:center;font-weight:800;color:var(--heading);font-size:16px}
.find-link:hover,.find-link:focus-visible{border-color:var(--ESC1)}
.side-quick{margin:14px 16px 0;padding:12px 0 0;border-top:1px solid var(--border-subtle);display:grid;gap:6px}
.side-quick span{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.side-quick button{font:inherit;font-size:14px;font-weight:700;text-align:left;border:1px solid var(--border);border-radius:var(--r-sm);background:var(--surface-card);color:var(--heading);padding:7px 10px;cursor:pointer}
.ov-seg{margin-top:36px}

/* Questions answered and Reports and data library (Oct. 14, 2026) */
.find-band{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0 0 22px}
.find-card{display:flex;flex-direction:column;gap:6px;text-align:left;font:inherit;color:inherit;background:var(--surface-card);border:1px solid var(--border);border-left:6px solid var(--ESC1);border-radius:var(--r-md);padding:16px 18px;cursor:pointer}
.find-card b{font-size:18px;color:var(--heading)}
.find-card span{font-size:14px;line-height:1.45}
.find-card .go{font-weight:800;color:var(--heading);font-size:13.5px}
.find-card:hover,.find-card:focus-visible{border-color:var(--ESC1)}
@media (max-width:760px){.find-band{grid-template-columns:1fr}}
.ask-lede{font-size:16px;line-height:1.55;margin:0 0 14px;max-width:none}
.ask-ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 16px}
.ask-ctl input[type=search]{flex:1 1 260px;min-width:0;font:inherit;font-size:15px;padding:9px 12px;border:1.5px solid var(--ctl);border-radius:var(--r-sm);background:var(--surface-card);color:var(--ink)}
.chipset{display:flex;flex-wrap:wrap;gap:6px}
.exp-grp{display:block;font-size:12px;font-weight:750;letter-spacing:.04em;text-transform:uppercase;color:var(--heading);margin:10px 0 2px}
.chip{font:inherit;font-size:13px;font-weight:700;padding:6px 11px;border-radius:var(--pill);border:1.5px solid var(--ctl);background:var(--surface-card);color:var(--ink);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--ESC3);border-color:var(--ESC3);color:#FFFFFF}
.ask-core{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:0 0 22px}
@media (max-width:1100px){.ask-core{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.ask-core{grid-template-columns:1fr}}
.ask-k{display:flex;flex-direction:column;gap:4px;text-align:left;font:inherit;color:inherit;background:var(--surface-card);border:1px solid var(--border);border-top:4px solid var(--ESC1);border-radius:var(--r-md);padding:14px 16px;cursor:pointer;min-width:0}
.ask-k .kk{font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--heading)}
.ask-k .kv{font-size:clamp(24px,2.4vw,30px);font-weight:900;font-style:italic;color:var(--heading);line-height:1.1;overflow-wrap:anywhere}
.ask-k .kl{font-size:13px;font-weight:700;line-height:1.35}
.ask-k .kq{font-size:14px;line-height:1.4;border-top:1px solid var(--border-subtle);padding-top:6px;margin-top:4px}
.ask-list{display:grid;gap:10px}
.ask-topic{margin:22px 0 8px;padding-top:8px;border-top:1px solid var(--heading);font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--heading)}
details.ask-item{border:1px solid var(--border);border-radius:12px;background:var(--surface-card)}
details.ask-item[open]{border-color:var(--ESC1)}
details.ask-item>summary{list-style:none;display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:16px;align-items:center;padding:14px 18px;cursor:pointer}
details.ask-item>summary::-webkit-details-marker{display:none}
.ask-q{font-size:17px;font-weight:800;color:var(--heading);display:block;line-height:1.3}
.ask-a{display:block;font-size:14.5px;line-height:1.5;margin-top:4px}
.ask-v{text-align:right;min-width:110px}.ask-v b{display:block;font-size:22px;font-weight:900;font-style:italic;color:var(--heading)}.ask-v small{display:block;font-size:12px;line-height:1.3;max-width:22ch;margin-left:auto}
.ask-group,details.ask-item,details.ask-item>summary>span{min-width:0}
@media (max-width:640px){details.ask-item>summary{grid-template-columns:minmax(0,1fr) auto;gap:8px;padding:12px 14px}details.ask-item>summary .ask-v{grid-column:1;grid-row:2;text-align:left;min-width:0}details.ask-item>summary .ask-v small{margin-left:0}details.ask-item>summary .ask-tog{grid-column:2;grid-row:1}.ask-body{padding:0 12px 14px}.ask-geo{font-size:13px}.ask-geo td.v{white-space:normal}}
.ask-geo-w{overflow-x:auto;max-width:100%}
.ask-tog{font-size:20px;font-weight:800;color:var(--heading);transition:transform .2s}
details.ask-item[open] .ask-tog{transform:rotate(90deg)}
.ask-body{padding:0 18px 18px;border-top:1px solid var(--border-subtle)}
.ask-grid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:18px;margin-top:14px;align-items:start}
@media (max-width:980px){.ask-grid{grid-template-columns:1fr}}
.ask-geo{width:100%;border-collapse:collapse;font-size:14px}
.ask-geo th,.ask-geo td{text-align:left;vertical-align:top;padding:8px 8px;border-bottom:1px solid var(--border-subtle)}
.ask-geo thead th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#FFFFFF;background:#125C60}
.ask-geo td.v{font-weight:800;white-space:nowrap}
.ask-geo .s{display:block;font-size:11.5px;opacity:.85;margin-top:2px}
.ask-notes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:14px}
@media (max-width:760px){.ask-notes{grid-template-columns:1fr}}
.ask-note{background:var(--surface-page);border:1px solid var(--border-subtle);border-radius:var(--r-sm);padding:10px 12px;font-size:14px;line-height:1.5}
.ask-note h4{margin:0 0 4px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--heading)}
.ask-files{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:14px}
.ask-files .lbl{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--heading);margin-right:4px}
.fbtn{font:inherit;font-size:13px;font-weight:700;color:var(--heading);background:var(--surface-card);border:1.5px solid var(--ESC1);border-radius:var(--r-sm);padding:5px 9px;cursor:pointer;text-decoration:none}
.fbtn:hover,.fbtn:focus-visible{background:var(--ESC4);color:#231F20}
.fbtn.go{background:var(--ESC3);border-color:var(--ESC3);color:#FFFFFF}
.stackv{display:grid;gap:10px}
.stackv .row{display:grid;grid-template-columns:minmax(90px,max-content) minmax(0,1fr);gap:10px;align-items:center}
.stackv .bar{display:flex;height:22px;border-radius:3px;overflow:hidden;border:1px solid var(--border)}
.stackv .seg{height:100%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#231F20;overflow:hidden;white-space:nowrap}
.stackv .seg.c0{background:#125C60;color:#FFFFFF}.stackv .seg.c1{background:#43A3A3;color:#231F20}.stackv .seg.c2{background:#77C7C9}.stackv .seg.c3{background:#B4D9E3}.stackv .seg.c4{background:#F9F9F2}
.stackv .key{display:flex;flex-wrap:wrap;gap:10px;font-size:12px;margin-top:4px}.stackv .key i{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:4px;vertical-align:-1px;border:1px solid var(--border)}
.lib-sum{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0 0 16px}
@media (max-width:760px){.lib-sum{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.lib-sum .dcard{padding:10px}.lib-sum .dcard p,.lib-sum .dcard .dk{display:none}.lib-sum .dcard .dfl{font-size:12px}}
.lib-group{margin:0 0 18px}
.lib-group>h3{margin:26px 0 4px;padding-top:10px;border-top:1px solid var(--heading);color:var(--heading)}
.lib-group>p{margin:0 0 10px;font-size:14px}
.lib-list{display:grid;gap:10px}
.lib-file{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:start;border:1px solid var(--border);border-radius:12px;background:var(--surface-card);padding:14px 16px}
@media (max-width:760px){.lib-file{grid-template-columns:auto minmax(0,1fr)}.lib-file .acts{grid-column:1/-1}}
.lib-file .ext{font-size:11px;font-weight:900;letter-spacing:.06em;color:#FFFFFF;background:var(--ESC3);border-radius:4px;padding:6px 7px;min-width:44px;text-align:center}
.lib-file .ext.x{background:#43A3A3;color:#231F20}.lib-file .ext.c{background:#77C7C9;color:#231F20}.lib-file .ext.z{background:#231F20}
.lib-file h4{margin:0;font-size:16px;line-height:1.3;color:var(--heading)}
.lib-file .meta{font-size:12.5px;margin:3px 0 6px;opacity:.9}
.lib-file p{margin:0 0 6px;font-size:14px;line-height:1.5}
.lib-file .note{font-size:12.5px;font-style:italic}
.lib-file .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;font-size:12.5px;align-items:center}
.lib-file .more-t{font-size:12.5px;font-style:italic}
.lib-file .tags b{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--heading)}
.lib-file .ltag{text-transform:none;letter-spacing:0;font:inherit;font-size:12.5px;font-weight:700;border:1px solid var(--border);border-radius:var(--pill);padding:3px 9px;background:var(--surface-page);color:var(--ink);cursor:pointer}
.lib-file .acts{display:flex;flex-direction:column;gap:6px;min-width:120px}
.lib-file .acts .fbtn{text-align:center}
.lib-more{margin-top:4px}.lib-more>summary{cursor:pointer;font-size:13px;font-weight:700;color:var(--heading)}
.lib-links{display:grid;gap:8px;margin:0;padding:0;list-style:none}
.lib-links li{border:1px solid var(--border-subtle);border-radius:var(--r-sm);padding:10px 12px;background:var(--surface-card)}
.lib-links a{font-weight:800;color:var(--heading)}
.lib-links span{display:block;font-size:13.5px;margin-top:3px}
.lib-empty{padding:16px;border:1px dashed var(--border);border-radius:12px;font-size:14px}
@media print{details.ask-item{break-inside:avoid}details.ask-item .ask-body{display:block}.ask-ctl,.lib-file .acts{display:none}}
"""

NM = os.path.join(BASE, '..', 'node_modules')
_mdi_src = open(os.path.join(NM, '@mdi/js/mdi.js'), encoding='utf-8').read()
_ICONS = ['account-group', 'calendar-range', 'cash-multiple', 'bed', 'chart-line', 'calendar-start', 'calendar-check', 'finance', 'chart-timeline-variant', 'weather-night', 'bullhorn', 'telescope', 'bus', 'calendar-star', 'file-document-multiple', 'folder', 'file-document-outline', 'presentation', 'palette-outline', 'view-dashboard-outline', 'movie-open-outline', 'creation', 'link-variant', 'table-large', 'close']
def _camel(n): return 'mdi' + ''.join(w.capitalize() for w in n.split('-'))
MDI = {}
for _n in _ICONS:
    _m = re.search(r'export var ' + _camel(_n) + r' = "([^"]+)"', _mdi_src)
    if _m: MDI[_n] = _m.group(1)
assert len(MDI) == len(_ICONS), set(_ICONS) - set(MDI)

BODY = f"""<meta charset="utf-8">
<title>OC Vibe Insights</title>
<meta name="robots" content="noindex, nofollow">
<style>
{css}
{EXTRA_CSS}
{open(BASE + '/make.css').read()}
</style>
<a class="skip" href="#main">Skip to dashboard</a>
<div id="app">
  <header class="band" id="band">
    <div class="brand">
      <div class="logo-chip">{logo_img}</div>
      <div class="titles">
        <h1>OC Vibe Insights</h1>
        <p id="periodLine">Prepared by Visit Anaheim for OC Vibe · Visitor spending, jobs, one more night, getting here, who visits, marketing reach and market outlook · Anaheim, Orange County and U.S. · Data through Sept. 2026 · Updated quarterly; next update {SC.NEXT_S}</p>
      </div>
    </div>
    <div class="hdr-ctl" id="hdrCtl">
      <div class="pb-r">
        <button type="button" class="nbtn" id="prevBtn">‹ Previous</button>
        <button type="button" class="nbtn" id="nextBtn">Next ›</button>
        <div class="seg" role="group" aria-label="View style"><button type="button" id="vsOne" aria-pressed="true">One page</button><button type="button" id="vsLong" aria-pressed="false">All pages</button></div>
        <button type="button" class="ctl fs" id="fsBtn" aria-pressed="false">Full screen</button>
        <button type="button" class="ctl accent" id="exportPdf" aria-haspopup="dialog">Export</button>
      </div>
    </div>
  </header>
  <p class="sr" aria-live="polite" id="live"></p>
  <div class="layout" id="layout">
    <aside class="side collapsed" id="side" aria-label="Jump to section">
      <div class="side-h"><span>Jump to…</span><button type="button" id="collapseAll" aria-expanded="false">Show details</button></div>
      <nav><ul id="sideList"></ul></nav>
      <div class="side-quick"><span>Find an answer</span><button type="button" data-go="p-ask">Questions answered →</button><button type="button" data-go="p-library">Reports and data library →</button><button type="button" data-export="">Export: report, doc, slides, design, video or data →</button></div>
    </aside>
    <button type="button" class="side-toggle" id="sideToggle" aria-controls="side" aria-expanded="true" aria-label="Close section menu">‹</button>
    <main id="main" tabindex="-1">
      <nav class="secnav" id="pagebar" aria-label="Sections">
        <div class="tabs" id="secPills"></div>
        <p class="sr" aria-live="polite"><span id="pgNum"></span> <span id="pgTitle"></span></p>
      </nav>
      <div id="pages" class="single">
        <section class="page" id="p-summary" data-title="Overview">
          <div class="page-h"><h2>Overview</h2><span class="badge">Mixed periods · data through Sept. 2026</span></div>
          <div class="seg-h ov-seg" id="ovPulse" style="margin-top:20px"><span class="seg-n" aria-hidden="true">1</span><div><h3>BI Pulse Summary</h3><p>The main announcement: where Anaheim's visitor market stands as OC Vibe opens, with a source and date for every figure.</p></div></div>
          <article class="ann" id="ann" aria-labelledby="annHead">
            <div class="ann-tools">
              <span class="sp"></span>
              <button type="button" class="ctl accent" id="annCopy" title="Copies with formatting; pastes as plain text where formatting is not supported">Copy</button>
            </div>
            <div class="ann-paper" id="annPaper"></div>
          </article>
          <div class="seg-h ov-seg" id="ovTk"><span class="seg-n" aria-hidden="true">2</span><div><h3>Key takeaways</h3><p>The headline number from each section, with its period. Select one to read the full story.</p></div></div>
          <div class="kts" id="keyTk"></div>
          <div class="seg-h ov-seg" id="ovFind"><span class="seg-n" aria-hidden="true">3</span><div><h3>Find an answer</h3><p>Questions answered for Anaheim, Orange County and the U.S., and every report and data file behind them.</p></div></div>
          <div class="find-row">
            <button type="button" class="find-link" data-go="p-ask"><b>Questions answered</b><span>Average spend, one more night, transportation, District 5 and 17 more</span><span class="go" aria-hidden="true">→</span></button>
            <button type="button" class="find-link" data-go="p-library"><b>Reports and data library</b><span>Open or download the source files</span><span class="go" aria-hidden="true">→</span></button>
            <button type="button" class="find-link" data-go="p-notes" data-target="updSched"><b>Updated quarterly</b><span>Last update {SC.LAST_S} · next {SC.NEXT_S}</span><span class="go" aria-hidden="true">→</span></button>
          </div>
        </section>
        <section class="page" id="p-ask" data-title="Questions answered">
          <div class="page-h"><h2>Questions answered</h2><span class="badge">Anaheim · Orange County · California · U.S. · data through Sept. 2026</span></div>
          <p class="ask-lede">General questions about Anaheim's visitor economy and the OC Vibe area. Each answer gives a short summary, the figures for Anaheim, Orange County and the U.S. (California where that is the closest published level), a visual, how the number is calculated, what to keep in mind, and the reports and data files to read more.</p>
          <div class="ask-ctl"><label class="sr" for="askQ">Search the questions</label><input type="search" id="askQ" placeholder="Search: spend, jobs, night, transportation, District 5, hotels…" autocomplete="off"><div class="chipset" id="askTopics" role="group" aria-label="Filter by topic"></div></div>
          <div class="seg-h" id="askCore"><span class="seg-n" aria-hidden="true">1</span><div><h3>The four core questions</h3><p>Select a card to open its full answer.</p></div></div>
          <div class="ask-core" id="askCoreGrid"></div>
          <div class="seg-h" id="askAll"><span class="seg-n" aria-hidden="true">2</span><div><h3>All questions</h3><p>Grouped by topic. Each opens to the figures, a visual, the method and the files.</p></div></div>
          <p class="sr" aria-live="polite" id="askCount"></p>
          <div class="ask-list" id="askList"></div>
          <p class="csub" style="font-weight:350;margin:16px 0 0">Have a question that is not here? Contact the Visit Anaheim BI team: <a href="mailto:bi@visitanaheim.org">bi@visitanaheim.org</a>.</p>
        </section>
        <div id="secHost" style="display:contents"></div>
        <section class="page" id="p-library" data-title="Reports and data library">
          <div class="page-h"><h2>Reports and data library</h2><span class="badge" id="libBadge"></span></div>
          <p class="ask-lede">Every report and data file used to build this app, as received from each publisher. Open a file to read it in the browser, or download it. Each file lists what it covers, the period and publication date, the questions it answers and the sections that use it.</p>
          <div class="lib-sum" id="libSum"></div>
          <div class="seg-h" id="libFilesH"><span class="seg-n" aria-hidden="true">1</span><div><h3>Source files</h3><p>Grouped by topic. Search or filter, then open or download.</p></div></div>
          <div class="ask-ctl"><label class="sr" for="libQ">Search the library</label><input type="search" id="libQ" placeholder="Search: Tourism Economics, Garden Grove, District 5, STR, OCTA…" autocomplete="off"><div class="chipset" id="libTopics" role="group" aria-label="Filter by topic"></div></div>
          <p class="sr" aria-live="polite" id="libCount"></p>
          <div id="libFiles"></div>
          <div class="seg-h"><span class="seg-n" aria-hidden="true">2</span><div><h3>Public sources</h3><p>Published by others and linked rather than hosted here.</p></div></div>
          <div class="box" id="libLinks"><h3>Public sources used (links)</h3><p class="csub" style="font-weight:350;margin:0 0 10px">Published by others and linked rather than hosted here.</p><ul class="lib-links" id="libLinkList"></ul></div>
          <p class="csub" style="font-weight:350;margin:16px 0 0">When quoting a figure, cite the publisher and date shown on the file. Questions about a file: <a href="mailto:bi@visitanaheim.org">bi@visitanaheim.org</a>.</p>
        </section>
        <section class="page" id="p-notes" data-title="Sources">
          <div class="page-h"><h2>Sources</h2><span class="badge">Prepared {PREP}</span></div>
          <div class="box upd-box" id="updSched"><h3>How this report is updated</h3>
            <p class="upd-lede" id="updLede"></p>
            <div id="updCards"></div>
            <div id="updTable"></div>
            <div id="updPlanned"></div>
          </div>
          <div class="takeaways"><h3>Key takeaways</h3><ul class="bul" id="takeaways"></ul></div>
          <div class="stack" style="margin-top:12px">
            <div class="box"><h3>Recommendations for OC Vibe</h3>
              <p class="csub" style="font-weight:350;margin:0 0 12px">Visit Anaheim BI recommendations based on the findings in this dashboard. These are suggestions for discussion, not findings.</p>
              <div id="recList"></div>
            </div>
            <div class="box"><h3>Downloads</h3>
              <div class="src-acts"><button type="button" class="dl" data-export="">Export the report, a doc, slides, a design, a video or the data</button><button type="button" class="dl" data-go="p-library">Open the Reports and data library</button></div>
            </div>
            <div class="box"><h3>Source register</h3>
              <p class="csub" style="font-weight:350;margin:0 0 12px">Every source used, with the period it covers, when it was published or pulled, how it is used and how Visit Anaheim BI checked it. Prepared Oct. 12, 2026.</p>
              <div id="regTbl"></div>
            </div>
            <div class="box"><h3>Data sources</h3>
              <ul class="src-list" id="srcList"></ul>
            </div>
            <div class="grid2">
              <div class="box"><h3>Methodology</h3>
                <dl class="defs">
                  <div><dt>Periods</dt><dd>Each section shows its own period. Economic impact is calendar 2025 vs. 2024; quarterly visitor data is Q2 2026 vs. Q2 2025; hotel forecasts run to 2030; CoStar hotel data is trailing 12 months or year to date through Aug. 2026; Symphony data covers the dates on each page.</dd></div>
                  <div><dt>Forecasts</dt><dd>Values marked F or "forecast" are third-party projections (Tourism Economics, LARC, CoStar) and can change with each edition.</dd></div>
                  <div><dt>BI calculations</dt><dd>Spending per visitor, food and beverage shares, commute shares, bus service counts and the one-more-night scenarios are calculated by Visit Anaheim BI from the published figures. They are labeled where used.</dd></div>
                  <div><dt>One more night</dt><dd>Headline: 2025 lodging spending ($1.72B) ÷ weighted average stay (2.17 days) = about $794M for one more night. Alternatives: overnight visitors adding a day at average daily spending ($1.02B); every visitor adding a day ($3.15B, upper bound).</dd></div>
                  <div><dt>Two hotel bases</dt><dd>LARC market tables use CoStar's Anaheim market. Visit Anaheim hotel set tables use the Anaheim and Garden Grove sets. CoStar's Disneyland submarket is a separate CoStar geography. Do not compare these bases directly.</dd></div>
                  <div><dt>Symphony (Azira)</dt><dd>Mobile location samples. Overnight and new-visitor shares count visitors who stayed 4+ hours, are not commuters and live 50+ miles away.</dd></div>
                </dl>
              </div>
              <div class="box"><h3>Definitions</h3>
                <dl class="defs">
                  <div><dt>Revenue per available room</dt><dd>Room revenue divided by rooms available (RevPAR).</dd></div>
                  <div><dt>Average nightly rate</dt><dd>Room revenue divided by rooms sold (ADR).</dd></div>
                  <div><dt>Visitor</dt><dd>Someone who stayed overnight or traveled more than 50 miles to the destination (Tourism Economics).</dd></div>
                  <div><dt>Total economic impact</dt><dd>Direct visitor spending plus supply-chain (indirect) and income (induced) effects.</dd></div>
                  <div><dt>Jobs supported</dt><dd>Full- and part-time jobs, including proprietors (Bureau of Economic Analysis definition).</dd></div>
                  <div><dt>Visits per 1,000 impressions</dt><dd>Observed visits after ad exposure divided by measurable impressions, times 1,000.</dd></div>
                  <div><dt>TID</dt><dd>TID: the Anaheim Tourism Improvement District that funds incentive buydowns.</dd></div>
                </dl>
              </div>
            </div>
            <div class="box"><h3>About the data</h3>
              <ul class="dq" id="dqList"></ul>
            </div>
          </div>
        </section>
      </div>
      <footer>
        <span>Sources: Tourism Economics; LARC; CoStar; Symphony | Tourism Economics (Azira); Datafy; OCTA; U.S. BTS; Visit Anaheim BI</span>
        <span>{SC.LINE}</span>
        <span>Powered by Visit Anaheim Business Intelligence Team · Contact us: <a href="mailto:bi@visitanaheim.org">bi@visitanaheim.org</a></span>
      </footer>
    </main>
  </div>
</div>
<button type="button" class="totop" id="toTop" hidden>↑ Go to top</button>
<button type="button" class="next-pill" id="nextPill" hidden></button>
<dialog id="expDlg" class="exp-dlg xp" aria-labelledby="expTitle"></dialog>
<div class="toast" id="toast" role="status" hidden></div>
<script>
const DATA = {json.dumps(DATA, ensure_ascii=False)};
const DQ = {json.dumps(C.DQ if hasattr(C,'DQ') else [], ensure_ascii=False)};
const ATTACH = {json.dumps({'deck': base64.b64encode(open(BASE + '/OC_Vibe_Insights.pptx','rb').read()).decode(), 'pdf': base64.b64encode(open(BASE + '/OC_Vibe_Insights.pdf','rb').read()).decode()})};
const PDFMAP = {open(BASE + '/deck_pages.json').read()};
const IMGS = {json.dumps({'adt_ocvibe.jpg': 'data:image/jpeg;base64,' + base64.b64encode(open(BASE + '/assets/adt_ocvibe.jpg','rb').read()).decode()})};
const RECS = {json.dumps(C.RECS, ensure_ascii=False)};
const RECS_T = {json.dumps(__import__('logic_content').RECS_T, ensure_ascii=False)};
</script>
<script>
/* JSZip v3.10.1 (MIT), used only to assemble PowerPoint exports */
{open(__import__('os').path.join(__import__('os').path.dirname(__import__('subprocess').check_output(['node','-p',"require.resolve('jszip',{paths:[require.resolve('pptxgenjs')]})"]).decode().strip()),'..','dist','jszip.min.js')).read()}
</script>
<script>
{open(BASE + '/pptx_subset.js').read()}
</script>
<script>
/* PptxGenJS v4.0.1 (MIT), builds the Make something new slides in the browser (uses the JSZip above) */
{open(NM + '/pptxgenjs/dist/pptxgen.min.js', encoding='utf-8').read()}
</script>
<script>
/* pdf-lib v1.17.1 (MIT), used only to cut PDF exports to the chosen sections */
{open(__import__('os').path.join(__import__('os').path.dirname(__import__('subprocess').check_output(['node','-p',"require.resolve('pdf-lib/package.json')"]).decode().strip()),'dist','pdf-lib.min.js'), encoding='utf-8').read().replace(chr(0xFFFD), chr(92) + 'ufffd')}
</script>
<script>
{open(BASE + '/pdf_subset.js').read()}
</script>
<script>
const MAPGEO = {open(BASE + '/maps_geo.json').read()};
{open(BASE + '/map_svg.js').read()}
</script>
<script>
{open(BASE + '/app.js').read()}
</script>
<script>
{open(BASE + '/ask_app.js').read()}
</script>
<script>
/* AntV G2 v5.4.8 (MIT) */
{open(NM + '/@antv/g2/dist/g2.min.js', encoding='utf-8').read()}
</script>
<script>
/* AntV T8 v0.3.1 (MIT) */
{open(NM + '/@antv/t8/dist/t8.min.js', encoding='utf-8').read()}
</script>
<script>
/* AntV Infographic v0.2.20 (MIT); remote font stylesheets disabled so the page makes no network requests */
{open(NM + '/@antv/infographic/dist/infographic.min.js', encoding='utf-8').read().replace('https://assets.antv.antgroup.com', 'data:text/css,').replace('https://www.weavefox.cn/api/v1/infographic/icon', 'data:application/json,%7B%22success%22%3Afalse%7D#').replace('\ufffd', '\\uFFFD')}
</script>
<script>
/* AntV X6 v3.1.8 (MIT) */
{open(NM + '/@antv/x6/dist/x6.min.js', encoding='utf-8').read()}
</script>
<script>
/* Material Design Icons (Apache-2.0), only the icons used */
window.MDI = {json.dumps(MDI)};
</script>
<script>
{open(BASE + '/antv_app.js').read()}
</script>
<script>
/* D3 v7.9.0 (ISC), pinned */
{open(NM + '/d3/dist/d3.min.js', encoding='utf-8').read()}
</script>
<script>
{open(BASE + '/d3_app.js').read()}
</script>
<script>
{open(BASE + '/make_app.js').read()}
</script>
"""
open(BASE + '/oc-vibe-insights.html', 'w').write(BODY)
print('bytes', len(BODY))
