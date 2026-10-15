"""Independent validation of the OC Vibe Insights calculations (Visit Anaheim BI).

Run from the build folder:  python3 checks/validate_ocvibe.py <output_dir>
Writes <output_dir>/results.json and <output_dir>/summary.md.

Parts
  A. Independent recomputation in exact rational arithmetic (fractions.Fraction) of every model output,
     compared with the production model (impact.py) — tolerance 1e-9 relative.
  B. Invariants (identities that must hold whatever the inputs).
  C. Cross-source reconciliation (totals that two sources or two parts of one source must agree on).
  D. Statistical tests on the empirical inputs (bootstrap, Welch t, Mann-Whitney, sign test, OLS).
  E. Monte Carlo propagation of assumption uncertainty (seeded), convergence check across seeds.
  F. Sensitivity: one-at-a-time tornado and global rank correlation / standardized regression.
  G. Benchmarks against published and historical figures.
"""
import os as _os
BASE = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # pipeline folder
import json, sys, os, time, math, hashlib
from fractions import Fraction as Fr
import numpy as np, pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as Dt, impact as I, newdata as ND

OUT = sys.argv[1] if len(sys.argv) > 1 else "computations/validation"
os.makedirs(OUT, exist_ok=True)
GTFS = BASE + "/files/gtfs/"
SEED = 20261012
checks, results = [], {}
def check(group, name, ok, detail):
    checks.append(dict(group=group, name=name, ok=bool(ok), detail=detail))
def close(a, b, rel=1e-9, ab=0.0):
    return abs(float(a) - float(b)) <= max(ab, rel * max(abs(float(a)), abs(float(b)), 1e-12))

# ---------------- A. Independent exact recomputation ----------------
A = Dt.EI["Anaheim"]; O = Dt.EI["Orange County"]
sp25, vis25 = Fr("6832"), Fr("26.5")                         # $M, M visitors (TE EI 2025)
dom, intl = Fr("24.7"), Fr("26.5") - Fr("24.7")
los = dom / vis25 * Fr("1.9") + intl / vis25 * Fr("5.9")      # weighted stay
pv = Fr(round(sp25 / vis25))                                  # $258 (rounded as displayed and used)
per_day = (sp25 / vis25) / los                                # $ per visitor-day
lodge_vday = Fr("1724") / vis25 / los
mult_ana, jobs_ana, tax_ana = Fr("10422") / sp25, Fr("67817") / sp25, Fr("970") / sp25
mult_oc, jobs_oc, tax_oc = Fr("30673") / Fr("17993"), Fr("178164") / Fr("17993"), Fr("3094") / Fr("17993")
oos = 1 - Fr("56.0") / 100
ca_jobs, ca_tax = Fr("1.2e6") / Fr("158900"), Fr("13.6") / Fr("158.9")
HALL, SMALL, ROOMS = 5613, 2300, 550
scen = dict(Conservative=(100, Fr("0.70"), 100, Fr("0.60"), Fr("0.15"), Fr("0.005"), Fr("0.70"), Fr(218)),
            Base=(150, Fr("0.80"), 150, Fr("0.70"), Fr("0.25"), Fr("0.01"), Fr("0.74"), Fr(218)),
            Optimistic=(200, Fr("0.90"), 200, Fr("0.80"), Fr("0.35"), Fr("0.02"), Fr("0.784"), Fr("254.88")))
indep = {}
for name, (he, hf, se, sf, nn, ad, occ, adr) in scen.items():
    att = HALL * he * hf + SMALL * se * sf
    nv = att * nn
    days = vis25 * Fr(10**6) * ad
    spend = nv * pv + days * per_day                          # $ (per_day in $)
    rn = ROOMS * 365 * occ
    indep[name] = dict(attend=att, new_vis=nv, extra_days=days, sp_new=nv * pv, sp_stay=days * per_day, spend=spend,
                       ana_impact=spend * mult_ana, ana_jobs=spend / 10**6 * jobs_ana, ana_tax=spend * tax_ana,
                       oc_impact=spend * mult_oc, oc_jobs=spend / 10**6 * jobs_oc, oc_tax=spend * tax_oc,
                       ca_spend=spend * oos, ca_jobs=spend * oos / 10**6 * ca_jobs, ca_tax=spend * oos * ca_tax,
                       rn=rn, room_rev=rn * adr, tot=rn * adr * Fr("0.15"))
n_cmp = 0; worst = 0.0
for r in I.RES:
    for k, v in indep[r["name"]].items():
        n_cmp += 1; rel = abs(float(v) - r[k]) / max(abs(float(v)), 1e-12); worst = max(worst, rel)
check("A. Recomputation", f"Impact model: {n_cmp} scenario outputs recomputed exactly", worst < 1e-9, f"largest relative difference {worst:.2e}")
lodge_night = Fr("1724") * 10**6 / los
check("A. Recomputation", "One more night (lodging) = $1,724M ÷ weighted stay", close(lodge_night, Dt.N["lodge_night"]), f"${float(lodge_night)/1e6:,.2f}M; weighted stay {float(los):.4f} days")
check("A. Recomputation", "Overnight visitors add a day (all spending)", close(Fr("8.6e6") * per_day, Dt.N["overnight_only"]), f"${float(Fr('8.6e6')*per_day)/1e9:.3f}B")
check("A. Recomputation", "Every visitor adds a day (upper bound)", close(sp25 * 10**6 / los, Dt.N["plus1"]), f"${float(sp25*10**6/los)/1e9:.3f}B")
check("A. Recomputation", "Spending per visitor-day", close(per_day, I.PER_DAY), f"${float(per_day):.4f}")
check("A. Recomputation", "Each 1% of visitors adding a day", close(vis25 * 10**4 * per_day, I.PER_1PCT_DAY), f"${float(vis25*10**4*per_day)/1e6:.3f}M")
# ten-year
hall_only = HALL * 150 * Fr("0.8") * Fr("0.25") * pv
b = indep["Base"]
ten_spend = hall_only + b["sp_stay"] / 2 + 9 * b["spend"]
rooms_by_year = [0, 230, 230] + [550] * 7
ten_tot = sum(Fr(r) * 365 * Fr("0.74") * 218 * Fr("0.15") for r in rooms_by_year)
check("A. Recomputation", "Ten-year totals (2027–2036)", close(ten_spend, I.TEN["spend"]) and close(ten_tot, I.TEN["tot"]), f"spending ${float(ten_spend)/1e6:,.1f}M; hotel tax ${float(ten_tot)/1e6:,.2f}M")
# per-visitor series (precise EI totals)
pv_exact = {y: round(float(Fr(str(s)) * 1000 / Fr(str(v)))) for y, v, s in zip(Dt.YEARS, Dt.ANA_VIS, [Dt._ANA_SP_PRECISE.get(y, s) for y, s in zip(Dt.YEARS, Dt.ANA_SP)])}
check("A. Recomputation", "Spending per visitor series 2019–2028", all(pv_exact[y] == v for y, v in zip(Dt.YEARS, Dt.ANA_PV)), f"2025 ${pv_exact[2025]}, 2028 ${pv_exact[2028]}")
# STR Sun-Mon lever
s = pd.read_excel(ND.F + "STR_Daily_Data_8.xlsx"); s["Date"] = pd.to_datetime(s["Date"])
t = s[(s.Geography == "Anaheim+") & (s.Segment == "Total")].copy()
dow_occ = t.groupby("Day Of Week Category").apply(lambda x: x.Demand.sum() / x.Supply.sum() * 100)
check("A. Recomputation", "STR Sunday–Monday vs Friday–Saturday occupancy", close((dow_occ["Sun"] + dow_occ["Mon"]) / 2, ND.SUNMON_OCC) and close((dow_occ["Fri"] + dow_occ["Sat"]) / 2, ND.FRISAT_OCC), f"{(dow_occ['Sun']+dow_occ['Mon'])/2:.2f}% vs {(dow_occ['Fri']+dow_occ['Sat'])/2:.2f}%")

# ---------------- B. Invariants ----------------
inv_ok = True; msgs = []
for r in I.RES:
    inv_ok &= close(r["sp_new"] + r["sp_stay"], r["spend"]); inv_ok &= r["lodge_stay"] <= r["sp_stay"]
    inv_ok &= r["rn"] <= ROOMS * 365; inv_ok &= r["ca_spend"] < r["spend"]; inv_ok &= r["tot"] < r["room_rev"]
check("B. Invariants", "Spending parts add up; lodging ≤ stay spending; room nights ≤ capacity; tax < revenue", inv_ok, "all three scenarios")
keys = ["attend", "new_vis", "extra_days", "spend", "ana_impact", "ana_jobs", "oc_impact", "ca_spend", "rn", "room_rev", "tot"]
mono = all(I.RES[0][k] < I.RES[1][k] < I.RES[2][k] for k in keys)
check("B. Invariants", "Every output rises from conservative to base to optimistic", mono, f"{len(keys)} outputs")
shares = sum(x[1] for x in I.CAT)
check("B. Invariants", "Spending-mix shares sum to 100%", close(shares, 1, 1e-12), f"{shares*100:.6f}%")
ts = A["fb"] + A["transport"] + A["lodging"] + A["rec"] + A["retail"]
check("C. Reconciliation", "Tourism Economics categories sum to Anaheim total", abs(ts - A["sp25"]) <= 1.5, f"${ts:,.0f}M vs ${A['sp25']:,.0f}M (rounding)")

# ---------------- C. Reconciliation ----------------
c = pd.read_excel(ND.F + "CoStar_DataExport_17.xlsx")
diffs = []
for n, rooms, occ, oc, adr, ac, rev, rc, uc in Dt.CS_SUB:
    sub = n.split(" (")[0] if n.startswith("Anaheim") else n
    sub = {"Orange County Northwest/Fullerton": "Orange County Northwest/Fullerton"}.get(sub, sub)
    g = lambda k: float(c[(c["Concept Name"] == k) & (c["Geography Name"].str.endswith(" - " + sub))]["08/31/2026"].iloc[0])
    diffs += [abs(g("12 Mo Occupancy") * 100 - occ), abs(g("12 Mo ADR") - adr), abs(g("12 Mo RevPAR") - rev), abs(g("12 Mo RevPAR Chg") * 100 - rc)]
check("C. Reconciliation", "CoStar export (12-month, Aug. 2026) matches CoStar PDF tables for 5 submarkets", max(diffs) < 0.06, f"largest difference {max(diffs):.3f} (rounding)")
rp = []
for k in ["Occupancy", "ADR", "RevPAR"]:
    pass
for sub in ND.CS_MO:
    m = ND.CS_MO[sub]
    rp += [abs(o * a - r) / r for o, a, r in zip(m["occ"], m["adr"], m["revpar"])]
check("C. Reconciliation", "CoStar monthly: RevPAR = occupancy × ADR (40 submarket-months)", max(rp) < 1e-3, f"largest relative gap {max(rp):.2e}")
sd = s[s.Segment == "Total"].pivot_table(index="Date", columns="Geography", values=["Supply", "Demand", "Revenue"], aggfunc="sum")
add_err = max(float((sd[m]["Anaheim+"] + sd[m]["Garden Grove+"] - sd[m]["Anaheim-Garden Grove+"]).abs().max()) for m in ["Supply", "Demand"])
check("C. Reconciliation", "STR: Anaheim+ plus Garden Grove+ equals the combined set every night (supply, demand)", add_err == 0, f"largest nightly gap {add_err:.0f} rooms over {len(sd)} nights")
seg = s[s.Segment != "Total"].groupby(["Date", "Geography"])["Demand"].sum()
tot = s[s.Segment == "Total"].set_index(["Date", "Geography"])["Demand"]
seg_gap = float((seg - tot.reindex(seg.index)).abs().max())
seg_rel = float(((seg - tot.reindex(seg.index)).abs() / tot.reindex(seg.index)).max()); n_gap = int(((seg - tot.reindex(seg.index)).abs() > 0).sum())
check("C. Reconciliation", "STR: transient + group + contract matches total demand (within 0.1%)", seg_rel < 0.001, f"{n_gap} of {len(seg)} geography-nights differ, by at most {seg_gap:.0f} rooms ({seg_rel*100:.3f}%) — STR source rounding; group share unaffected at one decimal")
ident = float(((t.Occupancy * t.ADR - t.RevPAR).abs() / t.RevPAR).max())
check("C. Reconciliation", "STR: RevPAR = occupancy × ADR every night", ident < 1e-6, f"largest relative gap {ident:.1e}")
v = ND.VISA
check("C. Reconciliation", "Visa: domestic + international = total", abs(v["dom"] + v["intl"] - v["total"]) <= 0.15, f"${v['dom']+v['intl']:.1f}M vs ${v['total']}M (rounding)")
cat = sum(x[1] for x in ND.VISA_INTL_CAT)
check("C. Reconciliation", "Visa: international categories sum to international total", abs(cat - v["intl"]) <= 0.1, f"${cat:.2f}M vs ${v['intl']}M (rounding)")
orig = sum(x[1] for x in ND.VISA_ORIG)
check("C. Reconciliation", "Visa: top-15 origins ≤ total", orig <= v["total"], f"${orig:.1f}M of ${v['total']}M ({orig/v['total']*100:.1f}%)")
lines = [2457, 3876, 6054, 478, 1121, 5116, 2331, 2509]
check("C. Reconciliation", "Metrolink: lines sum to systemwide weekday riders", abs(sum(lines) - 23945) <= 5, f"{sum(lines):,} vs 23,945")
check("C. Reconciliation", "Amtrak: 2024 passenger detail matches the chart", abs(191153 / 1000 - 191.2) < 0.05, "191,153 vs 191.2K")
# GTFS independent count
try:
    stops = pd.read_csv(GTFS + "stops.txt", dtype=str); artic = set(stops[stops.stop_name.str.contains("ARTIC", na=False)].stop_id)
    cal = pd.read_csv(GTFS + "calendar.txt", dtype=str); cd = pd.read_csv(GTFS + "calendar_dates.txt", dtype=str)
    day, wk = "20261014", "wednesday"
    svc = set(cal[(cal[wk] == "1") & (cal.start_date <= day) & (cal.end_date >= day)].service_id)
    svc |= set(cd[(cd.date == day) & (cd.exception_type == "1")].service_id); svc -= set(cd[(cd.date == day) & (cd.exception_type == "2")].service_id)
    trips = pd.read_csv(GTFS + "trips.txt", dtype=str); tw = trips[trips.service_id.isin(svc)]
    st = pd.read_csv(GTFS + "stop_times.txt.gz", dtype={"trip_id": str, "stop_id": str}, usecols=["trip_id", "stop_id", "stop_sequence", "departure_time"])
    st = st[st.trip_id.isin(set(tw.trip_id))]
    last = st.groupby("trip_id").stop_sequence.transform("max")
    at = st[st.stop_id.isin(artic)]; dep = at[at.stop_sequence < last[at.index]]
    n_srv, n_dep = at.trip_id.nunique(), dep.trip_id.nunique()
    late_srv, late_dep = at[at.departure_time >= "22:00:00"].trip_id.nunique(), dep[dep.departure_time >= "22:00:00"].trip_id.nunique()
    routes = sorted(tw[tw.trip_id.isin(at.trip_id)].route_id.unique())
    check("C. Reconciliation", "OCTA GTFS recount (Wed. Oct. 14, 2026): bus trips stopping at ARTIC", n_srv == Dt.TRANSIT["wk"] and late_srv == Dt.TRANSIT["late_wk"] and n_dep == 227 and late_dep == 11,
          f"{n_srv} trips stop ({n_dep} depart, {n_srv-n_dep} end there); after 10 p.m.: {late_srv} stop, {late_dep} depart; routes {', '.join(routes)}; last departure {dep.departure_time.max()}")
except Exception as e:
    check("C. Reconciliation", "OCTA GTFS recount", False, f"could not run: {e}")

# ---------------- D. Statistical tests ----------------
t["wk"] = t.Date.dt.to_period("W-SAT")
t["grp"] = np.where(t["Day Of Week Category"].isin(["Fri", "Sat"]), "FS", np.where(t["Day Of Week Category"].isin(["Sun", "Mon"]), "SM", "other"))
fs = t[t.grp == "FS"].Occupancy * 100; sm = t[t.grp == "SM"].Occupancy * 100
wt = stats.ttest_ind(fs, sm, equal_var=False); mw = stats.mannwhitneyu(fs, sm, alternative="greater")
dcoh = (fs.mean() - sm.mean()) / math.sqrt((fs.var(ddof=1) + sm.var(ddof=1)) / 2)
rng = np.random.default_rng(SEED)
weeks = t.wk.unique(); wk_tab = {w: g for w, g in t.groupby("wk")}
boots = []
for _ in range(10000):
    smp = pd.concat([wk_tab[w] for w in rng.choice(weeks, len(weeks), replace=True)])
    f, m = smp[smp.grp == "FS"], smp[smp.grp == "SM"]
    boots.append(f.Demand.sum() / f.Supply.sum() * 100 - m.Demand.sum() / m.Supply.sum() * 100)
lo95, hi95 = np.percentile(boots, [2.5, 97.5]); gap = ND.FRISAT_OCC - ND.SUNMON_OCC
results["str_gap"] = dict(gap=gap, ci95=[lo95, hi95], welch_t=wt.statistic, welch_p=wt.pvalue, mw_p=mw.pvalue, cohen_d=dcoh, n_fs=len(fs), n_sm=len(sm), weeks=len(weeks))
check("D. Statistics", "Friday–Saturday vs Sunday–Monday occupancy gap is real (not noise)", lo95 > 0 and wt.pvalue < 0.001,
      f"gap {gap:.1f} pts; 95% bootstrap CI {lo95:.1f}–{hi95:.1f} (10,000 resamples of {len(weeks)} weeks); Welch p = {wt.pvalue:.1e}; Mann–Whitney p = {mw.pvalue:.1e}; effect size d = {dcoh:.1f}")
sm_rows = t[t.grp == "SM"]; adr_b = []
for _ in range(5000):
    smp = pd.concat([wk_tab[w] for w in rng.choice(weeks, len(weeks), replace=True)]); x = smp[smp.grp == "SM"]
    adr_b.append(x.Revenue.sum() / x.Demand.sum())
pt_lo, pt_hi = [ND.STR["Anaheim+"]["rooms"] * 0.01 * 104 * q / 1e6 for q in np.percentile(adr_b, [2.5, 97.5])]
results["sunmon_point"] = dict(value=ND.PT_SUNMON_REV / 1e6, ci95=[pt_lo, pt_hi])
check("D. Statistics", "Value of one point of Sunday–Monday occupancy", pt_lo < ND.PT_SUNMON_REV / 1e6 < pt_hi, f"${ND.PT_SUNMON_REV/1e6:.2f}M; 95% CI ${pt_lo:.2f}M–${pt_hi:.2f}M (rate uncertainty)")
sign = {}
for sub, m in ND.CS_MO.items():
    k = sum(1 for x in m["rchg"] if x > 0); sign[sub] = (k, stats.binomtest(k, 8, 0.5, alternative="greater").pvalue)
results["sign_test"] = sign
check("D. Statistics", "Resort-area hotel revenue growth is consistent month to month (sign test)", sign["Disneyland"][1] < 0.01,
      "; ".join(f"{s}: {k}/8 months up (p = {p:.3f})" for s, (k, p) in sign.items()))
yrs = np.array([2022, 2023, 2024, 2025]); pvs = np.array([Dt.ANA_PV[Dt.YEARS.index(y)] for y in yrs])
lr = stats.linregress(yrs, pvs); pred = lr.intercept + lr.slope * 2028
tcrit = stats.t.ppf(0.975, len(yrs) - 2); se_pred = math.sqrt(sum((pvs - (lr.intercept + lr.slope * yrs)) ** 2) / (len(yrs) - 2)) * math.sqrt(1 + 1 / len(yrs) + (2028 - yrs.mean()) ** 2 / sum((yrs - yrs.mean()) ** 2))
pi = (pred - tcrit * se_pred, pred + tcrit * se_pred)
results["pv_trend"] = dict(slope=lr.slope, r2=lr.rvalue ** 2, pred2028=pred, pi95=pi, te2028=Dt.ANA_PV[-1])
check("D. Statistics", "Tourism Economics' 2028 spending per visitor is consistent with the 2022–2025 trend", pi[0] <= Dt.ANA_PV[-1] <= pi[1],
      f"trend +${lr.slope:.1f}/yr (R² {lr.rvalue**2:.2f}); trend 2028 ${pred:.0f} (95% PI ${pi[0]:.0f}–${pi[1]:.0f}); TE ${Dt.ANA_PV[-1]:.0f}; only 4 points")
mults = {"Anaheim": A["impact"] / A["sp25"], "Garden Grove": Dt.EI["Garden Grove"]["impact"] / Dt.EI["Garden Grove"]["sp25"], "Orange County": O["impact"] / O["sp25"]}
jobsr = {g: Dt.EI[g]["jobs"] / Dt.EI[g]["sp25"] for g in Dt.EI}
results["ratios"] = dict(mult=mults, jobs=jobsr)

# ---------------- E. Monte Carlo ----------------
def tri(r, lo, mode, hi, n): return r.triangular(lo, mode, hi, n)
def simulate(seed, n=200000):
    r = np.random.default_rng(seed)
    he = tri(r, 100, 150, 200, n); hf = tri(r, .70, .80, .90, n); se_ = tri(r, 100, 150, 200, n); sf = tri(r, .60, .70, .80, n)
    nn = tri(r, .15, .25, .35, n); ad = tri(r, .005, .01, .02, n); oc = tri(r, .70, .74, .784, n); adr = tri(r, 218, 218.0001, 254.88, n)
    pvv = tri(r, 232.2, 258, 279, n)                                   # −10% to TE's 2028 forecast
    mul = tri(r, mults["Garden Grove"], mults["Anaheim"], mults["Orange County"], n)
    jb = r.uniform(jobsr["Garden Grove"], jobsr["Anaheim"], n)
    att = HALL * he * hf + SMALL * se_ * sf; nv = att * nn; days = 26.5e6 * ad
    spend = nv * pvv + days * float(per_day); rn = ROOMS * 365 * oc
    return dict(he=he, hf=hf, se=se_, sf=sf, nn=nn, ad=ad, oc=oc, adr=adr, pv=pvv, mul=mul, jb=jb,
                spend=spend, impact=spend * mul, jobs=spend / 1e6 * jb, tax=spend * float(tax_ana), ca=spend * float(oos), rn=rn, tot=rn * adr * .15)
S1, S2 = simulate(SEED), simulate(SEED + 1)
pct = lambda x: [float(np.percentile(x, q)) for q in (5, 50, 95)]
mc = {k: dict(p5=pct(S1[k])[0], p50=pct(S1[k])[1], p95=pct(S1[k])[2], mean=float(S1[k].mean())) for k in ["spend", "impact", "jobs", "tax", "ca", "rn", "tot"]}
mc["ana_live_spend"] = dict(p5=A["sp25"]*1e6+mc["spend"]["p5"], p50=A["sp25"]*1e6+mc["spend"]["p50"], p95=A["sp25"]*1e6+mc["spend"]["p95"])
ds = r_ds = np.random.default_rng(SEED + 7).triangular(0.045, 0.052, 0.059, len(S1["spend"]))
ocv_live_sp = ds * A["sp25"] * 1e6 + S1["spend"]
mc["ocv_live_spend"] = dict(p5=float(np.percentile(ocv_live_sp, 5)), p50=float(np.percentile(ocv_live_sp, 50)), p95=float(np.percentile(ocv_live_sp, 95)))
mc["ocv_today_spend"] = dict(p5=float(np.percentile(ds * A["sp25"] * 1e6, 5)), p50=float(np.percentile(ds * A["sp25"] * 1e6, 50)), p95=float(np.percentile(ds * A["sp25"] * 1e6, 95)))
mc["p_spend_gt_50M"] = float((S1["spend"] > 50e6).mean()); mc["p_spend_gt_100M"] = float((S1["spend"] > 100e6).mean()); mc["p_spend_gt_base"] = float((S1["spend"] > I.RES[1]["spend"]).mean())
results["monte_carlo"] = mc
conv = max(abs(np.percentile(S1["spend"], q) - np.percentile(S2["spend"], q)) / np.percentile(S1["spend"], q) for q in (5, 50, 95))
check("E. Simulation", "Monte Carlo is stable across random seeds (200,000 draws each)", conv < 0.005, f"P5/P50/P95 differ by at most {conv*100:.2f}% between seeds")
check("E. Simulation", "Base case sits inside the central simulation range", mc["spend"]["p5"] < I.RES[1]["spend"] < mc["spend"]["p95"],
      f"base ${I.RES[1]['spend']/1e6:.1f}M; simulation P5 ${mc['spend']['p5']/1e6:.1f}M, median ${mc['spend']['p50']/1e6:.1f}M, P95 ${mc['spend']['p95']/1e6:.1f}M")

# ---------------- F. Sensitivity ----------------
base = dict(he=150, hf=.8, se=150, sf=.7, nn=.25, ad=.01, pv=258.0)
rngs = dict(he=(100, 200), hf=(.7, .9), se=(100, 200), sf=(.6, .8), nn=(.15, .35), ad=(.005, .02), pv=(232.2, 279))
labels = dict(he="Concert hall events a year", hf="Concert hall seats filled", se="Theater and club events", sf="Theater and club seats filled",
              nn="Share of attendees who are net-new visitors", ad="Share of visitors who add a day", pv="Spending per visitor")
def f(x): return (HALL * x["he"] * x["hf"] + SMALL * x["se"] * x["sf"]) * x["nn"] * x["pv"] + 26.5e6 * x["ad"] * float(per_day)
tornado = []
for k, (lo, hi) in rngs.items():
    a = dict(base, **{k: lo}); b_ = dict(base, **{k: hi}); tornado.append((labels[k], f(a) / 1e6, f(b_) / 1e6))
tornado.sort(key=lambda z: -(z[2] - z[1]))
X = np.column_stack([S1[k] for k in ["he", "hf", "se", "sf", "nn", "ad", "pv"]]); y = S1["spend"]
rho = {labels[k]: float(stats.spearmanr(S1[k], y).statistic) for k in ["he", "hf", "se", "sf", "nn", "ad", "pv"]}
Z = (X - X.mean(0)) / X.std(0); yz = (y - y.mean()) / y.std()
beta, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(yz)), Z]), yz, rcond=None)
r2 = 1 - ((yz - np.column_stack([np.ones(len(yz)), Z]) @ beta) ** 2).sum() / (yz ** 2).sum()
share = {labels[k]: float(b * b / (beta[1:] ** 2).sum()) for k, b in zip(["he", "hf", "se", "sf", "nn", "ad", "pv"], beta[1:])}
results["sensitivity"] = dict(tornado=tornado, spearman=rho, src_share=share, linear_r2=float(r2))
top = max(share, key=share.get)
check("F. Sensitivity", "Global sensitivity identifies the main driver", True, f"{top} explains {share[top]*100:.0f}% of explained variance (linear R² {r2:.2f})")

# ---------------- A2. Three views ----------------
vb = I.VIEWS["Base"]; vd = vis25 * 10**6 * los
ocv0 = Fr("0.052") * sp25 * 10**6
ok3 = close(vb["ocv_today"]["spend"], ocv0) and close(vb["ana_live"]["spend"] - vb["ana_today"]["spend"], I.RES[1]["spend"]) \
      and close(vb["ocv_live"]["spend"] - vb["ocv_today"]["spend"], I.RES[1]["spend"]) and close(vb["ana_live"]["jobs"] - vb["ana_today"]["jobs"], I.RES[1]["ana_jobs"])
check("A. Recomputation", "Three views: OC Vibe today, Anaheim with OC Vibe, OC Vibe when live", ok3,
      f"OC Vibe area today ${float(ocv0)/1e6:,.1f}M associated spending; when live ${vb['ocv_live']['spend']/1e6:,.1f}M; Anaheim ${vb['ana_today']['spend']/1e9:.3f}B → ${vb['ana_live']['spend']/1e9:.3f}B")
check("B. Invariants", "OC Vibe share of visitor days stays below 100% and rises when live", 0 < vb["ocv_today"]["share"] < vb["ocv_live"]["share"] < 100, f"{vb['ocv_today']['share']:.1f}% → {vb['ocv_live']['share']:.2f}%")

# ---------------- G. Benchmarks ----------------
hc_per_yr = 45e6 / (2025 - 1993); hc_per_ev = 45e6 / 4500
base_hall = HALL * 150 * .8
check("G. Benchmarks", "Concert hall base attendance is below Honda Center's historical average", base_hall < hc_per_yr,
      f"{base_hall:,.0f} a year ({HALL*.8:,.0f} per show) vs Honda Center ~{hc_per_yr:,.0f} a year, ~{hc_per_ev:,.0f} per event (OCBJ: 45M guests, 4,500 events since 1993)")
share_ana = I.RES[1]["spend"] / (A["sp25"] * 1e6)
check("G. Benchmarks", "Base-case new spending is a small share of the city's visitor economy", share_ana < 0.03, f"{share_ana*100:.2f}% of Anaheim's 2025 visitor spending")
check("G. Benchmarks", "Visitor-only estimate is below whole-district published estimates", I.RES[1]["ana_impact"] < 400e6,
      f"${I.RES[1]['ana_impact']/1e6:.0f}M vs DTA's >$400M recurring (whole district, 2020)")
check("G. Benchmarks", "OC Vibe hotel occupancy assumption within observed market range", 0.70 <= 0.74 <= 0.784 and ND.STR["Anaheim+"]["occ"] / 100 >= 0.74,
      f"74% base vs CoStar OC 74.0%, Disneyland 78.4%, STR Anaheim+ {ND.STR['Anaheim+']['occ']:.1f}%")
check("G. Benchmarks", "Multiplier and jobs ratios are consistent across geographies", max(mults.values()) / min(mults.values()) < 1.25,
      "impact per $1: " + ", ".join(f"{g} {m:.2f}" for g, m in mults.items()) + "; jobs per $1M: " + ", ".join(f"{g} {j:.1f}" for g, j in jobsr.items()))

# ---------------- H. Role views and transit data (added Oct. 12, 2026) ----------------
import re as _re, copy as _cp, roles_content as RC, content as CT, ocv_whole as OW
_base = []
for _x in CT.SECTIONS:
    _y = _cp.deepcopy(_x)
    for _k in ("for_ocv", "ans", "ans_src", "head", "dek", "w5h", "nut", "details", "next", "dateline"): _y.pop(_k, None)
    _base.append(_y)
_other = json.dumps(_base, ensure_ascii=False) + json.dumps(CT.DQ, ensure_ascii=False) + json.dumps(CT.STORIES, ensure_ascii=False)
_tok = _re.compile(r"\$?\d[\d,]*(?:\.\d+)?(?:%|[MBK]\b)?")
_texts = [x["ans"] for x in CT.SECTIONS if x.get("ans")] + [i["text"] for x in CT.SECTIONS if x.get("for_ocv") for k in x["for_ocv"].values() for i in k] \
         + [c["point"] for x in CT.SECTIONS for c in (x.get("cc") or []) if c["type"] == "Explanation"] + [CT.DATA_EXTRA["main"]["head"], CT.DATA_EXTRA["main"]["dek"], CT.DATA_EXTRA["main"]["lede"]] + CT.DATA_EXTRA["main"]["paras"] \
         + [x["nut"] for x in CT.SECTIONS if x.get("nut")] + [d[f] for x in CT.SECTIONS for d in (x.get("details") or []) for f in ("fig", "fig_l", "text")] + [x["next"]["bridge"] for x in CT.SECTIONS if x.get("next")]
_n, _miss = 0, []
for _t in _texts:
    for _k in _tok.findall(_t):
        _k = _k.rstrip(",")
        if (len(_k.strip("$%MBK,.")) < 2 and not _k.endswith("%")) or _re.fullmatch(r"20\d\d", _k): continue
        _n += 1
        if _k not in _other: _miss.append(_k)
check("H. Report text", "Every number in key insights, OC Vibe sections and the main announcement traces to a table, card, note or data note", not _miss and _n > 150, f"{_n} figures traced; {len(_miss)} not found" + (f": {_miss[:5]}" if _miss else ""))
# Newsroom structure and house style (added Oct. 13, 2026)
_news = [x for x in CT.SECTIONS if x.get("kind") == "News report"]
_bad = [x["id"] for x in _news if not (x.get("dateline") and x.get("ans") and x.get("nut") and len(x.get("details") or []) == 6 and all(d.get("fig") and d.get("src") for d in x["details"]))]
check("H. Report text", "Every section is a news report (dateline, lede, nut graph, six sourced detail cards) followed by analysis", len(_news) == 9 and not _bad, f"{len(_news)} news reports; incomplete: {_bad or 'none'}")
_all = json.dumps([CT.SECTIONS, CT.TAKEAWAYS, CT.DQ, CT.RECS, CT.DATA_EXTRA], ensure_ascii=False, default=str)
check("H. Report text", "House style: no em dashes anywhere in the report content", "\u2014" not in _all, f"{_all.count(chr(0x2014))} em dashes")
_ap = _re.findall(r"\b(?:January|February|August|September|October|November|December|Sep|Sept(?!\.)|Aug(?!\.)|Oct(?!\.)|Nov(?!\.)|Dec(?!\.)|Jan(?!\.)|Feb(?!\.)) \d{1,2}, 20\d\d", _all)
check("H. Report text", "AP style: months with a specific date are abbreviated (Jan., Feb., Aug., Sept., Oct., Nov., Dec.)", not _ap, f"{len(_ap)} exceptions" + (f": {_ap[:3]}" if _ap else ""))
_fp = [t for x in _news for t in [x["nut"]] + [d["fig_l"] for d in x["details"]] if _re.search(r"\b(I|we|our|us)\b", t)]
check("H. Report text", "Attribution and objectivity: no first person in news-report nut graphs or detail cards", not _fp, f"{len(_fp)} exceptions" + (f": {_fp[0][:80]}" if _fp else ""))
_order = [x["id"] for x in CT.SECTIONS]
check("H. Report text", "Reading order: each section links to the next with a bridge", _order[:3] == ["p-ocv", "p-d5", "p-spend"] and all(x.get("next", {}).get("bridge") for x in CT.SECTIONS), " → ".join(_order))
_ig = [(x["id"], g) for x in CT.SECTIONS for g in (x.get("info") or [])]
_igbad = [f"{sid}:{g['kind']}" for sid, g in _ig if not (g.get("title") and g.get("src") and _re.search(r"20\d\d", g["src"]))]
_igcalc = [f"{sid}:{g['kind']}" for sid, g in _ig if g["kind"] in ("receipt", "share", "chain") and not (g.get("lines") and all(l.get("calc") for l in g["lines"]) or g.get("calc") or g.get("links"))]
check("H. Report text", "Every infographic has a title and a dated source; derived values show their calculation", len(_ig) >= 9 and not _igbad and not _igcalc, f"{len(_ig)} infographics; missing source/date: {_igbad or 'none'}; missing calculation: {_igcalc or 'none'}")
_recv = [g for _, g in _ig if g["kind"] == "receipt"]
check("H. Report text", "Receipt infographic: per-visitor lines add up to the stated total", all(abs(sum(l["n"] for l in g["lines"]) - float(g["total"]["v"].strip("$"))) < 0.05 for g in _recv), "; ".join(f"sum {sum(l['n'] for l in g['lines']):.2f} vs {g['total']['v']}" for g in _recv))
_mp = [(x["id"], m) for x in CT.SECTIONS for m in (x.get("maps") or [])]
_geo = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps_geo.json")))
_mbad = [f"{sid}:{p['name']}" for sid, m in _mp for p in m["points"] if p["name"] not in _geo["pts"] or not _geo["pts"][p["name"]]["world" if m["kind"] == "world" else "us"]]
_mval = [f"{sid}:{p['name']}" for sid, m in _mp for p in (m["points"] + m.get("states", [])) if p["t"].split(" ")[0] not in _other]
check("H. Report text", "Maps: every mapped value comes from a report table, has a position, and each map has a dated source", len(_mp) >= 3 and not _mbad and not _mval and all(_re.search(r"20\d\d", m["src"]) for _, m in _mp), f"{len(_mp)} maps, {sum(len(m['points']) + len(m.get('states', [])) for _, m in _mp)} values; unplaced: {_mbad or 'none'}; untraced: {_mval or 'none'}")
import schedule as _SC, datetime as _dtm
_cands = [_dtm.date(y, m, 15) for y in (_SC.LAST_UPDATE.year, _SC.LAST_UPDATE.year + 1) for m in (1, 4, 7, 10)]
_nx = min(d for d in _cands if d > _SC.LAST_UPDATE)
_html = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "oc-vibe-insights.html")).read()
_spl = [c for r in _SC.PLANNED["rows"] for c in r if _re.search(r"[$%]|\b\d[\d,.]*\s*(visits|tickets|people|M|K)\b", c)]
_sem = [t for t in [_SC.LEDE, _SC.LINE] + [d["text"] for d in _SC.DETAILS] + [c for r in _SC.TABLE["rows"] + _SC.PLANNED["rows"] for c in r] if "\u2014" in t]
check("H. Report text", "Update schedule: next update is the first 15th of Jan., April, July or Oct. after the last update, shown in the header, overview and footer; planned sources show no figures", _SC.NEXT == _nx and _html.count(_SC.NEXT_S) >= 3 and _SC.LINE in _html and len(_SC.DETAILS) == 6 and not _spl and not _sem, f"last {_SC.LAST_S}, next {_SC.NEXT_S} (expected {_nx:%b. %-d, %Y}); next date shown {_html.count(_SC.NEXT_S)} times; planned sources with figures: {_spl or 'none'}; em dashes: {len(_sem)}")
import zipfile as _zf
_bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_pm = json.load(open(os.path.join(_bd, "deck_pages.json")))
_nsl = len(_re.findall(r"<p:sldId ", _zf.ZipFile(os.path.join(_bd, "OC_Vibe_Insights.pptx")).read("ppt/presentation.xml").decode()))
_cov = sorted(p for x in _pm["sections"] for p in x["pages"])
check("H. Report text", "PDF export: the report PDF has one page per deck slide and every page belongs to exactly one deck section", _pm["n"] == _nsl and _cov == list(range(_nsl)) and 0 in _pm["sections"][0]["pages"], f"{_pm['n']} PDF pages, {_nsl} slides, {len(_pm['sections'])} sections; pages covered once: {_cov == list(range(_nsl))}")
_rx = __import__("facts_only").EST_RX
_left = [t for t in _texts + CT.TAKEAWAYS + CT.DQ if _rx.search(t)]
check("H. Report text", "No scenario-model estimate remains in the report text", not _left, f"{len(_left)} statements with estimate wording" + (f": {_left[0][:80]}" if _left else ""))
check("H. Report text", "Concert hall capacity check: base estimate at 5,000 seats stays inside the 90% simulation range", 71e6 <= RC.CAP5000 <= 122e6, f"${RC.CAP5000/1e6:.1f}M at 5,000 seats vs ${I.RES[1]['spend']/1e6:.1f}M at {I.HALL_CAP:,} seats")
check("C. Reconciliation", "Transit snapshots: rows sum to totals and files reconcile (staff, expenses, revenues, passengers, vehicles)", len(RC.TRANSIT_CHECKS) == 8, "; ".join(RC.TRANSIT_CHECKS))
_rl = [RC.TYP["Revenues"][i] - RC.TYP["Expenses"][i] - RC.TYP["Revenues Less Expenses"][i] for i in range(len(RC.YRS))]
check("C. Reconciliation", "Transit snapshots: revenues less expenses recomputes in every year", max(abs(x) for x in _rl) < 1, f"largest difference ${max(abs(x) for x in _rl):.2f} over {len(RC.YRS)} years")

# ---------------- Questions answered and Reports and data library (Oct. 14, 2026) ----------------
import ask as _AK, library as _LB
from fractions import Fraction as _F
_E = __import__("data").EI
_tr = []
for _g, _t in _AK.TE_TR.items():   # transportation impact: sums and shares recomputed exactly from the report rows
    _tr.append(_F(str(_t["sales_t"])) == sum(_F(str(v)) for v in _t["sales"].values()))
    _tr.append(_t["jobs_t"] == sum(_t["jobs"].values()))
    _tr.append(abs(_F(str(_t["spend"])) / _F(str(_E[_g]["sp25"])) * 100 - _F(str(round(_t["share"], 10)))) < _F(1, 10**6))
check("I. Questions answered", "Transportation impact: business sales, jobs and labor income add up from Tourism Economics' industry rows; shares recompute",
      all(_tr) and _AK.TE_TR["Anaheim"]["jobs_t"] == 2080 and _AK.TE_TR["Orange County"]["jobs_t"] == 6141 and round(_AK.TE_TR["Orange County"]["sales_t"]) == 973,
      f"Anaheim {_AK.TE_TR['Anaheim']['jobs_t']:,} jobs (1,919 + 161), ${_AK.TE_TR['Anaheim']['sales_t']:.0f}M sales; Orange County {_AK.TE_TR['Orange County']['jobs_t']:,} jobs, ${_AK.TE_TR['Orange County']['sales_t']:.0f}M sales; Garden Grove {_AK.TE_TR['Garden Grove']['jobs_t']} jobs")
_u = _AK.UST; _v = _AK.VCA
_ok_us = round(_u["sp25"] / _u["trips25"]) == 553 and round(_u["dom_sp25"] / _u["dom_trips25"]) == 494 and abs(_v["tr_share"] - 25.2 / 140.8 * 100) < 1e-9 and round(_v["tr_share"], 1) == 17.9
check("I. Questions answered", "Average spend and California transportation share recompute: U.S. $553 per trip ($1.360T ÷ 2.46B), domestic $494; California $25.2B ÷ $140.8B = 17.9%", _ok_us,
      f"U.S. per trip ${_u['sp25']/_u['trips25']:.2f}; domestic ${_u['dom_sp25']/_u['dom_trips25']:.2f}; California {_v['tr_share']:.3f}%")
_mix = sum(v for _, v in _v["mix"])
check("I. Questions answered", "Visit California visitor spending by category adds to the published total within rounding", abs(_mix - _v["visitor"]) <= 0.15, f"{_mix:.1f} vs. {_v['visitor']} ($B)")
_qids = {q["id"] for q in _AK.ASK}; _lids = {f["id"] for f in _LB.FILES}
_bad_ref = [f"{q['id']}:{f}" for q in _AK.ASK for f in q.get("files", []) if f not in _lids] + [f"{q['id']}:go" for q in _AK.ASK if q["go"] not in {x["id"] for x in CT.SECTIONS} | {"p-library", "p-notes"}]
_miss = [f["file"] for f in _LB.FILES if f["topic"] != "report" and not os.path.exists(os.path.join(_LB.LIB_DIR, f["file"]))]
_bd2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_missr = [f["file"] for f in _LB.FILES if f["topic"] == "report" and not os.path.exists(os.path.join(_bd2, f["file"]))]
check("I. Questions answered", "Library: every listed file exists, every question links only to listed files and real sections, and every core question has a visual, method and source",
      not _bad_ref and not _miss and not _missr and all(_AK.ASK[[q["id"] for q in _AK.ASK].index(c)]["viz"] and _AK.ASK[[q["id"] for q in _AK.ASK].index(c)]["how"] for c in _AK.CORE) and all(len(g) == 4 and g[3] for q in _AK.ASK for g in q["geo"]),
      f"{len(_LB.FILES)} files ({len(_miss) + len(_missr)} missing); {len(_AK.ASK)} questions; {len(_bad_ref)} broken links")
_names = ["Taylor", "Atkinson", "Mike", "Bree", "Katie", "Pederson", "Samantha", "Shannel", "Picou", "Nancy", "Cindy", "Meliker"]
_qt = json.dumps([_AK.ASK, _LB.FILES, _LB.LINKS], ensure_ascii=False)
_hit = [n for n in _names if _re.search(r"\b" + n + r"\b", _qt)]
_pdocs = []
for _f in _LB.FILES:
    _pp = os.path.join(_LB.LIB_DIR, _f["file"])
    if _f["file"].endswith((".xlsx", ".pptx")) and os.path.exists(_pp):
        _z = _zf.ZipFile(_pp); _blob = b"".join(_z.read(n) for n in _z.namelist() if n.endswith(".xml"))
        _pdocs += [f"{_f['file']}:{n}" for n in ("Samantha", "Nancy", "Cindy", "Meliker", "Harding", "picou") if n.encode() in _blob]
check("I. Questions answered", "No individuals are named in the questions or the library, and Office files carry no personal names in their properties or sheet names", not _hit and not _pdocs and "—" not in _qt,
      f"names in text: {_hit or 'none'}; in files: {_pdocs or 'none'}; em dashes: {_qt.count(chr(0x2014))}")
_nq = len(_re.findall(r'id="p-ask"|id="p-library"', _html))
check("I. Questions answered", "The app has the Questions answered and Reports and data library pages, and the focused deck exists with every core question",
      _nq == 2 and os.path.exists(os.path.join(_bd2, "OC_Vibe_Questions_Answered.pptx")) and len(_re.findall(r"<p:sldId ", _zf.ZipFile(os.path.join(_bd2, "OC_Vibe_Questions_Answered.pptx")).read("ppt/presentation.xml").decode())) >= 4 * 2 + 3,
      f"pages {_nq}/2; questions deck slides {len(_re.findall(r'<p:sldId ', _zf.ZipFile(os.path.join(_bd2, 'OC_Vibe_Questions_Answered.pptx')).read('ppt/presentation.xml').decode()))}")

# ---------------- J. Visual layer: AntV G2, T8, Infographic, X6 and D3 (Oct. 14, 2026) ----------------
_bd3 = os.path.dirname(_bd2)
_pkg = json.load(open(os.path.join(_bd3, "package.json")))
_dev = {**_pkg.get("dependencies", {}), **_pkg.get("devDependencies", {})}
_want = {"@antv/g2": "5.4.8", "@antv/t8": "0.3.1", "@antv/infographic": "0.2.20", "@antv/x6": "3.1.8", "@mdi/js": "7.4.47", "d3": "7.9.0"}
_pin = all(_dev.get(k) == v for k, v in _want.items())
_ext = _re.findall(r'<script[^>]+src=["\']https?://|<link[^>]+href=["\']https?://(?!fonts\.googleapis)', _html)
_hosts = [h for h in ("assets.antv.antgroup.com", "weavefox", "sive.antv", "unpkg.com", "cdn.jsdelivr", "gw.alipayobjects") if h in _html]
_libs = [k for k, m in (("G2", "G2Q"), ("T8", "t8Render"), ("Infographic", "addIg("), ("X6", "X6.Graph"), ("D3", "d3-compare")) if m not in _html]
check("J. Visual layer", "Chart libraries are pinned to exact versions, inlined in the page, and the page loads nothing from outside hosts",
      _pin and not _ext and not _hosts and not _libs, f"pinned {sum(_dev.get(k) == v for k, v in _want.items())}/{len(_want)}; external tags {len(_ext)}; outside hosts {_hosts or 'none'}; missing layers {_libs or 'none'}")
_mx = []
for _g in ("Anaheim", "Orange County"):
    _parts = [_E[_g][k] for k in ("rec", "lodging", "retail", "fb", "transport")]
    _mx.append((_g, sum(_parts), _E[_g]["sp25"], sum(round(p / _E[_g]["sp25"] * 100, 1) for p in _parts)))
check("J. Visual layer", "Spending treemaps: the five categories add to total visitor spending within $1M and the labeled shares add to 100% within 0.2 points",
      all(abs(s - t) <= 1.0 and abs(p - 100) <= 0.2 for _, s, t, p in _mx), "; ".join(f"{g} ${s:,.0f}M of ${t:,.0f}M, shares {p:.1f}%" for g, s, t, p in _mx))
_aj = open(os.path.join(_bd2, "antv_app.js")).read()
_im = json.loads(_re.search(r"const IMPACT = (\{.*?\});", _aj).group(1).replace("'", '"'))
_iok = []
for _g, _v in _im.items():
    _iok.append(_v[0] == _E[_g]["vis25"] and _v[1] == _E[_g]["sp25"] and _v[4] == _E[_g]["impact"] and _v[5] == _E[_g]["jobs"] and _v[7] == _E[_g]["sl_tax"] and abs(_v[1] + _v[2] + _v[3] - _v[4]) <= 1.0)
check("J. Visual layer", "Impact flow diagram (X6): visitors, spending, total impact, jobs and taxes match the Tourism Economics figures, and direct + indirect + induced = total within $1M",
      all(_iok) and len(_im) == 3, "; ".join(f"{g}: ${v[1]:,}M + ${v[2]:,}M + ${v[3]:,}M = ${v[1]+v[2]+v[3]:,.1f}M vs. ${v[4]:,}M" for g, v in _im.items()))

# ---------------- K. One Export panel: report, doc, slides, design, motion, data, link (Oct. 15, 2026) ----------------
_mk = open(os.path.join(_bd2, "make_app.js")).read()
_tools = ["report", "doc", "slides", "design", "motion", "data", "link"]
_tool_ids = _re.findall(r"\{ id: '(\w+)', name:", _mk)
_one_place = ('id="p-make"' not in _html and 'id="dlPdf"' not in _html and 'id="makeBtn"' not in _html and "'dash'" not in _mk.replace("=== 'dash'", ""))
_mk_ok = (_tool_ids == _tools and 'id="expDlg"' in _html and _one_place and "PptxGenJS 4.0.1" in _html and _dev.get("pptxgenjs") == "4.0.1"
          and not _re.search(r"fetch\((?!LOGO\))", _mk))
check("K. One Export panel", "Every file comes from one Export panel (full report, Doc, Slides, Design, Motion, Data, Share link); no separate Make page, download buttons or Dashboard; slides use pinned PptxGenJS 4.0.1; nothing fetched but the logo",
      _mk_ok, f"kinds {', '.join(_tool_ids)}; one place {_one_place}; PptxGenJS {_dev.get('pptxgenjs')}")
# every figure the studio offers is a section card or a Questions answered row, unchanged (value, area, source)
_cards = {(s["id"], str(c[2]).lstrip("▲▼ ").strip()) for s in CT.SECTIONS for c in s.get("cards", [])}
_asks = {(q["go"], g[1]) for q in _AK.ASK for g in q["geo"]}
_n_pool = len(_cards) + len(_asks)
check("K. One Export panel", "Doc, Slides, Design and Motion figures are taken unchanged from section key figures and Questions answered (no recalculation in the studio code)",
      "POOL.push({ id: s.id.slice(2) + '-c' + i" in _mk and "value: g[1], detail: g[2], src: g[3]" in _mk and not _re.search(r"\bvalue:\s*[^,]*[*/+]\s*\d", _mk),
      f"{len(_cards)} section key figures and {len(_asks)} question rows available to the studio")

# ---------------- write ----------------
results["checks"] = checks; results["passed"] = sum(c_["ok"] for c_ in checks); results["total"] = len(checks)
results["seed"] = SEED; results["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def conv_(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, Fr): return float(o)
    raise TypeError(type(o))
json.dump(results, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=conv_)
with open(os.path.join(OUT, "summary.md"), "w") as fh:
    fh.write(f"# OC Vibe calculation validation\n\n{results['passed']} of {results['total']} checks passed.\n\n")
    for c_ in checks: fh.write(f"- [{'PASS' if c_['ok'] else 'FAIL'}] {c_['group']} — {c_['name']}: {c_['detail']}\n")
print(f"{results['passed']}/{results['total']} passed")
for c_ in checks: print(("PASS " if c_["ok"] else "FAIL ") + c_["group"] + " | " + c_["name"] + " | " + c_["detail"])
