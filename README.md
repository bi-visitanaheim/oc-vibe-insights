# OC Vibe Insights

A Visit Anaheim Business Intelligence dashboard and matching PowerPoint deck for OC Vibe (Jira BIREPORTS-966). It shows where Anaheim's visitor economy and the OC Vibe area stand today, using measured or published data only.

| | |
|---|---|
| **Owner** | Visit Anaheim Business Intelligence (John Picou, jpicou@visitanaheim.org) |
| **Audience** | OC Vibe (external partner) and Visit Anaheim staff |
| **Dashboard** | claude.ai artifact, version 19 (private until shared from its Share menu): https://claude.ai/artifact/QVGs5a6v3z4meGtc2XcZPB |
| **Repository** | GitHub `bi-visitanaheim/oc-vibe-insights` (public) |
| **Website** | https://oc-vibe-insights.vercel.app (public). Vercel project `oc-vibe-insights`, team "Visit Anaheim's projects" (Hobby plan). Deployment-specific URLs require a Vercel login |
| **Deck** | `OC_Vibe_Insights.pptx`, 94 slides, VA Branded; each section opens with a news report slide, a details slide and an "At a glance" infographic slide |
| **Data through** | Sept. 2026 (STR through Oct. 3, 2026; CoStar and Visa through Aug. 2026) |
| **Last updated** | Oct. 13, 2026 |

---

## 1. Reporting rules this app follows

1. **Facts only.** Every number is measured or published by a named source. The app has no Visit Anaheim BI estimate of OC Vibe's impact, because no OC Vibe attendance, ticketing or hotel data exists yet.
2. **Tourism Economics covers the City of Anaheim only.** Its totals are never allocated to OC Vibe.
3. **Years are labeled.** Calendar 2025 results (published 2026) appear beside Tourism Economics' 2026 forecast, and each is labeled.
4. **Every calculated number shows its breakdown,** for example $6.832B ÷ 26.5M visitors = $258.
5. **Every major point carries its source and date.**
6. **Every section is written as a broadsheet news report, then analysis.** The news report follows the inverted pyramid: dateline and lede, a nut graph ("Why it matters"), and six announcement-style detail cards (who, what, when, where, why and how). Attribution on every fact, no first person, AP style. No editorial or opinion content.
7. **Compare and contrast is covered for each section:** growth, opportunity, quick win, early hurdle, pitfall and explanation. Every hurdle and pitfall comes with a solution.
8. **The appendix has the glossary, methods and formulas.**
9. **Internal checks stay internal.** Validation results are not shown in the report.
10. **New customer-facing sections are confirmed with John Picou before publishing.**
11. **House writing style:** no em dashes; PhD-level analysis and research rigor, written so the audience can digest and defend it.
12. **Anaheim as a whole.** The report looks holistically at Anaheim; it has no calculator for individual events or for OC Vibe's own figures.

---

## 2. What the dashboard contains

The **Overview** is the main announcement, a facts-only BI Pulse release that can be copied with formatting. It is followed by questions and short answers.

| Tab | Question it answers | Main sources |
|---|---|---|
| Anaheim and OC Vibe today | Where do Anaheim's visitor economy and the OC Vibe area stand today? | Tourism Economics (2025; 2026 forecast), Datafy, Azira |
| Who visits | Who visits District 5 and the OC Vibe area? | Azira, Datafy, Visa |
| Visitor spending | How much does each visitor spend, and how is that changing? | Tourism Economics, Visa |
| Jobs and economy | What does the visitor economy support? | Tourism Economics |
| Hotel market | How are hotels performing, and when is there room? | CoStar, STR |
| One more night | What is one more night per visitor worth? | Visit Anaheim Extra Night study (TE, Azira) |
| Getting here | How do people reach OC Vibe? | OCTA, Amtrak, Metrolink, BTS, California transit snapshots |
| Marketing reach | Does Visit Anaheim's marketing bring visitors? | Azira media attribution |
| Market outlook | What in the market will affect OC Vibe? | LARC, public OC Vibe sources |
| Appendix | What do the terms, methods and formulas mean? | Visit Anaheim BI |
| Sources | Where does every number come from? | Source register (29 entries), data notes, recommendations |

Sections run in reading order; each answers the question the previous one raises, and ends with an "Up next" link that explains why the next topic follows.

Each section reads like a newspaper story, in this order:

**News report** (objective, inverted pyramid)
1. Kicker ("News report"), headline, dek and byline.
2. The lede: dateline (ANAHEIM, Calif. (Oct. 13, 2026):), the key insight, its key number and source.
3. Why it matters: the nut graph.
4. At a glance: one or two data infographics (see Features).
5. By the numbers (KPI cards).
6. How the key insight is calculated.
7. The details: six announcement-style data cards (who, what, when, where, why and how), each with a figure, its label or calculation, the detail and the source with its date.

**Analysis** (feature)
8. The question, featured charts and the main table.
9. What it means for OC Vibe: "What it enhances" and "What OC Vibe needs", tagged by topic, not by role.
10. Compare and contrast.
11. A collapsed panel, "More data and notes".
12. Up next.

### Features

- **Data infographics ("At a glance").** Built only from figures already in each section, each with its source, date and calculations: an economy chain (visitors, spending, impact, jobs, taxes), waffles (of every 100 District 5 visitors), an itemized visitor receipt with an "every $1" bar, a jobs pictogram, hotel occupancy towers by night, share bars (new hotel supply; day vs. overnight visitors), an ARTIC departures board, an impressions-to-visits funnel, and Anaheim vs. U.S. bars. On screen, numbers count up and bars grow once on entrance; off under reduced motion and in print or PDF.
- **Full-width layout.** Headlines and deks run the full page width; blocks stack full width with no side columns; stat rows stretch to fill; the overview release flows in three newspaper columns. Checked at 1920, 1440, 1024, 768 and 390 px.
- **Value tooltips.** Hover over or tab to any bar, column, line point, heatmap cell or overview bar to see its value. The selected mark is highlighted.
- **Export.** Choose sections, then export as PDF, CSV or PowerPoint. PowerPoint gives the title slide plus the slides for the chosen sections (all sections gives the full deck); it is assembled in the browser from the full deck (`pipeline/pptx_subset.js`, with JSZip 3.10.1, MIT), so slides stay editable. The deck can also be downloaded from the page.
- **Views and navigation:**
  - one page at a time or all pages; links, tabs and "Up next" land each section just below the sticky section bar;
  - full screen;
  - light and dark themes;
  - mobile layout;
  - entrance motion only, turned off for viewers who choose reduced motion.

---

## 3. Data sources

The source register on the Sources page lists each source's document, period covered, publication or pull date, use, and how BI checked it.

| Source | Period | Used for |
|---|---|---|
| Tourism Economics, Economic Impact of Visitors | Calendar 2025 (pub. 2026) | Visitors, spending, impact, jobs, taxes, spending by category |
| Tourism Economics, Anaheim Travel Forecast | Sept. 2026 | 2026–2028 forecast, Q2 2026 |
| STR daily data (Visit Anaheim hotel sets) | Jan. 1–Oct. 3, 2026 | Night-of-week and monthly occupancy, group share |
| CoStar reports and export | Through Aug. 2026 | Submarket performance, pipeline, investment |
| LARC Market Intelligence Reports | Jan.–Sept. 2026 | Market outlook, convention pace, RevPAR |
| Azira via Symphony | Jan.–Aug. 2026 | District 5 profile, origins, media attribution |
| Datafy | Calendar 2024 | OC Vibe area share of Anaheim visitor days (5.2%) |
| Visa Destination Insights via Symphony | Aug. 2026 | Card spending, origin markets |
| OCTA (traffic map, bus schedules) | Aug.–Nov. 2026 | Traffic counts, ARTIC bus service |
| Amtrak (Rail Passengers Association); Metrolink | 2018–2024; FY26 Q2 | Rail at ARTIC |
| California's transit systems data snapshots | 2003–2017 | Orange County transit staff, costs, riders, fleet |
| U.S. BTS | 2019–2025 | Travel costs, commute mode |
| City of Anaheim; OCVIBE; OCBJ; PR Newswire; BizBash | 2024–2026 | OC Vibe phasing, venues, published figures |
| Visit Anaheim Extra Night study; Simpleview TID bookings | 2025 inputs; Jan. 2025 export | One more night; group bookings |

---

## 4. Repository layout

| Path | What it holds |
|---|---|
| `pipeline/` | Content modules (Python), deck builder (`deck_head.js`, `deck_body.js`), page assembler (`build.py`, `app.js`) |
| `pipeline/files/` | California transit snapshot CSVs (public) |
| `pipeline/files/gtfs/` | OCTA GTFS schedule files used by the ARTIC bus recount (public; `stop_times` is gzipped) |
| `pipeline/files/licensed/` | CoStar and STR raw exports. **Not in Git** (the repository is public); copy them from the BI OneDrive folder before rebuilding |
| `pipeline/assets/` | VA Branded CSS and logo, ADT image |
| `pipeline/checks/`, `pipeline/computations/` | Internal validation script, contract and results (not shown in the report) |
| `public/` | What Vercel serves: `index.html`, `OC_Vibe_Insights.pptx`, `robots.txt` |
| `pipeline/infographics.py` | The "At a glance" infographic data for each section (attached after newsroom) |
| `pipeline/newsroom.py` | News report structure: nut graphs, detail cards, reading order, bridges and the em-dash rule (attached last) |
| `pipeline/pptx_subset.js` | PowerPoint export: keeps the chosen deck sections and removes the rest cleanly |
| `scripts/make_public.py` | Copies the built page and deck into `public/` |
| `docs/activity-log.md` | Build notes and the change log |
| `docs/quarterly-refresh.md` | Runbook for the quarterly data refresh |
| `vercel.json` | Static site settings: no build on Vercel, serve `public/`, no search indexing |

## 5. How to rebuild

Requirements: Python 3.11+ (`pip install -r requirements.txt`) and Node 18+ (`npm install`).

1. Copy `STR_Daily_Data_8.xlsx` and `CoStar_DataExport_17.xlsx` into `pipeline/files/licensed/`.
2. **Content:** `content.py` builds the sections and attaches these modules in order:
   1. `ocv_content.py`
   2. `new_content.py`
   3. `views_valid.py`
   4. `logic_content.py` (who/what/when/where/why/how, compare and contrast, appendix)
   5. `roles_content.py` (California transit snapshots and the source-register additions)
   6. `ocv_whole.py` ("What it means for OC Vibe", main announcement, hotel calendar, public facts)
   7. `calcs.py` (calculation breakdowns)
   8. `feature.py` (featured charts)
   9. `facts_only.py` (removes estimates and rebuilds the "Anaheim and OC Vibe today" section)
   10. `newsroom.py` (news report structure, reading order, house style)
   11. `infographics.py` (last step: "At a glance" infographics)
3. **Deck:** run `npm run deck`.
   - This writes `pipeline/deck_data.json`, then `pipeline/OC_Vibe_Insights.pptx`.
   - The VA theme step uses the pptx skill's `apply_theme.js`, which is not stored in this repository. Set `PPTX_THEME_SCRIPT` to its path to apply it. Without it, the deck is written unthemed and a warning is shown.
4. **Page:** run `npm run page`.
   - This writes `pipeline/oc-vibe-insights.html` (deck embedded) and copies the page and deck into `public/`.
   - Build the deck first.
5. **Check:** run `npm run shots` for screenshots and the overflow check, and `npm run validate` for the internal validation.
6. **Publish:**
   - **Website:** commit and push to `main`. Vercel deploys `public/` automatically.
   - **claude.ai artifact:** republish `pipeline/oc-vibe-insights.html` to the same artifact. The artifact keeps its declared capabilities (db, downloads and user); db is no longer used now that the calculator is removed.

**Internal validation (not shown in the report).**

- `pipeline/checks/validate_ocvibe.py` runs with `pipeline/checks/contract.json`.
- The latest recorded run is `pipeline/computations/validation-012` (Oct. 13, 2026): 50 of 50 checks passed, including the newsroom and infographic checks. The suite was re-run from this repository with the same result.
- The checks include:
  - every number in the report text traces to a table or data note;
  - no estimate wording remains;
  - the transit files reconcile;
  - every section is a complete news report (dateline, lede, nut graph, six sourced detail cards);
  - no em dashes, AP-style dates and no first person in news reports;
  - the reading order links each section to the next;
  - every infographic has a dated source and shows its calculations, and the visitor receipt adds up.

`impact.py` still holds the earlier scenario model for reference. `facts_only.py` keeps all of its output out of the report.

### Website vs. claude.ai artifact

| Feature | claude.ai artifact | Vercel website |
|---|---|---|
| Who can open it | People it is shared with | Anyone with the link to oc-vibe-insights.vercel.app |
| PDF, CSV and PowerPoint exports | Yes | Yes |

---

### Quarterly refresh

A scheduled task, "OC Vibe Insights quarterly refresh," runs on the 15th of January, April, July and October at about 9 a.m. Pacific, after Tourism Economics' quarterly forecast arrives. It looks for new TE, LARC, STR, CoStar, Azira and Visa files, updates only figures with a new published value, rebuilds the dashboard and deck, runs the checks, republishes the artifact, commits on the OneDrive copy and sends John a summary. John then runs `git push` so Vercel redeploys. Steps: `docs/quarterly-refresh.md`.

## 6. Data notes to keep in mind

- **Concert hall capacity** differs by source: 5,000 (OCVIBE, Mar. 2026) vs. 5,613 (City of Anaheim, 2026). Confirm with OC Vibe.
- **STR vs. CoStar:** they use different hotel sets. Compare trends, not levels.
- **Azira, Datafy and Visa** count visitors differently. Compare within each source.
- **California transit snapshots:**
  - The data ends in 2017.
  - Dollars are nominal.
  - Laguna Beach outliers are flagged.
  - Snapshots 3 and 4 were duplicates.
- **Extra Night study:** it is a "what if every visitor stayed one more night" calculation that holds spending per day constant.
- **OC Vibe cost and timeline** differ by source: CoStar $4B and 2028; LARC $5B and 2033; City $4B, through about 2030.

---

## 7. Approvals before sharing outside Visit Anaheim

- **Tourism Economics 2025 Economic Impact:** confirm it is cleared for distribution.
- **LARC reports:** consent is required.
- **CoStar, STR and Visa:** licensed data. Share summaries, not raw exports.
- **The website and repository are public** (decision by John Picou, Oct. 13, 2026). Licensed raw exports (CoStar, STR) are excluded by `.gitignore` and are never pushed.
- **The dashboard:** private until shared.

---

## 8. Open items

- Confirm the concert hall capacity with OC Vibe.
- Set up a quarterly data exchange with OC Vibe for ticket-buyer ZIP codes and hotel results once venues open (concert hall early 2027; first hotel 2028).
- Get post-2017 Orange County transit ridership, if available.
- Get Tourism Economics transportation impact data (not yet received).
- Confirm California 2025 figures against Visit California's primary report.

The full change history is in `docs/activity-log.md` and the project doc "OC Vibe Insights - build notes and activity log".
