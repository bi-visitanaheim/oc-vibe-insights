"""Update schedule for OCVIBE Insights (added Oct. 14, 2026, per John Picou).

The report is refreshed quarterly because Tourism Economics delivers its Anaheim Travel Forecast each quarter
(docs/quarterly-refresh.md). LAST_UPDATE is the date of the latest data update; the quarterly refresh sets it.
The next scheduled update is computed: the first 15th of January, April, July or October after LAST_UPDATE."""
import datetime as _dt

LAST_UPDATE = _dt.date(2026, 10, 19)       # data last updated (prepared date of this edition)
RUN_MONTHS, RUN_DAY = (1, 4, 7, 10), 15    # scheduled task "OCVIBE Insights quarterly refresh", about 9 a.m. Pacific
SCHED_SRC = "Visit Anaheim BI, quarterly refresh runbook (Oct. 13, 2026; cadence confirmed Oct. 14, 2026)"
CONTACT = "bi@visitanaheim.org"
_MON = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def ap(d):
    """AP-style date: Oct. 15, 2026."""
    return f"{_MON[d.month - 1]} {d.day}, {d.year}"


def next_update(after=LAST_UPDATE):
    for y in (after.year, after.year + 1):
        for m in RUN_MONTHS:
            d = _dt.date(y, m, RUN_DAY)
            if d > after:
                return d


NEXT = next_update()
LAST_S, NEXT_S = ap(LAST_UPDATE), ap(NEXT)
LINE = f"Updated quarterly · Data last updated {LAST_S}"   # Nov. 5, 2026: no next-update date is shown (the next update may come early)

LEDE = (f"Visit Anaheim Business Intelligence updates OCVIBE Insights each quarter, after Tourism Economics delivers "
        f"its quarterly Anaheim Travel Forecast, and sooner when new data arrives. The data was last updated {LAST_S}.")

# Who, what, when, where, why and how of the update (same card format as each section's "The details").
DETAILS = [
    dict(k="Who", fig="Visit Anaheim BI", fig_l="Business Intelligence team",
         text=f"Prepares each update and checks every figure against its source before it is published. Questions go to {CONTACT}.",
         src=SCHED_SRC),
    dict(k="What", fig="Changed figures only", fig_l="New published or measured values",
         text="Each update replaces only figures that have a new published or measured value, with the new period and publication date, and rewrites any sentence that cites them. A source with nothing new keeps its current, dated figures; no figure is estimated to fill a gap.",
         src=SCHED_SRC),
    dict(k="When", fig="Quarterly", fig_l="Each quarter, or sooner when new data arrives",
         text=f"Updates follow Tourism Economics' quarterly forecast and are posted as soon as new data is received and checked. Data last updated {LAST_S}.",
         src=SCHED_SRC),
    dict(k="Where", fig="3 formats", fig_l="Dashboard, deck and data tables",
         text="Each update is published to the dashboard (oc-vibe-insights.vercel.app and the claude.ai dashboard), the downloadable PowerPoint deck and the data tables (Excel and CSV).",
         src=SCHED_SRC),
    dict(k="Why", fig="Every quarter", fig_l="Tourism Economics forecast cycle",
         text="Tourism Economics data is the core of this report (Anaheim's visitor volume, spending and forecast), and its Anaheim Travel Forecast arrives each quarter. STR, CoStar and Visa are available weekly or monthly and Azira monthly; they are pulled at the same time, so every figure in an edition shares one as-of date.",
         src="Tourism Economics, Anaheim Travel Forecast (quarterly); " + SCHED_SRC),
    dict(k="How", fig="4 steps", fig_l="Find, update, check, publish",
         text="Find the newest file from each source; update only changed figures and the sentences that cite them; check every number against its table and source; republish the dashboard, deck and data tables with the new dates.",
         src=SCHED_SRC),
]

# When each source publishes and what the quarterly update does with it. Periods match the source register.
TABLE = dict(
    title="When each source updates",
    cols=[["Source", 0], ["How often it publishes", 0], ["In this edition", 0], ["At each quarterly update", 0]],
    rows=[
        ["Tourism Economics, Anaheim Travel Forecast", "Quarterly", "Sept. 2026", "Replaced with the newest forecast"],
        ["Tourism Economics, Economic Impact of Visitors", "Annual (spring)", "Calendar 2025 (pub. 2026)", "Replaced when the new year is published"],
        ["LARC Market Intelligence Reports; quarterly forecasts", "Monthly; quarterly", "Jan. to Sept. 2026", "Latest month and forecast added"],
        ["STR daily data (Visit Anaheim hotel sets)", "Weekly or monthly", "Jan. 1 to Oct. 3, 2026", "New export pulled through the latest date"],
        ["CoStar reports and export", "Weekly or monthly", "Through Aug. 2026", "New reports and export pulled"],
        ["Azira via Symphony", "Monthly", "Jan. to Aug. 2026", "New period pulled"],
        ["Visa Destination Insights via Symphony", "Weekly or monthly", "Aug. 2026", "Latest month pulled"],
        ["OCTA, Amtrak, Metrolink", "When a new schedule or fact sheet is published", "Aug. to Nov. 2026; 2018 to 2024; FY26 Q2", "Updated only if a new one is out"],
        ["Datafy, U.S. BTS, California transit snapshots, City and OCVIBE public sources", "As released", "See the source register", "Kept at their dated values until a new release is received"],
    ],
    src=SCHED_SRC + "; Visit Anaheim BI source register (Oct. 12, 2026)",
)

# Planned sources (added Oct. 14, 2026, per John Picou). Not in this edition: no figures are shown until the data is received,
# checked and cleared for sharing. Each is added at the next quarterly update after it arrives.
PLANNED = dict(
    title="Planned data sources (not in this edition)",
    cols=[["Source", 0], ["What it would add", 0], ["How it would tie in", 0], ["Status", 0]],
    rows=[
        ["Ticketmaster ticketing data, Honda Center (from OCVIBE)",
         "Tickets sold by event and ticket-buyer home ZIP code",
         "Shows how far event audiences travel; matched to STR nights and Visa spending on event dates; feeds Who visits and Hotel market",
         "To request from OCVIBE through a data-sharing agreement; summaries only"],
        ["Placer.ai foot-traffic data",
         "Visits, visitor home areas, dwell time and repeat visits at OCVIBE venues and the OCVIBE area",
         "Compared with Azira for District 5; tracks the OCVIBE area as venues open; feeds Who visits and Getting here",
         "To source; license holder to be confirmed; summaries only"],
    ],
    src="Visit Anaheim BI, data plan (Oct. 14, 2026)",
)

GLOSSARY = [["Quarterly update", f"The quarterly refresh of this report, after Tourism Economics' quarterly forecast or sooner when new data arrives. Only figures with a new published value change."]]
METHOD = [["Quarterly update", "Quarterly because Tourism Economics, the core of the report, delivers quarterly; weekly and monthly sources (STR, CoStar, Visa, Azira) are pulled at the same time so all figures share one as-of date. Each quarter, BI finds the newest file from each source, replaces only figures with a new published or measured value (with the new period and publication date), checks every number against its source, and republishes the dashboard, deck and data tables. Sources with nothing new keep their dated figures.", SCHED_SRC]]

SCHEDULE = dict(last=LAST_S, next=None, line=LINE, lede=LEDE, details=DETAILS, table=TABLE, planned=PLANNED, contact=CONTACT,
                months="15th of January, April, July and October", src=SCHED_SRC)
