# OC Vibe Insights

A Visit Anaheim Business Intelligence dashboard and matching PowerPoint deck for OC Vibe (Jira BIREPORTS-966). It shows where Anaheim's visitor economy and the OC Vibe area stand today, using measured or published data only.

| | |
|---|---|
| **Owner** | Visit Anaheim Business Intelligence (John Picou, jpicou@visitanaheim.org) |
| **Audience** | OC Vibe (external partner) and Visit Anaheim staff |
| **Dashboard** | claude.ai artifact, version 25 (private until shared from its Share menu): https://claude.ai/artifact/QVGs5a6v3z4meGtc2XcZPB |
| **Repository** | GitHub `bi-visitanaheim/oc-vibe-insights` (public) |
| **Website** | https://oc-vibe-insights.vercel.app (public). Vercel project `oc-vibe-insights`, team "Visit Anaheim's projects" (Hobby plan). Deployment-specific URLs require a Vercel login |
| **Deck** | `OC_Vibe_Insights.pptx`, 116 slides, VA Branded; a "Questions answered" section (the four core questions with detail slides) after the introduction and a "Reports and data library" section before next steps; key takeaways and "How this report is updated" slides up front, and each section opens with a news report slide, a details slide and an "At a glance" infographic slide; three map slides |
| **Questions deck** | `OC_Vibe_Questions_Answered.pptx`, 32 slides, VA Branded: average spend, one more night, transportation impact and District 5 for Anaheim, Orange County and the U.S., plus 14 more questions and the file list |
| **Library** | `public/library/`: 45 source files (73 MB with the report files), each viewable and downloadable in the app |
| **Data through** | Sept. 2026 (STR through Oct. 3, 2026; CoStar and Visa through Aug. 2026) |
| **Updated** | Quarterly, on the 15th of January, April, July and October (data last updated Oct. 13, 2026; next scheduled update Oct. 15, 2026) |

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

The **Overview** opens with **Key takeaways**: one card per section with its headline metric in bold, what it means, the period and a link to the section. Below them, an "Updated quarterly" bar gives the last and next update dates and links to the full schedule. Then comes the main announcement, a facts-only BI Pulse release that can be copied with formatting, and the questions and short answers.

| Tab | Question it answers | Main sources |
|---|---|---|
| Questions answered | 21 general questions (average spend, one more night, transportation impact, District 5, jobs, taxes, hotels, outlook), each for Anaheim, Orange County and the U.S. (California where that is the closest published level) | Tourism Economics, Visit California, U.S. Travel Association, BTS, Azira, Datafy, Visa, CoStar, STR, LARC |
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
| Reports and data library | Where can I read the full reports and data? | Every source file, as received (45 files), plus linked public sources |
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
8. The question, maps (where the data is geographic), featured charts and the main table.
9. What it means for OC Vibe: "What it enhances" and "What OC Vibe needs", tagged by topic, not by role.
10. Compare and contrast.
11. "More data and notes": a highlighted callout with a count of the extra charts and tables and a reminder to read the notes and caveats before quoting a number (opens automatically in print and PDF).
12. Up next: a full-width band with the section number, the next headline, why it follows and a Continue button.

### Features

- **Questions answered (Oct. 14, 2026).** A searchable page of general questions with topic filters. The four core questions (average spend, one more night, transportation impact, District 5) open first. Each answer has a short summary with the key number, a table of figures for Anaheim, Orange County and the U.S. (each with its source and date), a visual, "How it is calculated", "Keep in mind", links to the library files that answer it, linked public sources and a "Go deeper" link to the full section. Deep links: `#ask/<question id>`. No individuals are named; the questions are general.
- **Reports and data library (Oct. 14, 2026).** Every report and data file used to build the app, grouped by topic (economic impact, quarterly results, one more night, who visits and District 5, marketing attribution, hotels, market outlook, getting here, destination program, this report). Each file shows its publisher, type, period covered, publication date, pages and size, a summary, the questions it answers and the sections that use it, with Open and Download buttons, search and topic filters. Deep links: `#library/<file id>`. The overview opens with two cards that lead to these pages.
- **Select any value (Oct. 15, 2026).** Click, tap or press Enter on any chart mark (including the G2 canvas charts), table cell, key figure, bold number or highlighted value in the text to open a small data card: the value, what it measures, the chart or table it comes from, the period and the source, with "Copy with source", "Open the source file" (the matching file in the Reports and data library) and, for headline figures, "Show the data". On phones it opens as a bottom sheet. Hover tooltips are unchanged.
- **Name style.** The organization is always written "Visit Anaheim" (web addresses and emails stay lowercase); the validation suite checks the app and both decks.
- **One Export panel (Oct. 15, 2026).** Every file comes from the header's Export button (the Sources page and side menu open the same panel). It reads in numbered steps with a live preview and one Save button:
  1. What do you want? Full report (PDF or PowerPoint, the deck's pages for the chosen sections), Doc (new: Word, web page or Markdown brief), Slides (new: a short PowerPoint built from the choices, with editable charts, PptxGenJS 4.0.1 inlined), Design (new: PNG, PDF or SVG one-page graphic; social, letter or widescreen; teal, dark or light), Motion (beta: 1920 × 1080 video or still image), Data (Excel or CSV), Share link.
  2. Which sections? Chips plus All, Current page, the four core questions and Clear.
  3. Areas and details (Doc, Slides, Design, Motion): areas, title, subtitle, charts per section, design size and colors, and a folded list of key figures.
  4. Preview, live.
  Figures are used exactly as published, with period and source; nothing is recalculated. Choices are remembered per viewer. The separate Make page, the Dashboard output and the extra download buttons were removed so there is one place to get files.
- **Each section opens with its question and short answer** at the top of "The story", with the key number and source; the Overview no longer repeats them in a separate list. Appendix and Sources are the last two pages, after the Reports and data library.
- **Interactive charts and diagrams (Oct. 14, 2026).** All inlined, pinned and offline; colors follow the VA palette in light and dark mode; every visual keeps a text alternative (aria label, data table fold or written calculation).
  - AntV G2 5.4.8: section bar, column, line, heatmap and stacked charts and the overview growth bars, drawn on canvas when they scroll into view, with tooltips.
  - AntV T8 0.3.1: section ledes, nut paragraphs and question answers mark values, percent changes and periods; changes are colored up or down.
  - AntV Infographic 0.2.20: the one-more-night steps (with the calculation line), the quarterly update timeline and the library topic cards. Icons are Material Design Icons (@mdi/js 7.4.47) embedded in the page.
  - AntV X6 3.1.8: how visitor spending becomes economic impact (Anaheim, Garden Grove, Orange County toggle) and the data lineage graph on the Sources page.
  - D3 7.9.0: "How Anaheim compares" dot matrix on Questions answered (each row opens its answer) and spending treemaps for Anaheim and Orange County on Visitor spending. Deterministic SVG: fixed layout, sorted data, no randomness or animation.
  - On phones, diagrams keep a readable minimum width inside a frame that swipes sideways.
  - GPT-Vis guided chart-type choice; charts render through G2. The online icon search and chart-image services named by the skills are blocked by the network allowlist and are not used.
- **Data infographics ("At a glance").** Built only from figures already in each section, each with its source, date and calculations: an economy chain (visitors, spending, impact, jobs, taxes), waffles (of every 100 District 5 visitors), an itemized visitor receipt with an "every $1" bar, a jobs pictogram, hotel occupancy towers by night, share bars (new hotel supply; day vs. overnight visitors), an ARTIC departures board, an impressions-to-visits funnel, and Anaheim vs. U.S. bars. On screen, numbers count up and bars grow once on entrance; off under reduced motion and in print or PDF.
- **Maps for geographic data.** Who visits: a U.S. map shading the top origin states (Azira, District 5, Jan. 1 to May 31, 2026) with circles for the top metro areas. Visitor spending: a U.S. map of card spending by cardholder home metro and a world map of international card spending by country (Visa Destination Insights, Aug. 2026). Every value comes from a table in the section; circle area shows the value; Anaheim is marked; the legend ranks the top eight in bold. Boundaries: U.S. Census Bureau cartographic boundaries (us-atlas 3.0.1, Albers USA) and Natural Earth 1:110m (world-atlas 2.0.2). Geometry is built once by `npm run maps` (`pipeline/maps_geo.js` to `maps_geo.json`); `map_svg.js` draws the maps on the page, and `maps_render.js` renders them as PNGs for the deck.
- **Update schedule.** The header, overview bar, footer, release, Excel About sheet and deck title show "Updated quarterly" with the last and next update dates. The Sources page opens with "How this report is updated": who, what, when, where, why and how cards, a table of when each source publishes and what each quarterly update does with it, and the planned data sources (Ticketmaster data from Honda Center; Placer.ai), which show no figures until the data is received, checked and cleared. Dates and text live in `pipeline/schedule.py`; the next date is computed from `LAST_UPDATE`.
- **Key takeaways and bold statistics.** The overview's takeaway cards and a matching deck slide; key numbers are bold in the text.
- **Full-width layout.** Headlines and deks run the full page width; blocks stack full width with no side columns; stat rows stretch to fill; the overview release flows in three newspaper columns. Checked at 1920, 1440, 1024, 768 and 390 px.
- **Value tooltips.** Hover over or tab to any bar, column, line point, heatmap cell or overview bar to see its value. The selected mark is highlighted.
- **Export.** Choose sections, then export as PDF, PowerPoint, Excel, CSV or a share link. PDF and PowerPoint use the same cut: the title page plus the deck pages for the chosen sections (all sections gives the full 101-page report). The PDF is the deck rendered at build time (`pipeline/deck_pdf.py`, LibreOffice), cut in the browser with `pipeline/pdf_subset.js` (pdf-lib 1.17.1, MIT, inlined) and renumbered "n of N"; it needs no network, so it works on the claude.ai dashboard as well as the website. Excel gives a real .xlsx with an About sheet and one sheet per section (numbers stored as numbers, percents and dollars formatted, columns fitted to each table, long text wrapped, a source row under every table). The share link copies https://oc-vibe-insights.vercel.app/ (with the section anchor when one section is chosen) and opens the device share sheet where available. PowerPoint gives the title slide plus the slides for the chosen sections (all sections gives the full deck); it is assembled in the browser from the full deck (`pipeline/pptx_subset.js`, with JSZip 3.10.1, MIT), so slides stay editable. The deck can also be downloaded from the page.
- **Views and navigation:**
  - page by page (default): every section is split into separate pages, one segment each (The story, At a glance, The data, What it means, Behind the numbers; Overview, Questions answered, the library and Sources the same way), with a sticky Back/Next bar, segment chips as page tabs, arrow keys, deep links (#section/pN), and long lists shown one topic at a time; "Scroll all" shows everything in one scroll and print shows every page;
  - full screen;
  - light and dark themes;
  - mobile layout;
  - entrance motion only, turned off for viewers who choose reduced motion.
- **Contact.** The footer reads "Contact us: bi@visitanaheim.org" (mailto link).

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
| `public/` | What Vercel serves: `index.html`, `OC_Vibe_Insights.pptx`, `OC_Vibe_Insights.pdf`, `robots.txt` |
| `pipeline/infographics.py` | The "At a glance" infographic data for each section (attached after newsroom) |
| `pipeline/newsroom.py` | News report structure: nut graphs, detail cards, reading order, bridges and the em-dash rule (attached last) |
| `pipeline/schedule.py` | Update schedule: last and next update dates, the who/what/when/where/why/how cards, the source cadence table and planned sources |
| `pipeline/maps.py` | Map specs for geographic data, built from the section tables (attached after infographics) |
| `pipeline/maps_geo.js`, `maps_geo.json` | Map geometry and point positions (U.S. states, world countries, metro and country points) |
| `pipeline/map_svg.js`, `maps_render.js` | Map drawing shared by the page and Node; PNG rendering for the deck |
| `pipeline/deck_pdf.py`, `pdf_subset.js` | Report PDF: renders the deck to PDF and maps sections to pages; cuts the PDF to the chosen sections in the browser |
| `pipeline/pptx_subset.js` | PowerPoint export: keeps the chosen deck sections and removes the rest cleanly |
| `scripts/make_public.py` | Copies the built page and decks into `public/` |
| `scripts/stage_library.py` | Copies the original source files into `public/library/` under readable names; Visit Anaheim-owned Office files get neutral document properties, PDFs get the publisher as author, and no personal names remain |
| `pipeline/library.py` | Library list: every file with publisher, period, publication date, summary, geography, sections that use it; public source links |
| `pipeline/ask.py` | Questions answered: data (Tourism Economics transportation industry rows, Visit California 2025p, U.S. Travel Spring 2026), the 21 questions, and two new section tables (average spend by geography; economic impact of visitor transportation) |
| `pipeline/ask_app.js` | Renders the Questions answered and library pages (search, filters, visuals, downloads, deep links) |
| `pipeline/antv_app.js` | AntV layer: G2 chart specs and lazy mounting, T8 narrative markup, Infographic syntax, X6 impact flow and data lineage |
| `pipeline/detail_app.js` | Select any value: the data card for chart marks, table cells, key figures and bold numbers |
| `pipeline/make_app.js`, `pipeline/make.css` | The Export panel: full report, Doc, Slides, Design, Motion, Data and Share link, with live previews and saving |
| `pipeline/d3_app.js` | D3 layer: comparison dot matrix and spending treemaps |
| `pipeline/qa_slides.js`, `qa_body.js` | Question and library slides shared by both decks; the focused questions deck |
| `public/library/` | The source files served by the website and the claude.ai artifact |
| `docs/activity-log.md` | Build notes and the change log |
| `docs/quarterly-refresh.md` | Runbook for the quarterly data refresh |
| `vercel.json` | Static site settings: no build on Vercel, serve `public/`, no search indexing |

## 5. How to rebuild

Requirements: Python 3.11+ (`pip install -r requirements.txt`), Node 18+ (`npm install`), and LibreOffice (`soffice`) plus poppler (`pdfinfo`) for the report PDF.

1. Copy `STR_Daily_Data_8.xlsx` and `CoStar_DataExport_17.xlsx` into `pipeline/files/licensed/`. When source files change, put the originals in one folder and run `python3 scripts/stage_library.py <folder>` (names are mapped in `pipeline/library.py`).
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
   11. `infographics.py` ("At a glance" infographics)
   12. `maps.py` (maps for geographic data)
   13. `ask.py` (last step: questions answered, the two new tables, and the library list)
3. **Deck:** run `npm run deck`.
   - This writes `pipeline/deck_data.json`, renders the map PNGs (`pipeline/map_*.png`), writes `pipeline/OC_Vibe_Insights.pptx`, then renders it to `pipeline/OC_Vibe_Insights.pdf` with the section page map `pipeline/deck_pages.json`.
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
- The latest recorded run is `pipeline/computations/validation-021` (Oct. 15, 2026): 66 of 66 checks passed, including the Export panel checks and two new ones ("Visit Anaheim" written the same way everywhere in the app and decks; every chart mark, table cell, key figure and bold number opens a data card). The suite was re-run from this repository with the same result.
- The checks include:
  - every number in the report text traces to a table or data note;
  - no estimate wording remains;
  - the transit files reconcile;
  - every section is a complete news report (dateline, lede, nut graph, six sourced detail cards);
  - no em dashes, AP-style dates and no first person in news reports;
  - the reading order links each section to the next;
  - every infographic has a dated source and shows its calculations, and the visitor receipt adds up;
  - every mapped value traces to a report table, has a map position, and each map has a dated source;
  - the next update date is the first 15th of January, April, July or October after the last update and is shown on the page, and planned sources show no figures;
  - the report PDF has one page per deck slide and every page belongs to exactly one deck section.

`impact.py` still holds the earlier scenario model for reference. `facts_only.py` keeps all of its output out of the report.

### Website vs. claude.ai artifact

| Feature | claude.ai artifact | Vercel website |
|---|---|---|
| Who can open it | People it is shared with | Anyone with the link to oc-vibe-insights.vercel.app |
| PDF, PowerPoint, Excel, CSV and share-link exports | Yes | Yes (the share link always points to the website) |

---

### Quarterly refresh

The report is updated quarterly because Tourism Economics data, the core of the report, arrives each quarter. STR, CoStar and Visa are available weekly or monthly and Azira monthly; they are pulled at the same time so every figure in an edition shares one as-of date. A scheduled task, "OC Vibe Insights quarterly refresh," runs on the 15th of January, April, July and October at about 9 a.m. Pacific, after Tourism Economics' quarterly forecast arrives. It looks for new TE, LARC, STR, CoStar, Azira and Visa files, updates only figures with a new published value, rebuilds the dashboard and deck, runs the checks, republishes the artifact, commits on the OneDrive copy and sends John a summary. John then runs `git push` so Vercel redeploys. Steps: `docs/quarterly-refresh.md`.

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

- **All source files cleared for public sharing** (decision by John Picou, BI & Technology Director, Oct. 14, 2026): every report and data file used to build the app is posted in the Reports and data library on the website, the repository and the claude.ai artifact. This covers the Tourism Economics 2025 Economic Impact reports (marked client preliminary), LARC reports and forecasts, and CoStar, STR and Visa files.
- **The website and repository are public** (decision by John Picou, Oct. 13, 2026). The licensed raw exports used by the pipeline stay in `pipeline/files/licensed/` (not in Git); the same files are published as received in `public/library/` under the Oct. 14 decision.
- **The dashboard:** private until shared.

---

## 8. Open items

- Confirm the concert hall capacity with OC Vibe.
- Set up a quarterly data exchange with OC Vibe for ticket-buyer ZIP codes and hotel results once venues open (concert hall early 2027; first hotel 2028).
- Planned sources: request Ticketmaster ticketing data for Honda Center from OC Vibe (data-sharing agreement; summaries only) and confirm who holds a Placer.ai license. Add each at the next quarterly update after it arrives.
- Get post-2017 Orange County transit ridership, if available.
- Get Tourism Economics transportation impact data (not yet received). The Questions answered page uses the transportation rows of the 2025 Economic Impact reports until it arrives.
- Add Datafy's original calendar 2024 visitor report (the source of the 5.2% OC Vibe share) to the library; the library holds Datafy's calendar 2025 tables export, which uses a different basis and will be reconciled at the next quarterly update.
- Review OC Vibe's white paper when it is shared, and add any figures it needs to the questions page.
- Confirm California 2025 figures against Visit California's primary report.

The full change history is in `docs/activity-log.md` and the project doc "OC Vibe Insights - build notes and activity log".
