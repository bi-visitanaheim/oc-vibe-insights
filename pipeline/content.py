"""OC Vibe edition: content for the dashboard and deck. Audience: OC Vibe (external partner of Visit Anaheim)."""
from data import *

def num(v): return f"{v:,.0f}"
A, G, O = EI["Anaheim"], EI["Garden Grove"], EI["Orange County"]
lq = LARC_Q
q2pv, q2pv_ly = 1.76e3 / 6.74, 1.63e3 / 6.55
q2pv_chg = pct(q2pv, q2pv_ly)
SRC.update({
  "adt": "Orange County Transportation Authority (OCTA), 2026 Traffic Flow Map (published Aug. 2026; weekday average daily traffic)",
  "gtfs": "OCTA bus schedules (GTFS), service Aug. 9–Nov. 7, 2026; Visit Anaheim BI analysis",
  "datafy": "Datafy, Anaheim visitor report, calendar 2024 (visitors traveling 50+ miles; employees excluded)",
  "tet": "U.S. Bureau of Transportation Statistics, Transportation Economic Trends, Tables 3.1, 3.4 and 6.6 (data 2019–2025; accessed Oct. 12, 2026)",
  "bts": "U.S. Bureau of Transportation Statistics, County Transportation Profile: Orange County, CA (American Community Survey commute data; file provided Oct. 12, 2026; data year not stated in the file)",
})
BTS_SH = {m: v / BTS['workers'] * 100 for m, v in BTS['modes']}
SPYOY = {2023: 7.5, 2024: 2.3, 2025: 3.1, 2026: 5.6, 2027: 2.7, 2028: 3.5}

SECTIONS = []

# ---------- 1. Visitor spending (Tourism Economics Travel Forecast) ----------
SECTIONS.append(dict(
  id="p-spend", tab="Visitor spending",
  q="How much does each visitor spend, and how is that changing?",
  period="Tourism Economics Travel Forecast, Sept. 2026 · Q2 2026 actual",
  ans=f"About ${ANA_PV[6]:.0f} per Anaheim visitor in 2025, rising to about ${ANA_PV[7]:.0f} in 2026 and ${ANA_PV[9]:.0f} by 2028. In Q2 2026, visitors spent $1.76 billion (+7.8%), about ${q2pv:.0f} each (+{q2pv_chg:.1f}%).",
  hv=f"${ANA_PV[6]:.0f}", hl="spent per Anaheim visitor, 2025",
  cards=[
    ["Anaheim, 2025", "Spending per visitor", f"${ANA_PV[6]:.0f}", f"▲ +{A['pv_chg']:.1f}% vs. 2024 · 26.5M visits, $6.8B spent", "Tourism Economics; BI calculation"],
    ["Anaheim, Q2 2026", "Visitor spending", f"${Q['q2_sp']:.2f}B", f"▲ +{Q['q2_sp_chg']}% vs. Q2 2025 · visits ▲ +{Q['q2_vis_chg']}% to 6.74M", "Tourism Economics"],
    ["Anaheim, 2028 forecast", "Spending per visitor", f"${ANA_PV[9]:.0f}", "Visitor spending $7.7B · 27.6M visits", "Tourism Economics (forecast)"],
  ],
  tables=[dict(title="Anaheim visits, spending and spending per visitor", sub="Per visitor = visitor spending ÷ visits (BI calculation from Tourism Economics totals). F = forecast.",
    cols=[["Year",0],["Visits",1],["Day / overnight",1],["Visitor spending",1],["Per visitor",1],["Spending change",1]],
    rows=[[f"{y}{' F' if y>2025 else ''}", f"{v:.1f}M", d_o, f"${s:.1f}B", f"${pv:.0f}", D(SPYOY[y], sp(SPYOY[y]))]
          for y, v, s, pv, d_o in zip(YEARS, ANA_VIS, ANA_SP, ANA_PV, ["16.7M / 7.4M","9.1M / 3.4M","14.0M / 5.9M","16.4M / 8.4M","17.2M / 8.6M","17.7M / 8.6M","17.9M / 8.6M","18.1M / 8.9M","18.3M / 9.0M","18.5M / 9.1M"]) if y >= 2023],
    hi=2, src=SRC["te_fc"]),
    dict(title="Quarterly visitor spending, Anaheim", sub="Per visitor = quarterly spending ÷ quarterly visits (BI calculation).",
    cols=[["Quarter",0],["Visits",1],["Visitor spending",1],["Per visitor",1]],
    rows=[[q, f"{v:.2f}M", f"${s:.2f}B", f"${s*1000/v:.0f}"] for q, v, s in ANA_Q], hi=5, src=SRC["te_fc"]),
    dict(title="Spending per visitor by geography", sub="Garden Grove and Orange County for comparison.",
    cols=[["Geography",0],["2025 visits",1],["2025 spending",1],["Per visitor, 2025",1],["2026 forecast per visitor",1]],
    rows=[["Anaheim","26.5M","$6.83B",f"${A['pv25']:.0f}",f"${ANA_PV[7]:.0f}"],["Garden Grove","3.24M","$769.3M",f"${G['pv25']:.0f}",f"${GG_PV[7]:.0f}"],
          ["Orange County","51.3M","$17.99B","$350","Not forecast"]], hi=0,
    src="Tourism Economics, Economic Impact of Visitors 2025 and Travel Forecast (Sept. 2026). Orange County per-visitor value is published by Tourism Economics; others are BI calculations.")],
  charts=[dict(kind="cols", title=f"Each Anaheim visitor is forecast to spend ${ANA_PV[9]:.0f} by 2028, up from ${ANA_PV[0]:.0f} in 2019",
    sub="Visitor spending per visit, Anaheim. Outlined bars are Tourism Economics forecasts.",
    rows=[dict(l=str(y)+("F" if y>2025 else ""), v=pv, t=f"${pv:.0f}", fc=y>2025, hi=y==2025) for y, pv in zip(YEARS, ANA_PV)], src=SRC["te_fc"])],
  notes=["What it means for OC Vibe: spending per visitor is rising faster than visits (Tourism Economics forecasts visitor spending +4.1% a year to 2028 ($6.83B to $7.7B) vs. visits +1.4% (26.5M to 27.6M)), so growth comes from higher-value, longer stays rather than more day trips.",
         "Overnight visits are growing faster than day visits (Q2 2026: +4.5% vs. +2.1%); Tourism Economics expects overnight visits to grow 1.9% a year through 2028.",
         f"International visits to Anaheim and Garden Grove: {INTL['v2026']/1e6:.2f} million forecast for 2026 (+{INTL['v_chg']}%), spending ${INTL['s2026']/1000:.2f} billion; Mexico leads growth (+{INTL['mex_v_chg']}%).",
         "U.S. context (Tourism Economics, Sept. 2026): consumer spending is increasingly carried by higher-income households; the Federal Reserve is expected to hold rates until Q3 2027.",
         "Spending per visitor is a BI calculation from rounded Tourism Economics totals, so treat values as approximate (±$5)."],
))

# ---------- 2. Jobs and economy (TE regional economic impact) ----------
SECTIONS.append(dict(
  id="p-impact", tab="Jobs and economy",
  q="What does the visitor economy support in Anaheim, Garden Grove and Orange County?",
  period="Calendar 2025 vs. 2024 · Tourism Economics regional reports",
  ans=f"Visitors supported {num(A['jobs'])} jobs in Anaheim (one in three), {num(G['jobs'])} in Garden Grove and {num(O['jobs'])} countywide in 2025. Food and beverage holds {A['fb_job_share']:.1f}% of those jobs in Anaheim, {G['fb_job_share']:.1f}% in Garden Grove and {O['fb_job_share']:.1f}% countywide.",
  hv=num(A['jobs']), hl="Anaheim jobs supported, 2025",
  cards=[
    ["Anaheim", "Jobs supported by visitors", num(A['jobs']), f"{A['jobs_share']}% of all jobs · F&B {A['fb_job_share']:.1f}%", "Tourism Economics"],
    ["Garden Grove", "Jobs supported by visitors", num(G['jobs']), f"{G['jobs_share']}% of all jobs · F&B {G['fb_job_share']:.1f}%", "Tourism Economics"],
    ["Orange County", "Jobs supported by visitors", num(O['jobs']), f"{O['jobs_share']}% of all jobs · F&B {O['fb_job_share']:.1f}%", "Tourism Economics"],
  ],
  tables=[dict(title="Regional economic impact of visitors, 2025", sub="Food and beverage (F&B) share = F&B jobs ÷ all visitor-supported jobs (direct, indirect and induced).",
    cols=[["Geography",0],["Visitor spending",1],["Total economic impact",1],["Jobs supported",1],["F&B jobs",1],["F&B share of jobs",1],["F&B share of spending",1],["State & local taxes",1]],
    rows=[[g, f"${e['sp25']/1000:.2f}B" if e['sp25']>=1000 else f"${e['sp25']:.1f}M", f"${e['impact']/1000:.1f}B", num(e['jobs']), num(e['fb_jobs']), f"{e['fb_job_share']:.1f}%", f"{e['fb_share']:.1f}%",
           f"${e['sl_tax']/1000:.2f}B" if e['sl_tax']>=1000 else f"${e['sl_tax']:.1f}M"] for g, e in EI.items()],
    hi=0, src=SRC["te_ei"] + ". Shares are BI calculations."),
    dict(title="Visitor spending by category, 2025", sub="Share of visitor spending",
    cols=[["Category",0],["Anaheim",1],["Garden Grove",1],["Orange County",1]],
    rows=[["Recreation", "34.0%", "6.4%", "22.0%"], ["Lodging", "25.2%", "33.0%", "25.9%"], ["Retail", "21.9%", "22.6%", "20.5%"], ["Food & beverage", "15.6%", "32.0%", "27.6%"], ["Transportation", "3.3%", "6.1%", "3.9%"]],
    hi=3, src=SRC["te_ei"])],
  charts=[dict(kind="bars", title="Food and beverage is a larger share of tourism jobs outside the resort district",
    sub="Food and beverage jobs as a share of all visitor-supported jobs, 2025", rows=[dict(l=g, v=e['fb_job_share'], t=f"{e['fb_job_share']:.1f}%", hi=g=="Anaheim") for g, e in EI.items()], src=SRC["te_ei"])],
  notes=["What it means for OC Vibe: its 172,000 sq ft of planned restaurant and dining space sits in the category with the fastest visitor spending growth in 2025 (food and beverage +5.5% in Anaheim, +5.6% countywide).",
         "In Anaheim, recreation and entertainment is the largest tourism employer (28,970 jobs), reflecting the theme parks and venues; food and beverage is second (11,366).",
         "Garden Grove's economic impact report shows visitor spending flat at $769.3 million in 2025; its forecast report shows $767.4 million. Values differ slightly between Tourism Economics releases.",
         "Note on sources: the Anaheim and Garden Grove Travel Forecast does not include jobs or spending by category; these come from Tourism Economics' 2025 economic impact reports for each geography."],
))

# ---------- 3. One more night ----------
SECTIONS.append(dict(
  id="p-night", tab="One more night",
  q="What is one more night per visitor worth to Anaheim?",
  period="Scenario based on 2025 visitors, spending and length of stay",
  ans=f"About ${N['lodge_night']/1e6:.0f} million in added lodging spending if every visitor stayed one more night. Counting all trip spending by overnight visitors, the figure is about ${N['overnight_only']/1e9:.2f} billion; the original study's all-visitor ceiling is ${N['plus1']/1e9:.2f} billion.",
  hv=f"${N['lodge_night']/1e6:.0f}M", hl="one more night of lodging spending",
  cards=[
    ["One more night (headline)", "Added lodging spending", f"${N['lodge_night']/1e6:.0f}M", "$1.72B lodging spending ÷ 2.17-day average stay", "BI calculation; Tourism Economics; Azira"],
    ["Overnight visitors only", "Added spending, all categories", f"${N['overnight_only']/1e9:.2f}B", f"8.6M overnight visitors × ${N['per_visitor_day']:.0f} per visitor-day", "BI calculation"],
    ["Upper bound", "All visitors, all categories", f"${N['plus1']/1e9:.2f}B", "Extra Night deck method; adds a day for day-trippers too", "BI calculation"],
  ],
  tables=[dict(title="How the one-more-night estimate is built", sub="2025 inputs. Weighted average stay blends domestic and international stays.",
    cols=[["Step",0],["Value",1],["Basis",0]],
    rows=[["Visitors, 2025", "26.5M", "Tourism Economics"], ["Domestic / international share", f"{N['dom_share']*100:.1f}% / {N['intl_share']*100:.1f}%", "24.7M ÷ 26.5M"],
          ["Average stay, domestic / international", "1.9 / 5.9 days", "Azira location data"], ["Weighted average stay", f"{N['los']:.2f} days", "93.2% × 1.9 + 6.8% × 5.9"],
          ["Lodging spending, 2025", "$1.72B", "Tourism Economics (all accommodation types)"], ["One more night of lodging", f"${N['lodge_night']/1e6:.0f}M", "$1.72B ÷ 2.17 days"],
          ["Total visitor spending, 2025", "$6.83B", "Tourism Economics"], ["Spending per visitor-day", f"${N['per_visitor_day']:.2f}", "$6.83B ÷ (26.5M × 2.17)"],
          ["One more day, overnight visitors only", f"${N['overnight_only']/1e9:.2f}B", "8.6M × spending per visitor-day"], ["One more day, every visitor (upper bound)", f"${N['plus1']/1e9:.2f}B", "$6.83B ÷ 2.17"]],
    hi=5, src=SRC["night"]),
    dict(title="Group business booked with TID incentives", sub="Events and room nights contracted with Tourism Improvement District incentives, by event year; 2026 onward are future events on the books.",
    cols=[["Event year",0],["Events",1],["Room nights",1],["Attendees",1]],
    rows=[[str(y), str(e), num(r), num(a)] for y, e, r, a, c in TID], hi=4, src=SRC["tid"])],
  charts=[dict(kind="bars", title="One more night is worth about $0.8 billion in lodging alone",
    sub="Added spending under each scenario, $ billions (estimates)",
    rows=[dict(l="Lodging only (headline)", v=N['lodge_night']/1e9, t=f"${N['lodge_night']/1e9:.2f}B", hi=True), dict(l="Overnight visitors, all spending", v=N['overnight_only']/1e9, t=f"${N['overnight_only']/1e9:.2f}B"),
          dict(l="Half a day, all visitors", v=N['plus_half']/1e9, t=f"${N['plus_half']/1e9:.2f}B"), dict(l="Full day, all visitors", v=N['plus1']/1e9, t=f"${N['plus1']/1e9:.2f}B")],
    src="Visit Anaheim BI calculation (Oct. 12, 2026) from Tourism Economics 2025 and Azira inputs")],
  notes=["What it means for OC Vibe: evening events at Honda Center and the new concert hall, plus 550 planned hotel rooms, are the kind of draws that turn a day trip into an overnight stay or add a night to an existing one.",
         "Why $0.8 billion is the headline: a night is mainly a lodging decision, and the lodging-only figure matches the earlier BI callout (“half a night longer = $750 million”, built on 2025 forecast inputs).",
         "The $3.15 billion figure from the original Extra Night deck assumes all 26.5 million visitors, including 17.9 million day visitors, add a full day at average spending. Treat it as a ceiling, not a forecast.",
         "All values are estimates that hold spending per day constant."],
  warn="Estimate. These are scenarios, not forecasts.",
))

# ---------- 4. Getting here ----------
SECTIONS.append(dict(
  id="p-transport", tab="Getting here",
  q="How do people get to OC Vibe, and what transportation changes are coming?",
  period="OCTA traffic map Aug. 2026 · OCTA bus schedules Aug.–Nov. 2026 · Azira Aug. 2026",
  ans=f"Mostly by car on short trips: SR-57 beside the district carries about 275,000 vehicles a day and Ball Road about 54,000. ARTIC sees {TRANSIT['wk']} OCTA bus trips stopping on a weekday, with {TRANSIT['resort_trips_wk']} one-seat rides to the Disneyland Resort area in about 13 minutes. {GEO['lt50']}% of domestic trips to Anaheim and Garden Grove start within 50 miles.",
  hv="275K", hl="vehicles a day on SR-57 at OC Vibe",
  cards=[
    ["SR-57 beside OC Vibe", "Vehicles per weekday", "275,000", "Ball Rd to Katella Ave · I-5 at the resort: 299,000", "OCTA Traffic Flow Map (Caltrans 2024)"],
    ["ARTIC bus service", "Weekday bus trips stopping at ARTIC", f"{TRANSIT['wk']}", f"3 routes · about one every 3–4 minutes at peak · Sat. {TRANSIT['sat']}, Sun. {TRANSIT['sun']}", "OCTA bus schedules; BI analysis"],
    ["Visitor origin", "Domestic trips from within 50 miles", f"{GEO['lt50']}%", f"50–249 miles: {GEO['d50_249']}% · Aug. 2026", "Azira via Symphony"],
  ],
  tables=[dict(title="Daily traffic on roads serving OC Vibe", sub="Weekday average daily traffic (thousands of vehicles). Freeway volumes are Caltrans 2024; arterial counts are dated as shown.",
    cols=[["Road segment",0],["Vehicles per day",1],["Count year",0]],
    rows=[[n, f"{v}K", c] for n, v, c in ADT], hi=0, src=SRC["adt"]),
    dict(title="OCTA bus service at ARTIC", sub="Weekday, Saturday and Sunday bus trips stopping at ARTIC (both directions; 227 of the 277 weekday trips continue on, 50 end there). Excludes the seasonal OC Fair Express.",
    cols=[["Route",0],["Corridor",0],["Weekday",1],["Saturday",1],["Sunday",1]],
    rows=[[k, v[0], str(v[1]), str(v[2]) if v[2] else "—", str(v[3]) if v[3] else "—"] for k, v in TRANSIT['routes'].items()] + [["All", "ARTIC total", str(TRANSIT['wk']), str(TRANSIT['sat']), str(TRANSIT['sun'])]],
    hi=3, src=SRC["gtfs"]),
    dict(title="Transportation projects that affect access to OC Vibe", sub="As reported by LARC (Sept. 2026).",
    cols=[["Project",0],["Status",0],["Timing",0]],
    rows=[["ARTIC–Disneyland Resort transit link", "City studying gondola, trackless streetcar or autonomous vehicles (gondola up to $11M per mile)", "Goal: in place for the 2028 Olympics"],
          ["OC Streetcar (Santa Ana–Garden Grove)", "Daytime testing since April 2026; contractor lawsuit pending", "Full service targeted by end of 2026; Anaheim extension speculative"],
          ["California High-Speed Rail (ARTIC–Union Station–San Francisco)", "Central Valley segment under construction", "Central Valley service 2033; full corridor as late as 2040"],
          ["John Wayne Airport", "Passengers +3% in 2025, +4% Jan.–Apr. 2026; $700M terminal upgrade (no added capacity)", "Upgrade by 2031"],
          ["DisneylandForward 6,000-space parking structure", "Permits filed Oct. 2025", "Construction expected to begin 2026"]],
    hi=-1, src=SRC["larc"]),
    dict(title="How Orange County residents get to work", sub="Workers 16 and over (1,565,842); shares are BI calculations",
    cols=[["Means of transportation",0],["Workers",1],["Share",1]],
    rows=[[m, num(v), f"{BTS_SH[m]:.1f}%"] for m, v in BTS['modes']], hi=0, src=SRC["bts"]),
    dict(title="Cost of getting here: national transportation cost trends", sub="Annual averages, current dollars. West Coast gasoline covers California and neighboring states.",
    cols=[["Year",0],["Gasoline, West Coast ($/gal)",1],["Gasoline, U.S. ($/gal)",1],["Domestic airfare",1],["Car cost per mile",1]],
    rows=[[str(y), f"${TET_GAS[y][1]:.2f}", f"${TET_GAS[y][0]:.2f}", f"${TET_AIR[y]:.0f}", f"${TET_AUTO[y]:.2f}" if y in TET_AUTO else "—"] for y in range(2019, 2026)],
    hi=6, src=SRC["tet"])],
  charts=[dict(kind="bars", title="SR-57 carries five times the traffic of any arterial next to OC Vibe", sub="Weekday vehicles per day, thousands",
    rows=[dict(l=n.split(",")[0] if "SR-57 (" in n else n, v=v, t=f"{v}K", hi=i==0) for i, (n, v, c) in enumerate(ADT[:1] + ADT[4:8])], src=SRC["adt"]),
    dict(kind="img", title="2026 traffic flow around OC Vibe and ARTIC", sub="Excerpt of the OCTA 2026 Traffic Flow Map. Numbers are thousands of vehicles per weekday; Roman numerals show how many years before 2026 a count was taken.",
    src=SRC["adt"], img="adt_ocvibe.jpg")],
  notes=[f"Transit: Route 50 (Katella Ave) reaches the Katella/Harbor resort area from ARTIC in about {TRANSIT['resort_min_50']} minutes and Route 553 in about {TRANSIT['resort_min_553']}. Weekend one-seat service to the resort drops to {TRANSIT['resort_trips_sat']} trips on Saturday (Route 553 does not run). The single-ride bus fare is ${TRANSIT['fare']:.2f}.",
         f"Late events: {TRANSIT['late_wk']} weekday bus trips stop at ARTIC after 10 p.m. (11 leaving, 5 ending there); the last departure is at {TRANSIT['last_wk']}. The bus data does not include Metrolink or Amtrak trains, which also serve ARTIC.",
         "The 2026 traffic map repeats older counts near OC Vibe: freeway volumes are from 2024, and Katella Ave next to the district was last counted in 2021. New counts before OC Vibe's 2027 openings would set a clean baseline.",
         f"Cost trends (BTS): driving a car cost ${TET_AUTO[2024]:.2f} per mile in 2024, up {pct(TET_AUTO[2024], TET_AUTO[2019]):.0f}% from 2019; West Coast gasoline averaged ${TET_GAS[2025][1]:.2f} in 2025, about $1 above the U.S.; domestic airfares averaged ${TET_AIR[2025]:.0f} (+{pct(TET_AIR[2025], TET_AIR[2019]):.0f}% since 2019). LARC and Tourism Economics note gas prices spiked again in spring 2026, which weighs most on drive-market visitors.",
         f"County context (BTS): {BTS_SH['Drove alone']:.1f}% of Orange County workers drive alone and {BTS_SH['Public transportation']:.1f}% use public transportation; {BTS['hh_noveh']/BTS['hh']*100:.1f}% of households ({num(BTS['hh_noveh'])}) have no vehicle. The county has one medium-hub airport (John Wayne), 68 miles of passenger rail track and 1,181 bridges (2.8% in poor condition).",
         f"Drive market and air (CoStar): about {CS_ECON['drive_mkt']} million people live within 90 miles, which makes driving the main way visitors arrive. John Wayne Airport handled a record {CS_ECON['sna_23']} million passengers in 2023 and {CS_ECON['sna_24']} million in 2024, on 13 commercial airlines.",
         "Source note: the 2026 ADT file is OCTA's Traffic Flow Map, not Visit California data. Tourism Economics transportation impact data has not been received yet."],
))

# ---------- 5. Who visits (Symphony POI + Datafy + domestic geography) ----------
SECTIONS.append(dict(
  id="p-d5", tab="Who visits",
  q="Who visits District 5 and the OC Vibe area, and where do they come from?",
  period="Symphony (Azira) Jan.–May 2026 · Datafy calendar 2024",
  ans=f"District 5 visitors are mostly overnight guests ({D5['overnight']}%), {D5['new']}% are first-time visitors, and their median household income is ${D5['hhi']}K. Datafy shows the OC Vibe area already captured {DATAFY['clusters'][5][1]}% of Anaheim visitor days in 2024, ahead of meeting services.",
  hv=f"{D5['overnight']}%", hl="of District 5 visitors stay overnight",
  cards=[
    ["District 5, Jan.–May 2026", "Stay overnight", f"{D5['overnight']}%", f"New visitors {D5['new']}% · sample {num(D5['sample'])} devices", "Azira via Symphony"],
    ["District 5, Jan.–May 2026", "Median household income", f"${D5['hhi']}K", f"All Anaheim/Garden Grove visitors, Aug. 2026: ${GEO['hhi']}K", "Azira; U.S. Census Bureau"],
    ["OC Vibe area, 2024", "Share of Anaheim visitor days", f"{DATAFY['clusters'][5][1]}%", "Meeting services: 3.4% · Disneyland: 74.4%", "Datafy"],
  ],
  tables=[dict(title="Where District 5 visitors come from", sub="Share of domestic unique visitors, Jan.–May 2026",
    cols=[["Metro area",0],["Share",1]], rows=[[s, f"{v:.1f}%"] for s, v in D5_MSA], hi=0, src=SRC["poi"]),
    dict(title="Top origin states, District 5", sub="Share of domestic unique visitors", cols=[["State",0],["Share",1]], rows=[[s, f"{v:.1f}%"] for s, v in D5_STATE], hi=0, src=SRC["poi"]),
    dict(title="Anaheim visitor profile (Datafy, 2024)", sub="Visitors traveling 50+ miles", cols=[["Measure",0],["Value",1]],
    rows=[["Overnight share of visitor days", f"{DATAFY['overnight']}%"], ["Stays of 6+ days (share of visitor days)", f"{DATAFY['los6']}%"], ["Repeat visitors", f"{DATAFY['repeat']}%"],
          ["Top state: California", "51.2%"], ["Top metro: Los Angeles", "15.5%"], ["Household income $100K+", f"{DATAFY['inc100']}%"], ["Age 45–64", f"{DATAFY['age45_64']}%"]], hi=-1, src=SRC["datafy"]),
    dict(title="District 5 visits by day of week", sub="Share of total visits", cols=[["Day",0],["Share",1]], rows=[[d, f"{v:.1f}%"] for d, v in D5_DOW], hi=5, src=SRC["poi"])],
  charts=[dict(kind="bars", title="District 5 visitors also go to Districts 3, 6 and 4 and the Anaheim Resort", sub="Share of District 5 visitors who also visited each area, Jan.–May 2026",
    rows=[dict(l=n, v=v, t=f"{v:.1f}%", hi=i==4) for i, (n, v) in enumerate(D5_POI[:10])], src=SRC["poi"]),
    dict(kind="bars", title="OC Vibe already registers in Anaheim visitor activity", sub="Share of Anaheim visitor days that include each cluster, 2024 (a visitor day can include several clusters)",
    rows=[dict(l=n, v=v, t=f"{v}%", hi=n=="OC Vibe") for n, v in DATAFY['clusters']], src=SRC["datafy"])],
  notes=["What it means for OC Vibe: 13.7% of District 5 visitors also visit the Anaheim Resort and 8.4% the Disneyland Resort, which supports a resort–OC Vibe connection (see the transit link study under Getting here).",
         "Saturday (15.9%) and Sunday (15.3%) are the busiest days for District 5 visits.",
         "Virginia (4.2%) and the Washington, D.C. metro (3.6%) rank unusually high; this may reflect a group event or the device sample, so confirm before citing.",
         "Overnight and new-visitor shares count visitors who stayed 4+ hours, are not commuters and live 50+ miles away (Symphony definition). Datafy covers calendar 2024 and uses a different device panel than Symphony.",
         "District 5 geography is as defined in Symphony; Datafy's OC Vibe cluster is Datafy's own boundary."],
))

# ---------- 6. Marketing reach (media attribution) ----------
SECTIONS.append(dict(
  id="p-media", tab="Marketing reach",
  q="Does Visit Anaheim's marketing bring visitors who can reach OC Vibe?",
  period="Ad exposures Jan. 1–Aug. 31, 2026 · U.S. audiences",
  ans=f"Yes. Visit Anaheim's paid media produced {MED['impr']/1e6:.1f} million measurable impressions and {num(MED['visits'])} observed visits to Anaheim, {MED['per1k']} visits per 1,000 impressions, with visitors arriving about {MED['days']:.0f} days after seeing an ad.",
  hv=num(MED['visits']), hl="observed visits after ad exposure",
  cards=[
    ["All campaigns", "Measurable impressions", f"{MED['impr']/1e6:.1f}M", "U.S. audiences, Jan.–Aug. 2026", "Azira attribution via Symphony"],
    ["All campaigns", "Observed visits", num(MED['visits']), f"{MED['per1k']} per 1,000 impressions · visit rate {MED['rate']}%", "Azira attribution via Symphony"],
    ["Luxury campaign", "Best visit rate", "34.4", "visits per 1,000 impressions", "Azira attribution via Symphony"],
  ],
  tables=[dict(title="Visit rate by campaign", sub="Impressions and visits in thousands",
    cols=[["Campaign",0],["Channel",0],["Impressions (K)",1],["Visits (K)",1],["Visits per 1,000",1]],
    rows=[[c, v, f"{i:,.1f}", f"{o:,.1f}", f"{r:.1f}"] for c, v, i, o, r in MED_CAMP], hi=6, src=SRC["media"])],
  charts=[dict(kind="bars", title="Luxury and travel-planning placements convert best", sub="Visits per 1,000 impressions, top campaigns",
    rows=[dict(l=f"{c} · {v.split(' (')[0]}", v=r, t=f"{r:.1f}", hi=i==0) for i, (c, v, im, o, r) in enumerate(sorted(MED_CAMP, key=lambda x: -x[4])[:6])], src=SRC["media"])],
  notes=["What it means for OC Vibe: Visit Anaheim's campaigns reach high-income and luxury audiences that convert well (34.4 visits per 1,000 impressions); OC Vibe events and venues could be featured in this content.",
         "Observed visits are counted once per visitor, on the first visit at least three days after exposure.",
         "Campaign-to-district visit shares in the source export could not be matched reliably and are not shown."],
))

# ---------- 7. Hotel market (CoStar) ----------
co, dl, cp, ce = CS_OC, CS_DL, CS_PROF, CS_ECON
SRC.update({"costar": "CoStar Group, Hospitality Market, Submarket (Disneyland) and Capital Markets reports for Orange County, CA, pulled Oct. 12, 2026 (data through Aug. 2026). © 2026 CoStar Group, licensed to Visit Anaheim."})
SECTIONS.append(dict(
  id="p-hotel", tab="Hotel market",
  q="How are hotels around OC Vibe performing, and is there room for more?",
  period="CoStar, data through Aug. 2026",
  ans=f"Demand is strong and new supply is scarce. Hotels in CoStar's Disneyland submarket, the county's largest at {CS_SUB[0][1]:,} rooms, filled {CS_SUB[0][2]}% of rooms over the past 12 months at ${CS_SUB[0][4]:.0f} a night. Revenue per available room is up {dl['ytd_revpar_chg']}% so far in 2026. Only {co['uc_rooms']} rooms are under construction countywide ({co['uc_pct']}% of supply), which leaves room for OC Vibe's planned hotels.",
  hv=f"{CS_SUB[0][2]}%", hl="Disneyland submarket hotel occupancy, past 12 months",
  cards=[
    ["Disneyland submarket, 12 months", "Hotel occupancy", f"{CS_SUB[0][2]}%", f"▲ +{CS_SUB[0][3]}% · Orange County {co['occ']}%", "CoStar"],
    ["Disneyland submarket, 2026 YTD", "Revenue per available room", f"${dl['ytd_revpar']:.0f}", f"▲ +{dl['ytd_revpar_chg']}% vs. 2025 · Orange County ▲ +{co['ytd_revpar_chg']}%", "CoStar"],
    ["Orange County, under construction", "New hotel rooms", f"{co['uc_rooms']}", f"{co['uc_props']} hotels · {co['uc_pct']}% of {co['rooms']:,} rooms, through 2028", "CoStar"],
    ["Orange County hotels, 12 months", "F&B share of hotel revenue", f"{cp['oc_fb']}%", f"Disneyland submarket {cp['dl_fb']}% · food revenue per room ▲ +{cp['dl_food_chg']}%", "CoStar (hotel sample)"],
  ],
  tables=[dict(title="Hotel performance by Orange County submarket", sub="Trailing 12 months through Aug. 2026; change vs. prior 12 months",
    cols=[["Submarket",0],["Rooms",1],["Occupancy",1],["Average nightly rate",1],["Revenue per available room",1],["Change",1]],
    rows=[[n, f"{r:,}", f"{o:.1f}%", f"${a:.0f}", f"${rv:.0f}", D(rc, sp(rc))] for n, r, o, oc, a, ac, rv, rc, uc in CS_SUB] +
         [["Orange County total", f"{co['rooms']:,}", f"{co['occ']:.1f}%", f"${co['adr']}", f"${co['revpar']}", D(co['revpar_chg'], sp(co['revpar_chg']))]],
    hi=0, src=SRC["costar"]),
    dict(title="Disneyland submarket hotel performance by year", sub="2026 rates are 33% above 2019; occupancy is still below 2019",
    cols=[["Year",0],["Occupancy",1],["Average nightly rate",1],["Revenue per available room",1],["Change",1]],
    rows=[[y, f"{o:.1f}%", f"${a:.2f}", f"${r:.2f}", D(c, sp(c))] for y, o, a, r, c in CS_DL_YR], hi=5, src=SRC["costar"]),
    dict(title="Hotels under construction in Orange County", sub="All active construction; planned OC Vibe hotels are not yet under construction",
    cols=[["Hotel",0],["Submarket",0],["Rooms",1],["Expected opening",0]],
    rows=[[n, s, f"{r}", d] for n, s, r, d in CS_PIPE], hi=-1, src=SRC["costar"]),
    dict(title="Hotel investment", sub="Sales over the past 12 months and CoStar market pricing",
    cols=[["Measure",0],["Disneyland submarket",1],["Orange County",1]],
    rows=[["Sales volume, past 12 months", f"${dl['sales_12']}M ({dl['sales_n']} hotels)", f"${co['sales_12']}M ({co['sales_n']} hotels)"],
          ["Three-year annual average", f"${dl['sales_3yr']}M", f"${co['sales_3yr']}M"],
          ["Market cap rate", f"{dl['cap']}%", f"{co['cap']}%"],
          ["Market value per room (CoStar estimate)", f"${dl['ppr_mkt']:,}", f"${co['ppr_mkt']:,}"],
          ["Market value per room, 2030 (CoStar forecast)", f"${dl['ppr_2030']:,}", "$417,009"]],
    hi=-1, src=SRC["costar"]),
    dict(title="Orange County economy", sub="Oxford Economics via CoStar; job growth is the latest year-over-year rate",
    cols=[["Measure",0],["Orange County",1],["U.S.",1]],
    rows=[["Leisure and hospitality jobs", f"{ce['lh_jobs']}K", "—"], ["Leisure and hospitality concentration (U.S. = 1.0)", f"{ce['lh_lq']}", "1.0"],
          ["Leisure and hospitality job growth", f"+{ce['lh_gr']}%", f"+{ce['lh_gr_us']}%"], ["Leisure and hospitality, 5-year forecast (a year)", f"+{ce['lh_fc']}%", f"+{ce['lh_fc_us']}%"],
          ["Total job growth", f"+{ce['tot_gr']}%", f"+{ce['tot_gr_us']}%"], ["Median household income", f"${ce['hhi']:,}", f"${ce['hhi_us']:,}"],
          ["Unemployment rate", f"{ce['unemp']}%", f"{ce['unemp_us']}%"], ["Population (12-month change)", f"{ce['pop']/1e6:.2f}M ({sp(ce['pop_chg'])})", "+0.2%"]],
    hi=2, src="Oxford Economics, via CoStar Hospitality Market Report (Oct. 12, 2026)")],
  charts=[dict(kind="bars", title="Revenue per available room by submarket, past 12 months", sub="Orange County submarkets, trailing 12 months through Aug. 2026",
    rows=[dict(l=n.replace(" (outside Disneyland submarket)", ""), v=rv, t=f"${rv:.0f}", hi=(n == "Disneyland")) for n, r, o, oc, a, ac, rv, rc, uc in sorted(CS_SUB, key=lambda x: -x[6])] +
         [dict(l="Orange County", v=co['revpar'], t=f"${co['revpar']}")], src=SRC["costar"])],
  notes=[f"What it means for OC Vibe: the hotels nearest the resort run the county's highest occupancy ({CS_SUB[0][2]}%), and construction is limited by financing costs and entitlements. CoStar expects supply to grow only {co['uc_pct']}% through 2028. That supports demand for OC Vibe's planned 550 rooms.",
         f"Food and beverage is a growing part of hotel revenue. Over the past 12 months, Disneyland submarket hotels earned {cp['dl_fb']}% of revenue from food and beverage, and food revenue per available room rose {cp['dl_food_chg']}%. Countywide the share is {cp['oc_fb']}%. Labor is the largest cost: {cp['dl_labor']}% of revenue in the Disneyland submarket.",
         f"Leisure and hospitality is a specialty of the county: {ce['lh_jobs']}K jobs, 1.3 times the U.S. concentration, growing +{ce['lh_gr']}% vs. +{ce['lh_gr_us']}% nationally. Median household income is ${ce['hhi']:,}, 43% above the U.S. CoStar describes a drive market of {ce['drive_mkt']} million people within 90 miles.",
         f"Costs: California's minimum wage is ${ce['min_wage']:.2f} (2025), and Anaheim's resort-area living-wage ordinance brought covered Disney wages to ${ce['disney_wage']:.2f} in 2025.",
         f"Conventions, as cited by CoStar from Visit Anaheim: {ce['acc_events26']} events secured for 2026, projected at about ${ce['acc_eis26']} billion in economic impact and nearly 600,000 hotel room nights.",
         "Investment: hotel sales slowed with higher borrowing costs. In May 2026 a 352-room hotel at 101 E. Katella Ave. sold for $78.75 million ($223,722 per room). CoStar notes that the OC Vibe district could create opportunities for future hotel investment.",
         "CoStar describes OC Vibe as a $4 billion project with full buildout targeted by 2028. LARC reports $5 billion with a final phase by 2033. OC Vibe's own figures should be used.",
         "CoStar's \"Disneyland\" and \"Anaheim\" submarkets split the city's hotels. The exact boundary around OC Vibe could not be confirmed from the CoStar map."],
))

# ---------- 8. OC Vibe outlook (LARC) ----------
SECTIONS.append(dict(
  id="p-larc", tab="OC Vibe outlook",
  q="What in the hotel and market outlook will affect OC Vibe?",
  period="LARC Market Intelligence Reports, Jan.–Sept. 2026",
  ans=f"Strong tailwinds: Anaheim hotel revenue per available room rose {lq['q2_revpar']}% in Q2 2026 (U.S. +{lq['us_q2']}%), convention bookings pace +12% for 2026 and +17% for 2027, and the 2028 Olympics bring events to Anaheim. Watch rising costs: Anaheim inflation of about 3.2% a year and labor costs of about 6% a year.",
  hv=f"+{lq['q2_revpar']}%", hl="Anaheim hotel revenue per room, Q2 2026",
  cards=[
    ["Anaheim market, Q2 2026", "Revenue per available room", f"▲ +{lq['q2_revpar']}%", f"Rate ▲ +{lq['q2_adr']}% · occupancy ▲ +{lq['q2_occ']}% · U.S. ▲ +{lq['us_q2']}%", "LARC"],
    ["Anaheim Convention Center", "Room nights on the books", "▲ +12%", "2026 pace vs. last year · 2027 ▲ +17%", "LARC"],
    ["Anaheim inflation", "Consumer prices, 3-year average", f"{CPI['cagr3']}% a year", f"2026 {CPI['y26']}% · 2027 {CPI['y27']}% · U.S. 5-year {CPI['us5']}%", "LARC (Moody's Analytics)"],
  ],
  tables=[dict(title="OC Vibe as described in LARC's market reports", sub="Program and status, June and Sept. 2026 editions",
    cols=[["Element",0],["Detail",0]],
    rows=[["Scale", "100-acre, $5 billion mixed-use district; approved Oct. 2022"], ["Office", "1 million sq ft; The Weave (168,000 sq ft, six stories) vertical construction complete"],
          ["Entertainment", "835,500+ sq ft incl. Honda Center (18,300+ seats) and 185,500+ sq ft new (8,400+ seats); 104,000 sq ft concert hall vertical construction complete"],
          ["Hotels", "Two hotels, 550 rooms (Arena Hotel 320, Meadow Hotel 230), in planning"], ["Residential", "2,500+ units, 15% low-income"],
          ["Dining and retail", "~172,000 sq ft restaurant and outdoor dining; ~57,000 sq ft new retail plus 25,000 sq ft at ARTIC"],
          ["Public space and parking", "20 acres of parks and plazas, 3 miles of trails, OC River Walk (1.7 miles, $100M+); ~13,000 parking spaces"],
          ["Timing", "Katella Commons market hall (50,000 sq ft) and public plaza in 2027; final phase by 2033"]],
    hi=-1, src="LARC Market Intelligence Reports (June and Sept. 2026)"),
    dict(title="Anaheim market hotel outlook", sub="Anaheim market (CoStar basis). F = LARC forecast.",
    cols=[["Year",0],["Occupancy",1],["Average nightly rate",1],["Revenue per available room",1],["Change",1]],
    rows=[[f"{y}{' F' if f else ''}", f"{o:.1f}%", f"${a:.2f}", f"${r:.2f}", D(rc, sp(rc))] for y, o, oc, a, ac, r, rc, f in LARC],
    hi=2, src=SRC["larc"]),
    dict(title="Hotels planned near OC Vibe and the resort", sub="Named projects in LARC pipeline tables (all in planning unless noted)",
    cols=[["Project",0],["Rooms",1],["Status",0]],
    rows=[["OC Vibe Arena Hotel", "320", "Planning"], ["OC Vibe Meadow Hotel", "230", "Planning"], ["Nickelodeon Hotel & Resort Garden Grove", "500", "Planning"],
          ["Le Méridien Anaheim Garden Grove", "402", "Planning"], ["GardenWalk Hotel Two (Westgate)", "400", "Planning"], ["Disneyland Forward Hotel 2", "250", "Planning"],
          ["TownePlace Suites Anaheim Resort", "186", "Planning"], ["Roadhouse Tribute Portfolio Anaheim Downtown", "125", "Construction, opening 1Q 2027"]],
    hi=0, src="LARC Market Intelligence Reports (July and Sept. 2026)"),
    dict(title="Anaheim Convention Center booking pace, by report edition", sub="Definite room nights on the books vs. same point last year",
    cols=[["Report edition",0],["2026",1],["2027",1]], rows=[[e, f"+{a}%", f"+{b}%"] for e, a, b in CONV_PACE], hi=4, src="LARC Market Intelligence Reports, Jan.–Sept. 2026")],
  charts=[dict(kind="bars", title="Anaheim hotels are outpacing the U.S. in 2026", sub="Revenue per available room, change vs. last year",
    rows=[dict(l="Anaheim, Q2 2026", v=lq['q2_revpar'], t=f"+{lq['q2_revpar']}%", hi=True), dict(l="Anaheim, Q1 2026", v=lq['q1_revpar'], t=f"+{lq['q1_revpar']}%"),
          dict(l="Anaheim, 2026 forecast", v=LARC[2][6], t=f"+{LARC[2][6]}%"), dict(l="U.S., Q2 2026", v=lq['us_q2'], t=f"+{lq['us_q2']}%"), dict(l="U.S., 2026 forecast", v=lq['us_26'], t=f"+{lq['us_26']}%")], src=SRC["larc"])],
  notes=["Demand drivers near OC Vibe: Honda Center (Anaheim Ducks and concerts), Angel Stadium, ARTIC, the Anaheim Convention Center (1.8 million sq ft) and DisneylandForward ($1.9 billion; Avengers Campus expansion opening 2027). OC Sports & Entertainment now employs about 3,000 locally (up from 2,000 in the June report).",
         "Events: the 2028 Summer Olympics include cycling and volleyball events in Anaheim, and LARC expects a 2028 hotel lift from them. The 2026 World Cup lifted rates this year but becomes a tough comparison in Q2–Q3 2027.",
         "Office: Orange County office vacancy was 14.4% in Q2 2026 (down 3.4 points from a year earlier); Kiln took 39,000 sq ft in the Stadium Area, where The Weave adds 168,000 sq ft of Class A space.",
         "Costs and inflation: Anaheim consumer prices are forecast to rise 3.2% a year over three years (3.3% in 2026, 3.5% in 2027), above the U.S. Hotel wages are forecast to grow 2.6% a year, about 6.0% a year in total labor cost, and LA County's $30 hotel minimum wage (by 2030) may pressure Orange County wages.",
         "Risks LARC flags: higher gas prices and airfares tied to the Iran conflict, a possible 2026 federal shutdown, midterm-election softness in Q4 2026, and slower U.S. job growth.",
         "LARC tables use two bases (CoStar Anaheim market vs. Visit Anaheim hotel sets) that should not be compared directly. LARC data © Lodging Analytics Research & Consulting."],
))

# ---------- BI Pulse stories ----------
STORIES = {
 "p-larc": dict(measure="Anaheim revenue per available room, Q2 2026", v=lq['q2_revpar'], val=f"+{lq['q2_revpar']}%", basis="Whole Anaheim hotel market (LARC)", ok=True,
   head="Anaheim hotel revenue per room up 11.4% as OC Vibe nears opening",
   dek="Convention bookings pace ahead for 2026 and 2027; the 2028 Olympics add events in Anaheim.",
   lede="Anaheim hotels earned 11.4% more revenue per available room in the second quarter of 2026 than a year earlier, more than double the U.S. gain, as rates rose 7.8%.",
   paras=["Lodging Analytics Research & Consulting (LARC) reports convention center room nights pacing 12% ahead for 2026 and 17% ahead for 2027, and forecasts 7.0% growth in revenue per room for Anaheim this year.",
          "OC Vibe's first buildings, The Weave office and a 104,000-square-foot concert hall, have completed vertical construction; Katella Commons and the public plaza are expected in 2027, and two hotels with 550 rooms are in planning.",
          "Visitors spent $1.76 billion in Anaheim in the second quarter, up 7.8%, according to Tourism Economics."],
   stats=[["+11.4%","Anaheim revenue per available room, Q2 2026","LARC"],["+12%","Convention room nights on the books for 2026","LARC"],["550","Hotel rooms planned at OC Vibe","LARC"],["+17%","Convention room nights on the books for 2027","LARC"]],
   chart=dict(title="Revenue per available room, change vs. last year", rows=[["Anaheim, Q2 2026",11.4,"+11.4%",1],["Anaheim, 2026 forecast",7.0,"+7.0%",0],["U.S., Q2 2026",5.7,"+5.7%",0],["U.S., 2026 forecast",5.1,"+5.1%",0]], src="LARC"),
   srcs=[SRC["larc"], SRC["te_fc"]]),
 "p-hotel": dict(measure="Disneyland submarket revenue per available room, 2026 YTD", v=CS_DL['ytd_revpar_chg'], val=f"+{CS_DL['ytd_revpar_chg']}%", basis="CoStar Disneyland submarket, Jan.–Aug. 2026 vs. 2025", ok=True,
   head="Resort-area hotels fill 78% of rooms while new supply stays scarce",
   dek=f"Only {CS_OC['uc_rooms']} hotel rooms are under construction across Orange County, {CS_OC['uc_pct']}% of supply.",
   lede=f"Hotels in CoStar's Disneyland submarket filled {CS_SUB[0][2]}% of their rooms over the 12 months through August 2026, the highest in Orange County, and revenue per available room is up {CS_DL['ytd_revpar_chg']}% so far this year.",
   paras=[f"Average nightly rates in the submarket reached ${CS_DL['ytd_adr']:.0f} in 2026, 33% above 2019. Food and beverage made up {CS_PROF['dl_fb']}% of hotel revenue, and food revenue per available room rose {CS_PROF['dl_food_chg']}%.",
          f"Only three hotels with {CS_OC['uc_rooms']} rooms are under construction countywide, and none of them is at OC Vibe. CoStar notes the OC Vibe district could create opportunities for future hotel investment.",
          f"Leisure and hospitality employs {CS_ECON['lh_jobs']},000 people in Orange County and is growing faster than in the U.S. (+{CS_ECON['lh_gr']}% vs. +{CS_ECON['lh_gr_us']}%)."],
   stats=[[f"{CS_SUB[0][2]}%","Disneyland submarket occupancy, 12 months","CoStar"],[f"+{CS_DL['ytd_revpar_chg']}%","Revenue per available room, 2026 YTD","CoStar"],[f"{CS_OC['uc_rooms']}","Rooms under construction in Orange County","CoStar"]],
   chart=dict(title="Revenue per available room, 2026 YTD change vs. 2025", rows=[["Disneyland submarket",CS_DL['ytd_revpar_chg'],f"+{CS_DL['ytd_revpar_chg']}%",1],["Orange County",CS_OC['ytd_revpar_chg'],f"+{CS_OC['ytd_revpar_chg']}%",0]], src="CoStar"),
   srcs=[SRC["costar"]]),
 "p-spend": dict(measure="Anaheim visitor spending, Q2 2026", v=Q['q2_sp_chg'], val=f"+{Q['q2_sp_chg']}%", basis="All Anaheim visitors (Tourism Economics)", ok=True,
   head="Anaheim visitors spent $1.76 billion in the second quarter, up 7.8%",
   dek=f"Spending per visitor reached about ${q2pv:.0f}; Tourism Economics forecasts ${ANA_PV[9]:.0f} per visitor by 2028.",
   lede="Visitors spent $1.76 billion in Anaheim in the second quarter of 2026, up 7.8% from a year earlier, as visits rose 2.8% to 6.74 million, according to Tourism Economics.",
   paras=["Overnight visits led the gain, rising 4.5%, while day visits rose 2.1%. Higher prices also contributed: hotel rates were nearly 9% above the second quarter of 2025.",
          f"In 2025, each Anaheim visitor spent about ${ANA_PV[6]:.0f}. Tourism Economics forecasts total spending of $7.2 billion in 2026 and $7.7 billion by 2028, or about ${ANA_PV[9]:.0f} per visitor.",
          "Visitors supported 67,817 jobs in Anaheim in 2025, one in three in the city, and LARC reports hotel revenue per room rose 11.4% in the second quarter."],
   stats=[["$1.76B","Anaheim visitor spending, Q2 2026","Tourism Economics"],[f"${ANA_PV[6]:.0f}","Spending per Anaheim visitor, 2025","Tourism Economics; BI calculation"],["$7.7B","Visitor spending forecast, 2028","Tourism Economics"]],
   chart=dict(title="Second quarter 2026, change vs. last year", rows=[["Anaheim spending",7.8,"+7.8%",1],["Garden Grove spending",7.1,"+7.1%",0],["Anaheim overnight visits",4.5,"+4.5%",0],["Anaheim day visits",2.1,"+2.1%",0]], src="Tourism Economics"),
   srcs=[SRC["te_fc"], SRC["te_ei"]]),
 "p-impact": dict(measure="Anaheim visitor spending, 2025", v=A['sp_chg'], val=sp(A['sp_chg']), basis="All Anaheim visitors (Tourism Economics)", ok=True,
   head="Visitors supported 67,817 Anaheim jobs in 2025, one in three",
   dek="Spending of $6.8 billion generated $10.4 billion in total economic impact and $970 million in state and local taxes.",
   lede="Visitors spent $6.8 billion in Anaheim in 2025, up 3.1%, generating $10.4 billion in total economic impact and supporting 67,817 jobs, according to Tourism Economics.",
   paras=[f"Food and beverage accounts for 11,366 of those jobs, or {A['fb_job_share']:.1f}%. The share is higher in Garden Grove ({G['fb_job_share']:.1f}%) and countywide ({O['fb_job_share']:.1f}%), where theme parks play a smaller role.",
          "Across Orange County, 51.3 million visitors spent $18.0 billion, supporting 178,164 jobs, or 7.4% of all jobs in the county.",
          "Food and beverage was the fastest-growing visitor spending category in 2025, up 5.5% in Anaheim."],
   stats=[["67,817","Jobs supported in Anaheim, 2025","Tourism Economics"],["$10.4B","Total economic impact in Anaheim","Tourism Economics"],["178,164","Jobs supported in Orange County","Tourism Economics"]],
   chart=dict(title="Food and beverage share of visitor-supported jobs, 2025", rows=[["Garden Grove",40.6,"40.6%",0],["Orange County",29.1,"29.1%",0],["Anaheim",16.8,"16.8%",1]], src="Tourism Economics"),
   srcs=[SRC["te_ei"]]),
 "p-night": dict(measure="Lodging value of one more night (estimate)", v=None, val=f"${N['lodge_night']/1e6:.0f}M", basis="Scenario estimate", ok=False,
   warn="This highlight is an estimate from a scenario, not measured growth. Label it as an estimate wherever it is used.",
   head="One more night per visitor is worth about $794 million in lodging",
   dek="Counting all spending by overnight visitors, the value rises to about $1.0 billion.",
   lede=f"If every Anaheim visitor stayed one more night, lodging spending would rise by an estimated $794 million, based on 2025 Tourism Economics spending and Azira length-of-stay data.",
   paras=["Visitors stayed 2.17 days on average in 2025 (1.9 days domestic, 5.9 international) and spent $1.72 billion on lodging. One more night at that rate adds about $794 million.",
          "If only overnight visitors add a day and every category of spending is counted, the value is about $1.02 billion; the ceiling, adding a day for every visitor, is $3.15 billion.",
          "OC Vibe's evening venues and 550 planned hotel rooms are the kind of draws that extend stays."],
   stats=[["$794M","One more night of lodging (estimate)","BI calculation"],["$1.02B","Overnight visitors, all spending (estimate)","BI calculation"],["2.17 days","Weighted average stay, 2025","Azira; Tourism Economics"]],
   chart=dict(title="Added spending by scenario, $ billions", rows=[["Lodging only",0.79,"$0.79B",1],["Overnight, all spending",1.02,"$1.02B",0],["All visitors, full day",3.15,"$3.15B",0]], src="BI calculation"),
   srcs=[SRC["night"], SRC["te_ei"]]),
 "p-transport": dict(measure="Vehicles per day on SR-57 beside OC Vibe", v=None, val="275,000", basis="Single period; counts from 2021–2024", ok=False,
   warn="Traffic counts near OC Vibe date from 2021–2024 and are repeated on the 2026 map.",
   head="275,000 vehicles a day pass OC Vibe on SR-57",
   dek="ARTIC sees 277 weekday bus trips, with one-seat rides to the resort in about 14 minutes.",
   lede="The Orange Freeway beside OC Vibe carries about 275,000 vehicles on an average weekday, and Ball Road between State College Boulevard and SR-57 about 54,000, according to OCTA's 2026 Traffic Flow Map.",
   paras=["OCTA schedules show 277 weekday bus trips stopping at ARTIC on three routes. Routes 50 and 553 reach the Katella and Harbor resort area in about 14 to 15 minutes, and 11 buses leave ARTIC after 10 p.m.",
          "Most visitors drive short distances: 74.0% of domestic trips to Anaheim and Garden Grove in August 2026 started within 50 miles, according to Azira data.",
          "The city is studying a Disneyland Resort–ARTIC transit link for the 2028 Olympics, and John Wayne Airport passengers rose 4% through April."],
   stats=[["275K","Vehicles per weekday on SR-57 at OC Vibe","OCTA"],["277","Weekday bus trips stopping at ARTIC","OCTA schedules"],["74.0%","Domestic trips from within 50 miles","Azira via Symphony"]],
   chart=dict(title="Vehicles per weekday, thousands", rows=[["SR-57 at OC Vibe",275,"275K",1],["Ball Rd",54,"54K",0],["Katella Ave",36,"36K",0],["State College Blvd",25,"25K",0]], src="OCTA"),
   srcs=[SRC["adt"], SRC["gtfs"], SRC["geo"]]),
 "p-d5": dict(measure="District 5 overnight share", v=None, val="85.8%", basis="Single period; no comparison year", ok=False,
   head="Most District 5 visitors stay overnight, and 44% are new",
   dek="Datafy shows the OC Vibe area already appears in 5.2% of Anaheim visitor days.",
   lede="Among District 5 visitors from January through May 2026, 85.8% stayed overnight and 43.8% were new visitors, according to Azira location data in Symphony.",
   paras=["Los Angeles (23.6%) and Riverside–San Bernardino (22.6%) are the top origin metros; California supplies 56.0% of domestic visitors. Their median household income is $85.7K.",
          "District 5 visitors also go to District 3 (27.9%), District 6 (19.2%) and the Anaheim Resort (13.7%). Saturday is the busiest day.",
          "In 2024, Datafy measured the OC Vibe area in 5.2% of Anaheim visitor days, ahead of meeting services (3.4%)."],
   stats=[["85.8%","Stay overnight","Azira via Symphony"],["43.8%","New visitors","Azira via Symphony"],["5.2%","Anaheim visitor days that include OC Vibe, 2024","Datafy"]],
   chart=dict(title="Also visited, share of District 5 visitors", rows=[["District 3",27.9,"27.9%",1],["District 6",19.2,"19.2%",0],["Anaheim Resort",13.7,"13.7%",0],["Disneyland Resort",8.4,"8.4%",0]], src="Azira via Symphony"),
   srcs=[SRC["poi"], SRC["datafy"], SRC["geo"]]),
 "p-media": dict(measure="Visits per 1,000 impressions", v=None, val="11.9", basis="Single period; no comparison year", ok=False,
   head="Visit Anaheim marketing drove 368,416 observed visits this year",
   dek="31.0 million measurable impressions returned 11.9 visits per 1,000; luxury placements converted best.",
   lede="From January through August 2026, Visit Anaheim's paid media produced 31.0 million measurable impressions and 368,416 observed visits to Anaheim, according to Azira attribution in Symphony.",
   paras=["Visitors arrived about 39 days after exposure on average.", "The luxury campaign returned 34.4 visits per 1,000 impressions, the highest of any campaign."],
   stats=[["31.0M","Measurable impressions","Azira attribution"],["368,416","Observed visits","Azira attribution"],["11.9","Visits per 1,000 impressions","Azira attribution"]],
   chart=dict(title="Visits per 1,000 impressions, top campaigns", rows=[["Luxury",34.4,"34.4",1],["Fall/Winter",30.4,"30.4",0],["Leisure",28.6,"28.6",0],["All campaigns",11.9,"11.9",0]], src="Azira attribution via Symphony"),
   srcs=[SRC["media"]]),
}

TAKEAWAYS = [
  f"Visitors spend more each trip: about ${ANA_PV[6]:.0f} per Anaheim visitor in 2025, forecast to reach ${ANA_PV[9]:.0f} by 2028; Q2 2026 spending rose 7.8%.",
  f"The visitor economy supports {num(A['jobs'])} Anaheim jobs (one in three); food and beverage is {A['fb_job_share']:.1f}% of them, {O['fb_job_share']:.1f}% countywide.",
  f"One more night per visitor is worth about ${N['lodge_night']/1e6:.0f} million in lodging spending, and about ${N['overnight_only']/1e9:.1f} billion counting all spending by overnight visitors.",
  "OC Vibe sits on one of the county's busiest corridors (SR-57, about 275,000 vehicles a day) next to ARTIC's 277 weekday bus trips; a resort–ARTIC transit link is under study for 2028.",
  f"District 5 visitors are mostly overnight ({D5['overnight']}%) and Southern Californian, and Datafy already measures OC Vibe in 5.2% of Anaheim visitor days.",
  f"Resort-area hotels fill {CS_SUB[0][2]}% of rooms (CoStar Disneyland submarket, the highest in the county), and only {CS_OC['uc_rooms']} rooms are under construction countywide, so new hotel supply is scarce.",
  f"Anaheim hotels are outpacing the U.S. (Q2 revenue per room +{lq['q2_revpar']}% vs. +{lq['us_q2']}%), conventions are pacing ahead, and the 2028 Olympics come to Anaheim; inflation and labor costs are the main headwinds.",
]

RECS = [
  "Program evening events at Honda Center and the concert hall with hotel packages to convert day trips into overnight stays (lodging value of one more night: about $794 million citywide).",
  "Build OC Vibe dining and entertainment into Visit Anaheim campaigns aimed at luxury and Southern California drive markets, which convert best.",
  "Work with OCTA and the City on the resort–ARTIC transit link and late-night service so resort guests can reach OC Vibe without driving.",
  "Use the tight hotel pipeline (668 rooms under construction countywide) and the growth in hotel food and beverage revenue to support the case for OC Vibe's planned hotels and dining.",
  "Request new traffic counts on Katella Ave and SR-57 before the 2027 openings to set a baseline.",
  "Share OC Vibe event calendars with Visit Anaheim so BI can measure visitation, spending and length of stay before and after openings.",
]

SOURCES = [
  ("Tourism Economics: Anaheim and Garden Grove Travel Forecast", "Published Sept. 2026 (data through Aug. 31, 2026). Annual and quarterly visits and spending, forecasts to 2028, international visitors, U.S. outlook."),
  ("Tourism Economics: Economic Impact of Visitors, 2025", "Anaheim (Apr. 2026), Garden Grove and Orange County (May 2026). Visitors, spending by category, jobs (including food and beverage), income and taxes."),
  ("Visit Anaheim BI: Extra Night study", "One-more-night scenarios using 2025 Tourism Economics spending and Azira length of stay; TID incentive group bookings (Simpleview)."),
  ("U.S. Bureau of Transportation Statistics", "Transportation Economic Trends: gasoline prices, domestic airfares and per-mile car costs, 2019–2025. County Transportation Profile, Orange County: commute mode, transportation facilities, population, jobs and households."),
  ("OCTA: 2026 Traffic Flow Map and bus schedules", "Weekday average daily traffic (Caltrans freeway counts and city arterial counts); OCTA GTFS bus schedules for Aug. 9–Nov. 7, 2026."),
  ("Symphony | Tourism Economics (Azira)", "District 5 POI analysis (Jan.–May 2026), domestic visitors to Anaheim and Garden Grove (Aug. 2026), media attribution (Jan.–Aug. 2026)."),
  ("Datafy", "Anaheim visitor report, calendar 2024: clusters including OC Vibe, length of stay, origins and demographics."),
  ("CoStar Group", "Orange County Hospitality Market, Disneyland Hospitality Submarket and Orange County Hospitality Capital Markets reports, pulled Oct. 12, 2026 (data through Aug. 2026): hotel performance by submarket, construction, hotel sales and pricing, hotel revenue mix, and Orange County economy (Oxford Economics)."),
  ("Lodging Analytics Research & Consulting (LARC)", "Anaheim Market Intelligence Reports, Jan., Apr., June, July and Sept. 2026: hotel performance and forecasts, convention pacing, OC Vibe and area developments, local economy."),
]

DQ = [
  "Spending per visitor is calculated from rounded Tourism Economics totals and is approximate.",
  "One-more-night values are scenarios that hold spending per day constant; they are not forecasts.",
  "Traffic counts near OC Vibe on the 2026 map date from 2021–2024; freeway volumes are Caltrans 2024 counts.",
  "Symphony, Datafy and Tourism Economics use different methods, device panels and periods; compare them as context, not like-for-like.",
  "LARC's Anaheim market tables (CoStar) and Visit Anaheim hotel set tables use different bases.",
  "CoStar figures are trailing 12 months or year to date through Aug. 2026. CoStar's own text and tables differ in a few places: the Disneyland submarket 12-month rate ($250 in text, $255 in tables; tables used), Orange County 12-month sales ($218.1M headline, $234.2M in tables; tables used), and the name of the 352-room hotel sold in May 2026 (two names given; address shown instead).",
  "CoStar hotel revenue mix comes from a sample of reporting hotels and may not represent every property.",
  "OC Vibe's cost and timeline differ between CoStar ($4 billion, buildout by 2028) and LARC ($5 billion, final phase by 2033); OC Vibe's own figures should be used.",
  "Not yet received: Tourism Economics transportation impact data.",
]

# ---------- OC Vibe impact section and per-section OC Vibe notes ----------
import data as _data, ocv_content as _ocv
_ocv.attach(SECTIONS, STORIES, TAKEAWAYS, RECS, SOURCES, DQ, SRC, _data)

import new_content as _nc
_nc.attach(SECTIONS, SOURCES, DQ, _ocv.REGISTER, TAKEAWAYS)

import views_valid as _vv
_vv.attach(SECTIONS, STORIES, TAKEAWAYS, RECS, SOURCES, DQ, _ocv.REGISTER, SRC)

import logic_content as _lc
_lc.attach(SECTIONS, TAKEAWAYS, RECS, STORIES)
import roles_content as _rc
_rc.attach(SECTIONS, DQ, _ocv.REGISTER, SOURCES)
_rc.transit_attach(SECTIONS, DQ, _ocv.REGISTER, SOURCES)
DATA_EXTRA = {}
import ocv_whole as _ow
_ow.attach(SECTIONS, STORIES, TAKEAWAYS, RECS, DQ, _ocv.REGISTER, SOURCES, DATA_EXTRA)
import calcs as _cx
_cx.attach(SECTIONS, TAKEAWAYS, DATA_EXTRA['main'])
import feature as _ft
_ft.attach(SECTIONS)
import facts_only as _fo
_fo.attach(SECTIONS, TAKEAWAYS, DQ, STORIES, DATA_EXTRA['main'], SOURCES, _ocv.REGISTER)
import newsroom as _nr   # Oct. 13, 2026: broadsheet news report + analysis structure (facts only; no opinion)
import schedule as _sc   # Oct. 14, 2026: quarterly update schedule (glossary term and method)
_nr.GLOSSARY_ADD += _sc.GLOSSARY; _nr.METHOD_ADD += _sc.METHOD
_nr.attach(SECTIONS, "Oct. 13, 2026")
for _o in (TAKEAWAYS, DQ, RECS, SOURCES, DATA_EXTRA, STORIES): _nr.no_em(_o)
import infographics as _ig   # Oct. 13, 2026: data infographics per section
_ig.attach(SECTIONS); _nr.no_em(SECTIONS)
import maps as _mp   # Oct. 13, 2026: map visuals for geographic data
_mp.attach(SECTIONS); _nr.no_em(SECTIONS)
