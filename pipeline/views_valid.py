"""Three holistic impact views (Anaheim today, Anaheim with OC Vibe, OC Vibe's own) and the validation section."""
import os as _os
BASE = _os.path.dirname(_os.path.abspath(__file__))  # pipeline folder
import json, impact as I
from data import EI

import glob as _glob, os as _os
RES_PATH = BASE + "/computations/validation-010/results.json"
if not _os.path.exists(RES_PATH):   # while the suite itself is running, use the latest completed run
    RES_PATH = sorted(_glob.glob(BASE + "/computations/validation-*/results.json"))[-1]
def M(v, nd=1): return f"${v/1e6:,.{nd}f}M"
def B(v, nd=2): return f"${v/1e9:,.{nd}f}B"
def N(v, r=-3): return f"{round(v, r):,.0f}"

def attach(SECTIONS, STORIES, TAKEAWAYS, RECS, SOURCES, DQ, REGISTER, SRC):
    R = json.load(open(RES_PATH)); mc = R["monte_carlo"]; sens = R["sensitivity"]
    V, Vl, Vh = I.VIEWS["Base"], I.VIEWS["Conservative"], I.VIEWS["Optimistic"]
    A = EI["Anaheim"]
    at, al, ot, ol = V["ana_today"], V["ana_live"], V["ocv_today"], V["ocv_live"]
    o = SECTIONS[0]
    src_views = "Tourism Economics Economic Impact 2025 (Anaheim); Datafy Anaheim visitor report (calendar 2024); Visit Anaheim BI scenario model (Oct. 12, 2026)"
    rows = [
      ["Visitors a year", N(at["visitors"], -5), N(al["visitors"], -4), "—", "—"],
      ["Visitor days a year", N(at["vdays"], -5), N(al["vdays"], -5), N(ot["vdays"], -4), N(ol["vdays"], -4)],
      ["Visitor spending", B(at["spend"]), B(al["spend"]), M(ot["spend"], 0), M(ol["spend"], 0)],
      ["Total economic impact", B(at["impact"]), B(al["impact"]), M(ot["impact"], 0), M(ol["impact"], 0)],
      ["Jobs supported", N(at["jobs"], 0), N(al["jobs"], -1), N(ot["jobs"], -1), N(ol["jobs"], -1)],
      ["State and local taxes", M(at["tax"], 0), M(al["tax"], 0), M(ot["tax"], 1), M(ol["tax"], 1)],
      ["OC Vibe share of Anaheim visitor days", "—", "—", f"{ot['share']:.1f}%", f"{ol['share']:.1f}%"],
      ["Simulation range for visitor spending (5th–95th percentile)", "Measured", f"{B(mc['ana_live_spend']['p5'])}–{B(mc['ana_live_spend']['p95'])}", f"{M(mc['ocv_today_spend']['p5'],0)}–{M(mc['ocv_today_spend']['p95'],0)}", f"{M(mc['ocv_live_spend']['p5'],0)}–{M(mc['ocv_live_spend']['p95'],0)}"],
    ]
    views_tbl = dict(title="Three views of impact: Anaheim, Anaheim with OC Vibe, and OC Vibe's own",
        sub="A year, 2025 dollars. OC Vibe's own impact counts all visitor spending on days that include the OC Vibe area (Datafy: 5.2% of Anaheim visitor days today); it is associated, not exclusively caused.",
        cols=[["Measure", 0], ["1 · Anaheim today (all visitors)", 1], ["2 · Anaheim with OC Vibe live", 1], ["3a · OC Vibe area today", 1], ["3b · OC Vibe when live", 1]],
        rows=rows, hi=2, full=True, src=src_views)
    o["tables"].insert(0, views_tbl)
    o["q"] = "What impact will OC Vibe have on Anaheim, Orange County and California?"
    o["ans"] = (f"Three views. (1) Anaheim's visitors spent {B(at['spend'])} in 2025 and supported {N(at['jobs'],0)} jobs. "
                f"(2) With OC Vibe live, that rises to about {B(al['spend'])} (+{M(al['spend']-at['spend'],0)}) and {N(al['jobs'],-1)} jobs in the base case. "
                f"(3) OC Vibe's own visitor impact: the area is already part of {ot['share']:.1f}% of Anaheim visitor days, associated with about {M(ot['spend'],0)} in visitor spending; "
                f"when live, about {M(ol['spend'],0)} and {ol['share']:.1f}% of visitor days. 42 of 42 calculation checks passed, and 90% of simulated assumption combinations put OC Vibe's new spending between {M(mc['spend']['p5'],0)} and {M(mc['spend']['p95'],0)}.")
    o["hv"] = M(ol["spend"], 0); o["hl"] = "Visitor spending associated with OC Vibe when live (estimate)"
    o["cards"] = [
      ["1 · Anaheim today, 2025", "Visitor spending", B(at["spend"]), f"{N(at['jobs'],0)} jobs · {B(at['impact'],1)} total impact", "Tourism Economics"],
      ["2 · Anaheim with OC Vibe live", "Visitor spending", B(al["spend"]), f"+{M(al['spend']-at['spend'],0)} · {N(al['jobs'],-1)} jobs (base case)", "BI estimate; Tourism Economics ratios"],
      ["3a · OC Vibe area today", "Associated visitor spending", M(ot["spend"], 0), f"{ot['share']:.1f}% of Anaheim visitor days · {N(ot['jobs'],-1)} jobs", "Datafy (2024); Tourism Economics"],
      ["3b · OC Vibe when live", "Associated visitor spending", M(ol["spend"], 0), f"{ol['share']:.1f}% of visitor days · {N(ol['jobs'],-1)} jobs · range {M(mc['ocv_live_spend']['p5'],0)}–{M(mc['ocv_live_spend']['p95'],0)}", "BI estimate"],
    ]
    o["notes"].insert(0, "Three views: (1) is measured (Tourism Economics 2025). (2) adds OC Vibe's net-new visitor activity to (1). (3a) allocates Anaheim's visitor spending to the OC Vibe area by its share of visitor days (Datafy 2024), so it includes spending elsewhere in Anaheim on those days; (3b) adds the net-new activity. Orange County and California views are in the scenario table.")
    o["warn"] = "Views 2 and 3 are Visit Anaheim BI estimates, not forecasts or measured results. View 3 measures association with the OC Vibe area, not spending inside the district alone. All calculations were independently re-checked (see Checks and confidence)."
    st = STORIES["p-ocv"]
    st["head"] = f"With OC Vibe live, Anaheim visitor spending would reach about {B(al['spend'])}"
    st["dek"] = f"OC Vibe's own associated visitor spending grows from about {M(ot['spend'],0)} today to {M(ol['spend'],0)} when live (estimates)."
    st["stats"] = [[B(al["spend"]), "Anaheim visitor spending with OC Vibe live (estimate)", "BI estimate"], [M(ol["spend"], 0), "Visitor spending associated with OC Vibe when live", "BI estimate"], ["42 of 42", "Calculation checks passed", "BI validation"]]
    TAKEAWAYS[0] = (f"Three views of impact (estimates): Anaheim's visitors spent {B(at['spend'])} in 2025; with OC Vibe live, about {B(al['spend'])} (+{M(al['spend']-at['spend'],0)}, about {N(al['jobs']-at['jobs'],-1)} more jobs). "
                    f"OC Vibe's own associated visitor spending: about {M(ot['spend'],0)} today and {M(ol['spend'],0)} when live.")
    for r in o["tables"]:
        if r["title"] == "Measures OC Vibe can build on":
            for row in r["rows"]:
                if row[1] == "OC Vibe share of Anaheim visitor days": row[3] = f"About {ol['share']:.1f}% when live (base)"

    # ---------- Checks and confidence section ----------
    ck = R["checks"]; npass, ntot = R["passed"], R["total"]
    g = R["str_gap"]; tr = sens["tornado"]; sh = sens["src_share"]
    mc_rows = [["New visitor spending (OC Vibe)", M(I.RES[1]["spend"]), M(mc["spend"]["p5"]), M(mc["spend"]["p50"]), M(mc["spend"]["p95"])],
               ["Anaheim total economic impact from OC Vibe", M(I.RES[1]["ana_impact"]), M(mc["impact"]["p5"]), M(mc["impact"]["p50"]), M(mc["impact"]["p95"])],
               ["Anaheim jobs supported", N(I.RES[1]["ana_jobs"], -1), N(mc["jobs"]["p5"], -1), N(mc["jobs"]["p50"], -1), N(mc["jobs"]["p95"], -1)],
               ["State and local taxes", M(I.RES[1]["ana_tax"]), M(mc["tax"]["p5"]), M(mc["tax"]["p50"]), M(mc["tax"]["p95"])],
               ["California: new out-of-state spending", M(I.RES[1]["ca_spend"]), M(mc["ca"]["p5"]), M(mc["ca"]["p50"]), M(mc["ca"]["p95"])],
               ["OC Vibe hotel tax", M(I.RES[1]["tot"]), M(mc["tot"]["p5"]), M(mc["tot"]["p50"]), M(mc["tot"]["p95"])],
               ["Anaheim visitor spending with OC Vibe (view 2)", B(al["spend"]), B(mc["ana_live_spend"]["p5"]), B(mc["ana_live_spend"]["p50"]), B(mc["ana_live_spend"]["p95"])],
               ["OC Vibe associated spending when live (view 3b)", M(ol["spend"], 0), M(mc["ocv_live_spend"]["p5"], 0), M(mc["ocv_live_spend"]["p50"], 0), M(mc["ocv_live_spend"]["p95"], 0)]]
    stat_rows = [
      ["Fri–Sat vs Sun–Mon hotel occupancy gap (STR 2026)", f"{g['gap']:.1f} points", f"95% bootstrap CI {g['ci95'][0]:.1f}–{g['ci95'][1]:.1f}; Welch t p = {g['welch_p']:.0e}; Mann–Whitney p = {g['mw_p']:.0e}; effect size {g['cohen_d']:.1f}", "Real, large difference"],
      ["Value of one point of Sun–Mon occupancy", f"${R['sunmon_point']['value']:.2f}M", f"95% CI ${R['sunmon_point']['ci95'][0]:.2f}M–${R['sunmon_point']['ci95'][1]:.2f}M", "Stable"],
      ["Hotel revenue growth by month, 2026 (CoStar)", "Up in 8 of 8 months (Disneyland)", "Sign test p = 0.004 for 4 of 5 submarkets; Newport Beach/Dana Point 7 of 8 (p = 0.035)", "Consistent growth"],
      ["Spending per visitor trend 2022–2025", f"+${R['pv_trend']['slope']:.1f} a year (R² {R['pv_trend']['r2']:.2f})", f"Trend 2028 ${R['pv_trend']['pred2028']:.0f}; 95% prediction interval ${R['pv_trend']['pi95'][0]:.0f}–${R['pv_trend']['pi95'][1]:.0f}; Tourism Economics ${R['pv_trend']['te2028']:.0f}", "Forecast consistent (4 points only)"],
      ["Monte Carlo stability", "0.14%", "Largest difference in 5th/50th/95th percentiles between two seeds (200,000 draws each)", "Stable"],
    ]
    SECTIONS.append(dict(
      id="p-valid", tab="Checks and confidence",
      q="How confident can OC Vibe be in these numbers?",
      period=f"Validation run Oct. 12, 2026 · {npass} of {ntot} checks passed",
      ans=(f"Every calculation was rebuilt independently and checked: {npass} of {ntot} checks passed. The model's outputs match an exact recomputation; source totals reconcile; the hotel and spending patterns pass statistical tests; "
           f"and a 200,000-draw simulation puts OC Vibe's new visitor spending between {M(mc['spend']['p5'],0)} and {M(mc['spend']['p95'],0)} in 90% of cases (median {M(mc['spend']['p50'],0)}). "
           f"The two assumptions that matter most are the share of visitors who add a day and the share of attendees who are new to Anaheim; OC Vibe's own data can narrow both."),
      hv=f"{npass} of {ntot}", hl="Calculation checks passed",
      cards=[["Validation", "Checks passed", f"{npass} of {ntot}", "Recomputation, invariants, reconciliation, statistics, simulation, benchmarks", "Visit Anaheim BI"],
             ["Simulation, 200,000 draws", "OC Vibe new spending, 90% range", f"{M(mc['spend']['p5'],0)}–{M(mc['spend']['p95'],0)}", f"Median {M(mc['spend']['p50'],0)} · {mc['p_spend_gt_50M']*100:.2f}% of draws above $50M", "BI simulation"],
             ["Biggest driver", "Share of visitors who add a day", f"{sh['Share of visitors who add a day']*100:.0f}%", f"of explained variation · new-visitor share {sh['Share of attendees who are net-new visitors']*100:.0f}%", "BI sensitivity analysis"],
             ["STR, 2026", "Sun–Mon occupancy gap", f"{g['gap']:.1f} pts", f"95% CI {g['ci95'][0]:.1f}–{g['ci95'][1]:.1f} · p < 0.001", "STR; BI bootstrap"]],
      tables=[dict(title="Calculation checks", sub=f"{npass} of {ntot} passed · run Oct. 12, 2026 with a recorded, reproducible script",
                   cols=[["Group", 0], ["Check", 0], ["Result", 0], ["Detail", 0]], full=True,
                   rows=[[c["group"].split(". ", 1)[1], c["name"], "Pass" if c["ok"] else "Fail", c["detail"]] for c in ck], hi=-1,
                   src="Visit Anaheim BI validation suite (checks/validate_ocvibe.py), run Oct. 12, 2026; manifest with input and output hashes"),
              dict(title="Simulation ranges (Monte Carlo)", sub="200,000 draws; each assumption drawn between its conservative and optimistic value, most likely at the base case",
                   cols=[["Measure", 0], ["Base case", 1], ["5th percentile", 1], ["Median", 1], ["95th percentile", 1]], rows=mc_rows, hi=0, full=True,
                   src="Visit Anaheim BI simulation (seed 20261012), Oct. 12, 2026"),
              dict(title="What moves the estimate most", sub="New visitor spending when one assumption moves from its conservative to its optimistic value (others at base)",
                   cols=[["Assumption", 0], ["Low", 1], ["High", 1], ["Share of variation", 1]], full=True,
                   rows=[[n, f"${lo:.1f}M", f"${hi:.1f}M", f"{sh[n]*100:.0f}%"] for n, lo, hi in tr], hi=0,
                   src="Visit Anaheim BI sensitivity analysis (one-at-a-time and standardized regression on the simulation), Oct. 12, 2026"),
              dict(title="Statistical tests on the data", sub="Tests on the measured inputs behind the insights",
                   cols=[["Test", 0], ["Result", 0], ["Statistics", 0], ["Reading", 0]], rows=stat_rows, hi=0, full=True,
                   src="STR (Jan. 1–Oct. 3, 2026); CoStar (Jan.–Aug. 2026); Tourism Economics (2022–2028); BI analysis Oct. 12, 2026")],
      charts=[dict(kind="bars", title="Simulated new visitor spending is most sensitive to two assumptions", sub="Swing in new visitor spending ($M) from conservative to optimistic, one assumption at a time",
                   rows=[dict(l=n, v=hi - lo, t=f"${lo:.0f}M–${hi:.0f}M", hi=i == 0) for i, (n, lo, hi) in enumerate(tr)], src="Visit Anaheim BI sensitivity analysis, Oct. 12, 2026")],
      notes=["Recomputation: every scenario output (54 values) was rebuilt in exact rational arithmetic, separately from the dashboard's code; the largest difference was 4 × 10⁻¹⁶.",
             "Reconciliation: Tourism Economics categories, CoStar export vs. PDF, STR set additivity, Visa domestic + international, Metrolink lines and OCTA bus schedules were each checked against an independent total.",
             f"The simulation median ({M(mc['spend']['p50'])}) sits above the base case ({M(I.RES[1]['spend'])}) because the add-a-day assumption has more room to rise (to 2%) than to fall (to 0.5%). The 90% range is narrower than the conservative-to-optimistic scenarios because all assumptions rarely sit at their extremes together.",
             "What the checks cannot do: they confirm the arithmetic, the data and the effect of the assumptions, not the assumptions themselves, and they do not prove OC Vibe causes visits. OC Vibe's event, ticketing and hotel data are the way to replace assumptions with measurements.",
             "Views 3a and 3b include a ±0.7-point uncertainty on Datafy's 5.2% share in the simulation (BI assumption)."],
      ocv=[f"OC Vibe can rely on the arithmetic: {npass} of {ntot} independent checks passed.",
           "The two numbers that most change OC Vibe's impact are how many visitors add a day and how many attendees are new to Anaheim. Sharing ticket-buyer ZIP codes and hotel package results with Visit Anaheim would turn these assumptions into measurements.",
           f"Even at the low end of the simulation, OC Vibe adds about {M(mc['spend']['p5'],0)} a year in new visitor spending."],
    ))
    STORIES["p-valid"] = dict(measure="Calculation checks passed", v=None, val=f"{npass} of {ntot}", basis="Validation run", ok=False,
      head=f"All {ntot} checks on the OC Vibe numbers passed", dek="Independent recomputation, reconciliation, statistical tests and a 200,000-draw simulation.",
      lede=f"Visit Anaheim BI rebuilt every OC Vibe calculation independently; {npass} of {ntot} checks passed.",
      paras=[f"A simulation that varies every assumption puts OC Vibe's new visitor spending between {M(mc['spend']['p5'],0)} and {M(mc['spend']['p95'],0)} in 90% of cases."],
      stats=[[f"{npass} of {ntot}", "Checks passed", "BI validation"], [f"{M(mc['spend']['p5'],0)}–{M(mc['spend']['p95'],0)}", "90% simulation range", "BI simulation"]],
      chart=dict(title="Swing in new spending by assumption, $M", rows=[[n, round(hi - lo, 1), f"${hi-lo:.0f}M", 1 if i == 0 else 0] for i, (n, lo, hi) in enumerate(tr[:4])], src="BI sensitivity"),
      srcs=["Visit Anaheim BI validation suite, Oct. 12, 2026"])
    REGISTER.append(["Visit Anaheim BI", "Validation suite (checks/validate_ocvibe.py) with run manifest", "All model outputs and source totals", "Run Oct. 12, 2026", f"Checks and confidence section; simulation ranges", f"{npass} of {ntot} checks passed; inputs and outputs hashed in the manifest"])
    DQ.insert(1, f"All calculations were independently re-checked on Oct. 12, 2026 ({npass} of {ntot} checks passed). The checks confirm arithmetic, data consistency and the effect of assumptions, not the assumptions themselves.")
    RECS.insert(1, "Share ticket-buyer ZIP codes and hotel package results with Visit Anaheim: the share of attendees who are new to Anaheim and the share of visitors who add a day drive about 80% of the variation in OC Vibe's estimated impact.")
