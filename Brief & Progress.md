# Auditor Performance and Salary Analysis - Brief & Progress

Project Overview

An internal tool for the GP Audit Team to calculate auditor performance and generate salary reports by merging specialized audit data with MFS payment details.

## Technology Stack

- **Framework**: Streamlit (Python)
- **Data Handling**: Pandas

## Current Progress & Features

- [X] **File Uploads**: Supports CSV/XLSX for Audit data and CSV for MFS data.
- [X] **Sl Column**: Sequential serial numbers added as the first column.
- [X] **75/25 Salary Logic**: Implemented complex calculation:
    - **Fixed (75%)**: 75% of Max Payable.
    - **Variable (25%)**: 25% of Max Payable, reduced by Mismatch %.
    - **Actual Payable**: Sum of Fixed + Variable.
- [X] **Interactive Table**: Switched from HTML to `st.dataframe` for cell selection, sorting, and resizing.
- [X] **Performance Cleaning**: Mismatches are now correctly filtered only for re-audited visits.
- [X] **Clean UI**: Round figures for payments and percentages (e.g., 54% instead of 53.6%).

## Technical Context for Agents
- **Main App**: `app.py` is the only active file (Streamlit).
- **MFS Data Header**: The MFS CSV has 2 blank/title rows; must be read with `header=2`.
- **Merging**: Join key between Audit and MFS data is `Auditor Name` (from MFS) and `assigned_to` (from Audit).
- **Calculation Chain**: `Audited Visit` -> `Max Payable` -> `Fixed/Variable` -> `Actual Payable`.
- **Frontend Formatting**: `st.dataframe` height is set to 600px; columns are formatted as strings to remove `.0` and maintain leading zeros in MFS numbers.

## Rules of Thumb & Preferences
- **Conciseness**: The user prefers direct action over long explanations.
- **UI First**: Visual layout is prioritized (Full header names preferred over compact ones).
- **Interactivity**: User prefers `st.dataframe` for selectability over static HTML.
- **Rounding**: Use `round()` for display logic on the frontend.

## Next Steps / Future Enhancements

- Interactive sorting and filtering via `st.dataframe`.
- Sidebar inputs for dynamic `Unit Price` adjustments.
- Excel export functionality for payroll processing.
- Multi-region or date-based filtering.

---

*Created on: 2026-01-13*
