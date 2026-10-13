"""Role lenses for the OC Vibe team (BIREPORTS-966).

Built from public descriptions of OC Vibe's work and teams (no individuals are named anywhere in the output):
 - Orange County Business Journal, "First Phase of $4B OCVibe Takes Shape" (June 1, 2026)
 - Orange County Business Journal, "OCVibe Aims to be 365-Day-a-Year Destination" (June 30, 2025)
 - Orange County Business Journal, "The Weave Rises as OCVibe's Modern Office Hub" (Sept. 29, 2025)
 - OCVIBE concert hall release, PR Newswire (Mar. 12, 2026)
 - BizBash, Honda Center D23 evening showcases (Sept. 16, 2026)
 - ocvibe.com special events page (accessed Oct. 12, 2026)
Each role's numbers come from data already in this report, with source and date.
"""
import os as _os
BASE = _os.path.dirname(_os.path.abspath(__file__))  # pipeline folder
import impact as I, newdata as ND
from data import EI, N as NN
import logic_content as L

A = EI["Anaheim"]; B = I.RES[1]; V = I.VIEWS["Base"]; TR = I.TR

S_OCBJ26 = "Orange County Business Journal, OCVibe first phase (June 1, 2026)"
S_OCBJ25 = "Orange County Business Journal, OCVibe 365-day destination (June 30, 2025)"
S_WEAVE = "Orange County Business Journal, The Weave (Sept. 29, 2025)"
S_PR = "OCVIBE concert hall release, PR Newswire (Mar. 12, 2026)"
S_BIZ = "BizBash, Honda Center D23 showcases (Sept. 16, 2026)"
S_OSE = "ocvibe.com special events page (accessed Oct. 12, 2026)"
S_PUBLIC = "Public OC Vibe sources: OCBJ (June 30, 2025; Sept. 29, 2025; June 1, 2026), PR Newswire (Mar. 12, 2026), BizBash (Sept. 16, 2026), ocvibe.com (accessed Oct. 12, 2026)"

M = lambda v: f"${v/1e6:.1f}M"
sunmon, frisat = ND.SUNMON_OCC, ND.FRISAT_OCC
ana = ND.STR["Anaheim+"]
hall_lo, hall_hi = TR["hall_vehicles"]; both_lo, both_hi = TR["both_vehicles"]; pk_lo, pk_hi = TR["both_parking_share"]

# capacity check: concert hall seats differ by source (5,000 OCVIBE release; 5,613 City of Anaheim; 5,700 OCBJ 2025)
_cap0 = I.HALL_CAP; I.HALL_CAP = 5000; CAP5000 = I.run()[1]["spend"]; I.HALL_CAP = _cap0

ROLES = [
 dict(id="realestate", label="Real estate & development",
   name="Real estate programming and development operations",
   does="Decides what goes into the district and when (dining, retail, office, entertainment, parks and hotels) and runs the behind-the-scenes infrastructure that makes a guest's visit work from day one: parking, access, utilities, wayfinding and the opening sequence.",
   success="A district that is busy every day of the week, not only on event nights; long visits and repeat visits; tenants that perform; openings that run smoothly.",
   asks=["Which visitor spending categories should the tenant mix serve?", "When are visitors in the area, by day and season?", "Where do visitors come from, and how do they arrive and park?", "How much room is there for more hotel and dining supply?"],
   nums=[("p-ocv", f"New visitor spending splits **34.0% recreation and entertainment, 25.2% lodging, 21.9% retail and 15.6% food and beverage** (base case), a guide for the tenant mix.", f"{L.S_TE_EI}; {L.S_MODEL}"),
         ("p-d5", "District 5 visits are spread across the week: **Saturday 15.9%** at the peak and **Tuesday 13.3%** at the low, so weekday daytime programming matters.", L.S_AZIRA),
         ("p-d5", "**85.8%** of District 5 visitors stay overnight and their median household income is **$85.7K**.", L.S_AZIRA),
         ("p-hotel", f"Visit Anaheim hotels run **{sunmon:.1f}%** full on Sunday–Monday nights vs. **{frisat:.1f}%** on Friday–Saturday: weekday programming has room to fill.", L.S_STR),
         ("p-hotel", "Food and beverage is **29.4%** of Orange County hotel revenue (**22.4%** in the Disneyland submarket), and food revenue per room is up **28.9%**.", L.S_COSTAR),
         ("p-transport", f"When Honda Center and the concert hall both sell out, about **{round(both_lo,-2):,.0f}–{round(both_hi,-2):,.0f} vehicles** arrive, filling **{pk_lo*100:.0f}%–{pk_hi*100:.0f}%** of the 12,369–12,823 planned parking spaces (BI estimate).", f"{L.S_MODEL}; {L.S_CITY}"),
         ("p-transport", "**74.0%** of domestic visitors come from within 50 miles, and about **275,000 vehicles** pass the site on SR-57 each weekday.", f"{L.S_AZIRA}; {L.S_OCTA}"),
         ("p-larc", "Planned hotels near OC Vibe and the resort include OC Vibe's **320-room** Arena Hotel and **230-room** Meadow Hotel; Orange County has **668** rooms under construction.", f"{L.S_LARC}; {L.S_COSTAR}")],
   kpis=["Foot traffic by day and time of day", "Average visit length and repeat-visit rate", "Sales per square foot by tenant category", "Parking use on event and non-event days", "Share of visitors from 50+ miles"],
   wins=[("Plan weekday programming at Urban Park and Katella Commons around the day-of-week pattern and the Sunday–Monday hotel gap.", f"{L.S_AZIRA}; {L.S_STR}"),
         ("Share opening dates with Visit Anaheim so new venues appear in campaigns and the visitor trip planner as they open.", L.S_MT)],
   hurdles=[("Event nights peak while weekdays stay quiet.", "Anchor weekdays with convention groups, corporate lunches, markets and park programming; track foot traffic by day to adjust.", f"{L.S_AZIRA}; {L.S_LARC}"),
            ("Double sell-out nights strain parking and roads.", "Stagger start times with Honda Center, promote ARTIC and OCTA, and post parking guidance before each event.", f"{L.S_MODEL}; {L.S_OCTA}")],
   bring=["Tenant category mix and square footage", "Opening dates by venue", "Parking counts by garage", "Foot traffic counts once open"],
   secs=["p-ocv", "p-d5", "p-hotel", "p-transport", "p-larc"]),

 dict(id="research", label="Research & programming",
   name="Development programming, research and operations",
   does="Builds the evidence behind programming and development decisions: market and demand research, benchmarks and feasibility, plus the operating data that tracks performance once the district opens.",
   success="Decisions grounded in sourced, defensible numbers; baselines set before opening so impact can be measured; a steady data exchange with partners.",
   asks=["What is the baseline today?", "Which assumptions drive the estimate, and how confident is it?", "What should OC Vibe measure from opening day?", "Where do sources disagree?"],
   nums=[("p-ocv", f"Baseline: the OC Vibe area already draws **5.2%** of Anaheim visitor days, about **${V['ocv_today']['spend']/1e6:,.0f}M** in associated visitor spending.", f"{L.S_DATAFY}; {L.S_TE_EI}"),
         ("p-ocv", f"Base estimate **{M(B['spend'])}** a year in new visitor spending; each **1%** of Anaheim visitors adding a day is worth **{M(I.PER_1PCT_DAY)}**, and each **1,000** net-new visitors **$258,000**.", L.S_MODEL),
         ("p-valid", "**42 of 42** calculation checks passed; the 200,000-draw simulation puts new spending at **$71M–$122M** (90% range).", L.S_VALID),
         ("p-valid", "Two inputs drive most of the uncertainty: the share of visitors who add a day (**40%**) and the net-new share (**39%**). Both can be measured with ticketing and survey data.", L.S_VALID),
         ("p-ocv", f"Concert hall capacity differs by source (**5,000** OCVIBE release, Mar. 2026; **5,613** City of Anaheim, 2026; **5,700** OCVIBE fact sheet, 2024). At 5,000 seats the base estimate is **{M(CAP5000)}**, still inside the simulation range.", f"{S_PR}; {L.S_CITY}; {L.S_MODEL}"),
         ("p-appx", "The Appendix lists **19 formulas**, **30 terms** and **10 methods** so every number can be traced and repeated.", "Visit Anaheim BI (Oct. 12, 2026)")],
   kpis=["Ticket buyers by ZIP code (share from 50+ miles)", "Net-new share from a short attendee survey", "Length of stay of OC Vibe visitors", "Hotel room nights linked to OC Vibe events", "Card spending at OC Vibe businesses"],
   wins=[("Capture ticket-buyer ZIP codes from the first 2027 shows; this replaces the two biggest assumptions with measured data.", L.S_VALID),
         ("Enter OC Vibe's own figures in the staff calculator on the OC Vibe impact page to see the effect right away.", L.S_MODEL)],
   hurdles=[("No OC Vibe ticketing or hotel data exists yet, so the estimate rests on assumptions.", "Set baselines now (5.2% share, 2.17-day stay, 85.8% overnight) and refresh quarterly with Visit Anaheim BI as data arrives.", f"{L.S_DATAFY}; {L.S_AZIRA}"),
            ("Sources disagree on capacity, cost and timeline.", "Use the Sources page register as the single reference, confirm figures with OC Vibe, and rerun the model when they change.", "Visit Anaheim BI source register (Oct. 12, 2026)")],
   bring=["Confirmed venue capacities", "Event calendar and ticketing origin (ZIP codes)", "Hotel program and opening dates", "Attendee survey results"],
   secs=["p-ocv", "p-valid", "p-appx", "p-d5"]),

 dict(id="events", label="Special events",
   name="Special events",
   does="Sells and produces private and special events across OC Vibe venues: corporate events and product launches, galas, festivals, award shows and convention-related events, and runs the venue operations behind them.",
   success="More booked dates, especially in softer periods; repeat clients; strong food and beverage revenue per event; events that bring overnight visitors.",
   asks=["When is the market soft, and when is it full?", "Which groups are coming to Anaheim, and when?", "How can Convention Center events pair with OC Vibe venues?", "How do attendees get home after late events?"],
   nums=[("p-larc", "Anaheim Convention Center room nights on the books are up **12%** for 2026 and **17%** for 2027: a growing pool of groups looking for evening and off-site venues.", L.S_LARC),
         ("p-night", "Groups booked with Tourism Improvement District incentives (as of Jan. 2025): **30 events** and **460,566 room nights** in 2026, **26 events** in 2027.", "Simpleview TID incentive bookings (exported Jan. 20, 2025)"),
         ("p-hotel", f"Groups take **18.2%** of rooms sold at Visit Anaheim hotels; Sunday–Monday nights run **{sunmon:.1f}%** full vs. **{frisat:.1f}%** Friday–Saturday, and hotels passed **90%** on **38 nights** this year.", L.S_STR),
         ("p-ocv", "Each point of Sunday–Monday hotel occupancy citywide is worth about **22,200 room nights** and **$5.1M** in room revenue a year.", f"{L.S_STR}; {L.S_MODEL}"),
         ("p-spend", "Visitors spent **$85** per card in August 2026 (**+4.7%**), with an average transaction of **$43**.", L.S_VISA),
         ("p-transport", "On weekdays, **11** OCTA buses leave ARTIC after 10 p.m., so late events need their own plan for getting guests home.", L.S_OCTA)],
   kpis=["Booked event days by day of week", "Share of events with out-of-town guests", "Hotel room nights picked up from events", "Food and beverage revenue per guest", "Repeat-client rate"],
   wins=[("Package OC Vibe venues as evening and off-site options for Convention Center groups with Visit Anaheim's sales team; the D23 showcases (**36,000+** guests over three nights at Honda Center, paired with the Convention Center expo) show the model works.", f"{S_BIZ}; {L.S_LARC}"),
         ("Target corporate and midweek dates on Sunday–Thursday nights, when hotels have rooms and rates are lower.", L.S_STR)],
   hurdles=[("Late-night transit is thin after events.", "Plan shuttles and rideshare zones, and work with OCTA on extra event-night service from ARTIC.", L.S_OCTA),
            ("Hotel compression nights raise costs for out-of-town guests.", "Steer large out-of-town events to shoulder nights, or hold room blocks early with partner hotels.", L.S_STR)],
   bring=["Event calendar (dates, type, expected guests)", "Share of guests from out of town", "Room blocks and hotel pickup", "Post-event guest feedback"],
   secs=["p-larc", "p-hotel", "p-night", "p-spend", "p-transport"]),

 dict(id="venues", label="Entertainment & venues",
   name="Entertainment booking and venue operations",
   does="Books concerts, comedy, sports and other shows across Honda Center, the new concert hall and smaller venues, and runs the event-day operation: staffing, security, access, parking and guest flow.",
   success="High fill rates and well-used dates; a smooth arrival and exit on busy nights; audiences that include visitors from beyond the local area.",
   asks=["How many events and guests does the plan assume?", "What does a sell-out night mean for roads, parking and transit?", "Which nights and seasons are busiest?", "How many attendees are new visitors to Anaheim?"],
   nums=[("p-ocv", f"Base case: **300 events** a year (150 concert hall at 80% full, 150 theater and club at 70%), about **{B['attend']:,.0f} attendees**, of whom **25%** are net-new visitors.", L.S_MODEL),
         ("p-ocv", "Every **100** concert hall nights at 80% full bring about **449,000 attendees** and **$29.0M** in visitor spending at 25% net-new.", L.S_MODEL),
         ("p-transport", f"A sold-out concert hall night means about **{round(hall_lo,-2):,.0f}–{round(hall_hi,-2):,.0f} vehicles**; with Honda Center also sold out, **{round(both_lo,-2):,.0f}–{round(both_hi,-2):,.0f}**.", L.S_MODEL),
         ("p-transport", "About **20 million** people live within a 90-mile drive, and Saturdays are the busiest day in District 5.", f"{L.S_COSTAR}; {L.S_AZIRA}"),
         ("p-transport", "Orange County transit carried **43.8M** passengers in 2017, down from **70.7M** in 2007, while OCTA's fleet grew to **1,066** vehicles: plan for most guests to drive, with spare bus capacity outside peak hours.", "California's transit systems data snapshots (2003–2017; downloaded Oct. 12, 2026)"),
         ("p-hotel", "Visit Anaheim hotels are fullest on Friday and Saturday (**85.7%** and **86.8%**), so weekend shows compete with leisure stays for rooms.", L.S_STR)],
   kpis=["Fill rate by venue", "Event nights per year by venue", "Ticket buyers from 50+ miles", "Arrival and exit times on sell-out nights", "Transit and rideshare share on event nights"],
   wins=[("Coordinate show dates with Honda Center so double sell-outs are planned, not accidental.", L.S_MODEL),
         ("Offer hotel-and-show packages on Sunday and weekday nights with partner hotels.", L.S_STR)],
   hurdles=[("A new venue has no attendance history.", "Use the scenario ranges (100–200 events, 70%–90% full) for planning and replace them with actual counts each quarter.", L.S_MODEL),
            ("Most guests drive, so peak arrivals bunch up.", "Open garages early, use pre-show programming at the plazas, and promote ARTIC on event pages.", f"{L.S_OCTA}; {L.S_MODEL}")],
   bring=["Event counts and attendance by venue", "Ticketing origin (ZIP codes)", "Arrival and parking data on event nights"],
   secs=["p-ocv", "p-transport", "p-hotel", "p-d5"]),

 dict(id="leadership", label="Leadership & finance",
   name="Leadership, strategy and finance",
   does="Sets direction and tracks results for the whole district: strategy, budgets and capital priorities, the scorecard and the briefings that go to owners and the board.",
   success="A clear, sourced view of OC Vibe's contribution; a scorecard that shows progress each quarter; plans that hold up as conditions change.",
   asks=["What will OC Vibe add to Anaheim, Orange County and California?", "What does it already contribute today?", "Which measures belong on the scorecard?", "What could move the numbers up or down?"],
   nums=[("p-ocv", f"Anaheim visitor spending rises from **${V['ana_today']['spend']/1e9:.2f}B** today to **${V['ana_live']['spend']/1e9:.2f}B** with OC Vibe live (base case).", f"{L.S_TE_EI}; {L.S_MODEL}"),
         ("p-ocv", f"Base case a year: **{M(B['spend'])}** new visitor spending, **${B['ana_impact']/1e6:,.0f}M** Anaheim economic impact, about **{B['ana_jobs']:,.0f} jobs**, **{B['rn']/1e3:,.0f}K** hotel room nights and **{M(B['tot'])}** hotel tax.", L.S_MODEL),
         ("p-ocv", "Over the first ten years (2027–2036): **$873M** in new visitor spending and **$1.33B** in Anaheim economic impact (base case).", L.S_MODEL),
         ("p-spend", "Anaheim visitor spending rose **7.8%** in Q2 2026, and spending per visitor is forecast to reach **$279** by 2028.", L.S_TE_FC),
         ("p-larc", "Anaheim hotel revenue per room rose **11.4%** in Q2 2026; local prices are rising about **3.2%** a year.", L.S_LARC)],
   kpis=["Net-new visitor spending (north star)", "OC Vibe share of Anaheim visitor days (5.2% today)", "Overnight share and length of stay", "Hotel room nights and hotel tax", "Jobs supported"],
   wins=[("Adopt the \"Measures OC Vibe can build on\" table as the starting scorecard, with baselines already filled in.", L.S_MODEL),
         ("Hold a quarterly data review with Visit Anaheim BI to refresh the three views of impact.", "Visit Anaheim BI (Oct. 12, 2026)")],
   hurdles=[("Estimates can be mistaken for measured results.", "Report view 1 as measured and views 2–3 as estimates, and replace assumptions with OC Vibe data as it arrives.", L.S_MODEL),
            ("Market conditions (gas prices, airfares, inflation) can soften travel.", "Lean on the drive market within 90 miles and midweek convention groups, and review the scenarios each quarter.", f"{L.S_LARC}; {L.S_BTS}")],
   bring=["Phasing and opening dates", "Budget assumptions for events and hotels", "Scorecard measures already in use"],
   secs=["p-ocv", "p-impact", "p-spend", "p-larc", "p-valid"]),

 dict(id="marketing", label="Marketing & partnerships",
   name="Marketing, partnerships and community",
   does="Builds OC Vibe's audience and brand, sells sponsorships and founding partnerships, and works with the community and the City on the district's public spaces and benefits.",
   success="Growing audiences from new markets; partners who can see who they reach; a district the community values.",
   asks=["Who visits today, and where do they come from?", "Which markets and campaigns bring visitors most efficiently?", "What reach can partners expect?", "What does OC Vibe mean for local jobs and the community?"],
   nums=[("p-d5", "Visitor card spending in August 2026: **66.1%** from the Los Angeles metro; fly-in markets include Seattle, Phoenix, Las Vegas, Orlando and New York; Mexico (**$5.2M**) and Canada (**$3.2M**) lead international.", L.S_VISA),
         ("p-d5", "**43.8%** of District 5 visitors are new visitors, and **44%** of domestic visitors come from outside California.", L.S_AZIRA),
         ("p-media", "Visit Anaheim's luxury campaign drew **34.4** visits per 1,000 impressions vs. an **11.9** average across **31.0M** impressions.", L.S_MEDIA),
         ("p-transport", "Travelers ask Visit Anaheim's trip planner about OC Vibe's opening, Honda Center events and dining near the arena: early demand for content.", L.S_MT),
         ("p-impact", f"Visitors support **67,817** Anaheim jobs today; OC Vibe's base case adds about **{B['ana_jobs']:,.0f}**, including about **150** in food and beverage.", f"{L.S_TE_EI}; {L.S_MODEL}")],
   kpis=["Share of visitors from outside California", "Visits per 1,000 impressions for campaigns featuring OC Vibe", "Spending from fly-in and international markets", "New vs. repeat visitors", "Partner reach (impressions, attendance)"],
   wins=[("Feature OC Vibe openings in Visit Anaheim campaigns aimed at the luxury and fly-in audiences that perform best.", L.S_MEDIA),
         ("Publish clear answers on opening dates, parking and getting there; travelers are already asking.", L.S_MT)],
   hurdles=[("Most visitors live nearby (74.0% within 50 miles).", "Use locals for repeat visits and weekday traffic, and grow out-of-state share through Visit Anaheim campaigns.", L.S_AZIRA),
            ("International card spending fell 5.0% in August 2026.", "Focus on Mexico, Canada and Japan, the top three international markets, with Visit Anaheim.", L.S_VISA)],
   bring=["Campaign calendar and creative featuring OC Vibe", "Partner audience goals", "Community programming plans"],
   secs=["p-d5", "p-media", "p-impact", "p-transport", "p-spend"]),
]

for _r in ROLES:   # plain text; the app and deck bold key numbers automatically
    _r["nums"] = [(a, t.replace("**", ""), c) for a, t, c in _r["nums"]]
    _r["wins"] = [(w.replace("**", ""), c) for w, c in _r["wins"]]
ROLE_BY_ID = {r["id"]: r for r in ROLES}
assert not any(_n in repr(ROLES) for _n in ("Carter", "Atkinson", "Pederson"))   # roles only, no individuals


def _plain(t):
    return t.replace("**", "")


def team_section():
    first = lambda r: _plain(r["nums"][0][1])
    tabs = {"p-ocv": "OC Vibe impact", "p-spend": "Visitor spending", "p-impact": "Jobs and economy", "p-night": "One more night", "p-transport": "Getting here",
            "p-d5": "Who visits", "p-media": "Marketing reach", "p-hotel": "Hotel market", "p-larc": "OC Vibe outlook", "p-valid": "Checks and confidence", "p-appx": "Appendix"}
    t0 = dict(title="What this report gives each part of the OC Vibe team", sub="Choose a role above the sections to see its numbers on every page",
              cols=[["Role", 0], ["What success looks like", 0], ["Start with", 0]],
              rows=[[r["name"], r["success"], ", ".join(tabs[s] for s in r["secs"][:3])] for r in ROLES], hi=-1, full=True, wide=True,
              src=f"{S_PUBLIC}; Visit Anaheim BI (Oct. 12, 2026)")
    t1 = dict(title="Numbers each role can use", sub="With source and date", cols=[["Role", 0], ["Number and what it means", 0], ["Source and date", 0]],
              rows=[[r["label"], _plain(t), s] for r in ROLES for (_, t, s) in r["nums"]], hi=-1, wide=True, src="See each row")
    t2 = dict(title="Measures to track, by role", sub="Each can be added to the shared scorecard", cols=[["Role", 0], ["Measure", 0]],
              rows=[[r["label"], k] for r in ROLES for k in r["kpis"]], hi=-1, src="Visit Anaheim BI (Oct. 12, 2026)")
    t3 = dict(title="Quick wins and early hurdles, by role", sub="Every hurdle comes with a solution", cols=[["Role", 0], ["Type", 0], ["Point", 0], ["Solution", 0], ["Source and date", 0]],
              rows=[[r["label"], "Quick win", _plain(w), "—", s] for r in ROLES for (w, s) in r["wins"]] +
                   [[r["label"], "Early hurdle", h, sol, s] for r in ROLES for (h, sol, s) in r["hurdles"]], hi=-1, wide=True, src="See each row")
    return dict(
      id="p-team", tab="For your team",
      q="What does this report give each part of the OC Vibe team?",
      period=f"{len(ROLES)} roles · data through Sept. 2026 · Oct. 12, 2026",
      ans=f"Each part of the OC Vibe team gets the numbers it needs to decide and act: tenant mix and weekday traffic for real estate programming, baselines and confidence for research, soft dates and convention groups for special events, sell-out logistics for venues, the scorecard for leadership, and markets and reach for marketing. Choose a role at the top of any page to see its numbers there.",
      hv=f"{len(ROLES)}", hl="Role views, each with numbers, measures, quick wins and hurdles",
      cards=[["OC Vibe Phase 1", "Opens", "Early 2027", "Concert hall, Katella Commons market hall, The Weave office and Urban Park", S_OCBJ26],
             ["Convention Center", "Room nights on the books, 2027", "▲ +17%", "2026 ▲ +12% · groups looking for evening venues", L.S_LARC],
             ["Visit Anaheim hotels", "Sunday–Monday occupancy", f"{sunmon:.1f}%", f"vs. {frisat:.1f}% Friday–Saturday · room to grow weekdays", L.S_STR],
             ["OC Vibe area today", "Share of Anaheim visitor days", "5.2%", f"About {V['ocv_live']['share']:.1f}% when live (base case)", f"{L.S_DATAFY}; {L.S_MODEL}"]],
      tables=[t0, t1, t2, t3], charts=[],
      notes=["Role views describe the kinds of work each team does, drawn from OC Vibe's public descriptions of its district and teams; no individuals are named.",
             "Each number is repeated from the section it comes from, with the same source and date; estimates are labeled as Visit Anaheim BI estimates.",
             f"Public OC Vibe sources used: {S_PUBLIC}."],
      w5h=dict(who="OC Vibe's teams: real estate programming and development operations; research and programming; special events; entertainment and venues; leadership and finance; marketing, partnerships and community.",
               what="For each role: what it works on, what success looks like, the questions this report answers, the numbers to use, measures to track, quick wins, and early hurdles with solutions.",
               when="Data through Sept. 2026 (hotel data through Oct. 3, 2026); Phase 1 opens early 2027, the first hotel and the Katella bridge in 2028, full build-out about 2033 (OCBJ, June 2026).",
               where="The OC Vibe district around Honda Center and ARTIC, Anaheim's Platinum Triangle (Council District 5).",
               why="The same data answers different questions for different teams; showing each team its own numbers makes the report faster to use.",
               how="Matched each role's public responsibilities to sections of this report, then pulled the relevant figures with their sources and dates.",
               src=f"{S_PUBLIC}; Visit Anaheim BI (Oct. 12, 2026)"),
      cc=[dict(type="Growth", point="Convention Center room nights on the books are up 17% for 2027, a growing pool of groups for OC Vibe venues.", solution=None, src=L.S_LARC),
          dict(type="Opportunity", point=f"Sunday–Monday hotel occupancy ({sunmon:.1f}%) trails Friday–Saturday ({frisat:.1f}%); weekday programming and events can fill the gap.", solution=None, src=L.S_STR),
          dict(type="Quick win", point="Capture ticket-buyer ZIP codes from the first 2027 shows and share them quarterly with Visit Anaheim BI.", solution=None, src=L.S_VALID),
          dict(type="Early hurdle", point="Each team holds part of the data (tenants, events, tickets, hotels).", solution="Agree one quarterly data exchange and one shared scorecard across teams.", src=L.S_MODEL),
          dict(type="Pitfall", point="Teams can quote different numbers for the same thing (for example, concert hall capacity).", solution="Use the Sources page register as the single reference and confirm figures with OC Vibe before publishing.", src="Visit Anaheim BI source register (Oct. 12, 2026)")],
      roles=[{k: r[k] for k in ("id", "label", "name", "does", "success", "asks", "nums", "kpis", "wins", "hurdles", "bring", "secs")} for r in ROLES],
    )


REG_ROWS = [
 ["Orange County Business Journal", "First Phase of $4B OCVibe Takes Shape", "Phase 1 status as of June 2026", "June 1, 2026", "Phase 1 openings, parking, Katella Commons, LA28", "Matched against City of Anaheim and OCVIBE release"],
 ["Orange County Business Journal", "OCVibe Aims to be 365-Day-a-Year Destination; The Weave", "Plans as of 2025", "June 30, 2025; Sept. 29, 2025", "Phasing timeline, The Weave office", "Timeline cross-checked with June 2026 article; older dates flagged"],
 ["OCVIBE (PR Newswire)", "Concert hall design release", "As of Mar. 2026", "Mar. 12, 2026", "Concert hall capacity (5,000) and uses; capacity check", "Compared with City of Anaheim (5,613) and OCVIBE fact sheet 2024 (5,700); difference noted"],
 ["BizBash", "Honda Center D23 evening showcases", "Aug. 2026 event", "Sept. 16, 2026", "Honda Center and Convention Center event pairing", "Attendance as reported; not independently verified"],
 ["OCVIBE", "ocvibe.com special events page", "Current offering", "Accessed Oct. 12, 2026", "OC Vibe special events offering", "Public page; no figures used"],
]


def attach(SECTIONS, DQ, REGISTER, SOURCES):
    _cap = f" OCVIBE's newest figure is 5,000 seats (concert hall release, Mar. 12, 2026); at 5,000 seats the base estimate falls from {M(B['spend'])} to {M(CAP5000)}, inside the simulation range."
    _i = next((i for i, d in enumerate(DQ) if "5,613" in d), None)
    if _i is None: DQ.append("Concert hall capacity differs by source: 5,613 (City of Anaheim, 2026) and 5,700 (OCVIBE fact sheet, 2024)." + _cap + " Confirm with OC Vibe.")
    else: DQ[_i] = DQ[_i] + _cap
    REGISTER.extend(REG_ROWS)
    SOURCES.append(("Public OC Vibe sources", "Orange County Business Journal (June 30, 2025; Sept. 29, 2025; June 1, 2026), OCVIBE concert hall release (Mar. 12, 2026), BizBash (Sept. 16, 2026) and ocvibe.com (accessed Oct. 12, 2026): phasing, venues and events."))


# ---------- California transit systems data snapshots (Orange County operators, 2003–2017) ----------
import csv as _csv
S_SCO = "California's transit systems data snapshots, Orange County: Transit Operating Statistics (employees, passengers, vehicles) and Transit Financial Data (revenues and expenses), 2003–2017; downloaded Oct. 12, 2026"

def _snap(fn):
    rows = list(_csv.reader(open(BASE + "/files/" + fn, encoding="utf-8-sig")))
    hdr = next(r for r in rows if r and r[0] == "" and len(r) > 2)
    yrs = [int(y.strip()) for y in hdr[1:]]
    data = {r[0]: [float(v.replace(",", "").strip()) for v in r[1:]] for r in rows if r and r[0] and len(r) == len(hdr)}
    return yrs, data

YRS, STAFF = _snap("ca_transit_fte_orange.csv")
_y2, EXP = _snap("ca_transit_fin_orange.csv")       # Transit Financial Data - Orange; totals equal "Expenses" in the Types file
_y3, REV = _snap("ca_transit_rev_orange.csv")       # Transit Financial Data - Orange; totals equal "Revenues" in the Types file
_y4, TYP = _snap("ca_transit_types_orange.csv")     # Revenues, Expenses, Revenues Less Expenses (county)
_y5, PAX = _snap("ca_transit_pax_orange.csv")         # Total passengers by operator
_y6, PAXM = _snap("ca_transit_pax_mode_orange.csv")   # Total passengers by mode (county)
_y7, FLEET = _snap("ca_transit_fleet_orange.csv")     # Total revenue vehicle inventory by operator
assert YRS == _y2 == _y3 == _y4 == _y5 == _y6 == _y7
TRANSIT_CHECKS = []
for _name, _d in (("staff", STAFF), ("expenses", EXP), ("revenues", REV), ("passengers by operator", PAX), ("passengers by mode", PAXM), ("vehicles", FLEET)):   # totals equal the sum of operators
    for _i in range(len(YRS)):
        assert abs(sum(v[_i] for k, v in _d.items() if k != "Total") - _d["Total"][_i]) < 1, (_name, _i)
    TRANSIT_CHECKS.append(f"{_name}: operator rows sum to the total in all {len(YRS)} years")
for _i in range(len(YRS)):   # the operator files reconcile to the county types file
    assert abs(EXP["Total"][_i] - TYP["Expenses"][_i]) < 1 and abs(REV["Total"][_i] - TYP["Revenues"][_i]) < 1
    assert abs(TYP["Revenues"][_i] - TYP["Expenses"][_i] - TYP["Revenues Less Expenses"][_i]) < 1
TRANSIT_CHECKS.append("operator revenue and expense totals match the county Revenues and Expenses rows; revenues less expenses recomputes exactly")
for _i in range(len(YRS)):
    assert abs(PAX["Total"][_i] - PAXM["Total"][_i]) < 1
TRANSIT_CHECKS.append("passenger totals by operator and by mode match in all years")
OCTA, SPEC, LAG = "Orange County Transportation Authority", "Orange County Transportation Authority - Specialized Service", "Laguna Beach"


def transit_attach(SECTIONS, DQ, REGISTER, SOURCES):
    chg = lambda a: (a[-1] / a[0] - 1) * 100
    m = lambda v: ("−" if v < 0 else "") + f"${abs(v)/1e6:,.1f}M"
    i09, i10 = YRS.index(2009), YRS.index(2010)
    t1 = dict(title="Orange County transit operators: staff and expenses, 2003–2017",
              sub="Total employees and operating expenses by operator, nominal dollars · * 2006 total includes a Laguna Beach reporting outlier",
              cols=[["Year", 0], ["OCTA staff", 1], ["OCTA expenses", 1], ["Specialized service staff", 1], ["Specialized service expenses", 1], ["All operators, staff", 1], ["All operators, expenses", 1]],
              rows=[[str(y), f"{STAFF[OCTA][i]:,.0f}", m(EXP[OCTA][i]), f"{STAFF[SPEC][i]:,.0f}", m(EXP[SPEC][i]), f"{STAFF['Total'][i]:,.0f}" + (" *" if y == 2006 else ""), m(EXP["Total"][i])]
                    for i, y in enumerate(YRS)][::-1], hi=0, src=S_SCO)
    neg = sum(1 for v in TYP["Revenues Less Expenses"] if v < 0)
    t2 = dict(title="Orange County transit revenues and expenses, 2003–2017",
              sub="All operators, nominal dollars, as reported",
              cols=[["Year", 0], ["Revenues", 1], ["Expenses", 1], ["Revenues less expenses", 1], ["OCTA revenues", 1], ["Specialized service revenues", 1]],
              rows=[[str(y), m(TYP["Revenues"][i]), m(TYP["Expenses"][i]), m(TYP["Revenues Less Expenses"][i]), m(REV[OCTA][i]), m(REV[SPEC][i])] for i, y in enumerate(YRS)][::-1],
              hi=0, src=S_SCO)
    pk = max(range(len(YRS)), key=lambda i: PAX["Total"][i])
    t3 = dict(title="Orange County transit passengers and vehicles, 2003–2017",
              sub="Total passengers and revenue vehicles, all operators · expenses per passenger = expenses ÷ passengers (BI calculation)",
              cols=[["Year", 0], ["Passengers, all", 1], ["Bus", 1], ["Demand response", 1], ["OCTA vehicles", 1], ["All vehicles", 1], ["Expenses per passenger", 1]],
              rows=[[str(y), f"{PAX['Total'][i]/1e6:,.1f}M", f"{PAXM['Bus'][i]/1e6:,.1f}M", f"{PAXM['Demand Response'][i]/1e6:,.2f}M", f"{FLEET[OCTA][i]:,.0f}", f"{FLEET['Total'][i]:,.0f}", f"${EXP['Total'][i]/PAX['Total'][i]:.2f}"]
                    for i, y in enumerate(YRS)][::-1], hi=0, src=S_SCO)
    o_s, o_e = STAFF[OCTA], EXP[OCTA]
    per0, per1 = o_e[0] / o_s[0], o_e[-1] / o_s[-1]
    for s in SECTIONS:
        if s["id"] == "p-transport":
            s["tables"] += [t3, t1, t2]
            s["notes"].append(f"Orange County transit ridership peaked at {PAX['Total'][pk]/1e6:.1f}M passengers in {YRS[pk]} and fell to {PAX['Total'][-1]/1e6:.1f}M by {YRS[-1]} ({(PAX['Total'][-1]/PAX['Total'][pk]-1)*100:.0f}%), while OCTA's vehicle fleet grew from {FLEET[OCTA][0]:,.0f} to {FLEET[OCTA][-1]:,.0f}. Expenses per passenger rose from ${EXP['Total'][0]/PAX['Total'][0]:.2f} to ${EXP['Total'][-1]/PAX['Total'][-1]:.2f}. For OC Vibe this means most guests will drive, which supports the model's 5% transit assumption, and that buses have spare seats outside peak hours. Solution: pair event-night service requests with ticket-and-transit promotions so added buses fill.")
            s["notes"].append(f"Orange County transit, 2003–2017: OCTA's staff fell {abs(chg(o_s)):.1f}% ({o_s[0]:,.0f} to {o_s[-1]:,.0f}), with the largest drop after 2009 ({o_s[i09]:,.0f} to {o_s[i10]:,.0f}), while its expenses rose {chg(o_e):.1f}% ({m(o_e[0])} to {m(o_e[-1])}), or from ${per0/1e3:,.0f}K to ${per1/1e3:,.0f}K per employee. Specialized service expenses grew fastest ({m(EXP[SPEC][0])} to {m(EXP[SPEC][-1])}, +{chg(EXP[SPEC]):.0f}%). Countywide, expenses exceeded revenues in {neg} of {len(YRS)} years (2017: {m(TYP['Revenues Less Expenses'][-1])}). A leaner, cost-pressured system can limit how much extra event-night service OCTA adds on short notice. Solution: OC Vibe should request event-night service early, share its event calendar with OCTA, and consider co-funding late-night service on its biggest nights. The data ends in 2017, so it shows the long-term trend, not today's budgets.")
    DQ.append("California transit systems snapshots: the latest year is 2017, so they show trend, not current staffing or budgets. Dollars are nominal (not adjusted for inflation). The two operator files are expenses and revenues: their totals match the county Expenses and Revenues rows exactly. Laguna Beach shows 1,647 employees in 2006 (14–125 in other years), which points to a reporting error; the 2006 all-operator staff total (4,091) is affected. The OCTA rows are consistent.")
    DQ.append("California transit passenger and vehicle snapshots: Laguna Beach reports 0 passengers in 2013 and the mode file reports 0 \"Other\" passengers in 2007 and 2010, which look like missing reports. Demand-response passengers in 2010 differ by file (2.33M by mode vs. 1.48M for OCTA specialized service), though the county totals match. OCTA specialized service lists 848 vehicles in 2016 (486–587 around it), likely a reporting outlier. Two uploads were duplicates (Snapshot 3 and Snapshot 4) and were counted once.")
    REGISTER.append(["California's transit systems (data snapshots)", "Transit Operating Statistics (total passengers by operator and by mode; revenue vehicle inventory) – Orange County", "2003–2017", "Downloaded Oct. 12, 2026", "Transit ridership and fleet trends (Getting here)", "Operator and mode passenger totals match each other; rows sum to totals; zero-passenger years flagged"])
    REGISTER.append(["California's transit systems (data snapshots)", "Transit Operating Statistics (total employees); Transit Financial Data by operator (revenues, expenses) and by type – Orange County", "2003–2017", "Downloaded Oct. 12, 2026", "Transit staff, expense and revenue trends (Getting here)", "Operator rows sum to totals; operator totals match county revenues and expenses; revenues less expenses recomputed; Laguna Beach 2006 outlier flagged"])
    SOURCES.append(("California's transit systems data snapshots", "Orange County operators (OCTA, OCTA specialized service, Laguna Beach): total employees, revenues and expenses, 2003–2017, downloaded Oct. 12, 2026."))
