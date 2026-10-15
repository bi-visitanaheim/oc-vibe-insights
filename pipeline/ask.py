"""Questions answered and the Reports and data library (Oct. 14, 2026).

General questions anyone may ask about Anaheim's visitor economy and the OC Vibe area, each answered for Anaheim,
Orange County and the U.S. (California where that is the closest published level), with a short answer, a visual,
the method, sources with dates, and links to the files in the library. Facts only: every value is published by the
named source or is arithmetic on published values (shown). No individuals are named.
Attached last in content.py (after maps).
"""
from data import EI, N, TET_GAS, TET_AIR, TET_AUTO, D5, GEO, DATAFY, MED, TRANSIT, BTS, CS_SUB, CS_OC, CS_ECON, LARC_Q, LARC, Q, INTL, ANA_VIS, ANA_SP, YEARS
import library as L

A, G, O = EI["Anaheim"], EI["Garden Grove"], EI["Orange County"]

# ---------- Tourism Economics 2025: transportation industries (Business sales, jobs, labor income by industry tables) ----------
TE_TR = {
    "Anaheim":       dict(spend=224.0, sales=dict(other=159.0, gas=139.0, air=0.0), jobs=dict(other=1919, gas=161, air=0), inc=dict(other=38.0, gas=7.0, air=0.0)),
    "Garden Grove":  dict(spend=46.9, sales=dict(other=22.0, gas=29.8, air=0.0), jobs=dict(other=289, gas=37, air=0), inc=dict(other=5.3, gas=1.7, air=0.0)),
    "Orange County": dict(spend=707.0, sales=dict(other=496.0, gas=349.0, air=128.0), jobs=dict(other=5593, gas=361, air=187), inc=dict(other=112.0, gas=16.0, air=15.0)),
}
for g, t in TE_TR.items():
    t["share"] = t["spend"] / EI[g]["sp25"] * 100
    t["sales_t"] = sum(t["sales"].values()); t["jobs_t"] = sum(t["jobs"].values()); t["inc_t"] = sum(t["inc"].values())
    t["jobs_pct"] = t["jobs_t"] / EI[g]["jobs"] * 100

# ---------- Visit California (Dean Runyan Associates), The Economic Impact of Travel in California, 2025p (Apr. 6, 2026) ----------
VCA = dict(total=158.9, total24=156.2, visitor=140.8, other=18.1, jobs=1167470, earn=66.7, local_tax=7.2, state_tax=6.5, tax=13.6,
           mix=[("Accommodations", 35.2), ("Food service", 38.5), ("Food stores", 5.9), ("Arts, entertainment and recreation", 18.5),
                ("Retail", 17.4), ("Local transportation and gas", 18.7), ("Visitor air", 6.5)],
           jobs_ind=[("Accommodation and food service", 645.3), ("Arts, entertainment and recreation", 308.9), ("Retail, including gasoline", 85.5),
                     ("Ground transportation", 46.9), ("Visitor air", 26.2), ("Other travel", 54.7)],
           oc=dict(visitor=15394.2, other=1716.0, total=17.1, total24=16.7, jobs=134540, earn=6929.9, tax=1408.8))
VCA["tr"] = 18.7 + 6.5
VCA["tr_share"] = VCA["tr"] / VCA["visitor"] * 100
VCA["tr_jobs"] = (46.9 + 26.2) * 1000
VCA["chg"] = (VCA["total"] / VCA["total24"] - 1) * 100
S_VCA = "Visit California, The Economic Impact of Travel in California, 2025p (Dean Runyan Associates, Apr. 6, 2026)"

# ---------- U.S. Travel Association and Tourism Economics, Travel Forecast, Spring 2026 (real 2025 dollars) ----------
UST = dict(sp24=1.341e12, sp25=1.360e12, sp26=1.374e12, trips24=2.43e9, trips25=2.46e9, trips26=2.51e9, dom_sp25=1.185e12, dom_trips25=2.40e9,
           intl_arr25=68.3e6, jobs="15M+", output=3.0, sl_tax=92.0)
UST["per_trip"] = UST["sp25"] / UST["trips25"]
UST["dom_per_trip"] = UST["dom_sp25"] / UST["dom_trips25"]
UST["chg"] = (UST["sp25"] / UST["sp24"] - 1) * 100
UST["trips_chg26"] = (UST["trips26"] / UST["trips25"] - 1) * 100
S_UST = "U.S. Travel Association and Tourism Economics, Travel Forecast, Spring 2026 (real 2025 dollars)"
S_USE = "U.S. Travel Association, Economic Impact of the U.S. Travel Industry (2025 data; pub. 2026)"
S_TE = "Tourism Economics, Economic Impact of Visitors 2025 (pub. Apr.–May 2026)"
S_TEFC = "Tourism Economics, Anaheim and Garden Grove Travel Forecast (Sept. 2026)"

def m(v): return f"${v:,.0f}M" if v < 1000 else f"${v/1000:.2f}B"
def pc(v, nd=1): return f"{v:.{nd}f}%"

ASK = []
def q(**k): ASK.append(k)

# ===== Visitor spending =====
q(id="avg-spend", topic="Visitor spending", q="What does the average visitor spend?",
  a=f"Each Anaheim visitor spent about ${A['pv25']:.0f} in 2025. Countywide, the average was ${O['pv_pub'][0]} per visitor, and across the U.S. travel spending came to about ${UST['per_trip']:.0f} per trip.",
  key=f"${A['pv25']:.0f}", key_l="per Anaheim visitor, 2025",
  geo=[["Anaheim", f"${A['pv25']:.0f}", f"${A['sp25']/1000:.3f}B ÷ {A['vis25']}M visitors (2025)", S_TE],
       ["Garden Grove", f"${G['pv25']:.0f}", f"${G['sp25']:.1f}M ÷ {G['vis25']}M visitors (2025)", S_TE],
       ["Orange County", f"${O['pv_pub'][0]}", "Published by Tourism Economics; day visitors $58, overnight $737 (2025)", S_TE],
       ["U.S.", f"${UST['per_trip']:.0f} per trip", f"$1.360T ÷ 2.46B trips (2025, real 2025 dollars); domestic ${UST['dom_per_trip']:.0f}", S_UST]],
  viz=dict(kind="bars", title="Spending per visitor or trip, 2025", fmt='"$"#,##0', rows=[
      dict(l="Garden Grove", v=round(G['pv25']), t=f"${G['pv25']:.0f}"), dict(l="Anaheim", v=round(A['pv25']), t=f"${A['pv25']:.0f}", hi=True),
      dict(l="Orange County", v=O['pv_pub'][0], t=f"${O['pv_pub'][0]}"), dict(l="U.S. (per trip)", v=round(UST['per_trip']), t=f"${UST['per_trip']:.0f}")]),
  how="Spending per visitor = visitor spending ÷ visitors. Tourism Economics counts a visitor as anyone who stays overnight or travels more than 50 miles. The U.S. figure is per trip (domestic and international), in 2025 dollars.",
  caveat=f"Day trips pull averages down: 67.5% of Anaheim visitors are day visitors vs. 57.0% countywide, and Orange County overnight visitors spend $737 each vs. $58 for day visitors. Compare direction, not exact levels, across sources.",
  files=["te-ei-ana", "te-ei-gg", "te-ei-oc", "te-fc-sep"], go="p-spend", links=[1])

q(id="spend-growth", topic="Visitor spending", q="Is visitor spending growing?",
  a=f"Yes. Anaheim visitor spending rose {A['sp_chg']:.1f}% in 2025 and {Q['q2_sp_chg']}% in Q2 2026. Orange County grew {O['sp_chg']:.1f}%, California {VCA['chg']:.1f}% and the U.S. {UST['chg']:.1f}% after inflation.",
  key=f"+{Q['q2_sp_chg']}%", key_l="Anaheim visitor spending, Q2 2026 vs. Q2 2025",
  geo=[["Anaheim", f"+{A['sp_chg']:.1f}%", f"${A['sp24']/1000:.3f}B to ${A['sp25']/1000:.3f}B (2024 to 2025); Q2 2026 +{Q['q2_sp_chg']}%", S_TE + "; " + S_TEFC],
       ["Orange County", f"+{O['sp_chg']:.1f}%", f"${O['sp24']/1000:.2f}B to ${O['sp25']/1000:.2f}B (2024 to 2025)", S_TE],
       ["California", f"+{VCA['chg']:.1f}%", f"${VCA['total24']}B to ${VCA['total']}B direct travel spending (2024 to 2025)", S_VCA],
       ["U.S.", f"+{UST['chg']:.1f}%", "$1.341T to $1.360T (2024 to 2025, real 2025 dollars)", S_UST]],
  viz=dict(kind="bars", title="Growth in visitor or travel spending, 2025 vs. 2024", unit="%", rows=[
      dict(l="Anaheim", v=round(A['sp_chg'], 1), t=f"+{A['sp_chg']:.1f}%", hi=True), dict(l="Orange County", v=round(O['sp_chg'], 1), t=f"+{O['sp_chg']:.1f}%"),
      dict(l="California", v=round(VCA['chg'], 1), t=f"+{VCA['chg']:.1f}%"), dict(l="U.S. (after inflation)", v=round(UST['chg'], 1), t=f"+{UST['chg']:.1f}%")]),
  how="Growth = this year ÷ last year − 1. Anaheim, Orange County and California are in current dollars; the U.S. series is adjusted for inflation, so it reads lower.",
  caveat="Tourism Economics forecasts Anaheim visitor spending of $7.2B in 2026 (+5.6%).", files=["te-ei-ana", "te-ei-oc", "te-fc-sep"], go="p-spend", links=[0, 1])

q(id="q2-report", topic="Visitor spending", q="What did the latest quarterly Tourism Economics report (Q2 2026) show?",
  a=f"Anaheim welcomed {Q['q2_vis']}M visitors in Q2 2026 (+{Q['q2_vis_chg']}%), who spent ${Q['q2_sp']}B (+{Q['q2_sp_chg']}%). Overnight visits rose 4.5% and day visits 2.1%; hotel rates were nearly 9% higher. Garden Grove: 831,000 visitors (+3.4%), $200.4M (+7.1%).",
  key=f"${Q['q2_sp']}B", key_l="Anaheim visitor spending, Q2 2026 (+7.8%)",
  geo=[["Anaheim, Q2 2026", f"{Q['q2_vis']}M visitors · ${Q['q2_sp']}B", f"+{Q['q2_vis_chg']}% visitors · +{Q['q2_sp_chg']}% spending; first half 13.1M visitors, $3.5B", S_TEFC],
       ["Garden Grove, Q2 2026", "831,000 visitors · $200.4M", "+3.4% visitors · +7.1% spending", S_TEFC],
       ["Anaheim and Garden Grove, international", "2.16M visitors in 2026 (forecast)", "+1.0%; spending $2.79B (+1.8%); Mexico +6.9%", S_TEFC],
       ["U.S. outlook", "Steady, with risks", "Tourism Economics expects a prolonged Federal Reserve pause; risks include an equity correction and layoffs", S_TEFC]],
  viz=dict(kind="bars", title="Anaheim visitor spending by quarter ($B)", fmt='"$"0.00"B"', rows=[
      dict(l="Q1 2025", v=1.61, t="$1.61B"), dict(l="Q2 2025", v=1.63, t="$1.63B"), dict(l="Q3 2025", v=1.71, t="$1.71B"),
      dict(l="Q4 2025", v=1.87, t="$1.87B"), dict(l="Q1 2026", v=1.72, t="$1.72B"), dict(l="Q2 2026", v=1.76, t="$1.76B", hi=True)]),
  how="Quarterly visits and spending are Tourism Economics measurements in its Travel Forecast. Change is vs. the same quarter a year earlier.",
  caveat="The quarterly results are in the Travel Forecast (Sept. 2026). The annual Economic Impact reports cover calendar 2025; both are in the library.",
  files=["te-fc-sep", "te-fc-jun"], go="p-spend")

q(id="spend-mix", topic="Visitor spending", q="Where do visitor dollars go?",
  a=f"In Anaheim, recreation takes the largest share (34.0%), then lodging (25.2%), retail (21.9%), food and beverage (15.6%) and transportation (3.3%). Countywide, food and beverage leads (27.6%). Statewide, food service and lodging lead.",
  key="34.0%", key_l="of Anaheim visitor spending goes to recreation",
  geo=[["Anaheim", "Recreation 34.0%", "Lodging 25.2% · retail 21.9% · F&B 15.6% · transportation 3.3% ($6.83B, 2025)", S_TE],
       ["Orange County", "F&B 27.6%", "Lodging 25.9% · recreation 22.0% · retail 20.5% · transportation 3.9% ($17.99B, 2025)", S_TE],
       ["California", "Food service 27.3%", "Accommodations 25.0% · local transportation and gas 13.3% · arts and recreation 13.1% · retail 12.4% · visitor air 4.6% · food stores 4.2% ($140.8B, 2025)", S_VCA]],
  viz=dict(kind="stack", title="Share of visitor spending by category, 2025", rows=[
      dict(l="Anaheim", parts=[["Recreation", 34.0], ["Lodging", 25.2], ["Retail", 21.9], ["Food and beverage", 15.6], ["Transportation", 3.3]]),
      dict(l="Orange County", parts=[["Food and beverage", 27.6], ["Lodging", 25.9], ["Recreation", 22.0], ["Retail", 20.5], ["Transportation", 3.9]]),
      dict(l="California", parts=[["Food and beverage", round((38.5 + 5.9) / 140.8 * 100, 1)], ["Lodging", round(35.2 / 140.8 * 100, 1)], ["Recreation", round(18.5 / 140.8 * 100, 1)], ["Retail", round(17.4 / 140.8 * 100, 1)], ["Transportation", round(25.2 / 140.8 * 100, 1)]])]),
  how="Share = category spending ÷ total visitor spending. California food and beverage combines food service ($38.5B) and food stores ($5.9B); transportation combines local transportation and gas ($18.7B) and visitor air ($6.5B).",
  caveat="Category definitions differ by source: Tourism Economics' city and county figures count spending inside the area and include little air travel; Visit California includes visitor air fares.",
  files=["te-ei-ana", "te-ei-oc"], go="p-impact", links=[0])

# ===== Jobs and economy =====
q(id="jobs", topic="Jobs and economy", q="How many jobs does the visitor economy support?",
  a=f"Visitors supported {A['jobs']:,} Anaheim jobs in 2025, about one in three. Countywide the total was {O['jobs']:,} (one in 14), statewide 1.17 million direct travel jobs, and nationally more than 15 million.",
  key=f"{A['jobs']:,}", key_l="Anaheim jobs supported by visitors, 2025",
  geo=[["Anaheim", f"{A['jobs']:,}", f"{A['jobs_share']}% of all jobs; 47,925 direct + 19,892 indirect and induced", S_TE],
       ["Garden Grove", f"{G['jobs']:,}", f"{G['jobs_share']}% of all jobs", S_TE],
       ["Orange County", f"{O['jobs']:,}", f"{O['jobs_share']}% of all jobs; 125,511 direct", S_TE],
       ["California", f"{VCA['jobs']:,}", "Direct travel-generated jobs only (2025p)", S_VCA],
       ["U.S.", "15M+", "Jobs supported by travel (2025)", S_USE]],
  viz=dict(kind="bars", title="Share of all jobs supported by visitors, 2025", unit="%", rows=[
      dict(l="Anaheim", v=A['jobs_share'], t=f"{A['jobs_share']}%", hi=True), dict(l="Garden Grove", v=G['jobs_share'], t=f"{G['jobs_share']}%"),
      dict(l="Orange County", v=O['jobs_share'], t=f"{O['jobs_share']}%")]),
  how="Tourism Economics' totals add direct jobs (in businesses visitors buy from) to indirect (suppliers) and induced (workers' spending) jobs. Visit California's 1.17 million counts direct jobs only.",
  caveat="Jobs are full- and part-time, including proprietors, so they are not full-time equivalents.", files=["te-ei-ana", "te-ei-gg", "te-ei-oc", "te-ei-one"], go="p-impact", links=[0, 2])

q(id="fb-jobs", topic="Jobs and economy", q="What share of visitor-supported jobs are in food and beverage?",
  a=f"{A['fb_job_share']:.1f}% in Anaheim ({A['fb_jobs']:,} of {A['jobs']:,}), {G['fb_job_share']:.1f}% in Garden Grove and {O['fb_job_share']:.1f}% countywide. Statewide, accommodation and food service together hold 55.3% of direct travel jobs.",
  key=f"{O['fb_job_share']:.1f}%", key_l="of Orange County visitor-supported jobs are in food and beverage",
  geo=[["Anaheim", f"{A['fb_job_share']:.1f}%", f"{A['fb_jobs']:,} ÷ {A['jobs']:,} jobs", S_TE],
       ["Garden Grove", f"{G['fb_job_share']:.1f}%", f"{G['fb_jobs']:,} ÷ {G['jobs']:,} jobs", S_TE],
       ["Orange County", f"{O['fb_job_share']:.1f}%", f"{O['fb_jobs']:,} ÷ {O['jobs']:,} jobs", S_TE],
       ["California", "55.3%", "Accommodation and food service, 645,300 ÷ 1,167,500 direct jobs (combined category)", S_VCA]],
  viz=dict(kind="bars", title="Food and beverage share of visitor-supported jobs, 2025", unit="%", rows=[
      dict(l="Anaheim", v=round(A['fb_job_share'], 1), t=f"{A['fb_job_share']:.1f}%", hi=True), dict(l="Orange County", v=round(O['fb_job_share'], 1), t=f"{O['fb_job_share']:.1f}%"),
      dict(l="Garden Grove", v=round(G['fb_job_share'], 1), t=f"{G['fb_job_share']:.1f}%")]),
  how="Share = food and beverage jobs (direct, indirect and induced) ÷ all visitor-supported jobs, from each Tourism Economics regional report.",
  caveat="In Anaheim, recreation and entertainment holds the most visitor-supported jobs (28,970). California's figure combines lodging with food service.",
  files=["te-ei-ana", "te-ei-gg", "te-ei-oc"], go="p-impact", links=[0])

q(id="impact", topic="Jobs and economy", q="What is the total economic impact of visitors?",
  a=f"$10.4B in Anaheim in 2025 (visitor spending ${A['sp25']/1000:.2f}B plus $3.6B in supplier and worker spending), $1.1B in Garden Grove and $30.7B countywide. Nationally, travel generated $3.0 trillion in output.",
  key=f"${A['impact']/1000:.1f}B", key_l="Anaheim total economic impact, 2025",
  geo=[["Anaheim", f"${A['impact']/1000:.2f}B", "$6.832B direct + $1.460B indirect + $2.130B induced", S_TE],
       ["Garden Grove", f"${G['impact']/1000:.2f}B", "$769.3M + $127.7M + $191.1M", S_TE],
       ["Orange County", f"${O['impact']/1000:.2f}B", "$17.993B + $6.253B + $6.426B", S_TE],
       ["U.S.", "$3.0T", "Economic output supported by travel (2025)", S_USE]],
  viz=dict(kind="bars", title="Total economic impact of visitors, 2025 ($B)", fmt='"$"0.0"B"', rows=[
      dict(l="Garden Grove", v=round(G['impact'] / 1000, 2), t=f"${G['impact']/1000:.1f}B"), dict(l="Anaheim", v=round(A['impact'] / 1000, 2), t=f"${A['impact']/1000:.1f}B", hi=True),
      dict(l="Orange County", v=round(O['impact'] / 1000, 2), t=f"${O['impact']/1000:.1f}B")]),
  how="Total impact = direct visitor spending + indirect (supply chain) + induced (spending of income earned), from Tourism Economics' input-output model.",
  caveat="Each region is modeled on its own, so city totals are not additive with the county total.", files=["te-ei-ana", "te-ei-gg", "te-ei-oc", "te-ei-one"], go="p-impact", links=[2])

q(id="taxes", topic="Jobs and economy", q="How much tax revenue do visitors generate?",
  a=f"Visitors generated ${A['sl_tax']/1000:.2f}B in state and local taxes in Anaheim in 2025, ${O['sl_tax']/1000:.2f}B countywide, $13.6B statewide and $92B nationally.",
  key=f"${A['sl_tax']:,.0f}M", key_l="Anaheim state and local taxes from visitors, 2025",
  geo=[["Anaheim", f"${A['sl_tax']:,.0f}M", "Includes $351M sales, $218M property and $234M lodging taxes", S_TE],
       ["Garden Grove", f"${G['sl_tax']}M", "Includes $30.1M lodging taxes", S_TE],
       ["Orange County", f"${O['sl_tax']/1000:.2f}B", "Includes $557M lodging taxes; $2,857 per household", S_TE],
       ["California", "$13.6B", "Local $7.2B + state $6.5B (2025p)", S_VCA],
       ["U.S.", "$92B", "State and local taxes (2025)", S_USE]],
  viz=dict(kind="bars", title="State and local taxes from visitors, 2025 ($M)", fmt='"$"#,##0.0"M"', rows=[
      dict(l="Garden Grove", v=G['sl_tax'], t=f"${G['sl_tax']}M"), dict(l="Anaheim", v=A['sl_tax'], t=f"${A['sl_tax']:,.0f}M", hi=True),
      dict(l="Orange County", v=O['sl_tax'], t=f"${O['sl_tax']:,.0f}M")]),
  how="Tourism Economics estimates taxes generated by visitor spending and the activity it supports; components are listed in each one-pager.",
  caveat="Statewide local and state taxes add to $13.7B because of rounding; the report states $13.6B.", files=["te-ei-one", "te-ei-ana", "te-ei-oc"], go="p-impact", links=[0, 2])

# ===== One more night =====
q(id="night-value", topic="One more night", q="What is one more night per visitor worth?",
  a=f"If every Anaheim visitor stayed one more night, lodging spending would rise about ${N['lodge_night']/1e6:.0f}M. Counting all spending, one more day for overnight visitors is worth about ${N['overnight_only']/1e9:.2f}B, and one more day for every visitor about ${N['per_day']/1e9:.2f}B (the study's upper bound).",
  key=f"${N['lodge_night']/1e6:.0f}M", key_l="one more night of Anaheim lodging spending",
  geo=[["Anaheim, lodging (headline)", f"${N['lodge_night']/1e6:.0f}M", "$1.724B lodging spending ÷ 2.17-day weighted average stay", "Visit Anaheim Extra Night study; " + S_TE],
       ["Anaheim, overnight visitors", f"${N['overnight_only']/1e9:.2f}B", "8.6M overnight visitors × $118.71 per visitor-day", "Visit Anaheim BI calculation"],
       ["Anaheim, every visitor (upper bound)", f"${N['per_day']/1e9:.2f}B", "$6.832B ÷ 2.17 days; total with the extra day $9.98B", "Visit Anaheim Extra Night study"],
       ["Orange County", "$737 vs. $58", "Spending per overnight visitor vs. per day visitor (2025), 12.7 times as much", S_TE]],
  viz=dict(kind="bars", title="One more night or day in Anaheim, three ways ($M)", fmt='"$"#,##0"M"', rows=[
      dict(l="Lodging only", v=round(N['lodge_night'] / 1e6), t=f"${N['lodge_night']/1e6:.0f}M", hi=True),
      dict(l="Overnight visitors, all spending", v=round(N['overnight_only'] / 1e6), t=f"${N['overnight_only']/1e9:.2f}B"),
      dict(l="Every visitor, all spending", v=round(N['per_day'] / 1e6), t=f"${N['per_day']/1e9:.2f}B")]),
  how="Weighted average stay = 93.2% domestic × 1.9 days + 6.8% international × 5.9 days = 2.17 days (Azira stays; Tourism Economics visitor mix). Spending per day = 2025 spending ÷ 2.17. Spending per visitor-day = $6.832B ÷ (26.5M × 2.17) = $118.71.",
  caveat="These are scenarios that hold spending per day constant; they are not forecasts. The study deck shows $9.9B for the total; the calculation gives $9.98B. A countywide version needs Orange County length of stay, which can be pulled from Azira at the next update.",
  files=["va-night", "va-night-wb", "te-ei-ana", "te-ei-oc"], go="p-night")

q(id="night-1pct", topic="One more night", q="What is each 1% of visitors staying a day longer worth?",
  a=f"About $31.5M in Anaheim visitor spending: 26.5M visitors × 1% × ${N['per_visitor_day']:.2f} per visitor-day. On the hotel side, each point of Sunday–Monday occupancy is about 22,200 room nights and $5.1M a year.",
  key="$31.5M", key_l="per 1% of Anaheim visitors adding a day",
  geo=[["Anaheim, visitor spending", "$31.5M", f"26.5M × 1% × ${N['per_visitor_day']:.2f}", "Visit Anaheim BI calculation; " + S_TE],
       ["Anaheim hotels, Sunday–Monday", "22,200 room nights · $5.1M", "21,318 rooms × 1% × 104 nights × $230 average rate", "STR daily data (Jan. 1–Oct. 3, 2026)"],
       ["Anaheim hotels, the gap", "15.7 points", "Sunday–Monday 70.6% vs. Friday–Saturday 86.2% occupancy", "STR daily data (Jan. 1–Oct. 3, 2026)"]],
  viz=dict(kind="bars", title="Anaheim+ hotel occupancy by night, 2026 (%)", unit="%", rows=[
      dict(l="Sunday", v=70.6, t="70.6%", hi=True), dict(l="Monday", v=70.5, t="70.5%", hi=True), dict(l="Tuesday", v=74.3, t="74.3%"),
      dict(l="Wednesday", v=76.8, t="76.8%"), dict(l="Thursday", v=80.2, t="80.2%"), dict(l="Friday", v=85.7, t="85.7%"), dict(l="Saturday", v=86.8, t="86.8%")]),
  how="Value per 1% = visitors × 1% × spending per visitor-day. Value per occupancy point = rooms × 1% × Sunday and Monday nights in a year (104) × average Sunday–Monday rate.",
  caveat="Arithmetic on 2025 and 2026 source data; it is not a forecast of what OC Vibe will add.", files=["va-night", "str-daily", "te-ei-ana"], go="p-night")

# ===== Transportation =====
ta, tg, to = TE_TR["Anaheim"], TE_TR["Garden Grove"], TE_TR["Orange County"]
q(id="transport-impact", topic="Transportation", q="What is the economic impact of visitor transportation?",
  a=f"Visitors spent ${ta['spend']:.0f}M on transportation in Anaheim in 2025 ({ta['share']:.1f}% of spending), supporting {ta['jobs_t']:,} jobs in transportation and gas stations. Countywide: ${to['spend']:.0f}M and {to['jobs_t']:,} jobs. Statewide, visitors spent ${VCA['tr']:.1f}B on local transportation, gas and air ({VCA['tr_share']:.1f}% of visitor spending).",
  key=f"{ta['jobs_t']:,}", key_l="Anaheim transportation and gas station jobs supported by visitors, 2025",
  geo=[["Anaheim", f"${ta['spend']:.0f}M · {ta['jobs_t']:,} jobs", f"{ta['share']:.1f}% of spending; business sales ${ta['sales_t']:.0f}M (other transport $159M + gas stations $139M); labor income ${ta['inc_t']:.0f}M", S_TE],
       ["Garden Grove", f"${tg['spend']:.1f}M · {tg['jobs_t']:,} jobs", f"{tg['share']:.1f}% of spending; business sales ${tg['sales_t']:.1f}M; labor income ${tg['inc_t']:.1f}M", S_TE],
       ["Orange County", f"${to['spend']:.0f}M · {to['jobs_t']:,} jobs", f"{to['share']:.1f}% of spending; business sales ${to['sales_t']:.0f}M (other transport $496M + gas $349M + air $128M); labor income ${to['inc_t']:.0f}M", S_TE],
       ["California", f"${VCA['tr']:.1f}B · {VCA['tr_jobs']:,.0f} jobs", f"Local transportation and gas $18.7B + visitor air $6.5B; direct jobs: ground 46,900 + air 26,200 (2025p)", S_VCA],
       ["U.S. costs", f"${TET_GAS[2025][0]:.2f} vs. ${TET_GAS[2025][1]:.2f}", f"Gasoline per gallon, U.S. vs. West Coast (2025); average domestic airfare ${TET_AIR[2025]:.0f}", "U.S. Bureau of Transportation Statistics, Transportation Economic Trends"]],
  viz=dict(kind="bars", title="Visitor transportation spending, share of all visitor spending, 2025 (%)", unit="%", rows=[
      dict(l="Anaheim", v=round(ta['share'], 1), t=f"{ta['share']:.1f}%", hi=True), dict(l="Orange County", v=round(to['share'], 1), t=f"{to['share']:.1f}%"),
      dict(l="Garden Grove", v=round(tg['share'], 1), t=f"{tg['share']:.1f}%"), dict(l="California", v=round(VCA['tr_share'], 1), t=f"{VCA['tr_share']:.1f}%")]),
  how="Tourism Economics transportation = ride share, taxis, trains, rental cars, buses and gasoline bought locally, plus the local share of air travel where an airport exists. Jobs and sales add the 'other transport', 'gas stations' and 'air transport' rows (direct, indirect and induced) of each report's industry tables.",
  caveat="Shares differ because Visit California counts visitor air fares and statewide ground travel, while Anaheim (no commercial airport) counts spending inside the city. A dedicated Tourism Economics transportation impact analysis has been requested and will be added at the next quarterly update after it arrives.",
  files=["te-ei-ana", "te-ei-gg", "te-ei-oc", "bts-tet"], go="p-transport", links=[0, 4])

q(id="getting-here", topic="Transportation", q="How do people get to the OC Vibe area?",
  a=f"Mostly by car: 74.0% of domestic trips to Anaheim and Garden Grove start within 50 miles, and SR-57 beside OC Vibe carries about 275,000 vehicles a weekday. ARTIC adds {TRANSIT['wk']} weekday bus trips, Amtrak (191,153 passengers in 2024) and Metrolink.",
  key="275,000", key_l="vehicles a weekday on SR-57 beside OC Vibe",
  geo=[["OC Vibe area", "275,000 vehicles", "SR-57, Ball Rd to Katella Ave (Caltrans 2024 count)", "OCTA 2026 Traffic Flow Map (Aug. 2026)"],
       ["ARTIC", f"{TRANSIT['wk']} weekday bus trips", "Routes 50, 53 and 553; Saturday 182, Sunday 181", "OCTA schedules (Aug. 9–Nov. 7, 2026)"],
       ["Rail at ARTIC", "191,153 Amtrak passengers", "2024; Metrolink Orange County Line 5,116 weekday riders (FY26 Q2)", "Rail Passengers Association; Metrolink"],
       ["Orange County residents", f"{BTS['modes'][0][1]/BTS['workers']*100:.1f}% drive alone", f"{BTS['modes'][0][1]:,} of {BTS['workers']:,} workers; public transportation {BTS['modes'][4][1]/BTS['workers']*100:.1f}%", "U.S. BTS County Transportation Profile"]],
  viz=dict(kind="bars", title="How Orange County workers commute (%)", unit="%", rows=[
      dict(l=n, v=round(v / BTS['workers'] * 100, 1), t=f"{v / BTS['workers'] * 100:.1f}%", hi=(i == 0)) for i, (n, v) in enumerate(BTS['modes'])]),
  how="Bus trips are counted from OCTA's schedule files (every trip stopping at ARTIC on a weekday). Commute shares = workers by mode ÷ all workers 16 and over.",
  caveat="Metrolink figures are line totals, not ARTIC boardings. Traffic counts for arterials date from 2021 to 2024.",
  files=["octa-adt", "octa-gtfs", "rpa-ana", "metrolink", "bts-county", "az-geo"], go="p-transport")

q(id="travel-cost", topic="Transportation", q="What does it cost to travel here?",
  a=f"Gasoline averaged ${TET_GAS[2025][1]:.2f} a gallon on the West Coast in 2025 vs. ${TET_GAS[2025][0]:.2f} nationally. The average U.S. domestic airfare was ${TET_AIR[2025]:.0f} (+{(TET_AIR[2025]/TET_AIR[2019]-1)*100:.1f}% since 2019), and driving cost ${TET_AUTO[2024]:.2f} a mile in 2024.",
  key=f"${TET_GAS[2025][1]:.2f}", key_l="West Coast gasoline per gallon, 2025",
  geo=[["West Coast", f"${TET_GAS[2025][1]:.2f} a gallon", f"{(TET_GAS[2025][1]/TET_GAS[2025][0]-1)*100:.0f}% above the U.S. average (2025)", "U.S. BTS, Transportation Economic Trends, Table 3.1"],
       ["U.S.", f"${TET_GAS[2025][0]:.2f} a gallon", "Regular gasoline, 2025 average", "U.S. BTS, Table 3.1"],
       ["U.S. airfare", f"${TET_AIR[2025]:.0f}", f"Domestic average, 2025; ${TET_AIR[2019]:.0f} in 2019", "U.S. BTS, Table 3.4"],
       ["U.S. driving", f"${TET_AUTO[2024]:.2f} a mile", f"Average total cost, 2024; ${TET_AUTO[2019]:.2f} in 2019", "U.S. BTS, Table 6.6"]],
  viz=dict(kind="bars", title="Average domestic airfare, U.S. ($)", fmt='"$"#,##0', rows=[dict(l=str(y), v=round(v), t=f"${v:.0f}", hi=(y == 2025)) for y, v in TET_AIR.items()]),
  how="Values as published by BTS in current dollars.", caveat="National averages; Orange County fares and prices can differ.", files=["bts-tet"], go="p-transport", links=[4])

# ===== District 5 and who visits =====
q(id="d5-who", topic="District 5 and who visits", q="Who visits District 5, where OC Vibe is being built?",
  a=f"{D5['overnight']}% of District 5 visitors stay overnight and {D5['new']}% are first-time visitors (Jan.–May 2026). Their median household income is ${D5['hhi']}K, above the ${GEO['hhi']}K for all Anaheim and Garden Grove visitors and the ${CS_ECON['hhi_us']/1000:.1f}K U.S. household median.",
  key=f"{D5['overnight']}%", key_l="of District 5 visitors stay overnight",
  geo=[["District 5", f"{D5['overnight']}% overnight", f"{D5['new']}% new · median income ${D5['hhi']}K · 56.0% from California · sample {D5['sample']:,} devices", "Azira via Symphony (Jan. 1–May 31, 2026)"],
       ["Anaheim and Garden Grove", f"{GEO['overnight']}% overnight", f"{GEO['repeat']}% repeat · 1.3-day stay · median income ${GEO['hhi']}K · {GEO['ca']}% of trips from California", "Azira via Symphony (Aug. 2026)"],
       ["Orange County", f"${CS_ECON['hhi']/1000:.1f}K", "Median household income of residents", "Oxford Economics via CoStar (Oct. 12, 2026)"],
       ["U.S.", f"${CS_ECON['hhi_us']/1000:.1f}K", "Median household income", "Oxford Economics via CoStar (Oct. 12, 2026)"]],
  viz=dict(kind="bars", title="Top origin metros for District 5 visitors (% of unique visitors)", unit="%", rows=[
      dict(l="Los Angeles–Long Beach–Anaheim", v=23.6, t="23.6%", hi=True), dict(l="Riverside–San Bernardino–Ontario", v=22.6, t="22.6%"),
      dict(l="Washington–Arlington–Alexandria", v=3.6, t="3.6%"), dict(l="San Diego–Chula Vista–Carlsbad", v=3.2, t="3.2%"),
      dict(l="New York–Newark–Jersey City", v=2.0, t="2.0%"), dict(l="Phoenix–Mesa–Chandler", v=1.5, t="1.5%")]),
  how="Azira counts mobile devices seen in District 5. Overnight and new-visitor shares cover visitors who stayed 4+ hours, are not commuters and live 50+ miles away. Income is matched from U.S. Census data for home areas.",
  caveat="Location samples describe visitor mix; they are not visitor counts. Compare within Azira, not with Datafy or Visa.",
  files=["az-d5", "az-geo", "cs-mkt"], go="p-d5")

q(id="d5-share", topic="District 5 and who visits", q="How much Anaheim visitor activity already includes the OC Vibe area?",
  a=f"5.2% of Anaheim visitor days in 2024 included the OC Vibe area, before the new venues open (Datafy). Disneyland was in 74.4% and meeting services in 3.4%.",
  key="5.2%", key_l="of Anaheim visitor days included the OC Vibe area, 2024",
  geo=[["OC Vibe area", "5.2%", "Share of Anaheim visitor days (visitors 50+ miles; employees excluded)", "Datafy (calendar 2024)"],
       ["Disneyland", "74.4%", "Share of Anaheim visitor days", "Datafy (calendar 2024)"],
       ["Anaheim visitors", f"{DATAFY['overnight']}% overnight", f"Repeat {DATAFY['repeat']}% · 6+ day stays {DATAFY['los6']}%", "Datafy (calendar 2024)"]],
  viz=dict(kind="bars", title="Share of Anaheim visitor days that include each cluster, 2024 (%)", unit="%", rows=[
      dict(l=n, v=v, t=f"{v}%", hi=(n == "OC Vibe")) for n, v in DATAFY['clusters']]),
  how="Datafy assigns each visitor day to the clusters a device visited; a day can include several clusters, so shares add to more than 100%.",
  caveat="Datafy's calendar 2025 export (in the library) uses a different basis and is not yet used here; it will be reconciled at the next quarterly update.",
  files=["datafy-25", "az-d5"], go="p-d5")

q(id="d5-markets", topic="District 5 and who visits", q="Which markets bring visitors and spending?",
  a="Southern California dominates: Los Angeles and Riverside metros are 46.2% of District 5 visitors. By card spending, the leading fly-in metros are Seattle, Phoenix, Las Vegas, Orlando and New York; internationally, Mexico, Canada and Japan.",
  key="46.2%", key_l="of District 5 visitors come from the Los Angeles and Riverside metros",
  geo=[["District 5 visitors", "California 56.0%", "Texas 4.5% · Virginia 4.2% · Florida 3.7% · Arizona 2.4%", "Azira via Symphony (Jan. 1–May 31, 2026)"],
       ["Visitor card spending (U.S.)", "$464.6M", "Los Angeles metro 66.1%; Seattle $5.4M, Phoenix $4.9M, Las Vegas $4.5M, Orlando $3.4M, New York $3.3M (Aug. 2026)", "Visa Destination Insights via Symphony"],
       ["International card spending", "$17.9M", "Mexico $5.2M, Canada $3.2M, Japan $2.4M, United Kingdom $1.4M (Aug. 2026)", "Visa Destination Insights via Symphony"],
       ["International visitors", "2.16M (2026 forecast)", "Anaheim and Garden Grove; Mexico 819,078 (+6.9%)", S_TEFC]],
  viz=dict(kind="bars", title="Top states for District 5 visitors (% of unique domestic visitors)", unit="%", rows=[
      dict(l="California", v=56.0, t="56.0%", hi=True), dict(l="Texas", v=4.5, t="4.5%"), dict(l="Virginia", v=4.2, t="4.2%"),
      dict(l="Florida", v=3.7, t="3.7%"), dict(l="Arizona", v=2.4, t="2.4%"), dict(l="New York", v=2.2, t="2.2%")]),
  how="Origins are home locations of devices (Azira) or cardholder home metros (Visa). 46.2% = 23.6% + 22.6%.",
  caveat="Visa covers Visa cards only, and its geography set needs confirmation; use it for ranking markets, not totals.",
  files=["az-d5", "visa-type", "visa-intl", "te-fc-sep"], go="p-d5")

q(id="media", topic="District 5 and who visits", q="Does Visit Anaheim's marketing bring visitors?",
  a=f"Yes. From January through August 2026, paid media produced {MED['impr']/1e6:.1f}M measurable impressions and {MED['visits']:,} observed visits ({MED['per1k']} per 1,000 impressions), arriving about {MED['days']:.0f} days after seeing an ad.",
  key=f"{MED['visits']:,}", key_l="observed visits after ad exposure, Jan.–Aug. 2026",
  geo=[["All campaigns", f"{MED['visits']:,} visits", f"{MED['impr']:,} impressions · visit rate {MED['rate']}%", "Azira attribution via Symphony (Jan. 1–Aug. 31, 2026)"],
       ["Best campaign rate", "34.4 per 1,000", "Luxury campaign, Basis DSP", "Azira attribution via Symphony"],
       ["Top vendor by visits", "183,900 visits", "Basis DSP (13.3M impressions)", "Azira attribution via Symphony"]],
  viz=dict(kind="bars", title="Visits per 1,000 impressions by vendor", fmt='0.0', rows=[dict(l=v[0], v=v[3], t=f"{v[3]}", hi=(v[3] == max(x[3] for x in __import__('data').MED_VEND))) for v in __import__('data').MED_VEND]),
  how="Visits per 1,000 impressions = observed visits ÷ measurable impressions × 1,000. Only the first visit after exposure counts, with at least 3 days from exposure to visit.",
  caveat="Observed visits are a sample-based measure, not total visitors caused by ads.", files=["az-media"], go="p-media")

# ===== Hotels and outlook =====
dl = CS_SUB[0]
q(id="hotels", topic="Hotels and outlook", q="How are hotels performing?",
  a=f"Resort-area hotels filled {dl[2]}% of rooms at ${dl[4]:.0f} a night over the past 12 months (CoStar Disneyland submarket); countywide {CS_OC['occ']}% at ${CS_OC['adr']}. Anaheim hotel revenue per room rose {LARC_Q['q2_revpar']}% in Q2 2026, about twice the U.S. (+{LARC_Q['us_q2']}%).",
  key=f"{dl[2]}%", key_l="Disneyland submarket hotel occupancy, 12 months to Aug. 2026",
  geo=[["Disneyland submarket", f"{dl[2]}% · ${dl[4]:.0f}", f"RevPAR ${dl[6]:.2f} (+{dl[7]}%); {dl[1]:,} rooms", "CoStar (through Aug. 2026)"],
       ["Orange County", f"{CS_OC['occ']}% · ${CS_OC['adr']}", f"RevPAR ${CS_OC['revpar']} (+{CS_OC['revpar_chg']}%); {CS_OC['rooms']:,} rooms; {CS_OC['uc_rooms']} under construction", "CoStar (through Aug. 2026)"],
       ["Anaheim market vs. U.S.", f"+{LARC_Q['q2_revpar']}% vs. +{LARC_Q['us_q2']}%", "Revenue per available room, Q2 2026", "LARC Market Intelligence Report (Sept. 2026)"]],
  viz=dict(kind="bars", title="Hotel occupancy by Orange County submarket, 12 months (%)", unit="%", rows=[dict(l=s[0], v=s[2], t=f"{s[2]}%", hi=(i == 0)) for i, s in enumerate(CS_SUB)]),
  how="Occupancy = rooms sold ÷ rooms available; ADR = room revenue ÷ rooms sold; RevPAR = room revenue ÷ rooms available.",
  caveat="CoStar, STR and LARC use different hotel sets; compare trends, not levels.", files=["cs-mkt", "cs-dl", "larc-mir-09", "str-daily"], go="p-hotel")

l26 = [r for r in LARC if r[0] == 2026][0]
q(id="outlook", topic="Hotels and outlook", q="What is the outlook to 2028?",
  a=f"Tourism Economics forecasts Anaheim visitors rising to 27.6M and spending to $7.7B by 2028. LARC forecasts Anaheim hotel revenue per room of ${l26[5]:.2f} in 2026 (+{l26[6]}%). Nationally, trips are forecast to grow {UST['trips_chg26']:.1f}% in 2026.",
  key="$7.7B", key_l="Anaheim visitor spending forecast, 2028",
  geo=[["Anaheim visitors", "27.0M (2026) · 27.6M (2028)", "Spending $7.2B (2026) · $7.7B (2028)", S_TEFC],
       ["Anaheim hotels", f"${l26[5]:.2f} RevPAR (2026)", f"Occupancy {l26[1]}%, ADR ${l26[3]:.2f}", "LARC (Sept. 2026)"],
       ["U.S. travel", "2.51B trips (2026)", f"Spending $1.374T (real 2025 dollars); international arrivals 70.6M", S_UST]],
  viz=dict(kind="bars", title="Anaheim visitor spending, actual and forecast ($B)", fmt='"$"0.0"B"', rows=[
      dict(l=f"{y}{'F' if y > 2025 else ''}", v=s, t=f"${s:.1f}B", hi=(y == 2028)) for y, s in zip(YEARS, ANA_SP) if y >= 2022]),
  how="Forecasts as published by Tourism Economics (Sept. 2026), LARC (Sept. 2026) and the U.S. Travel Association (Spring 2026).",
  caveat="Forecasts change with each edition; the June edition had 27.1M visitors for 2026.", files=["te-fc-sep", "te-fc-jun", "larc-mir-09", "larc-set-3q"], go="p-larc", links=[1])

# ===== About this report =====
q(id="reports", topic="About this report", q="Where can I get the full reports and data behind this app?",
  a="Every file used to build this app is in the Reports and data library: Tourism Economics' 2025 Economic Impact reports for Anaheim, Garden Grove and Orange County, the Q2 2026 Travel Forecast, the One more night study, Symphony, CoStar, STR, LARC and transportation files.",
  key=str(len([f for f in L.FILES if f.get('orig')])), key_l="source files to view or download",
  geo=[["Economic impact", "7 files", "Anaheim, Garden Grove and Orange County reports, supplemental charts and one-pagers (2025)", "Tourism Economics"],
       ["Quarterly results", "2 files", "Travel Forecast, Sept. 2026 (Q2 results) and June 2026 (Q1)", "Tourism Economics"],
       ["One more night", "2 files", "Study deck and workbook", "Visit Anaheim BI"]],
  viz=None, how="Files are published as received; Visit Anaheim-owned files have neutral document properties.",
  caveat="Third-party reports remain the work of their publishers; cite the publisher and date when quoting.", files=["te-ei-ana", "te-ei-gg", "te-ei-oc", "te-fc-sep", "va-night"], go="p-library")

q(id="updates", topic="About this report", q="How often is this updated, and what is coming next?",
  a="Quarterly, on the 15th of January, April, July and October, after Tourism Economics' quarterly forecast. Planned additions: Ticketmaster data from Honda Center, Placer.ai foot traffic and a Tourism Economics transportation impact analysis.",
  key="Quarterly", key_l="next updates Jan. 15, Apr. 15, July 15 and Oct. 15",
  geo=[["Core data", "Tourism Economics", "Quarterly forecast and annual economic impact", "Visit Anaheim BI"],
       ["Pulled each update", "STR, CoStar, Visa, Azira", "Weekly or monthly sources pulled together so every figure shares one as-of date", "Visit Anaheim BI"],
       ["Planned", "3 new sources", "Ticketmaster (Honda Center), Placer.ai, Tourism Economics transportation impact; no figures until received and checked", "Visit Anaheim BI"]],
  viz=None, how="See Sources > How this report is updated.", caveat="", files=[], go="p-notes")

QORDER = ["Visitor spending", "Jobs and economy", "One more night", "Transportation", "District 5 and who visits", "Hotels and outlook", "About this report"]
CORE = ["avg-spend", "night-value", "transport-impact", "d5-who"]   # the four headline questions


def attach(SECTIONS, SOURCES, DQ, REGISTER, DATA_EXTRA):
    S = {s['id']: s for s in SECTIONS}
    # Visitor spending: average spend at every level
    S['p-spend']['tables'].append(dict(
        title="Average spend: Anaheim, Orange County, California and U.S.", hi=0,
        sub="Spending per visitor (Tourism Economics) or per trip (U.S. Travel Association). Calculation shown for each row.",
        cols=[["Geography", 0], ["Spending per visitor or trip", 1], ["How it is calculated", 0], ["Year", 0]],
        rows=[["Anaheim", f"${A['pv25']:.0f}", f"${A['sp25']/1000:.3f}B ÷ {A['vis25']}M visitors", "2025"],
              ["Garden Grove", f"${G['pv25']:.0f}", f"${G['sp25']:.1f}M ÷ {G['vis25']}M visitors", "2025"],
              ["Orange County", f"${O['pv_pub'][0]}", "Published by Tourism Economics (day $58, overnight $737)", "2025"],
              ["U.S., per trip", f"${UST['per_trip']:.0f}", "$1.360T ÷ 2.46B trips (real 2025 dollars)", "2025"],
              ["U.S., per domestic trip", f"${UST['dom_per_trip']:.0f}", "$1.185T ÷ 2.40B domestic trips", "2025"]],
        src=S_TE + "; " + S_UST + " (accessed Oct. 14, 2026)"))
    # Getting here: economic impact of visitor transportation
    S['p-transport']['tables'].append(dict(
        title="Economic impact of visitor transportation, 2025", hi=0,
        sub="Visitor transportation spending and the jobs, business sales and labor income it supports in transportation and gas stations (direct + indirect + induced).",
        cols=[["Geography", 0], ["Visitor transportation spending", 1], ["Share of visitor spending", 1], ["Business sales", 1], ["Jobs", 1], ["Labor income", 1]],
        rows=[[g, m(t['spend']) if t['spend'] >= 100 else f"${t['spend']:.1f}M", f"{t['share']:.1f}%", m(t['sales_t']) if t['sales_t'] >= 100 else f"${t['sales_t']:.1f}M", f"{t['jobs_t']:,}",
               f"${t['inc_t']:.0f}M" if t['inc_t'] >= 10 else f"${t['inc_t']:.1f}M"] for g, t in TE_TR.items()] +
             [["California (direct only)", f"${VCA['tr']:.1f}B", f"{VCA['tr_share']:.1f}%", "Not published", f"{VCA['tr_jobs']:,.0f}", "Not published"]],
        src=S_TE + " (industry tables: other transport, gas stations, air transport); " + S_VCA + " (accessed Oct. 14, 2026)"))
    REGISTER.extend([
        ["U.S. Travel Association and Tourism Economics", "Travel Forecast, Spring 2026", "2024–2026", "Spring 2026; accessed Oct. 14, 2026", "U.S. travel spending and trips; spending per trip", "Values read from the published forecast tables; real 2025 dollars"],
        ["U.S. Travel Association", "Economic Impact of the U.S. Travel Industry", "Calendar 2025", "2026; accessed Oct. 14, 2026", "U.S. jobs supported, output and state and local taxes", "Published fact sheet"],
        ["Visit California (Dean Runyan Associates)", "The Economic Impact of Travel in California, 2025p (primary report)", "Calendar 2025", "Apr. 6, 2026; accessed Oct. 14, 2026", "California and Orange County travel spending, jobs and taxes; transportation spending and jobs", "Primary report reviewed; preliminary (2025p)"],
    ])
    DQ.extend([
        "Average spend compares per-visitor values (Tourism Economics) with per-trip values (U.S. Travel Association, in 2025 dollars); compare direction, not exact levels.",
        "Visitor transportation shares differ by source: Visit California counts visitor air fares and statewide ground travel; Tourism Economics' city figures count spending inside the city (Anaheim has no commercial airport).",
        "Visit California's Orange County total ($17.1B direct travel spending, 2025p) uses a different method from Tourism Economics' ($17.99B visitor spending); use one source at a time.",
    ])
    lib = L.finalize(ASK)
    COMPARE = dict(title="How Anaheim compares: five measures, side by side", src="Tourism Economics, Economic Impact of Visitors 2025; Visit California 2025p; U.S. Travel Association and Tourism Economics, Spring 2026", rows=[
        dict(m="Spending per visitor (U.S.: per trip)", unit="$", q="avg-spend", pts=[["Anaheim", round(A['pv25'])], ["Garden Grove", round(G['pv25'])], ["Orange County", O['pv_pub'][0]], ["U.S.", round(UST['per_trip'])]]),
        dict(m="Visitor spending growth, 2025 (%)", unit="%", q="spend-growth", pts=[["Anaheim", round(A['sp_chg'], 1)], ["Orange County", round(O['sp_chg'], 1)], ["California", round(VCA['chg'], 1)], ["U.S.", round(UST['chg'], 1)]]),
        dict(m="Transportation share of visitor spending (%)", unit="%", q="transport-impact", pts=[[g, round(t['share'], 1)] for g, t in TE_TR.items()] + [["California", round(VCA['tr_share'], 1)]]),
        dict(m="Food and beverage share of visitor-supported jobs (%)", unit="%", q="fb-jobs", pts=[["Anaheim", round(A['fb_job_share'], 1)], ["Garden Grove", round(G['fb_job_share'], 1)], ["Orange County", round(O['fb_job_share'], 1)], ["California", 55.3]]),
        dict(m="Share of all jobs supported by visitors (%)", unit="%", q="jobs", pts=[["Anaheim", A['jobs_share']], ["Garden Grove", G['jobs_share']], ["Orange County", O['jobs_share']]]),
    ], notes="California food and beverage combines accommodation and food service (direct jobs only). U.S. spending is per trip in 2025 dollars; growth for the U.S. is after inflation.")
    MIX = dict(title="Where 2025 visitor spending goes: Anaheim and Orange County", src="Tourism Economics, Economic Impact of Visitors 2025 (pub. Apr.–May 2026)",
               geos=[dict(g="Anaheim", total=A['sp25'], parts=[["Recreation", A['rec']], ["Lodging", A['lodging']], ["Retail", A['retail']], ["Food and beverage", A['fb']], ["Transportation", A['transport']]]),
                     dict(g="Orange County", total=O['sp25'], parts=[["Recreation", O['rec']], ["Lodging", O['lodging']], ["Retail", O['retail']], ["Food and beverage", O['fb']], ["Transportation", O['transport']]])])
    DATA_EXTRA['ask'] = dict(items=ASK, order=QORDER, core=CORE, compare=COMPARE, mix=MIX)
    DATA_EXTRA['lib'] = dict(files=lib, topics=L.TOPICS, links=L.LINKS, asof='Oct. 14, 2026')
