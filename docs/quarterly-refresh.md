# Quarterly refresh runbook

Set up Oct. 13, 2026 at John Picou's request. Tourism Economics (TE) delivers its Anaheim Travel Forecast each quarter, so OC Vibe Insights is refreshed each quarter. A scheduled task named "OC Vibe Insights quarterly refresh" runs this runbook on the 15th of January, April, July and October at about 9 a.m. Pacific. Anyone can also run it by hand.

The refresh only uses measured or published data. If a source has nothing new, the run keeps the current figures and says so. It never estimates a missing figure.

## 1. Find the new data (read only)

Search in this order, newest first, and note the file name, date and location of every file used:

| Source | What to look for | Where |
|---|---|---|
| Tourism Economics | "Anaheim Travel Forecast - MM-YYYY" PDF (quarterly); "Economic Impact of Visitors" (annual, spring) | OC Vibe (Reporting) Claude project files; BI SharePoint (`data.py` `SP`); Outlook attachments from Tourism Economics |
| LARC | "MM Month YYYY Market Intelligence Report" PDF (monthly); "Visit Anaheim Forecasts Combined for Distro nQ-YY" workbook (quarterly) | Project files; SharePoint; Outlook |
| STR | "Daily Data" export for the Visit Anaheim hotel sets | BI OneDrive folder; project files |
| CoStar | Orange County market, Disneyland submarket and capital markets reports; "DataExport" workbook | Project files; SharePoint |
| Azira / Visa (Symphony) | POI analysis (District 5), domestic visitors, media attribution, Visa visitor type and international card activity | Project files; SharePoint |
| OCTA, Amtrak, Metrolink | Only if a new schedule period or fact sheet is published | Public sites (visitanaheim.org first, then the agency) |

Licensed raw exports (STR, CoStar) go into `pipeline/files/licensed/` on the OneDrive copy only. They are never committed (`.gitignore`).

## 2. Update the inputs

| Module | What holds what |
|---|---|
| `pipeline/data.py` | `SRC` source labels and dates; `EI` (TE Economic Impact); `YEARS`, `ANA_VIS`, `ANA_SP`, `ANA_SP_YOY`, `GG_*`, `Q` (TE quarterly), `ANA_Q`, `INTL`; `LARC`, `LARC_Q`, `LARC_REV`, `SET`, `CONV_PACE`, `CPI`; `CS_*` (CoStar reports); `POI`/`GEO`/`MED*` (Azira); `ADT`, `TRANSIT` |
| `pipeline/newdata.py` | Reads the STR and CoStar exports by file name (`F + "STR_Daily_Data_8.xlsx"`, `"CoStar_DataExport_17.xlsx"`); `VISA*`, `AMTRAK`, `METRO` |
| `pipeline/ocv_whole.py` | Reads the STR export for the hotel calendar |
| Section text | `facts_only.py`, `ocv_whole.py`, `calcs.py`, `newsroom.py` (nut graphs, detail cards, reading-order bridges), `infographics.py` |

Rules:
- Change only figures that have a new published value; update the period and publication date with each one.
- Update any sentence whose number changed (headlines, ledes, nut graphs, detail cards, infographics, compare and contrast). The number-trace check fails if text cites a number that is no longer in a table.
- Keep Tourism Economics figures as City of Anaheim totals; never allocate them to OC Vibe.
- House style: no em dashes, AP style, attribution on every fact, no first person, no opinion.

## 3. Rebuild and check

From the repository root (Python 3.11+, Node 18+; in a Claude session set `PPTX_THEME_SCRIPT` to the pptx skill's `apply_theme.js`):

1. `npm run deck`, then `npm run page`.
2. `npm run validate`, writing to `pipeline/computations/validation-NNN` (next number). Every check must pass. A failing check is fixed, not skipped.
3. `npm run shots` and look at 1920, 1440, 1024, 768 and 390 px: no horizontal scroll, no clipped text.
4. Run a data-quality audit on what changed (sources, periods, units, quarter-over-quarter jumps over 15%) and list the issues before publishing.

## 4. Publish

1. Republish `pipeline/oc-vibe-insights.html` to the claude.ai artifact (same URL; README lists it).
2. Commit on the OneDrive copy: `Quarterly refresh: <quarter> data (validation-NNN)`. Pushing to GitHub needs John's sign-in, so the run tells him to run `git push`; Vercel then redeploys.
3. Add a line to `docs/activity-log.md` and the project doc "OC Vibe Insights - build notes and activity log".

## 5. Report and approvals

- Send John a short summary: sources found (file, date), figures that changed (old → new, with source), sources with nothing new, check results, and anything that needs a decision.
- Draft (do not create) a BIREPORTS verification ticket for John's review. Create it only after he says yes.
- External sharing still needs the approvals in the README (TE draft clearance, LARC consent, licensed data as summaries only).
