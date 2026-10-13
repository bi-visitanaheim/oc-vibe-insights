"""John Picou's reporting logic, applied across the app:
 - every section explained by Who, What, When, Where, Why, How (W5H)
 - every major point carries its source and date
 - compare and contrast: growth, opportunities, quick wins, early hurdles, pitfalls (hurdles and pitfalls always with a solution)
 - an appendix with glossary, methods and formulas
"""
import impact as I, newdata as ND
from data import EI, N as NN

A, O = EI["Anaheim"], EI["Orange County"]
V = I.VIEWS["Base"]; B = I.RES[1]

# ---------------- source labels with dates ----------------
S_TE_EI = "Tourism Economics, Economic Impact 2025 (pub. Apr.–May 2026)"
S_TE_FC = "Tourism Economics, Travel Forecast (pub. Sept. 2026; data to Aug. 31, 2026)"
S_NIGHT = "Visit Anaheim BI, Extra Night study (2025 inputs; recalculated Oct. 12, 2026)"
S_OCTA = "OCTA Traffic Flow Map (pub. Aug. 2026) and bus schedules (Aug. 9–Nov. 7, 2026)"
S_AZIRA = "Azira via Symphony (District 5, Jan. 1–May 31, 2026; domestic visitors, Aug. 2026)"
S_DATAFY = "Datafy Anaheim visitor report (calendar 2024)"
S_MEDIA = "Azira media attribution via Symphony (ad exposures Jan. 1–Aug. 31, 2026)"
S_COSTAR = "CoStar reports and export (data through Aug. 2026; pulled Oct. 12, 2026)"
S_STR = "STR daily data, Visit Anaheim hotel sets (Jan. 1–Oct. 3, 2026)"
S_LARC = "LARC Market Intelligence Reports (Jan.–Sept. 2026)"
S_VISA = "Visa Destination Insights via Symphony (Aug. 2026 vs. Aug. 2025)"
S_RAIL = "Amtrak ANA fact sheet (2024 data; pub. Oct. 27, 2025); Metrolink FY26 Q2 (Oct.–Dec. 2025)"
S_MT = "Mindtrip trip planner messages (Oct. 1, 2025–Oct. 11, 2026)"
S_CITY = "City of Anaheim OCVibe page (2026); OCVIBE fact sheet (Apr. 2024)"
S_MODEL = "Visit Anaheim BI scenario model (Oct. 12, 2026)"
S_VALID = "Visit Anaheim BI validation suite (run Oct. 12, 2026)"
S_BTS = "U.S. BTS Transportation Economic Trends (2019–2025; accessed Oct. 12, 2026)"

# ---------------- W5H per section ----------------
W5H = {
 "p-ocv": dict(
   who="Visitors who travel 50+ miles or stay overnight, OC Vibe's operators and venues, and Anaheim, Orange County and California economies.",
   what=f"Three views of impact: Anaheim today (${V['ana_today']['spend']/1e9:.2f}B visitor spending), Anaheim with OC Vibe (${V['ana_live']['spend']/1e9:.2f}B), and OC Vibe's own associated impact (${V['ocv_today']['spend']/1e6:,.0f}M today, ${V['ocv_live']['spend']/1e6:,.0f}M when open).",
   when="Baseline is calendar 2025; OC Vibe's first venues open in 2027, the first hotel in 2028 and the full program by about 2030–2032. Estimates are a year at full operation.",
   where="The OC Vibe district (92–100 acres, by source) around Honda Center and ARTIC in Anaheim's Platinum Triangle (Council District 5), measured against Anaheim, Orange County and California.",
   why="OC Vibe's main question is what its opening will add. A holistic view shows today's base, the increase and OC Vibe's own share in one place.",
   how="Net-new visitors × $258 plus extra visitor days × $118.71, converted to impact, jobs and taxes with Tourism Economics 2025 ratios; tested with 42 checks and a 200,000-draw simulation.",
   src=f"{S_TE_EI}; {S_DATAFY}; {S_MODEL}; {S_VALID}"),
 "p-spend": dict(
   who="Anaheim and Garden Grove visitors (domestic and international), as measured by Tourism Economics and Visa cardholders.",
   what=f"Spending per visitor (${I.PV:.0f} in 2025, forecast $279 by 2028), Q2 2026 spending ($1.76B, +7.8%) and visitor card spending ($464.6M in Aug. 2026, +8.1%).",
   when="Calendar 2019–2025 actuals, Q2 2026 actual, forecasts to 2028; Visa August 2026 vs. August 2025.",
   where="City of Anaheim (and Garden Grove for comparison).",
   why="Spending per visitor sets the value of every visitor OC Vibe attracts.",
   how="Tourism Economics visitor spending ÷ visits; Visa reported card spending by visitor cardholders.",
   src=f"{S_TE_FC}; {S_TE_EI}; {S_VISA}"),
 "p-impact": dict(
   who="Workers and households in Anaheim, Garden Grove and Orange County supported by visitor spending.",
   what=f"{A['jobs']:,} jobs in Anaheim (one in three), $10.4B total impact and $970M in state and local taxes; food and beverage is {A['fb_job_share']:.1f}% of those jobs.",
   when="Calendar 2025 vs. 2024.",
   where="Anaheim, Garden Grove and Orange County.",
   why="These ratios turn OC Vibe's visitor spending into jobs and tax revenue.",
   how="Tourism Economics input-output model: direct spending plus supply-chain (indirect) and wage (induced) effects.",
   src=S_TE_EI),
 "p-night": dict(
   who="All 26.5 million Anaheim visitors (17.9 million day visitors, 8.6 million overnight).",
   what=f"One more night is worth about ${NN['lodge_night']/1e6:.0f}M in lodging citywide; each 1% of visitors adding a day is worth ${I.PER_1PCT_DAY/1e6:.1f}M.",
   when="2025 visitors, spending and length of stay.",
   where="City of Anaheim hotels and businesses.",
   why="Longer stays are the fastest way to grow spending without more visitors; OC Vibe's evening venues and hotels are built for this.",
   how="2025 lodging spending ($1.724B) ÷ weighted stay (2.17 days); scenarios hold spending per day constant.",
   src=f"{S_NIGHT}; {S_TE_EI}"),
 "p-transport": dict(
   who="Visitors arriving by car, bus, Amtrak and Metrolink; OCTA, the City and OC Vibe as operators.",
   what="SR-57 carries about 275,000 vehicles a day beside OC Vibe; 277 weekday buses stop at ARTIC (11 leave after 10 p.m.); 191,153 Amtrak passengers used the station in 2024.",
   when="Traffic counts 2021–2024 (2026 map); bus schedules Aug. 9–Nov. 7, 2026; Amtrak 2024; Metrolink Oct.–Dec. 2025.",
   where="SR-57, Katella Ave, Ball Rd, State College Blvd and ARTIC (2626 E. Katella Ave).",
   why="Access shapes how many visitors OC Vibe can host on peak nights and how easily resort guests reach it.",
   how="BI analysis of OCTA's traffic map and raw bus schedules, recounted independently; rail station and line reports.",
   src=f"{S_OCTA}; {S_RAIL}; {S_BTS}; {S_MT}"),
 "p-d5": dict(
   who="Visitors to Council District 5 (where OC Vibe sits) and to Anaheim overall, by origin market.",
   what="85.8% stay overnight, 43.8% are first-time visitors, 44% of domestic visitors come from outside California, and OC Vibe already appears in 5.2% of Anaheim visitor days.",
   when="Azira Jan. 1–May 31, 2026; Datafy calendar 2024; Visa August 2026.",
   where="District 5, Anaheim, and origin markets across the U.S. and abroad.",
   why="Knowing who already comes tells OC Vibe whom to target and how to add a day.",
   how="Mobile location data (Azira, Datafy) and card spending by cardholder origin (Visa).",
   src=f"{S_AZIRA}; {S_DATAFY}; {S_VISA}"),
 "p-media": dict(
   who="People who saw Visit Anaheim paid media and later visited Anaheim.",
   what="368,416 observed visits from 31.0M measurable impressions (11.9 per 1,000); luxury placements returned 34.4.",
   when="Ad exposures Jan. 1–Aug. 31, 2026.",
   where="U.S. audiences; visits observed in Anaheim.",
   why="Campaigns can put OC Vibe in front of audiences who already convert to visits.",
   how="Azira matches exposed devices to later visits (first visit at least three days after exposure).",
   src=S_MEDIA),
 "p-hotel": dict(
   who="Hotels in Orange County submarkets and Visit Anaheim's hotel sets; investors and developers.",
   what="Resort-area hotels fill 78.4% of rooms at $255; only 668 rooms are under construction countywide; Sunday–Monday occupancy is 70.6% vs. 86.2% Friday–Saturday.",
   when="Trailing 12 months and year to date through Aug. 2026 (CoStar); Jan. 1–Oct. 3, 2026 (STR).",
   where="CoStar Disneyland, Anaheim and other Orange County submarkets; Visit Anaheim's Anaheim+ and Garden Grove+ hotel sets.",
   why="Hotel demand and supply decide whether OC Vibe's 550 rooms will fill and which nights need help.",
   how="CoStar and STR performance data; BI recomputation and bootstrap tests.",
   src=f"{S_COSTAR}; {S_STR}"),
 "p-larc": dict(
   who="Anaheim's hotel market, Anaheim Convention Center groups, and developers near OC Vibe.",
   what="Q2 2026 hotel revenue per room +11.4% (U.S. +5.7%); convention room nights pacing +12% (2026) and +17% (2027); inflation about 3.2% a year.",
   when="LARC reports January–September 2026; forecasts to 2030.",
   where="Anaheim hotel market (CoStar basis), OC Vibe and nearby developments.",
   why="The market OC Vibe opens into sets its pricing power and costs.",
   how="LARC analysis of CoStar data, convention pace and Moody's Analytics economic forecasts.",
   src=S_LARC),
 "p-valid": dict(
   who="Visit Anaheim BI, for OC Vibe and anyone using these numbers.",
   what="42 of 42 checks passed; simulation range for OC Vibe's new spending $71M–$122M.",
   when="Validation run Oct. 12, 2026.",
   where="All calculations in this dashboard and deck.",
   why="So OC Vibe can rely on the arithmetic and see which assumptions matter most.",
   how="Exact recomputation, invariants, cross-source reconciliation, statistical tests, Monte Carlo simulation and sensitivity analysis.",
   src=S_VALID),
}

# ---------------- compare and contrast: (type, point, solution or None, source) ----------------
CC = {
 "p-ocv": [
   ("Growth", f"Anaheim visitor spending rises from ${V['ana_today']['spend']/1e9:.2f}B to ${V['ana_live']['spend']/1e9:.2f}B with OC Vibe live (+{B['spend']/V['ana_today']['spend']*100:.1f}%).", None, S_MODEL),
   ("Opportunity", f"OC Vibe's share of Anaheim visitor days can grow from 5.2% to about {V['ocv_live']['share']:.1f}%.", None, f"{S_DATAFY}; {S_MODEL}"),
   ("Quick win", "Share ticket-buyer ZIP codes with Visit Anaheim from the first 2027 shows to replace the two biggest assumptions with real data.", None, S_VALID),
   ("Early hurdle", "No OC Vibe ticketing or hotel data exists yet, so the estimate rests on assumptions.", "Use the staff calculator and Save figures as plans firm up; Visit Anaheim BI refreshes the estimate.", S_MODEL),
   ("Pitfall", "Counting visitors who would have come to Anaheim anyway overstates OC Vibe's impact.", "Count only net-new visitors (50+ miles or overnight, not already in town); report view 3 as associated, not caused.", S_MODEL)],
 "p-spend": [
   ("Growth", "Visitor spending grows faster than visits (+4.1% vs. +1.4% a year to 2028), so spending per visitor rises +2.6% a year.", None, S_TE_FC),
   ("Opportunity", "Visa spending per card rose 4.7% to $85 in August 2026: visitors are spending more per trip.", None, S_VISA),
   ("Quick win", "Price OC Vibe dining and event packages for visitors, not only locals.", None, f"{S_TE_FC}; {S_VISA}"),
   ("Early hurdle", "International card spending fell 5.0% in August 2026.", "Feature OC Vibe in Visit Anaheim's Mexico, Canada and Japan efforts, the top three international markets.", S_VISA),
   ("Pitfall", "Higher prices can inflate spending without more visitors.", "Track visits and spending per visitor together, not spending alone.", S_TE_FC)],
 "p-impact": [
   ("Growth", "Visitor spending grew 3.1% in 2025; jobs supported reached 67,817.", None, S_TE_EI),
   ("Opportunity", "Food and beverage was the fastest-growing category (+5.5%) and OC Vibe plans 35+ restaurants.", None, f"{S_TE_EI}; {S_CITY}"),
   ("Quick win", "Recruit restaurant staff through local hospitality programs before the 2027 openings.", None, S_TE_EI),
   ("Early hurdle", "Labor costs are rising about 6% a year.", "Plan staffing and pricing with those costs built in; cross-train staff across venues.", S_LARC),
   ("Pitfall", "Applying Anaheim's average ratios to a different mix of spending can misstate jobs.", "Refine with OC Vibe's actual category mix once venues report sales.", S_TE_EI)],
 "p-night": [
   ("Growth", "Each 1% of visitors who add a day is worth $31.5M a year.", None, S_NIGHT),
   ("Opportunity", "Two in three Anaheim visitors (67.5%) are day visitors who could be converted to overnight stays.", None, S_TE_EI),
   ("Quick win", "Bundle evening shows with hotel nights and late checkout.", None, S_NIGHT),
   ("Early hurdle", "OC Vibe's own hotels do not open until 2028.", "Partner with nearby Anaheim hotels for 2027 show-and-stay packages.", S_CITY),
   ("Pitfall", "The $3.15B upper bound assumes every visitor adds a day.", "Use the $794M lodging figure or the 1%-step values when planning.", S_NIGHT)],
 "p-transport": [
   ("Growth", "Metrolink's Orange County Line weekday riders rose 4%.", None, S_RAIL),
   ("Opportunity", "15.6 million people live within 50 miles of the ARTIC rail station.", None, S_RAIL),
   ("Quick win", "Publish one 'getting to OC Vibe' page with parking, bus, Amtrak and Metrolink options.", None, f"{S_OCTA}; {S_MT}"),
   ("Early hurdle", "Only 11 buses leave ARTIC after 10 p.m.", "Ask OCTA for event-night extra trips; set rideshare zones at ARTIC.", S_OCTA),
   ("Pitfall", "Sold-out nights at Honda Center and the concert hall together could fill 67%–87% of planned parking.", "Stagger start times, promote transit and the 2028 Katella bridge, and use dynamic parking pricing.", S_MODEL)],
 "p-d5": [
   ("Growth", "85.8% of District 5 visitors already stay overnight.", None, S_AZIRA),
   ("Opportunity", "44% of District 5's domestic visitors come from outside California; fly-in markets include Seattle, Phoenix, Las Vegas, Orlando and New York.", None, f"{S_AZIRA}; {S_VISA}"),
   ("Quick win", "Package OC Vibe with Anaheim Resort stays (13.7% of District 5 visitors already go there).", None, S_AZIRA),
   ("Early hurdle", "International restaurant spending fell 19.1% in August 2026.", "Offer menus and promotions aimed at Mexico and Canada visitors, the largest international markets.", S_VISA),
   ("Pitfall", "Azira, Datafy and Visa count visitors differently.", "Compare trends within each source, not levels across sources.", f"{S_AZIRA}; {S_DATAFY}; {S_VISA}")],
 "p-media": [
   ("Growth", "Paid media drove 368,416 observed visits in eight months of 2026.", None, S_MEDIA),
   ("Opportunity", "Luxury placements returned 34.4 visits per 1,000 impressions, nearly three times the average.", None, S_MEDIA),
   ("Quick win", "Add OC Vibe venues and dining to Visit Anaheim's luxury and travel-planning content.", None, S_MEDIA),
   ("Early hurdle", "Visitors arrive about 39 days after an ad.", "Share OC Vibe event calendars six to eight weeks ahead.", S_MEDIA),
   ("Pitfall", "Attribution shows association, not proof that an ad caused a visit.", "Use control markets or holdout tests for key campaigns.", S_MEDIA)],
 "p-hotel": [
   ("Growth", "Resort-area hotel revenue per room was up in 8 of 8 months of 2026 (+10.9% year to date).", None, S_COSTAR),
   ("Opportunity", "Sunday–Monday occupancy is 15.7 points below Friday–Saturday; each point is worth about $5.1M a year.", None, S_STR),
   ("Quick win", "Schedule Sunday shows and Monday conventions-plus-concert nights.", None, f"{S_STR}; {S_LARC}"),
   ("Early hurdle", "Construction and financing costs limit new hotels (668 rooms under construction countywide).", "Phase OC Vibe's hotels with pre-sold group blocks from the convention center.", S_COSTAR),
   ("Pitfall", "Pricing OC Vibe hotels at resort-area rates ($255) without resort-area demand.", "Benchmark against both the Anaheim ($130) and Disneyland ($255) submarkets and adjust by night of week.", S_COSTAR)],
 "p-larc": [
   ("Growth", "Q2 2026 hotel revenue per room +11.4%, double the U.S. (+5.7%).", None, S_LARC),
   ("Opportunity", "Convention room nights pace +17% for 2027, the year OC Vibe's first venues open.", None, S_LARC),
   ("Quick win", "Offer convention groups OC Vibe evening events in 2027 sales packages.", None, S_LARC),
   ("Early hurdle", "The 2026 World Cup makes Q2–Q3 2027 a tough comparison.", "Set 2027 targets against 2025 as well as 2026.", S_LARC),
   ("Pitfall", "Higher gas prices and airfares, a possible federal shutdown and slower job growth could soften travel.", "Lean on drive markets within 90 miles and flexible, refundable packages.", S_LARC)],
 "p-valid": [
   ("Growth", "Confidence rises as estimates are replaced with measured data after opening.", None, S_VALID),
   ("Opportunity", "Two assumptions explain about 80% of the uncertainty and both can be measured.", None, S_VALID),
   ("Quick win", "Collect ZIP codes at ticket purchase from day one.", None, S_VALID),
   ("Early hurdle", "Some sources disagree (for example, concert hall 5,613 vs. 5,700 seats).", "Use official City figures and confirm with OC Vibe.", S_CITY),
   ("Pitfall", "Treating estimates as forecasts.", "Label them as estimates and refresh them each quarter.", S_VALID)],
}

# ---------------- source + date per "What this means for OC Vibe" bullet ----------------
OCV_SRC = {
 "p-spend": [f"{S_TE_EI}; {S_TE_FC}", S_TE_FC, S_TE_FC, S_VISA],
 "p-impact": [S_TE_EI, f"{S_TE_EI}; {S_CITY}", "Visit Anaheim, 2025 tourism results (pub. June 3, 2026)"],
 "p-night": [S_NIGHT, S_NIGHT, f"{S_TE_EI}; {S_CITY}"],
 "p-transport": [f"{S_OCTA}; {S_COSTAR}", S_OCTA, S_BTS, S_MT, S_RAIL, S_RAIL],
 "p-d5": [S_DATAFY, S_AZIRA, S_AZIRA, S_VISA, S_VISA],
 "p-media": [S_MEDIA, S_MEDIA, S_MEDIA],
 "p-hotel": [f"{S_MODEL}; {S_COSTAR}", S_COSTAR, S_COSTAR, S_STR, S_COSTAR],
 "p-larc": [S_LARC, "Visit Anaheim via CoStar (2026 bookings)", S_LARC, S_LARC],
 "p-valid": [S_VALID, S_VALID, S_VALID],
}
CARD_SRC_DATE = {
 "Tourism Economics": "Tourism Economics (2025; pub. 2026)", "Tourism Economics; BI calculation": "Tourism Economics 2025; BI calc. Oct. 12, 2026",
 "Tourism Economics (forecast)": "Tourism Economics forecast (Sept. 2026)", "BI calculation; Tourism Economics; Azira": "BI calc. Oct. 12, 2026; TE 2025; Azira",
 "BI calculation": "BI calculation (Oct. 12, 2026)", "OCTA Traffic Flow Map (Caltrans 2024)": "OCTA map (Aug. 2026; Caltrans 2024)",
 "OCTA bus schedules; BI analysis": "OCTA schedules (Aug.–Nov. 2026)", "Azira via Symphony": "Azira via Symphony (2026)", "Azira; U.S. Census Bureau": "Azira (2026); U.S. Census",
 "Datafy": "Datafy (2024)", "Azira attribution via Symphony": "Azira attribution (Jan.–Aug. 2026)", "CoStar": "CoStar (through Aug. 2026)",
 "CoStar (hotel sample)": "CoStar hotel sample (12 mo. to Aug. 2026)", "LARC": "LARC (Sept. 2026)", "LARC (Moody's Analytics)": "LARC/Moody's (Sept. 2026)",
 "BI estimate; Tourism Economics ratios": "BI estimate (Oct. 12, 2026); TE 2025 ratios", "Datafy (2024); Tourism Economics": "Datafy (2024); TE 2025",
 "BI estimate": "BI estimate (Oct. 12, 2026)", "Visit Anaheim BI": "Visit Anaheim BI (Oct. 12, 2026)", "BI simulation": "BI simulation (Oct. 12, 2026)",
 "BI sensitivity analysis": "BI sensitivity (Oct. 12, 2026)", "STR; BI bootstrap": "STR (Jan.–Oct. 2026); BI bootstrap",
}
TAKE_SRC = [S_MODEL, S_MODEL, f"{S_TE_EI}; {S_TE_FC}", S_TE_EI, S_NIGHT, f"{S_OCTA}", f"{S_AZIRA}; {S_DATAFY}", S_COSTAR, S_LARC, f"{S_STR}; {S_VISA}; {S_RAIL}"]

# ---------------- recommendations as who / what / when / why / measure ----------------
RECS_T = [
 ["Share ticket-buyer ZIP codes and hotel package results with Visit Anaheim", "OC Vibe ticketing and hotels; Visit Anaheim BI", "From the first 2027 shows; monthly", "The new-visitor and add-a-day shares drive about 80% of the uncertainty", "Share of attendees from 50+ miles; extra nights booked"],
 ["Program evening events with hotel packages", "OC Vibe venues; Anaheim hotels", "2027 (partner hotels); 2028 (OC Vibe hotels)", "Each 1% of visitors who add a day is worth $31.5M a year", "Overnight share; average stay vs. 2.17 days"],
 ["Fill Sunday and Monday nights", "OC Vibe programming; Visit Anaheim sales", "From 2027", "Sun–Mon hotel occupancy is 15.7 points below Fri–Sat; each point is worth about $5.1M", "Sun–Mon occupancy (STR)"],
 ["Feature OC Vibe in Visit Anaheim campaigns for luxury and fly-in markets", "Visit Anaheim marketing; OC Vibe", "Six to eight weeks before each event", "Luxury placements return 34.4 visits per 1,000 impressions", "Visits per 1,000 impressions (Azira)"],
 ["Add late-night transit and a single access page", "OCTA; City of Anaheim; OC Vibe", "Before the 2027 openings", "Only 11 buses leave ARTIC after 10 p.m.", "Event-night transit riders; parking fill rate"],
 ["Use the tight hotel pipeline to support OC Vibe's hotels and dining", "OC Vibe development team", "2026–2028", "Only 668 rooms are under construction countywide; hotel F&B revenue is growing", "OC Vibe hotel occupancy and rate vs. market"],
 ["Set traffic and visitation baselines before opening", "City of Anaheim; Visit Anaheim BI", "Before 2027", "Current Katella counts date from 2021", "New counts on Katella Ave and SR-57; Datafy share 5.2%"],
]

# ---------------- appendix: glossary, methods, formulas ----------------
GLOSSARY = [
 ("ADR (average daily rate)", "Room revenue divided by rooms sold; the average nightly rate."),
 ("ADT (average daily traffic)", "Average number of vehicles passing a point on a weekday, both directions."),
 ("Associated spending", "All visitor spending on days that include a place (here, the OC Vibe area), wherever it is spent; not the same as spending caused by that place."),
 ("Base case", "The most likely set of assumptions; conservative and optimistic cases bracket it."),
 ("Bootstrap", "A statistical method that resamples the data thousands of times to measure how much a result could vary."),
 ("Cap rate", "A hotel's net operating income divided by its value; a measure of investment return."),
 ("Confidence interval (CI)", "A range likely to contain the true value; a 95% CI would capture it 95 times out of 100."),
 ("Day visitor", "A visitor who travels 50+ miles but does not stay overnight."),
 ("Direct, indirect and induced impact", "Visitor spending itself (direct), supplier purchases it triggers (indirect), and spending of wages it supports (induced)."),
 ("GTFS", "General Transit Feed Specification: the public format for bus and rail schedules."),
 ("Group vs. transient demand", "Rooms sold in blocks (conventions, tours) vs. rooms sold individually."),
 ("Jobs supported", "Full- and part-time jobs, including proprietors, sustained by visitor spending."),
 ("Length of stay (LOS)", "Days per visit; Anaheim's weighted average is 2.17 days (domestic 1.9, international 5.9)."),
 ("Monte Carlo simulation", "Running the model many times with assumptions drawn at random within their ranges, to see the spread of outcomes."),
 ("Multiplier", "Total economic impact per $1 of visitor spending (Anaheim 1.53)."),
 ("Net-new visitor", "A visitor who comes to Anaheim because of OC Vibe and would not otherwise have come."),
 ("Occupancy", "Rooms sold divided by rooms available."),
 ("Overnight visitor", "A visitor who stays at least one night in paid or unpaid lodging."),
 ("p-value", "The chance of seeing a result at least this large if there were no real difference; below 0.05 is usually treated as significant."),
 ("Percentile (P5, P50, P95)", "The value below which 5%, 50% (median) or 95% of simulated outcomes fall."),
 ("RevPAR", "Revenue per available room: room revenue divided by rooms available (occupancy × ADR)."),
 ("Scenario", "A consistent set of assumptions (conservative, base, optimistic) used to show a range."),
 ("Sensitivity analysis", "Testing how much the result changes when one assumption changes."),
 ("Sign test", "A test of whether values are consistently up (or down) more often than chance would allow."),
 ("Submarket", "A geographic area CoStar uses to group hotels (for example, Disneyland or Anaheim)."),
 ("TID", "Anaheim Tourism Improvement District: a hotel assessment that funds incentives and marketing."),
 ("TOT", "Transient occupancy tax: Anaheim's 15% tax on hotel room charges."),
 ("Visitor", "Someone who travels 50+ miles or stays overnight (Tourism Economics definition)."),
 ("Visitor day", "One visitor on one day; visitors × length of stay."),
 ("Welch t-test / Mann–Whitney test", "Tests of whether two groups differ; Welch allows unequal spread, Mann–Whitney uses ranks."),
]
FORMULAS = [
 ("Spending per visitor", "Visitor spending ÷ visits", "$6,832M ÷ 26.5M = $258 (2025)"),
 ("Weighted length of stay", "(domestic share × 1.9) + (international share × 5.9)", "(24.7 ÷ 26.5 × 1.9) + (1.8 ÷ 26.5 × 5.9) = 2.17 days"),
 ("Spending per visitor day", "Spending per visitor ÷ weighted stay", "$258 ÷ 2.17 = $118.71"),
 ("One more night (lodging)", "Lodging spending ÷ weighted stay", "$1,724M ÷ 2.17 = $794M"),
 ("Value of 1% adding a day", "Visitors × 1% × spending per visitor day", "26.5M × 1% × $118.71 = $31.5M"),
 ("Venue attendance", "Seats × events × share filled (concert hall + theater and club)", "5,613 × 150 × 80% + 2,300 × 150 × 70% = 915,060"),
 ("Net-new visitors", "Attendance × net-new share", "915,060 × 25% = 228,765"),
 ("New visitor spending", "Net-new visitors × $258 + extra visitor days × $118.71", "228,765 × $258 + 265,000 × $118.71 = $90.5M"),
 ("Total economic impact", "New spending × multiplier (Anaheim 1.53; Orange County 1.70)", "$90.5M × 1.5255 = $138.0M"),
 ("Jobs supported", "New spending ($M) × jobs per $1M (Anaheim 9.93)", "90.5 × 9.93 = about 900"),
 ("State and local taxes", "New spending × tax share (Anaheim 14.2%)", "$90.5M × 14.2% = $12.8M"),
 ("California new spending", "New spending × out-of-state share (44%)", "$90.5M × 44% = $39.8M"),
 ("Hotel room nights", "Rooms × 365 × occupancy", "550 × 365 × 74% = 148,555"),
 ("Hotel tax (TOT)", "Room nights × ADR × 15%", "148,555 × $218 × 15% = $4.9M"),
 ("OC Vibe associated spending (view 3)", "Datafy share × Anaheim visitor spending (+ new spending when live)", "5.2% × $6,832M = $355M; + $90.5M = $446M"),
 ("OC Vibe share of visitor days (live)", "(today's OC Vibe visitor days + new visitor days) ÷ new total", "(2.99M + 0.50M + 0.27M) ÷ 58.3M = 6.4%"),
 ("Value of one Sun–Mon occupancy point", "Rooms × 1% × 104 nights × Sun–Mon ADR", "21,318 × 1% × 104 × $230 = $5.1M"),
 ("Event-night vehicles", "Attendees × share by car ÷ people per car", "(5,613 + 18,300) × 90% ÷ 2.5 = about 8,600"),
 ("RevPAR", "Occupancy × ADR", "78.4% × $255 = $200 (Disneyland submarket)"),
]
METHODS = [
 ("OC Vibe impact (views 2, 3)", "Scenario model adding net-new visitors and extra visitor days to the 2025 base; Tourism Economics ratios for impact, jobs and taxes; Datafy share for view 3.", "Visit Anaheim BI, Oct. 12, 2026"),
 ("Validation", "Exact rational recomputation, invariants, cross-source reconciliation, statistical tests, 200,000-draw Monte Carlo with triangular distributions, sensitivity analysis.", "Visit Anaheim BI, Oct. 12, 2026"),
 ("One more night", "Lodging spending divided by weighted length of stay; scenarios hold spending per day constant.", "Visit Anaheim BI; Tourism Economics 2025"),
 ("Economic impact", "Input-output model (direct, indirect, induced) from visitor surveys, spending data and industry accounts.", "Tourism Economics, pub. Apr.–May 2026"),
 ("Visitor location data", "Mobile device panels matched to places; visitors defined by distance and dwell time.", "Azira via Symphony (2026); Datafy (2024)"),
 ("Card spending", "Reported Visa card transactions, classified by cardholder origin and merchant category.", "Visa via Symphony (Aug. 2026)"),
 ("Hotel performance", "Census and sample of hotel-reported rooms, rates and revenue.", "STR (2026); CoStar (through Aug. 2026)"),
 ("Bus service", "Raw GTFS schedules for a typical weekday (Wed. Oct. 14, 2026); trips stopping at ARTIC docks 1–7.", "OCTA (Aug. 9–Nov. 7, 2026)"),
 ("Traffic", "Weekday average daily traffic from Caltrans and city counts on the OCTA map.", "OCTA (pub. Aug. 2026)"),
 ("Media attribution", "Exposed devices matched to later visits at least three days after exposure.", "Azira via Symphony (2026)"),
]

def attach(SECTIONS, TAKEAWAYS, RECS, STORIES=None):
    if STORIES:
        extra = {"Tourism Economics; BI calculation": "Tourism Economics 2025; BI calc. Oct. 12, 2026", "Azira via Symphony": "Azira via Symphony (2026)", "Azira attribution": "Azira attribution (Jan.–Aug. 2026)", "OCTA": "OCTA (2026)", "OCTA schedules": "OCTA schedules (Aug.–Nov. 2026)", "BI validation": "BI validation (Oct. 12, 2026)", "BI sensitivity": "BI sensitivity (Oct. 12, 2026)", "Azira attribution via Symphony": "Azira attribution (Jan.–Aug. 2026)"}
        for st in STORIES.values():
            st["stats"] = [[v, l, CARD_SRC_DATE.get(src, extra.get(src, src))] for v, l, src in st["stats"]]
            st["chart"]["src"] = CARD_SRC_DATE.get(st["chart"]["src"], extra.get(st["chart"]["src"], st["chart"]["src"]))
    for s in SECTIONS:
        sid = s["id"]
        if sid in W5H: s["w5h"] = W5H[sid]
        if sid in CC: s["cc"] = [dict(type=t, point=p, solution=sol, src=src) for t, p, sol, src in CC[sid]]
        if s.get("ocv") and sid in OCV_SRC:
            srcs = OCV_SRC[sid]; s["ocv_src"] = [srcs[i] if i < len(srcs) else srcs[-1] for i in range(len(s["ocv"]))]
        s["cards"] = [c[:4] + [CARD_SRC_DATE.get(c[4], c[4])] for c in s["cards"]]
    # risk notes with solutions (LARC)
    for s in SECTIONS:
        if s["id"] == "p-larc":
            s["notes"] = [n.replace("becomes a tough comparison in Q2–Q3 2027.", "becomes a tough comparison in Q2–Q3 2027. Solution: set 2027 targets against 2025 as well as 2026.")
                          .replace("may pressure Orange County wages.", "may pressure Orange County wages. Solution: build these costs into OC Vibe pricing and staffing plans, and cross-train staff across venues.")
                          .replace("and slower U.S. job growth.", "and slower U.S. job growth. Solution: lean on drive markets within 90 miles, flexible packages and midweek convention groups.")
                          for n in s["notes"]]
    TAKEAWAYS[:] = [f"{t} (Source: {TAKE_SRC[i]})" if i < len(TAKE_SRC) else t for i, t in enumerate(TAKEAWAYS)]
    RECS[:] = [f"{r[0]}. Who: {r[1]}. When: {r[2]}. Why: {r[3]}. Measure: {r[4]}." for r in RECS_T]
    # appendix section
    SECTIONS.append(dict(
      id="p-appx", tab="Appendix",
      q="What do the terms, methods and formulas in this report mean?",
      period="Glossary, methods and formulas · Oct. 12, 2026",
      ans=f"A plain-language guide: {len(GLOSSARY)} terms, {len(METHODS)} methods and {len(FORMULAS)} formulas with the base-case numbers worked through, so every figure in this report can be traced and repeated.",
      hv=f"{len(FORMULAS)}", hl="Formulas worked through with base-case numbers",
      cards=[["Glossary", "Terms defined", f"{len(GLOSSARY)}", "From ADR to visitor day", "Visit Anaheim BI (Oct. 12, 2026)"],
             ["Methods", "Methods explained", f"{len(METHODS)}", "How each number was produced", "Visit Anaheim BI (Oct. 12, 2026)"],
             ["Formulas", "Formulas with worked examples", f"{len(FORMULAS)}", "Base case, 2025 dollars", "Visit Anaheim BI (Oct. 12, 2026)"]],
      tables=[dict(title="Formulas", sub="Each formula with the base-case numbers used in this report", cols=[["Measure", 0], ["Formula", 0], ["Worked example", 0]],
                   rows=[list(f) for f in FORMULAS], hi=7, full=True, src="Visit Anaheim BI scenario model and source data (Oct. 12, 2026)"),
              dict(title="Glossary", sub="Terms used in this report", cols=[["Term", 0], ["Meaning", 0]], rows=[list(g) for g in GLOSSARY], hi=-1, full=True, wide=True,
                   src="Visit Anaheim BI; Tourism Economics, STR, CoStar and Azira definitions"),
              dict(title="Methods", sub="How each type of number was produced", cols=[["Analysis", 0], ["Method", 0], ["Source and date", 0]], rows=[list(m) for m in METHODS], hi=-1, full=True, wide=True,
                   src="Visit Anaheim BI (Oct. 12, 2026)")],
      charts=[], notes=["Formulas use rounded inputs for readability; the model uses unrounded values, which explains small differences in the last digit.",
                        "See the Sources page for the full source register with dates and how each source was checked."],
      w5h=dict(who="Anyone reading or reusing these numbers.", what="Definitions, methods and formulas.", when="As of Oct. 12, 2026.", where="Applies to the whole dashboard and deck.",
               why="So every figure can be understood, traced and repeated.", how="Plain-language definitions and worked examples using the base case.", src="Visit Anaheim BI (Oct. 12, 2026)"),
    ))
