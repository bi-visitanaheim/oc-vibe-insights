"""OC Vibe visitor-impact scenarios (Visit Anaheim BI estimate).

Scope: visitor activity only (people traveling 50+ miles or staying overnight), at full operation,
in 2025 dollars. Excludes construction, office, resident and local-patron activity.
Every input is either sourced (see SRC_IN) or an explicit scenario assumption (see ASSUME).
"""
from data import EI, N, ANA_PV, D5, D5_STATE, CS_SUB, CS_OC

A, O = EI["Anaheim"], EI["Orange County"]

# ---------- Sourced inputs ----------
PV = ANA_PV[6]                                 # $ spending per Anaheim visitor, 2025 (TE EI)
PER_DAY = (A["sp25"] * 1e6 / (A["vis25"] * 1e6)) / N["los"]          # $ per visitor-day = $258 / 2.17
LODGE_PER_VDAY = A["lodging"] * 1e6 / (A["vis25"] * 1e6) / N["los"]  # lodging $ per visitor-day
MULT_ANA = A["impact"] / A["sp25"]             # total impact per $ of visitor spending (TE, Anaheim)
JOBS_ANA = A["jobs"] / A["sp25"]               # jobs per $1M visitor spending (TE, Anaheim)
TAX_ANA = A["sl_tax"] / A["sp25"]              # state & local taxes per $ (TE, Anaheim)
MULT_OC = O["impact"] / O["sp25"]
JOBS_OC = O["jobs"] / O["sp25"]
TAX_OC = O["sl_tax"] / O["sp25"]
CA = dict(spend=158.9e9, jobs=1.2e6, tax=13.6e9)   # Visit California 2025 economic impact (via RCRC summary, May 2026)
JOBS_CA = CA["jobs"] / (CA["spend"] / 1e6)
TAX_CA = CA["tax"] / CA["spend"]
OUT_OF_STATE = 1 - D5_STATE[0][1] / 100        # District 5 domestic visitors from outside California (Azira)
HALL_CAP = 5613                                 # concert hall capacity (City of Anaheim OCVibe page, 2026)
SMALL_CAP = 2000 + 300                          # theater + club (OCVIBE fact sheet, Apr. 2024)
ROOMS = 320 + 230                               # Arena Hotel + Meadow Hotel (City of Anaheim OCVibe page)
TOT = 0.15                                      # Anaheim transient occupancy tax (City of Anaheim)
DL = CS_SUB[0]                                  # CoStar Disneyland submarket (occ 78.4%, ADR $254.88)

# ---------- Scenario assumptions (BI) ----------
SCEN = ["Conservative", "Base", "Optimistic"]
ASSUME = dict(
    hall_events=(100, 150, 200),       # concert hall events a year
    hall_fill=(0.70, 0.80, 0.90),      # average share of seats filled
    small_events=(100, 150, 200),      # theater + club events a year
    small_fill=(0.60, 0.70, 0.80),
    net_new=(0.15, 0.25, 0.35),        # share of attendees who are net-new visitors to Anaheim (not locals, not already in town)
    add_day=(0.005, 0.01, 0.02),       # share of all Anaheim visitors who add a day because of OC Vibe
    hotel_occ=(0.70, CS_OC["occ"] / 100, DL[2] / 100),
    hotel_adr=(float(CS_OC["adr"]), float(CS_OC["adr"]), DL[4]),
)

def run():
    out = []
    for i, name in enumerate(SCEN):
        g = lambda k: ASSUME[k][i]
        attend = HALL_CAP * g("hall_events") * g("hall_fill") + SMALL_CAP * g("small_events") * g("small_fill")
        new_vis = attend * g("net_new")
        sp_new = new_vis * PV                                   # lever 1: new visitors
        extra_days = A["vis25"] * 1e6 * g("add_day")
        sp_stay = extra_days * PER_DAY                          # lever 2: longer stays
        lodge_stay = extra_days * LODGE_PER_VDAY
        spend = sp_new + sp_stay
        rn = ROOMS * 365 * g("hotel_occ")                       # lever 3: OC Vibe hotels (output, not added)
        room_rev = rn * g("hotel_adr")
        out.append(dict(name=name, attend=attend, new_vis=new_vis, sp_new=sp_new, extra_days=extra_days, sp_stay=sp_stay,
                        lodge_stay=lodge_stay, spend=spend, rn=rn, room_rev=room_rev, tot=room_rev * TOT,
                        ana_impact=spend * MULT_ANA, ana_jobs=spend / 1e6 * JOBS_ANA, ana_tax=spend * TAX_ANA,
                        oc_impact=spend * MULT_OC, oc_jobs=spend / 1e6 * JOBS_OC, oc_tax=spend * TAX_OC,
                        ca_spend=spend * OUT_OF_STATE, ca_jobs=spend * OUT_OF_STATE / 1e6 * JOBS_CA, ca_tax=spend * OUT_OF_STATE * TAX_CA,
                        share_ana=spend / (A["sp25"] * 1e6) * 100, share_oc=spend / (O["sp25"] * 1e6) * 100,
                        share_ca=spend * OUT_OF_STATE / CA["spend"] * 100))
    return out

# Per-1% sensitivities (for "what one more night means for OC Vibe")
PER_1PCT_DAY = A["vis25"] * 1e6 * 0.01 * PER_DAY             # every 1% of visitors adding a day
PER_1PCT_LODGE = A["vis25"] * 1e6 * 0.01 * LODGE_PER_VDAY      # lodging part of that
PER_1K_NEW = 1000 * PV                                         # every 1,000 net-new visitors
PER_100_EVENTS = HALL_CAP * 100 * 0.80                         # attendees from 100 concert-hall events at 80% fill
RES = run()

if __name__ == "__main__":
    print(f"PV {PV}  per-day {PER_DAY:.2f}  lodge/vday {LODGE_PER_VDAY:.2f}  mult {MULT_ANA:.4f} jobs/$M {JOBS_ANA:.3f} tax {TAX_ANA:.4f}")
    print(f"OC mult {MULT_OC:.4f} jobs {JOBS_OC:.3f} tax {TAX_OC:.4f}  CA jobs {JOBS_CA:.3f} tax {TAX_CA:.4f}  out-of-state {OUT_OF_STATE:.3f}")
    print(f"per 1% day {PER_1PCT_DAY/1e6:.1f}M lodge {PER_1PCT_LODGE/1e6:.2f}M  per 1k new {PER_1K_NEW/1e3:.0f}K")
    for r in RES:
        print({k: (round(v / 1e6, 2) if isinstance(v, float) and v > 1e5 else (round(v, 3) if isinstance(v, float) else v)) for k, v in r.items()})

# ---------- Transportation and other effects (base case unless noted) ----------
HONDA_SEATS = 18300                     # Honda Center seats (LARC, "18,300+")
PARKING = (12369, 12823)                # planned OCVIBE parking spaces (City of Anaheim)
TRANS = dict(car_share=0.90, per_car=(2.0, 2.5), transit_share=0.05, bus_load=60)   # BI assumptions
def transport():
    b = RES[1]
    car_share, (pc_lo, pc_hi) = TRANS["car_share"], TRANS["per_car"]
    hall_sell = HALL_CAP * car_share
    both_sell = (HALL_CAP + HONDA_SEATS) * car_share
    return dict(
        veh_round_trips_yr=b["attend"] * car_share / 2.5,
        hall_vehicles=(hall_sell / pc_hi, hall_sell / pc_lo),
        both_vehicles=(both_sell / pc_hi, both_sell / pc_lo),
        both_parking_share=(both_sell / pc_hi / PARKING[1], both_sell / pc_lo / PARKING[0]),
        hall_trips=hall_sell / pc_hi * 2,
        hall_vs_katella=hall_sell / pc_hi * 2 / 36000, hall_vs_sr57=hall_sell / pc_hi * 2 / 275000,
        transit_riders=HALL_CAP * TRANS["transit_share"], bus_loads=HALL_CAP * TRANS["transit_share"] / TRANS["bus_load"],
        transport_spend=b["spend"] * A["transport"] / A["sp25"],
    )
TR = transport()
SHARES = [("Recreation and entertainment", A["rec"]), ("Lodging", A["lodging"]), ("Retail", A["retail"]), ("Food and beverage", A["fb"]), ("Transportation", A["transport"])]
def by_category():
    b = RES[1]; tot = sum(v for _, v in SHARES)
    return [(n, v / tot, b["spend"] * v / tot) for n, v in SHARES]
CAT = by_category()
FB_JOBS = [x for x in CAT if x[0] == "Food and beverage"][0][2] / 1e6 * (A["fb_jobs"] / A["fb"])
def ten_year():
    b = RES[1]; hall_only = HALL_CAP * ASSUME["hall_events"][1] * ASSUME["hall_fill"][1] * ASSUME["net_new"][1] * PV
    yrs = list(range(2027, 2037))
    spend = [hall_only + b["sp_stay"] * 0.5] + [b["spend"]] * 9
    rooms = [0, 230, 230] + [550] * 7          # second hotel assumed 2030 (City: 2029–2032)
    tot = [r * 365 * ASSUME["hotel_occ"][1] * ASSUME["hotel_adr"][1] * TOT for r in rooms]
    return dict(yrs=yrs, spend=sum(spend), impact=sum(spend) * MULT_ANA, tax=sum(spend) * TAX_ANA, tot=sum(tot), rn=sum(r * 365 * ASSUME["hotel_occ"][1] for r in rooms))
TEN = ten_year()

if __name__ == "__main__":
    print(TR); print([(n, round(s*100,1), round(v/1e6,2)) for n,s,v in CAT], round(FB_JOBS)); print({k:(round(v/1e6,1) if isinstance(v,float) else v) for k,v in TEN.items()})

# Constants for the in-page calculator (OC Vibe staff inputs)
JS_MODEL = dict(pv=PV, per_day=PER_DAY, visitors=A["vis25"] * 1e6, mult_ana=MULT_ANA, jobs_ana=JOBS_ANA, tax_ana=TAX_ANA, mult_oc=MULT_OC,
                out_of_state=OUT_OF_STATE, hall_cap=HALL_CAP, small_cap=SMALL_CAP, tot=TOT, ana_today_sp=A['sp25'] * 1e6, ocv_today_sp=0.052 * A['sp25'] * 1e6,
                base=dict(hall_events=150, hall_fill=80, small_events=150, small_fill=70, net_new=25, add_day=1.0, rooms=550, occ=round(CS_OC["occ"]), adr=CS_OC["adr"]))

# ---------- Three views of impact (holistic) ----------
# 1) Anaheim today: all visitors (Tourism Economics 2025).
# 2) Anaheim with OC Vibe live: today + OC Vibe's net-new visitor activity (base case and range).
# 3) OC Vibe's own impact: visitor activity associated with the OC Vibe area today (Datafy: 5.2% of Anaheim visitor days, 2024),
#    and when live (today + net-new). "Associated" = all spending on visitor days that include the area, wherever it is spent.
DATAFY_SHARE = 0.052
VDAYS = A["vis25"] * 1e6 * N["los"]
def views(r):
    sp_today = A["sp25"] * 1e6
    nv_days = r["new_vis"] * N["los"]
    ocv_vd0 = DATAFY_SHARE * VDAYS; ocv_sp0 = DATAFY_SHARE * sp_today
    ocv_vd1 = ocv_vd0 + nv_days + r["extra_days"]; ocv_sp1 = ocv_sp0 + r["spend"]
    def block(vis, vd, sp, rn=None):
        return dict(visitors=vis, vdays=vd, spend=sp, impact=sp * MULT_ANA, jobs=sp / 1e6 * JOBS_ANA, tax=sp * TAX_ANA)
    return dict(
        ana_today=block(A["vis25"] * 1e6, VDAYS, sp_today) | dict(impact=A["impact"] * 1e6, jobs=A["jobs"], tax=A["sl_tax"] * 1e6),
        ana_live=block(A["vis25"] * 1e6 + r["new_vis"], VDAYS + nv_days + r["extra_days"], sp_today + r["spend"]) | dict(
            impact=A["impact"] * 1e6 + r["ana_impact"], jobs=A["jobs"] + r["ana_jobs"], tax=A["sl_tax"] * 1e6 + r["ana_tax"]),
        ocv_today=block(None, ocv_vd0, ocv_sp0) | dict(share=DATAFY_SHARE * 100),
        ocv_live=block(None, ocv_vd1, ocv_sp1) | dict(share=ocv_vd1 / (VDAYS + nv_days + r["extra_days"]) * 100, hotel_rn=r["rn"], hotel_tot=r["tot"]),
        oc_today=dict(spend=O["sp25"] * 1e6, impact=O["impact"] * 1e6, jobs=O["jobs"]),
        oc_live=dict(spend=O["sp25"] * 1e6 + r["spend"], impact=O["impact"] * 1e6 + r["oc_impact"], jobs=O["jobs"] + r["oc_jobs"]),
        ca_today=dict(spend=CA["spend"]), ca_live=dict(spend=CA["spend"] + r["ca_spend"]),
    )
VIEWS = {r["name"]: views(r) for r in RES}
if __name__ == "__main__":
    import json
    for k, v in VIEWS["Base"].items(): print(k, {a: (round(b / 1e6, 1) if b and b > 1e5 else (round(b, 2) if b else b)) for a, b in v.items()})
