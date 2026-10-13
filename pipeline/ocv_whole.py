"""OC Vibe as a whole: every insight written for the whole OC Vibe organization.

The work of OC Vibe's teams (real estate programming and development operations; development programming,
research and operations; special events; entertainment and venues; leadership; marketing and partnerships) shaped
which data and analysis appear in each section. Roles are never broken out or named; each insight says what it
enhances for OC Vibe and what OC Vibe needs to act on it, tagged by topic.

Also: the overview's main announcement, article headlines, key insights with source and date, an "Explanation"
compare-and-contrast item per section, a 2026 hotel calendar for event and programming planning (STR daily),
and recent public facts about OC Vibe. Validation stays internal: no checks page or check counts in the report.
"""
import os as _os
BASE = _os.path.dirname(_os.path.abspath(__file__))  # pipeline folder
import json, re
import pandas as pd
import impact as I, newdata as ND
import logic_content as L
import roles_content as RC

B = I.RES[1]; V = I.VIEWS["Base"]
M = lambda v, d=1: f"${v/1e6:,.{d}f}M"
sunmon, frisat = ND.SUNMON_OCC, ND.FRISAT_OCC

S_OCBJ26 = "Orange County Business Journal (June 1, 2026)"
S_PR = "OCVIBE concert hall release, PR Newswire (Mar. 12, 2026)"
S_BIZ = "BizBash (Sept. 16, 2026)"
S_TRANSIT = "California's transit systems data snapshots (2003–2017; downloaded Oct. 12, 2026)"
S_TID = "Simpleview TID incentive bookings (exported Jan. 20, 2025)"
S_VA = "Visit Anaheim, 2025 tourism results (pub. June 3, 2026)"

import glob as _glob
_R = json.load(open(sorted(_glob.glob(BASE + "/computations/validation-*/results.json"))[-1]))
_mc, _sh = _R["monte_carlo"]["spend"], _R["sensitivity"]["src_share"]
S_SIM = "Visit Anaheim BI scenario model: 200,000-draw simulation (Oct. 12, 2026)"
RANGE_TABLE = dict(title="How wide the estimate is, and what moves it", sub="New visitor spending from OC Vibe at full operation, 2025 dollars",
                   cols=[["Measure", 0], ["Value", 1], ["What it means", 0]],
                   rows=[["Base case", M(B["spend"]), "Stated assumptions (see Scenario assumptions)"],
                         ["Simulation range (90% of draws)", f"{M(_mc['p5'],0)}–{M(_mc['p95'],0)}", "Assumptions varied together between the conservative and optimistic cases"],
                         ["Simulation median", M(_mc["p50"], 0), "Above the base case because the add-a-day range is wider on the upside"]] +
                        [[f"Driver: {k.lower()}", f"{v*100:.0f}% of the range", "Measure it with OC Vibe data to narrow the estimate"] for k, v in sorted(_sh.items(), key=lambda kv: -kv[1])[:3]],
                   hi=1, src=S_SIM)


# ---------------- 2026 hotel calendar for event and programming planning (STR daily) ----------------
_s = pd.read_excel(BASE + "/files/licensed/STR_Daily_Data_8.xlsx"); _s["Date"] = pd.to_datetime(_s["Date"])
_t = _s[(_s.Geography == "Anaheim+") & (_s.Segment == "Total") & (_s.Date < "2026-10-01")].copy()
_g = _s[(_s.Geography == "Anaheim+") & (_s.Segment == "Group") & (_s.Date < "2026-10-01")].copy()
_t["m"] = _t.Date.dt.month; _t["d"] = _t.Date.dt.dayofweek; _g["m"] = _g.Date.dt.month
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept."]
CAL = []
for m, x in _t.groupby("m"):
    wk, we = x[x.d.isin([6, 0, 1, 2, 3])], x[x.d.isin([4, 5])]
    gg = _g[_g.m == m]
    CAL.append(dict(m=MONTHS[m - 1], occ=x.Demand.sum() / x.Supply.sum() * 100, adr=x.Revenue.sum() / x.Demand.sum(),
                    wk=wk.Demand.sum() / wk.Supply.sum() * 100, we=we.Demand.sum() / we.Supply.sum() * 100,
                    n90=int((x.Occupancy >= 0.9).sum()), grp=gg.Demand.sum() / x.Demand.sum() * 100))
SOFT = sorted(CAL, key=lambda c: c["wk"])[:4]                 # months with the most open weeknight rooms
PEAK90 = max(CAL, key=lambda c: c["n90"])
GRP_HI = sorted(CAL, key=lambda c: -c["grp"])[:2]
_sn = [c["m"] for c in sorted(SOFT, key=lambda c: MONTHS.index(c["m"]))]
soft_names = ", ".join(_sn[:-1]) + " and " + _sn[-1]
soft_rng = f"{min(c['wk'] for c in SOFT):.0f}%–{max(c['wk'] for c in SOFT):.0f}%"
CAL_TABLE = dict(title="When Anaheim hotels have room: 2026 by month", sub="Visit Anaheim hotel set (Anaheim+), Jan.–Sept. 2026 · weeknights = Sunday–Thursday nights",
                 cols=[["Month", 0], ["Occupancy", 1], ["Average rate", 1], ["Weeknight occupancy", 1], ["Friday–Saturday occupancy", 1], ["Nights at 90%+", 1], ["Group share of rooms", 1]],
                 rows=[[c["m"], f"{c['occ']:.1f}%", f"${c['adr']:.0f}", f"{c['wk']:.1f}%", f"{c['we']:.1f}%", str(c["n90"]), f"{c['grp']:.1f}%"] for c in CAL],
                 hi=MONTHS.index(PEAK90["m"]), full=True, src=L.S_STR + "; weeknight and monthly figures are BI calculations")

# ---------------- recent public facts about OC Vibe ----------------
FACTS_TABLE = dict(title="OC Vibe in recent public sources", sub="Phasing and venues as reported; figures differ by source (see About the data)",
                   cols=[["Item", 0], ["As reported", 0], ["Source and date", 0]],
                   rows=[["Phase 1", "Opens early 2027: concert hall, Katella Commons market hall, The Weave office and Urban Park", S_OCBJ26],
                         ["Concert hall", "5,000 capacity; concerts, comedy, televised and award shows, esports and private events", S_PR],
                         ["Katella Commons", "50,000 sq ft food hall with 21 culinary concepts and six bars", S_OCBJ26],
                         ["Parking", "Two of three new garages open; parking in the two new garages is free", S_OCBJ26],
                         ["2028", "Honda Center hosts LA28 indoor volleyball; first hotel and Katella bridge to ARTIC", S_OCBJ26 + "; " + L.S_LARC],
                         ["Honda Center events", "D23 evening showcases: 36,000+ guests over three nights, alongside the Convention Center expo (Aug. 2026)", S_BIZ],
                         ["Full build-out", "About 2033", S_OCBJ26]],
                   hi=-1, wide=True, src="Public OC Vibe sources as listed in each row")

# ---------------- key insights (lead paragraph of each article) with source and date ----------------
ANS = {
 "p-ocv": (f"The OC Vibe area already shares in about {M(V['ocv_today']['spend'],0)} of visitor spending a year (5.2% of Anaheim visitor days × ${V['ana_today']['spend']/1e9:.2f}B). "
           f"At full operation, Visit Anaheim BI estimates OC Vibe adds about {M(B['spend'])} a year in new visitor spending: {M(B['sp_new'])} from about {round(B['new_vis'],-3):,.0f} net-new visitors at $258 each, "
           f"plus {M(B['sp_stay'])} from {B['extra_days']:,.0f} extra visitor days at ${I.PER_DAY:.2f} each. Across 200,000 simulations of the assumptions, 90% of results fall between $71M and $122M. "
           f"That lifts Anaheim's visitor spending from ${V['ana_today']['spend']/1e9:.2f}B to ${V['ana_live']['spend']/1e9:.2f}B (${V['ana_today']['spend']/1e9:.2f}B + {M(B['spend'])}).",
           f"{L.S_TE_EI}; {L.S_DATAFY}; {L.S_MODEL}"),
 "p-spend": ("Each Anaheim visitor spent about $258 in 2025 ($6.83B visitor spending ÷ 26.5M visitors), and Tourism Economics forecasts $279 by 2028. Visitors spent $1.76B in Q2 2026, up 7.8% from Q2 2025.",
             f"{L.S_TE_EI}; {L.S_TE_FC}"),
 "p-impact": ("Visitors supported 67,817 Anaheim jobs in 2025, about one in three, and 178,164 countywide. Food and beverage holds 16.8% of those jobs in Anaheim and 29.1% countywide.",
              L.S_TE_EI),
 "p-night": ("If every Anaheim visitor stayed one more night, lodging spending would rise about $794M ($1.724B 2025 lodging spending ÷ 2.17-day average stay). For OC Vibe, each 1% of visitors who add a day is worth about $31.5M a year (26.5M visitors × 1% × $118.71 per visitor day).",
             f"{L.S_NIGHT}; {L.S_MODEL}"),
 "p-transport": ("Most visitors arrive by car: 74.0% of domestic trips start within 50 miles, and SR-57 beside OC Vibe carries about 275,000 vehicles a weekday. ARTIC adds 277 weekday bus trips (routes 50, 53 and 553: 100 + 102 + 75), Amtrak and Metrolink.",
                 f"{L.S_AZIRA}; {L.S_OCTA}; {L.S_RAIL}"),
 "p-d5": ("85.8% of District 5 visitors stay overnight and 43.8% are first-time visitors. The OC Vibe area already accounts for 5.2% of Anaheim visitor days.",
          f"{L.S_AZIRA}; {L.S_DATAFY}"),
 "p-media": ("Visit Anaheim's paid media produced 31.0M measurable impressions and 368,416 observed visits from January through August 2026; visitors arrived about 39 days after seeing an ad.",
             L.S_MEDIA),
 "p-hotel": (f"Demand is strong and new supply is scarce: Disneyland submarket hotels filled 78.4% of rooms at $255 a night, and only 668 rooms are under construction countywide. "
             f"Weeknights have the most room: Visit Anaheim hotels ran {sunmon:.1f}% full on Sunday–Monday nights vs. {frisat:.1f}% on Friday–Saturday, a {frisat-sunmon:.1f}-point gap (averages of the two nights each).",
             f"{L.S_COSTAR}; {L.S_STR}"),
 "p-larc": ("Anaheim hotel revenue per room rose 11.4% in Q2 2026 (U.S. +5.7%), and Convention Center room nights are pacing +12% for 2026 and +17% for 2027. Costs are the headwind: prices are rising about 3.2% a year and labor about 6%.",
            L.S_LARC),
}

# ---------------- what each insight enhances for OC Vibe, and what OC Vibe needs ----------------
FOR_OCV = {
 "p-ocv": dict(
   enhance=[("Strategy", f"Shows OC Vibe's value three ways: Anaheim today (${V['ana_today']['spend']/1e9:.2f}B), Anaheim with OC Vibe (${V['ana_live']['spend']/1e9:.2f}B), and OC Vibe's own associated spending ({M(V['ocv_today']['spend'],0)} today, {M(V['ocv_live']['spend'],0)} when live).", f"{L.S_TE_EI}; {L.S_DATAFY}; {L.S_MODEL}"),
            ("Community", f"Base case a year: about {round(B['ana_jobs'],-1):,.0f} Anaheim jobs, {M(B['ana_impact'],0)} in Anaheim economic impact and {M(B['ana_tax'])} in state and local taxes.", L.S_MODEL),
            ("Programming", "Shows where new spending goes: recreation and entertainment 34.0%, lodging 25.2%, retail 21.9%, food and beverage 15.6%, a guide for the district's tenant and venue mix.", f"{L.S_TE_EI}; {L.S_MODEL}"),
            ("Events", "Values each lever: every 1% of visitors who add a day is worth $31.5M, every 1,000 net-new visitors $258,000, and every 100 concert hall nights at 80% full brings about 449,000 attendees.", L.S_MODEL)],
   need=[("Measurement", "Ticket-buyer ZIP codes from the first 2027 shows, to measure how many attendees are new to Anaheim; this assumption drives 39% of the range.", S_SIM),
         ("Hotels", "Hotel and package results, to measure how many visitors add a day; this assumption drives 40% of the range.", S_SIM),
         ("Measurement", f"A confirmed concert hall capacity: 5,000 seats (OCVIBE, Mar. 2026) vs. 5,613 (City of Anaheim, 2026). At 5,000 seats the base case is {M(RC.CAP5000)}.", f"{S_PR}; {L.S_CITY}; {L.S_MODEL}"),
         ("Strategy", "One shared scorecard with baselines already set (5.2% of visitor days, 2.17-day average stay, 85.8% overnight), refreshed quarterly with Visit Anaheim BI.", f"{L.S_DATAFY}; {L.S_AZIRA}")]),
 "p-spend": dict(
   enhance=[("Strategy", "Values every new visitor at about $258 (2025), rising to $279 by 2028; every 1,000 net-new visitors adds about $258,000.", f"{L.S_TE_EI}; {L.S_TE_FC}"),
            ("Programming", "Visitor spending grows faster than visits (+4.1% vs. +1.4% a year to 2028), so premium seating, dining and packages add more value than attendance alone.", L.S_TE_FC),
            ("Marketing", "Visitor card spending reached $464.6M in August 2026 (+8.1%), and spending per card rose 4.7% to $85.", L.S_VISA)],
   need=[("Programming", "Dining, event and package pricing built for visitors as well as locals; the average visitor card transaction was $43 in August 2026.", L.S_VISA),
         ("Measurement", "Card spending mapped to the OC Vibe area, to separate OC Vibe's spending from the citywide total.", L.S_VISA),
         ("Measurement", "Visits and spending per visitor tracked together, so price increases are not mistaken for growth.", L.S_TE_FC)]),
 "p-impact": dict(
   enhance=[("Community", f"Each $1M of new visitor spending supports about 9.9 Anaheim jobs and $142,000 in state and local taxes; OC Vibe's base case supports about {round(B['ana_jobs'],-1):,.0f} jobs, about 150 in food and beverage.", f"{L.S_TE_EI}; {L.S_MODEL}"),
            ("Programming", "Food and beverage was the fastest-growing visitor spending category in 2025 (+5.5%), and OC Vibe plans 35+ restaurants (171,544 sq ft).", f"{L.S_TE_EI}; {L.S_CITY}"),
            ("Community", "Visitors saved each Anaheim household about $8,940 in taxes in 2025, a community benefit OC Vibe's visitors add to.", S_VA)],
   need=[("Operations", "A hiring plan for the 2027 openings, with labor costs rising about 6% a year.", L.S_LARC),
         ("Measurement", "OC Vibe's sales by category once venues open, to replace citywide ratios with its own mix.", L.S_TE_EI),
         ("Community", "Local hiring and wage figures, to report OC Vibe's jobs benefit directly.", L.S_TE_EI)]),
 "p-night": dict(
   enhance=[("Hotels", "Two in three Anaheim visitors (67.5%) are day visitors; evening shows and 550 planned hotel rooms are what turn a day trip into an overnight stay.", f"{L.S_TE_EI}; {L.S_CITY}"),
            ("Events", f"Each point of Sunday–Monday hotel occupancy citywide is about 22,200 room nights and $5.1M in room revenue a year.", f"{L.S_STR}; {L.S_MODEL}"),
            ("Events", "Groups booked with Tourism Improvement District incentives (as of Jan. 2025): 30 events and 460,566 room nights in 2026, 26 events in 2027.", S_TID)],
   need=[("Hotels", "Show-and-stay packages with nearby hotels for 2027, since OC Vibe's own hotels open in 2028.", L.S_CITY),
         ("Measurement", "Package redemptions (nights added) shared with Visit Anaheim, to measure the add-a-day share.", L.S_MODEL),
         ("Strategy", "Planning values in 1% steps ($15.7M at 0.5%, $31.5M at 1%, $62.9M at 2%) rather than the $3.15B ceiling.", L.S_NIGHT)]),
 "p-transport": dict(
   enhance=[("Marketing", "A large drive market: about 20 million people live within 90 miles, and 15.6 million within 50 miles of ARTIC.", f"{L.S_COSTAR}; {L.S_RAIL}"),
            ("Operations", "A transit front door: 277 weekday bus trips at ARTIC, Amtrak (191,153 passengers in 2024), Metrolink's Orange County Line (5,116 weekday riders, +4%) and the 2028 Katella bridge.", f"{L.S_OCTA}; {L.S_RAIL}"),
            ("Marketing", "Travelers already ask Visit Anaheim's trip planner about ARTIC parking, Honda Center events and OC Vibe's opening.", L.S_MT)],
   need=[("Operations", "An event-night plan: two sell-outs at once bring about 8,600–10,800 vehicles, filling 67%–87% of the 12,369–12,823 planned parking spaces.", f"{L.S_MODEL}; {L.S_CITY}"),
         ("Events", "Late-night service requested early: only 11 OCTA buses leave ARTIC after 10 p.m.; OCTA's staff fell 14.6% from 2003 to 2017 and county transit riders fell 38% from 2007 to 2017.", f"{L.S_OCTA}; {S_TRANSIT}"),
         ("Marketing", "One 'getting to OC Vibe' page covering parking, bus, Amtrak and Metrolink.", L.S_OCTA)]),
 "p-d5": dict(
   enhance=[("Measurement", "A baseline before opening: the OC Vibe area already accounts for 5.2% of Anaheim visitor days (2024).", L.S_DATAFY),
            ("Marketing", "New money: 44% of District 5 domestic visitors come from outside California; fly-in markets include Seattle, Phoenix, Las Vegas, Orlando and New York, and Mexico ($5.2M) and Canada ($3.2M) lead international card spending.", f"{L.S_AZIRA}; {L.S_VISA}"),
            ("Programming", "Visits are spread across the week (Saturday 15.9%, Tuesday 13.3%), so weekday programming has an audience.", L.S_AZIRA),
            ("Hotels", "13.7% of District 5 visitors also go to the Anaheim Resort, a direct path to packages and longer stays.", L.S_AZIRA)],
   need=[("Measurement", "Ticketing and loyalty data by origin, to track the out-of-state share.", L.S_AZIRA),
         ("Programming", "Dining offers for international guests: international restaurant spending fell 19.1% in August 2026.", L.S_VISA),
         ("Measurement", "Trends compared within each source (Azira, Datafy, Visa), since they count visitors differently.", f"{L.S_AZIRA}; {L.S_DATAFY}; {L.S_VISA}")]),
 "p-media": dict(
   enhance=[("Marketing", "Reach that converts: 11.9 visits per 1,000 impressions overall and 34.4 for the best luxury placements.", L.S_MEDIA),
            ("Measurement", "A measurable channel: attribution can track visits from target markets once OC Vibe appears in campaigns.", L.S_MEDIA),
            ("Events", "Timing: visitors arrive about 39 days after an ad, so events can be marketed six to eight weeks ahead.", L.S_MEDIA)],
   need=[("Events", "An event calendar shared with Visit Anaheim six to eight weeks ahead.", L.S_MEDIA),
         ("Marketing", "OC Vibe venue, dining and opening content for Visit Anaheim's luxury and travel-planning channels.", L.S_MEDIA),
         ("Measurement", "Control markets for key campaigns, since attribution shows association, not cause.", L.S_MEDIA)]),
 "p-hotel": dict(
   enhance=[("Hotels", "Room for OC Vibe's 550 planned rooms: about 141K–157K room nights, $30.6M–$40.1M in room revenue and $4.6M–$6.0M in hotel tax a year.", f"{L.S_MODEL}; {L.S_COSTAR}"),
            ("Events", f"Open weeknights for events: {soft_names} weeknights ran {soft_rng} full in 2026, while {PEAK90['m']} had {PEAK90['n90']} nights at 90%+.", L.S_STR),
            ("Programming", "Food and beverage is 29.4% of Orange County hotel revenue, and food revenue per room rose 28.9%.", L.S_COSTAR)],
   need=[("Hotels", "A rate position between the Anaheim submarket ($130) and the Disneyland submarket ($255), set by night of week.", L.S_COSTAR),
         ("Events", f"Group blocks timed to convention season: groups took {GRP_HI[0]['grp']:.1f}% of rooms in {GRP_HI[0]['m']} and {GRP_HI[1]['grp']:.1f}% in {GRP_HI[1]['m']} 2026.", L.S_STR),
         ("Measurement", "Monthly occupancy and rate from OC Vibe's hotels once open, to compare with STR and CoStar.", f"{L.S_STR}; {L.S_COSTAR}")]),
 "p-larc": dict(
   enhance=[("Events", "Opens into growth: 2027 convention pacing (+17%) coincides with OC Vibe's first venues, and conventions (142 events secured for 2026, about 600,000 room nights) bring weekday guests.", f"{L.S_LARC}; Visit Anaheim via CoStar (2026 bookings)"),
            ("Events", "A proven pairing: D23's evening showcases at Honda Center drew 36,000+ guests over three nights alongside the Convention Center expo (Aug. 2026).", S_BIZ),
            ("Marketing", "The 2028 Olympics bring indoor volleyball to Honda Center the same year OC Vibe's first hotel and the Katella bridge open.", f"{S_OCBJ26}; {L.S_LARC}")],
   need=[("Events", "Evening-event packages for 2027 Convention Center groups, sold with Visit Anaheim's sales team.", L.S_LARC),
         ("Strategy", "2027 targets set against 2025 as well as 2026, since the 2026 World Cup makes Q2–Q3 2027 a tough comparison.", L.S_LARC),
         ("Operations", "Staffing and pricing plans with labor (about 6% a year) and price growth (about 3.2% a year) built in.", L.S_LARC)]),
}

# ---------------- "Explanation" item for each compare-and-contrast ----------------
EXPLAIN = {
 "p-ocv": ("OC Vibe's impact comes from new visitors who would not otherwise come ($258 each) and existing visitors who stay longer ($118.71 per extra day). Locals and visitors already in town are not counted.", L.S_MODEL),
 "p-spend": ("Spending grows faster than visits because spending per trip rises with prices (Anaheim inflation about 3.2% a year) while visitor counts grow slowly.", f"{L.S_TE_FC}; {L.S_LARC}"),
 "p-impact": ("Tourism Economics converts visitor spending into direct, indirect and induced jobs and taxes; Anaheim's 2025 ratio is $1.53 of total impact per $1 of visitor spending.", L.S_TE_EI),
 "p-night": ("The $794M divides 2025 lodging spending ($1.72B) by the 2.17-day average stay; it assumes spending per night stays the same.", L.S_NIGHT),
 "p-transport": ("Driving dominates because most visitors live within 50 miles and county transit riders fell from 70.7M in 2007 to 43.8M in 2017; driving cost $0.82 a mile in 2024.", f"{L.S_AZIRA}; {S_TRANSIT}; {L.S_BTS}"),
 "p-d5": ("Azira counts devices seen in District 5 (sample 1,003,735, Jan.–May 2026); Datafy measures Anaheim visitor days in 2024. Both describe the area before OC Vibe's new venues open.", f"{L.S_AZIRA}; {L.S_DATAFY}"),
 "p-media": ("Attribution matches devices that saw an ad with devices later seen in Anaheim; it measures visits after exposure, not proof the ad caused them.", L.S_MEDIA),
 "p-hotel": ("CoStar covers submarkets and STR covers Visit Anaheim's hotel sets; the two use different hotels, so compare trends, not levels.", f"{L.S_COSTAR}; {L.S_STR}"),
 "p-larc": ("Booking pace compares convention room nights on the books with the same point a year earlier; LARC combines CoStar hotel data, Moody's economics and Visit Anaheim pacing.", L.S_LARC),
}

# ---------------- the overview's main announcement (facts only) ----------------
MAIN = dict(
  head="Anaheim's visitor market is growing into OC Vibe's 2027 opening",
  dek="Visitors spent $1.76 billion in Q2 2026 (+7.8%), hotel revenue per room rose 11.4%, and Convention Center room nights for 2027 are pacing 17% ahead.",
  lede="Anaheim's visitor economy is expanding ahead of OC Vibe's first openings in early 2027, Visit Anaheim Business Intelligence reported. Visitors spent $1.76 billion in the second quarter of 2026, up 7.8% from a year earlier (Tourism Economics, Sept. 2026), and hotel revenue per available room rose 11.4% (LARC, Sept. 2026).",
  paras=["The OC Vibe area already accounts for 5.2% of Anaheim visitor days (Datafy, 2024). In District 5, 85.8% of visitors stay overnight and 43.8% are first-time visitors (Azira, Jan.–May 2026).",
         f"Hotels have room on weeknights. Visit Anaheim's hotels ran {sunmon:.1f}% full on Sunday–Monday nights in 2026 vs. {frisat:.1f}% on Friday–Saturday, and {soft_names} weeknights had the most open rooms (STR, Jan.–Sept. 2026). Each point of Sunday–Monday occupancy is worth about $5.1M in room revenue a year.",
         "Groups are a growing source of weekday guests. Convention Center room nights for 2027 are pacing 17% ahead (LARC, Sept. 2026), and Disney's D23 evening showcases drew 36,000+ guests to Honda Center over three nights alongside the Convention Center expo (BizBash, Sept. 2026).",
         "Most visitors drive: 74.0% of domestic trips start within 50 miles, and SR-57 beside the district carries about 275,000 vehicles a weekday (Azira, Aug. 2026; OCTA, Aug. 2026). ARTIC adds 277 weekday bus trips, Amtrak and Metrolink, but only 11 buses leave after 10 p.m.",
         "The full report covers OC Vibe's estimated impact, visitor spending, jobs, one more night, getting here, who visits, marketing reach, hotels and the market outlook, with the source and date for every figure."],
  stats=[["$1.76B", "Anaheim visitor spending, Q2 2026 (+7.8%)", "Tourism Economics (Sept. 2026)"],
         ["+11.4%", "Anaheim hotel revenue per room, Q2 2026", "LARC (Sept. 2026)"],
         ["+17%", "Convention Center room nights on the books, 2027", "LARC (Sept. 2026)"],
         ["5.2%", "OC Vibe area share of Anaheim visitor days", "Datafy (2024)"],
         [f"{sunmon:.1f}%", "Sunday–Monday hotel occupancy, 2026", "STR (Jan. 1–Oct. 3, 2026)"]],
  chart=dict(title="Growth vs. a year earlier", src="Tourism Economics (Sept. 2026); LARC (Sept. 2026); Visa via Symphony (Aug. 2026)",
             rows=[["Convention room nights, 2027 pace", 17, "+17%", True], ["Hotel revenue per room, Q2", 11.4, "+11.4%", False],
                   ["Convention room nights, 2026 pace", 12, "+12%", False], ["Visitor card spending, Aug.", 8.1, "+8.1%", False], ["Visitor spending, Q2", 7.8, "+7.8%", False]]),
  srcs=[L.S_TE_FC, L.S_LARC, L.S_DATAFY, L.S_AZIRA, L.S_STR, L.S_OCTA, S_BIZ, L.S_VISA],
)

TAGS = ["Strategy", "Programming", "Events", "Hotels", "Operations", "Marketing", "Measurement", "Community"]
INTERNAL_RX = re.compile(r"(\d+ of \d+ (calculation )?checks passed|independently re-checked|validation suite|Checks and confidence)", re.I)


def attach(SECTIONS, STORIES, TAKEAWAYS, RECS, DQ, REGISTER, SOURCES, DATA_EXTRA):
    # 1) remove the internal checks page and the role-view page
    SECTIONS[:] = [s for s in SECTIONS if s["id"] not in ("p-valid", "p-team")]
    STORIES.pop("p-valid", None)
    for s in SECTIONS:
        sid = s["id"]
        s.pop("role_notes", None); s.pop("warn", None)
        if sid in ANS:
            s["ans"], s["ans_src"] = ANS[sid]
        if sid in FOR_OCV:
            s["for_ocv"] = {k: [dict(tag=t, text=x, src=src) for t, x, src in v] for k, v in FOR_OCV[sid].items()}
        if sid in EXPLAIN and s.get("cc"):
            s["cc"] = [c for c in s["cc"] if c["type"] != "Explanation"] + [dict(type="Explanation", point=EXPLAIN[sid][0], solution=None, src=EXPLAIN[sid][1])]
        st = STORIES.get(sid)
        if st:
            s["head"], s["dek"] = st["head"], st["dek"]
        if sid == "p-ocv":
            s["tables"].append(RANGE_TABLE)
        if sid == "p-larc":
            s["tab"] = "Market outlook"
            s["tables"].append(FACTS_TABLE)
        if sid == "p-hotel":
            s["tables"].insert(1, CAL_TABLE)
            s["notes"].append(f"2026 hotel calendar (STR, Jan.–Sept.): weeknights had the most open rooms in {soft_names} ({soft_rng} full); {PEAK90['m']} had the most nights at 90%+ ({PEAK90['n90']}); groups took the largest share of rooms in {GRP_HI[0]['m']} ({GRP_HI[0]['grp']:.1f}%) and {GRP_HI[1]['m']} ({GRP_HI[1]['grp']:.1f}%). Use these windows to schedule events that need hotel rooms, and avoid peak nights for large out-of-town groups.")
        # internal-only wording out of customer content
        s["notes"] = [n for n in s["notes"] if not INTERNAL_RX.search(n)]
        if s.get("w5h"):
            s["w5h"] = {k: v.replace("; tested with 42 checks and a 200,000-draw simulation", "; the range comes from a 200,000-draw simulation")
                           .replace("CoStar and STR performance data; BI recomputation and bootstrap tests.", "CoStar and STR performance data: occupancy, average rate and revenue per room by submarket, month and night of week.")
                           .replace("BI analysis of OCTA's traffic map and raw bus schedules, recounted independently; rail station and line reports.", "BI analysis of OCTA's traffic map and bus schedules; rail station and line reports; California transit operator statistics.")
                           for k, v in s["w5h"].items()}
            s["w5h"]["src"] = re.sub(r";?\s*Visit Anaheim BI validation suite \(run [^)]*\)", "", s["w5h"]["src"])
        s["cards"] = [c for c in s["cards"] if not INTERNAL_RX.search(" ".join(map(str, c)))]
        for c in s.get("cc", []):
            c["src"] = c["src"].replace("Visit Anaheim BI validation suite (run Oct. 12, 2026)", L.S_MODEL)
    # 2) appendix without validation content
    for s in SECTIONS:
        if s["id"] == "p-appx":
            s["head"] = "Terms, methods and formulas behind every number"
            s["dek"] = "A plain-language guide to the glossary, methods and formulas used in this report."
            s["ans_src"] = "Visit Anaheim Business Intelligence (Oct. 12, 2026)"
            s["tables"] = [t for t in s["tables"] if t["title"] in ("Formulas", "Glossary", "Methods")]
            for t in s["tables"]:
                t["rows"] = [r for r in t["rows"] if not INTERNAL_RX.search(" ".join(map(str, r))) and "validation" not in " ".join(map(str, r)).lower()]
            s["tables"].append(dict(title="Who, what, when, where, why and how, by section", sub="The essentials of each section in one place",
                                    cols=[["Section", 0], ["Who", 0], ["What", 0], ["When", 0], ["Where", 0], ["Why", 0], ["How", 0]],
                                    rows=[[x["tab"]] + [x["w5h"][k] for k in ("who", "what", "when", "where", "why", "how")] for x in SECTIONS if x.get("w5h") and x["id"] != "p-appx"],
                                    hi=-1, full=True, wide=True, src="Visit Anaheim Business Intelligence (Oct. 12, 2026); sources by section"))
    DQ[:] = [d for d in DQ if not INTERNAL_RX.search(d)]
    TAKEAWAYS[:] = [t for t in TAKEAWAYS if not INTERNAL_RX.search(t)]
    for s in STORIES.values():
        s["stats"] = [x for x in s["stats"] if not INTERNAL_RX.search(" ".join(map(str, x)))]
        s["paras"] = [p for p in s["paras"] if not INTERNAL_RX.search(p)]
        s["lede"] = INTERNAL_RX.sub("", s["lede"])
    REGISTER[:] = [r for r in REGISTER if "validation" not in " ".join(map(str, r)).lower()]
    DATA_EXTRA["main"] = MAIN
    DATA_EXTRA["tags"] = TAGS
