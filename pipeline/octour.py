"""Orange County tourism statistics (added Oct. 19, 2026, per John Picou).

Answers the five questions Entertainment + Culture Advisors (ECA) sent for OCVIBE on Oct. 19, 2026:
  1. Visitor arrivals to Orange County, 2019-2025 and 2026 year to date (domestic/international; overnight/day)
  2. Origin markets, including the Los Angeles-Long Beach-Anaheim split of Anaheim vs. outside Anaheim
  3. Monthly visitation patterns and seasonality
  4. Visitor profiles: trip purpose, length of stay, party size, travel with children
  5. Hotel inventory, occupancy and average daily rate (ADR)
Facts only: every value is published by the named source or is arithmetic on published values (shown).
Different sources use different methods; they are shown side by side, never blended into one series.
prep() runs before ask.attach (library entries and questions); attach() runs after it (the section).
"""
import library as L
import ask as K

ASOF = "Oct. 19, 2026"
S_CIC = "CIC Research, Annual Profile of Visitors to Anaheim and Orange County, 2019 (for Visit Anaheim, Apr. 2020)"
S_TEOC = "Tourism Economics, Economic Impact of Visitors to Orange County, 2025 (pub. May 2026)"
S_TEFC = "Tourism Economics, Anaheim and Garden Grove Travel Forecast (Sept. 2026)"
S_DR = "Dean Runyan Associates for Visit California, The Economic Impact of Travel in California, 2025p (Apr. 2026), Orange County detail"
S_CS = "CoStar, Orange County hotel market (monthly data through Sept. 2026; market report Oct. 12, 2026)"
S_CSSEG = "CoStar, Orange County hotel segmentation (12 months to Aug. 2026)"
S_AZ = "Symphony | Tourism Economics (Azira), Anaheim and Garden Grove, Jan. 1, 2023-Aug. 31, 2026 (pulled Oct. 19, 2026)"
S_VCFC = "Tourism Economics for Visit California, California Travel Forecast data (Sept. 2026)"
S_LF = "Tourism Economics for Visit California, State and Regional Lodging Forecast (Sept. 2026; CoStar data)"
S_MTI = "Visit California, Monthly Travel Indicators, Aug. 2026 (pub. Oct. 8, 2026)"

# ---------- Q1. Visitor volume (millions) ----------
CIC_VOL = {2009: (24.7, 18.0, 42.7), 2010: (24.1, 18.7, 42.7), 2011: (24.0, 18.9, 42.9), 2012: (24.4, 19.4, 43.8), 2013: (24.7, 19.7, 44.4),
           2014: (25.8, 20.4, 46.1), 2015: (26.3, 21.1, 47.4), 2016: (26.8, 21.4, 48.2), 2017: (27.9, 21.4, 49.4), 2018: (28.7, 21.5, 50.2),
           2019: (28.73, 21.48, 50.21)}          # (day, overnight, total), CIC Figure 1 and Table 3
TE_VOL = {2021: (22.7, 16.3, 39.0), 2022: (26.8, 21.1, 47.8), 2023: (28.0, 21.6, 49.6), 2024: (28.8, 21.9, 50.7), 2025: (29.2, 22.1, 51.3)}
TE_INTL25 = (47.9, 3.5)                          # domestic, international, millions, 2025
CIC_INTL19 = 9.1                                 # % of visitors, 2019 (4.6M)
DR_SP = {2019: 12673.3, 2020: 5919.6, 2021: 9572.1, 2022: 13425.7, 2023: 14174.1, 2024: 14899.1, 2025: 15394.2}
DR_DAY = {2019: 1974.9, 2020: 599.8, 2021: 1075.6, 2022: 1645.7, 2023: 1714.4, 2024: 1802.6, 2025: 1861.7}
ANA_H1 = dict(y25=(6.12, 6.55), y26=(6.32, 6.74))   # Anaheim visitors, Q1 and Q2, millions (Tourism Economics, Sept. 2026)
h1_25, h1_26 = sum(ANA_H1['y25']), sum(ANA_H1['y26'])
h1_chg = (h1_26 / h1_25 - 1) * 100
te_chg = (TE_VOL[2025][2] / TE_VOL[2021][2] - 1) * 100
dr_vs19 = (DR_SP[2025] / DR_SP[2019] - 1) * 100
dr_20 = DR_SP[2020] / DR_SP[2019] * 100

# ---------- Q2. Origins ----------
CIC_ORIG = [("Southern California (all)", "55.4%"), ("Los Angeles metro", "26%"), ("Riverside/San Bernardino", "19%"), ("San Diego", "6%"),
            ("San Francisco", "3%"), ("Phoenix", "Slightly under 3%"), ("Northern California", "8%"), ("Other western states", "15%"),
            ("Rest of the U.S.", "Almost 13%"), ("International", "9.1% (4.6M)")]
AZ_MSA = [("Los Angeles-Long Beach-Anaheim (includes Orange County)", 44.7), ("Riverside-San Bernardino-Ontario", 26.1), ("San Diego-Chula Vista-Carlsbad", 4.1),
          ("Phoenix", 2.3), ("Las Vegas", 1.9), ("San Francisco-Oakland", 1.3)]
AZ_DMA = [("Los Angeles", 55.6), ("Palm Springs", 16.3), ("San Diego", 4.1), ("Phoenix", 3.0)]
TE_INTL_MKT = [("Mexico", 766), ("Canada", 254), ("United Kingdom", 123), ("Australia", 104), ("New Zealand", 27), ("Rest of world", 865)]

# ---------- Q3. Seasonality: CoStar monthly occupancy (%) and ADR ($), Orange County ----------
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
OCC = {2019: [67.7, 75.6, 82.0, 77.7, 74.6, 81.2, 86.2, 80.9, 75.3, 81.4, 74.1, 72.1],
       2020: [70.7, 77.8, 34.8, 22.0, 30.9, 36.9, 40.4, 44.3, 45.8, 45.0, 35.8, 32.0],
       2021: [33.0, 37.7, 44.3, 46.7, 51.8, 62.7, 75.6, 63.6, 62.3, 67.1, 62.1, 66.4],
       2022: [51.1, 63.4, 71.7, 73.1, 69.2, 77.2, 80.2, 70.4, 75.8, 77.3, 67.4, 65.9],
       2023: [58.4, 69.1, 74.8, 73.7, 71.1, 76.2, 80.7, 70.7, 73.7, 74.6, 68.2, 68.3],
       2024: [61.7, 68.2, 72.1, 70.0, 68.7, 77.0, 80.0, 73.6, 77.2, 73.8, 70.0, 68.0],
       2025: [63.6, 69.8, 74.9, 70.9, 70.6, 75.9, 81.2, 74.9, 69.9, 76.9, 69.3, 70.4],
       2026: [65.5, 75.1, 78.5, 75.1, 72.0, 77.8, 82.6, 75.5, 75.5]}
ADR = {2019: [154, 157, 169, 159, 156, 170, 189, 179, 157, 168, 159, 159],
       2020: [160, 163, 143, 87, 101, 123, 135, 135, 132, 128, 115, 103],
       2021: [99, 110, 118, 132, 147, 174, 210, 197, 180, 185, 177, 186],
       2022: [160, 177, 200, 201, 199, 220, 236, 216, 207, 211, 199, 178],
       2023: [183, 201, 216, 208, 205, 216, 235, 215, 210, 218, 208, 207],
       2024: [195, 200, 215, 202, 197, 211, 224, 213, 215, 211, 200, 203],
       2025: [192, 201, 214, 198, 197, 210, 233, 215, 208, 225, 202, 208],
       2026: [196, 211, 231, 215, 211, 228, 246, 225, 223]}
AVG3 = [round(sum(OCC[y][i] for y in (2023, 2024, 2025)) / 3, 1) for i in range(12)]
AVG3_ALL = round(sum(AVG3) / 12, 1)
PEAK_I, LOW_I = AVG3.index(max(AVG3)), AVG3.index(min(AVG3))
ADR3 = [round(sum(ADR[y][i] for y in (2023, 2024, 2025)) / 3) for i in range(12)]

# ---------- Q5. Hotel market, CoStar ----------
HOT = [(2019, 58633, 59172, 77.4, 165.36), (2020, 50674, 60580, 44.0, 135.76), (2021, 56940, 61354, 57.1, 169.58), (2022, 59997, 60858, 70.2, 202.31),
       (2023, 60005, 60689, 71.6, 211.11), (2024, 60353, 60932, 71.7, 207.75), (2025, 60547, 60550, 72.3, 209.68), ("2026 YTD", 60219, 60224, 75.2, 221.67)]
def revpar(o, a): return o / 100 * a
H25, H26, H19 = HOT[6], HOT[7], HOT[0]
SEG = dict(transient=59.5, group=13.3, contract=1.2, total=74.0)

# ---------- Q4. Visitor profile, Orange County 2019 (CIC Table 3): hotel, private home, all overnight, day, all ----------
CIC_T3 = [
    ("Purpose: pleasure or visiting friends and relatives", "63.6%", "94.7%", "76.4%", "84.8%", "81.2%"),
    ("Purpose: business or convention", "29.0%", "3.5%", "18.5%", "2.8%", "9.6%"),
    ("Purpose: special events", "6.1%", "0.2%", "3.8%", "10.5%", "7.6%"),
    ("Mean travel party size (people)", "2.6", "2.4", "2.6", "2.9", "2.8"),
    ("Children in the travel group", "28.7%", "35.9%", "31.8%", "41.5%", "37.0%"),
    ("Mean nights stayed in Orange County", "3.8", "4.7", "4.2", "0", "1.8"),
    ("Median age of visitors (years)", "41", "38", "41", "30", "34"),
    ("Arrived by air", "51.0%", "50.3%", "50.5%", "7.6%", "24.8%"),
    ("Spending per visitor in Orange County", "$670", "$303", "$555", "$54", "$268"),
    ("Median household income", "$121,900", "$83,900", "$110,100", "$78,100", "$89,500"),
    ("Southern California resident", "12.5%", "17.3%", "13.8%", "84.7%", "55.4%"),
    ("International visitor", "22.4%", "9.9%", "18.5%", "4.1%", "9.1%"),
    ("First-time visitor", "17.7%", "12.5%", "16.1%", "5.3%", "9.9%"),
    ("Visitor volume", "12.40M", "7.12M", "21.48M", "28.73M", "50.21M"),
]

Q_TEXT = [
    ("1. Visitor arrivals", "How many visitors came to Orange County each year from 2019 to 2025, and so far in 2026, split by domestic and international and by overnight and day?"),
    ("2. Origin markets", "Where do visitors come from, and can the Los Angeles-Long Beach-Anaheim area be split into Anaheim and outside Anaheim?"),
    ("3. Seasonality", "How does visitation change month by month?"),
    ("4. Visitor profile", "What is the purpose of the trip, how long do visitors stay, how large is the travel party and how many travel with children?"),
    ("5. Hotels", "How many hotel rooms does Orange County have, and what are occupancy and average daily rate?"),
]


def prep():
    """Library topic, library files and the five questions. Runs before ask.attach (which finalizes the library)."""
    if not any(t[0] == "octour" for t in L.TOPICS):
        L.TOPICS.insert(1, ("octour", "Orange County tourism statistics", "Visitor volume, origins, seasonality, visitor profile and hotel data for Orange County (assembled Oct. 19, 2026)."))
    U = ["p-octour"]
    L.add("cic-profile-2019", "cic-visitor-profile-2019-anaheim-orange-county.pdf", "2019 Anaheim and OC Visitor Profile Report 04-10-2020.pdf", "octour",
          "Annual Profile of Visitors to Anaheim and Orange County, 2019", "CIC Research for Visit Anaheim", "Report", "Calendar 2019; visitor volume 2009-2019", "Apr. 2020",
          "50.21M Orange County visitors in 2019 (28.73M day, 21.48M overnight), $13.48B spending; trip purpose, party size, children, length of stay, origins, income and transportation by type of stay; Anaheim profile (24.16M visitors).",
          ["Anaheim", "Orange County"], U, "Latest edition found (SharePoint search, Oct. 19, 2026). Survey: 2,686 intercepts at 36 Orange County locations plus a panel of 2,087 households. Added to the public library Oct. 19, 2026 with Visit Anaheim BI approval.")
    L.add("vca-ei-2025p", "visit-california-economic-impact-of-travel-2025p.pdf", "CAEconomicImpactReport_2025 rev.pdf", "octour",
          "The Economic Impact of Travel in California, 2025p", "Dean Runyan Associates for Visit California", "Report", "2015-2025p", "Apr. 2026",
          "Statewide and county travel spending, jobs, earnings and taxes. Orange County: $15.39B visitor spending (2025p; 2019 $12.67B; 2020 $5.92B), 134,540 jobs, $1.41B local and state taxes.",
          ["California", "Orange County"], U, "Preliminary (2025p). Different method from Tourism Economics; do not mix the two series.")
    L.add("vca-ad-2025p", "visit-california-travel-impacts-by-assembly-district-2025p.pdf", "CA_Assembly_Districts_2025.pdf", "octour",
          "California Travel Impacts by Assembly District, 2025p", "Dean Runyan Associates for Visit California", "Report", "2019-2025p", "Apr. 2026",
          "Travel spending, jobs and taxes by Assembly District. District 68 (Santa Ana, Orange, Anaheim): $2.10B visitor spending in 2025p (2019: $1.70B), 16,800 jobs.",
          ["California", "Orange County"], U, "Preliminary (2025p).")
    L.add("vca-fc-data", "visit-california-travel-forecast-data-2026-09.xlsx", "CATravelForecast_Sept2026_data.xlsx", "octour",
          "California Travel Forecast data, Sept. 2026", "Tourism Economics for Visit California", "Data", "2019-2030 (forecast from 2026)", "Sept. 2026",
          "Statewide visits and spending: domestic and international, business and leisure. 2025: 271.4M visits (255.0M domestic, 16.4M international).",
          ["California"], U)
    L.add("vca-lodging-fc", "visit-california-state-regional-lodging-forecast-2026-09.xlsx", "State and Regional Lodging Forecast -Sept 2026.xlsx", "octour",
          "State and Regional Lodging Forecast, Sept. 2026", "Tourism Economics for Visit California (CoStar data)", "Data", "2013-2029 (forecast from 2026)", "Sept. 2026",
          "Hotel supply, demand, occupancy, ADR and RevPAR for California and 15 regions, including Orange County (2025 occupancy 72.8%, ADR $210.33; 2026 forecast 75.9%, $221.61).",
          ["California", "Orange County"], U)
    L.add("vca-mti-2026-08", "visit-california-monthly-travel-indicators-2026-08.pdf", "Monthly Travel Indicators_August 2026.pdf", "octour",
          "Monthly Travel Indicators, Aug. 2026", "Visit California", "Report", "Aug. 2026", "Oct. 8, 2026",
          "Statewide forecasts, traveler sentiment and travel intent (domestic and 13 international markets), lodging, airlift and international arrivals.",
          ["California", "U.S."], U, "No Orange County visitor profile, party size or travel with children.")
    L.add("vca-sentiment-2025", "visit-california-resident-sentiment-2025.xlsx", "California Resident Sentiment 2025  4.xlsx", "octour",
          "California Resident Sentiment on Travel and Tourism, 2022-2025", "Visit California (Omnitrak)", "Data", "2022-2025 survey waves", "Mar. 24, 2026",
          "Residents' views of tourism for the U.S., California, Orange County and Anaheim. Orange County 2025: 57.0% hold a high opinion of tourism in their area; 60.8% rate job creation high.",
          ["Anaheim", "Orange County", "California", "U.S."], U, "Survey of residents, not visitors. Anaheim samples are small (about 165-180 per question).")
    for i, f, o, t, s in [
        ("az-los", "azira-length-of-stay-trend-2023-2026.xlsx", "LOS Trend.xlsx", "Azira length of stay trend, Anaheim and Garden Grove", "Average length of stay by month (domestic visitors), Jan. 2023-Aug. 2026."),
        ("az-dist", "azira-distance-share-trend-2023-2026.xlsx", "Distance Share Trend.xlsx", "Azira distance share trend, Anaheim and Garden Grove", "Share of trips by distance traveled, by month, Jan. 2023-Aug. 2026."),
        ("az-msa", "azira-origin-share-by-msa-2023-2026.xlsx", "1-Share by MSA (1).xlsx", "Azira origin share by metro area (MSA), Anaheim and Garden Grove", "Share of domestic trips by home metro area; Los Angeles-Long Beach-Anaheim 44.7%."),
        ("az-dma", "azira-origin-share-by-dma-2023-2026.xlsx", "1-Share by MSA (2).xlsx", "Azira origin share by TV market (DMA), Anaheim and Garden Grove", "Share of domestic trips by home TV market; Los Angeles 55.6%, Palm Springs 16.3%."),
        ("az-intl-los", "azira-international-length-of-stay-2023-2026.xlsx", "2- INT Avg Length of Stay.xlsx", "Azira international average length of stay, Anaheim and Garden Grove", "International visitors' average length of stay: 4.99 days.")]:
        L.add(i, f, o, "octour", t, "Symphony | Tourism Economics (Azira)", "Data", "Jan. 1, 2023-Aug. 31, 2026", "Pulled Oct. 2026", s, ["Anaheim", "Garden Grove"], U,
              "Study geography is Anaheim and Garden Grove, not Orange County. No ZIP codes.")

    T = "Orange County tourism statistics"
    K.q(id="oc-arrivals", topic=T, q="How many visitors come to Orange County, and how many stay overnight?",
        a=f"Orange County drew {TE_VOL[2025][2]}M visitors in 2025: {TE_VOL[2025][0]}M day and {TE_VOL[2025][1]}M overnight; {TE_INTL25[0]}M domestic and {TE_INTL25[1]}M international (Tourism Economics). CIC Research counted {CIC_VOL[2019][2]}M in 2019 with a different method. No 2026 year-to-date count is published for the county; Anaheim drew {h1_26:.1f}M in Jan.-June 2026, +{h1_chg:.1f}%.",
        key=f"{TE_VOL[2025][2]}M", key_l="Orange County visitors, 2025",
        geo=[["Orange County, 2025", f"{TE_VOL[2025][2]}M", f"Day {TE_VOL[2025][0]}M + overnight {TE_VOL[2025][1]}M; domestic {TE_INTL25[0]}M (93.3%), international {TE_INTL25[1]}M (6.7%)", S_TEOC],
             ["Orange County, 2019", f"{CIC_VOL[2019][2]}M", f"Day {CIC_VOL[2019][0]}M + overnight {CIC_VOL[2019][1]}M; international 9.1% (4.6M)", S_CIC],
             ["Orange County, 2020", "Not published", f"Visitor spending fell to ${DR_SP[2020]/1000:.2f}B, {dr_20:.1f}% of 2019 ({S_DR.split(',')[0]})", S_DR],
             ["Anaheim, Jan.-June 2026", f"{h1_26:.2f}M", f"Q1 {ANA_H1['y26'][0]}M + Q2 {ANA_H1['y26'][1]}M vs. {h1_25:.2f}M in Jan.-June 2025 (+{h1_chg:.1f}%)", S_TEFC],
             ["California, 2025", "271.4M visits", "255.0M domestic, 16.4M international (2019: 285.6M)", S_VCFC]],
        viz=dict(kind="bars", title="Orange County visitors, millions", rows=[
            dict(l="2019 (CIC)", v=CIC_VOL[2019][2], t=f"{CIC_VOL[2019][2]}M"), dict(l="2023 (TE)", v=TE_VOL[2023][2], t=f"{TE_VOL[2023][2]}M"),
            dict(l="2024 (TE)", v=TE_VOL[2024][2], t=f"{TE_VOL[2024][2]}M"), dict(l="2025 (TE)", v=TE_VOL[2025][2], t=f"{TE_VOL[2025][2]}M", hi=True)]),
        how="Tourism Economics counts visitors who stay overnight or travel more than 50 miles. CIC Research estimated 2019 volume from visitor intercept surveys, a household panel and hotel data. Day + overnight = total.",
        caveat="CIC (2009-2019) and Tourism Economics (2021-2025) use different methods; compare each series within itself. Tourism Economics has not published Orange County visitors for 2019-2020 or a 2026 year-to-date count; both are on the request list for Tourism Economics.",
        files=["te-ei-oc", "cic-profile-2019", "vca-ei-2025p", "te-fc-sep"], go="p-octour", links=[])
    K.q(id="oc-origins", topic=T, q="Where do Orange County visitors come from?",
        a="More than half (55.4%) of Orange County visitors in 2019 lived in Southern California: Los Angeles metro 26%, Riverside/San Bernardino 19% and San Diego 6%; 9.1% were international (CIC). Location data for Anaheim and Garden Grove (Jan. 2023-Aug. 2026) shows 44.7% of domestic trips from the Los Angeles-Long Beach-Anaheim metro area, which includes Orange County.",
        key="55.4%", key_l="of Orange County visitors from Southern California, 2019",
        geo=[["Orange County, 2019", "55.4% Southern California", "Los Angeles 26%, Riverside/San Bernardino 19%, San Diego 6%; international 9.1% (Mexico 848K, Canada 786K)", S_CIC],
             ["Anaheim and Garden Grove", "44.7% Los Angeles-Long Beach-Anaheim", "Riverside-San Bernardino-Ontario 26.1%, San Diego 4.1%, Phoenix 2.3% (share of domestic trips)", S_AZ],
             ["Anaheim and Garden Grove, international, 2025", "Mexico 766K", "Canada 254K, U.K. 123K, Australia 104K", "Tourism Economics, Travel Forecast (Sept. 2026)"]],
        viz=dict(kind="bars", title="Share of domestic trips by home metro area, Anaheim and Garden Grove", unit="%", rows=[
            dict(l=n.split(" (")[0], v=v, t=f"{v}%", hi=(i == 0)) for i, (n, v) in enumerate(AZ_MSA[:5])]),
        how="CIC: visitor survey, share of all visitors. Azira: mobile location data, share of domestic trips to Anaheim and Garden Grove by home metro area.",
        caveat="The Los Angeles-Long Beach-Anaheim metro area includes all of Orange County. Azira does not provide ZIP codes, so it cannot be split into Anaheim and outside Anaheim.",
        files=["cic-profile-2019", "az-msa", "az-dma", "te-fc-sep"], go="p-octour", links=[])
    K.q(id="oc-season", topic=T, q="When is Orange County busiest?",
        a=f"July. Orange County hotels averaged {AVG3[6]}% occupancy in July across 2023-2025 vs. {AVG3[0]}% in January, the low month (CoStar). In 2026, July reached {OCC[2026][6]}%. Monthly visitor counts are not published for the county, so hotel occupancy is the monthly measure.",
        key=f"{AVG3[6]}%", key_l="July hotel occupancy, 2023-2025 average",
        geo=[["Orange County hotels, July", f"{AVG3[6]}%", f"Average of 2023 {OCC[2023][6]}%, 2024 {OCC[2024][6]}%, 2025 {OCC[2025][6]}%", S_CS],
             ["Orange County hotels, January", f"{AVG3[0]}%", f"Average of 2023 {OCC[2023][0]}%, 2024 {OCC[2024][0]}%, 2025 {OCC[2025][0]}%", S_CS],
             ["Orange County hotels, June", f"{AVG3[5]}%", "Second-highest month", S_CS]],
        viz=dict(kind="bars", title="Orange County hotel occupancy by month, 2023-2025 average", unit="%", rows=[
            dict(l=MON[i], v=AVG3[i], t=f"{AVG3[i]}%", hi=(i == PEAK_I)) for i in range(12)]),
        how="Average of the three most recent full years: (2023 + 2024 + 2025) / 3 for each month.",
        caveat="Hotel occupancy measures overnight guests only; day visitors (57% of county visitors in 2025) are not in it.",
        files=["cs-mkt", "vca-lodging-fc"], go="p-octour", links=[])
    K.q(id="oc-profile", topic=T, q="Why do people visit Orange County, and who travels with them?",
        a="In 2019, 81.2% of Orange County visitors came for pleasure or to see friends and relatives, 9.6% for business or conventions and 7.6% for special events. The average travel party was 2.8 people, 37.0% had children with them, and overnight visitors stayed 4.2 nights (CIC). It is the latest county visitor profile.",
        key="37.0%", key_l="of Orange County visitors traveled with children, 2019",
        geo=[["Orange County, all visitors, 2019", "Party of 2.8", "37.0% with children; 81.2% pleasure or VFR; 1.8 nights average (day visitors count as 0)", S_CIC],
             ["Orange County hotel guests, 2019", "Party of 2.6", "28.7% with children; 29.0% business or convention; 3.8 nights", S_CIC],
             ["Anaheim, all visitors, 2019", "Party of 3.0", "42.0% with children; 78.3% pleasure or VFR; 9.7% special events", S_CIC],
             ["Anaheim and Garden Grove, 2026", "1.28-1.46 days", "Average length of stay by month, Jan.-Aug. 2026; international 4.99 days (2023-2026)", S_AZ]],
        viz=dict(kind="bars", title="Main purpose of trip, Orange County visitors, 2019", unit="%", rows=[
            dict(l="Pleasure or VFR", v=81.2, t="81.2%", hi=True), dict(l="Business or convention", v=9.6, t="9.6%"), dict(l="Special events", v=7.6, t="7.6%"), dict(l="Other", v=1.6, t="1.6%")]),
        how="CIC Research surveyed 4,040 visitor groups in 2019 (2,686 intercepts at 36 Orange County locations plus a panel of 2,087 households).",
        caveat="The 2019 profile predates the pandemic; no newer Orange County visitor survey was found (SharePoint and Visit California sources searched Oct. 19, 2026). A new survey would update purpose, party size and children.",
        files=["cic-profile-2019", "az-los", "az-intl-los", "vca-mti-2026-08"], go="p-octour", links=[])
    K.q(id="oc-hotels", topic=T, q="How many hotel rooms does Orange County have, and how full are they?",
        a=f"Orange County had {H26[2]:,} hotel rooms in Sept. 2026. Hotels filled {H26[3]}% of rooms at ${H26[4]:.2f} a night in Jan.-Aug. 2026, up from {H25[3]}% and ${H25[4]:.2f} in 2025 and {H19[3]}% and ${H19[4]:.2f} in 2019 (CoStar).",
        key=f"{H26[3]}%", key_l="Orange County hotel occupancy, Jan.-Aug. 2026",
        geo=[["Orange County, 2026 YTD", f"{H26[3]}% · ${H26[4]:.2f}", f"Revenue per available room ${revpar(H26[3], H26[4]):.2f} ({H26[3]}% x ${H26[4]:.2f})", S_CS],
             ["Orange County, 2025", f"{H25[3]}% · ${H25[4]:.2f}", f"{H25[1]:,} rooms available a night on average", S_CS],
             ["Orange County, 2019", f"{H19[3]}% · ${H19[4]:.2f}", f"{H19[1]:,} rooms available a night on average", S_CS],
             ["Orange County, 2026 forecast", "75.9% · $221.61", "Tourism Economics lodging forecast for Visit California (CoStar basis)", S_LF]],
        viz=dict(kind="bars", title="Orange County hotel occupancy", unit="%", rows=[
            dict(l=str(r[0]), v=r[3], t=f"{r[3]}%", hi=(r[0] == "2026 YTD")) for r in HOT]),
        how="Rooms available a night = annual available room nights / days in the year. Revenue per available room = occupancy x ADR.",
        caveat="CoStar data is licensed; summary figures are shared, raw exports are not.",
        files=["cs-mkt", "cs-dl", "vca-lodging-fc"], go="p-octour", links=[])
    if T not in K.QORDER:
        K.QORDER.insert(0, T)


def attach(SECTIONS, SOURCES, DQ, REGISTER, TAKEAWAYS, DATA_EXTRA):
    if any(s["id"] == "p-octour" for s in SECTIONS):
        return
    v25, v19 = TE_VOL[2025], CIC_VOL[2019]
    rp19, rp25, rp26 = revpar(H19[3], H19[4]), revpar(H25[3], H25[4]), revpar(H26[3], H26[4])
    adr_chg = (H26[4] / H19[4] - 1) * 100
    sec = dict(
        id="p-octour", tab="Orange County tourism",
        q="How many visitors come to Orange County, from where and when, who are they, and what hotel capacity serves them?",
        period="CIC Research 2009-2019; Tourism Economics 2021-2025; CoStar through Sept. 2026; Azira Jan. 2023-Aug. 2026",
        ans=f"Orange County drew {v25[2]}M visitors in 2025, {v25[0]}M for the day and {v25[1]}M overnight, and 93.3% came from within the U.S. (Tourism Economics). Most come for leisure: in 2019, 81.2% traveled for pleasure or to see friends and relatives, in parties of 2.8, and 37.0% brought children (CIC Research). Hotels filled {H26[3]}% of {H26[2]:,} rooms at ${H26[4]:.2f} in Jan.-Aug. 2026, with July the busiest month (CoStar).",
        ans_src=f"{S_TEOC}; {S_CIC}; {S_CS}",
        hv=f"{v25[2]}M", hl="Orange County visitors, 2025 (Tourism Economics)",
        head=f"Orange County draws {v25[2]} million visitors a year; hotels fill {H26[3]:.0f}% of rooms in 2026",
        dek="Five questions from Entertainment + Culture Advisors for OCVIBE, answered with dated sources: arrivals, origins, seasonality, visitor profile and hotels.",
        cards=[["Orange County, 2025", "Visitors", f"{v25[2]}M", f"{v25[0]}M day · {v25[1]}M overnight · 6.7% international", S_TEOC],
               ["Orange County, 2019 baseline", "Visitors (different method)", f"{v19[2]}M", f"{v19[0]}M day · {v19[1]}M overnight · 9.1% international", S_CIC],
               ["Orange County hotels, Jan.-Aug. 2026", "Occupancy", f"{H26[3]}%", f"ADR ${H26[4]:.2f} · {H26[2]:,} rooms (Sept. 2026)", S_CS],
               ["Orange County visitors, 2019", "Traveled with children", "37.0%", "Party of 2.8 · 81.2% pleasure or VFR", S_CIC]],
        card_calc=[None, None, f"Year to date Jan.-Aug. 2026; 2025 full year {H25[3]}%", None],
    )
    sec["notes"] = [
        "The five questions, as sent by Entertainment + Culture Advisors on Oct. 19, 2026: " + " ".join(f"({i + 1}) {t}" for i, (_, t) in enumerate(Q_TEXT)),
        f"Two visitor series exist and are kept apart: CIC Research for Visit Anaheim (2009-2019, survey-based) and Tourism Economics (2021-2025, model-based). CIC counted {v19[2]}M visitors in 2019; Tourism Economics counted {v25[2]}M in 2025. Neither publishes 2020 for the county; Dean Runyan Associates shows county visitor spending fell to {dr_20:.1f}% of its 2019 level that year.",
        "Origins can be shown at the metro-area level. The Los Angeles-Long Beach-Anaheim metro area includes all of Orange County, and Azira does not supply ZIP codes, so a split between Anaheim and the rest of the metro area is not available from current sources.",
        f"Monthly visitor counts are not published for Orange County. Hotel occupancy is the monthly measure: July averaged {AVG3[6]}% and January {AVG3[0]}% over 2023-2025 (CoStar).",
        "The most recent Orange County visitor profile is CIC Research's 2019 study; no newer county survey was found in Visit Anaheim's SharePoint or in Visit California's research (searched Oct. 19, 2026).",
    ]
    sec["ocv"] = [
        f"OC Vibe opens into a county of {v25[2]}M visitors, {v25[1]}M of them overnight (2025).",
        "Family travel is a core audience: 37.0% of county visitors and 42.0% of Anaheim visitors traveled with children in 2019.",
        f"Special events already draw 7.6% of county visitors and 10.5% of day visitors (2019), a base for arena and concert programming.",
        f"Hotel rooms are tightest in July ({AVG3[6]}%) and June ({AVG3[5]}%) and most open in January ({AVG3[0]}%), December ({AVG3[11]}%) and February ({AVG3[1]}%), CoStar 2023-2025 averages: event dates in the open months fill rooms that would otherwise sit empty.",
    ]
    sec["w5h"] = dict(
        who="Visitors to Orange County (staying overnight or traveling 50+ miles), the county's hotels, and ECA and OCVIBE as the requesters.",
        what=f"{v25[2]}M visitors in 2025 ({v25[0]}M day, {v25[1]}M overnight; 93.3% domestic); 55.4% from Southern California (2019); July peak; 81.2% leisure, party of 2.8, 37.0% with children (2019); {H26[2]:,} hotel rooms at {H26[3]}% occupancy and ${H26[4]:.2f} ADR (2026 YTD).",
        when="Visitors 2009-2019 (CIC) and 2021-2025 (Tourism Economics); hotels Jan. 2019-Sept. 2026 (CoStar); Azira Jan. 1, 2023-Aug. 31, 2026. Assembled Oct. 19, 2026.",
        where="Orange County; Anaheim where the county figure is not published; Anaheim and Garden Grove for Azira location data.",
        why="ECA's market study for OCVIBE needs a county baseline for audience size, origin, timing, visitor mix and lodging capacity.",
        how="Published figures from each source, kept as separate series; BI arithmetic shown for averages, revenue per available room and changes.",
        src=f"{S_TEOC}; {S_CIC}; {S_CS}; {S_AZ}")
    sec["cc"] = [
        dict(type="Growth", point=f"Orange County visitors rose from {TE_VOL[2021][2]}M (2021) to {v25[2]}M (2025), +{te_chg:.1f}%; visitor spending in 2025p was {dr_vs19:.1f}% above 2019.",
             solution=None, src=f"{S_TEOC}; {S_DR}"),
        dict(type="Opportunity", point=f"January ({AVG3[0]}%), December ({AVG3[11]}%) and February ({AVG3[1]}%) are the most open hotel months (2023-2025 averages).",
             solution="Schedule OC Vibe events that draw overnight guests in those months and share dates with Visit Anaheim for hotel packages.", src=S_CS),
        dict(type="Quick win", point="The 2019 CIC profile answers purpose, party size and children for both Orange County and Anaheim.",
             solution="Use it now as the labeled 2019 baseline in ECA's study; it is in the Reports and data library.", src=S_CIC),
        dict(type="Early hurdle", point="No Orange County visitor count is published for 2020 or 2026 year to date, and the two visitor series use different methods.",
             solution="Request 2019-2020 and 2026 county estimates from Tourism Economics; until they arrive, show Anaheim's Jan.-June 2026 count (+3.1%) and county hotel data as the current read.", src=f"{S_TEFC}; {S_CS}"),
        dict(type="Pitfall", point="The Los Angeles-Long Beach-Anaheim metro area includes Orange County, so its 44.7% share mixes local and Los Angeles County trips; Azira has no ZIP codes.",
             solution="Report metro-level shares with that note; a county or ZIP origin split would require a custom pull from Symphony or a new survey.", src=S_AZ),
        dict(type="Explanation", point="Azira length of stay and distance shares shifted in 2026 (trips under 50 miles rose to 73.9%-83.4% from 59%-66%).",
             solution="Treat 2026 Azira trends as a method change until Symphony confirms; compare within 2026 only.", src=S_AZ),
    ]
    sec["for_ocv"] = dict(
        enhance=[dict(tag="Strategy", text=f"A sized market: {v25[2]}M county visitors and {v25[1]}M overnight visitors a year (2025).", src=S_TEOC),
                 dict(tag="Programming", text="Family and leisure audiences dominate: 81.2% leisure, 37.0% with children, parties of 2.8 (2019).", src=S_CIC),
                 dict(tag="Hotels", text=f"{H26[2]:,} county hotel rooms at {H26[3]}% occupancy (2026 YTD); January, December and February have the most room.", src=S_CS)],
        need=[dict(tag="Measurement", text="A current Orange County visitor survey (purpose, party size, children, origins by ZIP) to replace the 2019 baseline.", src=S_CIC),
              dict(tag="Measurement", text="Tourism Economics county estimates for 2019-2020 and 2026 year to date (to be requested from Tourism Economics).", src=S_TEOC)])
    sec["calc_steps"] = [
        ["1. Orange County visitors, 2025", "Day 29.2M + overnight 22.1M", f"{v25[2]}M", S_TEOC],
        ["2. Change in visitors, 2021-2025", f"{v25[2]} / {TE_VOL[2021][2]} - 1", f"+{te_chg:.1f}%", S_TEOC],
        ["3. Visitor spending vs. 2019", f"${DR_SP[2025]:,.1f}M / ${DR_SP[2019]:,.1f}M - 1", f"+{dr_vs19:.1f}%", S_DR],
        ["4. Anaheim visitors, Jan.-June 2026 vs. 2025", f"({ANA_H1['y26'][0]} + {ANA_H1['y26'][1]}) / ({ANA_H1['y25'][0]} + {ANA_H1['y25'][1]}) - 1", f"+{h1_chg:.1f}%", S_TEFC],
        ["5. July occupancy, 2023-2025 average", f"({OCC[2023][6]} + {OCC[2024][6]} + {OCC[2025][6]}) / 3", f"{AVG3[6]}%", S_CS],
        ["6. Revenue per available room, 2026 YTD", f"{H26[3]}% x ${H26[4]:.2f}", f"${rp26:.2f}", S_CS],
        ["7. ADR change, 2019 to 2026 YTD", f"${H26[4]:.2f} / ${H19[4]:.2f} - 1", f"+{adr_chg:.1f}%", S_CS],
    ]
    vol_rows = [dict(l=str(y), v=t, t=f"{t}M", hi=False) for y, (d, o, t) in CIC_VOL.items()] + \
               [dict(l=f"{y}", v=t, t=f"{t}M", hi=(y == 2025)) for y, (d, o, t) in TE_VOL.items()]
    sec["charts"] = [
        dict(kind="cols", title=f"Orange County visitors: {v19[2]}M in 2019 (CIC) and {v25[2]}M in 2025 (Tourism Economics)",
             sub="Millions · 2009-2019 CIC Research; 2021-2025 Tourism Economics; 2020 not published; methods differ", rows=vol_rows, src=f"{S_CIC}; {S_TEOC}"),
        dict(kind="bars", title="Orange County hotel occupancy by month, 2023-2025 average", sub="CoStar · July is the peak; January the low",
             rows=[dict(l=MON[i], v=AVG3[i], t=f"{AVG3[i]}%", hi=(i == PEAK_I)) for i in range(12)], src=S_CS),
        dict(kind="bars", title="Where domestic trips to Anaheim and Garden Grove come from", sub="Share of trips by home metro area, Jan. 2023-Aug. 2026 (Azira)",
             rows=[dict(l=n, v=v, t=f"{v}%", hi=(i == 0)) for i, (n, v) in enumerate(AZ_MSA)], src=S_AZ),
    ]
    sec["feature"] = [dict(kind="line", title="Orange County hotel occupancy by month: 2026 runs above 2025 and 2019 in most months",
                           sub="CoStar, Orange County market, occupancy %, Jan.-Sept. (2026 data through Sept.)", x=MON[:9],
                           series=[dict(name="2019", v=OCC[2019][:9]), dict(name="2025", v=OCC[2025][:9]), dict(name="2026", v=OCC[2026], focal=True)],
                           yfmt=dict(suf="%", dec=1), ymin=60, src=S_CS)]
    sec["more_charts"] = [
        dict(kind="cols", title="Orange County hotel occupancy by year", sub="CoStar · 2026 is Jan.-Aug.",
             rows=[dict(l=str(r[0]), v=r[3], t=f"{r[3]}%", hi=(r[0] == "2026 YTD"), fc=False) for r in HOT], src=S_CS),
        dict(kind="bars", title="Main purpose of trip, Orange County visitors, 2019", sub="CIC Research, all visitors",
             rows=[dict(l="Pleasure or visiting friends and relatives", v=81.2, t="81.2%", hi=True), dict(l="Business or convention", v=9.6, t="9.6%"),
                   dict(l="Special events", v=7.6, t="7.6%"), dict(l="Other", v=1.6, t="1.6%")], src=S_CIC),
    ]
    T = []
    T.append(dict(title="The five questions and where each is answered", hi=-1,
                  sub="Sent by Entertainment + Culture Advisors for OCVIBE, Oct. 19, 2026",
                  cols=[["Question", 0], ["What was asked", 0], ["Answer in brief", 0], ["Main source", 0], ["Gap and solution", 0]],
                  rows=[[Q_TEXT[0][0], Q_TEXT[0][1], f"{v25[2]}M in 2025 ({v25[0]}M day, {v25[1]}M overnight; {TE_INTL25[0]}M domestic, {TE_INTL25[1]}M international); {v19[2]}M in 2019 (CIC); Anaheim Jan.-June 2026 {h1_26:.2f}M (+{h1_chg:.1f}%).", "Tourism Economics 2025; CIC 2019; Tourism Economics Sept. 2026", "County 2020 and 2026 YTD not published; request them from Tourism Economics."],
                        [Q_TEXT[1][0], Q_TEXT[1][1], "55.4% Southern California (2019); 44.7% of Anaheim and Garden Grove domestic trips from the Los Angeles-Long Beach-Anaheim metro (2023-2026).", "CIC 2019; Azira", "No ZIP codes in Azira, so no Anaheim vs. outside-Anaheim split; a custom pull or survey would provide it."],
                        [Q_TEXT[2][0], Q_TEXT[2][1], f"Hotel occupancy peaks in July ({AVG3[6]}%) and is lowest in January ({AVG3[0]}%), 2023-2025 average.", "CoStar monthly", "No monthly county visitor counts; hotel occupancy is the monthly measure."],
                        [Q_TEXT[3][0], Q_TEXT[3][1], "81.2% leisure, 9.6% business, 7.6% special events; party of 2.8; 37.0% with children; overnight stay 4.2 nights (2019).", "CIC 2019; Azira", "Latest county profile is 2019; a new survey would update it."],
                        [Q_TEXT[4][0], Q_TEXT[4][1], f"{H26[2]:,} rooms (Sept. 2026); {H26[3]}% occupancy, ${H26[4]:.2f} ADR (Jan.-Aug. 2026).", "CoStar", "None."]],
                  src=f"{S_TEOC}; {S_CIC}; {S_CS}; {S_AZ}", wide=True))
    vrows = [[str(y), f"{t}M", f"{d}M", f"{o}M", "9.1% (4.6M)" if y == 2019 else "Not published", "CIC Research"] for y, (d, o, t) in CIC_VOL.items()]
    vrows.append(["2020", "Not published", "Not published", "Not published", "Not published", f"Spending ${DR_SP[2020]/1000:.2f}B ({dr_20:.1f}% of 2019), Dean Runyan"])
    vrows += [[str(y), f"{t}M", f"{d}M", f"{o}M", f"{TE_INTL25[1]}M (6.7%)" if y == 2025 else "Not published", "Tourism Economics"] for y, (d, o, t) in TE_VOL.items()]
    vrows.append(["2026 YTD", "Not published", "Not published", "Not published", "Not published", f"Anaheim only: {h1_26:.2f}M visitors Jan.-June (+{h1_chg:.1f}%), Tourism Economics"])
    T.append(dict(title="1. Visitor arrivals to Orange County, 2009-2026", hi=len(vrows) - 2,
                  sub="Millions of visitors · overnight = stayed at least one night; day = 50+ miles, no overnight stay · two methods, shown separately",
                  cols=[["Year", 0], ["Total visitors", 1], ["Day", 1], ["Overnight", 1], ["International", 1], ["Source", 0]], rows=vrows,
                  src=f"{S_CIC} (Figure 1, Table 3); {S_TEOC}; {S_DR}; {S_TEFC}"))
    T.append(dict(title="1b. Orange County visitor spending by type of stay, 2019-2025p", hi=6,
                  sub="$ millions, Dean Runyan Associates (spending, not visitor counts) · a third method; do not mix with Tourism Economics",
                  cols=[["Year", 0], ["Visitor spending", 1], ["Day travel", 1], ["Day travel share", 1], ["Change vs. 2019", 1]],
                  rows=[[str(y) + ("p" if y == 2025 else ""), f"${DR_SP[y]:,.1f}", f"${DR_DAY[y]:,.1f}", f"{DR_DAY[y] / DR_SP[y] * 100:.1f}%",
                         {"d": round((DR_SP[y] / DR_SP[2019] - 1) * 100, 1), "t": f"{(DR_SP[y] / DR_SP[2019] - 1) * 100:+.1f}%"}] for y in DR_SP],
                  src=S_DR + ", p. 67"))
    orow = [[a, b, "", ""] for a, b in CIC_ORIG]
    for i, (n, v) in enumerate(AZ_MSA):
        if i < len(orow): orow[i][2], orow[i][3] = n, f"{v}%"
    T.append(dict(title="2. Where visitors come from", hi=0,
                  sub="Orange County 2019 (CIC, share of all visitors) and Anaheim and Garden Grove 2023-2026 (Azira, share of domestic trips by home metro area)",
                  cols=[["Orange County origin, 2019", 0], ["Share", 1], ["Anaheim and Garden Grove origin metro", 0], ["Share", 1]], rows=orow,
                  src=f"{S_CIC}; {S_AZ}"))
    T.append(dict(title="2b. International and TV-market origins", hi=0,
                  sub="International visitors to Anaheim and Garden Grove, 2025 (Tourism Economics, thousands) and domestic trips by home TV market (Azira)",
                  cols=[["International market", 0], ["Visitors, 2025", 1], ["Home TV market (DMA)", 0], ["Share of domestic trips", 1]],
                  rows=[[TE_INTL_MKT[i][0], f"{TE_INTL_MKT[i][1]:,}K", AZ_DMA[i][0] if i < len(AZ_DMA) else "", f"{AZ_DMA[i][1]}%" if i < len(AZ_DMA) else ""] for i in range(len(TE_INTL_MKT))],
                  src=f"{S_TEFC}; {S_AZ}. Orange County 2019 international leaders: Mexico 848K, Canada 786K ({S_CIC})."))
    T.append(dict(title="3. Seasonality: Orange County hotel occupancy by month, 2019-2026", hi=8,
                  sub="CoStar, Orange County market, % of rooms sold · monthly visitor counts are not published for the county",
                  cols=[["Year", 0]] + [[m, 1] for m in MON],
                  rows=[[str(y)] + [f"{v}" for v in OCC[y]] + [""] * (12 - len(OCC[y])) for y in OCC] + [["2023-25 avg."] + [f"{v}" for v in AVG3]],
                  src=S_CS, wide=True))
    T.append(dict(title="3b. Seasonality: Orange County average daily rate by month, 2019-2026", hi=8,
                  sub="CoStar, Orange County market, $ per occupied room",
                  cols=[["Year", 0]] + [[m, 1] for m in MON],
                  rows=[[str(y)] + [f"${v}" for v in ADR[y]] + [""] * (12 - len(ADR[y])) for y in ADR] + [["2023-25 avg."] + [f"${v}" for v in ADR3]],
                  src=S_CS, wide=True))
    T.append(dict(title="4. Visitor profile: Orange County visitors by type of stay, 2019", hi=-1,
                  sub="CIC Research, Table 3 · latest Orange County visitor profile · VFR = visiting friends or relatives",
                  cols=[["Measure", 0], ["Hotel guests", 1], ["Private home", 1], ["All overnight", 1], ["Day visitors", 1], ["All visitors", 1]],
                  rows=[list(r) for r in CIC_T3], src=S_CIC + ", Table 3", wide=True))
    T.append(dict(title="4b. Visitor profile: more recent indicators", hi=-1,
                  sub="Each row names its geography and period; none is a full Orange County profile",
                  cols=[["Measure", 0], ["Value", 1], ["Geography and period", 0], ["Source", 0]],
                  rows=[["Anaheim visitors with children", "42.0%", "Anaheim, 2019 (hotel leisure groups 62.6%)", S_CIC],
                        ["Anaheim travel party", "3.0 people", "Anaheim, 2019 (hotel leisure groups 3.6)", S_CIC],
                        ["Average length of stay, domestic", "1.28-1.46 days", "Anaheim and Garden Grove, by month, Jan.-Aug. 2026", S_AZ],
                        ["Average length of stay, international", "4.99 days", "Anaheim and Garden Grove, Jan. 2023-Aug. 2026", S_AZ],
                        ["Visitor median household income", "$92.5K", "Anaheim and Garden Grove domestic visitors, Jan. 2023-Aug. 2026", S_AZ],
                        ["Hotel demand by segment", f"Transient {SEG['transient']}%, group {SEG['group']}%, contract {SEG['contract']}%", "Orange County hotels, 12 months to Aug. 2026 (occupancy points)", S_CSSEG],
                        ["Trip purpose, domestic visits", "Leisure 214.2M, business 40.8M", "California, 2025", S_VCFC]],
                  src=f"{S_CIC}; {S_AZ}; {S_CSSEG}; {S_VCFC}"))
    T.append(dict(title="5. Orange County hotel inventory, occupancy and ADR, 2019-2026", hi=7,
                  sub="CoStar · revenue per available room = occupancy x ADR (BI calculation) · 2026 is Jan.-Aug. (inventory Sept.)",
                  cols=[["Year", 0], ["Rooms available a night (avg.)", 1], ["Year-end inventory", 1], ["Occupancy", 1], ["ADR", 1], ["Revenue per available room", 1]],
                  rows=[[str(r[0]), f"{r[1]:,}", f"{r[2]:,}", f"{r[3]}%", f"${r[4]:.2f}", f"${revpar(r[3], r[4]):.2f}"] for r in HOT] +
                       [["2026 forecast", "n/a", "n/a", "75.9%", "$221.61", f"${revpar(75.9, 221.61):.2f}"]],
                  src=f"{S_CS}; 2026 forecast: {S_LF}"))
    T.append(dict(title="Compare and contrast: how the visitor sources differ", hi=-1,
                  sub="Why figures differ by source, and which to use",
                  cols=[["Source", 0], ["Measures", 0], ["Years", 0], ["Geography", 0], ["Method", 0], ["Use it for", 0]],
                  rows=[["CIC Research", "Visitors, profile, spending", "2009-2019", "Orange County; Anaheim", "Intercept survey, household panel, hotel data", "2019 baseline and visitor profile"],
                        ["Tourism Economics", "Visitors, spending, jobs, taxes", "2021-2025 (county); 2019-2028 (Anaheim)", "Orange County; Anaheim; Garden Grove", "Economic model from spending, lodging and survey data", "Current visitor volume"],
                        ["Dean Runyan Associates", "Spending, jobs, taxes", "2015-2025p", "California counties", "Economic model for Visit California", "2019-2025 trend including 2020"],
                        ["Azira (Symphony)", "Trips, origins, length of stay", "Jan. 2023-Aug. 2026", "Anaheim and Garden Grove", "Mobile location data", "Origins and recent behavior"],
                        ["CoStar", "Hotel rooms, occupancy, ADR", "1987-Sept. 2026", "Orange County market", "Hotel census and sample", "Hotel capacity and seasonality"]],
                  src=f"{S_CIC}; {S_TEOC}; {S_DR}; {S_AZ}; {S_CS}", wide=True))
    sec["tables"] = T
    sec["kind"] = "News report"
    sec["dateline"] = f"ANAHEIM, Calif. ({ASOF}):"
    sec["nut"] = (f"Entertainment + Culture Advisors asked five questions for OCVIBE's market study. The answers come from five sources with different methods: "
                  f"Tourism Economics for current visitor volume ({v25[2]}M in 2025), CIC Research for the 2019 baseline and visitor profile, Azira for origins, "
                  f"and CoStar for hotel rooms and seasonality. Gaps are named with their solutions.")
    figs = [(f"{v25[2]}M", "Orange County visitors, 2025", S_TEOC), ("55.4%", "of 2019 visitors from Southern California", S_CIC),
            (f"{AVG3[6]}%", "July hotel occupancy, 2023-2025 average", S_CS), ("37.0%", "of 2019 visitors traveled with children", S_CIC),
            (f"{H26[2]:,}", "Orange County hotel rooms, Sept. 2026", S_CS), (f"{H26[3]}%", "hotel occupancy, Jan.-Aug. 2026", S_CS)]
    sec["details"] = [dict(k=k.capitalize(), text=sec["w5h"][k], fig=f, fig_l=fl, src=s) for k, (f, fl, s) in zip(("who", "what", "when", "where", "why", "how"), figs)]
    sec["info"] = []
    # place after the opening section and rebuild the reading chain
    i = next(n for n, s in enumerate(SECTIONS) if s["id"] == "p-ocv")
    SECTIONS.insert(i + 1, sec)
    nx = SECTIONS[i + 2]
    SECTIONS[i]["next"] = dict(id="p-octour", tab=sec["tab"], bridge="Anaheim sits inside a larger county market. The next section sizes Orange County: arrivals, origins, seasonality, visitor profile and hotels.")
    sec["next"] = dict(id=nx["id"], tab=nx["tab"], bridge="With the county market sized, the next question is who visits the OC Vibe area itself.")
    # appendix: formulas, glossary, methods, who-what-when table
    ap = next((s for s in SECTIONS if s["id"] == "p-appx"), None)
    if ap:
        fo, gl, me = ap["tables"][0], ap["tables"][1], ap["tables"][2]
        fo["rows"] += [["Rooms available a night (average)", "Annual available room nights / days in the year", "21,400,998 / 365 = 58,633 (Orange County, 2019)"],
                       ["Seasonality average", "(Month in 2023 + 2024 + 2025) / 3", f"({OCC[2023][6]} + {OCC[2024][6]} + {OCC[2025][6]}) / 3 = {AVG3[6]}% (July)"],
                       ["Year-to-date change", "This year's months / same months last year - 1", f"{h1_26:.2f}M / {h1_25:.2f}M - 1 = +{h1_chg:.1f}% (Anaheim, Jan.-June)"]]
        have = {r[0] for r in gl["rows"]}
        gl["rows"] += [r for r in [
            ["Day visitor", "A visitor who does not stay overnight. Tourism Economics counts day visitors who travel 50+ miles."],
            ["Overnight visitor", "A visitor who stays at least one night: in a hotel, a private home or other lodging."],
            ["VFR (visiting friends or relatives)", "A trip whose main purpose is to see friends or family; often combined with pleasure in surveys."],
            ["MSA (metropolitan statistical area)", "A federal metro-area definition; Los Angeles-Long Beach-Anaheim includes Los Angeles and Orange counties."],
            ["DMA (designated market area)", "A TV market defined by Nielsen; used for media planning and origin reporting."],
            ["Transient, group and contract demand", "Hotel rooms sold to individual travelers, to groups of 10+ rooms, and under long-term contracts (for example, airline crews)."],
            ["Year to date (YTD)", "From Jan. 1 to the latest month with data."],
            ["Travel party", "The people traveling together on one trip, counted per group."]] if r[0] not in have]
        gl["rows"].sort(key=lambda r: r[0].lower())
        me["rows"] += [["Orange County visitor profile (2019)", "CIC Research: 2,686 intercept interviews at 36 Orange County locations plus an internet panel of 2,087 households; 4,040 visitor groups.", S_CIC],
                       ["Orange County visitor volume", "Tourism Economics model (2021-2025) and CIC estimates (2009-2019) are separate series; not combined.", f"{S_TEOC}; {S_CIC}"],
                       ["Seasonality", "CoStar monthly hotel occupancy and ADR used as the monthly measure; 2023-2025 average by month.", S_CS]]
        for c in ap["cards"]:
            if c[0] == "Glossary": c[2] = str(len(gl["rows"]))
            if c[0] == "Methods": c[2] = str(len(me["rows"]))
        ap["ans"] = f"A plain-language guide: {len(gl['rows'])} terms, {len(me['rows'])} methods and {len(fo['rows'])} formulas, so every figure in this report can be traced and repeated."
        for t in ap["tables"]:
            if t["title"].startswith("Who, what, when"):
                rows = [x for x in t["rows"] if x[0] != sec["tab"]]
                rows.insert(1, [sec["tab"]] + [sec["w5h"][k] for k in ("who", "what", "when", "where", "why", "how")])
                t["rows"] = rows
    REGISTER.extend([
        ["CIC Research for Visit Anaheim", "Annual Profile of Visitors to Anaheim and Orange County, 2019", "Calendar 2019 (volume 2009-2019)", "Apr. 2020; found Oct. 19, 2026", "Orange County visitor volume, origins and profile", "Original PDF reviewed; latest edition found"],
        ["Dean Runyan Associates for Visit California", "The Economic Impact of Travel in California, 2025p; Travel Impacts by Assembly District", "2015-2025p", "Apr. 2026; reviewed Oct. 19, 2026", "Orange County visitor spending including 2020", "Original PDFs reviewed; preliminary"],
        ["CoStar", "Orange County market monthly and segmentation tables", "Jan. 1987-Sept. 2026", "Pulled Oct. 2026; reviewed Oct. 19, 2026", "Hotel inventory, occupancy, ADR, segments, seasonality", "Licensed export; summary figures only"],
        ["Symphony | Tourism Economics (Azira)", "Domestic and International Visitors views (Anaheim and Garden Grove)", "Jan. 1, 2023-Aug. 31, 2026", "Pulled Oct. 2026; confirmed Oct. 19, 2026", "Origins, length of stay, distance share", "Geography and period confirmed with BI; 2026 method shift flagged"],
        ["Visit California", "Monthly Travel Indicators (Aug. 2026); Resident Sentiment 2025; Travel and Lodging Forecasts (Sept. 2026)", "2013-2030", "Mar.-Oct. 2026; reviewed Oct. 19, 2026", "Statewide context, county lodging forecast, resident sentiment", "Original files reviewed"],
    ])
    SOURCES.append(["Orange County tourism statistics (Oct. 19, 2026)", f"{S_CIC}; {S_TEOC}; {S_DR}; {S_CS}; {S_AZ}; {S_LF}; {S_MTI}."])
    DQ.extend([
        "Orange County visitor counts come from two methods (CIC Research 2009-2019; Tourism Economics 2021-2025) and are shown as separate series; 2020 and 2026 year to date are not published for the county.",
        "Azira files cover Anaheim and Garden Grove, not Orange County, and carry no ZIP codes; 2026 length of stay and distance shares reflect a likely method change.",
        "The latest Orange County visitor profile (trip purpose, party size, children) is CIC Research's 2019 study.",
    ])
    TAKEAWAYS.insert(1, f"Orange County market: {v25[2]}M visitors in 2025 ({v25[1]}M overnight; 93.3% domestic); 55.4% from Southern California and 37.0% traveling with children (2019); {H26[2]:,} hotel rooms at {H26[3]}% occupancy and ${H26[4]:.2f} ADR in Jan.-Aug. 2026, with July the peak month. (Source: {S_TEOC}; {S_CIC}; {S_CS})")
