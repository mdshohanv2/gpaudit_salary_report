# Auditor Performance and Salary Analysis - Brief & Progress

Project Overview

An internal tool for the GP Audit Team to calculate auditor performance and generate salary reports by merging specialized audit data with MFS payment details.

## Technology Stack

- **Framework**: Streamlit (Python)
- **Data Handling**: Pandas, OpenPyXL (for Excel Formatting)

## Current Progress & Features

- [x] **File Uploads**: Supports CSV/XLSX for Audit data and CSV for MFS data.
- [x] **Dynamic Column Mapping**: Users can map their file columns (Auditor, Visit ID, Re-Audit, Mismatch) manually with auto-detection for `assigned_to`, `visit_id`, etc.
- [x] **Automated Header Extraction**: Automatically identifies the report month and visit date range from the data.
- [x] **Live Salary Logic**: Sidebar input for **Unit Price (BDT)** with real-time updates to 75/25 calculation.
- [x] **Interactive Table**: Styled `st.dataframe` with custom header display for web view.
- [x] **Premium Excel Export**: 
    - [x] High-fidelity styling matching user requirements (Blue headers, nested titles).
    - [x] **Visual Excellence**: Highlighted "Actual Payable" column (Yellow) and full grid borders.
    - [x] **Live Formulas**: Exported `.xlsx` contains functional formulas (`SUM`, `ROUND`, etc.) for post-download adjustments.
    - [x] **Whole Numbers**: All salary calculations are rounded to 0 decimal places inside Excel.
- [x] **Clean UI**: Sidebar mapping guide and auto-formatting for MFS numbers (leading zeros).

## Technical Context for Agents
- **Main App**: `app.py` handles the entire pipeline (Upload -> Map -> Process -> Export).
- **MFS Data Header**: The MFS CSV has 2 blank/title rows; must be read with `header=2`.
- **Excel Logic**: Uses `openpyxl` to inject formula strings into cells rather than static values.
- **Auto-Detection**: The `find_col` function prioritizes standard GP headers but fallbacks to keyword search.

## Rules of Thumb & Preferences
- **Conciseness**: The user prefers direct action over long explanations.
- **High-Fidelity Excel**: The exported file must look exactly like the reference image (colors, merging, borders).
- **Interactivity**: Preference for `st.dataframe` on web and `ROUND` formulas in Excel.
- **Rounding**: All payments must be round figures for payroll.

## Next Steps / Future Enhancements

- [x] Interactive sorting and filtering via `st.dataframe`.
- [x] Sidebar inputs for dynamic `Unit Price` adjustments.
- [x] Excel export functionality with live formulas.
- [ ] Multi-region or date-based filtering.
- [ ] Email automation for salary slip distribution.

---

*Updated on: 2026-01-13*
