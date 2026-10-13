"""Data infographics (added Oct. 13, 2026, per John Picou): one or two per section, built only from figures already in
the section's tables, cards and notes. Every derived figure carries its calculation; every infographic its source and date.
Rendered by app.js (infoHtml) with entrance animation (count-up numbers, growing bars, filling waffles; off under reduced
motion and in print/PDF) and by deck_body.js (infoSlide). Attach after newsroom.py.

Kinds: chain, waffle, receipt, people, towers, share, board, funnel, versus.
"""
import re

TE = "Tourism Economics, Economic Impact of Visitors (calendar 2025; pub. 2026)"
STR = "STR daily data, Visit Anaheim hotel sets (Jan. 1–Oct. 3, 2026)"
COSTAR = "CoStar (data through Aug. 2026; pulled Oct. 12, 2026)"


def _num(s):
    return float(re.sub(r"[^\d.]", "", s))


def _t(sec, start):
    return next(t for t in sec["tables"] if t["title"].startswith(start))


def build(S):
    o, h, m, l, tr = S["p-ocv"], S["p-hotel"], S["p-media"], S["p-larc"], S["p-transport"]
    eco = {r[0]: r for r in _t(o, "Anaheim's visitor economy")["rows"]}
    mix = [r for r in _t(o, "Where Anaheim visitor spending goes")["rows"] if r[0] != "Total"]
    vis, spend = _num(eco["Visitors"][1]), 6832.0           # 26.5M visitors; $6,832M (Tourism Economics, 2025)
    jobs, imp, tax = 67817, 10.42, 970
    jobs_share = 32.8                                     # "32.8% of all Anaheim jobs" (Tourism Economics note in the table)
    nights = next(c for c in h["charts"] if c["title"].startswith("Sunday and Monday"))["rows"]
    pipe = 668; supply = 60223                            # CoStar: 668 rooms under construction, 1.1% of 60,223 rooms
    INFO = {}

    INFO["p-ocv"] = [dict(kind="chain", title="How 26.5 million visitors move through Anaheim's economy",
        sub="City of Anaheim, calendar 2025 · each link shows its calculation",
        steps=[dict(v="26.5M", n=26.5, suf="M", l="visitors"),
               dict(v="$6.83B", n=6.83, pre="$", suf="B", dec=2, l="visitor spending"),
               dict(v="$10.42B", n=10.42, pre="$", suf="B", dec=2, l="total economic impact"),
               dict(v="67,817", n=67817, l="jobs supported (32.8% of all Anaheim jobs)"),
               dict(v="$970M", n=970, pre="$", suf="M", l="state and local taxes")],
        links=[f"${spend/vis:,.0f} each: $6.832B ÷ 26.5M",
               f"×{imp*1000/spend:.2f}: $10.42B ÷ $6.832B",
               f"{jobs/spend:.1f} jobs per $1M: 67,817 ÷ 6,832",
               f"${tax/spend*1e3:,.0f}K per $1M: $970M ÷ 6,832"],
        src=TE)]

    INFO["p-d5"] = [dict(kind="waffle", title="Of every 100 District 5 visitors", sub="Each square is one visitor in 100 · rounded from the measured share",
        items=[dict(pct=85.8, l="stay overnight", src="Azira via Symphony (District 5, Jan. 1–May 31, 2026)"),
               dict(pct=43.8, l="are first-time visitors", src="Azira via Symphony (District 5, Jan. 1–May 31, 2026)"),
               dict(pct=44.0, l="of domestic visitors come from outside California", src="Azira via Symphony (domestic visitors, Aug. 2026)")],
        src="Azira via Symphony (District 5, Jan. 1–May 31, 2026; domestic visitors, Aug. 2026)")]

    lines = []
    for name, amt, share, _ in mix:
        a = _num(amt)
        lines.append(dict(l=name, v=f"${a/vis:,.2f}", n=round(a / vis, 2), pre="$", dec=2, pct=_num(share), calc=f"{amt} ÷ 26.5M visitors"))
    tot = sum(_num(x[1]) for x in mix)
    INFO["p-spend"] = [dict(kind="receipt", title="What one Anaheim visitor spends, itemized", sub="Average per visitor, calendar 2025 · category spending ÷ 26.5M visitors",
        lines=lines, total=dict(l="Total per visitor", v=f"${tot/vis:,.2f}", calc=f"${tot:,.0f}M ÷ 26.5M; Tourism Economics' $6.832B total gives $258 (rounding)"),
        src=TE)]

    INFO["p-impact"] = [dict(kind="people", title="About one in three Anaheim jobs is supported by visitors", sub="Each figure is 10% of all jobs in Anaheim, 2025",
        pct=jobs_share, v="32.8%", l="of all Anaheim jobs: 67,817 jobs supported by visitor spending", src=TE + "; share as reported")]

    INFO["p-hotel"] = [dict(kind="towers", title="How full Visit Anaheim hotels are, night by night", sub="Average occupancy by night of the week, Jan. 1–Oct. 3, 2026 · Sunday and Monday highlighted",
                            nights=[dict(l=r["l"][:3], v=round(float(r["v"]), 1), hi=r["l"] in ("Sunday", "Monday")) for r in nights], src=STR),
                       dict(kind="share", title="New hotel supply is a sliver of the market", sub="Rooms under construction vs. existing rooms, Orange County",
                            part=dict(v="668", n=pipe, l="rooms under construction"), whole=dict(v="60,223", n=supply, l="existing rooms"),
                            pct=round(pipe / supply * 100, 1), calc="668 ÷ 60,223 = 1.1%", src=COSTAR)]

    INFO["p-night"] = [dict(kind="share", title="Most Anaheim visitors come for the day", sub="Day and overnight visitors, calendar 2025",
                            part=dict(v="8.6M", n=8.6, l="overnight visitors"), whole=dict(v="26.5M", n=26.5, l="all visitors (17.9M day visitors)"),
                            pct=round(8.6 / 26.5 * 100, 1), calc="8.6M ÷ 26.5M = 32.5%; day visitors 17.9M ÷ 26.5M = 67.5%",
                            src=TE + "; Visit Anaheim BI, Extra Night study (Oct. 12, 2026)")]

    INFO["p-transport"] = [dict(kind="board", title="ARTIC departures: weekday OCTA bus trips", sub="OCTA schedules, Aug. 9–Nov. 7, 2026 · beside OC Vibe at 2626 E. Katella Ave.",
        rows=[dict(r=r[0], d=r[1], n=int(r[2])) for r in _t(tr, "OCTA bus service at ARTIC")["rows"] if r[0] != "All"],
        total=dict(l="All routes", n=277, calc="100 + 102 + 75"),
        extra=[dict(v="11", l="weekday buses leave after 10 p.m."), dict(v="275,000", l="vehicles a weekday on SR-57 (Caltrans 2024)"), dict(v="191,153", l="Amtrak passengers at Anaheim, 2024")],
        src="OCTA bus schedules (Aug. 9–Nov. 7, 2026); OCTA Traffic Flow Map (Aug. 2026); Amtrak ANA fact sheet (2024 data)")]

    INFO["p-media"] = [dict(kind="funnel", title="From ad impressions to visits in Anaheim", sub="Visit Anaheim paid media, ad exposures Jan. 1–Aug. 31, 2026",
        stages=[dict(v="31.0M", n=31.0, suf="M", l="measurable impressions"), dict(v="368,416", n=368416, l="observed visits (first visit 3+ days after exposure)")],
        rates=[dict(v="11.9", l="visits per 1,000 impressions, all campaigns", calc="368,416 ÷ 31.0M × 1,000"),
               dict(v="34.4", l="visits per 1,000 impressions, luxury placements", calc=f"{34.4/11.9:.1f}× the all-campaign rate: 34.4 ÷ 11.9")],
        src="Azira media attribution via Symphony (ad exposures Jan. 1–Aug. 31, 2026)")]

    INFO["p-larc"] = [dict(kind="versus", title="Anaheim vs. the U.S. and the year ahead", sub="LARC Market Intelligence Reports, Jan.–Sept. 2026",
        rows=[dict(l="Hotel revenue per room, Q2 2026", a=11.4, b=5.7, la="Anaheim", lb="U.S."),
              dict(l="Convention room nights on the books", a=17.0, b=12.0, la="2027 events", lb="2026 events"),
              dict(l="Costs, a year", a=6.0, b=3.2, la="Hotel labor (about)", lb="Anaheim prices")],
        src="LARC Market Intelligence Reports (Jan.–Sept. 2026)")]
    return INFO


def attach(SECTIONS):
    S = {s["id"]: s for s in SECTIONS}
    for sid, items in build(S).items():
        S[sid]["info"] = items
