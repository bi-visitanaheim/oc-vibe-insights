"""Map visuals for geographic data (added Oct. 13, 2026, per John Picou). Values come only from the report tables;
geometry and point positions come from maps_geo.json (node maps_geo.js). Rendered by map_svg.js in the page and as PNGs
(node maps_render.js) in the deck. Attach after infographics.py."""
import re


def _t(sec, start):
    return next(t for t in sec["tables"] if t["title"].startswith(start))


def _pct(s):
    return float(re.sub(r"[^\d.]", "", s))


def _money(s):  # "$307.3M" / "$797K" -> $M
    v = float(re.sub(r"[^\d.]", "", s))
    return v / 1000 if s.strip().endswith("K") else v


def attach(SECTIONS):
    S = {s["id"]: s for s in SECTIONS}
    d5 = S["p-d5"]
    st, mt = _t(d5, "Top origin states"), _t(d5, "Where District 5 visitors come from")
    visa, intl = _t(d5, "Where visitor card spending comes from"), _t(d5, "International visitor card spending")
    d5["maps"] = [dict(kind="us", title="Where District 5's domestic visitors come from",
        sub="Share of District 5 domestic visitors, by state (shading) and metro area (circles), Jan. 1–May 31, 2026",
        states=[dict(name=r[0], v=_pct(r[1]), t=r[1]) for r in st["rows"]],
        points=[dict(name=r[0], v=_pct(r[1]), t=r[1]) for r in mt["rows"]],
        unit="share", bins=[(20, "20% or more"), (3, "3% to 20%"), (0, "Under 3%")], other="Not in the top 11 states",
        home="Anaheim", src=(st.get("src") or mt.get("src") or "Azira via Symphony (District 5, Jan. 1–May 31, 2026)"))]
    us_rows = [r for r in visa["rows"] if r[0] not in ("Mexico", "Canada")]
    ctry = [(r[0].replace("Country: ", ""), r[1]) for r in intl["rows"] if r[0].startswith("Country: ")]
    S["p-spend"]["maps"] = [
        dict(kind="us", title="Where visitor card spending in Anaheim comes from, by U.S. metro area",
             sub="Visitor card spending by cardholder home metro, August 2026 · circle area shows spending",
             points=[dict(name=r[0], v=_money(r[1]), t=f"{r[1]} ({r[2]} of total)") for r in us_rows],
             unit="money", home="Anaheim", src=visa.get("src") or "Visa Destination Insights via Symphony (Aug. 2026)"),
        dict(kind="world", title="International card spending, by visitor's home country",
             sub="International visitor card spending in Anaheim, August 2026 · circle area shows spending",
             points=[dict(name=n, v=_money(v), t=v) for n, v in ctry],
             unit="money", home="Anaheim", src=intl.get("src") or "Visa Destination Insights via Symphony (Aug. 2026)")]
