"""Adds STR, CoStar monthly, Visa, Amtrak and Metrolink content (files received Oct. 12, 2026)."""
import newdata as ND
from data import D, sp

def M(v): return f"${v:,.1f}M"
DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
DOWL = dict(Sun="Sunday", Mon="Monday", Tue="Tuesday", Wed="Wednesday", Thu="Thursday", Fri="Friday", Sat="Saturday")
MON = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept."]

SRC_STR = f"STR, daily hotel data for Visit Anaheim hotel sets (Anaheim+, Garden Grove+), Jan. 1–Oct. 3, 2026 (export provided Oct. 12, 2026)"
SRC_CSM = "CoStar Group, submarket analytic export, monthly Jan.–Aug. 2026 (last processed Aug. 31, 2026; exported Oct. 12, 2026)"
SRC_VISA = "Visa Destination Insights (reported Visa card data) via Symphony | Tourism Economics, Visitor Type and International Card Activity, Aug. 2026 vs. Aug. 2025 (exported Oct. 12, 2026)"
SRC_AMTRAK = "Rail Passengers Association, Amtrak service in Anaheim, CA (ANA) fact sheet, 2018–2024 data (published Oct. 27, 2025)"
SRC_METRO = "Metrolink (SCRRA), Fact Sheet FY2025-26 Q2 (Oct.–Dec. 2025); rider profile from 2025 Customer Survey (March–April 2025)"

REG_ADD = [
  ["STR", "Daily hotel data, Visit Anaheim hotel sets (Anaheim+, Anaheim-Garden Grove+, Garden Grove+)", "Jan. 1–Oct. 3, 2026 (daily; by segment)", "Exported and provided Oct. 12, 2026", "Day-of-week occupancy and rates, group vs. transient mix, monthly 2026", "Totals recomputed from daily supply, demand and revenue; partial October excluded from monthly view"],
  ["CoStar Group", "Submarket analytic export (Anaheim, Disneyland, Newport Beach/Dana Point, Santa Ana/Costa Mesa, Northwest/Fullerton)", "Monthly Jan.–Aug. 2026", "Last processed Aug. 31, 2026; provided Oct. 12, 2026", "Monthly hotel performance by submarket", "12-month figures match the CoStar PDF reports"],
  ["Visa Destination Insights (via Symphony)", "Visitor Type; International Card Activity (Visit Anaheim view)", "Aug. 2026 vs. Aug. 2025", "Exported Oct. 12, 2026", "Visitor card spending, origin markets, international categories and countries", "Original PDFs reviewed; two identical copies received; confirm the geography set in the Visit Anaheim view"],
  ["Rail Passengers Association", "Amtrak service in Anaheim, CA (ANA) station fact sheet", "2018–2024", "Oct. 27, 2025", "Amtrak passengers at ARTIC, trip length, fare, top city pairs", "Original PDF reviewed; 2023 figure unusually low"],
  ["Metrolink (SCRRA)", "Fact Sheet FY2025-26 Q2", "Oct.–Dec. 2025", "FY2025-26 Q2 edition", "Orange County and Inland Empire–Orange County line ridership; rider profile", "Original PDF reviewed; line totals, not ARTIC station boardings"],
]

def attach(SECTIONS, SOURCES, DQ, REGISTER, TAKEAWAYS):
    sec = {s["id"]: s for s in SECTIONS}
    A = ND.STR["Anaheim+"]; G = ND.STR["Garden Grove+"]; AG = ND.STR["Anaheim-Garden Grove+"]
    gap = ND.FRISAT_OCC - ND.SUNMON_OCC

    # ---------- Hotel market: STR + CoStar monthly ----------
    h = sec["p-hotel"]
    h["tables"].append(dict(title="Visit Anaheim hotels by night of the week, 2026", sub=f"STR, Jan. 1–Oct. 3, 2026 ({A['nights']} nights)",
        cols=[["Night", 0], ["Anaheim+ occupancy", 1], ["Anaheim+ average rate", 1], ["Garden Grove+ occupancy", 1]], full=True,
        rows=[[DOWL[d], f"{A['dow'][d][0]:.1f}%", f"${A['dow'][d][1]:.0f}", f"{G['dow'][d][0]:.1f}%"] for d in DOW], hi=0, src=SRC_STR))
    h["tables"].append(dict(title="Visit Anaheim hotel sets, 2026 year to date", sub="STR, Jan. 1–Oct. 3, 2026",
        cols=[["Measure", 0], ["Anaheim+", 1], ["Garden Grove+", 1], ["Anaheim–Garden Grove+", 1]], full=True,
        rows=[["Rooms", f"{A['rooms']:,}", f"{G['rooms']:,}", f"{AG['rooms']:,}"],
              ["Occupancy", f"{A['occ']:.1f}%", f"{G['occ']:.1f}%", f"{AG['occ']:.1f}%"],
              ["Average nightly rate", f"${A['adr']:.0f}", f"${G['adr']:.0f}", f"${AG['adr']:.0f}"],
              ["Revenue per available room", f"${A['revpar']:.0f}", f"${G['revpar']:.0f}", f"${AG['revpar']:.0f}"],
              ["Group share of rooms sold", f"{A['group_share']:.1f}%", f"{G['group_share']:.1f}%", f"{AG['group_share']:.1f}%"],
              ["Nights at 90%+ occupancy", f"{A['n90']}", f"{G['n90']}", f"{AG['n90']}"]], hi=1, src=SRC_STR))
    dl, an = ND.CS_MO["Disneyland"], ND.CS_MO["Anaheim"]
    h["tables"].append(dict(title="Resort area vs. the rest of Anaheim, by month, 2026", sub="CoStar Disneyland and Anaheim submarkets; change is revenue per available room vs. the same month of 2025",
        cols=[["Month", 0], ["Disneyland occupancy", 1], ["Disneyland rate", 1], ["Anaheim occupancy", 1], ["Anaheim rate", 1], ["Anaheim change", 1]], full=True,
        rows=[[MON[i], f"{dl['occ'][i]*100:.1f}%", f"${dl['adr'][i]:.0f}", f"{an['occ'][i]*100:.1f}%", f"${an['adr'][i]:.0f}", D(an['rchg'][i]*100, sp(an['rchg'][i]*100))] for i in range(8)],
        hi=6, src=SRC_CSM))
    h["charts"].append(dict(kind="bars", title=f"Sunday and Monday nights run {gap:.0f} points below Friday and Saturday", sub="Anaheim+ hotel occupancy by night, Jan. 1–Oct. 3, 2026 (STR)",
        rows=[dict(l=DOWL[d], v=A['dow'][d][0], t=f"{A['dow'][d][0]:.1f}%", hi=d in ("Sun", "Mon")) for d in DOW], src=SRC_STR))
    h["ocv"].append(f"Sunday and Monday are the open nights: Visit Anaheim hotels ran {ND.SUNMON_OCC:.1f}% occupancy on those nights in 2026 vs. {ND.FRISAT_OCC:.1f}% on Fridays and Saturdays (STR). Each point OC Vibe adds on Sunday and Monday nights is about {round(ND.PT_SUNMON_RN, -2):,.0f} room nights and ${ND.PT_SUNMON_REV/1e6:.1f}M in room revenue a year.")
    h["ocv"].append(f"The rest of Anaheim (CoStar's Anaheim submarket) averages ${an['adr12']:.0f} a night vs. ${dl['adr12']:.0f} in the resort area. Where OC Vibe's hotels price between those two will drive their revenue more than occupancy.")
    h["notes"].append(f"STR hotel sets: groups filled {A['group_share']:.1f}% of rooms sold at Anaheim+ hotels in 2026 at ${A['group_adr']:.0f} a night; leisure and other transient guests filled {A['trans_share']:.1f}% at ${A['trans_adr']:.0f}.")

    # ---------- Visitor spending: Visa ----------
    v = ND.VISA
    s = sec["p-spend"]
    s["tables"].append(dict(title="Visitor card spending, August 2026", sub="Visa cardholders visiting; change vs. August 2025",
        cols=[["Measure", 0], ["Total", 1], ["Domestic", 1], ["International", 1]], full=True,
        rows=[["Spending", f"${v['total']}M", f"${v['dom']}M", f"${v['intl']}M"],
              ["Change vs. Aug. 2025", D(v['total_chg'], sp(v['total_chg'])), D(v['dom_chg'], sp(v['dom_chg'])), D(v['intl_chg'], sp(v['intl_chg']))],
              ["Cards", f"{v['cards']}M", "5.3M", "143.8K"], ["Spending per card", f"${v['per_card']}", "$84", f"${v['intl_per_card']}"],
              ["Average transaction", f"${v['ticket']}", "$42", "$59"]], hi=0, src=SRC_VISA))
    s["ocv"].append(f"Visitor card spending reached ${v['total']}M in August 2026, up {v['total_chg']}% (Visa). Spending per card rose {v['per_card_chg']}% to ${v['per_card']}, so each visitor is spending more, the same pattern Tourism Economics shows.")
    # ---------- Who visits: Visa origins + international ----------
    d5 = sec["p-d5"]
    d5["tables"].append(dict(title="Where visitor card spending comes from, August 2026", sub="Visa: top 15 origin markets (domestic metro areas and countries)",
        cols=[["Origin", 0], ["Spending", 1], ["Share of total", 1]], full=True,
        rows=[[n, f"${x:.1f}M", f"{x/v['total']*100:.1f}%"] for n, x in ND.VISA_ORIG], hi=0, src=SRC_VISA))
    d5["tables"].append(dict(title="International visitor card spending, August 2026", sub="Visa: by category and by country; change vs. August 2025",
        cols=[["Category or country", 0], ["Spending", 1], ["Change", 1]], full=True,
        rows=[[n, f"${x:.1f}M" if x >= 1 else f"${x*1000:,.0f}K", D(c, sp(c))] for n, x, c in ND.VISA_INTL_CAT] +
             [[f"Country: {n}", f"${x:.1f}M" if x >= 1 else f"${x*1000:,.0f}K", ""] for n, x in ND.VISA_INTL_CTRY[:6]], hi=1, src=SRC_VISA))
    d5["ocv"].append(f"New markets: beyond Southern California, the largest visitor spending comes from San Francisco, Seattle, Phoenix, Las Vegas, San Jose, Sacramento, Orlando, New York and Detroit, and internationally from Mexico (${ND.VISA_INTL_CTRY[0][1]}M), Canada and Japan (Visa, Aug. 2026). These are fly-in markets where OC Vibe events can justify a longer trip.")
    d5["ocv"].append("International visitors spent $5.4M on restaurants and dining in August 2026, but that was down 19.1% from a year earlier, while retail rose 9.3% (Visa). Dining is OC Vibe's biggest category and the one to watch with international guests.")

    # ---------- Getting here: rail ----------
    a, m = ND.AMTRAK, ND.METRO
    t = sec["p-transport"]
    t["tables"].append(dict(title="Amtrak passengers at Anaheim (ARTIC), by year", sub="Arrivals and departures, thousands",
        cols=[["Year", 0], ["Passengers (thousands)", 1], ["vs. 2018", 1]], full=True,
        rows=[[str(y), f"{x:.1f}", f"{x/a['yrs'][2018]*100:.0f}%"] for y, x in a["yrs"].items()], hi=6, src=SRC_AMTRAK))
    t["tables"].append(dict(title="Rail service into ARTIC", sub="Amtrak (2024) and Metrolink lines serving Anaheim (Oct.–Dec. 2025)",
        cols=[["Measure", 0], ["Value", 1], ["Detail", 0]], full=True,
        rows=[["Amtrak passengers, 2024", f"{a['pax24']:,}", f"Average trip {a['trip']} miles; average fare ${a['fare']:.2f}; {a['lt100']}% of trips under 100 miles"],
              ["Top Amtrak city pairs", "", ", ".join(a["pairs"])],
              ["People within 25 / 50 miles of the station", f"{a['pop25']/1e6:.1f}M / {a['pop50']/1e6:.1f}M", "Rail Passengers Association"],
              ["Metrolink Orange County Line, weekday riders", f"{m['oc_wk']:,}", f"{sp(m['oc_wk_chg'], 0)} vs. a year earlier; {m['oc_we']:,} weekend riders in the quarter ({sp(m['oc_we_chg'], 0)})"],
              ["Metrolink Inland Empire–Orange County Line, weekday riders", f"{m['ieoc_wk']:,}", f"{sp(m['ieoc_wk_chg'], 0)}; {m['ieoc_we']:,} weekend riders ({sp(m['ieoc_we_chg'], 0)})"],
              ["Metrolink trips that are not commutes", f"{m['noncommute']}%", f"Rider median household income ${m['hhi']:,}; average trip {m['trip']} miles"]],
        hi=0, src=SRC_AMTRAK + "; " + SRC_METRO))
    t["ocv"].append(f"Rail already brings visitors to OC Vibe's front door: {a['pax24']:,} Amtrak passengers used the Anaheim station at ARTIC in 2024 (79% of the 2018 level), mostly on trips under 100 miles from San Diego and Los Angeles. {a['pop50']/1e6:.1f} million people live within 50 miles of the station.")
    t["ocv"].append(f"Metrolink's Orange County Line carries {m['oc_wk']:,} weekday riders and is growing ({sp(m['oc_wk_chg'], 0)}), and {m['noncommute']}% of Metrolink trips are not commutes. Weekend ridership is down, so event-night rail service is a gap to raise with Metrolink and OCTA.")
    t["notes"].append("Rail data are station totals (Amtrak) and line totals (Metrolink); ARTIC station-level Metrolink boardings were not available.")

    # ---------- OC Vibe impact: levers and KPIs ----------
    o = sec["p-ocv"]
    o["tables"][1]["rows"].append(["Each point of Sunday–Monday hotel occupancy citywide", f"About {round(ND.PT_SUNMON_RN, -2):,.0f} room nights", f"About ${ND.PT_SUNMON_REV/1e6:.1f}M room revenue a year (STR Anaheim+, 2026)"])
    kpi = o["tables"][8]["rows"]
    kpi.insert(6, ["Hotel stays", "Sunday–Monday occupancy, Visit Anaheim hotels", f"{ND.SUNMON_OCC:.1f}% (STR, 2026 YTD)", "Narrow the gap to Friday–Saturday (86.2%)", "Visit Anaheim BI (STR)", "Monthly"])
    kpi.insert(10, ["Spending", "Visitor card spending, Anaheim and the OC Vibe area", f"${v['total']}M in Aug. 2026 (citywide view)", "Track the OC Vibe area once mapped", "Visit Anaheim BI (Visa via Symphony)", "Monthly"])
    kpi.insert(11, ["New markets", "Visitor spending from fly-in markets (outside Southern California)", "Seattle, Phoenix, Las Vegas, Orlando, New York, Mexico, Canada", "Grow share year over year", "Visit Anaheim BI (Visa)", "Monthly"])
    kpi.append(["Access", "Rail passengers at ARTIC", f"{a['pax24']:,} Amtrak (2024); Metrolink line totals", "Back to 2018's 256,600", "Amtrak; Metrolink; OCTA", "Annual"])

    order = ["North star", "Visitation", "Length of stay", "Hotel stays", "New markets", "Spending", "Access"]
    kpi.sort(key=lambda r: order.index(r[0]))
    REGISTER.extend(REG_ADD)
    SOURCES.extend([("STR", SRC_STR + "."), ("CoStar submarket export", SRC_CSM + "."), ("Visa Destination Insights", SRC_VISA + "."),
                    ("Amtrak (Rail Passengers Association)", SRC_AMTRAK + "."), ("Metrolink", SRC_METRO + ".")])
    DQ.extend([
      "Visa figures come from Visit Anaheim's Visa Destination Insights view in Symphony; confirm the geography it covers before comparing it with other sources. The two Visitor Type files received are identical.",
      "Amtrak's 2023 count at Anaheim (70,700) is unusually low compared with 2022 and 2024; check it before using it in a trend.",
      "STR and CoStar measure different hotel sets (Visit Anaheim sets vs. CoStar submarkets) and should not be compared directly.",
    ])
    TAKEAWAYS.append(f"Hotels near OC Vibe have room on Sunday and Monday nights ({ND.SUNMON_OCC:.1f}% occupancy vs. {ND.FRISAT_OCC:.1f}% Friday–Saturday, STR 2026), and visitor card spending rose {v['total_chg']}% in August 2026 (Visa); rail at ARTIC carried {a['pax24']:,} Amtrak passengers in 2024.")
