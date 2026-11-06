"""Confidential data and shareable summaries (Nov. 5, 2026, per John Picou).

Visit Anaheim-owned studies and licensed data stay in full in the app as the main view, marked Confidential.
For each confidential finding the app offers a shareable summary: the finding in words, without the underlying
figures, so OCVIBE can brief outside representatives without passing on Visit Anaheim's proprietary or licensed data.

Confidential sources (John Picou, Nov. 5, 2026):
  Visit Anaheim-owned studies: One more night study and workbook, paid-media attribution, CIC Research visitor profile.
  Licensed data: STR, CoStar, Symphony | Tourism Economics (Azira, Visa), Datafy, LARC.
Public and published sources (Tourism Economics reports, Visit California, U.S. Travel, OCTA, BTS, City, OCVIBE) are not
marked and can be quoted with their source and date. Library files stay downloadable, labeled Confidential.
Runs last in content.py, after clarity.py.
"""

CONF_PUB = ("Visit Anaheim Business Intelligence", "Symphony", "Visa Destination Insights", "Datafy", "CoStar", "STR (", "Lodging Analytics", "CIC Research")
CONF_NOT = {"ocv-report", "ocv-deck", "ocv-qa", "vca-lodging-fc"}   # this report itself; Visit California's published forecast
LABEL = "Confidential"
NOTE = ("Confidential: Visit Anaheim proprietary or licensed data. Use the figures inside OCVIBE; when sharing with outside "
        "representatives, use the shareable summary instead of the figures or this file.")

# Shareable summaries: findings in words, no figures. Each is factual and traces to the question's answer.
Q_SHARE = {
    "night-value": "Visit Anaheim's One more night study shows that longer stays are one of the largest growth levers for Anaheim's visitor economy: each added night per visitor adds substantial lodging and total visitor spending.",
    "night-1pct": "Even a small share of visitors staying one day longer adds meaningful visitor spending. Sunday and Monday are the most open hotel nights, so events on those nights fill rooms that would otherwise sit empty.",
    "getting-here": "Most visitors to Anaheim and Garden Grove arrive by car from within driving distance. SR-57 beside OCVIBE is one of the area's busiest freeways, and ARTIC adds bus, Amtrak and Metrolink service.",
    "d5-who": "Most visitors to District 5, where OCVIBE is being built, stay overnight, a large share are first-time visitors, and their household incomes are above the average for Anaheim and Garden Grove visitors.",
    "d5-share": "The OCVIBE area already accounts for a small but measurable share of Anaheim visitor days before its new venues open, which gives a baseline for measuring OCVIBE's growth.",
    "d5-markets": "Southern California is the largest source of District 5 visitors. The leading fly-in markets by visitor card spending are Seattle, Phoenix, Las Vegas, Orlando and New York; internationally, Mexico, Canada and Japan.",
    "media": "Visit Anaheim's paid media is measurably linked to later visits to Anaheim, and luxury and travel-planning placements perform best.",
    "hotels": "Hotels in the Disneyland resort area run among the highest occupancy and rates in Orange County, and Anaheim's hotel revenue growth is outpacing the U.S.",
    "outlook": "Visit Anaheim's licensed hotel forecast points to continued growth in Anaheim hotel revenue in 2026. Tourism Economics' published visitor and spending forecast can be quoted with its source and date.",
    "oc-arrivals": "Orange County's 2025 visitor count from Tourism Economics can be quoted with its source and date. Compared with the pre-pandemic 2019 baseline from Visit Anaheim's commissioned visitor survey, 2025 volume is at a similar level.",
    "oc-origins": "More than half of Orange County visitors come from Southern California. The Los Angeles and Inland Empire metros are the largest domestic markets, and Mexico and Canada lead international markets.",
    "oc-season": "Orange County hotels are fullest in summer, peaking in July, and have the most open rooms in January, December and February.",
    "oc-profile": "Most Orange County visitors travel for leisure or to see friends and family, usually in small groups, and more than a third bring children. Overnight visitors stay several nights.",
    "oc-hotels": "Orange County's hotel market is running fuller and at higher rates in 2026 than in 2025, with rates well above the pre-pandemic baseline.",
}

# Section-level summaries: which figures are confidential, and the summary to share instead.
S_SHARE = {
    "p-ocv": ("The OCVIBE area's share of Anaheim visitor days (Datafy).", ["d5-share"]),
    "p-octour": ("The 2019 visitor survey figures (CIC Research), hotel occupancy, rates and seasonality (CoStar) and Anaheim and Garden Grove origins and length of stay (Azira).", ["oc-arrivals", "oc-origins", "oc-season", "oc-profile", "oc-hotels"]),
    "p-d5": ("District 5 visitor profile and markets (Azira, Visa) and the OCVIBE area share (Datafy).", ["d5-who", "d5-markets", "d5-share"]),
    "p-hotel": ("Hotel occupancy, rates and pipeline (CoStar, STR, LARC).", ["hotels", "night-1pct"]),
    "p-night": ("The One more night study and its workbook (Visit Anaheim) and the hotel-night figures (STR).", ["night-value", "night-1pct"]),
    "p-transport": ("Visitor origin by distance (Azira). Traffic, bus, rail and cost figures are public and can be quoted.", ["getting-here"]),
    "p-media": ("Paid-media impressions, visits and visit rates (Azira attribution).", ["media"]),
    "p-larc": ("LARC hotel and convention figures (licensed).", ["outlook", "hotels"]),
}


def _is_conf(f):
    return f["id"] not in CONF_NOT and any(p in f["publisher"] for p in CONF_PUB)


def attach(SECTIONS, DATA_EXTRA):
    lib = DATA_EXTRA["lib"]["files"]
    conf_ids = set()
    for f in lib:
        if _is_conf(f):
            f["conf"] = True
            conf_ids.add(f["id"])
            if NOTE not in (f.get("note") or ""):
                f["note"] = (f.get("note", "") + " " + NOTE).strip()
    ask = DATA_EXTRA["ask"]
    QS = {q["id"]: q for q in ask["items"]}
    for qid, txt in Q_SHARE.items():
        if qid in QS:
            QS[qid]["conf"] = True
            QS[qid]["share"] = txt
    # The shareable recap: every confidential finding in one place, to copy for outside representatives
    rec = [[QS[k]["q"], v, ", ".join(sorted({FILE_PUB(lib, fid) for fid in QS[k]["files"] if fid in conf_ids}))] for k, v in Q_SHARE.items() if k in QS]
    if not any(q["id"] == "conf-recap" for q in ask["items"]):
        ask["items"].append(dict(
            id="conf-recap", topic="OCVIBE requests", q="What can OCVIBE share outside about Visit Anaheim's confidential data?",
            a=f"Use the shareable summaries: {len(rec)} findings in words, without the figures. The full figures stay in this app for OCVIBE's own use; outside representatives receive the summaries, with Visit Anaheim named as the source.",
            key=str(len(rec)), key_l="shareable summaries of confidential findings",
            geo=[[r[0], "Shareable summary", r[1], "Visit Anaheim (confidential source: " + (r[2] or "Visit Anaheim") + ")"] for r in rec],
            viz=None,
            how="Confidential sources: Visit Anaheim-owned studies (One more night, paid-media attribution, CIC Research visitor profile) and licensed data (STR, CoStar, Azira and Visa via Symphony, Datafy, LARC). Each summary states the finding without the underlying figures.",
            caveat="Published sources (Tourism Economics reports, Visit California, U.S. Travel, OCTA, BTS, City of Anaheim, OCVIBE) are not confidential and can be quoted with their source and date. Questions about sharing: bi@visitanaheim.org.",
            files=[], go="p-library", links=[], conf=True,
            share="\n".join(f"{r[0]} {r[1]}" for r in rec)))
    for s in SECTIONS:
        if s["id"] in S_SHARE:
            what, qids = S_SHARE[s["id"]]
            s["conf"] = dict(label=LABEL, what=what, share=" ".join(Q_SHARE[q] for q in qids if q in Q_SHARE))
    DATA_EXTRA["conf"] = dict(label=LABEL, note=NOTE, recap=rec)


def FILE_PUB(lib, fid):
    f = next((x for x in lib if x["id"] == fid), None)
    if not f:
        return ""
    p = f["publisher"]
    for k, v in (("Visa", "Visa via Symphony"), ("Symphony", "Azira via Symphony"), ("STR", "STR"), ("CoStar", "CoStar"), ("Lodging", "LARC"),
                 ("Datafy", "Datafy"), ("CIC", "CIC Research"), ("Visit Anaheim", "Visit Anaheim study")):
        if k in p:
            return v
    return p
