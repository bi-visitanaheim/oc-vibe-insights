"""Calculation breakdowns for every derived number in the report (John Picou: never show a calculated number without its breakdown).

Adds:
 - s["calc_steps"]: step table under each section's key insight (calculated steps and reported inputs);
 - "calc" on each What-it-means-for-OC-Vibe item, compare-and-contrast item and By-the-numbers card that carries a derived number;
 - a "How it's calculated" column on the OC Vibe impact tables;
 - calculations appended to the summary findings and the main announcement.
All values come from the model modules, so the breakdown text always matches the numbers shown.
"""
import impact as I, newdata as ND, data as D
from data import EI, N
import roles_content as RC

A = EI["Anaheim"]; B = I.RES[1]; C0, C2 = I.RES[0], I.RES[2]; V = I.VIEWS["Base"]
sp25 = A["sp25"] * 1e6; vis = A["vis25"] * 1e6; los = N["los"]; pd = I.PER_DAY
m = lambda v, d=1: f"${v/1e6:,.{d}f}M"
bn = lambda v, d=2: f"${v/1e9:,.{d}f}B"
n0 = lambda v: f"{v:,.0f}"
STR = ND.STR["Anaheim+"]; dow = STR["dow"]
YR = D.YEARS; i25, i28 = YR.index(2025), YR.index(2028)
SP_CAGR = ((D.ANA_SP[i28] / D._ANA_SP_PRECISE[2025]) ** (1 / 3) - 1) * 100
VIS_CAGR = ((D.ANA_VIS[i28] / D.ANA_VIS[i25]) ** (1 / 3) - 1) * 100
PV_CAGR = ((D.ANA_PV[i28] / D.ANA_PV[i25]) ** (1 / 3) - 1) * 100
hall = I.HALL_CAP * I.ASSUME["hall_events"][1] * I.ASSUME["hall_fill"][1]
small = I.SMALL_CAP * I.ASSUME["small_events"][1] * I.ASSUME["small_fill"][1]
nv_days = B["new_vis"] * los
vd0 = 0.052 * vis * los; vd_live = vis * los + nv_days + B["extra_days"]
ocv_vd1 = vd0 + nv_days + B["extra_days"]
both_seats = I.HALL_CAP + I.HONDA_SEATS
PK_LO, PK_HI = I.PARKING
fb_ratio = A["fb_jobs"] / A["fb"]
sunmon_adr = ND.SUNMON_ADR
S_MODEL = "Visit Anaheim BI scenario model (Oct. 12, 2026)"

# ---------------- shared calculation strings ----------------
CALC = dict(
  attend=f"150 concert hall events × {n0(I.HALL_CAP)} seats × 80% full ({n0(hall)}) + 150 theater and club events × {n0(I.SMALL_CAP)} seats × 70% full ({n0(small)}) = {n0(B['attend'])} attendees",
  netnew=f"{n0(B['attend'])} attendees × 25% net-new = {n0(B['new_vis'])} net-new visitors",
  sp_new=f"{n0(B['new_vis'])} net-new visitors × $258 per visitor = {m(B['sp_new'])}",
  per_day=f"$258 per visitor ÷ {los:.2f}-day average stay = ${pd:.2f} per visitor day",
  days=f"{A['vis25']:.1f}M Anaheim visitors × 1% who add a day = {n0(B['extra_days'])} extra visitor days",
  sp_stay=f"{n0(B['extra_days'])} extra visitor days × ${pd:.2f} = {m(B['sp_stay'])}",
  total=f"{m(B['sp_new'])} from net-new visitors + {m(B['sp_stay'])} from longer stays = {m(B['spend'])}",
  ocv0=f"5.2% of Anaheim visitor days × {bn(sp25,3)} Anaheim visitor spending = {m(V['ocv_today']['spend'],2)} (about {m(V['ocv_today']['spend'],0)})",
  ocv1=f"{m(V['ocv_today']['spend'],2)} + {m(B['spend'],2)} new = {m(V['ocv_live']['spend'],2)} (about {m(V['ocv_live']['spend'],0)})",
  ana1=f"{bn(sp25,3)} + {m(B['spend'])} = {bn(V['ana_live']['spend'],3)} (about {bn(V['ana_live']['spend'])})",
  jobs=f"{m(B['spend'])} × {I.JOBS_ANA:.2f} jobs per $1M ({n0(A['jobs'])} jobs ÷ ${A['sp25']:,.0f}M visitor spending, 2025) = about {round(B['ana_jobs'],-1):,.0f} jobs",
  impact=f"{m(B['spend'])} × {I.MULT_ANA:.4f} (${A['impact']:,.0f}M total impact ÷ ${A['sp25']:,.0f}M visitor spending, 2025) = {m(B['ana_impact'],0)}",
  tax=f"{m(B['spend'])} × {I.TAX_ANA*100:.1f}% (${A['sl_tax']:,.0f}M state and local taxes ÷ ${A['sp25']:,.0f}M visitor spending) = {m(B['ana_tax'])}",
  share1=f"({vd0/1e6:.2f}M OC Vibe area visitor days today + {nv_days/1e6:.2f}M from net-new visitors + {B['extra_days']/1e6:.2f}M extra days) ÷ {vd_live/1e6:.1f}M Anaheim visitor days = {ocv_vd1/vd_live*100:.1f}%",
  growth=f"{m(B['spend'])} ÷ {bn(sp25)} = +{B['spend']/sp25*100:.1f}%",
  pv=f"{bn(sp25)} visitor spending ÷ {A['vis25']:.1f}M visitors = ${sp25/vis:.0f} per visitor",
  per1k="1,000 net-new visitors × $258 = $258,000",
  per100=f"{n0(I.HALL_CAP)} seats × 100 nights × 80% full = {n0(I.PER_100_EVENTS)} attendees",
  per1pct=f"{A['vis25']:.1f}M visitors × 1% × ${pd:.2f} per visitor day = {m(I.PER_1PCT_DAY)}",
  cap5000=f"(5,000 × 150 × 80% + {n0(I.SMALL_CAP)} × 150 × 70%) × 25% net-new × $258 + {m(B['sp_stay'])} from longer stays = {m(RC.CAP5000)}",
  mix=f"Each category's share of Anaheim's 2025 visitor spending × {m(B['spend'])}: " + "; ".join(f"{s*100:.1f}% = {m(v)}" for _, s, v in I.CAT[:4]),
  fbjobs=f"{m(I.CAT[3][2])} food and beverage spending × {fb_ratio:.2f} jobs per $1M ({n0(A['fb_jobs'])} F&B jobs ÷ ${A['fb']:,.0f}M F&B visitor spending) = about {round(I.FB_JOBS,-1):,.0f} jobs",
  jobs_per1m=f"{n0(A['jobs'])} jobs ÷ ${A['sp25']:,.0f}M visitor spending = {I.JOBS_ANA:.1f} jobs per $1M; {I.TAX_ANA*100:.1f}% × $1M = ${I.TAX_ANA*1e6:,.0f} in taxes",
  lodge_night=f"${N['lodging']/1e9:.3f}B 2025 lodging spending ÷ {los:.2f}-day average stay = {m(N['lodge_night'],0)}",
  los=f"Average stay = {N['dom_share']*100:.1f}% domestic visitors × {N['los_dom']} days + {N['intl_share']*100:.1f}% international × {N['los_intl']} days = {los:.2f} days",
  overnight=f"{N['overnight']:.1f}M overnight visitors × ${pd:.2f} per visitor day = {bn(N['overnight_only'])}",
  upper=f"{bn(sp25)} visitor spending ÷ {los:.2f}-day stay = {bn(N['plus1'])} (every visitor adds a day)",
  day_share=f"{N['day']:.1f}M day visitors ÷ {N['total']:.1f}M visitors = {N['day']/N['total']*100:.1f}%",
  steps=f"0.5% × {A['vis25']:.1f}M × ${pd:.2f} = {m(I.PER_1PCT_DAY*0.5)}; 1% = {m(I.PER_1PCT_DAY)}; 2% = {m(I.PER_1PCT_DAY*2)}",
  sunmon=f"(Sunday {dow['Sun'][0]:.1f}% + Monday {dow['Mon'][0]:.1f}%) ÷ 2 = {ND.SUNMON_OCC:.1f}%; (Friday {dow['Fri'][0]:.1f}% + Saturday {dow['Sat'][0]:.1f}%) ÷ 2 = {ND.FRISAT_OCC:.1f}%; occupancy = room nights sold ÷ rooms available",
  gap=f"{ND.FRISAT_OCC:.2f}% − {ND.SUNMON_OCC:.2f}% = {ND.FRISAT_OCC-ND.SUNMON_OCC:.2f}, about {ND.FRISAT_OCC-ND.SUNMON_OCC:.1f} points",
  pt_sunmon=f"{n0(STR['rooms'])} rooms × 1 point × 104 Sunday and Monday nights a year = {n0(ND.PT_SUNMON_RN)} room nights; × ${sunmon_adr:.2f} average Sunday–Monday rate = {m(ND.PT_SUNMON_REV)}",
  hotels=f"550 rooms × 365 nights × 70.0%–78.4% occupancy = {n0(C0['rn'])}–{n0(C2['rn'])} room nights; × $218–${I.ASSUME['hotel_adr'][2]:.2f} average rate = {m(C0['room_rev'])}–{m(C2['room_rev'])}; × 15% hotel tax = {m(C0['tot'])}–{m(C2['tot'])}",
  hotels_base=f"550 rooms × 365 × 74% = {n0(B['rn'])} room nights; × $218 = {m(B['room_rev'])}; × 15% = {m(B['tot'])}",
  vehicles=f"({n0(I.HALL_CAP)} concert hall + {n0(I.HONDA_SEATS)} Honda Center seats) × 90% arriving by car ÷ 2.5 to 2.0 people per car = {n0(I.TR['both_vehicles'][0])}–{n0(I.TR['both_vehicles'][1])} vehicles; ÷ {n0(PK_HI)} to {n0(PK_LO)} planned spaces = {I.TR['both_parking_share'][0]*100:.0f}%–{I.TR['both_parking_share'][1]*100:.0f}%",
  hall_veh=f"{n0(I.HALL_CAP)} seats × 90% by car ÷ 2.5 to 2.0 people per car = {n0(I.TR['hall_vehicles'][0])}–{n0(I.TR['hall_vehicles'][1])} vehicles",
  bus=f"Route 50 ({D.TRANSIT['routes']['50'][1]}) + route 53 ({D.TRANSIT['routes']['53'][1]}) + route 553 ({D.TRANSIT['routes']['553'][1]}) weekday trips stopping at ARTIC = {D.TRANSIT['wk']}, counted from OCTA schedules",
  staff=f"{n0(RC.STAFF[RC.OCTA][-1])} ÷ {n0(RC.STAFF[RC.OCTA][0])} − 1 = {(RC.STAFF[RC.OCTA][-1]/RC.STAFF[RC.OCTA][0]-1)*100:.1f}% (2003 to 2017)",
  riders=f"{RC.PAX['Total'][-1]/1e6:.1f}M (2017) ÷ {max(RC.PAX['Total'])/1e6:.1f}M (2007) − 1 = {(RC.PAX['Total'][-1]/max(RC.PAX['Total'])-1)*100:.0f}%",
  out_state=f"100% − {D.D5_STATE[0][1]:.1f}% from California = {100-D.D5_STATE[0][1]:.0f}% from other states",
  per1k_media=f"{n0(D.MED['visits'])} observed visits ÷ {D.MED['impr']/1e6:.1f}M impressions × 1,000 = {D.MED['per1k']}",
  lux=f"74.9K visits ÷ 2,177.3K impressions × 1,000 = 34.4 (Basis DSP luxury placements); 34.4 ÷ {D.MED['per1k']} = {34.4/D.MED['per1k']:.1f} times the average",
  spend_growth=f"Visitor spending {bn(sp25)} (2025) → ${D.ANA_SP[i28]:.1f}B (2028 forecast) = +{SP_CAGR:.1f}% a year; visits {A['vis25']:.1f}M → {D.ANA_VIS[i28]:.1f}M = +{VIS_CAGR:.1f}% a year; per visitor $258 → $279 = +{PV_CAGR:.1f}% a year",
  sp_2025=f"{bn(sp25)} (2025) ÷ ${D._ANA_SP_PRECISE[2024]:.3f}B (2024) − 1 = +{(D._ANA_SP_PRECISE[2025]/D._ANA_SP_PRECISE[2024]-1)*100:.1f}%",
  revpar_us="11.4% ÷ 5.7% = 2.0 times the U.S. rate",
  ten=f"2027: {m(I.HALL_CAP*150*0.8*0.25*258)} from the concert hall's net-new visitors + half of the longer-stay value ({m(B['sp_stay']*0.5)}) = {m(I.HALL_CAP*150*0.8*0.25*258 + B['sp_stay']*0.5)}; 2028–2036: 9 × {m(B['spend'])}; total {m(I.TEN['spend'],0)}",
)

# ---------------- key-insight step tables ----------------
def R(step, calc, result, src):
    return [step, calc, result, src]
REP = "Reported"
KEY_STEPS = {
 "p-ocv": [R("1. Attendance a year", CALC["attend"].rsplit(" = ", 1)[0], n0(B["attend"]), S_MODEL),
           R("2. Net-new visitors", f"{n0(B['attend'])} attendees × 25% net-new", n0(B["new_vis"]), S_MODEL),
           R("3. Spending from net-new visitors", f"{n0(B['new_vis'])} × $258 per visitor (Tourism Economics, 2025)", m(B["sp_new"]), S_MODEL),
           R("4. Extra visitor days", f"{A['vis25']:.1f}M Anaheim visitors × 1% who add a day", n0(B["extra_days"]), S_MODEL),
           R("5. Spending per visitor day", f"$258 ÷ {los:.2f}-day average stay", f"${pd:.2f}", S_MODEL),
           R("6. Spending from longer stays", f"{n0(B['extra_days'])} × ${pd:.2f}", m(B["sp_stay"]), S_MODEL),
           R("7. New visitor spending", f"{m(B['sp_new'])} + {m(B['sp_stay'])}", m(B["spend"]), S_MODEL),
           R("8. Range", "5th to 95th percentile of 200,000 simulations, each varying the assumptions between the conservative and optimistic cases", "$71M–$122M", S_MODEL),
           R("9. OC Vibe area today", f"5.2% of Anaheim visitor days (Datafy, 2024) × {bn(sp25,3)}", m(V["ocv_today"]["spend"],2), "Datafy (2024); Tourism Economics (2025)"),
           R("10. Anaheim with OC Vibe", f"{bn(sp25,3)} + {m(B['spend'])}", bn(V["ana_live"]["spend"],3), S_MODEL),
           R("11. OC Vibe when live", f"{m(V['ocv_today']['spend'],2)} + {m(B['spend'],2)}", m(V["ocv_live"]["spend"],2), S_MODEL)],
 "p-spend": [R("Spending per visitor, 2025", f"{bn(sp25)} visitor spending ÷ {A['vis25']:.1f}M visitors", f"${sp25/vis:.0f}", "Tourism Economics (2025)"),
             R("Forecast per visitor, 2028", REP, "$279", "Tourism Economics forecast (Sept. 2026)"),
             R("Visitor spending, Q2 2026", f"{REP}; vs. Q2 2025", "$1.76B (+7.8%)", "Tourism Economics (Sept. 2026)"),
             R("Growth rates to 2028", CALC["spend_growth"], f"+{SP_CAGR:.1f}% vs. +{VIS_CAGR:.1f}%", "Tourism Economics; BI calculation")],
 "p-impact": [R("Jobs supported, Anaheim", f"{REP} (direct, indirect and induced)", n0(A["jobs"]), "Tourism Economics (2025)"),
              R("Share of all Anaheim jobs", REP, "32.8%, about one in three", "Tourism Economics (2025)"),
              R("Jobs supported, Orange County", REP, "178,164", "Tourism Economics (2025)"),
              R("Food and beverage share of jobs", REP, "16.8% Anaheim; 29.1% Orange County", "Tourism Economics (2025)")],
 "p-night": [R("Average stay", CALC["los"].replace("Average stay = ", "").rsplit(" = ", 1)[0], f"{los:.2f} days", "Tourism Economics; Azira"),
             R("One more night, lodging", f"${N['lodging']/1e9:.3f}B lodging spending ÷ {los:.2f} days", m(N["lodge_night"], 0), "Tourism Economics (2025); BI calculation"),
             R("Spending per visitor day", f"$258 ÷ {los:.2f} days", f"${pd:.2f}", "BI calculation"),
             R("Each 1% of visitors adding a day", f"{A['vis25']:.1f}M × 1% × ${pd:.2f}", m(I.PER_1PCT_DAY), S_MODEL)],
 "p-transport": [R("Domestic trips from within 50 miles", REP, "74.0%", "Azira (Aug. 2026)"),
                 R("Vehicles on SR-57 beside OC Vibe", f"{REP} (Caltrans 2024 count on OCTA's map)", "275,000 a weekday", "OCTA (Aug. 2026)"),
                 R("Weekday bus trips stopping at ARTIC", CALC["bus"].rsplit(" = ", 1)[0], str(D.TRANSIT["wk"]), "OCTA schedules (Aug.–Nov. 2026); BI count")],
 "p-d5": [R("Overnight share, District 5", REP, "85.8%", "Azira (Jan.–May 2026)"),
          R("First-time visitors", REP, "43.8%", "Azira (Jan.–May 2026)"),
          R("OC Vibe area share of Anaheim visitor days", REP, "5.2%", "Datafy (2024)")],
 "p-media": [R("Measurable impressions", REP, "31.0M", "Azira (Jan.–Aug. 2026)"),
             R("Observed visits", REP, "368,416", "Azira (Jan.–Aug. 2026)"),
             R("Visits per 1,000 impressions", CALC["per1k_media"].rsplit(" = ", 1)[0], str(D.MED["per1k"]), "BI calculation"),
             R("Days from ad to visit", REP, "39", "Azira (Jan.–Aug. 2026)")],
 "p-hotel": [R("Disneyland submarket occupancy and rate", REP, "78.4%; $255", "CoStar (12 months to Aug. 2026)"),
             R("Rooms under construction", REP, "668", "CoStar (Aug. 2026)"),
             R("Sunday–Monday occupancy", f"(Sunday {dow['Sun'][0]:.1f}% + Monday {dow['Mon'][0]:.1f}%) ÷ 2", f"{ND.SUNMON_OCC:.1f}%", "STR (2026); BI calculation"),
             R("Friday–Saturday occupancy", f"(Friday {dow['Fri'][0]:.1f}% + Saturday {dow['Sat'][0]:.1f}%) ÷ 2", f"{ND.FRISAT_OCC:.1f}%", "STR (2026); BI calculation")],
 "p-larc": [R("Hotel revenue per room, Q2 2026", REP, "+11.4% (U.S. +5.7%)", "LARC (Sept. 2026)"),
            R("Convention room nights on the books", f"{REP}; vs. same point last year", "+12% (2026); +17% (2027)", "LARC (Sept. 2026)"),
            R("Price and labor growth", REP, "About 3.2% and 6% a year", "LARC/Moody's (Sept. 2026)")],
}

# ---------------- calcs for What-it-means-for-OC-Vibe items: (section, kind, index) ----------------
ITEM = {
 ("p-ocv", "enhance", 0): f"{CALC['ana1']}; {CALC['ocv0']}; {CALC['ocv1']}",
 ("p-ocv", "enhance", 1): f"Jobs: {CALC['jobs']}. Impact: {CALC['impact']}. Taxes: {CALC['tax']}",
 ("p-ocv", "enhance", 2): CALC["mix"],
 ("p-ocv", "enhance", 3): f"{CALC['per1pct']}; {CALC['per1k']}; {CALC['per100']}",
 ("p-ocv", "need", 0): "Share of the simulation's variation explained by each assumption (standardized regression on 200,000 draws)",
 ("p-ocv", "need", 1): "Share of the simulation's variation explained by each assumption (standardized regression on 200,000 draws)",
 ("p-ocv", "need", 2): CALC["cap5000"],
 ("p-ocv", "need", 3): f"{CALC['los']}; 85.8% overnight and 5.2% share are reported (Azira; Datafy)",
 ("p-spend", "enhance", 0): f"{CALC['pv']}; {CALC['per1k']}",
 ("p-spend", "enhance", 1): CALC["spend_growth"],
 ("p-impact", "enhance", 0): f"{CALC['jobs_per1m']}; {CALC['jobs']}; {CALC['fbjobs']}",
 ("p-night", "enhance", 0): CALC["day_share"],
 ("p-night", "enhance", 1): CALC["pt_sunmon"],
 ("p-night", "need", 2): CALC["steps"],
 ("p-transport", "need", 0): CALC["vehicles"],
 ("p-transport", "need", 1): f"OCTA staff: {CALC['staff']}; county transit riders: {CALC['riders']}",
 ("p-media", "enhance", 0): f"{CALC['per1k_media']}; {CALC['lux'].split(';')[0]}",
 ("p-hotel", "enhance", 0): CALC["hotels"],
 ("p-hotel", "enhance", 1): "Weeknight occupancy = Sunday–Thursday room nights sold ÷ rooms available, by month (STR daily data); nights at 90%+ counted from daily occupancy",
 ("p-hotel", "need", 1): "Group share = group room nights ÷ all room nights sold, by month (STR daily data)",
 ("p-d5", "enhance", 1): CALC["out_state"],
}

# ---------------- calcs for compare-and-contrast items: (section, type) ----------------
CC = {
 ("p-ocv", "Growth"): CALC["growth"], ("p-ocv", "Opportunity"): CALC["share1"],
 ("p-spend", "Growth"): CALC["spend_growth"],
 ("p-impact", "Growth"): CALC["sp_2025"], ("p-impact", "Explanation"): f"${A['impact']:,.0f}M total impact ÷ ${A['sp25']:,.0f}M visitor spending = ${I.MULT_ANA:.2f} per $1",
 ("p-night", "Growth"): CALC["per1pct"], ("p-night", "Opportunity"): CALC["day_share"], ("p-night", "Pitfall"): CALC["upper"], ("p-night", "Explanation"): CALC["lodge_night"],
 ("p-transport", "Pitfall"): CALC["vehicles"], ("p-transport", "Explanation"): CALC["riders"],
 ("p-d5", "Opportunity"): CALC["out_state"],
 ("p-media", "Opportunity"): CALC["lux"],
 ("p-hotel", "Opportunity"): f"{CALC['gap']}; {CALC['pt_sunmon']}",
 ("p-larc", "Growth"): CALC["revpar_us"],
}

# ---------------- calcs for By-the-numbers cards: (section, value) ----------------
CARD = {
 ("p-ocv", bn(sp25)): "Reported by Tourism Economics (2025)",
 ("p-ocv", bn(V["ana_live"]["spend"])): CALC["ana1"],
 ("p-ocv", m(V["ocv_today"]["spend"], 0)): CALC["ocv0"],
 ("p-ocv", m(V["ocv_live"]["spend"], 0)): CALC["ocv1"],
 ("p-spend", "$258"): CALC["pv"],
 ("p-night", "$794M"): CALC["lodge_night"], ("p-night", "$1.02B"): CALC["overnight"], ("p-night", "$3.15B"): CALC["upper"],
 ("p-transport", "277"): CALC["bus"],
 ("p-media", "34.4"): CALC["lux"].split(";")[0],
}

# ---------------- "How it's calculated" column for the OC Vibe impact tables ----------------
TABLE_CALC = {
 "Three views of impact: Anaheim, Anaheim with OC Vibe, and OC Vibe's own": {
   "Visitors a year": f"View 2 = {A['vis25']:.1f}M + {n0(B['new_vis'])} net-new visitors",
   "Visitor days a year": f"Visitors × {los:.2f}-day stay; view 2 adds {nv_days/1e6:.2f}M days from net-new visitors and {B['extra_days']/1e6:.2f}M extra days; 3a = 5.2% of Anaheim visitor days; 3b = 3a + the same additions",
   "Visitor spending": f"View 2 = {bn(sp25)} + {m(B['spend'])}; 3a = 5.2% × {bn(sp25)}; 3b = 3a + {m(B['spend'])}",
   "Total economic impact": f"View 1 reported; others = spending × {I.MULT_ANA:.4f}",
   "Jobs supported": f"View 1 reported; others = spending ÷ $1M × {I.JOBS_ANA:.2f}",
   "State and local taxes": f"View 1 reported; others = spending × {I.TAX_ANA*100:.1f}%",
   "OC Vibe share of Anaheim visitor days": "OC Vibe area visitor days ÷ Anaheim visitor days",
   "Simulation range for visitor spending (5th–95th percentile)": "5th–95th percentile of 200,000 simulations"},
 "OC Vibe visitor impact by scenario": {
   "Concert hall, theater and club attendance": f"Concert hall events × {n0(I.HALL_CAP)} seats × fill + theater and club events × {n0(I.SMALL_CAP)} seats × fill",
   "Net-new visitors to Anaheim": "Attendance × net-new share (15% / 25% / 35%)",
   "Extra visitor days from longer stays": f"{A['vis25']:.1f}M visitors × share who add a day (0.5% / 1% / 2%)",
   "New visitor spending, total": "From net-new visitors + from longer stays",
   "· from net-new visitors": "Net-new visitors × $258",
   "· from longer stays": f"Extra visitor days × ${pd:.2f}",
   "· of which lodging": f"Extra visitor days × ${I.LODGE_PER_VDAY:.2f} lodging per visitor day (${N['lodging']/1e9:.3f}B ÷ {vis*los/1e6:.1f}M visitor days)",
   "Anaheim: total economic impact": f"New spending × {I.MULT_ANA:.4f}",
   "Anaheim: jobs supported": f"New spending ÷ $1M × {I.JOBS_ANA:.2f}",
   "Anaheim: state and local taxes": f"New spending × {I.TAX_ANA*100:.1f}%",
   "Orange County: total economic impact": f"New spending × {I.MULT_OC:.4f} (Orange County ratio)",
   "Orange County: jobs supported": f"New spending ÷ $1M × {I.JOBS_OC:.2f}",
   "Orange County: state and local taxes": f"New spending × {I.TAX_OC*100:.1f}%",
   "California: new out-of-state visitor spending": f"New spending × {I.OUT_OF_STATE*100:.0f}% from outside California",
   "California: jobs supported": f"California spending ÷ $1M × {I.JOBS_CA:.2f} (Visit California 2025)",
   "California: state and local taxes": f"California spending × {I.TAX_CA*100:.1f}%",
   "OC Vibe hotels: room nights a year": "550 rooms × 365 × occupancy (70% / 74% / 78.4%)",
   "OC Vibe hotels: room revenue": f"Room nights × average rate ($218 / $218 / ${I.ASSUME['hotel_adr'][2]:.2f})",
   "OC Vibe hotels: Anaheim hotel tax (15%)": "Room revenue × 15%"},
 "What each lever is worth": {
   "Every 1% of Anaheim visitors who add a day": CALC["per1pct"],
   "Every 1,000 net-new visitors": CALC["per1k"],
   "Every 100 concert hall nights at 80% full": f"{CALC['per100']}; × 25% net-new × $258 = {m(I.PER_100_EVENTS*0.25*258)}",
   "Each point of OC Vibe hotel occupancy": "550 rooms × 365 × 1% = 2,008 room nights; × $218 = $437,700; × 15% = $65,700",
   "Each $1M in new visitor spending": CALC["jobs_per1m"],
   "Each point of Sunday–Monday hotel occupancy citywide": CALC["pt_sunmon"]},
 "Transportation effects (base case)": {
   "Vehicle round trips a year from new venue attendance": f"{n0(B['attend'])} attendees × 90% by car ÷ 2.5 people per car = {n0(I.TR['veh_round_trips_yr'])}",
   "Vehicles on a sold-out concert hall night": CALC["hall_veh"],
   "Vehicles when Honda Center and the concert hall both sell out": CALC["vehicles"],
   "Transit riders on a sold-out concert hall night (5% by transit)": f"{n0(I.HALL_CAP)} × 5% = {n0(I.TR['transit_riders'])} riders ÷ 60 per bus = {I.TR['bus_loads']:.1f} bus loads",
   "New visitor spending on transportation a year": f"{m(B['spend'])} × 3.3% transportation share = {m(I.TR['transport_spend'])}",
   "Cost of driving (illustrative 60-mile round trip)": "60 miles × $0.82 per mile = $49"},
 "Where the new visitor spending goes (base case)": {
   **{c: f"{s*100:.1f}% × {m(B['spend'])}" for c, s, _ in I.CAT},
   "Food and beverage jobs supported": CALC["fbjobs"]},
 "First ten years, 2027–2036 (base case)": {
   "New visitor spending": CALC["ten"],
   "Anaheim total economic impact": f"{m(I.TEN['spend'],0)} × {I.MULT_ANA:.4f}",
   "State and local taxes": f"{m(I.TEN['spend'],0)} × {I.TAX_ANA*100:.1f}%",
   "OC Vibe hotel room nights": "(230 rooms × 2 years + 550 rooms × 7 years) × 365 × 74%",
   "Anaheim hotel tax from OC Vibe hotels (15%)": "Room nights × $218 × 15%"},
}

TAKE = {0: f"{CALC['ana1']}; jobs {n0(A['jobs'])} + about {round(B['ana_jobs'],-1):,.0f}; {CALC['ocv0']}; {CALC['ocv1']}",
        1: CALC["vehicles"], 2: CALC["pv"], 4: f"{CALC['lodge_night']}; {CALC['overnight']}", 9: CALC["sunmon"].split("; occupancy")[0]}


def attach(SECTIONS, TAKEAWAYS, MAIN):
    for s in SECTIONS:
        sid = s["id"]
        if sid in KEY_STEPS:
            s["calc_steps"] = KEY_STEPS[sid]
        if s.get("for_ocv"):
            for kind, items in s["for_ocv"].items():
                for i, it in enumerate(items):
                    if (sid, kind, i) in ITEM: it["calc"] = ITEM[(sid, kind, i)]
        for c in s.get("cc") or []:
            if (sid, c["type"]) in CC: c["calc"] = CC[(sid, c["type"])]
        s["card_calc"] = [CARD.get((sid, c[2])) for c in s["cards"]]
        for t in s["tables"]:
            tc = TABLE_CALC.get(t["title"])
            if tc and not any(col[0] == "How it's calculated" for col in t["cols"]):
                t["cols"] = t["cols"] + [["How it's calculated", 0]]
                t["rows"] = [r + [tc.get(r[0], "")] for r in t["rows"]]
                t["wide"] = True
    for i, c in TAKE.items():
        if i < len(TAKEAWAYS):
            t = TAKEAWAYS[i]; k = t.rfind(" (Source: ")
            TAKEAWAYS[i] = (t[:k] + f" (Calculation: {c})" + t[k:]) if k > 0 else t + f" (Calculation: {c})"
    MAIN["paras"] = [p.replace("Each point of Sunday–Monday occupancy is worth about $5.1M in room revenue a year.",
                               f"Each point of Sunday–Monday occupancy is worth about $5.1M in room revenue a year ({CALC['pt_sunmon']}).") for p in MAIN["paras"]]
    MAIN["stat_calc"] = [None, None, None, None, CALC["sunmon"].split("; (Friday")[0]]
