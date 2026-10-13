# Licensed raw exports (not in Git)

This folder holds licensed raw data exports that the pipeline reads. They are excluded from the repository by `.gitignore` and stay on Visit Anaheim storage (the BI OneDrive folder "Business Intelligence-Apps - OC Vibe").

| File | Source | Period | Read by |
|---|---|---|---|
| `STR_Daily_Data_8.xlsx` | STR daily data, Visit Anaheim hotel sets | Jan. 1–Oct. 3, 2026 | `newdata.py`, `ocv_whole.py` |
| `CoStar_DataExport_17.xlsx` | CoStar export | Through Aug. 2026 | `newdata.py` |

Put both files here before rebuilding. Share summaries outside Visit Anaheim, not these raw exports.
