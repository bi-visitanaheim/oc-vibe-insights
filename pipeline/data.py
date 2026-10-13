"""Single source of truth for the OC Vibe dashboard + deck. Every figure traces to a source below."""
import json

def pct(a, b): return (a / b - 1) * 100
def D(v, t): return {"d": round(v, 1), "t": t}
def sp(v, nd=1): return ("+" if v > 0 else "−" if v < 0 else "") + f"{abs(v):.{nd}f}%"

# ---------------- Sources ----------------
SP = "https://visitanaheimorg.sharepoint.com/sites/BusinessIntelligence2/Shared%20Documents/General/"
SRC = {
  "te_ei": "Tourism Economics, Economic Impact of Visitors 2025 (Anaheim, Garden Grove, Orange County; published Apr–May 2026)",
  "te_fc": "Tourism Economics, Anaheim and Garden Grove Travel Forecast (published Sept. 2026; data through Aug. 31, 2026)",
  "larc": "Lodging Analytics Research & Consulting (LARC), Anaheim Market Intelligence Report, Sept. 2026",
  "larc_set": "LARC, Visit Anaheim hotel set forecast (Forecasts Combined for Distro 3Q-26)",
  "night": "Visit Anaheim BI, Extra Night Calculation deck and TID Request workbook (2025 Tourism Economics and Azira inputs; recalculated Oct. 12, 2026)",
  "tid": "Simpleview, TID incentive bookings (TID Request workbook, exported Jan. 20, 2025; event years 2022–2034)",
  "poi": "Symphony | Tourism Economics, Azira POI Analysis: District 5 (Jan. 1–May 31, 2026)",
  "geo": "Symphony | Tourism Economics, Azira Domestic Visitors: Anaheim and Garden Grove (Aug. 2026)",
  "media": "Symphony | Tourism Economics, Azira Media Attribution (exposures Jan. 1–Aug. 31, 2026)",
}

# ---------------- Tourism Economics Economic Impact 2025 ----------------
EI = {
  "Anaheim":       dict(vis25=26.5, vis24=26.3, sp25=6832.0, sp24=6626.0, impact=10422.0, jobs=67817, jobs_share=32.8, sl_tax=970.0,
                        fb=1067.0, fb_jobs=11366, transport=224.0, lodging=1724.0, rec=2321.0, retail=1495.0, day_share=67.5),
  "Garden Grove":  dict(vis25=3.24, vis24=3.26, sp25=769.3, sp24=769.1, impact=1088.1, jobs=6694, jobs_share=11.8, sl_tax=83.6,
                        fb=246.2, fb_jobs=2721, transport=46.9, lodging=253.8, rec=48.9, retail=173.6, day_share=55.7),
  "Orange County": dict(vis25=51.3, vis24=50.7, sp25=17993.0, sp24=17398.0, impact=30673.0, jobs=178164, jobs_share=7.4, sl_tax=3094.0,
                        fb=4974.0, fb_jobs=51892, transport=707.0, lodging=4661.0, rec=3960.0, retail=3691.0, day_share=57.0),
}
for g, e in EI.items():
    e["pv25"] = e["sp25"] / e["vis25"]
    e["pv24"] = e["sp24"] / e["vis24"]
    e["pv_chg"] = pct(e["pv25"], e["pv24"])
    e["sp_chg"] = pct(e["sp25"], e["sp24"])
    e["vis_chg"] = pct(e["vis25"], e["vis24"])
    e["fb_share"] = e["fb"] / e["sp25"] * 100
    e["fb_job_share"] = e["fb_jobs"] / e["jobs"] * 100
    e["tr_share"] = e["transport"] / e["sp25"] * 100
# OC per-visitor published by TE: $350 (2025), $343 (2024)
EI["Orange County"]["pv_pub"] = (350, 343)

# ---------------- Tourism Economics forecast (Sept 2026) ----------------
YEARS = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028]
ANA_VIS = [24.2, 12.5, 19.9, 24.9, 25.8, 26.3, 26.5, 27.0, 27.3, 27.6]
ANA_SP = [5.4, 2.6, 4.5, 6.0, 6.5, 6.6, 6.8, 7.2, 7.4, 7.7]
ANA_SP_YOY = {2025: 3.1, 2026: 5.6, 2027: 2.7, 2028: 3.5}
GG_SP = [705.8, 330.1, 520.2, 710.5, 757.4, 767.3, 767.4, 806.4, 823.7, 848.6]
GG_VIS = [3.38, 1.67, 2.46, 3.06, 3.24, 3.26, 3.24, 3.31, 3.34, 3.38]
Q = dict(q2_vis=6.74, q2_vis_chg=2.8, q2_sp=1.76, q2_sp_chg=7.8, h1_vis=13.1, h1_sp=3.5, h1_vis_chg=3.1, h1_sp_chg=7.5,
         on_chg=4.5, day_chg=2.1, adr_q2="nearly 9%", gg_q2_vis=831, gg_q2_vis_chg=3.4, gg_q2_sp=200.4, gg_q2_sp_chg=7.1)
INTL = dict(v2026=2159658, s2026=2788.7, v_chg=1.0, s_chg=1.8, mex_v_chg=6.9, mex_s_chg=9.9)
ana_pv26 = 7.2e3 / 27.0      # rounded published inputs -> estimate
gg_pv26 = 806.4 / 3.31

# ---------------- LARC Sept 2026 (Anaheim market, CoStar basis) ----------------
LARC = [  # year, occ, occ chg, adr, adr chg, revpar, revpar chg, forecast
  (2024, 71.7, 0.1, 207.82, -1.6, 148.93, -1.5, False),
  (2025, 72.3, 0.9, 209.68, 0.9, 151.58, 1.8, False),
  (2026, 73.9, 2.2, 219.53, 4.7, 162.18, 7.0, True),
  (2027, 73.0, -1.2, 232.78, 6.0, 169.95, 4.8, True),
  (2028, 71.9, -1.6, 244.80, 5.2, 175.90, 3.5, True),
  (2029, 71.4, -0.6, 255.09, 4.2, 182.20, 3.6, True),
  (2030, 71.2, -0.3, 264.56, 3.7, 188.33, 3.4, True),
]
LARC_Q = dict(q1_revpar=10.6, q2_revpar=11.4, q2_adr=7.8, q2_occ=3.3, us_q2=5.7, us_26=5.1, us_26_adr=4.4, us_26_occ=0.7,
              us_27=2.1, conv_26=12, conv_27=17, supply_26=-0.5, cagr5=4.4, rank=7, of=64, jwa_2025=3, jwa_ytd=4)
# 2026 RevPAR forecast by LARC edition (Anaheim market basis; 2025 base differs slightly by edition)
LARC_REV = [("Jan. 2026", 155.99, 152.04), ("Apr. 2026", 158.86, 151.61), ("June 2026", 165.07, 151.55), ("Sept. 2026", 162.18, 151.58)]
# Visit Anaheim hotel set (LARC Forecasts Combined 3Q-26)
SET = dict(ana25=(0.7503, 235.56, 176.75), ana26=(0.7755, 247.74, 192.12), ana26_chg=(3.35, 5.17, 8.70),
           ana_q2=(186.84, 15.62), gg25=(0.7015, 161.36, 113.20), gg26=(0.7248, 164.16, 118.98), gg26_chg=(3.32, 1.73, 5.11))

# ---------------- Extra night (TID Request workbook, 'full day' sheet) ----------------
N = dict(total=26.5, dom=24.7, intl_listed=1.9, day=17.9, overnight=8.6, los_dom=1.9, los_intl=5.9, spend=6.832e9)
N["dom_share"] = N["dom"] / N["total"]
N["intl_share"] = 1 - N["dom_share"]
N["w_dom"] = N["dom_share"] * N["los_dom"]
N["w_intl"] = N["intl_share"] * N["los_intl"]
N["los"] = N["w_dom"] + N["w_intl"]
N["per_day"] = N["spend"] / N["los"]
N["plus1"] = N["per_day"]
N["plus_half"] = N["per_day"] * 0.5
N["total_plus1"] = N["spend"] + N["plus1"]
N["uplift"] = N["plus1"] / N["spend"] * 100
TID = [(2022,20,260199,312900,1122858),(2023,20,327558,268900,1085130),(2024,26,502401,533774,1620717),(2025,26,369827,397964,887225),
       (2026,30,460566,651200,1636000),(2027,26,401201,503796,1721956),(2028,20,299178,419540,1202300),(2029,15,286883,218500,1056000),
       (2030,8,213374,115840,845000),(2031,6,105951,82500,582500),(2032,3,66361,40540,225000),(2033,6,167194,95000,645000),(2034,4,125163,87000,410000)]

# ---------------- District 5 (Symphony POI) ----------------
D5 = dict(sample=1003735, overnight=85.8, new=43.8, hhi=85.7)
D5_POI = [("District 3",27.9),("District 6",19.2),("District 4",18.4),("District 2",17.2),("Anaheim Resort",13.7),("District 1",9.0),
          ("Disneyland Resort",8.4),("Disney California Adventure",5.5),("City of Orange",5.2),("Garden Grove",4.3),("Disneyland Park",3.6),
          ("Dana Point",3.2),("Newport Beach/Balboa",2.7),("Laguna Beach",2.6)]
D5_STATE = [("California",56.0),("Texas",4.5),("Virginia",4.2),("Florida",3.7),("Arizona",2.4),("New York",2.2),("Illinois",1.8),
            ("Georgia",1.7),("Pennsylvania",1.6),("North Carolina",1.6),("Ohio",1.5)]
D5_MSA = [("Los Angeles–Long Beach–Anaheim",23.6),("Riverside–San Bernardino–Ontario",22.6),("Washington–Arlington–Alexandria",3.6),
          ("San Diego–Chula Vista–Carlsbad",3.2),("New York–Newark–Jersey City",2.0),("Bakersfield–Delano",1.5),("Phoenix–Mesa–Chandler",1.5),
          ("Dallas–Fort Worth–Arlington",1.4),("Las Vegas–Henderson",1.2),("Chicago–Naperville–Elgin",1.2),("Oxnard–Thousand Oaks–Ventura",1.2)]
D5_DOW = [("Mon",13.6),("Tue",13.3),("Wed",13.4),("Thu",14.0),("Fri",14.4),("Sat",15.9),("Sun",15.3)]
GEO = dict(sample=182703, los=1.3, overnight=81.7, repeat=82.5, ca=93.3, la=47.7, riv=34.0, sd=4.8, lt50=74.0, d50_249=17.3, hhi=79.9)

# ---------------- Media attribution ----------------
MED = dict(impr=31011072, visits=368416, rate=1.19, per1k=11.9, days=39.0)
MED_CAMP = [("Leisure","Epsilon",8100.7,121.7,15.0),("Leisure","TripAdvisor",4019.4,53.9,13.4),("Leisure","Basis DSP (Adgenuity)",2236.7,63.9,28.6),
            ("Leisure","Travelzoo",1062.3,9.8,9.3),("New Brand","Basis DSP (Adgenuity)",8675.5,67.9,7.8),("Luxury","Epsilon",2259.3,32.1,14.2),
            ("Luxury","Basis DSP (Adgenuity)",2177.3,74.9,34.4),("Tourism","Expedia",763.8,17.6,23.0),("Tourism","Priceline",698.6,4.0,5.7),
            ("Fall/Winter 2025–26 Domestic","Expedia",245.1,7.5,30.4)]
MED_VEND = [("Basis DSP (Adgenuity)",13308.7,183.9,13.8),("Epsilon",10360.0,143.8,13.9),("TripAdvisor",4019.4,53.9,13.4),("Travelzoo",1062.3,9.8,9.3),
            ("Expedia",1008.9,24.9,24.7),("Priceline",698.6,4.0,5.7),("Klaviyo",56.2,1.1,19.8)]

if __name__ == "__main__":
    for g, e in EI.items():
        print(g, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in e.items()})
    print({k: round(v, 4) if isinstance(v, float) else v for k, v in N.items()})
    print("ana pv26", ana_pv26, "gg pv26", gg_pv26)
    for lab, a, b in LARC_REV: print(lab, a, pct(a, b))
    # media checks
    for c in MED_CAMP: print(c[0], c[1], round(c[3]/c[2]*1000, 1), c[4])
    for v in MED_VEND: print(v[0], round(v[2]/v[1]*1000, 1), v[3])

# ---------------- Additions for OC Vibe edition ----------------
ANA_Q = [("Q1 2025",6.12,1.61),("Q2 2025",6.55,1.63),("Q3 2025",6.85,1.71),("Q4 2025",7.01,1.87),("Q1 2026",6.32,1.72),("Q2 2026",6.74,1.76)]
_ANA_SP_PRECISE = {2021: 4.472, 2022: 6.024, 2023: 6.479, 2024: 6.626, 2025: 6.832}   # TE EI 2025 report ($B)
ANA_PV = [round(_ANA_SP_PRECISE.get(y, sp)*1000/v, 0) for y, v, sp in zip(YEARS, ANA_VIS, ANA_SP)]   # $ per visit
GG_PV = [round(sp/v, 0) for v, sp in zip(GG_VIS, GG_SP)]
# Extra-night scenario ladder (2025 inputs)
N["lodging"] = 1724.0e6                                   # TE EI 2025, Anaheim lodging spending
N["lodge_night"] = N["lodging"] / N["los"]                # one more night of lodging, all visitors
N["overnight_only"] = N["spend"] / (N["total"] * N["los"]) * N["overnight"]   # all spending, overnight visitors only
N["per_visitor_day"] = N["spend"] / (N["total"] * 1e6 * N["los"])
# OCTA 2026 Traffic Flow Map (weekday ADT, thousands); superscript = years before 2026 the count was taken
ADT = [("SR-57 (Orange Fwy), Ball Rd to Katella Ave", 275, "Caltrans 2024"), ("SR-57, north of Ball Rd", 287, "Caltrans 2024"),
       ("SR-57, Katella Ave to Orangewood Ave", 242, "Caltrans 2024"), ("I-5, Anaheim Resort area", 299, "Caltrans 2024"),
       ("Ball Rd, State College Blvd to SR-57", 54, "2024 count"), ("Katella Ave, State College Blvd to SR-57", 36, "2021 count"),
       ("Katella Ave, SR-57 to Santa Ana River", 29, "2021 count"), ("Katella Ave, east of river (Orange)", 24, "2024 count"),
       ("State College Blvd near Katella Ave", 25, "2024 count"), ("Orangewood Ave at SR-57", 25, "2021 count")]
# OCTA GTFS (service Aug. 9–Nov. 7, 2026): ARTIC docks
TRANSIT = dict(wk=277, sat=182, sun=181, routes={"50": ("Long Beach–Orange via Katella Ave", 100, 59, 58), "53": ("Anaheim–Irvine via Main St", 102, 123, 123),
              "553": ("Rapid Anaheim–Costa Mesa via Katella/Main", 75, 0, 0)}, resort_trips_wk=87, resort_trips_sat=29, resort_min_50=14, resort_min_553=15,
              late_wk=16, last_wk="1:38 a.m.", peak_2h=35, fare=2.00)
# Datafy 2024 (visitors 50+ miles, employees excluded)
DATAFY = dict(clusters=[("Attractions and activities",75.8),("Disneyland",74.4),("Accommodations",65.8),("Shopping",51.1),("Dining",28.7),("OC Vibe",5.2),("Meeting services",3.4)],
              overnight=79.2, day=20.8, repeat=49.6, los6=27.6, states=[("California",51.2),("Arizona",11.9),("Nevada",5.62),("Texas",4.57),("Washington",4.49),("Utah",4.44)],
              dmas=[("Los Angeles",15.5),("San Diego",10.8),("Phoenix–Prescott",10.6),("San Francisco–Oakland–San Jose",8.07),("Sacramento–Stockton–Modesto",7.1),("Las Vegas",4.98)],
              age45_64=35.8, age25_44=29.8, inc100=38.9)
# LARC: OC Vibe area
CONV_PACE = [("Jan. 2026", 22, 2), ("Apr. 2026", 16, 16), ("June 2026", 16, 16), ("July 2026", 12, 17), ("Sept. 2026", 12, 17)]
CPI = dict(cagr3=3.2, cagr5=3.0, y26=3.3, y27=3.5, y28=2.9, us5=2.3)
# BTS U.S. County Transportation Profile, Orange County (Bureau of Transportation Statistics)
BTS = dict(pop=3165820, workers=1565842, businesses=106961, jobs=1580778, hh=1082960, hh_noveh=51573,
           modes=[("Drove alone",1057284),("Worked from home",290235),("Carpooled",139549),("Walked",26586),("Public transportation",18009)],
           airports_medium=1, airports_regional=1, docks=6, rail_miles=121, pass_rail_miles=68, bridges=1181, bridges_good=56.6, bridges_fair=40.6, bridges_poor=2.8)
# BTS Transportation Economic Trends (data.bts.gov tcq5-4pgu), annual
TET_GAS = {2019:(2.604,3.337),2020:(2.168,2.820),2021:(3.008,3.700),2022:(3.951,4.952),2023:(3.519,4.513),2024:(3.304,4.184),2025:(3.097,4.094)}  # (U.S., West Coast) $/gal regular
TET_AIR = {2019:352.25,2020:292.26,2021:306.96,2022:378.13,2023:381.50,2024:383.60,2025:387.01}  # domestic average airfare, current $
TET_AUTO = {2019:0.6188,2020:0.6374,2021:0.6444,2022:0.7153,2023:0.8121,2024:0.8197}  # avg total cost per mile, current $

# ---------------- CoStar hospitality reports (pulled Oct. 12, 2026; data through Aug. 2026) ----------------
CS_SUB = [  # submarket, rooms, 12-mo occ, occ chg, ADR, ADR chg, RevPAR, RevPAR chg, under construction rooms
  ("Disneyland", 21213, 78.4, 3.1, 254.88, 4.6, 199.78, 7.9, 496),
  ("Newport Beach/Dana Point", 11719, 70.8, 1.2, 299.69, 5.9, 212.21, 7.1, 0),
  ("Santa Ana/Costa Mesa", 14209, 72.7, 2.6, 173.44, 2.9, 126.13, 5.6, 172),
  ("Anaheim (outside Disneyland submarket)", 5445, 71.6, 3.1, 130.16, 2.0, 93.14, 5.1, 0),
  ("Orange County Northwest/Fullerton", 7637, 70.4, -2.0, 131.85, 2.9, 92.81, 0.8, 0),
]
CS_OC = dict(rooms=60223, occ=74.0, occ_chg=2.0, adr=218, adr_chg=4.8, revpar=162, revpar_chg=6.9,
             ytd_occ=75.2, ytd_occ_chg=3.4, ytd_adr=221.67, ytd_adr_chg=6.2, ytd_revpar=166.64, ytd_revpar_chg=9.9,
             uc_rooms=668, uc_props=3, uc_pct=1.1, sales_12=234.2, sales_n=16, sales_3yr=311, cap=7.3, ppr_mkt=385794, ppr_chg=3.9, asset=23.3)
CS_DL = dict(ytd_occ=78.6, ytd_occ_chg=4.9, ytd_adr=252.55, ytd_adr_chg=5.7, ytd_revpar=198.51, ytd_revpar_chg=10.9,
             sales_12=90.9, sales_n=3, sales_3yr=133, cap=7.2, ppr_mkt=332755, ppr_2030=360353, big_sale=78.75, big_ppr=223722)
# Disneyland submarket annual performance (occ %, ADR, RevPAR, RevPAR chg)
CS_DL_YR = [("2019", 82.0, 190.22, 155.94, 5.1), ("2022", 75.0, 226.45, 169.75, 66.4), ("2023", 77.0, 245.13, 188.87, 11.3),
            ("2024", 76.0, 243.22, 184.86, -2.1), ("2025", 75.9, 246.00, 186.80, 1.0), ("2026 YTD (Jan.–Aug.)", 78.6, 252.55, 198.51, 10.9)]
CS_PIPE = [("Tribute Portfolio Anaheim Downtown", "Disneyland", 125, "Mar. 2027"), ("Home2 Suites by Hilton Irvine/Orange County", "Santa Ana/Costa Mesa", 172, "June 2027"),
           ("Kimpton Garden Grove Anaheim (mixed-use, with dining and retail)", "Disneyland", 371, "Sept. 2028")]
# Hotel revenue mix, trailing 12 months to Aug. 2026 (share of total hotel revenue; F&B = food + beverage + other F&B)
CS_PROF = dict(dl_rooms=69.4, dl_fb=22.4, dl_food_chg=28.9, dl_bev_chg=51.3, dl_labor=41.8, dl_ebitda=24.3,
               oc_rooms=61.3, oc_fb=29.4, oc_labor=38.9, oc_ebitda=23.0)
# Orange County economy (Oxford Economics via CoStar)
CS_ECON = dict(lh_jobs=244, lh_lq=1.3, lh_gr=2.69, lh_gr_us=1.59, lh_fc=0.98, lh_fc_us=0.59, tot_jobs=1697, tot_gr=0.53, tot_gr_us=0.44,
               hhi=121883, hhi_us=85449, pop=3140744, pop_chg=-0.3, unemp=4.1, unemp_us=4.3, drive_mkt=20, sna_23=11.74, sna_24=11.09,
               min_wage=16.50, disney_wage=20.42, acc_events26=142, acc_eis26=1.74, acc_rn26=600000)
