# Licensed raw exports (not in Git)

This folder holds licensed raw data exports that the pipeline reads. They are excluded from the repository by `.gitignore` and stay on Visit Anaheim storage (the BI OneDrive folder "Business Intelligence-Apps - OCVIBE").

| File | Source | Period | Read by |
|---|---|---|---|
| `STR_Daily_Data_8.xlsx` | STR daily data, Visit Anaheim hotel sets | Jan. 1–Oct. 3, 2026 | `newdata.py`, `ocv_whole.py` |
| `CoStar_DataExport_17.xlsx` | CoStar export | Through Aug. 2026 | `newdata.py` |
| `CoStar_OC_Monthly_DataTable_26.xlsx` | CoStar, Orange County market: inventory, occupancy, ADR, RevPAR (monthly) | Jan. 1987–Sept. 2026 (forecast to Mar. 2028) | OC Tourism Statistics answers (Oct. 19, 2026) |
| `CoStar_OC_Monthly_Segmentation_DataTable_27.xlsx` | CoStar, Orange County market: transient, group, contract (monthly) | Jan. 1987–Sept. 2026 | OC Tourism Statistics answers |
| `CoStar_OC_Daily_DataTable_28.xlsx` | CoStar, Orange County market (daily) | Oct. 10, 2024–Oct. 10, 2026 | Not yet used |
| `CoStar_OC_Daily_Segmentation_DataTable_29.xlsx` | CoStar, Orange County market segmentation (daily) | Oct. 10, 2024–Oct. 10, 2026 | Not yet used |

Put both files here before rebuilding. Share summaries outside Visit Anaheim, not these raw exports.
