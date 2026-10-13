# OC Vibe Insights: build notes (BIREPORTS-966)

**Requested by:** John Picou · **Audience:** OC Vibe (external partner) · **Prepared:** Oct. 12, 2026 · **Data through:** Sept. 2026 (CoStar and Visa through Aug. 2026; STR through Oct. 3, 2026)

## Deliverables
- Dashboard (claude.ai artifact, private until shared): https://claude.ai/artifact/QVGs5a6v3z4meGtc2XcZPB
  - OC Vibe edition (v13): Overview plus 10 sections (OC Vibe impact, Visitor spending, Jobs and economy, One more night, Getting here, Who visits, Marketing reach, Hotel market, Market outlook, Appendix) and Sources.
  - The Overview is the main announcement: a facts-only BI Pulse release headlined "Anaheim's visitor market is growing into OC Vibe's 2027 opening", with a source and date for every figure.
  - Every section reads like an article, in this order:
    - kicker, headline, dek and the question;
    - key insight with key number, source and date;
    - "The details" (who, what, when, where, why, how);
    - By the numbers;
    - main table;
    - "What it means for OC Vibe";
    - compare and contrast;
    - a collapsed "More data and notes".
  - "What it means for OC Vibe" covers OC Vibe as a whole, in two columns: what it enhances, and what OC Vibe needs.
    - Items are tagged by topic (Strategy, Programming, Events, Hotels, Operations, Marketing, Measurement, Community), not by role, and no one is named.
    - The roles researched (real estate programming and development operations; development programming, research and operations; special events; and the wider team) shaped which data and analysis appear.
  - Compare and contrast now includes an Explanation item and appears as one table: type, point, solution, source and date.
  - New analysis:
    - 2026 hotel calendar by month (STR): weeknight and weekend occupancy, nights at 90%+ and group share. Use it for event and programming planning.
    - OC Vibe in recent public sources.
    - Estimate range and drivers.
  - Removed from the customer version:
    - the Checks and confidence page;
    - all check counts and validation wording;
    - the role bar and role pages.
    Validation stays internal; new customer-facing sections are to be confirmed with John before publishing.
- PowerPoint: OC_Vibe_Insights.pptx (63 slides, VA Branded).
  - Order: main announcement (2 slides), summary of findings, then each section's data slides followed by a "What it means for OC Vibe" slide.
  - Also includes: a hotel calendar slide, an OC Vibe public-sources slide, compare and contrast (5 slides), recommendations, sources, about the data, and the appendix (formulas, glossary, methods, and who/what/when/where/why/how by section).
  - No checks or role slides.

## Jira items and where they are answered
| Jira item | Answer | Source |
|---|---|---|
| OC Vibe impact (OC Vibe's main question) | Base case about $90M a year in new visitor spending (range $36M–$187M); $138M Anaheim economic impact; about 900 jobs; 149K hotel room nights; $4.9M hotel tax | BI scenario model |
| Average spend per visitor | $258 per visitor in 2025; forecast $279 by 2028; Visa spending per card $85 in Aug. 2026 (+4.7%) | TE EI 2025; Travel Forecast Sept. 2026; Visa |
| Q2 TE report | Q2 2026 Anaheim visitor spending +7.8% | Travel Forecast Sept. 2026 |
| Jobs and F&B share | Anaheim 67,817 jobs; F&B share is 16.8% Anaheim, 40.6% Garden Grove, 29.1% OC | TE EI 2025 regional reports |
| Extra night / "One more night" | Extra Night deck headline (lodging, Visit Anaheim methodology). For OC Vibe, each 1% of visitors adding a day is worth $31.5M; each point of Sunday–Monday hotel occupancy is worth ~22,200 room nights and $5.1M | Extra Night deck; TID workbook; STR |
| Transportation | SR-57 275K ADT; 277 weekday OCTA trips at ARTIC (16 after 10 p.m.); Amtrak ANA 191,153 passengers (2024); Metrolink OC Line 5,116 weekday riders; 20M people within 90 miles | OCTA; Amtrak (RPA); Metrolink; CoStar |
| Visit CA / 2026-ADT | The PDF is OCTA's traffic map, not Visit California data. Visit California 2025 statewide totals were added for the California impact | 2026-ADT.pdf; Visit California (via RCRC) |
| District 5 / new markets | 85.8% overnight; 44% out of state; Datafy 5.2%. Fly-in markets by Visa spending: Seattle, Phoenix, Las Vegas, Orlando, NY; internationally Mexico, Canada, Japan | Azira; Datafy; Visa |
| Hotel market | CoStar Disneyland submarket 78.4%, $255; Anaheim submarket $130. STR Anaheim+ 77.9%, $241; group share 18.2% | CoStar; STR |
| LARC / inflation | Q2 RevPAR +11.4%; Anaheim CPI about 3.2% a year | LARC 2026 |

## OC Vibe impact model (impact.py, ocv_content.py)
- **Scope:** visitors only, full operation, 2025 dollars.
- **Formula:** new spending = net-new visitors × $258 + extra visitor days × $118.71.
- **Ratios applied:**
  - Anaheim (TE 2025): 1.53 total impact per $1, 9.9 jobs per $1M, 14.2% state and local taxes.
  - Orange County (TE 2025): 1.70 total impact per $1.
  - California: Visit California ratios applied to the 44% out-of-state share.
- **Base case:**
  - 150 concert-hall events at 80% fill (5,613 seats).
  - 150 theater/club events at 70% fill (2,300 seats).
  - 25% of attendees are net-new visitors.
  - 1% of visitors add a day.
  - Hotels: 550 rooms at 74% occupancy and $218.
- **Results (conservative / base / optimistic):**
  - New visitor spending: $36.3M / $90.5M / $187.4M.
  - Anaheim economic impact: $55M / $138M / $286M.
  - Anaheim jobs: 360 / 900 / 1,860.
  - Hotel room nights: 141K / 149K / 157K.
  - TOT: $4.6M / $4.9M / $6.0M.
  - California new spending: $16M / $40M / $82M.
- **Published comparisons** (whole district, not like-for-like):
  - OCVIBE fact sheet (2024): 3,000+ jobs; about $10M a year in tax revenue to Anaheim.
  - DTA (2020): more than $400M a year in recurring impact; 3,300 jobs.

## Three views of impact (base case, 2025 dollars)
| | Spending | Total impact | Jobs |
|---|---|---|---|
| 1 Anaheim today (TE 2025, measured) | $6.83B | $10.42B | 67,817 |
| 2 Anaheim with OC Vibe live (estimate) | $6.92B (90% sim. range $6.90B–$6.95B) | $10.56B | 68,720 |
| 3a OC Vibe area today (associated) | $355M | $542M | 3,530 |
| 3b OC Vibe when live (associated) | $446M (range $410M–$492M) | $680M | 4,420 |

Notes on the views:
- 3a uses Datafy's 5.2% share of Anaheim visitor days and includes all spending on those days.
- When OC Vibe is live, its share rises to 6.4%.

## Validation (computation audit)
- Suite: checks/validate_ocvibe.py, run Oct. 12, 2026 through the provenance runner.
- Manifest: computations/validation-010/manifest.json (valid; Oct. 12, 2026; INTERNAL ONLY, not shown in the customer report). 42 of 42 checks passed, including: 226 numbers in the report text trace to its tables and data notes; the transit snapshots reconcile; and the concert hall capacity sensitivity.
- Result: 38 of 38 checks passed. The suite covered:
  - exact-rational recomputation of 54 outputs (max difference 3.7e-16);
  - invariants and cross-source reconciliation;
  - statistical tests: STR gap 15.7 pts, bootstrap CI 12.5–18.6, Welch p 1e-22; CoStar sign tests p = 0.004; TE trend PI;
  - Monte Carlo with 200K draws, seed-stable within 0.14%;
  - sensitivity (add-a-day share 40% and net-new share 39% of variance);
  - benchmarks.
- New spending simulation: 5th–95th percentile $71M–$122M, median $95M.
- Fixed during the audit:
  - "277 weekday departures" was relabeled "277 weekday bus trips stopping at ARTIC" (227 depart, 50 end there).
  - The after-10 p.m. figure is now 11 departures (16 trips stop).
  - Route 50's ride to the resort is 14 minutes (was 13).

## Data quality notes
- Concert hall capacity: OCVIBE's newest release (Mar. 12, 2026) says 5,000 seats; the model uses the City's 5,613. At 5,000 seats the base estimate is $85.7M instead of $90.5M, still inside the simulation range. Confirm with OC Vibe.
- California transit systems snapshots (2003–2017):
  - Snapshots 3 and 4 were duplicates.
  - Laguna Beach has outliers: 1,647 employees in 2006 and 0 passengers in 2013.
  - "Other" passengers by mode are 0 in 2007 and 2010.
  - Demand-response passengers in 2010 differ by file.
  - Dollars are nominal.
- The five transportation files re-sent on Oct. 12 (ana.pdf, the Metrolink fact sheet, 2026-ADT 3, Demographics and the Economy, TET metadata) were identical to earlier uploads and were already in use.
- Extra Night deck: shows "$9.9B"; the calculation gives $9.98B.
- LARC: uses two bases.
- CoStar text and tables differ ($250 vs. $255 ADR; $218.1M vs. $234.2M in sales). The CoStar monthly export matches the PDFs' 12-month figures.
- OC Vibe cost and timeline differ by source:
  - CoStar: $4B, 2028.
  - LARC: $5B, 2033.
  - City: $4B, through about 2030.
  - visitanaheim.org: 5,700 seats and 865K sq ft of office.
- Visa: the geography of the "Visitor Type" view needs confirmation; the two Visitor Type files are identical.
- Amtrak: the 2023 figure (70.7K) is anomalous.
- Metrolink: line totals only, not ARTIC boardings.
- STR vs. CoStar: different hotel sets; do not compare directly.

## Open items
- Confirm the concert hall capacity (5,000 vs. 5,613) with OC Vibe, then rerun the model.
- The California transit data ends in 2017; newer years would show post-pandemic ridership.
- OC Vibe staff need edit access to save figures in the dashboard. Outside-organization viewers can write only when invited by email as Editors while the page is not shared by link; otherwise they use Download.
- The OC Vibe impact estimate needs OC Vibe's event calendar, ticketing origin data and hotel plans.
- Confirm California 2025 figures against Visit California's primary report.
- TE transportation impact data has not yet been received.
- Approval is needed before external distribution:
  - TE 2025 EI is a draft.
  - LARC requires consent.
  - CoStar, STR and Visa are licensed data.

## Build files
- Dashboard: data.py + newdata.py → impact.py → content.py (+ ocv_content.py, new_content.py, views_valid.py, logic_content.py, roles_content.py) → build.py (HTML; app.js includes the calculator).
- Deck: export_deck.py → deck_data.json → deck.js (deck_head.js + deck_body.js).

## Activity log (newest first)
2026-10-13 5:40 PM PT | John Picou | Added PowerPoint as an export format (dashboard v19). Export > PowerPoint gives the title slide plus the slides for the chosen sections, built in the browser from the full 94-slide deck (pptx_subset.js with inlined JSZip 3.10.1); all sections returns the full deck. Tested current-section (10 slides), Overview + Visitor spending (12) and all (94): each passes the pptx validator and opens in LibreOffice. Skill: /visit-anaheim-powerpoint-generator conventions (deck unchanged).
2026-10-13 4:55 PM PT | John Picou | Layout and infographics (dashboard v18, deck 94 slides). Full-width headlines and deks; sections now stack full width (lede, why it matters, at a glance, by the numbers, calculation, details) with flexible stat strips; overview release in three newspaper columns with a horizontal By the numbers strip and full-width chart; checked at 1920, 1440, 1024, 768 and 390 px with no overflow. Added "At a glance" data infographics to every news report (economy chain, District 5 waffles, itemized visitor receipt with every-$1 bar, jobs pictogram, hotel night towers, hotel supply and day/overnight share bars, ARTIC departures board, impressions-to-visits funnel, Anaheim vs. U.S. bars), all from existing section figures with sources and calculations; count-up and grow animations on entrance, off under reduced motion and in print. Deck: one native-shape infographic slide per section. Validation-012: 50/50 (adds infographic sourcing and receipt sum checks). VA Branded: added page layout rules and data infographic rules to Data, charts and tables and a DataInfographics component (pending design-team review). Added docs/quarterly-refresh.md runbook. Skills: /va-data-visualization, /visit-anaheim. Data: unchanged, through Sept. 2026.
2026-10-13 4:10 PM PT | John Picou | Newsroom revision (dashboard v17, deck 85 slides). Each section is now a broadsheet news report (kicker, headline, dateline + lede, "Why it matters" nut graph, calculation, By the numbers, six announcement-style detail cards with figure, label, detail and dated source) followed by a labeled Analysis band; no opinion pieces (John's choice). Sections reordered for reading flow (today, who visits, spending, jobs, hotels, one more night, getting here, marketing, outlook, appendix) with an Up next bridge at the end of each; sticky-nav scroll offset and hashchange navigation fixed. Removed the "Enter OC Vibe's own figures" calculator (holistic Anaheim view). House style: no em dashes anywhere (0 remain). Appendix: 8 newsroom terms and 1 method added (26 terms, 9 methods). Deck: news report and details slides per section, Analysis kickers, a "How this report reads" slide, appendix W5H slides removed. Validation-011: 48/48 (adds newsroom structure, no em dash, AP dates, no first person, reading order). VA Branded design system (org-shared): added "Data reporting: newspaper styles" to the BI-owned Data, charts and tables section, NewsReport and DetailCards components (pending design-team review) and a Report narrative row; em-dash rule flagged for Marketing review. Skills: /va-data-visualization, /visit-anaheim. Data: unchanged, through Sept. 2026.
2026-10-13 3:45 PM PT | John Picou | John force-pushed main (b6a391c) to GitHub bi-visitanaheim/oc-vibe-insights; Vercel deployed it to https://oc-vibe-insights.vercel.app (public). Verified live: page loads with no script errors, 150 value tooltips, no sideways scroll at 375 px, deck download 200 (676,907 bytes), robots.txt and noindex/X-Frame-Options headers applied, source folders (pipeline/, README) not served. Calculator shows Download-only mode as designed.
2026-10-13 3:35 PM PT | John Picou | Checked the new GitHub repo and Vercel project. Found: the GitHub repo bi-visitanaheim/oc-vibe-insights holds only README.md (2 commits) and is public; the Vercel production deployment (ece1bb8) serves 404 on every path; on the Hobby plan, Standard Protection locks deployment URLs but oc-vibe-insights.vercel.app is public. John chose to keep both the repo and the site public. Updated the README to match (repository and website public; licensed CoStar and STR exports stay excluded by .gitignore), committed locally (b6a391c) and set the origin remote. Open: John to force-push main from his Mac so Vercel deploys the app.
2026-10-13 3:12 PM PT | John Picou | Packaged the entire OC Vibe Insights app as a Git repository (oc-vibe-insights, branch main, 1 commit, 96 tracked files) for GitHub and Vercel: pipeline, data, deck, README, validation, and a public/ static site with vercel.json. Paths made repo-relative; rebuilt in the repo with identical page content and a valid 70-slide deck; validation re-run 43/43. Licensed CoStar and STR raw exports excluded from Git. Repo placed in the BI OneDrive folder "Business Intelligence-Apps - OC Vibe". Open: publish to GitHub (bi-visitanaheim, private), then link the Vercel project with Vercel Authentication. Skill: /va-org-routing-approval (no routing needed; John oversees IT/BI).
2026-10-13 2:59 PM PT | John Picou | Created README.md for the OC Vibe Insights app covering purpose, reporting rules, sections, features, sources, rebuild steps, data notes, approvals and open items. Saved to the project as "OC Vibe Insights - README".
2026-10-13 2:55 PM PT | John Picou | Dashboard v16: hovering over or tabbing to any chart mark now shows its value in a tooltip and highlights it while dimming the other marks. Covers bars, columns, line points, the heatmap, the overview bars and the range and waterfall charts. The deck already labels every chart value. Skill: /va-data-visualization.
2026-10-13 2:46 PM PT | John Picou | Facts-only revision of the deck (70 slides) and dashboard (v15), per John's direction.
  - Removed the Visit Anaheim BI scenario model from both: the $90.5M estimate, net-new and add-a-day assumptions, event counts, OC Vibe hotel occupancy, parking and vehicle estimates, ten-year totals and the simulation range.
  - Tourism Economics city totals are no longer allocated to OC Vibe.
  - The OC Vibe section is now "Anaheim and OC Vibe today": 2025 measured results (published 2026) shown beside TE's 2026 forecast (27.0M visitors, $7.2B), plus the OC Vibe area's measured figures (Datafy 5.2%, Azira District 5), measures with baselines, and figures published by OCVIBE and DTA.
  - Old slide 13 is now slide 8, rebased on Anaheim's actual 2025 spending by category: recreation $2,321M, lodging $1,724M, retail $1,495M, F&B $1,067M, transportation $224M.
  - The staff calculator now starts blank and uses only the figures OC Vibe enters; the BI base case and the California share were removed.
  - Kept: Visit Anaheim's Extra Night study and the per-1% and per-occupancy-point sensitivities, which are arithmetic on source data.
  - Internal validation: 43/43 passed (validation-010), including a check that no estimate wording remains.
  - Skills: /bi-analytics-expert, /va-data-visualization, /visit-anaheim-powerpoint-generator, /mathbox:computation-audit.
2026-10-12 4:18 PM PT | John Picou | Added calculation breakdowns across the dashboard (v14) and deck (74 slides).
  - Every calculated number now shows its breakdown. Each section's key insight has a "How the key insight is calculated" step table; OC Vibe items, compare-and-contrast rows, KPI cards, summary findings and the main announcement carry a Calculation line; and the OC Vibe impact tables gained a "How it's calculated" column.
  - The $90.5M is broken down as: $59.0M from 228,765 net-new visitors × $258, plus $31.5M from 265,000 extra visitor days × $118.71. The range ($71M–$122M) is the 5th–95th percentile of 200,000 simulations.
  - Corrected the growth claim from "+3.9% vs. +1.3%" to computed values: visitor spending +4.1% a year vs. visits +1.4% (2025–2028), and +2.6% a year per visitor.
  - Added featured BI charts: a waterfall of the $90.5M, a simulation range chart, a transit riders line (2003–2017), a convention pace line, a 2026 hotel occupancy heatmap, D5 visits by day, and the add-a-day scenarios.
  - KPI cards now follow the VA Branded KpiCard style, with entrance-only motion (fade and 12px rise, off under reduced motion).
  - Deck additions: a waterfall slide, step-by-step calculation slides, and native line charts.
  - Validation is internal only: 42/42 checks passed (validation-008).
  - Skills: /va-data-visualization, /bi-pulse-dashboard, /bi-analytics-expert, /mathbox:computation-audit.
2026-10-12 3:40 PM PT | John Picou | Cleaned up the dashboard (v13) and deck (63 slides). The overview is now the main announcement and every section reads like an article with key insight, source and date, the 5W+H details, What it means for OC Vibe as a whole (what it enhances and what OC Vibe needs, by topic), compare and contrast with explanations, and collapsed extra data. Removed the role views and the Checks and confidence page (validation stays internal, 42/42, validation-006). Added the 2026 hotel calendar (STR), OC Vibe public sources, and the estimate range and drivers. Skills: /bi-pulse-dashboard, /bi-analytics-expert, /va-data-visualization, /mathbox:computation-audit.
2026-10-12 3:22 PM PT | John Picou | Added role views for the OC Vibe team (dashboard v12, deck 64 slides). Researched OC Vibe's public descriptions of its teams; no individuals are named. Added Orange County transit staff, expenses, revenues, passengers and vehicles for 2003–2017 (California's transit systems data snapshots). Flagged the concert hall capacity difference. Validation: 42/42 checks passed (validation-004). Skills: /bi-analytics-expert, /bi-pulse-dashboard, /va-data-visualization, /data-quality-audit, /mathbox:computation-audit.
2026-10-12 3:02 PM PT | John Picou | Applied the BI logic across the dashboard (v11) and deck (49 slides): essentials (who, what, when, where, why, how) on every section; source and date on every finding, card, takeaway and summary stat; compare and contrast with a solution for each point; solutions added to risk notes; recommendations table; new Appendix (19 formulas, 30 glossary terms, 10 methods). Removed the summary highlight picker and internal warnings so the summary shows measured facts only. Re-ran validation (38/38). Skills: /bi-pulse-dashboard, /bi-analytics-expert, /va-data-visualization, /mathbox:computation-audit.
2026-10-12 2:44 PM PT | John Picou | Bolded key metrics in teal across the dashboard (short answers, OC Vibe boxes, notes, takeaways, recommendations, BI Pulse summary, card captions) and the deck (bullets, callouts, insight table). Added a key-number callout beside each section's short answer (v10). Skills: /va-data-visualization, /bi-pulse-dashboard.
2026-10-12 2:31 PM PT | John Picou | Added the three views of impact (Anaheim today, Anaheim with OC Vibe, OC Vibe's own today and when live) and a "Checks and confidence" section. Ran a computation audit with statistical validation (38/38 checks passed) and corrected the ARTIC bus wording. Updated the calculator and expanded the deck to 37 slides. Skills: /mathbox:computation-audit, /bi-analytics-expert, /bi-pulse-dashboard.
2026-10-12 2:09 PM PT | John Picou | Changes to the dashboard (v8):
  - Added STR daily data (VA hotel sets, Jan.–Oct. 3, 2026), CoStar monthly submarkets (Jan.–Aug. 2026), Visa Destination Insights (Aug. 2026), Amtrak ANA (2018–2024) and Metrolink (FY26 Q2).
  - Added the OC Vibe staff input calculator with shared saves, a single Copy button, and a dated, vetted source register.
  - Expanded the deck to 33 slides.
  - Skills: /bi-analytics-expert, /bi-pulse-dashboard, /va-data-visualization, /data-quality-audit.
2026-10-12 1:38 PM PT | John Picou | Added the OC Vibe impact scenarios, KPI framework, risks, "What this means for OC Vibe" boxes, selected-tab highlighting and section-choice export (v6); deck 25 slides.
2026-10-12 1:25 PM PT | John Picou | Added the CoStar hotel market section (v3); deck 20 slides.
2026-10-12 1:15 PM PT | John Picou | Republished as the OC Vibe edition; deck 17 slides.
2026-10-12 12:28 PM PT | John Picou | Created the OC Vibe Insights dashboard and 12-slide PowerPoint.
