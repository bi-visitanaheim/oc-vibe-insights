"""Newsroom structure (added Oct. 13, 2026, per John Picou): each section reads as a broadsheet news report
followed by analysis. Facts only: no editorial or opinion pieces (John's decision, Oct. 13, 2026).

News report (objective, inverted pyramid): headline, dateline + lede (the key insight), nut graph ("Why it matters"),
then "The details": six announcement-style data cards (who, what, when, where, why, how), each with a figure, the
figure's label (and its calculation when the figure is calculated), the plain-language detail and the source with its date.
Analysis (feature): featured charts, main table, what it means for OC Vibe, compare and contrast.

Every figure on a card is copied from the section's existing text, tables or cards (number-trace check H in
checks/validate_ocvibe.py). AP style: abbreviated months with dates (Jan., Feb., Aug., Sept., Oct., Nov., Dec.),
March–July spelled out, % with numerals, "a.m."/"p.m.", Oxford comma per VA voice rules.
Attach last in content.py (after facts_only).
"""

DATELINE = "ANAHEIM, Calif."
KIND_NEWS, KIND_ANALYSIS = "News report", "Analysis"

TE_EI = "Tourism Economics, Economic Impact of Visitors (calendar 2025; pub. 2026)"
TE_FC = "Tourism Economics, Anaheim Travel Forecast (pub. Sept. 2026)"
DATAFY = "Datafy Anaheim visitor report (calendar 2024)"
AZ_D5 = "Azira via Symphony (District 5, Jan. 1–May 31, 2026)"
AZ_DOM = "Azira via Symphony (domestic visitors, Aug. 2026)"
VISA = "Visa Destination Insights via Symphony (Aug. 2026 vs. Aug. 2025)"
XN = "Visit Anaheim BI, Extra Night study (2025 inputs; recalculated Oct. 12, 2026)"
OCTA_MAP = "OCTA Traffic Flow Map (pub. Aug. 2026)"
OCTA_BUS = "OCTA bus schedules (Aug. 9–Nov. 7, 2026)"
AMTRAK = "Amtrak ANA fact sheet (2024 data; pub. Oct. 27, 2025)"
AZ_MEDIA = "Azira media attribution via Symphony (ad exposures Jan. 1–Aug. 31, 2026)"
COSTAR = "CoStar reports and export (data through Aug. 2026; pulled Oct. 12, 2026)"
STR = "STR daily data, Visit Anaheim hotel sets (Jan. 1–Oct. 3, 2026)"
LARC = "LARC Market Intelligence Reports (Jan.–Sept. 2026)"
PUB = "OCVIBE and City of Anaheim public releases (2024–2026)"
BI = "Visit Anaheim Business Intelligence (Oct. 13, 2026)"

# (fig, fig_l, src) per who/what/when/where/why/how; the card body is the section's own w5h text.
D = lambda *rows: [dict(zip(("fig", "fig_l", "src"), r)) for r in rows]

NEWS = {
 "p-ocv": dict(
   nut="These are City of Anaheim totals, measured before OC Vibe's first venues open in 2027, so they set the baseline that OC Vibe's own results can be compared with later. Tourism Economics does not measure OC Vibe; the OC Vibe area's 5.2% share of Anaheim visitor days comes from Datafy (calendar 2024).",
   details=D(("26.5M", "Anaheim visitors, 2025", TE_EI),
             ("$6.83B", "visitor spending, 2025", TE_EI),
             ("2025 · 2026", "measured year · forecast year", TE_EI + "; " + TE_FC),
             ("District 5", "OC Vibe area, beside Honda Center and ARTIC", AZ_D5 + "; " + PUB),
             ("2027", "first OC Vibe venues open", PUB),
             ("3 sources", "Tourism Economics, Datafy and Azira", TE_EI + "; " + DATAFY + "; " + AZ_D5))),
 "p-spend": dict(
   nut="Spending per visitor sets the value of each visitor OC Vibe draws. Tourism Economics reports $258 per visitor in 2025 ($6.832B ÷ 26.5M) and forecasts $279 by 2028, and Visa shows visitor card spending up 8.1% in August 2026.",
   details=D(("26.5M", "Anaheim visitors, 2025", TE_EI),
             ("$1.76B", "visitor spending, Q2 2026 (+7.8% vs. Q2 2025)", TE_FC),
             ("Q2 2026", "latest measured quarter; forecasts to 2028", TE_FC),
             ("Anaheim", "with Garden Grove for comparison", TE_FC),
             ("$279", "forecast spending per visitor, 2028", TE_FC),
             ("$258", "per visitor, 2025: $6.832B ÷ 26.5M visitors", TE_EI))),
 "p-impact": dict(
   nut="Visitor spending reaches well beyond hotels and attractions. Tourism Economics counts direct, indirect and induced effects, which together support about one in three Anaheim jobs; these published ratios link visitor spending to jobs and tax revenue.",
   details=D(("67,817", "Anaheim jobs supported by visitors, 2025", TE_EI),
             ("$10.4B", "total economic impact, Anaheim, 2025", TE_EI),
             ("2025 vs. 2024", "calendar years compared", TE_EI),
             ("178,164", "jobs supported countywide (Orange County)", TE_EI),
             ("$970M", "state and local taxes, Anaheim, 2025", TE_EI),
             ("3 effects", "direct, indirect and induced spending", TE_EI))),
 "p-night": dict(
   nut="Longer stays raise spending without adding visitors. The Visit Anaheim Extra Night study values one more night per visitor at about $794 million in lodging ($1.724B ÷ 2.17 days), holding spending per day constant.",
   details=D(("26.5M", "Anaheim visitors, 2025", TE_EI),
             ("$794M", "one more night in lodging: $1.724B ÷ 2.17 days", XN),
             ("2025", "visitors, spending and length of stay", XN),
             ("Anaheim", "hotels and businesses citywide", XN),
             ("$31.5M", "each 1% adding a day: 26.5M × 1% × $118.71", XN),
             ("2.17 days", "weighted average stay, 2025", XN))),
 "p-transport": dict(
   nut="Access decides how many visitors OC Vibe can host on peak nights. Most visitors arrive by car, and SR-57 beside OC Vibe carries about 275,000 vehicles a day; ARTIC adds bus and rail service, though only 11 weekday buses leave after 10 p.m.",
   details=D(("74.0%", "of domestic trips start within 50 miles; most arrive by car", AZ_DOM),
             ("275,000", "vehicles a day on SR-57 beside OC Vibe", OCTA_MAP),
             ("Aug. 9–Nov. 7, 2026", "current OCTA bus schedule", OCTA_BUS),
             ("ARTIC", "2626 E. Katella Ave., beside OC Vibe", OCTA_BUS),
             ("11", "weekday buses leave ARTIC after 10 p.m.", OCTA_BUS),
             ("277", "weekday bus trips at ARTIC: 100 + 102 + 75 (routes 50, 53 and 553)", OCTA_BUS))),
 "p-d5": dict(
   nut="Knowing who already visits shows OC Vibe where its audience comes from. Most District 5 visitors stay overnight and many are first-time visitors, and the OC Vibe area already appears in 5.2% of Anaheim visitor days.",
   details=D(("85.8%", "of District 5 visitors stay overnight", AZ_D5),
             ("43.8%", "are first-time visitors", AZ_D5),
             ("Jan.–May 2026", "Azira observation period", AZ_D5),
             ("44%", "of domestic visitors come from outside California", AZ_DOM),
             ("5.2%", "of Anaheim visitor days include the OC Vibe area", DATAFY),
             ("3 sources", "Azira, Datafy and Visa", AZ_D5 + "; " + DATAFY + "; " + VISA))),
 "p-media": dict(
   nut="Paid media already moves people to travel to Anaheim, which gives OC Vibe a proven channel. Azira matched 368,416 visits to 31.0 million measurable impressions, or 11.9 visits per 1,000, from Jan. 1 to Aug. 31, 2026.",
   details=D(("31.0M", "measurable impressions", AZ_MEDIA),
             ("368,416", "observed visits after ad exposure", AZ_MEDIA),
             ("39 days", "average time from ad to visit", AZ_MEDIA),
             ("U.S.", "audiences; visits observed in Anaheim", AZ_MEDIA),
             ("34.4", "visits per 1,000 impressions, luxury placements", AZ_MEDIA),
             ("11.9", "visits per 1,000 impressions: 368,416 ÷ 31.0M × 1,000", AZ_MEDIA))),
 "p-hotel": dict(
   nut="OC Vibe plans 550 hotel rooms in a market with strong demand and little new supply. CoStar reports 78.4% occupancy in the Disneyland submarket and only 668 rooms under construction countywide, and STR shows the most open rooms on Sunday and Monday nights.",
   details=D(("668", "hotel rooms under construction countywide", COSTAR),
             ("78.4%", "Disneyland submarket occupancy, at $255 a night", COSTAR),
             ("Jan. 1–Oct. 3, 2026", "STR daily data period", STR),
             ("Anaheim+", "Visit Anaheim hotel set; CoStar Orange County submarkets", STR + "; " + COSTAR),
             ("550", "hotel rooms planned at OC Vibe", PUB),
             ("15.7 points", "Fri.–Sat. vs. Sun.–Mon. occupancy: 86.24% − 70.59%", STR))),
 "p-larc": dict(
   nut="OC Vibe opens into a market with rising hotel revenue and strong convention pace, along with rising costs. LARC reports Anaheim revenue per available room up 11.4% in Q2 2026 and convention room nights pacing 17% ahead for 2027, with inflation about 3.2% a year.",
   details=D(("+12%", "Convention Center room nights on the books, 2026", LARC),
             ("+11.4%", "Anaheim hotel revenue per room, Q2 2026 (U.S. +5.7%)", LARC),
             ("Jan.–Sept. 2026", "LARC report editions; forecasts to 2030", LARC),
             ("Anaheim", "hotel market, CoStar basis", LARC),
             ("+17%", "Convention Center room nights on the books, 2027", LARC),
             ("3.2%", "inflation a year (Moody's Analytics via LARC)", LARC))),
}

# Newsroom terms and method, added to the appendix glossary and methods (AP and journalism usage).
GLOSSARY_ADD = [
    ["News report", "An objective, factual account of the five Ws (who, what, when, where, why) plus how, written in an inverted pyramid. Each section opens with one."],
    ["Analysis", "The feature part of each section: charts, tables, what the data means for OC Vibe, and compare and contrast. Built only on the facts reported above it."],
    ["Inverted pyramid", "Most important facts first, then supporting details in descending order of importance."],
    ["Lede", "The opening sentence or paragraph that gives the core of the story; here, the key insight after the dateline."],
    ["Nut graph", "The paragraph that explains the context and why the story matters (\"Why it matters\")."],
    ["Dateline", "The place and date that open a news report: ANAHEIM, Calif. (Oct. 13, 2026)."],
    ["Attribution", "Naming the source and date of every fact. No unsourced statements and no first person in news reports."],
    ["AP style", "Associated Press rules for dates, numbers, titles and punctuation (for example, Oct. 13, 2026; 9 p.m.; 7.8%)."],
]
METHOD_ADD = [["Newsroom structure", "Each section is written as a broadsheet news report (dateline, lede, nut graph and six detail cards) followed by analysis. No editorial or opinion content.", "Visit Anaheim BI, Oct. 13, 2026; AP Stylebook conventions"]]

# Reading order (Oct. 13, 2026, per John Picou): each section answers the question the previous one raises.
ORDER = ["p-ocv", "p-octour", "p-d5", "p-spend", "p-impact", "p-hotel", "p-night", "p-transport", "p-media", "p-larc", "p-appx"]
BRIDGE = {
 "p-ocv": "The baseline counts visitors; the next question is who they are. Origin, overnight share and first-time share show which audiences the OC Vibe area already reaches.",
 "p-d5": "Knowing who visits leads to what each visitor is worth. Spending per visitor converts audience size into economic value.",
 "p-spend": "Spending is the input; jobs and tax revenue are the outcome. The next section traces how visitor dollars move through the Anaheim and Orange County economy.",
 "p-impact": "Lodging is one of the largest categories of visitor spending ($1.724B in 2025), so hotel capacity comes next: how full Anaheim hotels are, at what rate, and on which nights rooms are open.",
 "p-hotel": "Open rooms on Sunday and Monday nights point to the most direct lever, longer stays. The next section measures what one more night per visitor is worth.",
 "p-night": "Longer stays depend on how easily visitors arrive and leave, especially after evening events. The next section examines road, bus and rail access to the OC Vibe area.",
 "p-transport": "Access determines who can come; marketing influences who chooses to. The next section shows how paid media converts into measured visits.",
 "p-media": "With audience, value, capacity, access and reach measured, the last section looks at the market conditions OC Vibe will open into.",
 "p-larc": "The appendix defines every term, method and formula used above, so each figure can be traced, repeated and defended.",
 "p-appx": "The Sources page lists every source with its period, publication date and how Visit Anaheim BI checked it.",
}


def no_em(o):
    """House style: no em dashes. Empty table cells become "n/a"; prose dashes become commas."""
    if isinstance(o, str):
        return "n/a" if o.strip() == "\u2014" else o.replace(" \u2014 ", ", ").replace("\u2014", ", ")
    if isinstance(o, list):
        for i, v in enumerate(o): o[i] = no_em(v)
        return o
    if isinstance(o, tuple):
        return tuple(no_em(v) for v in o)
    if isinstance(o, dict):
        for k in o: o[k] = no_em(o[k])
        return o
    return o


def attach(SECTIONS, prepared="Oct. 13, 2026"):
    for s in SECTIONS:
        n = NEWS.get(s["id"])
        if s["id"] == "p-appx":
            gl, me = s["tables"][1], s["tables"][2]
            have = {r[0] for r in gl["rows"]}
            gl["rows"] += [r for r in GLOSSARY_ADD if r[0] not in have]
            gl["rows"].sort(key=lambda r: r[0].lower())
            if not any(r[0] == METHOD_ADD[0][0] for r in me["rows"]): me["rows"] += METHOD_ADD
            fo = s["tables"][0]
            s["ans"] = f"A plain-language guide: {len(gl['rows'])} terms, {len(me['rows'])} methods and {len(fo['rows'])} formulas, so every figure in this report can be traced and repeated."
            for c in s["cards"]:
                if c[0] == "Glossary": c[2] = str(len(gl["rows"]))
                if c[0] == "Methods": c[2] = str(len(me["rows"]))
            s["kind"] = "Reference"
            continue
        if not n: continue
        assert len(n["details"]) == 6 and s.get("w5h")
        s["kind"] = KIND_NEWS
        s["dateline"] = f"{DATELINE} ({prepared}):"
        s["nut"] = n["nut"]
        s["details"] = [dict(k=k.capitalize(), text=s["w5h"][k], **d) for k, d in zip(("who", "what", "when", "where", "why", "how"), n["details"])]
    pos = {sid: i for i, sid in enumerate(ORDER)}
    SECTIONS.sort(key=lambda x: pos.get(x["id"], len(ORDER)))
    for i, s in enumerate(SECTIONS):
        nx = SECTIONS[i + 1] if i + 1 < len(SECTIONS) else None
        s["next"] = dict(id=nx["id"] if nx else "p-notes", tab=nx["tab"] if nx else "Sources", bridge=BRIDGE.get(s["id"], ""))
        if nx and nx["id"] == "p-appx":   # the app reads: last section, the library, then the Appendix and Sources (Oct. 15, 2026)
            s["next"] = dict(id="p-library", tab="Reports and data library", bridge="Every report and data file behind these sections can be opened or downloaded in the library; the Appendix and Sources follow.")
    no_em(SECTIONS)
