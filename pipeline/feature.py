"""Featured BI charts for each section (shown up front in the article), built from the same model and source data.
Chart kinds rendered by app.js: bars, cols (existing), line, wf (waterfall), range, heat.
"""
import impact as I, newdata as ND, data as D
import roles_content as RC, ocv_whole as OW, calcs as CX
from data import EI, N

A = EI["Anaheim"]; B = I.RES[1]
m = lambda v, d=1: f"${v/1e6:,.{d}f}M"
S_MODEL = "Visit Anaheim BI scenario model (Oct. 12, 2026)"
_R = OW._R; _mc = _R["monte_carlo"]["spend"]

NEW = {
 "p-ocv": [
   dict(kind="wf", title=f"New visitor spending of {m(B['spend'])} comes from two sources",
        sub="Base case, a year at full operation, 2025 dollars",
        steps=[dict(l="Net-new visitors", v=B["sp_new"] / 1e6, t=m(B["sp_new"]), note=f"{B['new_vis']:,.0f} × $258"),
               dict(l="Longer stays", v=B["sp_stay"] / 1e6, t=m(B["sp_stay"]), note=f"{B['extra_days']:,.0f} days × ${I.PER_DAY:.2f}"),
               dict(l="New visitor spending", v=B["spend"] / 1e6, t=m(B["spend"]), total=True, note="Sum of the two sources")],
        src=S_MODEL),
   dict(kind="range", title=f"90% of 200,000 simulations fall between {m(_mc['p5'],0)} and {m(_mc['p95'],0)}",
        sub="New visitor spending a year, $M · band = 5th to 95th percentile",
        min=0, max=200, lo=_mc["p5"] / 1e6, hi=_mc["p95"] / 1e6,
        marks=[dict(v=I.RES[0]["spend"] / 1e6, l=f"Conservative {m(I.RES[0]['spend'])}", k="end"),
               dict(v=B["spend"] / 1e6, l=f"Base {m(B['spend'])}", k="base"),
               dict(v=_mc["p50"] / 1e6, l=f"Median {m(_mc['p50'],0)}", k="mid"),
               dict(v=I.RES[2]["spend"] / 1e6, l=f"Optimistic {m(I.RES[2]['spend'])}", k="end")],
        src=S_MODEL + "; simulation of 200,000 draws")],
 "p-night": [
   dict(kind="bars", title="Each additional 1% of visitors who add a day is worth about $31.5M",
        sub=f"New visitor spending a year by share of Anaheim visitors who add a day · {A['vis25']:.1f}M visitors × share × ${I.PER_DAY:.2f}",
        rows=[dict(l=f"{p}% add a day", v=I.PER_1PCT_DAY * k / 1e6, t=m(I.PER_1PCT_DAY * k), hi=(k == 1)) for p, k in (("0.5", 0.5), ("1", 1), ("2", 2))],
        src=S_MODEL)],
 "p-transport": [
   dict(kind="line", title="Orange County transit riders fell 38% from the 2007 peak",
        sub="Total passengers a year, all operators, millions · 2003–2017 (latest available)",
        x=[str(y) for y in RC.YRS], series=[dict(name="Passengers", v=[round(v / 1e6, 1) for v in RC.PAX["Total"]], focal=True)],
        yfmt=dict(suf="M", dec=1), src="California's transit systems data snapshots (2003–2017; downloaded Oct. 12, 2026)")],
 "p-d5": [
   dict(kind="bars", title="District 5 visits peak on Saturday but stay above 13% every day",
        sub="Share of District 5 visits by day of week, Jan.–May 2026",
        rows=[dict(l=d, v=v, t=f"{v:.1f}%", hi=(d == "Sat")) for d, v in D.D5_DOW],
        src="Azira via Symphony (District 5, Jan. 1–May 31, 2026)")],
 "p-hotel": [
   dict(kind="heat", title=f"Weeknights have the most room in {OW.soft_names}",
        sub="Visit Anaheim hotel set (Anaheim+), occupancy by month, 2026 · weeknights = Sunday–Thursday",
        cols=["Weeknights", "Friday–Saturday", "All nights"],
        rows=[dict(l=c["m"], cells=[c["wk"], c["we"], c["occ"]], extra=f"{c['n90']} nights at 90%+ · groups {c['grp']:.1f}%") for c in OW.CAL],
        src="STR daily data, Visit Anaheim hotel sets (Jan. 1–Sept. 30, 2026); BI calculation")],
 "p-larc": [
   dict(kind="line", title="Convention bookings for 2027 strengthened through 2026",
        sub="Convention Center room nights on the books vs. same point last year, by LARC report edition",
        x=[e for e, _, _ in D.CONV_PACE],
        series=[dict(name="2027 events", v=[b for _, _, b in D.CONV_PACE], focal=True), dict(name="2026 events", v=[a for _, a, _ in D.CONV_PACE])],
        yfmt=dict(pre="+", suf="%", dec=0), ymin=0, src="LARC Market Intelligence Reports (Jan.–Sept. 2026)")],
}


def attach(SECTIONS):
    for s in SECTIONS:
        sid = s["id"]; ch = s.get("charts", [])
        if sid == "p-hotel":
            dow = [c for c in ch if c["title"].startswith("Sunday and Monday")]
            s["feature"] = NEW["p-hotel"] + dow
            s["more_charts"] = [c for c in ch if c not in dow]
        elif sid in ("p-appx",):
            s["feature"] = []; s["more_charts"] = ch
        else:
            first = [c for c in ch if c.get("kind") != "img"][:1]
            s["feature"] = NEW.get(sid, []) + first
            s["more_charts"] = [c for c in ch if c not in first]
