"""Reports and data library (Oct. 14, 2026): every source file behind OC Vibe Insights, viewable and downloadable in the app.

Decision recorded Oct. 14, 2026: John Picou (BI & Technology Director) cleared all source files used to build the app
for public sharing in the app and on the public website. Files are served from public/library/ (website) and the same
paths on the claude.ai artifact. `orig` is the original file name as received; `file` is the published name.
Visit Anaheim-owned Office files are published with neutral document properties (scripts/stage_library.py).
"""
import os

LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'library')

# Topics, in the order the library shows them
TOPICS = [
    ("econ", "Economic impact (Tourism Economics)", "Annual visitors, spending, jobs, income and taxes for Anaheim, Garden Grove and Orange County."),
    ("forecast", "Quarterly results and forecasts", "Tourism Economics' quarterly travel forecast, including the latest quarter's actual results."),
    ("night", "One more night study", "Visit Anaheim's Extra Night study and its workbook."),
    ("visitors", "Who visits and District 5", "Symphony | Tourism Economics (Azira) location data, Visa card spending and Datafy."),
    ("media", "Marketing attribution", "Visits observed after Visit Anaheim's paid media."),
    ("hotels", "Hotels", "CoStar, STR and LARC hotel performance, pipeline and forecasts."),
    ("outlook", "Market outlook", "LARC Market Intelligence Reports for the Anaheim market."),
    ("transport", "Getting here and transportation", "Traffic, transit, rail and travel-cost data."),
    ("program", "Destination program", "Visit Anaheim's 2027 program of experiences."),
    ("report", "This report", "The full OC Vibe Insights report and the questions-answered deck."),
]

F = []
def add(id, file, orig, topic, title, publisher, kind, period, published, summary, geo, used_in, note="", **kw):
    F.append(dict(id=id, file=file, orig=orig, topic=topic, title=title, publisher=publisher, kind=kind, period=period,
                  published=published, summary=summary, geo=geo, used_in=used_in, note=note, **kw))

# ---- Economic impact (Tourism Economics, calendar 2025) ----
add("te-ei-ana", "te-economic-impact-2025-anaheim.pdf", "Anaheim Tourism Economic Impact - 2025 - CLIENT PRELIMINARY.pdf", "econ",
    "Economic Impact of Visitors to Anaheim, 2025", "Tourism Economics for Visit Anaheim", "Report", "Calendar 2025 vs. 2024", "Apr. 2026",
    "26.5M visitors, $6.832B visitor spending, $10.4B total economic impact, 67,817 jobs (one in three), $3.0B labor income, $1.0B state and local taxes; spending and jobs by industry, including food and beverage and transportation.",
    ["Anaheim"], ["p-ocv", "p-spend", "p-impact", "p-night", "p-transport"], "Marked client preliminary by Tourism Economics.")
add("te-ei-ana-sup", "te-economic-impact-2025-anaheim-supplemental-charts.pdf", "Anaheim Tourism Economic Impact - Supplemental Charts - 2025 - CLIENT PRELIMINARY.pdf", "econ",
    "Economic Impact of Visitors to Anaheim, 2025: supplemental charts", "Tourism Economics for Visit Anaheim", "Charts", "Calendar 2025", "Apr. 2026",
    "Charts of business sales, employment, personal income and taxes by type of impact and by industry.", ["Anaheim"], ["p-impact"])
add("te-ei-gg", "te-economic-impact-2025-garden-grove.pdf", "Garden Grove Tourism Economic Impact - 2025 - CLIENT PRELIMINARY.pdf", "econ",
    "Economic Impact of Visitors to Garden Grove, 2025", "Tourism Economics for Visit Anaheim", "Report", "Calendar 2025 vs. 2024", "Apr. 2026",
    "3.24M visitors, $769.3M visitor spending, $1.1B total impact, 6,694 jobs (one in eight), with food and beverage holding 40.6% of jobs.",
    ["Garden Grove"], ["p-impact", "p-spend"], "Marked client preliminary by Tourism Economics.")
add("te-ei-gg-sup", "te-economic-impact-2025-garden-grove-supplemental-charts.pdf", "Garden Grove Tourism Economic Impact - Supplemental Charts - 2025 - CLIENT PRELIMINARY.pdf", "econ",
    "Economic Impact of Visitors to Garden Grove, 2025: supplemental charts", "Tourism Economics for Visit Anaheim", "Charts", "Calendar 2025", "Apr. 2026",
    "Charts of business sales, employment, personal income and taxes by type of impact and by industry.", ["Garden Grove"], ["p-impact"])
add("te-ei-oc", "te-economic-impact-2025-orange-county.pdf", "Orange County Tourism Economic Impact - 2025 - CLIENT PRELIMINARY.pdf", "econ",
    "Economic Impact of Visitors to Orange County, 2025", "Tourism Economics for Visit Anaheim", "Report", "Calendar 2025 vs. 2024", "May 2026",
    "51.3M visitors, $18.0B visitor spending ($350 per visitor; day $58, overnight $737), $30.7B total impact, 178,164 jobs (one in 14), $3.1B state and local taxes.",
    ["Orange County"], ["p-impact", "p-spend", "p-transport"], "Marked client preliminary by Tourism Economics.")
add("te-ei-oc-sup", "te-economic-impact-2025-orange-county-supplemental-charts.pdf", "Orange County Tourism Economic Impact - Supplemental Charts - 2025 - CLIENT PRELIMINARY.pdf", "econ",
    "Economic Impact of Visitors to Orange County, 2025: supplemental charts", "Tourism Economics for Visit Anaheim", "Charts", "Calendar 2025", "May 2026",
    "Charts of business sales, employment, personal income and taxes by type of impact and by industry.", ["Orange County"], ["p-impact"])
add("te-ei-one", "te-economic-impact-2025-one-pagers.pdf", "One_Pagers_2025 - CLIENT PRELIMINARY.pdf", "econ",
    "Economic impact one-pagers, 2025: Orange County, Anaheim and Garden Grove", "Tourism Economics for Visit Anaheim", "Summary", "Calendar 2025", "Apr. 2026",
    "One page each: total impact, jobs, labor income, and state and local, sales, property and lodging tax revenue.",
    ["Anaheim", "Garden Grove", "Orange County"], ["p-impact"])

# ---- Quarterly results and forecasts ----
add("te-fc-sep", "te-travel-forecast-2026-09-q2-results.pdf", "Anaheim Travel Forecast - 09-2026 - CLIENT PRELIMINARY.pdf", "forecast",
    "Anaheim and Garden Grove Travel Forecast, Sept. 2026 (Q2 2026 results)", "Tourism Economics for Visit Anaheim", "Report", "2019–2028; Q2 2026 actual", "Sept. 2026",
    "Q2 2026: Anaheim 6.74M visitors (+2.8%) spent $1.76B (+7.8%); Garden Grove 831,000 visitors (+3.4%) spent $200.4M (+7.1%). Forecasts to 2028, international visitors by market and the U.S. outlook.",
    ["Anaheim", "Garden Grove", "U.S."], ["p-spend", "p-ocv", "p-larc"], "Data through Aug. 31, 2026. Marked client preliminary.")
add("te-fc-jun", "te-travel-forecast-2026-06-q1-results.pdf", "Anaheim Travel Forecast - 06-2026 - CLIENT PRELIMINARY (1).pdf", "forecast",
    "Anaheim and Garden Grove Travel Forecast, June 2026 (Q1 2026 results)", "Tourism Economics for Visit Anaheim", "Report", "2019–2028; Q1 2026 actual", "June 2026",
    "Q1 2026: Anaheim 6.31M visitors (+3.1%) spent $1.72B (+7.1%). The prior edition, for comparison with September.",
    ["Anaheim", "Garden Grove", "U.S."], ["p-spend"], "Superseded by the Sept. 2026 edition.")

# ---- One more night ----
add("va-night", "visit-anaheim-extra-night-study.pptx", "Extra Night Calculation (1).pptx", "night",
    "One more night study (Extra Night Calculation)", "Visit Anaheim Business Intelligence", "Study", "2025 inputs", "2025; recalculated Oct. 12, 2026",
    "If every visitor stayed one more day: weighted average stay 2.17 days, spending per day $3.15B, total $9.98B. Also lists TID incentive group bookings by year, 2022–2034.",
    ["Anaheim"], ["p-night"], "The deck shows $9.9B; the calculation gives $9.98B.", scrub=True)
add("va-night-wb", "visit-anaheim-extra-night-workbook.xlsx", "TID Request_1_20_25.xlsx", "night",
    "One more night workbook (TID Request data)", "Visit Anaheim Business Intelligence (Symphony, STR, Simpleview inputs)", "Data", "2020–2025; hotel nights July 2024–2025", "Exported Jan. 20, 2025",
    "Sheets behind the study: the full-day calculation, incremental spending, day vs. overnight visitors by year, and a daily hotel and group room-night calendar.",
    ["Anaheim"], ["p-night", "p-hotel"], "Working-sheet names made neutral for publishing; values unchanged.", scrub=True, rename_sheets=True)

# ---- Who visits ----
add("az-d5", "azira-district-5-poi-analysis-2026-01-05.pdf", "POI Analysis.pdf", "visitors",
    "District 5 visitor profile (POI Analysis)", "Symphony | Tourism Economics (Azira)", "Data report", "Jan. 1–May 31, 2026", "Exported 2026",
    "District 5, where OC Vibe is being built: 85.8% overnight, 43.8% new visitors, sample 1,003,735 devices; origin states and metros, cross-visited places, visits by day, household income and age.",
    ["District 5"], ["p-d5", "p-ocv"])
add("az-geo", "azira-domestic-visitors-2026-08.pdf", "Domestic Visitors by Geography.pdf", "visitors",
    "Domestic visitors to Anaheim and Garden Grove", "Symphony | Tourism Economics (Azira)", "Data report", "Aug. 2026", "Exported 2026",
    "1.3-day average stay, 81.7% overnight, 82.5% repeat; 74.0% of trips start within 50 miles; origin states and metros; places visited.",
    ["Anaheim", "Garden Grove"], ["p-d5", "p-transport"])
add("visa-type", "visa-visitor-type-2026-08.pdf", "Visitor Type.pdf", "visitors",
    "Visitor card spending by visitor type", "Visa Destination Insights via Symphony | Tourism Economics", "Data report", "Aug. 2026 vs. Aug. 2025", "Exported Oct. 12, 2026",
    "Visitor card spending $464.6M (+8.1%), 5.4M cards, $85 per card; spending by home metro.", ["Anaheim area", "U.S."], ["p-spend", "p-d5"])
add("visa-intl", "visa-international-2026-08.pdf", "International.pdf", "visitors",
    "International card activity", "Visa Destination Insights via Symphony | Tourism Economics", "Data report", "Aug. 2026 vs. Aug. 2025", "Exported Oct. 12, 2026",
    "International card spending $17.9M (−5.0%) by category and country (Mexico, Canada, Japan lead).", ["Anaheim area", "International"], ["p-d5", "p-spend"])
add("datafy-25", "datafy-anaheim-tables-export-2025.xlsx", "Datafy Tables Export_2_17_26.xlsx", "visitors",
    "Datafy tables export, Anaheim, calendar 2025", "Datafy", "Data", "Jan. 1–Dec. 31, 2025 (trends 2023–2025)", "Exported Feb. 17, 2026",
    "Domestic visitation by month and day, origin states, DMAs, metros, counties and cities, demographics, points of interest and clusters (including OC Vibe and District 5), length of stay and repeat visits.",
    ["Anaheim", "District 5"], ["p-d5"], "Calendar 2025 export. The report's 5.2% OC Vibe share comes from Datafy's calendar 2024 visitor report (visitors traveling 50+ miles); 2025 values will be reconciled at the next quarterly update.")

# ---- Marketing ----
add("az-media", "azira-media-attribution-2026-01-08.pdf", "Media Attribution.pdf", "media",
    "Media attribution summary", "Symphony | Tourism Economics (Azira attribution feed)", "Data report", "Exposures Jan. 1–Aug. 31, 2026", "Exported 2026",
    "31.0M measurable impressions, 368,416 observed visits (11.9 per 1,000 impressions), 39 days from exposure to visit; results by campaign, vendor and metro.",
    ["U.S. audiences", "Anaheim"], ["p-media"])

# ---- Hotels ----
add("cs-mkt", "costar-orange-county-hospitality-market-2026-10-12.pdf", "Orange County - CA USA-Hospitality-Market-2026-10-12.pdf", "hotels",
    "Orange County hospitality market report", "CoStar Group", "Report", "12 months and YTD through Aug. 2026", "Pulled Oct. 12, 2026",
    "Countywide hotel performance (74.0% occupancy, $218 ADR), submarkets, construction (668 rooms), economy (Oxford Economics).",
    ["Orange County", "U.S."], ["p-hotel"])
add("cs-dl", "costar-disneyland-hospitality-submarket-2026-10-12.pdf", "Disneyland-Hospitality-Submarket-2026-10-12.pdf", "hotels",
    "Disneyland hospitality submarket report", "CoStar Group", "Report", "12 months and YTD through Aug. 2026", "Pulled Oct. 12, 2026",
    "Resort-area hotels: 78.4% occupancy, $255 ADR, RevPAR $199.78 (+7.9%); history since 2019, pipeline and sales.",
    ["Disneyland submarket"], ["p-hotel"])
add("cs-cap", "costar-orange-county-hospitality-capital-markets-2026-10-12.pdf", "Orange County - CA USA-Hospitality-Capital Market-2026-10-12.pdf", "hotels",
    "Orange County hospitality capital markets report", "CoStar Group", "Report", "Through Aug. 2026", "Pulled Oct. 12, 2026",
    "Hotel sales ($234.2M over 12 months), prices per room, cap rates.", ["Orange County"], ["p-hotel"])
add("cs-exp", "costar-submarket-export-2026-01-08.xlsx", "DataExport (17).xlsx", "hotels",
    "CoStar submarket export, monthly", "CoStar Group", "Data", "Monthly Jan.–Aug. 2026", "Processed Aug. 31, 2026",
    "Monthly occupancy, ADR and RevPAR for the Anaheim, Disneyland, Newport Beach/Dana Point, Santa Ana/Costa Mesa and Northwest/Fullerton submarkets.",
    ["Orange County submarkets"], ["p-hotel"])
add("str-daily", "str-daily-hotel-data-2026-01-10.xlsx", "Daily Data (8).xlsx", "hotels",
    "STR daily hotel data, Visit Anaheim hotel sets", "STR (CoStar Group)", "Data", "Jan. 1–Oct. 3, 2026, daily", "Provided Oct. 12, 2026",
    "Daily supply, demand, revenue, occupancy and rates by segment for Anaheim+, Anaheim-Garden Grove+ and Garden Grove+.",
    ["Anaheim", "Garden Grove"], ["p-hotel", "p-night"])
for q, per, pub, f in [("1Q", "Forecast to 2030", "1Q 2026", "Visit Anaheim Forecasts Combined for Distro 1Q-26.xlsx"),
                       ("2Q", "Forecast to 2030", "2Q 2026", "Visit Anaheim Forecasts Combined For Distro 2Q-26.xlsx"),
                       ("3Q", "Forecast to 2030", "3Q 2026", "Visit Anaheim Forecasts Combined For Distro 3Q-26.xlsx")]:
    add(f"larc-set-{q.lower()}", f"larc-forecasts-combined-{q.lower()}26.xlsx", f, "hotels",
        f"Hotel forecasts combined, {q} 2026 edition", "Lodging Analytics Research & Consulting (LARC)", "Data", per, pub,
        "Occupancy, ADR and RevPAR forecasts for the Visit Anaheim (Anaheim and Garden Grove) hotel sets and the market.",
        ["Anaheim", "Garden Grove"], ["p-hotel", "p-larc"])

# ---- Market outlook ----
for mo, mon, f in [("01", "Jan.", "01 January 2026 Market Intelligence Report.pdf"), ("04", "Apr.", "04 April 2026 Market Intelligence Report.pdf"),
                   ("06", "June", "06 June 2026 Market Intelligence Report.pdf"), ("07", "July", "07 July 2026 Market Intelligence Report.pdf"),
                   ("09", "Sept.", "09 September 2026 Market Intelligence Report.pdf")]:
    add(f"larc-mir-{mo}", f"larc-market-intelligence-report-2026-{mo}.pdf", f, "outlook",
        f"Anaheim Market Intelligence Report, {mon} 2026", "Lodging Analytics Research & Consulting (LARC)", "Report", f"Data to {mon} 2026 edition", f"{mon} 2026",
        "Hotel performance and forecasts, Anaheim vs. U.S., Convention Center pace, OC Vibe and area developments, local economy and inflation.",
        ["Anaheim", "U.S."], ["p-larc", "p-hotel"])

# ---- Getting here ----
add("octa-adt", "octa-traffic-flow-map-2026.pdf", "2026-ADT.pdf", "transport",
    "2026 Traffic Flow Map", "Orange County Transportation Authority (OCTA)", "Map", "Counts 2021–2024", "Aug. 2026",
    "Weekday average daily traffic on freeways and arterials, including SR-57 beside OC Vibe (275,000 vehicles).", ["Orange County"], ["p-transport"])
add("octa-gtfs", "octa-bus-schedules-gtfs.zip", "google_transit.zip", "transport",
    "OCTA bus schedules (GTFS feed)", "Orange County Transportation Authority (OCTA)", "Data", "Service Aug. 9–Nov. 7, 2026", "Provided Oct. 12, 2026",
    "The raw schedule files used to count 277 weekday bus trips stopping at ARTIC, late-night service and travel times.", ["Orange County"], ["p-transport"])
add("rpa-ana", "amtrak-anaheim-ana-station-fact-sheet.pdf", "ana.pdf", "transport",
    "Amtrak service in Anaheim, CA (ANA)", "Rail Passengers Association", "Fact sheet", "2018–2024", "Oct. 27, 2025",
    "Amtrak passengers at ARTIC by year (191,153 in 2024), trip length, fare and top city pairs.", ["Anaheim"], ["p-transport"])
add("metrolink", "metrolink-fact-sheet-fy26-q2.pdf", "fact_sheet_q2-fy26.pdf", "transport",
    "Metrolink fact sheet, FY2025-26 Q2", "Metrolink (SCRRA)", "Fact sheet", "Oct.–Dec. 2025", "FY2025-26 Q2",
    "Ridership by line, including the Orange County Line (5,116 weekday riders), and rider profile.", ["Southern California"], ["p-transport"])
add("bts-county", "bts-orange-county-transportation-profile.pdf", "Dashboard.pdf", "transport",
    "County Transportation Profile: Orange County, CA", "U.S. Bureau of Transportation Statistics", "Profile", "American Community Survey (year not stated)", "Provided Oct. 12, 2026",
    "Commute mode, households without a vehicle, transportation facilities, population and jobs.", ["Orange County", "U.S."], ["p-transport"])
add("bts-county-x", "bts-orange-county-demographics-and-economy.xlsx", "Demographics and the Economy.xlsx", "transport",
    "County Transportation Profile data: demographics and the economy", "U.S. Bureau of Transportation Statistics", "Data", "As in the profile", "Provided Oct. 12, 2026",
    "Population 3,165,820; workers 1,565,842; businesses; jobs; households without a vehicle.", ["Orange County"], ["p-transport"])
add("bts-tet", "bts-transportation-economic-trends-metadata.xlsx", "TET_Online_MetaData_All.xlsx", "transport",
    "Transportation Economic Trends: table guide", "U.S. Bureau of Transportation Statistics", "Data guide", "All TET tables", "Accessed Oct. 12, 2026",
    "Guide to the national tables used for gas prices (3.1), airfares (3.4) and per-mile car costs (6.6).", ["U.S."], ["p-transport"])
for i, (f, what) in enumerate([("California’s transit systems Data Snapshot.csv", "Operating statistics by operator"),
                               ("California’s transit systems Data Snapshot (1).csv", "Financial data by operator"),
                               ("California’s transit systems Data Snapshot (2).csv", "Financial data by operator (second view)"),
                               ("California’s transit systems Data Snapshot (3).csv", "Financial data by type"),
                               ("California’s transit systems Data Snapshot (5).csv", "Total passengers by mode"),
                               ("California’s transit systems Data Snapshot (6).csv", "Operating statistics by operator (second view)"),
                               ("California’s transit systems Data Snapshot (7).csv", "Operating statistics by operator (third view)")], 1):
    add(f"ca-transit-{i}", f"california-transit-snapshot-orange-{i}.csv", f, "transport",
        f"California's transit systems, Orange County: {what.lower()}", "California's transit systems (state data snapshots)", "Data", "2003–2017", "Downloaded Oct. 12, 2026",
        "Orange County transit staff, expenses, revenues, passengers and vehicles, 2003–2017 (nominal dollars).", ["Orange County"], ["p-transport"],
        "A duplicate copy received on Oct. 12, 2026 is not repeated here.")

# ---- Destination program ----
add("va-poe", "visit-anaheim-program-of-experiences-2027.pdf", "Visit-Anaheim-Program-of-Experiences-2027 (2).pdf", "program",
    "Program of Experiences, 2027", "Visit Anaheim", "Program", "2027", "2026",
    "Visit Anaheim's 2027 program of experiences.", ["Anaheim"], ["p-larc"])

# ---- This report (built by the pipeline; no `orig`) ----
add("ocv-report", "OC_Vibe_Insights.pdf", None, "report", "OC Vibe Insights, full report (PDF)", "Visit Anaheim Business Intelligence",
    "Report", "Data through Sept. 2026", "Updated quarterly", "Every section of this app as report pages.", ["Anaheim", "Orange County", "California", "U.S."], ["p-summary"])
add("ocv-deck", "OC_Vibe_Insights.pptx", None, "report", "OC Vibe Insights, full deck (PowerPoint)", "Visit Anaheim Business Intelligence",
    "Deck", "Data through Sept. 2026", "Updated quarterly", "The same report as editable slides.", ["Anaheim", "Orange County", "California", "U.S."], ["p-summary"])
add("ocv-qa", "OC_Vibe_Questions_Answered.pptx", None, "report", "Questions answered: Anaheim, Orange County and U.S. (PowerPoint)", "Visit Anaheim Business Intelligence",
    "Deck", "Data through Sept. 2026", "Oct. 14, 2026", "Average spend, one more night, transportation impact and District 5, each with a summary, visual and method.",
    ["Anaheim", "Orange County", "California", "U.S."], ["p-ask"])

FILES = F

# Public sources used but not hosted here: link out (accessed dates as noted)
LINKS = [
    ("Visit California: The Economic Impact of Travel in California, 2025p (Dean Runyan Associates, Apr. 6, 2026)", "https://www.visitvisalia.com//caeconomicimpactreport_2025-low-res.pdf",
     "California and Orange County travel spending, jobs and taxes; statewide spending on local transportation, gas and visitor air. Accessed Oct. 14, 2026."),
    ("U.S. Travel Association and Tourism Economics: Travel Forecast, Spring 2026", "https://www.ustravel.org/sites/default/files/2026-05/US_Travel-Forecast_Spring26.pdf",
     "U.S. travel spending ($1.360T in 2025) and trips (2.46B), real 2025 dollars. Accessed Oct. 14, 2026."),
    ("U.S. Travel Association: Economic Impact of the U.S. Travel Industry (2025 data)", "https://www.ustravel.org/sites/default/files/media_root/economic-impact/pdf/DCH26_EconImp_National_FIN.pdf",
     "U.S. jobs supported (15M+), economic output ($3.0T) and state and local taxes ($92B). Accessed Oct. 14, 2026."),
    ("Visit California 2025 report summary (Rural County Representatives of California, May 15, 2026)", "https://www.rcrcnet.org/general/visit-california-releases-2025-economic-impact-report-a-story-of-resilience/",
     "Secondary summary of the statewide 2025 results."),
    ("U.S. Bureau of Transportation Statistics: Transportation Economic Trends data", "https://data.bts.gov/resource/tcq5-4pgu.json",
     "Gas prices, airfares and car costs, 2019–2025 (Tables 3.1, 3.4, 6.6). Accessed Oct. 12, 2026."),
    ("U.S. Bureau of Economic Analysis: Travel and Tourism Satellite Account, 2018–2023", "https://apps.bea.gov/scb/issues/2025/02-february/0225-travel-tourism-satellite-account.htm",
     "National tourism output ($1.52T direct, 2023) and 6.5M direct tourism jobs. Accessed Oct. 14, 2026."),
]


def finalize(ask_items=()):
    """Add file sizes and page counts, and which questions each file answers."""
    import subprocess, re
    for f in FILES:
        p = os.path.join(LIB_DIR, f['file'])
        if f['topic'] == 'report':
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), f['file'])
        f['ext'] = f['file'].rsplit('.', 1)[-1].upper()
        f['bytes'] = os.path.getsize(p) if os.path.exists(p) else None
        f['pages'] = None
        if f['ext'] == 'PDF' and os.path.exists(p):
            try:
                out = subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout
                m = re.search(r'Pages:\s+(\d+)', out); f['pages'] = int(m.group(1)) if m else None
            except Exception:
                pass
        f['answers'] = [q['id'] for q in ask_items if f['id'] in q.get('files', [])]
    return FILES
