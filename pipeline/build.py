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
DATA = dict(main=C.DATA_EXTRA['main'], tags=C.DATA_EXTRA['tags'], sections=C.SECTIONS, stories=C.STORIES, takeaways=C.TAKEAWAYS, sources=C.SOURCES, prepared=PREP, register=OCVC.REGISTER)

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
.kind{display:inline-block;font-weight:800;color:#fff;background:var(--heading);border-radius:3px;padding:1px 7px;margin-right:2px;letter-spacing:.1em}
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
"""

BODY = f"""<title>OC Vibe Insights</title>
<meta name="robots" content="noindex, nofollow">
<style>
{css}
{EXTRA_CSS}
</style>
<a class="skip" href="#main">Skip to dashboard</a>
<div id="app">
  <header class="band" id="band">
    <div class="brand">
      <div class="logo-chip">{logo_img}</div>
      <div class="titles">
        <h1>OC Vibe Insights</h1>
        <p id="periodLine">Prepared by Visit Anaheim for OC Vibe · Visitor spending, jobs, one more night, getting here, who visits, marketing reach and market outlook · Anaheim, Orange County and U.S. · Data through Sept. 2026</p>
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
          <article class="ann" id="ann" aria-labelledby="annHead">
            <div class="ann-tools">
              <span class="sp"></span>
              <button type="button" class="ctl accent" id="annCopy" title="Copies with formatting; pastes as plain text where formatting is not supported">Copy</button>
            </div>
            <div class="ann-paper" id="annPaper"></div>
          </article>
          <h3 class="ov-h">Questions and short answers</h3>
          <p class="csub" style="font-weight:350;margin:0 0 12px">Each question with a short answer. Select a question to see the details.</p>
          <div class="qa" id="qa"></div>
        </section>
        <div id="secHost" style="display:contents"></div>
        <section class="page" id="p-notes" data-title="Sources">
          <div class="page-h"><h2>Sources</h2><span class="badge">Prepared {PREP}</span></div>
          <div class="takeaways"><h3>Key takeaways</h3><ul class="bul" id="takeaways"></ul></div>
          <div class="stack" style="margin-top:12px">
            <div class="box"><h3>Recommendations for OC Vibe</h3>
              <p class="csub" style="font-weight:350;margin:0 0 12px">Visit Anaheim BI recommendations based on the findings in this dashboard. These are suggestions for discussion, not findings.</p>
              <div id="recList"></div>
            </div>
            <div class="box"><h3>Downloads</h3>
              <div class="src-acts"><button type="button" class="dl" id="dlDeck">Download the OC Vibe Insights deck (.pptx)</button><button type="button" class="dl" id="dlCsv">Download the data tables (.csv)</button></div>
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
        <span>Powered by Visit Anaheim Business Intelligence Team</span>
      </footer>
    </main>
  </div>
</div>
<button type="button" class="totop" id="toTop" hidden>↑ Go to top</button>
<dialog id="expDlg" class="exp-dlg" aria-labelledby="expTitle">
  <h3 id="expTitle">Export</h3>
  <p class="exp-sub">Choose the sections to include and the format.</p>
  <fieldset class="exp-fmt"><legend>Format</legend>
    <label><input type="radio" name="expFmt" value="pdf" checked> PDF (pages as shown)</label>
    <label><input type="radio" name="expFmt" value="csv"> CSV (data tables only)</label>
  </fieldset>
  <fieldset><legend>Sections</legend>
    <div class="exp-quick"><button type="button" class="ctl" id="expAll">Select all</button><button type="button" class="ctl" id="expNone">Clear</button><button type="button" class="ctl" id="expCur">Current section only</button></div>
    <div class="exp-list" id="expList"></div>
    <p class="exp-count" id="expCount" aria-live="polite"></p>
  </fieldset>
  <div class="exp-acts"><button type="button" class="ctl" id="expCancel">Cancel</button><button type="button" class="ctl accent" id="expGo">Export</button></div>
</dialog>
<div class="toast" id="toast" role="status" hidden></div>
<script>
const DATA = {json.dumps(DATA, ensure_ascii=False)};
const DQ = {json.dumps(C.DQ if hasattr(C,'DQ') else [], ensure_ascii=False)};
const ATTACH = {json.dumps({'deck': base64.b64encode(open(BASE + '/OC_Vibe_Insights.pptx','rb').read()).decode()})};
const IMGS = {json.dumps({'adt_ocvibe.jpg': 'data:image/jpeg;base64,' + base64.b64encode(open(BASE + '/assets/adt_ocvibe.jpg','rb').read()).decode()})};
const RECS = {json.dumps(C.RECS, ensure_ascii=False)};
const RECS_T = {json.dumps(__import__('logic_content').RECS_T, ensure_ascii=False)};
</script>
<script>
{open(BASE + '/app.js').read()}
</script>
"""
open(BASE + '/oc-vibe-insights.html', 'w').write(BODY)
print('bytes', len(BODY))
