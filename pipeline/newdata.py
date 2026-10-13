"""New datasets added Oct. 12, 2026: STR daily (Visit Anaheim sets), CoStar monthly submarkets, Visa Destination Insights, Amtrak ANA, Metrolink."""
import os as _os
BASE = _os.path.dirname(_os.path.abspath(__file__))  # pipeline folder
import pandas as pd
F = BASE + "/files/licensed/"

# ---------- STR daily, Visit Anaheim hotel sets (Jan. 1–Oct. 3, 2026) ----------
_s = pd.read_excel(F + "STR_Daily_Data_8.xlsx"); _s["Date"] = pd.to_datetime(_s["Date"])
STR_FROM, STR_TO = _s.Date.min(), _s.Date.max()
def _str(geo):
    t = _s[(_s.Geography == geo) & (_s.Segment == "Total")]
    sup, dem, rev = t.Supply.sum(), t.Demand.sum(), t.Revenue.sum()
    dow = {d: (x.Demand.sum() / x.Supply.sum() * 100, x.Revenue.sum() / x.Demand.sum()) for d, x in t.groupby("Day Of Week Category")}
    seg = _s[(_s.Geography == geo) & (_s.Segment != "Total")].groupby("Segment")[["Demand", "Revenue"]].sum()
    full = t[t.Date < "2026-10-01"]
    mo = {m: (x.Demand.sum() / x.Supply.sum() * 100, x.Revenue.sum() / x.Demand.sum(), x.Revenue.sum() / x.Supply.sum()) for m, x in full.groupby(full.Date.dt.month)}
    return dict(rooms=int(t.Supply.iloc[-1]), occ=dem / sup * 100, adr=rev / dem, revpar=rev / sup, nights=len(t),
                n90=int((t.Occupancy >= 0.9).sum()), n95=int((t.Occupancy >= 0.95).sum()), dow=dow,
                group_share=seg.loc["Group", "Demand"] / dem * 100, group_adr=seg.loc["Group", "Revenue"] / seg.loc["Group", "Demand"],
                trans_share=seg.loc["Transient", "Demand"] / dem * 100, trans_adr=seg.loc["Transient", "Revenue"] / seg.loc["Transient", "Demand"], mo=mo)
STR = {g: _str(g) for g in ["Anaheim+", "Anaheim-Garden Grove+", "Garden Grove+"]}
A_ = STR["Anaheim+"]
SUNMON_OCC = (A_["dow"]["Sun"][0] + A_["dow"]["Mon"][0]) / 2
FRISAT_OCC = (A_["dow"]["Fri"][0] + A_["dow"]["Sat"][0]) / 2
SUNMON_ADR = (A_["dow"]["Sun"][1] + A_["dow"]["Mon"][1]) / 2
PT_SUNMON_RN = A_["rooms"] * 0.01 * 104                    # each 1 point of Sun+Mon occupancy over a year (104 nights)
PT_SUNMON_REV = PT_SUNMON_RN * SUNMON_ADR

# ---------- CoStar monthly submarkets (Jan.–Aug. 2026) ----------
_c = pd.read_excel(F + "CoStar_DataExport_17.xlsx")
_M = ["01/31/2026", "02/28/2026", "03/31/2026", "04/30/2026", "05/31/2026", "06/30/2026", "07/31/2026", "08/31/2026"]
def cs(concept, sub):
    r = _c[(_c["Concept Name"] == concept) & (_c["Geography Name"].str.endswith(" - " + sub))]
    return [float(r[m].iloc[0]) for m in _M]
CS_MO = {sub: dict(occ=cs("Occupancy", sub), adr=cs("ADR", sub), revpar=cs("RevPAR", sub), rchg=cs("RevPAR Chg (YOY)", sub),
                   occ12=cs("12 Mo Occupancy", sub)[-1], adr12=cs("12 Mo ADR", sub)[-1], revpar12=cs("12 Mo RevPAR", sub)[-1])
         for sub in ["Disneyland", "Anaheim", "Newport Beach/Dana Point", "Santa Ana/Costa Mesa", "Orange County Northwest/Fullerton"]}

# ---------- Visa Destination Insights via Symphony (Aug. 2026) ----------
VISA = dict(total=464.6, total_chg=8.1, dom=446.6, dom_chg=8.7, intl=17.9, intl_chg=-5.0, cards=5.4, cards_chg=3.2,
            ticket=43, ticket_chg=3.5, per_card=85, per_card_chg=4.7, tx=10.9, tx_chg=4.4, intl_per_card=125, intl_per_card_chg=-8.9)
VISA_ORIG = [("Los Angeles–Long Beach–Anaheim", 307.3), ("Riverside–San Bernardino–Ontario", 28.9), ("San Diego–Chula Vista–Carlsbad", 10.5),
             ("San Francisco–Oakland–Berkeley", 8.6), ("Seattle–Tacoma–Bellevue", 5.4), ("Mexico", 5.2), ("Phoenix–Mesa–Chandler", 4.9),
             ("Las Vegas–Henderson–Paradise", 4.5), ("San Jose–Sunnyvale–Santa Clara", 4.5), ("Sacramento–Roseville–Folsom", 3.8),
             ("Orlando–Kissimmee–Sanford", 3.4), ("New York–Newark–Jersey City", 3.3), ("Canada", 3.2), ("Oxnard–Thousand Oaks–Ventura", 2.8), ("Detroit–Warren–Dearborn", 2.5)]
VISA_INTL_CAT = [("Retail", 6.9, 9.3), ("Restaurants and dining", 5.4, -19.1), ("Hotels and lodging", 2.6, -3.6), ("Other", 1.7, 6.4), ("Entertainment", 0.75, -32.7), ("Transportation", 0.6078, 19.4)]
VISA_INTL_CTRY = [("Mexico", 5.2), ("Canada", 3.2), ("Japan", 2.4), ("United Kingdom", 1.4), ("China (mainland)", 0.7967), ("Australia", 0.5943), ("France", 0.3707), ("Germany", 0.2721), ("Taiwan", 0.2475), ("South Korea", 0.1949)]

# ---------- Amtrak, Anaheim station (ANA, at ARTIC) — Rail Passengers Association fact sheet, 2024 data ----------
AMTRAK = dict(yrs={2018: 256.6, 2019: 242.0, 2020: 112.6, 2021: 71.9, 2022: 163.8, 2023: 70.7, 2024: 191.2}, pax24=191153, trip=76, fare=28.00,
              lt100=89.5, pop25=7944259, pop50=15630674, pairs=["San Diego", "Los Angeles", "San Diego Old Town", "Solana Beach", "Oceanside"])
# ---------- Metrolink, FY2025-26 Q2 (Oct.–Dec. 2025) fact sheet ----------
METRO = dict(sys_wk=23945, sys_wk_chg=-2, sys_we=235661, sys_we_chg=-22, oc_wk=5116, oc_wk_chg=4, oc_we=50778, oc_we_chg=-6,
             ieoc_wk=2331, ieoc_wk_chg=6, ieoc_we=15964, ieoc_we_chg=-41, noncommute=55, hhi=90399, trip=38)

if __name__ == "__main__":
    print(STR_FROM, STR_TO)
    for g, v in STR.items(): print(g, {k: (round(x, 1) if isinstance(x, float) else x) for k, x in v.items() if k not in ("dow", "mo")})
    print(round(SUNMON_OCC, 1), round(FRISAT_OCC, 1), round(SUNMON_ADR, 2), round(PT_SUNMON_RN), round(PT_SUNMON_REV))
    print({k: (round(v['occ12'], 3), round(v['adr12'], 2)) for k, v in CS_MO.items()})
    print(sum(v for _, v in VISA_ORIG), 307.3 / 464.6)
