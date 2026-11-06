"""Comparison clarity (Nov. 5, 2026, OCVIBE feedback).

Rule: whenever a figure is compared with another period, place or baseline, the comparison is
stated in one place: the latest figure first, then "vs." or "compared with" and the comparison
period (for example "51.3M in 2025 vs. the 2019 baseline of 50.21M"). A baseline is a reference
point, never the period being reported. Figures from the latest available survey are labeled
"latest ... (year)" so they are not read as an old comparison.

This module runs last in content.py. PHRASES rewrites rendered text exactly (each pair must match
at least once; unmatched pairs are listed in UNUSED for the validation suite).
"""
import re

PHRASES = [
    # Anaheim and OCVIBE today
    ("Tourism Economics forecasts 27.0M visitors (+1.9%) and $7.2B (+5.6%) for 2026.",
     "Tourism Economics forecasts 27.0M visitors and $7.2B for 2026, up 1.9% and 5.6% vs. 2025."),
    ("▲ +0.8% vs. 2024 · 2026 forecast 27.0M", "▲ +0.8% vs. 2024 · 2026 forecast 27.0M (+1.9% vs. 2025)"),
    ("▲ +3.1% vs. 2024 · 2026 forecast $7.2B", "▲ +3.1% vs. 2024 · 2026 forecast $7.2B (+5.6% vs. 2025)"),
    ("Anaheim Q2 2026: 6.74M visitors (+2.8%), $1.76B spending (+7.8%);", "Anaheim Q2 2026 vs. Q2 2025: 6.74M visitors (+2.8%), $1.76B spending (+7.8%);"),
    ("visitor spending of $7.2B in 2026, up 5.6%, with visitors up 1.9% to 27.0M.", "visitor spending of $7.2B in 2026, up 5.6% vs. 2025, with visitors up 1.9% to 27.0M."),
    ("Visitors returned to 26.5 million in 2025, above 2019's 24.2 million", "Visitors: 26.5 million in 2025 vs. the 2019 baseline of 24.2 million"),
    ("Anaheim only: 13.06M visitors Jan.-June (+3.1%), Tourism Economics", "Anaheim only: 13.06M visitors Jan.-June 2026 (+3.1% vs. Jan.-June 2025), Tourism Economics"),
    # Visitor spending and Visa
    ("International restaurant spending fell 19.1% in August 2026.", "International restaurant spending fell 19.1% in August 2026 vs. August 2025."),
    ("international restaurant spending fell 19.1% in August 2026.", "international restaurant spending fell 19.1% in August 2026 vs. August 2025."),
    ("2.16 million forecast for 2026 (+1.0%), spending $2.79 billion; Mexico leads growth (+6.9%).",
     "2.16 million forecast for 2026 (+1.0% vs. 2025), spending $2.79 billion; Mexico leads growth (+6.9% vs. 2025)."),
    ("Q2 2026 visitor spending rose 7.8% and overnight visits 4.5%.", "Q2 2026 visitor spending rose 7.8% and overnight visits 4.5% vs. Q2 2025."),
    ("Visitor card spending reached $464.6M in August 2026, up 8.1% (Visa). Spending per card rose 4.7% to $85,",
     "Visitor card spending reached $464.6M in August 2026, up 8.1% vs. August 2025 (Visa). Spending per card rose 4.7% to $85,"),
    ("Q2 2026 spending ($1.76B, +7.8%) and visitor card spending ($464.6M in Aug. 2026, +8.1%).",
     "Q2 2026 spending ($1.76B, +7.8% vs. Q2 2025) and visitor card spending ($464.6M in Aug. 2026, +8.1% vs. Aug. 2025)."),
    ("Visa spending per card rose 4.7% to $85 in August 2026:", "Visa spending per card rose 4.7% to $85 in August 2026 vs. August 2025:"),
    ("International card spending fell 5.0% in August 2026.", "International card spending fell 5.0% in August 2026 vs. August 2025."),
    ("Visitor card spending reached $464.6M in August 2026 (+8.1%), and spending per card rose 4.7% to $85.",
     "Visitor card spending reached $464.6M in August 2026 (+8.1% vs. August 2025), and spending per card rose 4.7% to $85."),
    ("Anaheim visitors spent $1.76 billion in the second quarter, up 7.8%", "Anaheim visitors spent $1.76 billion in the second quarter, up 7.8% from a year earlier"),
    ("$1.76B (+7.8%)", "$1.76B (+7.8% vs. Q2 2025)"),
    ("and Visa shows visitor card spending up 8.1% in August 2026.", "and Visa shows visitor card spending up 8.1% in August 2026 vs. August 2025."),
    ("Each Anaheim visitor is forecast to spend $279 by 2028, up from $223 in 2019",
     "Each Anaheim visitor is forecast to spend $279 by 2028, compared with $258 in 2025 and the 2019 baseline of $223"),
    # Jobs and economy
    ("fastest-growing spending category in 2025 (+5.5%).", "fastest-growing spending category in 2025 (+5.5% vs. 2024)."),
    ("Visitor spending grew 3.1% in 2025; jobs supported reached 67,817.", "Visitor spending grew 3.1% in 2025 vs. 2024; jobs supported reached 67,817."),
    ("Food and beverage was the fastest-growing category (+5.5%)", "Food and beverage was the fastest-growing category in 2025 (+5.5% vs. 2024)"),
    ("fastest-growing visitor spending category in 2025 (+5.5%),", "fastest-growing visitor spending category in 2025 (+5.5% vs. 2024),"),
    ("fastest-growing visitor spending category in 2025, up 5.5% in Anaheim.", "fastest-growing visitor spending category in 2025, up 5.5% in Anaheim vs. 2024."),
    ("Visitors spent $6.8 billion in Anaheim in 2025, up 3.1%,", "Visitors spent $6.8 billion in Anaheim in 2025, up 3.1% vs. 2024,"),
    # Hotel market
    ("▲ +3.1% · Orange County 74.0%", "▲ +3.1% vs. prior 12 months · Orange County 74.0%"),
    ("▲ +10.9% vs. 2025 · Orange County ▲ +9.9%", "▲ +10.9% vs. Jan.–Aug. 2025 · Orange County ▲ +9.9%"),
    ("food revenue per room ▲ +28.9%", "food revenue per room ▲ +28.9% vs. prior 12 months"),
    ("2026 rates are 33% above 2019; occupancy is still below 2019", "2026 year-to-date rates are 33% above the 2019 baseline; occupancy is still below the 2019 baseline"),
    ("growing +2.69% vs. +1.59% nationally.", "growing +2.69% over the past year vs. +1.59% nationally."),
    ("(+10.9% year to date).", "(+10.9% Jan.–Aug. 2026 vs. Jan.–Aug. 2025)."),
    ("and food revenue per room rose 28.9%.", "and food revenue per room rose 28.9% vs. the prior 12 months."),
    ("revenue per available room is up 10.9% so far this year.", "revenue per available room is up 10.9% in Jan.–Aug. 2026 vs. the same months of 2025."),
    ("reached $253 in 2026, 33% above 2019.", "reached $253 in Jan.–Aug. 2026, 33% above the 2019 baseline."),
    ("food revenue per available room rose 28.9%.", "food revenue per available room rose 28.9% vs. the prior 12 months."),
    # Getting here
    ("Passengers +3% in 2025, +4% Jan.–Apr. 2026;", "Passengers +3% in 2025 vs. 2024, +4% Jan.–Apr. 2026 vs. Jan.–Apr. 2025;"),
    ("+6%; 15,964 weekend riders (−41%)", "+6% vs. a year earlier; 15,964 weekend riders (−41% vs. a year earlier)"),
    ("carries 5,116 weekday riders and is growing (+4%),", "carries 5,116 weekday riders and is growing (+4% vs. a year earlier),"),
    ("Metrolink's Orange County Line weekday riders rose 4%.", "Metrolink's Orange County Line weekday riders rose 4% vs. a year earlier."),
    ("(5,116 weekday riders, +4%)", "(5,116 weekday riders, +4% vs. a year earlier)"),
    ("up 32% from 2019;", "up 32% from the 2019 baseline;"),
    ("(+10% since 2019).", "(+10% vs. the 2019 baseline)."),
    ("John Wayne Airport passengers rose 4% through April.", "John Wayne Airport passengers rose 4% in Jan.–Apr. 2026 vs. Jan.–Apr. 2025."),
    # Market outlook (LARC)
    ("rose 11.4% in Q2 2026 (U.S. +5.7%), and Convention Center room nights are pacing +12% for 2026 and +17% for 2027.",
     "rose 11.4% in Q2 2026 vs. Q2 2025 (U.S. +5.7%), and Convention Center room nights on the books are pacing +12% for 2026 and +17% for 2027 vs. the same point a year earlier."),
    ("2026 pace vs. last year · 2027 ▲ +17%", "2026 pace vs. the same point last year · 2027 ▲ +17%"),
    ("Rate ▲ +7.8% · occupancy ▲ +3.3% · U.S. ▲ +5.7%", "Q2 2026 vs. Q2 2025 · rate ▲ +7.8% · occupancy ▲ +3.3% · U.S. ▲ +5.7%"),
    ("Anaheim hotel revenue per room rose 11.4% in Q2 2026, and convention room nights are pacing +12% for 2026 and +17% for 2027.",
     "Anaheim hotel revenue per room rose 11.4% in Q2 2026 vs. Q2 2025, and convention room nights are pacing +12% for 2026 and +17% for 2027 vs. the same point a year earlier."),
    ("Q2 2026 hotel revenue per room +11.4% (U.S. +5.7%); convention room nights pacing +12% (2026) and +17% (2027);",
     "Q2 2026 hotel revenue per room +11.4% vs. Q2 2025 (U.S. +5.7%); convention room nights pacing +12% (2026) and +17% (2027) vs. the same point a year earlier;"),
    ("Q2 2026 hotel revenue per room +11.4%, double the U.S. (+5.7%).", "Q2 2026 hotel revenue per room +11.4% vs. Q2 2025, double the U.S. (+5.7%)."),
    ("Convention room nights pace +17% for 2027,", "Convention room nights for 2027 pace +17% ahead of the same point a year earlier,"),
    ("2027 convention pacing (+17%)", "2027 convention pacing (+17% vs. the same point a year earlier)"),
    ("Anaheim hotel revenue per room up 11.4% as OCVIBE nears opening", "Anaheim hotel revenue per room up 11.4% from a year earlier as OCVIBE nears opening"),
    ("+11.4% (U.S. +5.7%)", "+11.4% vs. Q2 2025 (U.S. +5.7%)"),
    ("+12% (2026); +17% (2027)", "+12% (2026); +17% (2027), each vs. the same point a year earlier"),
    ("revenue per available room up 11.4% in Q2 2026 and convention room nights pacing 17% ahead for 2027,",
     "revenue per available room up 11.4% in Q2 2026 vs. Q2 2025 and convention room nights pacing 17% ahead for 2027 vs. the same point a year earlier,"),
    ("Anaheim hotel revenue per room, Q2 2026 (U.S. +5.7%)", "Anaheim hotel revenue per room, Q2 2026 vs. Q2 2025 (U.S. +5.7%)"),
    # Questions answered
    ("Yes. Anaheim visitor spending rose 3.1% in 2025 and 7.8% in Q2 2026. Orange County grew 3.4%, California 1.7% and the U.S. 1.4% after inflation.",
     "Yes. Anaheim visitor spending rose 3.1% in 2025 vs. 2024 and 7.8% in Q2 2026 vs. Q2 2025. In 2025 vs. 2024, Orange County grew 3.4%, California 1.7% and the U.S. 1.4% after inflation."),
    ("Tourism Economics forecasts Anaheim visitor spending of $7.2B in 2026 (+5.6%).", "Tourism Economics forecasts Anaheim visitor spending of $7.2B in 2026 (+5.6% vs. 2025)."),
    ("Anaheim welcomed 6.74M visitors in Q2 2026 (+2.8%), who spent $1.76B (+7.8%). Overnight visits rose 4.5% and day visits 2.1%; hotel rates were nearly 9% higher. Garden Grove: 831,000 visitors (+3.4%), $200.4M (+7.1%).",
     "Anaheim welcomed 6.74M visitors in Q2 2026, who spent $1.76B. Compared with Q2 2025: visitors +2.8%, spending +7.8%, overnight visits +4.5%, day visits +2.1% and hotel rates nearly 9% higher. Garden Grove: 831,000 visitors (+3.4% vs. Q2 2025), $200.4M (+7.1%)."),
    ("Anaheim visitor spending, Q2 2026 (+7.8%)", "Anaheim visitor spending, Q2 2026 (+7.8% vs. Q2 2025)"),
    ("+2.8% visitors · +7.8% spending; first half 13.1M visitors, $3.5B", "Q2 2026 vs. Q2 2025: +2.8% visitors · +7.8% spending; first half 2026 13.1M visitors, $3.5B"),
    ("+3.4% visitors · +7.1% spending", "Q2 2026 vs. Q2 2025: +3.4% visitors · +7.1% spending"),
    ("+1.0%; spending $2.79B (+1.8%); Mexico +6.9%", "2026 forecast vs. 2025: +1.0%; spending $2.79B (+1.8%); Mexico +6.9%"),
    ("The average U.S. domestic airfare was $387 (+9.9% since 2019),", "The average U.S. domestic airfare was $387 in 2025 (+9.9% vs. the 2019 baseline),"),
    ("Domestic average, 2025; $352 in 2019", "2025 domestic average; compared with $352 in the 2019 baseline"),
    ("Average total cost, 2024; $0.62 in 2019", "2024 average total cost; compared with $0.62 in the 2019 baseline"),
    ("Anaheim and Garden Grove; Mexico 819,078 (+6.9%)", "Anaheim and Garden Grove; Mexico 819,078 (+6.9% vs. 2025)"),
    ("Anaheim hotel revenue per room rose 11.4% in Q2 2026, about twice the U.S. (+5.7%).", "Anaheim hotel revenue per room rose 11.4% in Q2 2026 vs. Q2 2025, about twice the U.S. (+5.7%)."),
    ("RevPAR $199.78 (+7.9%); 21,213 rooms", "RevPAR $199.78 (+7.9% vs. prior 12 months); 21,213 rooms"),
    ("RevPAR $162 (+6.9%); 60,223 rooms;", "RevPAR $162 (+6.9% vs. prior 12 months); 60,223 rooms;"),
    ("LARC forecasts Anaheim hotel revenue per room of $162.18 in 2026 (+7.0%). Nationally, trips are forecast to grow 2.0% in 2026.",
     "LARC forecasts Anaheim hotel revenue per room of $162.18 in 2026 (+7.0% vs. 2025). Nationally, trips are forecast to grow 2.0% in 2026 vs. 2025."),
    # Takeaways, BI Pulse Summary and stories
    ("forecast to reach $279 by 2028; Q2 2026 spending rose 7.8%.", "forecast to reach $279 by 2028; Q2 2026 spending rose 7.8% vs. Q2 2025."),
    ("(Q2 revenue per room +11.4% vs. +5.7%)", "(Q2 2026 revenue per room vs. Q2 2025: Anaheim +11.4%, U.S. +5.7%)"),
    ("visitor card spending rose 8.1% in August 2026 (Visa);", "visitor card spending rose 8.1% in August 2026 vs. August 2025 (Visa);"),
    ("Visitors spent $1.76 billion in Q2 2026 (+7.8%), hotel revenue per room rose 11.4%, and Convention Center room nights for 2027 are pacing 17% ahead.",
     "Visitors spent $1.76 billion in Q2 2026 (+7.8% vs. Q2 2025), hotel revenue per room rose 11.4% vs. Q2 2025, and Convention Center room nights for 2027 are pacing 17% ahead of the same point a year earlier."),
    ("Visitors spent $1.76 billion in Anaheim in the second quarter, up 7.8%, according to Tourism Economics.",
     "Visitors spent $1.76 billion in Anaheim in the second quarter, up 7.8% from the second quarter of 2025, according to Tourism Economics."),
    ("Overnight visits led the gain, rising 4.5%, while day visits rose 2.1%.", "Overnight visits led the gain, rising 4.5% from a year earlier, while day visits rose 2.1%."),
    ("LARC reports hotel revenue per room rose 11.4% in the second quarter.", "LARC reports hotel revenue per room rose 11.4% in the second quarter vs. a year earlier."),
]

# Plain-language reader aids (glossary and method rows) added to the Appendix.
GLOSSARY = [
    ["Baseline", "A reference period that a newer figure is compared against, such as 2019 (before the pandemic). The baseline is not the period being reported: the latest figure is shown first and the baseline second, for example \"51.3M in 2025 vs. the 2019 baseline of 50.21M\"."],
    ["Comparison (vs.)", "Every change in this report names both sides: the latest period first, then the period, place or baseline it is compared with (for example \"Q2 2026 vs. Q2 2025\" or \"Anaheim vs. U.S.\")."],
    ["Latest available survey", "The newest published survey on a topic. When the newest county visitor survey is from 2019, its figures are labeled \"latest county survey (2019)\" because no newer edition exists, not because 2019 is being compared."],
]
METHOD = [["How comparisons are written", "Each comparison is stated in one place: latest figure and period, then \"vs.\" or \"compared with\" and the comparison period or baseline, then the change. Data cards that compare two years carry both values in the same card.", "Visit Anaheim BI (Nov. 5, 2026)"]]

# Whole-string replacements (short labels that must match exactly).
EXACT = {"Revenue per available room, Q2 2026": "Revenue per available room, Q2 2026 vs. Q2 2025"}

UNUSED = []


_ORDER = sorted(range(len(PHRASES)), key=lambda i: -len(PHRASES[i][0]))   # longest first, so short phrases never split a longer one


def _walk(o, hits):
    if isinstance(o, dict):
        for k in list(o):
            o[k] = _walk(o[k], hits)
        return o
    if isinstance(o, list):
        for i in range(len(o)):
            o[i] = _walk(o[i], hits)
        return o
    if isinstance(o, tuple):
        return tuple(_walk(x, hits) for x in o)
    if isinstance(o, str):
        if o in EXACT:
            return EXACT[o]
        for i in _ORDER:
            a, b = PHRASES[i]
            if a in o and b not in o:
                o = o.replace(a, b); hits[i] += 1
            elif b in o:
                hits[i] += 1
        return o
    return o


def attach(SECTIONS, STORIES, TAKEAWAYS, RECS, DQ, DATA_EXTRA):
    hits = [0] * len(PHRASES)
    for obj in (SECTIONS, STORIES, TAKEAWAYS, RECS, DQ, DATA_EXTRA):
        _walk(obj, hits)
    UNUSED[:] = [PHRASES[i][0] for i, h in enumerate(hits) if not h]
    ap = next((s for s in SECTIONS if s.get("id") == "p-appx"), None)
    if ap:
        gl, me = ap["tables"][1], ap["tables"][2]
        have = {r[0] for r in gl["rows"]}
        gl["rows"] += [r for r in GLOSSARY if r[0] not in have]
        gl["rows"].sort(key=lambda r: r[0].lower())
        if not any(r[0] == METHOD[0][0] for r in me["rows"]):
            me["rows"] += METHOD
        for c in ap.get("cards", []):
            if c[0] == "Glossary": c[2] = str(len(gl["rows"]))
            if c[0] == "Methods": c[2] = str(len(me["rows"]))
        fo = ap["tables"][0]
        ap["ans"] = re.sub(r"\d+ terms, \d+ methods and \d+ formulas", f"{len(gl['rows'])} terms, {len(me['rows'])} methods and {len(fo['rows'])} formulas", ap.get("ans", ""))
