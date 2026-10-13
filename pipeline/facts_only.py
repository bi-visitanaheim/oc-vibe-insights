"""Facts only (John Picou, Oct. 13, 2026): no assumptions that cannot be backed with data.

 - Removes the Visit Anaheim BI scenario model from the report (the $90.5M estimate, net-new and add-a-day assumptions,
   event counts, OC Vibe hotel occupancy, parking and vehicle estimates, ten-year totals, simulation range).
 - Tourism Economics covers the City of Anaheim only; it is not allocated to OC Vibe.
 - Shows calendar 2025 results (Tourism Economics, published 2026) beside Tourism Economics' 2026 forecast.
 - The OC Vibe section becomes "Anaheim and OC Vibe today": measured figures for Anaheim and the OC Vibe area as they are now.
"""
import re, json
import data as D, newdata as ND, impact as I
from data import EI
import logic_content as L, ocv_whole as OW, roles_content as RC

A = EI["Anaheim"]
YR = D.YEARS; i25, i26 = YR.index(2025), YR.index(2026)
VIS25, VIS26 = D.ANA_VIS[i25], D.ANA_VIS[i26]
SP25, SP26 = A["sp25"] / 1000, D.ANA_SP[i26]
PV25, PV26 = D.ANA_PV[i25], D.ANA_PV[i26]
S_TE = "Tourism Economics, Economic Impact of Visitors (calendar 2025; pub. 2026)"
S_TEF = "Tourism Economics, Anaheim Travel Forecast (Sept. 2026)"
S_PR = OW.S_PR; S_OCBJ26 = OW.S_OCBJ26
CAT = [("Recreation and entertainment", A["rec"]), ("Lodging", A["lodging"]), ("Retail", A["retail"]), ("Food and beverage", A["fb"]), ("Transportation", A["transport"])]
CAT_SUM = sum(v for _, v in CAT)

EST_RX = re.compile(r"(\$90\.5M|\$90M|\$446M|\$355M|\$6\.92B|\$138M|base case|base-case|scenario model|net-new|8,600–10,800|67%–87%|141K–157K|\$71M–\$122M|simulation|\$85\.7M|first ten years|views 2 and 3|associated visitor spending|OC Vibe's own associated)", re.I)

# ---------------- the rebuilt OC Vibe section ----------------
T_ANA = dict(title="Anaheim's visitor economy: 2025 results and 2026 forecast", sub="City of Anaheim only · Tourism Economics · 2025 measured (published 2026); 2026 is Tourism Economics' forecast",
             cols=[["Measure", 0], ["2025 (measured)", 1], ["2026 (forecast)", 1], ["Change", 1], ["How it's calculated", 0]],
             rows=[["Visitors", f"{VIS25:.1f}M", f"{VIS26:.1f}M", "+1.9%", "Reported by Tourism Economics; change as published (Sept. 2026 forecast)"],
                   ["Visitor spending", f"${SP25:.2f}B", f"${SP26:.1f}B", "+5.6%", "Reported by Tourism Economics; change as published (Sept. 2026 forecast)"],
                   ["Spending per visitor", f"${PV25:.0f}", f"${PV26:.0f}", f"+{(PV26/PV25-1)*100:.1f}%", f"${SP25:.3f}B ÷ {VIS25:.1f}M = ${PV25:.0f}; ${SP26:.1f}B ÷ {VIS26:.1f}M = ${PV26:.0f}"],
                   ["Total economic impact", f"${A['impact']/1000:.2f}B", "Not forecast", "—", "Reported by Tourism Economics (direct, indirect and induced)"],
                   ["Jobs supported", f"{A['jobs']:,}", "Not forecast", "—", "Reported by Tourism Economics; 32.8% of all Anaheim jobs"],
                   ["State and local taxes", f"${A['sl_tax']:,.0f}M", "Not forecast", "—", "Reported by Tourism Economics"],
                   ["Day visitors", f"{A['day_share']}%", "Not forecast", "—", "17.9M day visitors ÷ 26.5M visitors (Tourism Economics)"]],
             hi=1, wide=True, src=f"{S_TE}; {S_TEF}")
T_AREA = dict(title="The OC Vibe area today, before the new venues open", sub="Measured or published figures only; each with its source and period",
              cols=[["Measure", 0], ["Value", 1], ["Period", 0], ["Source", 0]],
              rows=[["OC Vibe area share of Anaheim visitor days", "5.2%", "Calendar 2024", "Datafy"],
                    ["District 5 visitors who stay overnight", "85.8%", "Jan.–May 2026", "Azira via Symphony"],
                    ["District 5 first-time visitors", "43.8%", "Jan.–May 2026", "Azira via Symphony"],
                    ["District 5 domestic visitors from outside California", f"{100-D.D5_STATE[0][1]:.0f}%", "Jan.–May 2026", "Azira via Symphony"],
                    ["Busiest day for District 5 visits", "Saturday (15.9%)", "Jan.–May 2026", "Azira via Symphony"],
                    ["Vehicles on SR-57 beside the district", "275,000 a weekday", "Caltrans 2024 count", "OCTA Traffic Flow Map (Aug. 2026)"],
                    ["Weekday OCTA bus trips stopping at ARTIC", "277 (11 leave after 10 p.m.)", "Schedules Aug.–Nov. 2026", "OCTA"],
                    ["Amtrak passengers at Anaheim (ARTIC)", "191,153", "2024", "Rail Passengers Association"],
                    ["Honda Center seats", "18,300+", "2026", "LARC (Sept. 2026)"],
                    ["Concert hall capacity", "5,000 (OCVIBE) / 5,613 (City)", "Mar. 2026 / 2026", "OCVIBE release; City of Anaheim"],
                    ["Planned hotel rooms at OC Vibe", "550 (two hotels)", "2026", "City of Anaheim OCVibe page"],
                    ["Planned parking spaces", "12,369–12,823", "2026", "City of Anaheim OCVibe page"]],
              hi=0, wide=True, src="Datafy (2024); Azira via Symphony (Jan.–May 2026); OCTA (2026); Rail Passengers Association (2024 data); LARC (Sept. 2026); OCVIBE (Mar. 2026); City of Anaheim (2026)")
T_MIX = dict(title="Where Anaheim visitor spending goes, by category", sub="City of Anaheim, calendar 2025 · Tourism Economics (published 2026)",
             cols=[["Category", 0], ["Spending", 1], ["Share", 1], ["How it's calculated", 0]],
             rows=[[c, f"${v:,.0f}M", f"{v/A['sp25']*100:.1f}%", f"${v:,.0f}M ÷ ${A['sp25']:,.0f}M total visitor spending"] for c, v in CAT] +
                  [["Total", f"${CAT_SUM:,.0f}M", f"{CAT_SUM/A['sp25']*100:.1f}%", f"Sum of categories; Tourism Economics total ${A['sp25']:,.0f}M (difference is rounding)"]],
             hi=3, wide=True, src=S_TE)
T_PUB = dict(title="Figures OC Vibe's developers and others have published", sub="Published by others, shown as reported; not produced or checked by Visit Anaheim BI",
             cols=[["Published by", 0], ["Figures", 0], ["Scope", 0]],
             rows=[["OCVIBE fact sheet (Apr. 2024)", "3,000+ ongoing jobs; about $10M a year in tax revenue to Anaheim; $255M in public benefits", "Whole district: office, residents, local patrons and visitors"],
                   ["DTA analysis, cited by Visit Anaheim (June 2020)", "More than $400M a year in recurring economic impact; 3,300 permanent jobs; $2B one-time construction impact", "Whole district, earlier and larger program"]],
             hi=-1, wide=True, src="OCVIBE fact sheet (Apr. 2024); Visit Anaheim article (June 24, 2020)")

S_ALL = f"{S_TE}; {S_TEF}; {L.S_DATAFY}; {L.S_AZIRA}"
NEW_OCV = dict(
  id="p-ocv", tab="Anaheim and OC Vibe today",
  q="Where do Anaheim's visitor economy and the OC Vibe area stand today?",
  period="Tourism Economics: 2025 results (pub. 2026) and 2026 forecast (Sept. 2026) · Datafy 2024 · Azira Jan.–May 2026",
  head=f"Anaheim welcomed {VIS25:.1f} million visitors who spent ${SP25:.2f} billion in 2025",
  dek=f"Tourism Economics forecasts {VIS26:.1f} million visitors and ${SP26:.1f} billion for 2026; the OC Vibe area already accounts for 5.2% of Anaheim visitor days.",
  ans=(f"In 2025, {VIS25:.1f}M visitors spent ${SP25:.2f}B in Anaheim, ${PV25:.0f} each (${SP25:.3f}B ÷ {VIS25:.1f}M), and supported {A['jobs']:,} jobs (Tourism Economics, published 2026). "
       f"Tourism Economics forecasts {VIS26:.1f}M visitors (+1.9%) and ${SP26:.1f}B (+5.6%) for 2026. These are City of Anaheim totals; they do not measure OC Vibe. "
       f"For the OC Vibe area today, Datafy measured 5.2% of Anaheim visitor days in 2024, and 85.8% of District 5 visitors stay overnight (Azira, Jan.–May 2026)."),
  ans_src=S_ALL,
  hv=f"${SP25:.2f}B", hl="Anaheim visitor spending, 2025 (Tourism Economics)",
  cards=[["Anaheim, 2025", "Visitors", f"{VIS25:.1f}M", f"▲ +0.8% vs. 2024 · 2026 forecast {VIS26:.1f}M", "Tourism Economics (2025; pub. 2026)"],
         ["Anaheim, 2025", "Visitor spending", f"${SP25:.2f}B", f"▲ +3.1% vs. 2024 · 2026 forecast ${SP26:.1f}B", "Tourism Economics (2025; pub. 2026)"],
         ["Anaheim, 2025", "Jobs supported by visitors", f"{A['jobs']:,}", f"32.8% of all jobs · ${A['impact']/1000:.1f}B total impact", "Tourism Economics (2025; pub. 2026)"],
         ["OC Vibe area, 2024", "Share of Anaheim visitor days", "5.2%", "Measured before the new venues open", "Datafy (2024)"]],
  tables=[T_ANA, T_AREA, T_MIX, T_PUB], charts=[],
  notes=["Tourism Economics figures cover the City of Anaheim. They are not allocated to OC Vibe, and this report does not estimate OC Vibe's impact: no OC Vibe attendance, ticketing or hotel data exists yet.",
         "2025 figures are measured results published in 2026; 2026 figures are Tourism Economics' forecast (Sept. 2026). Changes for 2026 are as Tourism Economics published them; the rounded values shown may differ slightly.",
         "Change vs. 2024: visitors 26.3M to 26.5M (+0.8%); spending $6.626B to $6.832B (+3.1%), both from Tourism Economics.",
         "Concert hall capacity differs by source: 5,000 (OCVIBE release, Mar. 12, 2026) and 5,613 (City of Anaheim, 2026). Confirm with OC Vibe."],
  w5h=dict(who="Visitors to the City of Anaheim (travelling 50+ miles or staying overnight) and visitors to District 5, where OC Vibe is being built.",
           what=f"Anaheim: {VIS25:.1f}M visitors, ${SP25:.2f}B spending, {A['jobs']:,} jobs and ${A['sl_tax']:,.0f}M state and local taxes in 2025; Tourism Economics forecasts {VIS26:.1f}M visitors and ${SP26:.1f}B in 2026. OC Vibe area: 5.2% of Anaheim visitor days (2024).",
           when="Calendar 2025 (measured, published 2026); 2026 forecast published Sept. 2026; Datafy calendar 2024; Azira Jan.–May 2026.",
           where="City of Anaheim; the OC Vibe area around Honda Center and ARTIC in Council District 5.",
           why="A measured baseline before OC Vibe's venues open in 2027, so OC Vibe's own results can be compared with it later.",
           how="Tourism Economics visitor and spending models for Anaheim; Datafy and Azira mobile location data for the area; no Visit Anaheim BI assumptions.",
           src=S_ALL),
  cc=[dict(type="Growth", point=f"Tourism Economics forecasts Anaheim visitor spending of ${SP26:.1f}B in 2026, up 5.6%, with visitors up 1.9% to {VIS26:.1f}M.", solution=None, src=S_TEF),
      dict(type="Opportunity", point="The OC Vibe area already accounts for 5.2% of Anaheim visitor days, a measured starting point.", solution=None, src=L.S_DATAFY),
      dict(type="Quick win", point="Capture ticket-buyer ZIP codes from the first 2027 shows so OC Vibe's visitors can be measured, not estimated.", solution=None, src=L.S_AZIRA),
      dict(type="Early hurdle", point="No OC Vibe attendance, ticketing or hotel data exists yet.", solution="Agree a quarterly data exchange with Visit Anaheim BI before the 2027 openings.", src=L.S_DATAFY),
      dict(type="Pitfall", point="Citywide Tourism Economics totals do not measure OC Vibe.", solution="Report OC Vibe with its own ticketing, hotel and card data and Datafy's area share, not a share of city totals.", src=S_TE),
      dict(type="Explanation", point="Tourism Economics measures visitors and spending for the City of Anaheim; Datafy and Azira measure activity in specific areas, such as the OC Vibe area and District 5.", solution=None, src=f"{S_TE}; {L.S_DATAFY}; {L.S_AZIRA}")],
  for_ocv=dict(
    enhance=[dict(tag="Strategy", text=f"A measured baseline: {VIS25:.1f}M visitors and ${SP25:.2f}B spending in 2025, with Tourism Economics forecasting ${SP26:.1f}B for 2026.", src=f"{S_TE}; {S_TEF}",
                  calc=f"${SP25:.3f}B ÷ {VIS25:.1f}M = ${PV25:.0f} per visitor (2025); ${SP26:.1f}B ÷ {VIS26:.1f}M = ${PV26:.0f} (2026 forecast)"),
             dict(tag="Measurement", text="The OC Vibe area already accounts for 5.2% of Anaheim visitor days (2024), the starting point for measuring growth.", src=L.S_DATAFY),
             dict(tag="Marketing", text=f"District 5 visitors are 85.8% overnight and 43.8% first-time, and {100-D.D5_STATE[0][1]:.0f}% of domestic visitors come from outside California.", src=L.S_AZIRA,
                  calc=f"100% − {D.D5_STATE[0][1]:.1f}% from California = {100-D.D5_STATE[0][1]:.0f}%"),
             dict(tag="Programming", text="Visitors spend most on recreation and entertainment (34.0%), then lodging (25.2%), retail (21.9%) and food and beverage (15.6%).", src=S_TE,
                  calc=f"Recreation ${A['rec']:,.0f}M, lodging ${A['lodging']:,.0f}M, retail ${A['retail']:,.0f}M, food and beverage ${A['fb']:,.0f}M ÷ ${A['sp25']:,.0f}M total")],
    need=[dict(tag="Measurement", text="Ticket-buyer ZIP codes from the first 2027 shows, to measure how many attendees travel 50+ miles.", src=L.S_AZIRA),
          dict(tag="Hotels", text="Occupancy, rate and guest origin from OC Vibe's hotels once open (first hotel 2028), reported monthly.", src=S_OCBJ26),
          dict(tag="Measurement", text="A confirmed concert hall capacity: 5,000 seats (OCVIBE, Mar. 2026) vs. 5,613 (City of Anaheim, 2026).", src=f"{S_PR}; {L.S_CITY}"),
          dict(tag="Strategy", text="One shared scorecard built on today's baselines (5.2% of visitor days, 2.17-day average stay, 85.8% overnight), refreshed quarterly with Visit Anaheim BI.", src=f"{L.S_DATAFY}; {L.S_AZIRA}",
               calc="2.17 days = 93.2% domestic × 1.9 days + 6.8% international × 5.9 days (Tourism Economics; Azira)")]),
  calc_steps=[["Spending per visitor, 2025", f"${SP25:.3f}B ÷ {VIS25:.1f}M visitors", f"${PV25:.0f}", "Tourism Economics (2025)"],
              ["Spending per visitor, 2026 forecast", f"${SP26:.1f}B ÷ {VIS26:.1f}M visitors", f"${PV26:.0f}", "Tourism Economics forecast (Sept. 2026)"],
              ["Visitors, 2026 vs. 2025", "Reported", "+1.9%", "Tourism Economics forecast (Sept. 2026)"],
              ["Visitor spending, 2026 vs. 2025", "Reported", "+5.6%", "Tourism Economics forecast (Sept. 2026)"],
              ["Jobs supported, 2025", "Reported", f"{A['jobs']:,}", "Tourism Economics (2025)"],
              ["OC Vibe area share of visitor days", "Reported", "5.2%", "Datafy (2024)"]],
  feature=[dict(kind="cols", title=f"Anaheim visitor spending reached ${SP25:.1f} billion in 2025; Tourism Economics forecasts ${D.ANA_SP[-1]:.1f} billion by 2028",
                sub="City of Anaheim, $ billions · 2019–2025 measured; 2026–2028 forecast (Sept. 2026)",
                rows=[dict(l=str(y), v=v, t=f"${v:.1f}B", fc=y >= 2026, hi=y == 2025) for y, v in zip(YR, D.ANA_SP)], src=S_TEF),
           dict(kind="line", title=f"Visitors returned to {VIS25:.1f} million in 2025, above 2019's 24.2 million",
                sub="City of Anaheim visitors, millions · 2026–2028 are Tourism Economics' forecast",
                x=[str(y) for y in YR], series=[dict(name="Visitors", v=D.ANA_VIS, focal=True)], yfmt=dict(suf="M", dec=1), src=S_TEF)],
  more_charts=[], card_calc=[f"Reported by Tourism Economics; 26.3M (2024) → 26.5M (2025) = +0.8%", f"Reported; $6.626B (2024) → $6.832B (2025) = +3.1%", "Reported by Tourism Economics", "Reported by Datafy"],
)


def _clean_item(it):
    return not EST_RX.search(it["text"])


def attach(SECTIONS, TAKEAWAYS, DQ, STORIES, MAIN, SOURCES, REGISTER):
    # 1) replace the OC Vibe impact section
    for i, s in enumerate(SECTIONS):
        if s["id"] == "p-ocv":
            old = next((t for t in s["tables"] if t["title"] == "Measures OC Vibe can build on"), None)
            if old:
                ci = [j for j, c in enumerate(old["cols"]) if c[0] not in ("Marker", "How it's calculated")]
                rows = [[r[j] for j in ci] for r in old["rows"]]
                rows = [r for r in rows if not EST_RX.search(" ".join(map(str, r)))]
                NEW_OCV["tables"].insert(3, dict(title="Measures OC Vibe can build on", sub="Today's baselines from measured data; OC Vibe adds its own results once open",
                                                 cols=[old["cols"][j] for j in ci], rows=rows, hi=-1, wide=True, src=old.get("src", "")))
            SECTIONS[i] = NEW_OCV
    STORIES["p-ocv"] = dict(STORIES.get("p-ocv", {}), head=NEW_OCV["head"], dek=NEW_OCV["dek"], measure="Anaheim visitor spending, 2025", val=f"${SP25:.2f}B", basis="Measured (Tourism Economics)",
                            lede=NEW_OCV["ans"], paras=[], stats=[[c[2], c[1] + ", " + c[0], c[4]] for c in NEW_OCV["cards"]],
                            chart=dict(title="Anaheim visitor spending, $ billions", src=S_TEF, rows=[[str(y), v, f"${v:.1f}B", y == 2025] for y, v in zip(YR, D.ANA_SP)]),
                            srcs=[S_TE, S_TEF, L.S_DATAFY, L.S_AZIRA])
    # 2) strip estimate-based statements elsewhere
    for s in SECTIONS:
        sid = s["id"]
        if s.get("ocv"): s["ocv"] = [x for x in s["ocv"] if not EST_RX.search(x)]
        if s.get("for_ocv") and sid != "p-ocv":
            for kind in s["for_ocv"]:
                s["for_ocv"][kind] = [it for it in s["for_ocv"][kind] if _clean_item(it)]
        s["notes"] = [n for n in s["notes"] if not EST_RX.search(n)]
        if sid == "p-impact":
            s["notes"].append(f"Ratios from Tourism Economics 2025: about {I.JOBS_ANA:.1f} jobs and about ${round(I.TAX_ANA*1e6,-3):,.0f} in state and local taxes per $1M of visitor spending ({A['jobs']:,} jobs ÷ ${A['sp25']:,.0f}M; ${A['sl_tax']:,.0f}M ÷ ${A['sp25']:,.0f}M).")
            s["for_ocv"]["enhance"].insert(0, dict(tag="Community", text=f"Each $1M of visitor spending in Anaheim supports about {I.JOBS_ANA:.1f} jobs and about ${round(I.TAX_ANA*1e6,-3):,.0f} in state and local taxes (2025).",
                                                   src=L.S_TE_EI, calc=f"{A['jobs']:,} jobs ÷ ${A['sp25']:,.0f}M = {I.JOBS_ANA:.1f} per $1M; ${A['sl_tax']:,.0f}M ÷ ${A['sp25']:,.0f}M = {I.TAX_ANA*100:.1f}%"))
        if sid == "p-transport":
            s["for_ocv"]["need"].insert(0, dict(tag="Operations", text="An event-night plan: Honda Center (18,300+ seats) and the concert hall (5,000 seats) can hold events the same night, and the City lists 12,369–12,823 planned parking spaces.",
                                                src=f"{L.S_LARC}; {S_PR}; {L.S_CITY}"))
            s["cc"] = [c if c["type"] != "Pitfall" else dict(type="Pitfall", point="Honda Center and the concert hall can both hold events on the same night, while late transit is thin (11 buses after 10 p.m.).",
                                                              solution="Coordinate event start times and parking plans with Honda Center, and ask OCTA for event-night service.", src=f"{L.S_LARC}; {L.S_OCTA}") for c in s["cc"]]
        if sid == "p-hotel":
            s["for_ocv"]["enhance"].insert(0, dict(tag="Hotels", text="OC Vibe plans 550 rooms in two hotels, while only 668 rooms are under construction across Orange County.", src=f"{L.S_CITY}; {L.S_COSTAR}"))
        if sid == "p-night":
            s["ans"] = ("If every Anaheim visitor stayed one more night, lodging spending would rise about $794M ($1.724B 2025 lodging spending ÷ 2.17-day average stay; Visit Anaheim Extra Night study). "
                        "Each 1% of Anaheim visitors who stay one more day adds about $31.5M in visitor spending (26.5M visitors × 1% × $118.71 per visitor day).")
        if sid == "p-appx":
            for t in s["tables"]:
                if t["title"] == "Formulas":
                    keep = {"Spending per visitor", "Weighted length of stay", "Spending per visitor day", "One more night (lodging)", "Value of 1% adding a day", "Value of one Sun–Mon occupancy point", "RevPAR"}
                    t["rows"] = [r for r in t["rows"] if r[0] in keep]
                    t["hi"] = -1
                if t["title"] == "Glossary":
                    drop = {"Associated spending", "Base case", "Bootstrap", "Confidence interval (CI)", "Monte Carlo simulation", "Net-new visitor", "p-value", "Percentile (P5, P50, P95)", "Scenario", "Sensitivity analysis", "Sign test", "Welch t-test / Mann–Whitney test"}
                    t["rows"] = [r for r in t["rows"] if r[0] not in drop]
                if t["title"] == "Methods":
                    t["rows"] = [r for r in t["rows"] if not r[0].startswith("OC Vibe impact")]
                if t["title"].startswith("Who, what, when"):
                    t["rows"] = [[x["tab"]] + [x["w5h"][k] for k in ("who", "what", "when", "where", "why", "how")] for x in SECTIONS if x.get("w5h") and x["id"] != "p-appx"]
            fo = next(t for t in s["tables"] if t["title"] == "Formulas"); gl = next(t for t in s["tables"] if t["title"] == "Glossary"); me = next(t for t in s["tables"] if t["title"] == "Methods")
            s["cards"] = [["Glossary", "Terms defined", str(len(gl["rows"])), "From ADR to visitor day", "Visit Anaheim BI (Oct. 13, 2026)"],
                          ["Methods", "Methods explained", str(len(me["rows"])), "How each number was produced", "Visit Anaheim BI (Oct. 13, 2026)"],
                          ["Formulas", "Formulas with worked examples", str(len(fo["rows"])), "Each with 2025 inputs", "Visit Anaheim BI (Oct. 13, 2026)"]]
            s["hv"] = str(len(fo["rows"])); s["hl"] = "Formulas worked through with 2025 inputs"
            s["ans"] = f"A plain-language guide: {len(gl['rows'])} terms, {len(me['rows'])} methods and {len(fo['rows'])} formulas, so every figure in this report can be traced and repeated."
            s["w5h"]["how"] = "Plain-language definitions and worked examples using 2025 inputs."
            s["card_calc"] = [None, None, None]
    # 3) summary findings, data notes, announcement
    TAKEAWAYS[0] = (f"Anaheim's visitor economy: {VIS25:.1f}M visitors spent ${SP25:.2f}B in 2025 and supported {A['jobs']:,} jobs; Tourism Economics forecasts {VIS26:.1f}M visitors and ${SP26:.1f}B for 2026. "
                    f"These are City of Anaheim totals; the OC Vibe area accounted for 5.2% of Anaheim visitor days in 2024. (Source: {S_TE}; {S_TEF}; {L.S_DATAFY})")
    TAKEAWAYS[1] = ("Getting to OC Vibe: SR-57 beside the district carries about 275,000 vehicles a weekday; ARTIC has 277 weekday bus trips but only 11 leave after 10 p.m.; the City lists 12,369–12,823 planned parking spaces. "
                    f"(Source: {L.S_OCTA}; {L.S_CITY})")
    TAKEAWAYS[:] = [t for t in TAKEAWAYS if not EST_RX.search(t)]
    DQ[:] = [d for d in DQ if not d.startswith("OC Vibe impact figures are")]
    DQ[:] = [re.sub(r" OCVIBE's newest figure is 5,000 seats \(concert hall release, Mar\. 12, 2026\); at 5,000 seats the base estimate falls from \$[\d.]+M to \$[\d.]+M, inside the simulation range\.",
                    " OCVIBE's newest figure is 5,000 seats (concert hall release, Mar. 12, 2026).", d) for d in DQ]
    DQ[:] = [d for d in DQ if not EST_RX.search(d)]
    DQ.insert(0, "Tourism Economics figures cover the City of Anaheim. They are not allocated to OC Vibe, and this report contains no estimate of OC Vibe's impact; OC Vibe's results will be measured once its venues open.")
    DQ.insert(1, "Years: 2025 figures are measured results that Tourism Economics published in 2026; 2026 figures are Tourism Economics' forecast (Sept. 2026) and are labeled as such.")
    MAIN["paras"] = [p.replace("The full report covers OC Vibe's estimated impact, visitor spending,", "The full report covers Anaheim and the OC Vibe area today, visitor spending,") for p in MAIN["paras"]]
    REGISTER[:] = [r for r in REGISTER if "scenario model" not in " ".join(map(str, r)).lower()]
    for r in L.RECS_T:
        if "80% of the uncertainty" in r[3]:
            r[3] = "No OC Vibe visitor data exists yet; ZIP codes and hotel results measure OC Vibe's visitors directly instead of estimating them"
    for s in SECTIONS:
        s["notes"] = [n.replace("which supports the model's 5% transit assumption, and that", "and that") for n in s["notes"]]
    # 4) relabel remaining calculation sources (they are arithmetic on source data, not a scenario model)
    def fix(o):
        if isinstance(o, str):
            return (o.replace("Visit Anaheim BI scenario model (Oct. 12, 2026)", "Visit Anaheim BI calculation from source data (Oct. 13, 2026)")
                     .replace("Each formula with the base-case numbers used in this report", "Each formula with the 2025 inputs used in this report")
                     .replace("Visit Anaheim BI scenario model and source data (Oct. 12, 2026)", "Visit Anaheim BI calculations from source data (Oct. 13, 2026)"))
        if isinstance(o, list): return [fix(x) for x in o]
        if isinstance(o, dict): return {k: fix(v) for k, v in o.items()}
        return o
    SECTIONS[:] = [fix(x) for x in SECTIONS]
    for s in SECTIONS:
        if s.get("ocv") is not None: s.pop("ocv_src", None)
    TAKEAWAYS[:] = fix(TAKEAWAYS); DQ[:] = fix(DQ)
    for k in list(STORIES): STORIES[k] = fix(STORIES[k])
