"""OC Vibe impact section, per-section 'What this means for OC Vibe' notes, and KPI framework.
Imported at the end of content.py; mutates SECTIONS, STORIES, TAKEAWAYS, RECS, SOURCES, DQ, SRC."""
import impact as I

def M(v, nd=1): return f"${v/1e6:,.{nd}f}M"
def K(v): return f"{v/1e3:,.0f}K"
R = {r["name"]: r for r in I.RES}
lo, bs, hi = R["Conservative"], R["Base"], R["Optimistic"]

def attach(SECTIONS, STORIES, TAKEAWAYS, RECS, SOURCES, DQ, SRC, data):
    A = data.EI["Anaheim"]; O = data.EI["Orange County"]
    SRC.update({
      "ocvibe": "OCVIBE (ocvibe.com) and OCVIBE fact sheet (Apr. 2024); City of Anaheim OCVibe page (2026)",
      "visca": "Visit California, 2025 economic impact of travel (released Apr. 2026; via Rural County Representatives of California summary, May 15, 2026)",
      "model": "Visit Anaheim BI scenario model (estimate). Inputs: Tourism Economics 2025 Anaheim and Orange County economic impact ratios; Azira District 5 origins; CoStar hotel performance; City of Anaheim OCVibe program; Visit California 2025.",
    })

    # ---------- per-section "What this means for OC Vibe" ----------
    OCV = {
     "p-spend": [
       f"Each visitor OC Vibe brings to Anaheim is worth about ${I.PV:.0f} in spending (2025), forecast to rise to $279 by 2028. Every 1,000 net-new visitors adds about ${I.PER_1K_NEW:,.0f}.",
       "Spending per visitor is growing faster than visits (spending +4.1% a year vs. visits +1.4% to 2028), so OC Vibe's value grows with longer stays and more spending per trip, not attendance alone.",
       "The market OC Vibe opens into is growing: Q2 2026 visitor spending rose 7.8% and overnight visits 4.5%."],
     "p-impact": [
       f"Each $1 million of visitor spending supports about {I.JOBS_ANA:.1f} jobs in Anaheim and ${I.TAX_ANA*1e6/1e3:,.0f},000 in state and local taxes (Tourism Economics 2025 ratios). In the base case, OC Vibe's {M(bs['spend'],0)} in new visitor spending supports about {round(bs['ana_jobs'],-1):,.0f} jobs.",
       f"Food and beverage is {A['fb_job_share']:.1f}% of visitor-supported jobs in Anaheim and {O['fb_job_share']:.1f}% countywide, and was the fastest-growing spending category in 2025 (+5.5%). OC Vibe's 35+ restaurants (171,544 sq ft) sit in that category.",
       "Visitors saved each Anaheim household about $8,940 in taxes in 2025 (Visit Anaheim, June 2026). New visitors drawn by OC Vibe add to that base."],
     "p-night": [
       f"Citywide, one more night for every visitor is worth about ${data.N['lodge_night']/1e6:.0f} million in lodging. OC Vibe does not need every visitor: each 1% of Anaheim visitors who add a day because of OC Vibe is worth about {M(I.PER_1PCT_DAY)} in spending, including {M(I.PER_1PCT_LODGE)} in lodging.",
       f"Scenarios: 0.5% of visitors add a day ({M(lo['sp_stay'])}), 1% ({M(bs['sp_stay'])}, base case) or 2% ({M(hi['sp_stay'])}).",
       f"Two in three Anaheim visitors ({A['day_share']}%) are day visitors. Evening shows at the 5,613-seat concert hall and Honda Center, plus 550 hotel rooms on site, are what turn a day trip into an overnight stay."],
     "p-transport": [
       "About 275,000 vehicles a day pass OC Vibe on SR-57, and 20 million people live within a 90-mile drive (CoStar). Most OC Vibe visitors will arrive by car, so parking (12,369–12,823 planned spaces) and event-day traffic plans matter.",
       "ARTIC's 277 weekday bus trips and the 2028 Katella pedestrian bridge are OC Vibe's transit front door. Only 11 buses leave ARTIC after 10 p.m., which limits late-event trips without a car.",
       "Rising travel costs (West Coast gas $4.09 a gallon in 2025; average domestic airfare $387) favor nearby drive markets, which are OC Vibe's core audience."],
     "p-d5": [
       "OC Vibe already appears in 5.2% of Anaheim visitor days (Datafy, 2024), before the new venues open. This is the baseline to measure OC Vibe's growth against.",
       f"District 5 visitors are {data.D5['overnight']}% overnight and {data.D5['new']}% first-time, and {I.OUT_OF_STATE*100:.0f}% of domestic visitors come from outside California (Texas, Virginia, Florida, Arizona and New York lead). Out-of-state visitors are the ones who bring new money to California.",
       "13.7% of District 5 visitors also go to the Anaheim Resort, so packaging OC Vibe with resort stays is a direct way to add a day."],
     "p-media": [
       "Visit Anaheim's paid media drove 368,416 observed visits (11.9 per 1,000 impressions); luxury placements returned 34.4. Featuring OC Vibe in these campaigns reaches audiences already converting to visits.",
       "Visitors arrive about 39 days after seeing an ad, so OC Vibe event calendars shared with Visit Anaheim six to eight weeks ahead can be marketed in time.",
       "Media attribution gives OC Vibe a measurable way to track visits from target markets once its venues are included in Visit Anaheim campaigns."],
     "p-hotel": [
       f"OC Vibe's 550 planned rooms would produce about {K(lo['rn'])}–{K(hi['rn'])} room nights a year and {M(lo['room_rev'])}–{M(hi['room_rev'])} in room revenue, generating {M(lo['tot'])}–{M(hi['tot'])} in Anaheim hotel tax (15%).",
       "The market can absorb these rooms: resort-area hotels run 78.4% occupancy, and only 668 rooms are under construction countywide.",
       f"Each point of occupancy at OC Vibe's hotels equals about 2,000 room nights and ${550*365*0.01*218/1e3:,.0f},000 in room revenue at the county average rate."],
     "p-larc": [
       "OC Vibe opens into a strong market: Anaheim hotel revenue per room rose 11.4% in Q2 2026, and convention room nights are pacing +12% for 2026 and +17% for 2027.",
       "Conventions (142 events secured for 2026, about 600,000 room nights) bring weekday visitors that OC Vibe's restaurants and evening venues can capture.",
       "The 2028 Olympics coincide with OC Vibe's first hotel and the Katella bridge, a one-time showcase to new markets.",
       "Watch costs: Anaheim inflation of about 3.2% a year and labor costs of about 6% a year will affect OC Vibe operators and pricing."],
    }
    for s in SECTIONS:
        s["notes"] = [n for n in s["notes"] if not n.startswith("What it means for OC Vibe")]
        if s["id"] in OCV: s["ocv"] = OCV[s["id"]]

    # ---------- OC Vibe impact section ----------
    def row(label, key, fmt): return [label] + [fmt(r[key]) for r in (lo, bs, hi)]
    num = lambda v: f"{round(v, -3):,.0f}"
    jn = lambda v: f"{round(v, -1):,.0f}"
    scen_rows = [
      row("Concert hall, theater and club attendance", "attend", num),
      row("Net-new visitors to Anaheim", "new_vis", num),
      row("Extra visitor days from longer stays", "extra_days", num),
      row("New visitor spending, total", "spend", M),
      row("· from net-new visitors", "sp_new", M),
      row("· from longer stays", "sp_stay", M),
      row("· of which lodging", "lodge_stay", M),
      row("Anaheim: total economic impact", "ana_impact", M),
      row("Anaheim: jobs supported", "ana_jobs", jn),
      row("Anaheim: state and local taxes", "ana_tax", M),
      row("Orange County: total economic impact", "oc_impact", M),
      row("Orange County: jobs supported", "oc_jobs", jn),
      row("Orange County: state and local taxes", "oc_tax", M),
      row("California: new out-of-state visitor spending", "ca_spend", M),
      row("California: jobs supported", "ca_jobs", jn),
      row("California: state and local taxes", "ca_tax", M),
      row("OC Vibe hotels: room nights a year", "rn", num),
      row("OC Vibe hotels: room revenue", "room_rev", M),
      row("OC Vibe hotels: Anaheim hotel tax (15%)", "tot", M),
    ]
    a = I.ASSUME
    pct = lambda v: f"{v*100:.1f}%".replace(".0%", "%")
    assume_rows = [
      ["Concert hall events a year (5,613 seats)", *map(str, a["hall_events"]), "Honda Center has averaged about 140 events a year since 1993 (4,500+ events; OCBJ)"],
      ["Concert hall seats filled", *map(pct, a["hall_fill"]), "BI assumption"],
      ["Theater and club events a year (2,300 seats)", *map(str, a["small_events"]), "OCVIBE fact sheet lists a 2,000-seat theater and 300-seat club; BI assumption"],
      ["Theater and club seats filled", *map(pct, a["small_fill"]), "BI assumption"],
      ["Attendees who are net-new visitors to Anaheim", *map(pct, a["net_new"]), "Excludes locals and people already in Anaheim; BI assumption"],
      ["Anaheim visitors who add a day because of OC Vibe", *map(pct, a["add_day"]), "Applied to 26.5M visitors (Tourism Economics 2025)"],
      ["OC Vibe hotel occupancy", *map(pct, a["hotel_occ"]), "CoStar: Orange County 74.0%, Disneyland submarket 78.4%"],
      ["OC Vibe hotel average nightly rate", *[f"${v:,.0f}" for v in a["hotel_adr"]], "CoStar: Orange County $218, Disneyland submarket $255"],
      ["Spending per visitor / per visitor day", f"${I.PV:.0f} / ${I.PER_DAY:.2f}", "same", "same", "Tourism Economics 2025; 2.17-day weighted stay"],
      ["Economic impact per $1 of visitor spending", f"Anaheim {I.MULT_ANA:.2f} · OC {I.MULT_OC:.2f}", "same", "same", "Tourism Economics 2025 ratios (total impact ÷ direct spending)"],
      ["Share of new spending that is new to California", f"{I.OUT_OF_STATE*100:.0f}%", "same", "same", "District 5 domestic visitors from outside California (Azira)"],
    ]
    # phase ramp (base case)
    hall_only = I.HALL_CAP * a["hall_events"][1] * a["hall_fill"][1] * a["net_new"][1] * I.PV
    ramp = [
      ["2027", "Concert hall, Katella Commons market hall, first restaurants, urban park", M(hall_only + bs["sp_stay"] * 0.5), "—"],
      ["2028", "Adds south plaza, theater and club, first hotel (230-room Meadow Hotel assumed; sources differ), Katella bridge; LA Olympics", M(bs["spend"]), num(230 * 365 * a["hotel_occ"][1])],
      ["2029–2032 (full program)", "Adds Arena Hotel (320 rooms), apartments, north plaza", M(bs["spend"]), num(bs["rn"])],
    ]
    sens = [
      ["Every 1% of Anaheim visitors who add a day", M(I.PER_1PCT_DAY), f"Includes {M(I.PER_1PCT_LODGE)} in lodging"],
      ["Every 1,000 net-new visitors", f"${I.PER_1K_NEW:,.0f}", f"${I.PV:.0f} per visitor (2025)"],
      ["Every 100 concert hall nights at 80% full", f"{round(I.PER_100_EVENTS,-3):,.0f} attendees", f"At 25% net-new: {M(I.PER_100_EVENTS*0.25*I.PV)} in visitor spending"],
      ["Each point of OC Vibe hotel occupancy", "About 2,000 room nights", f"About ${round(550*365*0.01*218,-3):,.0f} room revenue; ${round(550*365*0.01*218*0.15,-3):,.0f} hotel tax"],
      ["Each $1M in new visitor spending", f"{I.JOBS_ANA:.1f} Anaheim jobs", f"${I.MULT_ANA:.2f}M total impact; about ${round(I.TAX_ANA*1e6,-3):,.0f} state and local taxes"],
    ]
    context = [
      ["OCVIBE fact sheet (Apr. 2024)", "3,000+ ongoing jobs; about $10M a year in tax revenue to Anaheim; $255M in public benefits", "Whole district: office, residents, local patrons and visitors"],
      ["DTA analysis, cited by Visit Anaheim (June 2020)", "More than $400M a year in recurring economic impact; 3,300 permanent jobs; $2B one-time construction impact", "Whole district, earlier and larger program"],
      ["This estimate (Visit Anaheim BI, Oct. 2026)", f"{M(bs['spend'],0)} new visitor spending; {M(bs['ana_impact'],0)} Anaheim economic impact; about {round(bs['ana_jobs'],-1):,.0f} jobs (base case)", "Visitors only (50+ miles or overnight); excludes construction, office and residents"],
    ]
    SECTIONS.insert(0, dict(
      id="p-ocv", tab="OC Vibe impact",
      q="What impact will OC Vibe have on Anaheim, Orange County and California?",
      period="Scenario estimate at full operation, 2025 dollars",
      ans=(f"In the base case, OC Vibe would bring about {round(bs['new_vis'],-3):,.0f} net-new visitors and {round(bs['extra_days'],-3):,.0f} extra visitor days to Anaheim a year, adding about {M(bs['spend'],0)} in visitor spending "
           f"(range {M(lo['spend'],0)}–{M(hi['spend'],0)}). That supports about {M(bs['ana_impact'],0)} in total economic impact, {round(bs['ana_jobs'],-1):,.0f} jobs and {M(bs['ana_tax'])} in state and local taxes in Anaheim. "
           f"Its 550 hotel rooms would add about {round(bs['rn'],-3):,.0f} room nights and {M(bs['tot'])} in hotel tax a year."),
      hv=M(bs["spend"], 0), hl="New visitor spending a year, base case (estimate)",
      warn="These are Visit Anaheim BI scenario estimates, not forecasts or measured results. They cover visitor activity only and depend on the assumptions listed below. Refine them with OC Vibe's event, ticketing and hotel plans.",
      cards=[
        ["Base case, a year", "New visitor spending", M(bs["spend"], 0), f"Range {M(lo['spend'],0)}–{M(hi['spend'],0)} · {bs['share_ana']:.1f}% of Anaheim's 2025 total", "BI estimate"],
        ["Anaheim, base case", "Total economic impact", M(bs["ana_impact"], 0), f"{round(bs['ana_jobs'],-1):,.0f} jobs · {M(bs['ana_tax'])} state and local taxes", "BI estimate; Tourism Economics ratios"],
        ["Visitation, base case", "Net-new visitors + extra days", f"{bs['new_vis']/1e3:,.0f}K + {bs['extra_days']/1e3:,.0f}K", f"From {bs['attend']/1e6:.2f}M attendees; 1% of visitors add a day", "BI estimate"],
        ["OC Vibe hotels, base case", "Room nights a year", f"{bs['rn']/1e3:,.0f}K", f"{M(bs['room_rev'])} room revenue · {M(bs['tot'])} hotel tax", "BI estimate; CoStar"],
      ],
      tables=[
        dict(title="OC Vibe visitor impact by scenario", sub="A year at full operation, 2025 dollars. Hotel figures are part of visitor spending, not added to it.",
             cols=[["Measure",0],["Conservative",1],["Base",1],["Optimistic",1]], rows=scen_rows, hi=3, full=True, src=SRC["model"]),
        dict(title="What each lever is worth", sub="Use these to size OC Vibe's own plans", cols=[["Lever",0],["Value",1],["Detail",0]], rows=sens, hi=0, src=SRC["model"]),
        dict(title="Scenario assumptions", sub="Change these as OC Vibe's programming and hotel plans are confirmed",
             cols=[["Assumption",0],["Conservative",1],["Base",1],["Optimistic",1],["Basis",0]], rows=assume_rows, hi=-1, full=True, src=SRC["model"]),
        dict(title="How the impact builds as OC Vibe opens (base case)", sub="Phasing from the City of Anaheim OCVibe page and OCVIBE fact sheet",
             cols=[["Phase",0],["What opens",0],["New visitor spending a year",1],["Hotel room nights",1]], rows=ramp, hi=2, src=SRC["model"] + "; " + SRC["ocvibe"]),
        dict(title="How this compares with published OC Vibe estimates", sub="Different scopes; not directly comparable",
             cols=[["Estimate",0],["Figures",0],["Scope",0]], rows=context, hi=2, wide=True, src="OCVIBE fact sheet (Apr. 2024); Visit Anaheim article (June 24, 2020); Visit Anaheim BI"),
      ],
      charts=[dict(kind="bars", title="New visitor spending a year, by scenario", sub="Estimate at full operation, 2025 dollars",
                   rows=[dict(l="Conservative", v=lo["spend"]/1e6, t=M(lo["spend"],0)), dict(l="Base", v=bs["spend"]/1e6, t=M(bs["spend"],0), hi=True),
                         dict(l="Optimistic", v=hi["spend"]/1e6, t=M(hi["spend"],0))], src=SRC["model"])],
      notes=[
        "Method: new visitor spending = net-new visitors × $258 + extra visitor days × $118.71. Economic impact, jobs and taxes apply Tourism Economics 2025 ratios for Anaheim and Orange County. California applies Visit California 2025 jobs and tax ratios to the out-of-state share only.",
        "No double counting: hotel guests are a subset of visitors, so hotel room revenue and room nights are shown as outputs and are not added to spending.",
        f"Orange County figures treat the new spending as new to the county; some visitors would otherwise have spent elsewhere in Orange County. California counts only out-of-state visitors ({I.OUT_OF_STATE*100:.0f}% of District 5 domestic visitors); international visitors are excluded, so the California figure is conservative.",
        f"Scale: the base case equals {bs['share_ana']:.1f}% of Anaheim's 2025 visitor spending, {bs['share_oc']:.1f}% of Orange County's and {bs['share_ca']:.3f}% of California's $158.9 billion.",
        "Not included: construction spending, office and resident activity, local patrons, Honda Center's existing events, and spending growth after 2025.",
        "The OC Vibe program (5,613-seat concert hall, 550 hotel rooms, 35+ restaurants) comes from the City of Anaheim and OCVIBE. Figures differ by source and edition; confirm with OC Vibe.",
      ],
    ))

    # ---------- KPI framework (on the impact page) ----------
    kpi = [
      ["North star", "Net-new visitor spending from OC Vibe", "Not yet measured", f"{M(bs['spend'],0)} a year (base)", "Visit Anaheim BI (Tourism Economics, Datafy)", "Annual"],
      ["Visitation", "OC Vibe share of Anaheim visitor days", "5.2% (Datafy, 2024)", "Track growth after 2027 openings", "Visit Anaheim BI (Datafy)", "Quarterly"],
      ["Visitation", "Visitors from 50+ miles at OC Vibe venues", "Set from ticketing data", f"{a['net_new'][1]*100:.0f}% of attendees net-new (base)", "OC Vibe ticketing (ZIP codes)", "Monthly"],
      ["Length of stay", "Average stay of visitors who visit OC Vibe", "2.17 days (Anaheim, 2025)", "Above the Anaheim average", "Visit Anaheim BI (Azira, Datafy)", "Quarterly"],
      ["Length of stay", "Overnight share of OC Vibe visitors", "85.8% (District 5, Jan.–May 2026)", "Hold or raise after openings", "Visit Anaheim BI (Azira)", "Quarterly"],
      ["Hotel stays", "OC Vibe hotel occupancy and average rate", "Market: 78.4% and $255 (CoStar)", f"{a['hotel_occ'][1]*100:.0f}% at ${a['hotel_adr'][1]:.0f} (base)", "OC Vibe hotels; CoStar", "Monthly"],
      ["Hotel stays", "Room nights and hotel tax from OC Vibe hotels", "Opens 2028", f"{round(bs['rn'],-3):,.0f} nights; {M(bs['tot'])} tax (base)", "OC Vibe hotels; City of Anaheim", "Monthly"],
      ["New markets", "Share of OC Vibe visitors from outside California", f"{I.OUT_OF_STATE*100:.0f}% (District 5)", "Grow out-of-state share", "Visit Anaheim BI (Azira)", "Quarterly"],
      ["New markets", "Visits from Visit Anaheim campaigns featuring OC Vibe", "11.9 visits per 1,000 impressions", "At or above campaign average", "Visit Anaheim BI (Azira attribution)", "Per campaign"],
      ["Spending", "Visitor card spending at OC Vibe businesses", "Set at opening", "Grow with visitor share", "Datafy or card data; OC Vibe tenants", "Quarterly"],
      ["Access", "Event-day transit trips and late-night departures from ARTIC", "277 weekday bus trips; 11 leave after 10 p.m.", "More late service on event nights", "OCTA", "Quarterly"],
      ["Access", "Traffic on SR-57 and Katella Ave", "275,000 and 36,000 vehicles a day", "New baseline counts before 2027", "OCTA; City of Anaheim", "Annual"],
    ]
    SECTIONS[0]["tables"].append(dict(title="Measures OC Vibe can build on", sub="Baselines from Visit Anaheim data; base-case markers from this estimate",
        cols=[["Area",0],["Measure",0],["Baseline today",0],["Marker",0],["Source and owner",0],["How often",0]], rows=kpi, hi=0, full=True, wide=True,
        src="Visit Anaheim BI (Oct. 12, 2026); Datafy (calendar 2024); Azira via Symphony (Jan.–Aug. 2026); CoStar (through Aug. 2026); OCTA (2026); Tourism Economics (2025)"))

    risks = [
      ["Concert hall bookings below plan", "Fewer net-new visitors (each 100 nights at 80% full is about 449,000 attendees)", "Medium", "Share the event calendar with Visit Anaheim; co-market with conventions"],
      ["Visitors shift from other Anaheim venues", "Overstates net-new spending", "Medium", "Measure origin ZIP codes; count only 50+ mile and overnight visitors"],
      ["Event-night capacity", "Honda Center (18,300+ seats) and concert hall (5,613) on the same night exceed 12,369–12,823 planned parking spaces at typical car occupancy", "Medium", "Event scheduling, ARTIC transit, late-night service, pedestrian bridge (2028)"],
      ["Construction or phasing delays", "Pushes impact later than 2027–2028", "Medium", "Update the phase table each edition"],
      ["Costs and pricing", "Inflation (about 3.2% a year) and labor (about 6% a year) raise prices; may slow visits", "Medium", "Track spending per visitor and rates vs. the market"],
      ["Hotel market softens", "Lower occupancy and rate at OC Vibe hotels", "Low to medium", "CoStar shows 78.4% occupancy and little new supply through 2028"],
    ]
    SECTIONS[0]["tables"].append(dict(title="Risks to the estimate", sub="What could move OC Vibe's impact up or down", cols=[["Risk",0],["Effect",0],["Likelihood",0],["How to manage it",0]],
        rows=risks, hi=-1, wide=True, full=True, src="Visit Anaheim BI (Oct. 12, 2026); City of Anaheim OCVibe page (2026); CoStar (through Aug. 2026); LARC (Sept. 2026); OCTA (2026)"))

    STORIES["p-ocv"] = dict(measure="New visitor spending from OC Vibe (estimate)", v=None, val=M(bs["spend"], 0), basis="Scenario estimate", ok=False,
      warn="This highlight is a scenario estimate, not measured growth. Label it as an estimate wherever it is used.",
      head=f"OC Vibe could add about {M(bs['spend'],0)} a year in Anaheim visitor spending",
      dek=f"Base case: {round(bs['new_vis'],-3):,.0f} net-new visitors, {round(bs['extra_days'],-3):,.0f} extra visitor days and {round(bs['rn'],-3):,.0f} hotel room nights a year.",
      lede=f"At full operation, OC Vibe's concert hall, smaller venues, restaurants and 550 hotel rooms could add about {M(bs['spend'],0)} a year in visitor spending in Anaheim, according to a Visit Anaheim BI scenario estimate.",
      paras=[f"That spending would support about {M(bs['ana_impact'],0)} in total economic impact, {round(bs['ana_jobs'],-1):,.0f} jobs and {M(bs['ana_tax'])} in state and local taxes in Anaheim, based on Tourism Economics 2025 ratios. The range runs from {M(lo['spend'],0)} to {M(hi['spend'],0)}.",
             f"Each 1% of Anaheim visitors who add a day because of OC Vibe is worth {M(I.PER_1PCT_DAY)}; OC Vibe's hotels would add about {M(bs['tot'])} a year in hotel tax.",
             f"About {I.OUT_OF_STATE*100:.0f}% of District 5's domestic visitors come from outside California, the share that brings new money to the state."],
      stats=[[M(bs["spend"],0), "New visitor spending a year (base case)", "BI estimate"], [f"{round(bs['ana_jobs'],-1):,.0f}", "Anaheim jobs supported (base case)", "BI estimate"], [M(I.PER_1PCT_DAY), "Value of each 1% of visitors adding a day", "BI estimate"]],
      chart=dict(title="New visitor spending a year, $ millions", rows=[["Conservative", round(lo["spend"]/1e6,1), M(lo["spend"],0), 0], ["Base", round(bs["spend"]/1e6,1), M(bs["spend"],0), 1], ["Optimistic", round(hi["spend"]/1e6,1), M(hi["spend"],0), 0]], src="BI estimate"),
      srcs=[SRC["model"], SRC["ocvibe"]])

    TAKEAWAYS.insert(0, f"OC Vibe impact (estimate): about {M(bs['spend'],0)} a year in new visitor spending in the base case (range {M(lo['spend'],0)}–{M(hi['spend'],0)}), supporting {M(bs['ana_impact'],0)} in Anaheim economic impact, about {round(bs['ana_jobs'],-1):,.0f} jobs and {round(bs['rn'],-3):,.0f} hotel room nights.")
    RECS.insert(0, "Adopt the measurement framework on the OC Vibe impact page: share event ticketing ZIP codes and hotel results with Visit Anaheim so BI can replace these estimates with measured visitation, length of stay and spending from 2027.")
    SOURCES.insert(0, ("OCVIBE and City of Anaheim", "ocvibe.com (accessed Oct. 12, 2026); OCVIBE fact sheet (Apr. 2024); City of Anaheim OCVibe page (2026): program, phasing, concert hall capacity and hotel rooms."))
    SOURCES.append(("Visit California and Visit Anaheim publications", "Visit California 2025 economic impact (via RCRC, May 2026); Visit Anaheim articles (June 2020 DTA estimates; June 2026 tax relief per household); City of Anaheim transient occupancy tax (15%); OCBJ (Apr. 29, 2025) for Honda Center history."))
    DQ.insert(0, "OC Vibe impact figures are Visit Anaheim BI scenario estimates built from published ratios and stated assumptions; they are not forecasts and should be replaced with measured data after opening.")
    attach_more(SECTIONS, SOURCES, DQ, RECS, SRC)
    TAKEAWAYS.insert(1, f"Transportation (estimate): when Honda Center and the concert hall both sell out, about {round(I.TR['both_vehicles'][0],-2):,.0f}–{round(I.TR['both_vehicles'][1],-2):,.0f} vehicles would fill {I.TR['both_parking_share'][0]*100:.0f}%–{I.TR['both_parking_share'][1]*100:.0f}% of OC Vibe's planned parking; only 11 weekday buses leave ARTIC after 10 p.m.")
    DQ.append("California's 2025 statewide figures come from a secondary summary of Visit California's report; confirm against the primary report before external use.")

# ---------- Transportation, spending mix, ten-year view, traveler questions, source register ----------
REGISTER = [
  # source, publisher / document, period covered, published or pulled, how used, vetting
  ["Tourism Economics", "Anaheim and Garden Grove Travel Forecast, client preliminary (June and Sept. 2026 editions)", "2019–2025 actuals; Q1–Q2 2026; forecast to 2028", "Sept. 2026 (data through Aug. 31, 2026)", "Visits, spending, spending per visitor, Q2 2026", "Original PDF reviewed; preliminary edition"],
  ["Tourism Economics", "Economic Impact of Visitors 2025: Anaheim, Garden Grove, Orange County", "Calendar 2025 vs. 2024", "Apr.–May 2026", "Jobs, F&B jobs, taxes, spending by category; impact ratios in the OC Vibe model", "Original reports reviewed; marked Draft – Not for Distribution"],
  ["Visit Anaheim BI", "Extra Night Calculation deck; TID Request workbook (Simpleview export)", "2025 inputs; TID events 2022–2034", "Workbook exported Jan. 20, 2025; recalculated Oct. 12, 2026", "One-more-night scenarios; TID group bookings", "Recalculated; deck total $9.9B vs. $9.98B noted"],
  ["Symphony | Tourism Economics (Azira)", "POI Analysis (District 5); Domestic Visitors by Geography; Media Attribution", "Jan. 1–May 31, 2026; Aug. 2026; Jan. 1–Aug. 31, 2026", "Exported 2026 (project files)", "District 5 profile and origins; drive distance; campaign visits", "Original PDFs reviewed; some charts only partly readable"],
  ["Datafy", "Anaheim visitor report", "Calendar 2024", "Provided Oct. 12, 2026", "OC Vibe share of visitor days (5.2%); clusters", "Original PDF reviewed"],
  ["Lodging Analytics Research & Consulting (LARC)", "Anaheim Market Intelligence Reports; Forecasts Combined 1Q–3Q-26", "Hotel data to Q2 2026; forecasts to 2030", "Jan., Apr., June, July, Sept. 2026", "Hotel outlook, convention pace, inflation, OC Vibe program, pipeline", "Original PDFs and workbooks reviewed; redistribution needs LARC consent"],
  ["CoStar Group", "Orange County Hospitality Market, Disneyland Submarket and Capital Markets reports", "Trailing 12 months and YTD through Aug. 2026", "Pulled Oct. 12, 2026", "Submarket hotel performance, pipeline, sales, revenue mix, OC economy (Oxford Economics)", "Original PDFs reviewed; text-vs-table differences noted; licensed to Visit Anaheim"],
  ["OCTA", "2026 Traffic Flow Map (Caltrans and city counts)", "Counts 2021–2024", "Published Aug. 2026", "Traffic near OC Vibe", "Original map reviewed; roads located with GTFS stop coordinates"],
  ["OCTA", "Bus schedules (GTFS feed)", "Service Aug. 9–Nov. 7, 2026", "Provided Oct. 12, 2026", "ARTIC bus trips, late service, travel times, fare", "Analyzed by BI from raw files; recounted independently Oct. 12, 2026 (277 trips: 227 departing, 50 ending)"],
  ["U.S. Bureau of Transportation Statistics", "County Transportation Profile: Orange County, CA", "American Community Survey (year not stated in file)", "Provided Oct. 12, 2026", "Commute mode, households without a vehicle, facilities", "File reviewed; confirm data year on bts.gov"],
  ["U.S. Bureau of Transportation Statistics", "Transportation Economic Trends, Tables 3.1, 3.4, 6.6", "2019–2025", "Accessed Oct. 12, 2026 (data.bts.gov)", "Gas prices, airfares, car cost per mile", "Pulled from BTS open data"],
  ["City of Anaheim", "OCVibe project page and fact sheet; Transient Occupancy Tax page", "Program through about 2030–2032; TOT 15%", "2026 versions; accessed Oct. 12, 2026", "Concert hall seats (5,613), hotels (320 + 230 rooms), phasing, parking; hotel tax rate", "Official city pages reviewed"],
  ["OCVIBE", "ocvibe.com; OCVIBE fact sheet", "Program as published", "Fact sheet Apr. 2024; website accessed Oct. 12, 2026", "Program, 3,000+ jobs, ~$10M tax revenue, 35+ restaurants", "Developer-published; not independently verified"],
  ["Visit Anaheim (visitanaheim.org)", "OCVIBE meetings page; articles (June 24, 2020, DTA estimates; June 3, 2026)", "2025 visitor results; 2020 estimates", "As dated; accessed Oct. 12, 2026", "Published OC Vibe estimates; program cross-check", "Reviewed; site lists 5,700 seats and 865,000 sq ft office, which differ from the City"],
  ["Visit California", "Economic Impact of Travel in California, 2025", "Calendar 2025", "Released Apr. 2026 (summary by RCRC, May 15, 2026)", "Statewide spending, jobs and tax ratios", "Secondary summary; confirm with Visit California's primary report"],
  ["Mindtrip (Visit Anaheim trip planner)", "Traveler chat messages", "Oct. 1, 2025–Oct. 11, 2026", "Pulled Oct. 12, 2026", "What travelers ask about ARTIC, Honda Center and OC Vibe", "Live search of chat messages; small counts"],
  ["Orange County Business Journal", "Honda Center set for $1.1B overhaul", "1993–2025", "Apr. 29, 2025", "Honda Center history (4,500+ events) for the event-count assumption", "Third-party reporting"],
  ["Visit Anaheim BI", "OC Vibe impact scenario model", "Full operation, 2025 dollars", "Oct. 12, 2026", "All OC Vibe impact estimates", "Recomputed independently; estimates, not forecasts"],
]

def attach_more(SECTIONS, SOURCES, DQ, RECS, SRC):
    s0 = SECTIONS[0]
    tr, ten = I.TR, I.TEN
    s0["tables"].insert(5, dict(title="Transportation effects (base case)", sub="Event-day travel at OC Vibe; vehicle figures use 2.0–2.5 people per car and 90% arriving by car (BI assumptions)",
        cols=[["Measure",0],["Estimate",1],["What it means",0]], wide=True, full=True,
        rows=[["Vehicle round trips a year from new venue attendance", f"{round(tr['veh_round_trips_yr'],-3):,.0f}", "Spread over about 300 events a year; Saturdays are the busiest day in District 5"],
              ["Vehicles on a sold-out concert hall night", f"{round(tr['hall_vehicles'][0],-2):,.0f}–{round(tr['hall_vehicles'][1],-2):,.0f}", f"About {round(tr['hall_trips'],-2):,.0f} trips in and out: {tr['hall_vs_katella']*100:.0f}% of Katella Ave's daily traffic (2021 count) or {tr['hall_vs_sr57']*100:.1f}% of SR-57's"],
              ["Vehicles when Honda Center and the concert hall both sell out", f"{round(tr['both_vehicles'][0],-2):,.0f}–{round(tr['both_vehicles'][1],-2):,.0f}", f"Fills {tr['both_parking_share'][0]*100:.0f}%–{tr['both_parking_share'][1]*100:.0f}% of the 12,369–12,823 planned parking spaces"],
              ["Transit riders on a sold-out concert hall night (5% by transit)", f"{round(tr['transit_riders'],-1):,.0f}", f"About {tr['bus_loads']:.0f} bus loads at 60 riders; OCTA runs 11 weekday departures from ARTIC after 10 p.m."],
              ["New visitor spending on transportation a year", M(tr["transport_spend"]), "Tourism Economics: transportation is 3.3% of Anaheim visitor spending"],
              ["Cost of driving (illustrative 60-mile round trip)", f"${60*0.8197:.0f}", "At BTS's $0.82 average cost per mile (2024); favors nearby drive markets"]],
        src="Visit Anaheim BI (Oct. 12, 2026) using City of Anaheim parking (2026), LARC Honda Center seats (Sept. 2026), OCTA counts and GTFS (2026), BTS TET (2024) and Tourism Economics (2025)"))
    s0["tables"].insert(6, dict(title="Where the new visitor spending goes (base case)", sub="Split by Anaheim's 2025 visitor spending mix; OC Vibe's mix will differ",
        cols=[["Category",0],["Share",1],["New spending a year",1]],
        rows=[[n, f"{sh*100:.1f}%", M(v)] for n, sh, v in I.CAT] + [["Food and beverage jobs supported", "", f"About {round(I.FB_JOBS,-1):,.0f}"]],
        hi=3, src="Visit Anaheim BI (Oct. 12, 2026) from Tourism Economics Economic Impact 2025 (Anaheim)"))
    s0["tables"].insert(7, dict(title="First ten years, 2027–2036 (base case)", sub="2025 dollars; second hotel assumed to open in 2030 (City: 2029–2032)",
        cols=[["Measure",0],["Ten-year total",1]],
        rows=[["New visitor spending", M(ten["spend"], 0)], ["Anaheim total economic impact", f"${ten['impact']/1e9:.2f}B"], ["State and local taxes", M(ten["tax"], 0)],
              ["OC Vibe hotel room nights", f"{round(ten['rn'],-4)/1e6:.2f}M"], ["Anaheim hotel tax from OC Vibe hotels (15%)", M(ten["tot"])]],
        hi=0, src="Visit Anaheim BI scenario model (Oct. 12, 2026)"))
    s0["notes"].insert(1, "Transportation: vehicle, parking and transit figures are planning-level estimates from stated assumptions (90% by car, 2.0–2.5 people per car, 5% by transit, 60 riders per bus). OC Vibe's event traffic plans and OCTA ridership data would replace them.")
    s0["ocv"] = None
    # traveler questions (Mindtrip) on the Getting here page
    tp = [x for x in SECTIONS if x["id"] == "p-transport"][0]
    tp["tables"].append(dict(title="What travelers ask Visit Anaheim's trip planner about this area", sub="Messages mentioning ARTIC, Honda Center, the Ducks or OC Vibe, Oct. 1, 2025–Oct. 11, 2026 (BI grouping of the messages)",
        cols=[["Topic",0],["Messages",1],["Examples",0]], full=True,
        rows=[["Getting around and transit via ARTIC", "16", "ARTIC to Disneyland; Disneyland back to ARTIC after 8 p.m.; Amtrak and Metrolink passes; convention center shuttle"],
              ["Parking at ARTIC", "13", "Overnight and short-term parking; Lot C walking route; World Cup parking; parking to reach Disneyland"],
              ["Honda Center events and Ducks games", "11", "What's on this weekend; next home game; combining a Ducks game with Disneyland (Australia)"],
              ["OC Vibe itself", "4", "When OC Vibe opens; what will be finished before LA28; what the district includes"],
              ["Dining and hotels near Honda Center", "3", "Where to eat before a game; rooftop bars; hotel near Honda Center and the beach (Germany)"],
              ["All matching messages (incl. 6 quiz entries)", "53", "Out of 3,149 traveler messages in the period (37 chats)"]],
        hi=0, src="Mindtrip trip planner on visitanaheim.org, live search of traveler messages, Oct. 1, 2025–Oct. 11, 2026 (pulled Oct. 12, 2026); grouping by Visit Anaheim BI"))
    tp["ocv"].append("Travelers already treat ARTIC as a parking and transit hub for Disneyland and the convention center (29 of 53 related trip-planner messages), and ask about late returns. OC Vibe can meet that traffic with dining and evening programming at the ARTIC end of the district.")
    SOURCES.insert(1, ("Mindtrip trip planner (visitanaheim.org)", "Traveler messages mentioning ARTIC, Honda Center, the Ducks or OC Vibe, Oct. 1, 2025–Oct. 11, 2026 (pulled Oct. 12, 2026)."))
    DQ.append("Mindtrip counts are small (53 of 3,149 messages) and include six quiz entries; treat them as signals, not measures.")
    DQ.append("Published OC Vibe program figures differ by source: concert hall 5,613 seats (City, 2026) vs. 5,700 (OCVIBE 2024; visitanaheim.org); office up to 563,875 sq ft (City) vs. 865,000 sq ft (visitanaheim.org). The model uses the City's figures.")
